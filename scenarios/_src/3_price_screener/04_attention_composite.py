# %% [markdown]
# # 3-04 기간 주목주 종합 — 시세·공시·뉴스를 합친 '주목도' 랭킹
#
# **질문 예시:** "지금 시장에서 가장 주목받는 종목을 종합 점수로 랭킹해줘",
# "이번 달 급등·거래폭증·변동성 다 합쳐서 주목주 상위 뽑아줘"
#
# 기간 수익률·최대 일간 변동·거래대금 증가율을 따로 보지 않고 **하나의 점수**로 줄 세운 뒤,
# 상위 종목에 공시를 붙여 왜 주목받는지 바로 읽습니다.
#
# **각색·확장한 점:**
# - CHECK 원본(`3_시세스크리너/04`)은 시세 지표 3개만 합쳤습니다. 여기서는 **공시 건수와 뉴스 증가율**을 더합니다.
#   DeepSearch는 뉴스·공시에 종목 태그가 있어 `DocumentAggregation` **한 번 호출로 전 종목 건수**를 셉니다.
# - 전 종목 시세는 거래일마다 한 번씩 받는 스냅샷(40회)으로 만듭니다. 코스닥도 전수입니다.

# %%
ASOF = "2026-11-24"   # 기준일
PERIOD = 20           # 주목 기간(거래일) — 약 한 달
BASE = 20             # 비교 기준 구간(주목 기간 직전 거래일)
MIN_VALUE = 3e9       # 주목 기간 평균 거래대금 하한(30억)
TOP = 15
# 점수 가중치 (합이 1일 필요는 없음)
WEIGHTS = {"ret": 1.0, "move": 1.0, "value_x": 1.0, "disc": 0.5, "news_x": 0.5}

# %% [markdown]
# ## 1. 전 종목 시세 패널 (40거래일)

# %%
idx = index_prices((pd.Timestamp(ASOF) - pd.Timedelta(days=90)).date(), ASOF)
days = sorted(idx["date"].dt.date.unique())[-(PERIOD + BASE):]
period_days, base_days = days[-PERIOD:], days[:BASE]
print(f"기준 구간 {base_days[0]} ~ {base_days[-1]} / 주목 기간 {period_days[0]} ~ {period_days[-1]}")

def stocks(day):
    """일반법인(1)·공기업(2) 보통주 전 종목 하루치. 헬퍼의 all_stocks(common_only=True)는 공기업 8종목
    (한국전력·기업은행·강원랜드 등, company_type_l1='2')을 빼므로 여기서 직접 거릅니다."""
    s = all_stocks(day, common_only=False)
    return s[s["company_type_l1"].isin(["1", "2"]) & s["symbol"].str.endswith("0")].reset_index(drop=True)

frames = []
for d in days:
    s = stocks(d)
    frames.append(s[s["date"].dt.date == d])
panel = pd.concat(frames, ignore_index=True)
panel = panel[panel["volume"] > 0]
panel["d"] = panel["date"].dt.date
print(panel.shape, "종목 수", panel["symbol"].nunique())

# %% [markdown]
# ## 2. 시세 지표
# - **기간 수익률**: 주목 기간 일별 등락률을 복리로 곱한 값(수정주가 기준)
# - **최대 일간 변동**: 주목 기간 중 하루 |등락률| 최댓값
# - **거래대금 증가 배수**: 주목 기간 평균 ÷ 기준 구간 평균

# %%
pp, bp = panel[panel["d"].isin(period_days)], panel[panel["d"].isin(base_days)]
gp = pp.groupby("symbol")
m = pd.DataFrame({
    "name": gp["name"].last(), "market": gp["market"].last(),
    "n_days": gp["d"].nunique(),
    "ret": gp["change_rate"].apply(lambda s: ((1 + s).prod() - 1) * 100),
    "move": gp["change_pct"].apply(lambda s: s.abs().max()),
    "value_p": gp["value"].mean(),
    "value_b": bp.groupby("symbol")["value"].mean(),
    "mcap": gp["market_cap"].last(),
})
m = m[(m["n_days"] >= PERIOD - 2) & (m["value_b"] > 0) & (m["value_p"] >= MIN_VALUE)].copy()
m["value_x"] = m["value_p"] / m["value_b"]
print("점수 대상 종목:", len(m))

# %% [markdown]
# ## 3. 공시·뉴스 건수 (전 종목 한 번에)
# `DocumentAggregation(..., "securities.symbol:N")`은 종목코드별 문서 수를 돌려줍니다.
# - **공시 건수**: 주목 기간 공시(회사 공시 + 거래소 경보) 수
# - **뉴스 증가 배수**: (주목 기간 뉴스 + 1) ÷ (기준 구간 뉴스 + 1).
#   'DB', 'NEW', '영광'처럼 일반 단어와 같은 종목명은 관련 없는 기사까지 태그되어 절대 건수가 부풀려집니다.
#   기준 구간도 같은 비율로 부풀려지므로 **증가 배수**로 쓰면 이 오탐이 상쇄됩니다.

