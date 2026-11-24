# %% [markdown]
# # 2-03 공매도 과열종목 지정 — 지정 전후 주가·거래량
#
# **질문 예시:** "이번 달 공매도 과열로 지정된 종목들, 지정 뒤 주가 어떻게 됐어?", "공매도 과열 지정이 많은 날은 시장이 빠진 날이야?"
#
# CHECK 원본(`2_공시뉴스/03_공매도과열`)은 **공매도 거래대금·잔고비중**으로 "왜 지정됐고 지정 후 공매도가 얼마나 줄었나"를 봤습니다.
# DeepSearch에는 공매도 수치가 없어서(`research/data_gaps`), **지정 공시**와 **주가·거래량**만으로 다시 짭니다.
#
# | 단계 | DeepSearch 함수 |
# |---|---|
# | 지정 공시 모으기 | `DocumentSearch(["company"],["disclosure"], 'title:"공매도 과열"')` — 유가증권·코스닥시장본부 공시 |
# | 지정 전후 주가·거래량 | `GetStockPrices([종목들], …)` 한 번 |
# | 시장 대비 | `GetMarketIndexes` |
# | 날짜별 지정 건수 | `DocumentTrends(… interval="1d")` |
#
# **각색한 점**
# - 공매도 거래대금·잔고·대차는 없습니다. "지정 직전 공매도 급증"은 볼 수 없고, 대신 **트리거일의 주가 낙폭·거래량 배수**를 봅니다.
# - 거래소 시장 공시(공매도 과열·시장경보)는 **2026년 8월부터** 촘촘히 들어 있습니다(그 전은 월 10건 안팎).
#   CHECK 예시(6월 리노공업·솔브레인·에스원)는 DeepSearch에 없어 **최근 한 달 지정 종목 전체**로 바꿨습니다.

# %%
ASOF = "2026-11-24"
FROM = "2026-10-27"        # 지정 공시를 모을 기간 (약 한 달)

# %% [markdown]
# ## 1. 지정 공시 모으기
# 제목이 `공매도 과열종목 지정`이면 신규 지정, `연장`이면 지정 연장입니다. 공시는 대개 장 마감 뒤 20시께 나오고, **다음 거래일부터** 공매도가 금지됩니다.

# %%
total, d = doc_search("company", ["disclosure"], 'title:"공매도 과열"', FROM, ASOF, count=100, pages=4)
d["구분"] = d["title"].str.contains("연장").map({True: "연장", False: "지정"})
d["시장"] = d["publisher"].map({"유가증권시장본부": "KOSPI", "코스닥시장본부": "KOSDAQ"})
print(f"공매도 과열 공시 {total}건 (받은 것 {len(d)}건)")
print(pd.crosstab(d["시장"], d["구분"], margins=True, margins_name="합계"))
print(f"종목 태그가 없는 공시: {(d['symbols'] == '').sum()}건 — 제목에 우선주 이름만 있거나 태그 누락. 이 노트북에서는 뺍니다.")

# %% [markdown]
# ## 2. 트리거일 정하기
# 20시 공시는 **그날 거래**를 보고 지정한 것이라 공시일을 트리거일 **T**로 둡니다. 장 시작 전(09:30 이전) 공시는 직전 거래일을 T로 봅니다.
# 같은 종목이 기간 안에 여러 번 지정됐으면 **첫 신규 지정**만 씁니다.

# %%
ev = d[(d["구분"] == "지정") & (d["symbols"] != "")].copy()
ev["symbol"] = "KRX:" + ev["symbols"].str.split(", ").str[0]     # 공시 종목코드엔 KRX: 접두어가 없다
ev["종목"] = ev["stocks"].str.split(", ").str[0]
ev = ev.sort_values("created_at").drop_duplicates("symbol")
repeat = d[d["symbols"] != ""].groupby("stocks").size().sort_values(ascending=False)
print(f"신규 지정 종목 {len(ev)}개 | 기간 중 공시가 3건 이상(지정+연장 반복)인 종목:",
      ", ".join(f"{k}({v})" for k, v in repeat[repeat >= 3].items()) or "없음")

p_from = (pd.Timestamp(FROM) - pd.Timedelta(days=45)).date()
px = stock_prices(ev["symbol"].tolist(), p_from, ASOF)

def market_index(d1, d2):
    """GetMarketIndexes 는 긴 기간이면 최근 약 1,300행만 주므로 90일씩 나눠 받는다."""
    parts, cur, end = [], pd.Timestamp(d1), pd.Timestamp(d2)
    while cur <= end:
        nxt = min(cur + pd.Timedelta(days=89), end)
        parts.append(index_prices(cur.date(), nxt.date()))
        cur = nxt + pd.Timedelta(days=1)
    i = pd.concat(parts).drop_duplicates(["date", "symbol"])
    return i[i["symbol"].isin(["KRX:KOSPI", "KRX:KOSDAQ"])].pivot_table(index="date", columns="symbol", values="close")

idx = market_index(p_from, ASOF)
print(PRICE_NOTICE)
print(f"시세 {len(px):,}행")

# %% [markdown]
# ## 3. 지정 전후 반응
# - **T 수익률·거래량 배수**: 트리거일 하루 등락과, 그날 거래량 ÷ 직전 20거래일 평균. 지정 사유(급락·공매도 급증)의 그림자입니다.
# - **T+1, T+3, T+5**: 공매도 금지가 적용된 뒤의 수익률(T 종가 대비). **초과**는 같은 기간 해당 시장 지수 수익률을 뺀 값.

