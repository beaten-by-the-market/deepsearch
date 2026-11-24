# %% [markdown]
# # 1-10 한국의 배당계급 — 몇 년째 배당을 늘려 왔나
#
# **질문 예시:** "배당을 10년 넘게 계속 늘린 회사 있어?", "삼성전자·신한지주 배당 몇 년째 늘었어?", "배당 귀족 같은 거 한국에도 있어?"
#
# 미국에는 배당을 연속으로 늘린 햇수로 매기는 등급이 있습니다. 이 노트북은 같은 잣대를 국내 상장사에 적용합니다.
#
# | 미국 등급 | 기준 | 이 노트북 |
# |---|---|---|
# | 배당 왕 (Dividend Kings) | 50년 이상 연속 증가 | 그대로 |
# | 배당 귀족 (Aristocrats) | 25년 이상 + S&P500 편입 | **해당 없음** (지수 편입 조건이 국내에 없음) |
# | 배당 챔피언 (Champions) | 25년 이상 | 그대로 |
# | 배당 도전자 (Contenders) | 10~24년 | 그대로 |
# | 배당 신규 진입자 (Challengers) | 5~9년 | 그대로 |
#
# CHECK 원본(`1_기업펀더멘털/10_배당주`)은 배당수익률·배당성향·ROE로 몇 종목을 비교했습니다.
# 여기서는 **배당을 주는 전 종목**의 연속 증가 햇수를 계산하고 등급을 매깁니다. 원래 앱의 약점이던 종목별 반복 호출과 기준연도 하드코딩은 없앴습니다.
#
# | 단계 | DeepSearch |
# |---|---|
# | 배당 지급 종목 | 자연어 질의 `… and (날짜 배당수익률 > 0)` 한 번 |
# | 연도별 주당배당금(2013년~) | `GetDartDividends` (정기보고서 배당 표, 400종목씩 일괄) |
# | 그 이전 이력(1996년~) | `GetCompanyDividends` (상위 후보만 일괄) |

# %%
ASOF = "2026-11-24"   # 기준일 (배당수익률·배당 지급 여부를 보는 날)
EXTEND_TOP = 150      # 장기 이력으로 연장할 후보 최대 수

# %% [markdown]
# ## 1. 배당을 주는 종목
# 기준일 배당수익률이 0보다 큰 코스피·코스닥 종목을 한 번에 받습니다. 우선주는 빼고 보통주만 남깁니다.

# %%
pay = ds_df(f"(('코스피' 상장 기업) or ('코스닥' 상장 기업)) and ({ASOF} 배당수익률 > 0)")
ycol = [c for c in pay.columns if c.startswith("배당수익률")][0]
u = universe()
pay = pay[["symbol", ycol]].rename(columns={ycol: "배당수익률(%)"}).merge(u, on="symbol", how="left")
pay = pay[pay["company_type_l1"].isin(["1", "2"]) & pay["symbol"].str.endswith("0")].reset_index(drop=True)
print(f"배당 지급 보통주 {len(pay):,}종목 (공기업 {int((pay['company_type_l1'] == '2').sum())}종목 포함)")
pay.groupby("market").size().rename("종목 수").to_frame()

# %% [markdown]
# ## 2. 정기보고서 배당 표에서 보통주 주당배당금 뽑기
# `GetDartDividends`는 사업·분기·반기보고서의 배당 표를 줍니다. 보고서마다 **당기·전기·전전기** 값이 함께 있어서,
# 2015년 사업보고서부터 받으면 2013 회계연도까지 거슬러 갑니다.
#
# - **사업보고서만** 씁니다(보고서 기준일의 월 = 결산월).
# - 주당 현금배당금 행 가운데 **우선주·종류주는 빼고**, `보통주`·`소액주주`·`의결권 있는 주식` 같은 표기를 보통주로 봅니다.
#   차등배당(최대주주·소액주주 따로)이면 큰 값(대개 소액주주)을 씁니다. 표기가 비어 있으면 그 보고서에 다른 후보가 없을 때만 보통주로 봅니다.

# %%
import re
syms = pay["symbol"].tolist()
parts = [ds_df(f"GetDartDividends([{', '.join(syms[i:i + 400])}], date_from=2012-01-01, date_to={ASOF})")
         for i in range(0, len(syms), 400)]
dart = pd.concat(parts, ignore_index=True)
print(f"배당 표 {len(dart):,}행, {dart['symbol'].nunique():,}종목, 보고서 기준일 {dart['date'].min().date()} ~ {dart['date'].max().date()}")

