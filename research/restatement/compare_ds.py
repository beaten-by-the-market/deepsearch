"""2단계: 표본 회사-연도의 DeepSearch 값을 OpenDART 원래값/재작성값과 대조.

표본 (단위 = 회사·연도·재무제표구분)
- restated_cfs : 연결 재작성 사례, 연도별 N_CFS건
- restated_ofs : 별도 재작성 사례(연결 없는 회사 우선), 연도별 N_OFS건
- control      : 재작성 없는 연결 사례, 연도별 N_CTRL건 (매칭 방법 자체 검증용)
- ifrs17       : 2022년 상장 보험사 전체 (IFRS17 전환 재작성)
- 고정 사례    : LG전자 2020 등 (FIXED)

DeepSearch 호출: GetFinancialStatements(KRX:종목, consolidated=연결여부, report_ids=Income|BalanceSheet,
                 date_from=Y-01-01, date_to=Y-12-31)

출력: data/ds_vs_dart.csv  (계정 단위 1행)
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from collect_dart import FIN_PAT as INSURER_PAT   # 보험사 + 보험 자회사가 있는 금융지주
from common import CACHE, DATA, ds

SEED = 20261120
N_CFS, N_OFS, N_CTRL = 35, 10, 10
FIXED = [("066570", 2020, "CFS")]                     # LG전자: MC사업부 중단영업 재분류

# DART 계정 → (DeepSearch report_ids, account_id 후보 순서)
# 당기순이익: 연결은 8200(총당기순이익), 별도는 9000(당기순이익(손실))
DS_ACCOUNT = {
    "매출액": ("Income", ["1000"]),
    "영업이익": ("Income", ["5000"]),
    "당기순이익": ("Income", ["8200", "9000"]),
    "자산총계": ("BalanceSheet", ["5000"]),
    "부채총계": ("BalanceSheet", ["8000"]),
    "자본총계": ("BalanceSheet", ["8900"]),
}
REL_TOL, ABS_TOL = 0.0005, 1e6   # 0.05% 이내 또는 100만원 이내면 같은 값


def pick_units(pairs: pd.DataFrame) -> pd.DataFrame:
    u = (pairs.groupby(["corp_code", "stock_code", "corp_name", "year", "fs_div"])["restated_flag"]
         .any().reset_index())
    # 외국기업(종목코드 9xxxxx)은 DART가 외화, DeepSearch가 원화 환산값이라 비교 대상에서 제외
    u = u[~u.stock_code.str.startswith("9")]
    has_cfs = set(u.loc[u.fs_div == "CFS", ["corp_code", "year"]].itertuples(index=False, name=None))
    u["has_cfs"] = [(c, y) in has_cfs for c, y in zip(u.corp_code, u.year)]
    ins = u.corp_name.str.contains(INSURER_PAT, regex=True)

    picks = []
    for y, g in u.groupby("year"):
        g = g[~ins.loc[g.index]]
        picks.append(g[(g.fs_div == "CFS") & g.restated_flag]
                     .sample(min(N_CFS, ((g.fs_div == "CFS") & g.restated_flag).sum()), random_state=SEED)
                     .assign(group="restated_cfs"))
        ofs = g[(g.fs_div == "OFS") & g.restated_flag].sort_values("has_cfs")  # 연결 없는 회사 먼저
        ofs = pd.concat([ofs[~ofs.has_cfs].sample(min(N_OFS, (~ofs.has_cfs).sum()), random_state=SEED),
                         ofs[ofs.has_cfs]]).head(N_OFS)
        picks.append(ofs.assign(group="restated_ofs"))
        picks.append(g[(g.fs_div == "CFS") & ~g.restated_flag]
                     .sample(N_CTRL, random_state=SEED).assign(group="control"))
    picks.append(u[ins & (u.year == 2022) & u.restated_flag &
                   ((u.fs_div == "CFS") | ~u.has_cfs)].assign(group="ifrs17"))
    for code, y, fs in FIXED:
        picks.append(u[(u.stock_code == code) & (u.year == y) & (u.fs_div == fs)].assign(group="fixed"))
    out = pd.concat(picks).drop_duplicates(["corp_code", "year", "fs_div"], keep="last")
    return out.drop(columns=["restated_flag"])


def ds_values(stock: str, year: int, consolidated: bool) -> dict[str, float | None]:
    vals = {}
    for rid in ("Income", "BalanceSheet"):
        q = (f'GetFinancialStatements(KRX:{stock}, consolidated={consolidated}, report_ids="{rid}", '
             f'date_from={year}-01-01, date_to={year}-12-31)')
        d = ds(q)
        if not d:
            continue
        df = pd.DataFrame(d)
        if df.empty or "date" not in df or "account_id" not in df:
            continue
        df = df[df["date"].astype(str).str[:4] == str(year)]
        if df.empty:
            continue
        last = df["date"].max()                     # 결산월이 여러 개면 마지막
        df = df[df["date"] == last]
        for acc, (r, aids) in DS_ACCOUNT.items():
            if r != rid:
                continue
            vals[acc] = None
            for aid in aids:
                v = df.loc[df["account_id"] == aid, "value"]
                if len(v) and pd.notna(v.iloc[0]):
                    vals[acc] = float(v.iloc[0])
                    break
    return vals


def same(a, b) -> bool:
    if a is None or b is None or pd.isna(a) or pd.isna(b):
        return False
    d = abs(a - b)
    return d <= ABS_TOL or d <= REL_TOL * max(abs(a), abs(b))


def classify(ds_v, orig, rest) -> str:
    if ds_v is None or pd.isna(ds_v):
        return "ds_missing"
    if orig is None or pd.isna(orig):                 # 금융사 2022: 원래값 없음
        return "restated" if same(ds_v, rest) else "not_restated"
    o, r = same(ds_v, orig), same(ds_v, rest)
    if o and r:
        return "both"          # 원래값=재작성값 (재작성 안 된 계정)
    if o:
        return "original"
    if r:
        return "restated"
    return "neither"


def main():
    pairs = pd.read_csv(CACHE / "dart_pairs.csv", dtype={"stock_code": str, "corp_code": str})
    units = pick_units(pairs)
    print("표본:", units.group.value_counts().to_dict())

    def work(row):
        return row, ds_values(row.stock_code, int(row.year), row.fs_div == "CFS")

    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(work, r) for r in units.itertuples(index=False)]
        for i, f in enumerate(as_completed(futs), 1):
            row, vals = f.result()
            results[(row.corp_code, row.year, row.fs_div)] = vals
            if i % 50 == 0:
                print(f"  DeepSearch {i}/{len(futs)}")

    key = pairs.set_index(["corp_code", "year", "fs_div"]).index
    sub = pairs[key.isin(list(results))].merge(
        units[["corp_code", "year", "fs_div", "group"]], on=["corp_code", "year", "fs_div"])
    sub["deepsearch"] = [results[(c, y, f)].get(a) for c, y, f, a in
                         zip(sub.corp_code, sub.year, sub.fs_div, sub.account)]
    sub["result"] = [classify(d, o, r) for d, o, r in zip(sub.deepsearch, sub.original, sub.restated)]
    cols = ["group", "stock_code", "corp_name", "year", "fs_div", "account", "original", "restated",
            "deepsearch", "result", "restated_flag", "rcept_y", "rcept_y1"]
    sub[cols].sort_values(["group", "year", "stock_code", "fs_div", "account"]).to_csv(
        DATA / "ds_vs_dart.csv", index=False, encoding="utf-8-sig")
    print("저장:", DATA / "ds_vs_dart.csv", len(sub), "행")


if __name__ == "__main__":
    main()
