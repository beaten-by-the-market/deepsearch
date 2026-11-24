# %% [markdown]
# # 2-01 공시 이벤트 스터디 — 공시 뒤 주가·거래량은 어떻게 움직였나
#
# **질문 예시:** "가온전선 무상증자 공시 나고 주가 어떻게 됐어?", "지난달 무상증자 낸 종목들 공시 후 5일 수익률 비교해줘"
#
# CHECK 원본(`2_공시뉴스/01_공시이벤트스터디`)과 같은 6개 공시(2026년 6월)를 DeepSearch로 다시 봅니다.
#
# | 단계 | DeepSearch 함수 |
# |---|---|
# | 공시 찾기(제목·시각) | `DocumentSearch(["company"],["disclosure"], "securities.name:종목 and title:키워드")` |
# | 주가·거래량 | `GetStockPrices([종목들], …)` — 여러 종목을 한 번에 |
# | 시장 대비 초과수익 | `GetMarketIndexes` (코스피·코스닥) |
#
# **각색한 점:** DeepSearch에는 투자자별 수급(외국인·기관·개인)이 없어 "누가 샀나" 열은 뺐습니다.
# 대신 **시장(지수) 대비 초과수익**과 **공시 시각(장중/장후)**을 붙였습니다.

# %%
ASOF = "2026-11-24"

# (종목명, 제목 키워드, 검색 시작, 검색 끝) — CHECK 원본과 같은 사건
EVENTS = [
    ("가온전선", "무상증자", "2026-06-10", "2026-06-26"),
    ("카카오게임즈", "최대주주변경", "2026-06-10", "2026-06-26"),
    ("미래에셋증권", "자기주식취득", "2026-06-10", "2026-06-26"),
    ("제테마", "전환사채", "2026-06-10", "2026-06-26"),
    ("KB금융", "현금ㆍ현물배당결정", "2026-06-10", "2026-06-26"),
    ("오리온", "잠정", "2026-06-10", "2026-06-26"),
]
HORIZONS = [0, 1, 2, 5, 10]   # D0(공시 이상 첫 거래일), D+1 … 누적수익률 기준점은 D-1 종가

# %% [markdown]
# ## 1. 공시 찾기
# 종목별로 기간 안에서 제목에 키워드가 든 **가장 이른 공시**를 이벤트로 잡습니다(정정공시는 제외).

# %%
u = universe()
name2sym = dict(zip(u["name"], u["symbol"]))
name2mkt = dict(zip(u["name"], u["market"]))

ev_rows = []
for name, kw, d1, d2 in EVENTS:
    total, docs = doc_search("company", ["disclosure"], f"securities.name:{name} and title:{kw}", d1, d2, count=20)
    docs = docs[~docs["title"].str.contains("정정")].sort_values("created_at")
    if docs.empty:
        print("공시 없음:", name, kw)
        continue
    d = docs.iloc[0]
    ev_rows.append({"종목": name, "symbol": name2sym[name], "시장": name2mkt[name],
                    "공시": d["title"], "공시시각": d["created_at"], "url": d["url"]})
events = pd.DataFrame(ev_rows)
events[["종목", "시장", "공시", "공시시각"]]

# %% [markdown]
# ## 2. 주가·거래량 받기 (한 번에)
# 공시일 앞 30거래일(거래량 평소 수준 계산용)부터 뒤 15거래일까지 받습니다.

# %%
p_from = (events["공시시각"].min() - pd.Timedelta(days=50)).date()
p_to = (events["공시시각"].max() + pd.Timedelta(days=25)).date()
px = stock_prices(events["symbol"].tolist(), p_from, p_to)
def market_index(d1, d2):
    """코스피·코스닥 종가. GetMarketIndexes 는 긴 기간이면 최근 약 1,300행(≈118거래일)만 주고
    앞을 잘라내므로(2026-11-25 확인) 90일씩 나눠 받는다."""
    parts, cur, end = [], pd.Timestamp(d1), pd.Timestamp(d2)
    while cur <= end:
        nxt = min(cur + pd.Timedelta(days=89), end)
        parts.append(index_prices(cur.date(), nxt.date()))
        cur = nxt + pd.Timedelta(days=1)
    i = pd.concat(parts).drop_duplicates(["date", "symbol"])
    return i[i["symbol"].isin(["KRX:KOSPI", "KRX:KOSDAQ"])].pivot_table(index="date", columns="symbol", values="close")

idx = market_index(p_from, p_to)
print(PRICE_NOTICE)
print(f"시세 {len(px):,}행, 기간 {p_from} ~ {p_to}")

# %% [markdown]
# ## 3. 이벤트 스터디
# - **D0** = 공시일 이상 첫 거래일 (CHECK와 같은 정의). 15:30 이후 공시는 실제 반응이 D+1부터일 수 있어 `장후` 표시를 붙입니다.
# - **누적수익률** = D-1 종가 대비. **초과수익** = 같은 기간 해당 시장 지수 수익률을 뺀 값.
# - **거래량 배수** = D0~D+5 중 최대 거래량 ÷ D-20~D-1 평균 거래량.