PREF = re.compile(r"우선|종류|상환")
COMMON = re.compile(r"보통|보퉁|보동|일반주|소액주주|대주주|최대주주|의결권\s*있")
fye = u.set_index("symbol")["fiscal_year_end"].to_dict()

def common_dps(d):
    x = d[d["data_type"].str.replace(" ", "") == "주당현금배당금(원)"].copy()
    x["결산월"] = x["symbol"].map(fye).fillna(12).astype(int).replace(0, 12)
    x = x[x["date"].dt.month == x["결산월"]]                       # 사업보고서만
    x = x[~x["stock_type"].fillna("").str.contains(PREF)]           # 우선·종류주 제외
    x["표기"] = x["stock_type"].fillna("").str.contains(COMMON)

    def pick(g):
        e = g[g["표기"]]
        h = e if len(e) else g
        rule = "보통주 표기" if len(e) else ("표기 없음(행 1개)" if len(g) == 1 else "표기 없음(여러 행→최대)")
        return pd.Series({"this": h["this_period"].max(), "last": h["last_period"].max(),
                          "two": h["two_periods_ago"].max(), "규칙": rule})

    r = x.groupby(["symbol", "entity_name", "date"]).apply(pick, include_groups=False).reset_index()
    par = d[d["data_type"].str.replace(" ", "").str.startswith("주당액면가액")]
    par = par.groupby(["symbol", "date"])[["this_period", "last_period", "two_periods_ago"]].max()
    par.columns = ["par_this", "par_last", "par_two"]
    r = r.merge(par, left_on=["symbol", "date"], right_index=True, how="left")
    r["fy"] = r["date"].dt.year
    return r

rep = common_dps(dart)
print(f"사업보고서 {len(rep):,}건")
rep["규칙"].value_counts().rename("보고서 수").to_frame()

# %% [markdown]
# ## 3. 해마다 "늘렸나"를 판정하기 (액면분할 보정)
# 회계연도 Y의 증가 여부는 **Y 사업보고서 안의 당기 vs 전기**로 판정합니다. Y 보고서가 없으면 Y+1 보고서의 전기 vs 전전기를 씁니다.
#
# 같은 보고서 안이라도 **전기 배당을 분할 전 기준으로 적어 둔 회사가 있습니다**(삼성전자 2018 사업보고서: 당기 1,416원, 전기 42,500원).
# 그래서 같은 보고서의 **액면가(당기·전기)** 비율로 전기 배당을 보정합니다. 액면가와 배당을 함께 재작성한 회사는 비율이 1이라 영향이 없습니다.
#
# - **연속배당증가**: 당기 > 전기 가 이어진 햇수 (아니면 0으로 리셋)
# - **배당증가유지**: 당기 ≥ 전기 이고 당기 ≠ 0 이 이어진 햇수 (동결도 인정)

# %%
def yearly(r):
    rows = []
    for sym, g in r.groupby("symbol"):
        g = g.set_index("fy").sort_index()
        for y in range(g.index.min() - 1, g.index.max() + 1):
            if y in g.index:
                cur, prev, pa, pb, src = g.at[y, "this"], g.at[y, "last"], g.at[y, "par_this"], g.at[y, "par_last"], f"{y} 보고서"
            elif y + 1 in g.index:
                cur, prev, pa, pb, src = g.at[y + 1, "last"], g.at[y + 1, "two"], g.at[y + 1, "par_last"], g.at[y + 1, "par_two"], f"{y + 1} 보고서(전기)"
            else:
                continue
            adj = pa / pb if (pd.notna(pa) and pd.notna(pb) and pa > 0 and pb > 0 and pa != pb) else 1.0
            if adj != 1.0:
                src += f", 액면 {pb:,.0f}→{pa:,.0f} 보정"
            cur = 0.0 if pd.isna(cur) else float(cur)
            prev = None if pd.isna(prev) else float(prev) * adj
            rows.append({"symbol": sym, "fy": y, "dps": cur, "전기(보정)": prev, "출처": src,
                         "증가": None if prev is None else cur > prev,
                         "증가·유지": None if prev is None else (cur >= prev and cur != 0)})
    return pd.DataFrame(rows)

yr = yearly(rep)
END = int(rep.groupby("symbol")["fy"].max().value_counts().idxmax())   # 가장 많은 종목이 사업보고서를 낸 최신 연도
first_fy = yr.dropna(subset=["증가"]).groupby("symbol")["fy"].min()     # 종목별 첫 판정 연도
FIRST = int(first_fy.value_counts().idxmax())
OBS_MAX = END - FIRST + 1
print(f"기준 회계연도 {END} (최신 완결 연도 자동 판정) · 대부분 종목의 첫 판정 연도 {FIRST} "
      f"→ DART만으로 관측 가능한 최대 연속 {OBS_MAX}년")

