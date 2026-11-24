# %% [markdown]
# # 2-12 오늘의 이슈 토픽 — 지금 시장에서 뭐가 화제고, 관련 종목은 어떻게 움직였나
#
# **질문 예시:** "지금 경제 뉴스에서 제일 큰 이슈 뭐야? 요약해줘", "그 이슈 관련 종목 주가는?", "SK하이닉스 최근 두 달 주요 이슈를 주가랑 같이 타임라인으로 보여줘"
#
# CHECK API 뉴스는 종목·키워드로 기사를 찾는 방식이라 "무엇이 화제인가"를 직접 주지 않습니다. DeepSearch는 기사를 **토픽(이슈)으로 묶고**,
# 토픽마다 **AI 요약(인사이트)**까지 줘서 새로 만든 시나리오입니다.
#
# | 단계 | DeepSearch 함수 |
# |---|---|
# | 지금 뜨는 토픽 | `SearchTrendingTopics(["news"], ["economy"])` — 실행 시점 기준 |
# | 토픽 기사 | `GetTrendingTopic(["news"], ["economy"], 토픽uid, count=20)` |
# | 토픽 요약·예상 질문 | REST `GET /v1/topic-insight/insight`, `/questions` (같은 API 키) |
# | 종목의 과거 이슈 타임라인 | `SearchHistoricalTopics(["news"], ["economy"], "종목", …)` |
# | 관련 종목 주가 | `GetStockPrices` |
#
# ⚠️ 트렌딩 토픽은 **실행할 때마다 바뀝니다.** 아래 출력은 2026-11-25 새벽(06시대) 실행 결과입니다.

# %%
ASOF = "2026-11-24"          # 주가 기준일 (토픽은 실행 시점)
SECTIONS = ["economy", "tech"]
STOCK = "SK하이닉스"          # 4절 타임라인 종목
T_FROM = "2026-09-15"

# %% [markdown]
# ## 1. 지금 뜨는 토픽

# %%
def trending(section):
    c = _pod(ds(f'SearchTrendingTopics(["news"], ["{section}"])'))["content"]["data"]
    return c["timestamp"], c["topics"]["news"][section]

topics = []
for sec in SECTIONS:
    ts, tl = trending(sec)
    for t in tl:
        topics.append({"섹션": sec, "순위": t["rank"], "uid": t["uid"], "토픽": t["topic"],
                       "기사 수": t["statistics"]["doc_count"],
                       "키워드": ", ".join(k["keyword"] for k in t["keywords"][:5]),
                       "태그 종목": ", ".join(s.get("name", "") for s in t["statistics"]["securities"])})
topics = pd.DataFrame(topics)
print("토픽 기준 시각:", ts)
topics.drop(columns="uid")

# %% [markdown]
# ## 2. 1위 토픽 요약과 예상 질문 (토픽 인사이트)
# compute 함수가 아니라 별도 REST 주소지만 같은 키로 됩니다. 요약은 DeepSearch의 생성형 AI가 만든 글이라, 숫자는 원문 기사로 확인하세요.

# %%
def insight(kind, section, uid):
    r = requests.get(f"https://api.deepsearch.com/v1/topic-insight/{kind}",
                     params={"type": "trending", "section": section, "topicId": uid, "stream": "false"},
                     headers={"Authorization": "Basic " + _KEY}, timeout=180)
    j = r.json()
    return j.get("data") if j.get("success") else f"(실패: {r.status_code} {str(j)[:200]})"

top1 = topics.iloc[0]
print(f"[{top1['섹션']} 1위] {top1['토픽']}\n")
print(insight("insight", top1["섹션"], top1["uid"]))
print("\n--- 예상 질문 ---")
print(insight("questions", top1["섹션"], top1["uid"]))

# %% [markdown]
# ## 3. 토픽별 관련 종목과 주가
# 토픽 기사(최대 20건)에 붙은 **종목 태그**를 세고, 그 종목의 기준일 등락률과 5거래일 수익률을 붙입니다.

# %%
rows = []
for _, t in topics.iterrows():
    c = _pod(ds(f'GetTrendingTopic(["news"], ["{t["섹션"]}"], {t["uid"]}, count=20)'))["content"]["data"]
    docs = c["topics"]["news"][t["섹션"]][0].get("docs") or []
    for d in docs:
        for s in d.get("securities") or []:
            if s.get("symbol"):
                rows.append({"섹션": t["섹션"], "순위": t["순위"], "토픽": t["토픽"][:30],
                             "symbol": "KRX:" + str(s["symbol"]), "종목": s.get("name")})
