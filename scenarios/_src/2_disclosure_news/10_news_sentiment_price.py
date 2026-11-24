# %% [markdown]
# # 2-10 뉴스 관심도·감성 × 주가 — 뉴스가 몰린 날, 톤이 바뀐 날 주가는?
#
# **질문 예시:** "삼성전자·SK하이닉스·리노공업 최근 석 달 뉴스량이랑 감성 비교해줘", "뉴스가 갑자기 터진 날 주가는 어땠어?", "뉴스 톤이 좋아지면 다음 날 주가도 오르나?"
#
# CHECK 원본(`2_공시뉴스/06_뉴스커버리지감성`)을 **확장**한 시나리오입니다. CHECK 뉴스에는 종목 태그가 없어 키워드로 찾고 감성을 따로 계산해야 했지만,
# DeepSearch 뉴스에는 **종목 태그(`securities`)와 긍정·중립·부정 분류**가 붙어 있어 종목별 일자 집계를 함수 하나로 받습니다.
#
# | 단계 | DeepSearch 함수 |
# |---|---|
# | 종목 뉴스 일별 건수·긍부정 건수·감성점수 | `GetSentimentScore("securities.name:종목", interval="1d", …)` — 종목당 1회 |
# | 주가·거래대금 | `GetStockPrices([종목들], …)` — 1회 |
#
# `GetSentimentScore`의 `sentiment` = (긍정 − 부정) ÷ (긍정 + 중립 + 부정). 긍부정 분류가 붙은 기사만 셉니다(`total_count`는 분류 없는 기사까지 포함한 전체 건수).
#
# **종목 태그 vs 키워드:** `securities.name:종목` 태그는 그 종목이 **제목에 나오는 주제 기사**에 붙습니다(건수가 제목 검색과 거의 같음, 2026-11-25 확인).
# 그냥 `종목명`으로 찾으면 시황 기사 속 **단순 언급**까지 잡혀 몇 배~수십 배 많아집니다. 감성은 태그 기준(주제 기사)으로 보고, 두 건수를 나란히 둡니다.

# %%
ASOF = "2026-11-24"
START = "2026-09-01"
STOCKS = ["삼성전자", "SK하이닉스", "리노공업", "카카오게임즈", "에코프로비엠"]

# %% [markdown]
# ## 1. 데이터 받기

# %%
u = universe()
name2sym = dict(zip(u["name"], u["symbol"]))

sent = {}
for n in STOCKS:
    df = ds_df(f'GetSentimentScore("securities.name:{n}", interval="1d", date_from={START}, date_to={ASOF})')
    sent[n] = df.set_index("date")[["total_count", "no_positives", "no_neutral", "no_negatives", "sentiment"]].astype(float)

# 키워드(단순 언급 포함) 기사 수는 기간 합계만 받는다
mention = {n: ds_df(f'GetSentimentScore("{n}", interval="1M", date_from={START}, date_to={ASOF})')["total_count"].sum()
           for n in STOCKS}

px = stock_prices([name2sym[n] for n in STOCKS], START, ASOF, columns=["close", "value", "change_rate"])
px["name"] = px["symbol"].map({v: k for k, v in name2sym.items()})
print(PRICE_NOTICE)

# %% [markdown]
# 주말·휴일 뉴스는 **다음 거래일**로 합칩니다(월요일 주가는 주말 뉴스를 반영하므로).

# %%
def to_trading_days(s_df, days):
    pos = days.searchsorted(s_df.index)
    ok = pos < len(days)
    g = s_df[ok].groupby(days[pos[ok]]).sum(min_count=1)
    g["sentiment"] = (g["no_positives"] - g["no_negatives"]) / (g["no_positives"] + g["no_neutral"] + g["no_negatives"])
    return g

panel = []
for n in STOCKS:
    p = px[px["name"] == n].set_index("date").sort_index()
    g = to_trading_days(sent[n], p.index)
    panel.append(p[["close", "value", "change_rate"]].join(g, how="left").assign(name=n))
panel = pd.concat(panel)
panel["ret"] = panel["change_rate"] * 100
panel["next_ret"] = panel.groupby("name")["ret"].shift(-1)

# %% [markdown]
# ## 2. 커버리지 — 얼마나 많이, 어떤 톤으로
# **긍정·부정 비율**은 분류가 붙은 기사 중 비율입니다. **뉴스량·거래대금 상관**은 거래일별 기사 수와 거래대금의 상관계수로, CHECK 원본이 말한 "뉴스량 = 관심도 프록시"를 확인합니다.

