# %% [markdown]
# # 3-09 테마 바스켓 — 키워드로 테마주를 찾고 수익률을 지수와 비교
#
# **질문 예시:** "원전 테마주 최근 3개월 수익률 어때? 코스피보다 나았어?", "로봇 관련주 뭐가 있고 어떤 종목이 끌어올렸어?"
#
# 테마 키워드 하나로 ① 관련 상장사를 찾고, ② 그중 **그 테마로 주로 언급되는 종목**(순수도)을 골라 바스켓을 만든 뒤,
# ③ 바스켓 수익률을 코스피·코스닥과 비교하고 ④ 종목별 기여도를 봅니다.
#
# **왜 DeepSearch로 하나 (신규):** CHECK에는 업종 분류도 문서 태그도 없어 테마 종목을 고를 방법이 없습니다.
# DeepSearch는 문서 기반 연관 기업 검색(`FindAssociatedEntity`)과 뉴스 종목 태그 집계(`DocumentAggregation`)로
# 테마 구성 종목을 데이터로 정합니다.

# %%
ASOF = "2026-11-24"
THEMES = ["원전", "로봇"]      # 키워드를 바꿔 보세요 (예: "방산", "2차전지", "조선")
LOOKBACK_MONTHS = 3            # 수익률·뉴스 집계 기간
MIN_MENTIONS = 10              # 기간 중 테마 기사 최소 건수
MIN_PURITY = 0.05              # 그 종목 기사 중 테마 기사 비율 하한
BASKET_SIZE = 12
MAX_WEIGHT = 0.25              # 시총가중 바스켓의 한 종목 비중 상한
# 종목명이 일반 단어와 같아 관련 없는 기사까지 태그되는 종목(동명 오탐). 예: '미래산업'은 3개월 기사 4,244건으로
# 시가총액에 비해 비정상적으로 많고 '미래 산업'이라는 표현에 걸린 기사가 대부분입니다.
EXCLUDE = {"KRX:025560"}       # 미래산업

START = (pd.Timestamp(ASOF) - pd.DateOffset(months=LOOKBACK_MONTHS)).date()
print("기간", START, "~", ASOF)

# %% [markdown]
# ## 1. 후보 종목: 연관 기업 검색 + 테마 기사 종목 집계
# - `FindAssociatedEntity(키워드, N, date_from, date_to)`: 공시·뉴스·리포트를 바탕으로 한 연관도 점수(0~100)
# - **순수도** = (테마 키워드가 들어간 그 종목 기사 수) ÷ (그 종목 전체 기사 수). 기사 수는 `DocumentAggregation`으로 전 종목을 한 번에 셉니다.
# - **테마 점수** = 테마 기사 수 × 순수도. 기사가 많으면서 그 테마로 주로 언급되는 종목이 위로 옵니다.
#   (기사 수만 쓰면 현대차·삼성전자 같은 대형주가, 순수도만 쓰면 기사 몇 건뿐인 소형주가 위로 옵니다.)

# %%
def agg_news(query, size=3000):
    df = ds_df(f'DocumentAggregation(["news"],[],{json.dumps(query, ensure_ascii=False)},'
               f'"securities.symbol:{size}",date_from={START},date_to={ASOF})')
    df = df[df["key"].str.fullmatch(r"\d{6}")]
    return df.set_index("KRX:" + df["key"])["count"].astype(float)

all_news = agg_news("*")          # 종목별 전체 기사 수 (테마 공통)
u = universe()
# 일반법인(1)·공기업(2) 보통주. 공기업(한국전력·한전기술 등)은 company_type_l1이 "2"라 "1"만 거르면 빠집니다.
common = u[u["company_type_l1"].isin(["1", "2"]) & u["symbol"].str.endswith("0")].set_index("symbol")

def candidates(theme):
    fae = ds_df(f'FindAssociatedEntity({json.dumps(theme, ensure_ascii=False)}, 40, date_from={START}, date_to={ASOF})')
    fae = fae.set_index("symbol").iloc[:, -1].rename("연관점수")
    theme_news = agg_news(f'"{theme}"', size=300).rename("테마기사")
    c = pd.concat([fae, theme_news], axis=1)
    c = c[c.index.isin(common.index) & ~c.index.isin(EXCLUDE)]
    c["전체기사"] = all_news.reindex(c.index)
    c["순수도"] = c["테마기사"] / c["전체기사"]
    c["테마점수"] = c["테마기사"] * c["순수도"]
    c.insert(0, "name", common.loc[c.index, "name"])
    c.insert(1, "market", common.loc[c.index, "market"])
    return c

cands = {t: candidates(t) for t in THEMES}
for t, c in cands.items():
    print(f"[{t}] 후보 {len(c)}개 (연관검색 {c['연관점수'].notna().sum()}, 테마기사 집계 {c['테마기사'].notna().sum()})")