rel = pd.DataFrame(rows)
if rel.empty:
    print("토픽 기사에 종목 태그가 없습니다.")
else:
    rel = rel.groupby(["섹션", "순위", "토픽", "symbol", "종목"]).size().rename("기사 수").reset_index()
    px = stock_prices(rel["symbol"].unique().tolist(), (pd.Timestamp(ASOF) - pd.Timedelta(days=14)).date(), ASOF,
                      columns=["close", "change_rate", "market_cap"])
    last = px.sort_values("date").groupby("symbol").tail(6)
    perf = last.groupby("symbol").apply(lambda g: pd.Series({
        "기준일": g["date"].iloc[-1].date(), "등락률(%)": g["change_rate"].iloc[-1] * 100,
        "5일 수익률(%)": (g["close"].iloc[-1] / g["close"].iloc[0] - 1) * 100,
        "시가총액": krw(g["market_cap"].iloc[-1])}), include_groups=False)
    print(PRICE_NOTICE)
    out = rel.merge(perf, left_on="symbol", right_index=True, how="left").sort_values(["섹션", "순위", "기사 수"], ascending=[True, True, False])
    display(out.drop(columns="symbol").round(2))

# %% [markdown]
# ## 4. 종목의 이슈 타임라인 × 주가
# `SearchHistoricalTopics`는 날짜별로 묶인 과거 토픽을 줍니다. 종목 이름으로 찾아 **주가가 크게 움직인 날의 토픽**을 나란히 봅니다.

# %%
hist, total = [], None
for page in range(1, 9):                      # 한 번에 30건씩 온다 → 최대 8페이지(240건)
    c = _pod(ds(f'SearchHistoricalTopics(["news"], ["economy"], "{STOCK}", count=30, page={page}, '
                f'date_from={T_FROM}, date_to={ASOF})'))["content"]["data"]
    total = c["total_matches"]
    hist += c["topics"]                       # 과거 토픽은 섹션 구분 없이 바로 목록
    if len(hist) >= total or not c["topics"]:
        break
ht = pd.DataFrame([{"date": pd.Timestamp(t["date"]), "토픽": t["topic"], "score": t["score"]} for t in hist])
c = {"total_matches": total}
print(f"'{STOCK}' 과거 토픽 {c['total_matches']}건 중 {len(ht)}건 받음, {ht['date'].min().date()} ~ {ht['date'].max().date()}")

sym = universe().set_index("name").loc[STOCK, "symbol"]
sp = stock_prices(sym, T_FROM, ASOF, columns=["close", "change_rate"]).set_index("date")
sp["등락률(%)"] = sp["change_rate"] * 100
big = sp.reindex(sp["등락률(%)"].abs().sort_values(ascending=False).index).head(6)
for d, r in big.sort_index().iterrows():
    same = ht[ht["date"] == d].sort_values("score", ascending=False)["토픽"].head(3).tolist()
    print(f"{d.date()}  {r['등락률(%)']:+6.2f}%  | " + (" / ".join(same) if same else "(그날 토픽 없음)"))

# %%
daily = ht.groupby("date").size()
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(sp.index, sp["close"], color="k")
ax.set_ylabel("종가(수정주가)")
ax2 = ax.twinx()
ax2.bar(daily.index, daily.values, color="#4f81bd", alpha=.35, width=.8)
ax2.set_ylabel("그날 토픽 수")
for d in big.index:
    ax.axvline(d, color="#c0504d", alpha=.4, ls="--")
ax.set_title(f"{STOCK} 주가와 이슈 토픽 수 (빨간 점선: 등락률 상위 6일)"); ax.grid(alpha=.3)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **트렌딩 토픽은 지금 이 순간의 순위**입니다. 같은 노트북을 다시 실행하면 토픽이 바뀝니다. 과거 특정일의 토픽은 4절처럼 `SearchHistoricalTopics`로 봅니다.
# - 토픽 요약(인사이트)은 생성형 AI 요약입니다. 사실관계·숫자는 토픽 기사 원문으로 확인하세요.
# - 거시·업황 토픽은 종목 태그가 없는 경우가 많습니다. 관련 종목이 비면 키워드로 `DocumentSearch`를 따로 돌리세요.
# - 4절의 토픽은 종목명이 들어간 이슈만 잡히고, 하루에 여러 토픽이 겹칠 수 있습니다. 큰 등락의 "원인"이 아니라 "그날 무슨 이야기가 있었나"로 읽으세요.