def run_length(flags, end):
    n, y = 0, end
    while flags.get(y) is True:
        n, y = n + 1, y - 1
    return n

st = []
for sym, g in yr.groupby("symbol"):
    inc, keep = dict(zip(g["fy"], g["증가"])), dict(zip(g["fy"], g["증가·유지"]))
    st.append({"symbol": sym, "연속배당증가": run_length(inc, END), "배당증가유지": run_length(keep, END),
               "END 보고서": END in set(g["fy"])})
st = pd.DataFrame(st)
st["첫 판정 연도"] = st["symbol"].map(first_fy)
st["관측 한계"] = END - st["첫 판정 연도"] + 1          # 이 종목을 DART로 셀 수 있는 최대 연수
dist =pd.DataFrame({"연속배당증가": st["연속배당증가"].value_counts(), "배당증가유지": st["배당증가유지"].value_counts()}).fillna(0).astype(int).sort_index()
dist.index.name = "연수"
dist.T

# %% [markdown]
# ## 4. 관측 한계에 닿은 종목은 더 오래된 이력으로 연장
# DART 표만으로는 최대 위 연수까지만 셀 수 있습니다. 그 한계에 닿은 종목은 `GetCompanyDividends`(1996년~)로 이어 붙입니다.
#
# 이 데이터는 **분할 보정이 안 된 원래 값**이고, 실제로는 배당했는데 **0원으로 들어 있는 해**가 있습니다(예: 신한지주 2023년 0원, DART에는 2,100원).
# 그래서 다음 규칙으로 보수적으로 셉니다.
# - DART와 겹치는 해는 DART 값을 씁니다. 연장은 그 종목의 DART 첫 판정 연도 이전으로만 합니다.
# - 이어 붙이는 첫해는 두 출처의 주당배당금이 같아야 합니다(다르면 "출처 불일치"로 멈춤).
# - 직전 해의 30% 미만으로 급감하면 **분할인지 실제 감배(예: 1997~98년 외환위기)인지 구분할 수 없어** 멈추고, 앞뒤 해가 양수인데 가운데가 0원이면 **결측 가능**으로 보고 거기서 멈춥니다(연장하지 않음).

# %%
hit = ((st["연속배당증가"] >= st["관측 한계"]) | (st["배당증가유지"] >= st["관측 한계"])) & (st["관측 한계"] >= 5)
cand = st[hit].sort_values("관측 한계", ascending=False)["symbol"].tolist()[:EXTEND_TOP]
print(f"DART 관측 한계(5년 이상)에 닿은 종목 {int(hit.sum())}개 중 {len(cand)}개를 연장 후보로")
gcd = ds_df(f"GetCompanyDividends([{', '.join(cand)}], date_from=1990-01-01, date_to={ASOF})") if cand else pd.DataFrame()
DPS_COLS = ["주당현금배당액(소주주,보통주)(원)", "보통주현금배당액"]

def gcd_series(sym):
    a = gcd[(gcd["symbol"] == sym) & (gcd["accounting_type"] == "1") & gcd["dividend_type_name"].isin(DPS_COLS)]
    if a.empty:
        return pd.Series(dtype=float)
    p = a.pivot_table(index="date", columns="dividend_type_name", values="amount", aggfunc="max")
    s = p[DPS_COLS[0]] if DPS_COLS[0] in p else p[DPS_COLS[1]]
    if DPS_COLS[1] in p:
        s = s.fillna(p[DPS_COLS[1]])
    s.index = s.index.year
    return s.groupby(level=0).max().sort_index()   # 같은 해에 연간 행이 둘이면 큰 값

