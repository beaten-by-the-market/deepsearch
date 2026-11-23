"""3단계: data/ds_vs_dart.csv 를 집계해 README용 표(마크다운)를 출력.

사용: python research/restatement/summarize.py > research/restatement/data/summary.md
"""
from __future__ import annotations

import pandas as pd

from common import DATA

LABEL = {"restated": "재작성값", "original": "원래값", "neither": "둘 다 아님",
         "ds_missing": "DS 값 없음", "not_restated": "재작성값 아님", "both": "같음"}


def md(df: pd.DataFrame) -> str:
    return df.to_markdown(index=True) if hasattr(df, "to_markdown") else df.to_string()


def unit_verdict(g: pd.DataFrame) -> str:
    r = g.loc[g.restated_flag, "result"]
    r = r[r != "ds_missing"]
    if r.empty:
        return "판정 불가"
    s = set(r)
    if s <= {"restated"}:
        return "재작성값"
    if s <= {"original", "not_restated"}:
        return "원래값" if "original" in s else "재작성값 아님"
    if "neither" in s and len(s) == 1:
        return "둘 다 아님"
    return "혼합"


def pct_table(df, by):
    t = pd.crosstab(df[by], df["result"].map(LABEL), margins=True, margins_name="합계")
    return t


def main():
    d = pd.read_csv(DATA / "ds_vs_dart.csv", dtype={"stock_code": str})
    rs = d[d.restated_flag & (d.group != "control")]
    ctrl = d[d.group == "control"]

    print("## 계정 단위: 재작성된 계정에서 DeepSearch가 고른 값\n")
    print(md(pct_table(rs, "group")), "\n")

    units = (d[d.group != "control"].groupby(["group", "stock_code", "corp_name", "year", "fs_div"])
             .apply(unit_verdict, include_groups=False).rename("verdict").reset_index())
    print("## 회사·연도 단위 판정\n")
    print(md(pd.crosstab(units.group, units.verdict, margins=True, margins_name="합계")), "\n")
    print("### 연도별 (restated_cfs + restated_ofs)\n")
    u2 = units[units.group.isin(["restated_cfs", "restated_ofs"])]
    print(md(pd.crosstab(u2.year, u2.verdict, margins=True, margins_name="합계")), "\n")

    # 바뀐 계정 종류: 손익만(재분류 성격) vs 재무상태표 포함(소급 재작성 성격)
    gen = d[d.group.isin(["restated_cfs", "restated_ofs"]) & d.restated_flag]
    kind = (gen.groupby(["stock_code", "year", "fs_div"])["account"]
            .apply(lambda a: "재무상태표 포함" if a.isin(["자산총계", "부채총계", "자본총계"]).any() else "손익만")
            .rename("kind").reset_index())
    k = u2.merge(kind, on=["stock_code", "year", "fs_div"])
    k = k[k.verdict.isin(["원래값", "재작성값"])]
    k.to_csv(DATA / "unit_kinds.csv", index=False, encoding="utf-8-sig")
    print("### 바뀐 계정 종류별 (원래값/재작성값으로 판정된 회사·연도)\n")
    print(md(pd.crosstab([k.kind, k.fs_div], k.verdict, margins=True, margins_name="합계")), "\n")
    print("### 연도 × 바뀐 계정 종류\n")
    print(md(pd.crosstab(k.year, [k.kind, k.verdict])), "\n")

    print("### 계정별 (재작성된 계정만, 일반기업)\n")
    print(md(pct_table(rs[rs.group.isin(["restated_cfs", "restated_ofs", "fixed"])], "account")), "\n")

    print("## 대조군: 재작성 없는 계정에서 DeepSearch = DART 인가\n")
    print(md(pct_table(ctrl, "account")), "\n")

    print("## IFRS17 금융사 2022 (원래값은 OpenDART에 없음)\n")
    f = rs[rs.group == "ifrs17"].copy()
    f["DS(억)"] = (f.deepsearch / 1e8).round()
    f["재작성(억)"] = (f.restated / 1e8).round()
    print(md(f.pivot_table(index=["corp_name", "fs_div"], columns="account",
                           values="result", aggfunc="first").fillna("")), "\n")

    units.to_csv(DATA / "unit_verdicts.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
