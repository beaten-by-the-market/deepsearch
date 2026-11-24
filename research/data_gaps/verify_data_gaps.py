"""DeepSearch로 받을 수 없는 시장 데이터 확인 (CHECK API 케이스 시나리오 대조).

확인하는 것
1. 자연어 질의: 수급·공매도·대차·신용 용어가 데이터로 해석되는가, 기업 개요 표로 빠지는가
2. GetStockPrices 컬럼: 허용 컬럼 목록 (없는 컬럼을 넣으면 오류 메시지에 목록이 나온다)
3. 한국은행 시리즈: 수급·신용·선물·국고채 관련 통계표가 있는가, 마지막 시점은 언제인가
4. 사건 문서: 공매도 과열 지정·블록딜처럼 수치 대신 문서로 잡히는 것
5. 기타: 지수 목록(선물 없음), 채권 함수, 시리즈 검색(FindEntity DataSeries)

출력 (data/)
- nl_probe.csv        : 자연어 질의별 결과 컬럼과 기업 개요 표로 빠졌는지 여부
- price_columns.csv   : GetStockPrices 허용 컬럼
- bok_series.csv      : 한국은행 통계표 항목별 마지막 시점
- doc_events.csv      : 사건 문서 검색 건수와 예시 제목
- other_probes.csv    : 지수 목록, 채권 함수, 시리즈 검색 결과

사용: python research/data_gaps/verify_data_gaps.py [기준일 YYYY-MM-DD]
      기준일 기본값 2026-11-24 (검증일 2026-11-25 직전 거래일). 키는 레포 루트 .env 의 API_KEY.
      원시 응답은 data/cache/ 에 캐시되므로 다시 돌리면 API를 부르지 않는다.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = HERE / "data"
CACHE = DATA / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO / "skills" / "deepsearch" / "scripts"))

from _ds_common import (DeepSearchError, compute, dataframe_records,  # noqa: E402
                        find_api_key, result_pod)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ASOF = sys.argv[1] if len(sys.argv) > 1 else "2026-11-24"
D_TO = date.fromisoformat(ASOF)
D_FROM = (D_TO - timedelta(days=23)).isoformat()
KEY = find_api_key()

# 기업 개요 표(FindEntity 결과)에만 있는 컬럼. 이게 보이면 질의가 데이터로 해석되지 않은 것이다.
FALLBACK_MARK = {"ceo", "business_rid", "company_rid"}

NL_TERMS = ["거래량",  # 대조군: 정상 해석되는 시장데이터
            "외국인 순매수", "기관 순매수", "외국인보유비율",
            "공매도", "공매도잔고", "대차잔고", "대차거래",
            "신용잔고", "신용융자", "신용비율",
            "프로그램매매", "미결제약정", "베이시스", "NAV", "괴리율", "대량매매"]

# (통계표, 설명) — 항목 목록과 마지막 시점을 QueryBankOfKoreaSeriesInfo 로 확인
BOK_TABLES = [("901Y056", "증시주변자금동향 (투자자예탁금·신용융자·신용대주)"),
              ("901Y055", "투자자별 주식거래"),
              ("901Y057", "주가지수선물거래"),
              ("064Y001", "주식시장(일) — 지수·거래대금·외국인 순매수"),
              ("817Y002", "시장금리(일) — 국고채·콜·CD")]

DOC_EVENTS = [("공매도 과열종목 지정 공시", '["company"],["disclosure"],"title:과열"'),
              ("시장경보(투자경고) 공시", '["company"],["disclosure"],"title:투자경고"'),
              ("블록딜 뉴스 (제목)", '["news"],[],"title:블록딜"'),
              ("신용융자 잔고 뉴스", '["news"],[],"신용융자 잔고"')]


def ds(query: str) -> dict:
    """compute 호출 → {'query', 'ok', 'error', 'pod_class', 'columns', 'rows'} (캐시)."""
    p = CACHE / (hashlib.sha1(query.encode()).hexdigest() + ".json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    out = {"query": query, "ok": True, "error": "", "pod_class": "", "columns": [], "rows": [],
           "raw": None}
    try:
        body = compute(KEY, query, timeout=180)
        pod = result_pod(body)
        if pod is not None:
            out["pod_class"] = pod.get("class", "")
            content = pod.get("content") or {}
            if isinstance(content, dict):
                out["columns"] = list(content.get("columns") or [])
            out["rows"] = dataframe_records(content) or []
            if not out["rows"] and out["pod_class"] != "Result:DataFrame":
                out["raw"] = content
    except DeepSearchError as e:
        out["ok"], out["error"] = False, str(e)
    p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def write_csv(name: str, rows: list[dict]) -> None:
    path = DATA / name
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"  → {path.relative_to(REPO)} ({len(rows)}행)")


# ------------------------------------------------------------ 1. 자연어 질의
def nl_probe() -> list[dict]:
    rows = []
    for term in NL_TERMS:
        r = ds(f"삼성전자 {term} {D_FROM}-{ASOF}")
        cols = r["columns"]
        rows.append({"질의": f"삼성전자 {term} {D_FROM}-{ASOF}",
                     "컬럼수": len(cols),
                     "기업개요표로_빠짐": bool(FALLBACK_MARK & set(cols)),
                     "컬럼_앞부분": " ".join(map(str, cols[:6])),
                     "오류": r["error"][:150]})
    return rows


# ------------------------------------------------------ 2. GetStockPrices 컬럼
def price_columns() -> list[dict]:
    r = ds(f'GetStockPrices([KRX:005930], columns=["no_such_column"], date_from={ASOF}, date_to={ASOF})')
    m = re.search(r"Allowed columns: \[(.*?)\]", r["error"])
    allowed = re.findall(r"'([^']+)'", m.group(1)) if m else []
    if not allowed:
        print("  ! 허용 컬럼 목록을 오류 메시지에서 찾지 못했습니다:", r["error"][:200])
    gap_words = ("short", "loan", "credit", "lend", "foreign", "inst", "program", "nav", "open_interest")
    return [{"column": c, "공매도·대차·신용·수급·NAV 관련": any(w in c for w in gap_words)} for c in allowed]


# ------------------------------------------------------------ 3. 한국은행 시리즈
def bok_series() -> list[dict]:
    rows = []
    for code, desc in BOK_TABLES:
        r = ds(f'QueryBankOfKoreaSeriesInfo(stat_codes="{code}")')
        last: dict[str, dict] = {}
        for x in r["rows"]:
            item = x.get("item_code")
            if item not in last or str(x.get("end_time")) > str(last[item].get("end_time")):
                last[item] = x
        for item, x in last.items():
            rows.append({"stat_code": code, "통계표": x.get("stat_name_ko") or desc,
                         "item_code": item, "항목": x.get("item_name_ko"),
                         "주기": x.get("cycle"), "마지막_시점": x.get("end_time"),
                         "단위": x.get("unit")})
        if not r["rows"]:
            rows.append({"stat_code": code, "통계표": desc, "item_code": "", "항목": "(결과 없음)",
                         "주기": "", "마지막_시점": "", "단위": r["error"][:100]})
    return rows


# ---------------------------------------------------------------- 4. 사건 문서
def doc_events() -> list[dict]:
    rows = []
    for label, args in DOC_EVENTS:
        q = f"DocumentSearch({args},count=5,date_from={D_FROM},date_to={ASOF})"
        try:
            body = compute(KEY, q, timeout=180)
            res = ((body.get("data") or {}).get("pods") or [{}, {}])[1].get("content") or {}
            # DocumentSearch 결과는 content.data 아래에 total_matches/docs 가 있다
            d = res.get("data") if isinstance(res.get("data"), dict) else res
            docs = d.get("docs") or []
            rows.append({"사건": label, "쿼리": q, "건수": d.get("total_matches"),
                         "예시_제목": " | ".join((x.get("title") or "").strip()[:40] for x in docs[:3])})
        except DeepSearchError as e:
            rows.append({"사건": label, "쿼리": q, "건수": "", "예시_제목": f"오류: {e}"[:150]})
    return rows


# ---------------------------------------------------------------------- 5. 기타
def other_probes() -> list[dict]:
    rows = []
    r = ds("GetMarketIndexSymbols()")
    rows.append({"확인": "지수 목록 (GetMarketIndexSymbols)", "결과": f"{len(r['rows'])}종",
                 "내용": ", ".join(str(x.get("name_ko")) for x in r["rows"])})
    r = ds(f"GetBondYields(date_from={D_FROM}, date_to={ASOF})")
    rows.append({"확인": "채권 수익률 (GetBondYields)", "결과": "오류" if not r["ok"] else f"{len(r['rows'])}행",
                 "내용": r["error"][:150]})
    for kw in ["실업률", "신용융자", "공매도", "국고채"]:
        r = ds(f'FindEntity("DataSeries", "{kw}", count=20)')
        rows.append({"확인": f'시리즈 검색 FindEntity("DataSeries", "{kw}")',
                     "결과": f"{len(r['rows'])}행", "내용": r["error"][:150]})
    return rows


def main() -> None:
    print(f"기준일 {ASOF} (자연어 질의 구간 {D_FROM} ~ {ASOF})")
    print("1. 자연어 질의");         write_csv("nl_probe.csv", nl_probe())
    print("2. GetStockPrices 컬럼"); write_csv("price_columns.csv", price_columns())
    print("3. 한국은행 시리즈");     write_csv("bok_series.csv", bok_series())
    print("4. 사건 문서");           write_csv("doc_events.csv", doc_events())
    print("5. 기타");                write_csv("other_probes.csv", other_probes())


if __name__ == "__main__":
    main()
