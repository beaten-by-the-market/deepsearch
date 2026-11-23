"""DeepSearch 시장데이터 PBR/BPS 정의 검증.

확인하는 것
1. 키워드 옵션: '별도', '지배주주', '연결', '분기', '보통주'를 붙여도 값이 바뀌는가
2. 갱신 시점: BPS/EPS가 언제 바뀌는가 (일별 시계열의 변경점)
3. 정의: 시장데이터 BPS를 재무제표 계정으로 역산하면 어떤 정의와 일치하는가
4. 다른 경로: GetCompanyDividends '주당순자산(원)', 컨센서스 csd_bps

출력 (data/)
- keyword_variants.csv       : 쿼리별 PBR/BPS 값
- bps_eps_changepoints.csv   : BPS 또는 EPS가 바뀐 날만
- bps_definition_check.csv   : 정의별 BPS 계산값 vs 시장데이터 BPS
- dividends_bps.csv          : GetCompanyDividends 의 주당순자산/주당순이익
- consensus_bps.csv          : SearchFirmFundamentalsForecasts 의 csd_bps/csd_pbr

사용: python research/pbr_bps/verify_pbr_bps.py [기준일 YYYY-MM-DD]
      기준일 기본값 2026-11-20 (검증일). 키는 레포 루트 .env 의 API_KEY.
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

requests.packages.urllib3.disable_warnings()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = HERE / "data"
CACHE = DATA / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

ASOF = sys.argv[1] if len(sys.argv) > 1 else "2026-11-20"
COMPANIES = ["삼성전자", "SK하이닉스", "현대차"]
SERIES_FROM = "2023-01-01"

# GetFinancialStatements 계정 (report_id, account_id)
ACC = {
    "지배기업소유주지분": ("11", "8050"),
    "자본총계": ("11", "8900"),
    "보통주발행주식수": ("11", "8111"),
    "우선주발행주식수": ("11", "8121"),
    "보통주자기주식수": ("11", "8431"),
    "우선주자기주식수": ("11", "8432"),
    "기본주당이익": ("12", "9009"),
}


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
    """compute 호출 → {'tagged': 해석결과, 'columns': [...], 'data': {col: [...]}}"""
    p = CACHE / (hashlib.sha1(query.encode()).hexdigest() + ".json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    last = None
    for i in range(4):
        try:
            r = requests.get("https://api.deepsearch.com/v1/compute?input=" + quote(query, safe=""),
                             headers={"Authorization": "Basic " + _api_key()},
                             verify=False, timeout=180)
            r.raise_for_status()
            j = r.json()
            break
        except Exception as e:  # 네트워크/일시 오류
            last = e
            time.sleep(3 * (i + 1))
    else:
        raise RuntimeError(f"요청 실패: {query}: {last}")
    pods = (j.get("data") or {}).get("pods") or []
    out = {"query": query, "tagged": None, "columns": [], "data": {}}
    for pod in pods:
        c = pod.get("content") or {}
        if pod.get("class") == "Input":
            out["tagged"] = (c.get("interpretation") or {}).get("tagged")
        elif str(pod.get("class", "")).startswith("Result") and not out["columns"]:
            out["columns"] = c.get("columns") or []
            out["data"] = c.get("data") or {}
    p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def frame(res: dict) -> pd.DataFrame:
    return pd.DataFrame({k: res["data"].get(k, []) for k in res["columns"]})


# -------------------------------------------------------------- 1. 키워드
def keyword_variants() -> pd.DataFrame:
    queries = ["삼성전자 PBR", "삼성전자 별도 PBR", "삼성전자 지배주주 PBR",
               "삼성전자 BPS", "삼성전자 연결 BPS", "삼성전자 분기 BPS",
               "삼성전자 보통주 BPS", "삼성전자 주당순자산가치"]
    rows = []
    for q in queries:
        r = ds(q)
        df = frame(r)
        val_col = [c for c in df.columns if c not in ("date", "symbol", "entity_name")][0]
        rows.append({"query": q, "interpretation": r["tagged"], "column": val_col,
                     "value": df[val_col].iloc[-1], "date": str(df.get("date", pd.Series([None])).iloc[-1])[:10]})
    return pd.DataFrame(rows)


# --------------------------------------------------------------- 2. 시계열
def series(name: str) -> pd.DataFrame:
    df = frame(ds(f"{name} 종가 PBR BPS EPS PER {SERIES_FROM}-{ASOF}"))
    df.columns = [c.split(" ")[0] for c in df.columns]
    df["date"] = df["date"].str[:10]
    return df


def changepoints(df: pd.DataFrame) -> pd.DataFrame:
    sig = df[["BPS", "EPS"]].astype(str).agg("|".join, axis=1)
    return df[sig != sig.shift()]


# --------------------------------------------------------------- 3. 정의
def accounts(name: str, consolidated: bool, year: int) -> dict:
    q = (f'GetFinancialStatements({name}, report_type="IFRS", consolidated={consolidated}, '
         f"is_annual=True, date_from={year}-01-01, date_to={year}-12-31)")
    df = frame(ds(q))
    df = df[df["date"].str[:4] == str(year)]
    out = {}
    for k, (rid, aid) in ACC.items():
        hit = df[(df["report_id"].astype(str) == rid) & (df["account_id"].astype(str) == aid)]
        out[k] = float(hit["value"].iloc[0]) if len(hit) else None
    return out


def definition_check(name: str, s: pd.DataFrame, years=(2024, 2025)) -> list[dict]:
    rows = []
    for y in years:
        nxt = s[s["date"] >= f"{y + 1}-01-01"]
        if nxt.empty:
            continue
        mkt_bps = float(nxt["BPS"].iloc[0])
        c, sep = accounts(name, True, y), accounts(name, False, y)
        z = lambda v: v or 0.0
        issued = z(c["보통주발행주식수"]) + z(c["우선주발행주식수"])
        treasury = z(c["보통주자기주식수"]) + z(c["우선주자기주식수"])
        outstanding = issued - treasury
        variants = {
            "연결 지배지분 / 유통주식수": (c["지배기업소유주지분"], outstanding),
            "연결 지배지분 / 발행주식수": (c["지배기업소유주지분"], issued),
            "연결 자본총계 / 유통주식수": (c["자본총계"], outstanding),
            "별도 자본총계 / 유통주식수": (sep["자본총계"], outstanding),
            "연결 지배지분 / 보통주 유통주식수": (c["지배기업소유주지분"],
                                         z(c["보통주발행주식수"]) - z(c["보통주자기주식수"])),
        }
        for label, (num, den) in variants.items():
            bps = num / den if num and den else None
            rows.append({"entity": name, "fiscal_year": y, "market_bps_from": nxt["date"].iloc[0],
                         "market_bps": mkt_bps, "definition": label,
                         "equity_조원": round(num / 1e12, 4) if num else None,
                         "shares": int(den) if den else None,
                         "computed_bps": round(bps) if bps else None,
                         "diff_won": round(bps - mkt_bps) if bps else None})
        rows.append({"entity": name, "fiscal_year": y, "definition": "참고: 연결 기본주당이익(공시)",
                     "computed_bps": c["기본주당이익"]})
    return rows


# ------------------------------------------------------------ 4. 다른 경로
def dividends_bps(name: str) -> pd.DataFrame:
    df = frame(ds(f"GetCompanyDividends({name}, date_from=2023-01-01, date_to={ASOF[:4]}-12-31)"))
    df = df[df["dividend_type_name"].isin(["주당순자산(원)", "주당순이익(원)"])]
    return df.pivot_table(index=["symbol", "date", "accounting_type"], columns="dividend_type_name",
                          values="amount", aggfunc="first").reset_index()


def consensus_bps(name: str) -> pd.DataFrame:
    since = (pd.Timestamp(ASOF) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")
    df = frame(ds(f'SearchFirmFundamentalsForecasts({name}, True, "K", {since})'))
    keep = ["forecast_date", "name_ko", "date", "csd_bps", "csd_pbr", "csd_eps", "bps", "pbr"]
    return df[[c for c in keep if c in df.columns]]


def main():
    DATA.mkdir(exist_ok=True)
    kv = keyword_variants()
    kv.to_csv(DATA / "keyword_variants.csv", index=False, encoding="utf-8-sig")
    print(kv.to_string(index=False), "\n")

    cps, defs = [], []
    for name in COMPANIES:
        s = series(name)
        cp = changepoints(s)
        cp.insert(0, "entity", name)
        cps.append(cp)
        cps.append(s.tail(1).assign(entity=name, note=f"기준일({ASOF}) 값"))
        defs += definition_check(name, s)
    cp = pd.concat(cps, ignore_index=True)
    cp.to_csv(DATA / "bps_eps_changepoints.csv", index=False, encoding="utf-8-sig")
    print(cp.to_string(index=False), "\n")
    dd = pd.DataFrame(defs)
    dd.to_csv(DATA / "bps_definition_check.csv", index=False, encoding="utf-8-sig")
    print(dd.to_string(index=False), "\n")

    dv = dividends_bps("삼성전자")
    dv.to_csv(DATA / "dividends_bps.csv", index=False, encoding="utf-8-sig")
    print(dv.to_string(index=False), "\n")
    cs = consensus_bps("삼성전자")
    cs.to_csv(DATA / "consensus_bps.csv", index=False, encoding="utf-8-sig")
    print(cs.to_string(index=False))


if __name__ == "__main__":
    main()
