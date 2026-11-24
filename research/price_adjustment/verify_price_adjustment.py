"""DeepSearch 주가(시장데이터)의 수정주가 여부 검증.

확인하는 것
1. 옵션: GetStockPrices 에 원주가/수정주가를 고르는 파라미터나 컬럼이 있는가
2. 분할 사례: 시가·종가는 수정되고 거래량·주식수·시가총액은 원래 값인가, 수정계수는 명목 분할비율과 같은가
3. 수정 대상: 배당·무상증자·유상증자 권리락도 수정하는가 (일별 수정계수의 변경점)
4. 자연어 쿼리: GetStockPrices 와 같은 값인가, 과거 날짜를 어디까지 받는가

수정계수 = 원주가 / close, 원주가 = market_cap / shares_outstanding (시가총액은 원주가 × 원주식수로 저장돼 있음)

출력 (data/)
- param_probe.csv          : 파라미터·컬럼 이름별 HTTP 상태
- split_cases.csv          : 분할 전후 일별 값 + 원주가·수정계수
- factor_changepoints.csv  : 수정계수가 0.1% 넘게 바뀐 날만
- nl_vs_func.csv           : 같은 기간 자연어 쿼리 vs GetStockPrices 값 비교
- nl_date_probe.csv        : 자연어 쿼리 날짜 범위별 실제 반환 범위

사용: python research/price_adjustment/verify_price_adjustment.py [기준일 YYYY-MM-DD]
      기준일 기본값 2026-11-24 (검증일 2026-11-25 직전 거래일). 키는 레포 루트 .env 의 API_KEY.
      원시 응답은 data/cache/ 에 캐시되므로 다시 돌리면 API를 부르지 않는다.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = HERE / "data"
CACHE = DATA / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

ASOF = sys.argv[1] if len(sys.argv) > 1 else "2026-11-24"
FACTOR_FROM = "2018-01-01"

# (이름, 종목코드, 조회 시작, 조회 끝, 명목 분할비율)
SPLITS = [
    ("삼성전자", "005930", "2018-04-25", "2018-05-08", 50),
    ("NAVER", "035420", "2018-10-01", "2018-10-16", 5),
    ("카카오", "035720", "2021-04-07", "2021-04-19", 5),
]
# 삼성전자: 배당만 있는 대조군 / 유한양행: 매년 무상증자 + 2020 분할 / 대한항공: 2020·2021 유상증자
FACTOR_STOCKS = [("삼성전자", "005930"), ("유한양행", "000100"), ("대한항공", "003490")]
PRICE_COLS = ["open", "high", "low", "close", "volume", "value",
              "shares_outstanding", "market_cap", "trading_halted"]
NL_DATE_RANGES = ["2018-04-25-2018-05-08", "2019-06-03-2019-06-07", "2019-12-02-2019-12-06",
                  "2019-12-23-2020-01-10", "2020-01-02-2020-01-08", "2021-06-03-2021-06-07",
                  "2024-06-03-2024-06-07"]


# ------------------------------------------------------------------ API
def _api_key() -> str:
    k = os.environ.get("API_KEY")
    if not k and (REPO / ".env").exists():
        for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("API_KEY") and "=" in line:
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        raise SystemExit("API_KEY 가 환경변수나 .env 에 없습니다.")
    return base64.b64encode(k.encode()).decode() if ":" in k else k


def ds(query: str) -> dict:
    """compute 호출 → {'status': HTTP 상태, 'columns': [...], 'data': {col: [...]}}

    4xx 는 재시도하지 않고 결과로 돌려준다 (모르는 파라미터·컬럼이면 400).
    """
    p = CACHE / (hashlib.sha1(query.encode()).hexdigest() + ".json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    last = None
    for i in range(4):
        try:
            r = requests.get("https://api.deepsearch.com/v1/compute?input=" + quote(query, safe=""),
                             headers={"Authorization": "Basic " + _api_key()},
                             timeout=180)
            if 400 <= r.status_code < 500:
                out = {"query": query, "status": r.status_code, "columns": [], "data": {}}
                p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
                return out
            r.raise_for_status()
            j = r.json()
            break
        except Exception as e:  # 네트워크/일시 오류
            last = e
            time.sleep(3 * (i + 1))
    else:
        raise RuntimeError(f"요청 실패: {query}: {last}")
    pods = (j.get("data") or {}).get("pods") or []
    out = {"query": query, "status": 200, "columns": [], "data": {}}
    for pod in pods:
        c = pod.get("content") or {}
        if str(pod.get("class", "")).startswith("Result") and not out["columns"]:
            out["columns"] = c.get("columns") or []
            out["data"] = c.get("data") or {}
    p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def frame(res: dict) -> pd.DataFrame:
    df = pd.DataFrame({k: res["data"].get(k, []) for k in res["columns"]})
    if "date" in df:
        df["date"] = df["date"].astype(str).str[:10]
    return df


def stock_prices(code: str, cols: list[str], date_from: str, date_to: str) -> pd.DataFrame:
    cs = ", ".join(f'"{c}"' for c in cols)
    return frame(ds(f"GetStockPrices(KRX:{code}, columns=[{cs}], date_from={date_from}, date_to={date_to})"))


def add_factor(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["raw_close"] = df["market_cap"] / df["shares_outstanding"]
    df["factor"] = df["raw_close"] / df["close"]
    return df


# -------------------------------------------------------------- 1. 옵션
def param_probe() -> pd.DataFrame:
    base = "GetStockPrices(KRX:005930, columns={c}, date_from=2018-04-26, date_to=2018-04-26{p})"
    cases = [("기본 호출", '["close"]', ""),
             ("대조군: 없는 파라미터 foo=1", '["close"]', ", foo=1"),
             ("adjusted=False", '["close"]', ", adjusted=False"),
             ("adjusted=True", '["close"]', ", adjusted=True"),
             ("adjust=False", '["close"]', ", adjust=False"),
             ("raw=True", '["close"]', ", raw=True"),
             ('price_type="raw"', '["close"]', ', price_type="raw"')]
    cases += [(f"컬럼 {c}", f'["{c}"]', "") for c in
              ["adj_close", "raw_close", "adjusted_close", "수정종가", "원주가"]]
    rows = []
    for label, cols, extra in cases:
        r = ds(base.format(c=cols, p=extra))
        df = frame(r)
        val = df.iloc[0, -1] if len(df) else None
        rows.append({"case": label, "status": r["status"], "value": val, "query": r["query"]})
    return pd.DataFrame(rows)


# ------------------------------------------------------------ 2. 분할 사례
def split_cases() -> pd.DataFrame:
    out = []
    for name, code, d0, d1, ratio in SPLITS:
        df = add_factor(stock_prices(code, PRICE_COLS, d0, d1))
        df.insert(0, "name", name)
        df["nominal_ratio"] = ratio
        out.append(df)
    return pd.concat(out, ignore_index=True)


# ------------------------------------------------------ 3. 수정계수 변경점
def factor_changepoints() -> pd.DataFrame:
    out = []
    for name, code in FACTOR_STOCKS:
        df = add_factor(stock_prices(code, ["close", "shares_outstanding", "market_cap"], FACTOR_FROM, ASOF))
        df = df.dropna(subset=["factor"])
        prev = df["factor"].shift()
        cp = df[prev.isna() | ((df["factor"] / prev - 1).abs() > 0.001)].copy()
        cp["factor_change"] = (cp["factor"] / prev[cp.index]).round(5)
        cp.insert(0, "name", name)
        out.append(cp)
    return pd.concat(out, ignore_index=True)


# ------------------------------------------------------------ 4. 자연어
def nl_vs_func() -> pd.DataFrame:
    name, code, d0, d1 = "카카오", "035720", "2021-04-07", "2021-04-19"
    nl = frame(ds(f"{name} 시가 종가 거래량 거래대금 시가총액 {d0}-{d1}"))
    nl.columns = [c.split(" ")[0] for c in nl.columns]
    fn = stock_prices(code, ["open", "close", "volume", "value", "market_cap"], d0, d1)
    m = fn.merge(nl, on="date", how="outer")
    pairs = {"open": "시가", "close": "종가", "volume": "거래량", "value": "거래대금", "market_cap": "시가총액"}
    for f, k in pairs.items():
        m[f"{f}_same"] = (m[f].astype(float) == m[k].astype(float))
    return m


def nl_date_probe() -> pd.DataFrame:
    rows = []
    for rng in NL_DATE_RANGES:
        df = frame(ds(f"삼성전자 종가 {rng}"))
        rows.append({"requested": rng, "rows": len(df),
                     "first_date": df["date"].iloc[0] if len(df) else None,
                     "last_date": df["date"].iloc[-1] if len(df) else None,
                     "first_close": df.iloc[0, -1] if len(df) else None})
    return pd.DataFrame(rows)


def main():
    pp = param_probe()
    pp.to_csv(DATA / "param_probe.csv", index=False, encoding="utf-8-sig")
    print("[1] 파라미터·컬럼 이름별 상태\n", pp[["case", "status", "value"]].to_string(index=False), "\n")

    sc = split_cases()
    sc.to_csv(DATA / "split_cases.csv", index=False, encoding="utf-8-sig")
    print("[2] 분할 사례\n", sc[["name", "date", "close", "volume", "shares_outstanding",
                               "raw_close", "factor", "nominal_ratio"]].round(5).to_string(index=False), "\n")

    fc = factor_changepoints()
    fc.to_csv(DATA / "factor_changepoints.csv", index=False, encoding="utf-8-sig")
    print("[3] 수정계수 변경점\n", fc[["name", "date", "close", "raw_close", "factor", "factor_change"]]
          .round(5).to_string(index=False), "\n")

    nv = nl_vs_func()
    nv.to_csv(DATA / "nl_vs_func.csv", index=False, encoding="utf-8-sig")
    same = nv[[c for c in nv.columns if c.endswith("_same")]].all()
    print("[4a] 자연어 vs GetStockPrices 일치 여부\n", same.to_string(), "\n")

    nd = nl_date_probe()
    nd.to_csv(DATA / "nl_date_probe.csv", index=False, encoding="utf-8-sig")
    print("[4b] 자연어 날짜 범위\n", nd.to_string(index=False))


if __name__ == "__main__":
    main()
