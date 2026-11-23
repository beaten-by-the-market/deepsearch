"""1단계: OpenDART 상장사 주요계정 수집 → 원래값/재작성값 쌍 만들기.

- 대상: corpCode.xml 에서 종목코드가 있는 회사 전체
- API : fnlttMultiAcnt (사업보고서 11011, 100개사씩)
- 쌍  : Y년의 원래값 = Y년 사업보고서 당기(thstrm),
        Y년의 재작성값 = Y+1년 사업보고서 전기(frmtrm)

출력
- data/cache/dart_pairs.csv      : 모든 쌍 (커서 git 제외)
- data/dart_restatements.csv     : 두 값이 다른 쌍만 (커밋)

사용: python research/restatement/collect_dart.py [시작연도] [끝연도]
      기본 2015 2023 (Y 기준. Y+1 보고서까지 받으므로 2024년 보고서까지 호출)
"""
from __future__ import annotations

import io
import sys
import zipfile
import xml.etree.ElementTree as ET

import pandas as pd
import requests

from common import CACHE, DATA, _key, dart, to_num

ACCOUNTS = ["자산총계", "부채총계", "자본총계", "매출액", "영업이익", "당기순이익(손실)", "당기순이익"]
REL_TOL = 0.001      # 0.1% 넘게 다르면 재작성으로 본다
ABS_TOL = 1e6        # 100만원 미만 차이는 무시(반올림)