# %%
def event_study(px, idx, sym, when, market, horizons=HORIZONS):
    s = px[px["symbol"] == sym].set_index("date").sort_index()
    days = s.index
    d0_pos = days.searchsorted(pd.Timestamp(when.date()))
    if d0_pos == 0 or d0_pos >= len(days):
        return None
    base = s["close"].iloc[d0_pos - 1]
    ibase = idx[f"KRX:{market}"].reindex(days).iloc[d0_pos - 1]
    out = {"D0": days[d0_pos].date()}
    for h in horizons:
        if d0_pos + h < len(days):
            r = s["close"].iloc[d0_pos + h] / base - 1
            ir = idx[f"KRX:{market}"].reindex(days).iloc[d0_pos + h] / ibase - 1
            out[f"D+{h}"] = round(r * 100, 1)
            out[f"초과 D+{h}"] = round((r - ir) * 100, 1)
    vol_base = s["volume"].iloc[max(0, d0_pos - 20):d0_pos].mean()
    win = s["volume"].iloc[d0_pos:d0_pos + 6]
    out["거래량 최대배수"] = round(win.max() / vol_base, 1)
    out["최대배수일"] = f"D+{int(win.values.argmax())}"
    return out

rows = []
for _, e in events.iterrows():
    r = event_study(px, idx, e["symbol"], e["공시시각"], e["시장"])
    if r:
        rows.append({"종목": e["종목"], "공시": e["공시"][:22], "시각": e["공시시각"].strftime("%m-%d %H:%M"),
                     "장후": e["공시시각"].hour * 100 + e["공시시각"].minute >= 1530, **r})
res = pd.DataFrame(rows)
res[["종목", "공시", "시각", "장후", "D0", "D+0", "D+1", "D+2", "D+5", "D+10", "초과 D+5", "거래량 최대배수", "최대배수일"]]

# %% [markdown]
# 수익률 단위는 %입니다. 예: `D+5 = 31.6`은 D-1 종가 대비 5거래일 뒤 +31.6%.

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
for _, e in events.iterrows():
    s = px[px["symbol"] == e["symbol"]].set_index("date").sort_index()["close"]
    pos = s.index.searchsorted(pd.Timestamp(e["공시시각"].date()))
    path = s.iloc[max(0, pos - 5): pos + 11] / s.iloc[pos - 1] * 100 - 100
    ax.plot(range(-min(5, pos), -min(5, pos) + len(path)), path.values, marker=".", label=e["종목"])
ax.axvline(0, color="gray", ls="--"); ax.axhline(0, color="gray", lw=.5)
ax.set_xlabel("D0 기준 거래일"); ax.set_ylabel("D-1 종가 대비 %"); ax.set_title("공시 전후 누적수익률")
ax.legend(ncol=3, fontsize=8); ax.grid(alpha=.3)

# %% [markdown]
# ## 4. 확장 — 같은 종류 공시를 한꺼번에 비교
# "지난달 무상증자 낸 종목들 공시 후 수익률"처럼 **공시 종류 하나를 기간 전체로** 모아 봅니다.
# 회사가 직접 낸 `무상증자결정` 공시만 쓰고(권리락·추가상장 같은 거래소 후속 공시는 제외), 시세는 다시 한 번에 받습니다.

# %%
KIND, K_FROM, K_TO = "무상증자결정", "2026-06-01", "2026-10-31"
total, docs = doc_search("company", ["disclosure"], f"title:{KIND}", K_FROM, K_TO, count=100)
docs = docs[(docs["symbols"] != "") & ~docs["title"].str.contains("정정")]
# 공시 문서의 종목코드는 "117670"처럼 KRX: 접두어가 없다
docs["symbol"] = "KRX:" + docs["symbols"].str.split(", ").str[0]
docs = docs[docs["symbol"].isin(u["symbol"])].sort_values("created_at").drop_duplicates("symbol")
print(f"'{KIND}' 공시 {total}건 → 상장사 {len(docs)}개 종목")

b_from, b_to = (pd.Timestamp(K_FROM) - pd.Timedelta(days=45)).date(), (pd.Timestamp(K_TO) + pd.Timedelta(days=25)).date()
px2 = stock_prices(docs["symbol"].tolist(), b_from, b_to)
idx2 = market_index(b_from, b_to)
rows = []
for _, d in docs.iterrows():
    mk = u.set_index("symbol").loc[d["symbol"], "market"]
    if mk not in ("KOSPI", "KOSDAQ"):
        continue
    r = event_study(px2, idx2, d["symbol"], d["created_at"], mk, horizons=[0, 1, 5])
    if r and "D+5" in r:
        rows.append({"종목": d["stocks"].split(", ")[0], "공시일": d["created_at"].date(), **r})
bulk = pd.DataFrame(rows)
print("평균(%):", bulk[["D+0", "D+1", "D+5", "초과 D+5"]].mean().round(1).to_dict(),
      "| 중앙값 D+5:", round(bulk["D+5"].median(), 1), "| D+5 상승 종목 비율:", f"{(bulk['D+5'] > 0).mean():.0%}")
bulk.sort_values("D+5", ascending=False)[["종목", "공시일", "D0", "D+0", "D+1", "D+5", "초과 D+5", "거래량 최대배수"]]

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 같은 종류 공시라도 시장 국면에 따라 반응이 다릅니다. 1건은 사례일 뿐이고, 4절처럼 여러 건을 모아 평균·중앙값을 같이 보세요.
# - **수급(외국인·기관·개인)은 DeepSearch에 없습니다**(`research/data_gaps`). "누가 샀나"는 이 노트북으로 답할 수 없습니다.
# - 주가는 수정주가라 무상증자 권리락이 과거 가격에 소급 반영돼 있습니다. 권리락 전후로 가격이 끊기지 않으니 수익률 계산에는 오히려 맞습니다.
# - 공시 시각은 DART 접수 시각입니다. `장후`(15:30 이후) 공시는 D0 수익률에 반영되지 않았을 수 있습니다.