def extend(sym, key, base):
    """DART로 관측 한계까지 이어졌으면, 그 종목의 첫 판정 연도 직전 해부터 거꾸로 GetCompanyDividends로 이어 센다."""
    row = st[st["symbol"] == sym].iloc[0]
    if sym not in cand or base < row["관측 한계"]:
        return base, ""
    s = gcd_series(sym)
    f0 = yr[(yr["symbol"] == sym) & (yr["fy"] == row["첫 판정 연도"])]
    dart_y0 = f0["전기(보정)"].iloc[0] if len(f0) else None     # DART가 아는 가장 오래된 해의 주당배당금
    y = int(row["첫 판정 연도"]) - 1
    g0 = s.get(y)
    if dart_y0 is None or g0 is None or pd.isna(g0) or abs(g0 - dart_y0) > 0.5:
        return base, f"{y}년 출처 불일치(DART {dart_y0}, GCD {g0})로 연장 안 함"
    n, note = base, ""
    while True:
        cur, prev = s.get(y), s.get(y - 1)
        if cur is None or prev is None or pd.isna(cur) or pd.isna(prev):
            note = f"{y - 1}년 이전 자료 없음"
            break
        nxt = s.get(y - 2)
        if prev == 0 and cur > 0 and nxt is not None and nxt > 0:
            note = f"{y - 1}년 0원(결측 가능)에서 멈춤"
            break
        if prev > 0 and cur < 0.3 * prev:
            note = f"{y}년 급감(분할 또는 실제 감배)에서 멈춤"
            break
        ok = cur > prev if key == "연속배당증가" else (cur >= prev and cur != 0)
        if not ok:
            note = f"{y}년에 끊김"
            break
        n, y = n + 1, y - 1
    return n, note

for key in ("연속배당증가", "배당증가유지"):
    res = [extend(s_, key, b) for s_, b in zip(st["symbol"], st[key])]
    st[key + "(연장)"] = [r[0] for r in res]
    st[key + " 메모"] = [r[1] for r in res]
ext = st[st["symbol"].isin(cand)].merge(u[["symbol", "name"]], on="symbol")
print("연장으로 늘어난 종목 수 — 연속배당증가:", int((ext["연속배당증가(연장)"] > ext["연속배당증가"]).sum()),
      "/ 배당증가유지:", int((ext["배당증가유지(연장)"] > ext["배당증가유지"]).sum()))
print("멈춘 이유(배당증가유지):", ext["배당증가유지 메모"].str.replace(r"^\d{4}년\s*", "", regex=True)
      .str.replace(r"\(DART.*", "", regex=True).value_counts().to_dict())
ext[["name", "연속배당증가", "연속배당증가(연장)", "연속배당증가 메모", "배당증가유지", "배당증가유지(연장)", "배당증가유지 메모"]] \
    .sort_values(["배당증가유지(연장)", "연속배당증가(연장)"], ascending=False).head(15).reset_index(drop=True)

# %% [markdown]
# ## 5. 배당계급표
# 연장까지 반영한 **연속배당증가** 햇수로 등급을 매기고, 최근 5년 주당배당금, 배당수익률, 배당성향(현금배당총액 ÷ 연결 당기순이익)을 붙입니다.
# 동결을 인정하는 **배당증가유지** 기준 등급도 옆에 둡니다(국내는 배당을 몇 년 동결하는 경우가 많아 이쪽이 실감에 가깝습니다).

# %%
def tier(n):
    if n >= 50: return "👑 배당 왕 (50년+)"
    if n >= 25: return "🏆 배당 챔피언 (25년+)"
    if n >= 10: return "🏅 배당 도전자 (10~24년)"
    if n >= 5:  return "🚀 신규 진입자 (5~9년)"
    return "-"

def recent5(sym):
    g = yr[yr["symbol"] == sym].set_index("fy")["dps"]
    return " → ".join(f"{g.get(y, float('nan')):,.0f}" for y in range(END - 4, END + 1))

fy_end = dart[(dart["date"].dt.year == END) & (dart["date"].dt.month == dart["symbol"].map(fye).fillna(12).astype(int).replace(0, 12))]
tot = fy_end[fy_end["data_type"].str.contains("현금배당금총액")].groupby("symbol")["this_period"].max()
ni = None
for label in ("(연결)당기순이익", "(별도)당기순이익", "(개별)당기순이익"):   # 연결이 없으면 별도·개별
    s_ = fy_end[fy_end["data_type"].str.startswith(label)].groupby("symbol")["this_period"].max()
    ni = s_ if ni is None else ni.combine_first(s_)
payout = (tot / ni.where(ni > 0) * 100).rename("배당성향(%)")   # 순이익 0 이하(적자)면 비움

board = st.merge(pay[["symbol", "name", "market", "배당수익률(%)"]], on="symbol").merge(payout, left_on="symbol", right_index=True, how="left")
board["등급(증가)"] = board["연속배당증가(연장)"].map(tier)
board["등급(증가·유지)"] = board["배당증가유지(연장)"].map(tier)
board[f"DPS {END - 4}~{END}"] = board["symbol"].map(recent5)
board = board.sort_values(["연속배당증가(연장)", "배당증가유지(연장)", "배당수익률(%)"], ascending=False)

