# %% [markdown]
# # 3-03 거래대금 급증·변동성 — 갑자기 돈이 몰리거나 요동친 종목
#
# **질문 예시:** "요즘 거래대금이 갑자기 터진 종목 있어? 평소 대비 몇 배인지랑 공시도 붙여줘",
# "최근 하루 변동성이 제일 큰 종목 뽑아줘"
#
# 방향(등락)이 아니라 **관심의 폭발**(거래대금 급증)과 **불안정성**(일간 변동성)으로 종목을 고르고,
# 각 종목의 공시를 붙여 원인을 확인합니다.
#
# **각색한 점:** CHECK 원본(`3_시세스크리너/03`)은 종목별 기간 시세를 돌며 계산했습니다.
# DeepSearch는 `GetStockPrices`에 종목을 생략하면 **전 종목 하루치**가 한 번에 오므로,
# 거래일마다 한 번씩(25회) 불러 전 종목 패널을 만듭니다. 그래서 코스닥도 상위권이 아니라 **전수**입니다.
# 거래대금은 KRX 기준(NXT 미포함)입니다.

# %%
ASOF = "2026-11-24"   # 기준일
RECENT = 5            # 최근 구간(거래일)
BASE = 20             # 비교 기준 구간(최근 구간 직전 거래일)
MIN_RECENT_VALUE = 5e9   # 최근 구간 평균 거래대금 하한(50억) — 거래가 거의 없는 종목의 배수 착시 방지
TOP = 10

# %% [markdown]
# ## 1. 거래일 목록과 전 종목 패널
# 거래일은 지수 시세(`GetMarketIndexes`)의 날짜로 정합니다. 거래일마다 전 종목 스냅샷을 불러 이어 붙입니다.

# %%
idx = index_prices((pd.Timestamp(ASOF) - pd.Timedelta(days=60)).date(), ASOF)
days = sorted(idx["date"].dt.date.unique())[-(RECENT + BASE):]
print(f"거래일 {len(days)}개: {days[0]} ~ {days[-1]}")

def stocks(day):
    """일반법인(1)·공기업(2) 보통주 전 종목 하루치. 헬퍼의 all_stocks(common_only=True)는 공기업 8종목
    (한국전력·기업은행·강원랜드 등, company_type_l1='2')을 빼므로 여기서 직접 거릅니다."""
    s = all_stocks(day, common_only=False)
    return s[s["company_type_l1"].isin(["1", "2"]) & s["symbol"].str.endswith("0")].reset_index(drop=True)

frames = []
for d in days:
    s = stocks(d)
    frames.append(s[s["date"].dt.date == d])   # 휴장일 대체 방지: 그날 행만
panel = pd.concat(frames, ignore_index=True)
panel = panel[panel["volume"] > 0]              # 거래정지일 제외
print(panel.shape, "종목 수", panel["symbol"].nunique())

# %% [markdown]
# ## 2. 지표 계산
# - **거래대금 급증 배수** = 최근 5거래일 평균 거래대금 ÷ 직전 20거래일 평균 거래대금
# - **최대 일간 변동** = 최근 5거래일 중 하루 |등락률| 최댓값
# - **평균 일중 폭** = (고가 − 저가) ÷ 전일 종가의 최근 5일 평균
#
# 25거래일 중 거래일이 20일 미만인 종목(신규상장·장기 거래정지)은 뺍니다.

# %%
recent_days, base_days = set(days[-RECENT:]), set(days[:BASE])
panel["d"] = panel["date"].dt.date
panel["prev_close"] = panel["close"] / (1 + panel["change_rate"])
panel["range_pct"] = (panel["high"] - panel["low"]) / panel["prev_close"] * 100

g = panel.groupby("symbol")
m = pd.DataFrame({
    "name": g["name"].last(), "market": g["market"].last(),
    "n_days": g["d"].nunique(),
    "recent_value": panel[panel["d"].isin(recent_days)].groupby("symbol")["value"].mean(),
    "base_value": panel[panel["d"].isin(base_days)].groupby("symbol")["value"].mean(),
    "max_abs_move": panel[panel["d"].isin(recent_days)].groupby("symbol")["change_pct"].apply(lambda s: s.abs().max()),
    "limit_days": panel[panel["d"].isin(recent_days)].groupby("symbol")["change_pct"].apply(lambda s: int((s.abs() >= 29.5).sum())),
    "avg_range": panel[panel["d"].isin(recent_days)].groupby("symbol")["range_pct"].mean(),
    "ret_recent": panel[panel["d"].isin(recent_days)].groupby("symbol")["change_rate"].apply(lambda s: ((1 + s).prod() - 1) * 100),
})
m = m[(m["n_days"] >= 20) & m["base_value"].gt(0)].copy()
m["limit_days"] = m["limit_days"].astype(int)
m["surge_x"] = m["recent_value"] / m["base_value"]
print("계산 대상 종목:", len(m))