# %%
cov = panel.groupby("name").apply(lambda g: pd.Series({
    "주제 기사(태그)": g["total_count"].sum(),
    "거래일 평균": g["total_count"].mean(),
    "최다일 기사": g["total_count"].max(),
    "긍정 비율": g["no_positives"].sum() / g[["no_positives", "no_neutral", "no_negatives"]].sum().sum(),
    "부정 비율": g["no_negatives"].sum() / g[["no_positives", "no_neutral", "no_negatives"]].sum().sum(),
    "평균 감성점수": g["sentiment"].mean(),
    "뉴스량·거래대금 상관": g["total_count"].corr(g["value"]),
    "기간 수익률(%)": (g["close"].iloc[-1] / g["close"].iloc[0] - 1) * 100,
}), include_groups=False).loc[STOCKS]
cov.insert(1, "언급 기사(키워드)", pd.Series(mention).astype(float))
cov.round(3)

# %% [markdown]
# ## 3. 뉴스 폭증일 — 그날과 다음 날 주가
# 폭증일 = 그 종목의 거래일 평균 기사 수의 **3배 이상이면서 평균 + 2표준편차 이상**인 날.

# %%
def bursts(g):
    m, s = g["total_count"].mean(), g["total_count"].std()
    b = g[(g["total_count"] >= 3 * m) & (g["total_count"] >= m + 2 * s)]
    return b.assign(평소=m)

bt = pd.concat([bursts(g) for _, g in panel.groupby("name")])
bt = bt.reset_index()[["name", "date", "평소", "total_count", "sentiment", "ret", "next_ret"]]
bt.columns = ["종목", "날짜", "평소(건/일)", "그날 기사", "그날 감성", "그날 수익률(%)", "다음날 수익률(%)"]
print(f"폭증일 {len(bt)}일 | 그날 |수익률| 평균 {bt['그날 수익률(%)'].abs().mean():.2f}% vs 전체 평균 {panel['ret'].abs().mean():.2f}%")
bt.round(2).sort_values("날짜")

# %% [markdown]
# 폭증일의 **절대 수익률**이 평소보다 크면, 뉴스량이 "큰 움직임이 있던 날"을 잘 잡는다는 뜻입니다(방향은 따로 봐야 합니다).

# %% [markdown]
# ## 4. 감성과 수익률 — 같은 날 vs 다음 날
# 같은 날 상관은 "주가가 오르면 좋은 기사가 나온다"(반응)도 섞여 있습니다. **다음 날 수익률**과의 상관이 예측력에 가깝습니다.
# 하루 주제 기사가 3건 미만인 날은 감성이 흔들려서 빼고, 남은 거래일이 20일 미만인 종목은 `표본 부족`으로 둡니다.

# %%
valid = panel[panel["total_count"] >= 3]
valid = valid[valid.groupby("name")["ret"].transform("size") >= 20]
print("표본 부족(제외):", ", ".join(sorted(set(STOCKS) - set(valid["name"]))) or "없음")
corr = valid.groupby("name").apply(lambda g: pd.Series({
    "표본(거래일)": len(g),
    "감성·당일수익률 상관": g["sentiment"].corr(g["ret"]),
    "감성·다음날수익률 상관": g["sentiment"].corr(g["next_ret"]),
    "감성 상위 1/3일 다음날 평균(%)": g.loc[g["sentiment"] >= g["sentiment"].quantile(2 / 3), "next_ret"].mean(),
    "감성 하위 1/3일 다음날 평균(%)": g.loc[g["sentiment"] <= g["sentiment"].quantile(1 / 3), "next_ret"].mean(),
}), include_groups=False)
corr.round(3)

# %% [markdown]
# ## 5. 한 종목 자세히 보기

# %%
PICK = "SK하이닉스"
g = panel[panel["name"] == PICK]
fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1, 1]})
axes[0].plot(g.index, g["close"], color="k"); axes[0].set_title(f"{PICK} 종가(수정주가)")
axes[1].bar(g.index, g["total_count"], color="#4f81bd"); axes[1].set_title("기사 수(주말·휴일분은 다음 거래일에 합산)")
axes[2].bar(g.index, g["sentiment"], color=["#c0504d" if v >= 0 else "#4f81bd" for v in g["sentiment"].fillna(0)])
axes[2].axhline(0, color="gray", lw=.5); axes[2].set_title("감성점수 (긍정-부정)/분류 기사")
for a in axes:
    a.grid(alpha=.3)
plt.tight_layout()

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **뉴스량은 관심도**입니다. 거래대금과의 상관이 높게 나오면 "뉴스가 많은 날 = 거래가 몰린 날"이라는 뜻이고, 폭증일은 큰 움직임과 겹칩니다.
# - **감성은 대부분 당일 반응**입니다. 같은 날 상관이 다음 날 상관보다 크면, 기사가 주가를 따라 쓰였다고 보는 편이 맞습니다. 몇 달·몇 종목 표본으로 예측력을 단정하지 마세요.
# - 긍부정은 DeepSearch 모델 분류이고, 최근 기사의 절반가량은 분류가 비어 있습니다(`total_count`와 긍정+중립+부정 합의 차이).
# - 종목 태그는 기사 본문에서 자동 추출됩니다. 동명 단어(예: "오리온")가 많은 종목은 태그가 섞일 수 있어 제목·본문을 표본으로 확인하세요.