def listed_corps() -> pd.DataFrame:
    p = CACHE / "corpcode.csv"
    if p.exists():
        return pd.read_csv(p, dtype=str)
    r = requests.get("https://opendart.fss.or.kr/api/corpCode.xml",
                     params={"crtfc_key": _key("DART_API_KEY")}, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        root = ET.fromstring(z.read(z.namelist()[0]))
    rows = [{c.tag: (c.text or "").strip() for c in el} for el in root.iter("list")]
    df = pd.DataFrame(rows)
    df = df[df["stock_code"].str.len() == 6][["corp_code", "corp_name", "stock_code"]]
    df.to_csv(p, index=False, encoding="utf-8-sig")
    return df


def fetch_year(corp_codes: list[str], year: int) -> pd.DataFrame:
    out = []
    for i in range(0, len(corp_codes), 100):
        j = dart("fnlttMultiAcnt.json", corp_code=",".join(corp_codes[i:i + 100]),
                 bsns_year=str(year), reprt_code="11011")
        out.extend(j.get("list", []))
    df = pd.DataFrame(out)
    if df.empty:
        return df
    df = df[df["account_nm"].isin(ACCOUNTS)].copy()
    # 당기순이익 표기 통일, 같은 계정이 두 번 나오면 첫 행(연결 전체 순이익) 사용
    df["account"] = df["account_nm"].replace({"당기순이익(손실)": "당기순이익"})
    df = df.drop_duplicates(["corp_code", "fs_div", "account"], keep="first")
    df["year"] = year
    return df[["corp_code", "stock_code", "fs_div", "account", "year",
               "thstrm_amount", "frmtrm_amount", "rcept_no"]]


# fnlttMultiAcnt 는 2022년 이전 보고서에서 금융업(은행·보험·금융지주)을 돌려주지 않고(013),
# fnlttSinglAcntAll 도 금융사는 2023년 사업보고서부터만 있다.
# → 보험사 2022년은 2023년 보고서 전기값(IFRS17 재작성값)만 받고, 원래값(IFRS4)은 비워 둔다.
FIN_PAT = r"^(?!.*(생명공학|생명과학)).*(생명|화재|손해보험|해상|보험|금융지주|신한지주)"
FIN_TAGS = {
    "ifrs-full_Assets": "자산총계",
    "ifrs-full_Liabilities": "부채총계",
    "ifrs-full_Equity": "자본총계",
    "ifrs-full_ProfitLoss": "당기순이익",
    "dart_OperatingIncomeLoss": "영업이익",
}


def fetch_fin(corp_code: str, year: int, fs_div: str) -> pd.DataFrame:
    j = dart("fnlttSinglAcntAll.json", corp_code=corp_code, bsns_year=str(year),
             reprt_code="11011", fs_div=fs_div)
    df = pd.DataFrame(j.get("list", []))
    if df.empty:
        return df
    df = df[df["account_id"].isin(FIN_TAGS) & df["sj_div"].isin(["BS", "IS", "CIS"])].copy()
    df["account"] = df["account_id"].map(FIN_TAGS)
    df = df.drop_duplicates("account", keep="first")
    df["fs_div"], df["year"], df["corp_code"] = fs_div, year, corp_code
    return df[["corp_code", "fs_div", "account", "year", "thstrm_amount", "frmtrm_amount", "rcept_no"]]


def fin_pairs(corps: pd.DataFrame) -> pd.DataFrame:
    fin = corps[corps["corp_name"].str.contains(FIN_PAT, regex=True)]
    rows = []
    for c in fin.itertuples():
        for fs in ("CFS", "OFS"):
            b = fetch_fin(c.corp_code, 2023, fs)
            for r in b.itertuples():
                rows.append({"corp_code": c.corp_code, "stock_code": c.stock_code, "fs_div": fs,
                             "account": r.account, "year": 2022,
                             "original": None, "restated": to_num(r.frmtrm_amount),
                             "rcept_y": None, "rcept_y1": r.rcept_no})
    print(f"  금융사 {len(fin)}곳 2022년 재작성값(2023 보고서 전기) 보충: {len(rows)}행")
    return pd.DataFrame(rows)


def main(y0=2015, y1=2023):
    corps = listed_corps()
    codes = corps["corp_code"].tolist()
    print(f"상장사 {len(codes)}곳, 보고서 {y0}~{y1 + 1}")
    years = {}
    for y in range(y0, y1 + 2):
        years[y] = fetch_year(codes, y)
        print(f"  {y} 사업보고서: {years[y]['corp_code'].nunique() if not years[y].empty else 0}개사")

    pairs = []
    for y in range(y0, y1 + 1):
        a, b = years[y], years[y + 1]
        if a.empty or b.empty:
            continue
        m = a.merge(b, on=["corp_code", "fs_div", "account"], suffixes=("_y", "_y1"))
        pairs.append(pd.DataFrame({
            "corp_code": m["corp_code"], "stock_code": m["stock_code_y"],
            "fs_div": m["fs_div"], "account": m["account"], "year": y,
            "original": m["thstrm_amount_y"].map(to_num),       # Y년 보고서 당기
            "restated": m["frmtrm_amount_y1"].map(to_num),      # Y+1년 보고서 전기
            "rcept_y": m["rcept_no_y"], "rcept_y1": m["rcept_no_y1"],
        }))
    pairs = pd.concat(pairs, ignore_index=True).dropna(subset=["original", "restated"])
    fin = fin_pairs(corps).dropna(subset=["restated"])
    fin = fin[~fin.set_index(["corp_code", "year", "fs_div", "account"]).index.isin(
        pairs.set_index(["corp_code", "year", "fs_div", "account"]).index)]
    pairs = pd.concat([pairs, fin], ignore_index=True)
    pairs = pairs.merge(corps[["corp_code", "corp_name"]], on="corp_code", how="left")
    pairs.insert(2, "corp_name", pairs.pop("corp_name"))
    diff = (pairs["restated"] - pairs["original"]).abs()
    base = pairs[["original", "restated"]].abs().max(axis=1)
    pairs["restated_flag"] = (diff > ABS_TOL) & (diff > REL_TOL * base)
    pairs.loc[pairs["original"].isna(), "restated_flag"] = True   # 금융사 2022: IFRS17 재작성 전제
    pairs.to_csv(CACHE / "dart_pairs.csv", index=False, encoding="utf-8-sig")
    rs = pairs[pairs["restated_flag"]].drop(columns="restated_flag")
    rs.to_csv(DATA / "dart_restatements.csv", index=False, encoding="utf-8-sig")

    print(f"\n쌍 {len(pairs):,}개 중 재작성 {len(rs):,}개 ({len(rs) / len(pairs):.1%})")
    cy = pairs.groupby(["corp_code", "year", "fs_div"])["restated_flag"].any()
    print(f"회사-연도-재무제표 {len(cy):,}개 중 하나라도 재작성 {cy.sum():,}개 ({cy.mean():.1%})")


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:3]]
    main(*args)