# %%
m["recent_eok"] = m["recent_value"] / 1e8   # 억원
m["base_eok"] = m["base_value"] / 1e8
surge = m[m["recent_value"] >= MIN_RECENT_VALUE].sort_values("surge_x", ascending=False).head(TOP).copy()
print(PRICE_NOTICE)
print("거래대금 급증 상위 (금액 단위: 억원, 수익률·변동: %)")
surge[["name", "market", "surge_x", "recent_eok", "base_eok", "ret_recent", "max_abs_move"]].round(1)

# %% [markdown]
# 상·하한가(±30%)가 많아 최대 일간 변동만으로는 동점이 생깁니다. **상·하한가 일수 → 최대 일간 변동 → 평균 일중 폭** 순으로 정렬합니다.

# %%
vol = (m[m["recent_value"] >= 1e9]
       .sort_values(["limit_days", "max_abs_move", "avg_range"], ascending=False).head(TOP).copy())
print("변동성 상위 (최근 5거래일, %)")
vol[["name", "market", "limit_days", "max_abs_move", "avg_range", "ret_recent", "surge_x"]].round(1)

# %% [markdown]
# ## 3. 공시 붙이기
# 두 목록의 종목을 묶어 **한 번의 공시 검색**(`securities.symbol:(코드 or 코드 …)`)으로 최근 구간 공시를 받습니다.
# 회사가 낸 공시와 거래소가 붙인 경보(투자주의·투자경고·공매도 과열 등)가 함께 나옵니다.

# %%
def attach_disclosures(symbols, date_from, date_to, per_stock=4):
    codes = [s.split(":")[-1] for s in symbols]
    total, docs = doc_search("company", ["disclosure"], "securities.symbol:(" + " or ".join(codes) + ")",
                             date_from, date_to, count=100, pages=3)
    out = {}
    if docs.empty:   # 0건이면 doc_search 가 열 없는 표를 돌려줌
        return {"KRX:" + c: (0, "(공시 없음)") for c in codes}
    for code in codes:
        sub = docs[docs["symbols"].str.contains(code, na=False)].sort_values("created_at")
        titles = sub["title"].str.replace(r"\s+", " ", regex=True).drop_duplicates().tolist()
        out["KRX:" + code] = (len(sub), " → ".join(titles[-per_stock:]) if titles else "(공시 없음)")
    return out

syms = list(dict.fromkeys(list(surge.index) + list(vol.index)))
disc = attach_disclosures(syms, days[-RECENT], ASOF)
for name, tbl in (("거래대금 급증", surge), ("변동성", vol)):
    tbl["공시수"] = [disc[s][0] for s in tbl.index]
    tbl["최근 공시(오래된→최근)"] = [disc[s][1] for s in tbl.index]

surge[["name", "surge_x", "공시수", "최근 공시(오래된→최근)"]].round(1)

# %%
vol[["name", "max_abs_move", "공시수", "최근 공시(오래된→최근)"]].round(1)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **배수는 "최근 거래가 평소의 몇 배인가"**입니다. 기준 구간 거래가 거의 없던 종목은 배수가 과장되므로
#   최근 평균 거래대금 하한(`MIN_RECENT_VALUE`)을 둡니다.
# - **최대 일간 변동이 30%에 가까우면 상·하한가**입니다. 거래정지 후 재개 첫날은 30%를 넘을 수 있습니다.
# - 공시가 없으면 본주 공시 없이 테마·뉴스로 움직인 경우입니다 → `08_movers_with_reasons`에서 뉴스까지 붙여 보세요.
# - 가격은 수정주가라 기간 중 무상증자·분할이 있어도 등락률이 왜곡되지 않습니다. 대신 표의 가격은 당시 호가와 다를 수 있습니다.
# - 거래대금은 KRX만 집계되어 NXT 거래분만큼 작게 나옵니다(대형주는 절반 가까이).
