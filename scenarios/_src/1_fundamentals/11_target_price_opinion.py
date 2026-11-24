# %% [markdown]
# # 1-11 목표주가·투자의견 — 증권사 눈높이와 상승여력 (신규)
#
# **질문 예시:** "SK하이닉스 증권사 목표가 지금 얼마야? 최근에 내렸어?", "요즘 목표주가 올라간 종목 뭐야?"
#
# CHECK 데이터에는 목표주가·투자의견이 없어서 원본 시나리오들은 "전망치 리비전"으로 대신했습니다.
# DeepSearch에는 **증권사별 목표주가와 투자의견이 날짜별로** 있어서 직접 볼 수 있습니다.
#
# | 단계 | DeepSearch |
# |---|---|
# | 종목 하나의 목표가·의견 이력 | `SearchTargetPrices(종목, date_from, date_to)` — 증권사·애널리스트·목표가·의견·당시 주가 |
# | 시장 전체 목표가 변화 | `GetTargetPriceConsensusChange(relative_to, duration)` — **한 번 호출로 300여 종목** |
# | 현재가 | 전 종목 시세(`GetStockPrices`) |
#
# 투자의견 코드: 1~2 매도·비중축소(부정), 3 중립, 4~5 매수(긍정).

# %%
ASOF = "2026-11-24"
STOCK = "KRX:000660"      # SK하이닉스
WINDOW_DAYS = 90          # 이 기간 안에 낸 목표가만 컨센서스에 씀
print(PRICE_NOTICE)

# %% [markdown]
# ## 1. 한 종목의 목표가 컨센서스와 상승여력
# 증권사별로 **최근 90일 안에 낸 가장 최신 목표가**만 남겨 평균을 냅니다(같은 증권사가 여러 번 내면 마지막 것만).

# %%
asof = pd.Timestamp(ASOF)
tp = ds_df(f"SearchTargetPrices({STOCK}, date_from={(asof - pd.DateOffset(years=1)).date()}, date_to={ASOF})")
NAME = tp["entity_name"].iloc[0]
OPINION = {1: "매도", 2: "비중축소", 3: "중립", 4: "매수", 5: "적극매수"}
px = stock_prices(STOCK, (asof - pd.DateOffset(years=1)).date(), ASOF, columns=["close"]).set_index("date")["close"]
close = px.iloc[-1]

recent = tp[tp["date"] > asof - pd.Timedelta(days=WINDOW_DAYS)].sort_values("date").groupby("inst_code").tail(1)
cons = recent["target_price"].mean()
print(f"{NAME} 종가 {close:,.0f}원 ({px.index[-1].date()})")
print(f"목표가 컨센서스 {cons:,.0f}원 — 증권사 {len(recent)}곳, 범위 {recent['target_price'].min():,.0f} ~ {recent['target_price'].max():,.0f}원")
print(f"상승여력 {cons / close - 1:+.1%}")
print("투자의견:", recent["opinion_code"].map(OPINION).value_counts().to_dict())
recent.assign(의견=recent["opinion_code"].map(OPINION), 당시주가=recent["current_price"],
              목표가괴리=(recent["target_price"] / recent["current_price"] - 1).map("{:+.0%}".format))[
    ["date", "name_ko", "의견", "target_price", "당시주가", "목표가괴리"]].rename(columns={"name_ko": "증권사", "target_price": "목표가"})

# %% [markdown]
# ## 2. 목표가 이력과 주가
# 점 하나가 증권사 리포트 하나입니다. 선은 날짜마다 다시 계산한 90일 컨센서스입니다.

# %%
def cons_at(t):
    d = tp[(tp["date"] <= t) & (tp["date"] > t - pd.Timedelta(days=WINDOW_DAYS))]
    return d.sort_values("date").groupby("inst_code").tail(1)["target_price"].mean()

line = pd.Series({t: cons_at(t) for t in px.index})
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(px.index, px.values, label="종가(수정주가)", color="black", lw=1)
ax.plot(line.index, line.values, label="목표가 컨센서스(90일)", color="tab:red")
for code, g in tp.groupby("opinion_code"):
    ax.scatter(g["date"], g["target_price"], s=18, alpha=.6, label=f"리포트 목표가 ({OPINION.get(code, code)})")
ax.set_title(f"{NAME} 목표주가와 주가"); ax.legend(fontsize=8); ax.grid(alpha=.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v / 1e4:,.0f}만"))

# %% [markdown]
# ## 3. 증권사별 목표가 변경
# 같은 증권사가 목표가를 바꾼 기록만 모았습니다. 하향이 이어지면 눈높이가 내려가는 중입니다.