# %% [markdown]
# ## 2. 바스켓 구성
# 테마 기사 `MIN_MENTIONS`건 이상, 순수도 `MIN_PURITY` 이상인 종목을 테마 점수 순으로 `BASKET_SIZE`개 고릅니다.
# 연관 점수는 높지만 테마 비중이 낮아 빠진 종목도 함께 보여 줍니다.

# %%
baskets = {}
for t, c in cands.items():
    ok = c[(c["테마기사"] >= MIN_MENTIONS) & (c["순수도"] >= MIN_PURITY)]
    baskets[t] = ok.sort_values("테마점수", ascending=False).head(BASKET_SIZE)
    dropped = c[c["연관점수"].notna() & ~c.index.isin(baskets[t].index)].sort_values("연관점수", ascending=False).head(5)
    print(f"\n[{t}] 바스켓 {len(baskets[t])}종목 / 연관 점수는 높지만 제외된 예: "
          + ", ".join(f"{r.name_}({r.순수도:.0%})" for r in dropped.rename(columns={"name": "name_"}).itertuples()))

baskets[THEMES[0]][["name", "market", "테마점수", "테마기사", "전체기사", "순수도", "연관점수"]].round(2)

# %%
baskets[THEMES[1]][["name", "market", "테마점수", "테마기사", "전체기사", "순수도", "연관점수"]].round(2)

# %% [markdown]
# ## 3. 바스켓 수익률 vs 지수
# 바스켓 종목 시세를 한 번에 받아(`GetStockPrices([종목…])`) 동일가중·시가총액가중 누적수익률을 계산하고 코스피·코스닥과 비교합니다.
# 둘 다 시작일 비중으로 사고 그대로 두는 방식(리밸런싱 없음)이고, 시총가중은 한 종목 비중을 `MAX_WEIGHT`로 제한합니다.

# %%
idx = index_prices(START, ASOF)
idx = idx[idx["symbol"].isin(["KRX:KOSPI", "KRX:KOSDAQ"])].pivot(index="date", columns="entity_name", values="close")
curves = {f"{n} 지수": idx[n] / idx[n].iloc[0] - 1 for n in idx.columns}
contrib = {}

for t, b in baskets.items():
    px = stock_prices(list(b.index), START, ASOF, columns=["close", "market_cap"])
    close = px.pivot(index="date", columns="symbol", values="close").sort_index().ffill()
    mcap0 = px.sort_values("date").groupby("symbol")["market_cap"].first()
    close = close.dropna(axis=1, subset=[close.index[0]])      # 기간 중 상장 종목 제외
    rel = close / close.iloc[0]
    w = mcap0.reindex(rel.columns); w = w / w.sum()
    for _ in range(20):                                         # 비중 상한 적용 후 다시 나눠 맞춤
        over = w > MAX_WEIGHT
        if not over.any():
            break
        w[over] = MAX_WEIGHT
        w[~over] = w[~over] / w[~over].sum() * (1 - MAX_WEIGHT * over.sum())
    curves[f"{t} 동일가중"] = rel.mean(axis=1) - 1
    curves[f"{t} 시총가중"] = (rel * w).sum(axis=1) - 1
    r = rel.iloc[-1] - 1
    contrib[t] = pd.DataFrame({"name": b.loc[r.index, "name"], "수익률(%)": r * 100,
                               "시총비중(%)": w * 100, "시총가중 기여(%p)": r * w * 100}).sort_values("시총가중 기여(%p)", ascending=False)

perf = pd.DataFrame(curves)
print(PRICE_NOTICE)
(perf.iloc[[-1]].T * 100).round(1).rename(columns=lambda c: f"누적수익률(%) {c:%Y-%m-%d}")

# %%
ax = (perf * 100).plot(figsize=(9, 4.5), title=f"테마 바스켓 vs 지수 누적수익률 ({START} ~ {ASOF})")
ax.set_ylabel("%"); ax.axhline(0, color="gray", lw=.8); ax.grid(alpha=.3)

# %% [markdown]
# ## 4. 종목별 기여도
# 시총가중 수익률 = Σ(시작 시총 비중 × 종목 수익률). 누가 바스켓을 끌어올렸는지 봅니다.

# %%
contrib[THEMES[0]].round(1)

# %%
contrib[THEMES[1]].round(1)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 테마 구성은 **기사 언급 기반**이라 기간을 바꾸면 종목이 달라집니다. 순수도 하한을 낮추면 대형주가 들어오고
#   시총가중 수익률이 지수와 비슷해집니다.
# - 뉴스 종목 태그에는 동명 종목 오탐(예: 'DB', '미래산업')이 있습니다. 전체 기사 수가 회사 규모에 비해 지나치게 많으면
#   기사를 확인하고 `EXCLUDE`에 넣으세요. 다른 회사 이야기에 함께 언급된 계열사(예: 원전 기사 속 두산로보틱스)도 섞일 수 있습니다.
# - 현재 상장 종목 기준이라 기간 중 상장폐지된 종목은 빠지고(생존 편향), 기간 중 신규 상장 종목은 수익률 계산에서 제외합니다.
# - 가격은 수정주가(배당 미반영)라 총수익률이 아닌 가격수익률입니다.