# %%
rows = []
for _, e in ev.iterrows():
    s = px[px["symbol"] == e["symbol"]].set_index("date").sort_index()
    if s.empty:
        continue
    t_day = pd.Timestamp(e["created_at"].date())
    if e["created_at"].hour * 100 + e["created_at"].minute < 930:
        t_day -= pd.Timedelta(days=1)
    pos = s.index.searchsorted(t_day, side="right") - 1       # T = t_day 이하 마지막 거래일
    if pos < 20:
        continue
    close, vol = s["close"], s["volume"]
    mi = idx[f"KRX:{e['시장']}"].reindex(s.index)
    r = {"종목": e["종목"], "시장": e["시장"], "T": s.index[pos].date(),
         "T 수익률": (close.iloc[pos] / close.iloc[pos - 1] - 1) * 100,
         "T 지수": (mi.iloc[pos] / mi.iloc[pos - 1] - 1) * 100,
         "T 거래량배수": vol.iloc[pos] / vol.iloc[pos - 20:pos].mean(),
         "T-5~T 수익률": (close.iloc[pos] / close.iloc[pos - 5] - 1) * 100}
    for h in (1, 3, 5):
        if pos + h < len(s):
            rr = close.iloc[pos + h] / close.iloc[pos] - 1
            r[f"T+{h}"] = rr * 100
            r[f"초과 T+{h}"] = (rr - (mi.iloc[pos + h] / mi.iloc[pos] - 1)) * 100
    rows.append(r)
res = pd.DataFrame(rows)
res.round(1).sort_values("T", ascending=False).head(15)

# %% [markdown]
# ### 요약 통계
# 지정 후 5거래일이 지나지 않은 최근 지정은 T+5가 비어 있어 평균에서 빠집니다.

# %%
summary = pd.DataFrame({
    "종목 수": res.groupby("시장").size(),
    "T 수익률 중앙값(%)": res.groupby("시장")["T 수익률"].median(),
    "T 하락 비율": res.groupby("시장")["T 수익률"].apply(lambda x: (x < 0).mean()),
    "T 거래량배수 중앙값": res.groupby("시장")["T 거래량배수"].median(),
    "T+1 평균(%)": res.groupby("시장")["T+1"].mean(),
    "T+5 평균(%)": res.groupby("시장")["T+5"].mean(),
    "초과 T+5 평균(%p)": res.groupby("시장")["초과 T+5"].mean(),
    "T+5 상승 비율": res.groupby("시장")["T+5"].apply(lambda x: (x.dropna() > 0).mean()),
})
summary.round(2)

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(res["T 수익률"], bins=25, color="#c0504d")
axes[0].set_title("트리거일(T) 등락률 분포"); axes[0].set_xlabel("%")
axes[1].hist(res["초과 T+5"].dropna(), bins=25, color="#4f81bd")
axes[1].axvline(0, color="k", lw=.8)
axes[1].set_title("지정 후 5거래일 초과수익 분포"); axes[1].set_xlabel("%p")
for a in axes:
    a.grid(alpha=.3)

# %% [markdown]
# ## 4. 시장 전체: 지정이 몰린 날은 시장이 빠진 날인가
# 날짜별 신규 지정 공시 건수(`DocumentTrends`)를 코스닥 지수 등락률과 나란히 봅니다. 기간은 수집이 촘촘해진 2026-08 이후입니다.

# %%
cnt = doc_trends("company", ["disclosure"], 'title:"공매도 과열종목 지정"', "2026-08-01", ASOF, interval="1d")
k = market_index("2026-07-25", ASOF)["KRX:KOSDAQ"].pct_change() * 100
m = cnt.set_index("date")["count"].to_frame("지정 공시").join(k.rename("코스닥 등락률(%)"), how="inner").dropna()
m = m[m.index.dayofweek < 5]
print(f"거래일 {len(m)}일, 상관계수 {m['지정 공시'].corr(m['코스닥 등락률(%)']):.2f}")
print("지정 공시가 많았던 날 상위 5:")
print(m.sort_values("지정 공시", ascending=False).head(5).round(2).to_string())

# %%
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.bar(m.index, m["지정 공시"], color="#9bbb59", label="공매도 과열 지정 공시(건)")
ax2 = ax.twinx()
ax2.plot(m.index, m["코스닥 등락률(%)"], color="#c0504d", lw=1, label="코스닥 등락률(%)")
ax2.axhline(0, color="gray", lw=.5)
ax.set_title("날짜별 공매도 과열 지정 vs 코스닥 등락률"); ax.grid(alpha=.3)
fig.legend(loc="upper left", bbox_to_anchor=(0.07, 0.88), fontsize=8);

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 공매도 과열 지정 기준에는 **주가 급락**과 **공매도 비중·거래대금 급증**이 들어 있습니다. DeepSearch로는 주가 쪽만 보이므로, T일 급락과 거래량 폭증이 "지정 사유의 그림자"입니다.
# - **공매도 거래대금이 지정 뒤 얼마나 줄었는지, 잔고가 언제 풀리는지는 이 데이터로 답할 수 없습니다.** 필요하면 CHECK API나 KRX 정보데이터시스템을 쓰세요.
# - 거래소 시장 공시는 2026-08 이전엔 일부만 들어 있어 과거 사례 연구에는 쓰기 어렵습니다.
# - 공시의 10% 안팎은 종목 태그가 없어 빠졌습니다(주로 우선주). 본문을 읽어 종목을 채우는 방법은 `2-05 공시 본문`에서 다룹니다.