# %%
ch = tp.sort_values("date").copy()
ch["이전 목표가"] = ch.groupby("inst_code")["target_price"].shift()
ch = ch[ch["이전 목표가"].notna() & (ch["target_price"] != ch["이전 목표가"])]
ch["변경률"] = (ch["target_price"] / ch["이전 목표가"] - 1).map("{:+.1%}".format)
ch[["date", "name_ko", "이전 목표가", "target_price", "변경률"]].rename(
    columns={"name_ko": "증권사", "target_price": "새 목표가"}).tail(10)

# %% [markdown]
# ## 4. 시장 전체: 최근 1개월 목표가 상향·하향 종목
# `GetTargetPriceConsensusChange(relative_to=1, duration=3)`은 종목마다
# - `mean_after`: **지금** 기준 최근 3개월 안 증권사별 최신 목표가 평균
# - `mean_before`: **1개월 전** 기준 같은 평균
# 을 돌려줍니다(SK하이닉스로 직접 계산해 같은 값인지 확인함). **날짜 인자가 없어 항상 호출하는 날 기준**입니다.

# %%
chg = ds_df("GetTargetPriceConsensusChange(relative_to=1, duration=3)")
snap = all_stocks(ASOF)
m = chg.merge(snap[["symbol", "market", "close", "market_cap"]], on="symbol", how="inner")
m = m[(m["count_before"] >= 2) & (m["count_after"] >= 2)].copy()
m["목표가 변화"] = m["mean_after"] / m["mean_before"] - 1
m["상승여력"] = m["mean_after"] / m["close"] - 1
print(f"전체 {len(chg)}종목 중 앞뒤 모두 증권사 2곳 이상: {len(m)}종목 | 상향 {int((m['목표가 변화'] > 0).sum())} · 하향 {int((m['목표가 변화'] < 0).sum())} · 유지 {int((m['목표가 변화'] == 0).sum())}")

def view(df):
    out = df[["entity_name", "market", "mean_before", "mean_after", "목표가 변화", "count_after", "close", "상승여력", "market_cap"]].copy()
    out["목표가 변화"] = out["목표가 변화"].map("{:+.1%}".format)
    out["상승여력"] = out["상승여력"].map("{:+.0%}".format)
    out["market_cap"] = out["market_cap"].map(krw)
    for c in ("mean_before", "mean_after"):
        out[c] = out[c].round(-1).map("{:,.0f}".format)
    return out.rename(columns={"entity_name": "종목", "mean_before": "1개월 전", "mean_after": "현재", "count_after": "증권사", "close": "종가", "market_cap": "시가총액"})

print("■ 목표가 상향 상위")
display(view(m.sort_values("목표가 변화", ascending=False).head(15)))
print("■ 목표가 하향 상위")
display(view(m.sort_values("목표가 변화").head(10)))

# %% [markdown]
# ## 5. 상승여력이 큰 대형주
# 시가총액 5조 이상에서 목표가 컨센서스 대비 상승여력 순입니다. 목표가가 최근 하향 중인지 같이 봅니다.

# %%
big = m[m["market_cap"] >= 5e12].sort_values("상승여력", ascending=False)
view(big.head(15))

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **상승여력** = 목표가 컨센서스 ÷ 현재가 − 1. 증권사 목표가는 대체로 낙관적이라 절대 수준보다 **변화 방향**이 더 쓸모 있습니다.
# - 주가가 급락한 직후에는 목표가가 따라 내려오기 전이라 상승여력이 크게 부풀려 보입니다. 2026-11 기준 대형주 상승여력이 +100%를 넘는 것은 10~11월 급락(예: LG이노텍 57.2만→28.5만 원)을 목표가가 아직 반영하지 못했기 때문입니다(분할 등 주가 기준 문제는 아님을 리포트 당시 주가로 확인).
# - 투자의견은 대부분 "매수"(코드 4)라 변별력이 낮습니다. 의견 하향(4→3)이 나오면 드문 신호입니다.
# - DeepSearch가 받는 증권사는 종목당 수 곳이라 시장 전체 컨센서스(20곳 이상)와 숫자가 다를 수 있습니다.
# - 시장 전체 함수는 **오늘 기준만** 됩니다. 과거 시점의 상향·하향 목록이 필요하면 종목별 `SearchTargetPrices`로 1절처럼 계산해야 합니다.
# - 수정주가 기준이라 분할·증자가 있었던 종목은 과거 목표가와 현재가를 그대로 비교하면 안 됩니다.