ORDER = ["👑 배당 왕 (50년+)", "🏆 배당 챔피언 (25년+)", "🏅 배당 도전자 (10~24년)", "🚀 신규 진입자 (5~9년)", "-"]
summary = pd.DataFrame({"연속배당증가 기준": board["등급(증가)"].value_counts(),
                        "배당증가유지 기준": board["등급(증가·유지)"].value_counts()}).reindex(ORDER).fillna(0).astype(int)
summary.rename(index={"-": "5년 미만"})

# %%
cols = ["name", "market", "연속배당증가(연장)", "배당증가유지(연장)", "등급(증가)", f"DPS {END - 4}~{END}", "배당수익률(%)", "배당성향(%)"]
top = board[board["연속배당증가(연장)"] >= 5][cols].round(2).reset_index(drop=True)
top.index += 1
top.head(30)

# %% [markdown]
# ### 동결을 인정하면 (배당증가유지 10년 이상, 배당수익률 순)

# %%
keep10 = board[board["배당증가유지(연장)"] >= 10].sort_values("배당수익률(%)", ascending=False)[cols].round(2).reset_index(drop=True)
keep10.index += 1
print(f"배당증가유지 10년 이상: {len(keep10)}종목")
keep10.head(20)

# %% [markdown]
# ## 6. 손으로 검산
# 몇 종목은 연도별 판정을 그대로 펼쳐 봅니다. 출처 열에 어느 보고서에서 읽었는지, 액면 보정이 들어갔는지 나옵니다.

# %%
CHECKS = {"KRX:055550": "신한지주", "KRX:005930": "삼성전자", "KRX:000270": "기아", "KRX:033780": "KT&G"}
for sym, nm in CHECKS.items():
    g = yr[yr["symbol"] == sym][["fy", "dps", "전기(보정)", "증가", "증가·유지", "출처"]].tail(8)
    b = board[board["symbol"] == sym]
    head = f"{nm}: 연속배당증가 {int(b['연속배당증가(연장)'].iloc[0])}년, 배당증가유지 {int(b['배당증가유지(연장)'].iloc[0])}년" if len(b) else nm
    print(head)
    display(g.reset_index(drop=True))

# %%
# GetCompanyDividends 와 DART 가 어긋나는 해 (DART 쪽이 맞는 사례 확인용)
chk = ds_df(f"GetCompanyDividends([{', '.join(CHECKS)}], date_from=2013-01-01, date_to={ASOF})")
cmp_rows = []
for sym, nm in CHECKS.items():
    s = chk[(chk["symbol"] == sym) & (chk["accounting_type"] == "1") & (chk["dividend_type_name"] == DPS_COLS[0])]
    s = s.set_index(s["date"].dt.year)["amount"]
    for _, r in yr[yr["symbol"] == sym].iterrows():
        g = s.get(r["fy"])
        if g is not None and abs(g - r["dps"]) > 0.5:
            cmp_rows.append({"종목": nm, "회계연도": r["fy"], "DART": r["dps"], "GetCompanyDividends": g})
pd.DataFrame(cmp_rows) if cmp_rows else "두 출처가 모두 일치"

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **국내에는 25년 이상 연속 증가(챔피언)가 사실상 없습니다.** 연속 증가는 10년 안팎이 최상위이고, 동결을 인정하면 훨씬 많은 종목이 10년 이상 이어집니다.
# - **배당 귀족**은 S&P500 편입 조건이라 국내에 대응 개념이 없어 매기지 않았습니다.
# - DART 배당 표로는 **2013 회계연도부터** 판정됩니다. 그 이전은 `GetCompanyDividends`로 연장했는데, 분할 보정이 없고 0원 결측이 섞여 있어 **급감·0원에서 멈추는 보수적 기준**입니다(실제 연속 햇수보다 짧게 나올 수 있음).
# - 액면분할은 보정하지만 **무상증자로 주식 수가 늘어난 해**는 보정하지 않습니다. 이때 주당배당금이 줄어 연속이 끊긴 것처럼 보일 수 있습니다.
# - 중간·분기배당은 사업보고서의 연간 합계 기준입니다. 특별배당을 준 다음 해는 "감소"로 셉니다(삼성전자 2020→2021).
# - 배당 지급 종목은 **기준일에 배당수익률이 있는 현재 상장사**입니다. 배당을 끊은 회사, 상장폐지된 회사는 빠집니다.