# %%
def agg_by_symbol(category, section, date_from, date_to, size=3000):
    q = (f'DocumentAggregation(["{category}"],{json.dumps(section)},"*","securities.symbol:{size}",'
         f'date_from={date_from},date_to={date_to})')
    df = ds_df(q)
    if df.empty:
        return pd.Series(dtype=float)
    df = df[df["key"].str.fullmatch(r"\d{6}")]          # 상장사 6자리 코드만 (8자리는 DART 고유번호)
    return df.set_index("KRX:" + df["key"])["count"].astype(float)

disc_p = agg_by_symbol("company", ["disclosure"], period_days[0], period_days[-1])
news_p = agg_by_symbol("news", [], period_days[0], period_days[-1])
news_b = agg_by_symbol("news", [], base_days[0], base_days[-1])
print("태그된 종목 수 — 공시", len(disc_p), "/ 뉴스(기간)", len(news_p), "/ 뉴스(기준)", len(news_b))

m["disc"] = disc_p.reindex(m.index).fillna(0)
m["news_p"] = news_p.reindex(m.index).fillna(0)
m["news_b"] = news_b.reindex(m.index).fillna(0)
m["news_x"] = (m["news_p"] + 1) / (m["news_b"] + 1)

# %% [markdown]
# ## 4. 주목도 점수
# 각 지표를 전 종목 내 **백분위(0~100)**로 바꾼 뒤 가중 평균합니다. 수익률은 오른 쪽·내린 쪽 모두 주목이므로 절댓값을 씁니다.
# 점수는 종목 간 순위를 매기는 상대값입니다.

# %%
pct = pd.DataFrame({
    "ret": m["ret"].abs().rank(pct=True), "move": m["move"].rank(pct=True),
    "value_x": m["value_x"].rank(pct=True), "disc": m["disc"].rank(pct=True),
    "news_x": m["news_x"].rank(pct=True),
}) * 100
m["score"] = sum(pct[k] * w for k, w in WEIGHTS.items()) / sum(WEIGHTS.values())
top = m.sort_values("score", ascending=False).head(TOP).copy()
top["시총"] = top["mcap"].map(krw)
top["거래대금(억/일)"] = top["value_p"] / 1e8
print(PRICE_NOTICE)
top[["name", "market", "score", "ret", "move", "value_x", "거래대금(억/일)", "disc", "news_p", "news_x", "시총"]].round(1)

# %% [markdown]
# ## 5. 상위 종목의 공시 흐름
# 상위 종목을 묶어 한 번에 공시를 받아, 종목별로 시간순 제목을 이어 붙입니다.

# %%
codes = [s.split(":")[-1] for s in top.index]
_, docs = doc_search("company", ["disclosure"], "securities.symbol:(" + " or ".join(codes) + ")",
                     period_days[0], ASOF, count=100, pages=4)

def chain(code, n=4):
    if docs.empty:
        return "(공시 없음)"
    sub = docs[docs["symbols"].str.contains(code, na=False)].sort_values("created_at")
    t = sub["title"].drop_duplicates().tolist()
    return " → ".join(t[-n:]) if t else "(공시 없음)"

top["공시 흐름(최근 4건)"] = [chain(c) for c in codes]
top[["name", "score", "ret", "공시 흐름(최근 4건)"]].round(1)

# %%
ax = top.set_index("name")[["ret"]].rename(columns={"ret": "기간 수익률(%)"}).iloc[::-1].plot.barh(
    figsize=(7, 6), legend=False, title=f"주목도 상위 {TOP} — 기간 수익률 ({period_days[0]}~{period_days[-1]})")
ax.axvline(0, color="gray", lw=.8); ax.grid(alpha=.3, axis="x")

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 상위권은 **급등(또는 급락) + 거래 폭증 + 경보 공시**가 겹친 종목으로 채워집니다. 가중치(`WEIGHTS`)를 바꾸면
#   "거래대금 급증 위주", "뉴스 화제 위주"처럼 성격을 바꿀 수 있습니다.
# - 공시 건수에는 정기보고서·임원 지분 보고 같은 일상 공시도 섞입니다. 그래서 가중치를 시세 지표의 절반으로 두었습니다.
# - 뉴스 종목 태그는 동명 종목 오탐이 있습니다(위 3절). 뉴스 증가 배수는 이를 줄이지만 없애지는 못합니다.
# - 거래대금은 KRX 기준(NXT 미포함), 가격은 수정주가입니다.
