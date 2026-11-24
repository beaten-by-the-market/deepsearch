# %% [markdown]
# # 2-14 종목 한 장 보기 — 뉴스·공시·IR·리포트와 52주 주가를 한 화면에
#
# **질문 예시:** "삼성전자 최근 1년 문서 흐름이랑 주가 한 번에 보여줘", "에코프로비엠 최근 공시·IR·리포트 최신 것만 정리해줘"
#
# 종목 하나를 정하면 다음을 한 번에 모읍니다.
# - 최근 1년 **뉴스·공시·IR·증권사 리포트** 건수와 월별 추이
# - 각 종류의 **최신 목록**(뉴스는 이슈 카테고리로 태그)
# - **52주 주가 차트**에 주요 공시일·IR 날짜 표시
#
# 종목 지정은 모든 문서 종류에서 `securities.symbol:6자리`로 합니다.

# %%
ASOF = "2026-11-24"
STOCK = "005930"
N_LATEST = 5

ISSUE_PRESETS = {
    "계약/수주": "(수주 and 체결) or (수주 and 공급) or (계약 and 체결) or (계약 and 공급)",
    "인수/투자": "인수 or 합병 or 분할 or 영업양도 or 영업양수 or 엠앤에이 or 출자",
    "실적": "실적 or 매출 or 영업이익 or 어닝",
    "증자/감자": "증자 or 감자 or 주식교환 or 주식이전 or 우회상장",
    "주주환원": "배당 or 자사주 or 소각 or 주주환원",
    "소송/규제": "소송 or 횡령 or 배임 or 공소 or 기소 or 혐의 or 제재",
}
ROUTINE = "소유상황보고서|소유주식변동|대량보유|상품ㆍ용역거래|기업설명회|증권발행실적|정정"   # 차트에서 뺄 일상 공시

def doc_pages(category, section, query, date_from, date_to, pages=1, count=100):
    """doc_search 와 같은 표를 주되, 페이지가 count보다 적게 와도 전체 건수에 닿을 때까지 다음 페이지를 받습니다.
    (서버가 중복을 빼고 주는지 한 페이지가 80~90건으로 오는 일이 흔합니다.)"""
    raw, total = [], 0
    for p in range(1, pages + 1):
        q = (f'DocumentSearch(["{category}"],{json.dumps(section, ensure_ascii=False)},{json.dumps(query, ensure_ascii=False)},'
             f'count={count},page={p},date_from={date_from},date_to={date_to})')
        c = _pod(ds(q)).get("content") or {}
        d = c.get("data") if isinstance(c.get("data"), dict) else c
        total = d.get("total_matches") or 0
        docs = d.get("docs") or []
        raw += docs
        if not docs or p * count >= total:
            break
    rows = [{"created_at": pd.to_datetime(str(x.get("created_at"))[:19], errors="coerce"),
             "publisher": x.get("publisher"), "title": " ".join(str(x.get("title") or "").split()),
             "stocks": ", ".join(s.get("name", "") for s in x.get("securities") or []),
             "symbols": ", ".join(s.get("symbol", "") for s in x.get("securities") or []),
             "polarity": _polarity(x), "url": x.get("content_url")} for x in raw]
    cols = ["created_at", "publisher", "title", "stocks", "symbols", "polarity", "url"]
    return total, pd.DataFrame(rows, columns=cols).drop_duplicates("url")

def issue_tags(title):
    tags = []
    for name, expr in ISSUE_PRESETS.items():
        for term in expr.split(" or "):
            words = [w.strip(" ()") for w in term.split(" and ")]
            if all(w in title for w in words):
                tags.append(name); break
    return tags

u = universe(); u["code"] = u.symbol.str.replace("KRX:", "", regex=False)
me = u[u.code == STOCK].iloc[0]
print(f"{me['name']} ({STOCK}, {me.market}) — {me.industry_name}")

# %% [markdown]
# ## 1. 최근 1년 문서 건수와 월별 추이
# 건수는 `total_matches`, 추이는 `DocumentTrends`(월별)로 받습니다. 문서를 다 받지 않아도 됩니다.

# %%
d1y = (pd.Timestamp(ASOF) - pd.DateOffset(years=1) + pd.Timedelta(days=1)).date()
KINDS = {"뉴스": ("news", []), "공시": ("company", ["disclosure"]), "IR": ("company", ["ir"]), "리포트": ("research", [])}
q = f"securities.symbol:{STOCK}"
totals, monthly = {}, {}
for k, (cat, sec) in KINDS.items():
    t = doc_trends(cat, sec, q, d1y, ASOF, interval="1M")
    monthly[k] = t.set_index(t.date.dt.strftime("%Y-%m"))["count"]
    totals[k] = int(t["count"].sum())
print("최근 1년 건수:", totals)
m = pd.DataFrame(monthly).fillna(0).astype(int)
m.tail(6)

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 3), gridspec_kw={"width_ratios": [1, 1]})
m["뉴스"].plot.bar(ax=axes[0], color="#4C78A8", title="뉴스 (월별)")
m[["공시", "IR", "리포트"]].plot.bar(ax=axes[1], title="공시·IR·리포트 (월별)")
for a in axes:
    a.grid(alpha=.3, axis="y"); a.set_xlabel("")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## 2. 최신 목록

# %%
d2w = (pd.Timestamp(ASOF) - pd.Timedelta(days=13)).date()
_, news = doc_pages("news", [], q, d2w, ASOF, pages=5)
news["이슈"] = news.title.map(issue_tags)
print(f"최근 2주 뉴스 {len(news)}건 | 이슈별:", news.이슈.explode().value_counts().to_dict(),
      "| 긍부정:", news.polarity.value_counts().to_dict())
news[news.이슈.str.len() > 0][["created_at", "publisher", "title", "이슈", "polarity"]].head(N_LATEST)

# %%
latest = {}
for k in ("공시", "IR", "리포트"):
    cat, sec = KINDS[k]
    qq = q if k != "공시" else f"{q} and !title:소유상황보고서"
    _, df = doc_search(cat, sec, qq, d1y, ASOF, count=N_LATEST)
    latest[k] = df
    print(f"\n■ {k} 최신 {len(df)}건")
    print(df[["created_at", "publisher", "title"]].to_string(index=False, max_colwidth=50))

# %% [markdown]
# ## 3. 52주 주가와 공시·IR 날짜
# 공시 중 소유상황 보고 같은 일상 공시는 빼고, 남은 공시와 IR 자료 날짜를 주가 위에 표시합니다.

# %%
px = stock_prices(f"KRX:{STOCK}", d1y, ASOF, columns=["close", "volume"]).set_index("date")
# 1년 공시의 대부분이 임원·주요주주 소유상황 보고라, 검색 단계에서 제외(!title:)하고 받습니다
not_routine = " and ".join(f"!title:{w}" for w in ["소유상황보고서", "소유주식변동", "대량보유"])
n_all, _ = doc_pages("company", ["disclosure"], q, d1y, ASOF, count=1)
_, disc = doc_pages("company", ["disclosure"], f"{q} and {not_routine}", d1y, ASOF, pages=3)
key = disc[~disc.title.str.contains(ROUTINE, regex=True)].copy()
_, irs = doc_search("company", ["ir"], q, d1y, ASOF, count=100)
print(PRICE_NOTICE)
print(f"1년 공시 {n_all:,}건 → 소유상황 보고 등 제외 {len(disc)}건 → 차트 표시 {len(key)}건, IR {len(irs)}건")

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(px.index, px.close, color="#333", lw=1.2, label="종가")
for d in key.created_at.dt.normalize().unique():
    ax.axvline(d, color="#E45756", alpha=.25, lw=1)
for d in irs.created_at.dt.normalize().unique():
    ax.axvline(d, color="#54A24B", alpha=.8, lw=1.5, ls="--")
ax.plot([], [], color="#E45756", alpha=.5, label="주요 공시"); ax.plot([], [], color="#54A24B", ls="--", label="IR 자료")
ax.set_title(f"{me['name']} 52주 주가 (최고 {px.close.max():,.0f} / 최저 {px.close.min():,.0f} / 현재 {px.close.iloc[-1]:,.0f})")
ax.legend(loc="upper left"); ax.grid(alpha=.3); plt.show()

# %%
# 주요 공시 직후 5거래일 수익률 (참고)
rows = []
for _, r in key.sort_values("created_at").iterrows():
    d = r.created_at.normalize() + (pd.Timedelta(days=1) if r.created_at.hour >= 15 else pd.Timedelta(0))
    idx = px.index[px.index >= d]
    if len(idx) > 5:
        p0 = px.close[px.index < idx[0]].iloc[-1] if (px.index < idx[0]).any() else px.close[idx[0]]
        rows.append({"날짜": r.created_at.strftime("%Y-%m-%d %H:%M"), "공시": r.title[:40],
                     "5거래일 수익률(%)": round((px.close[idx[4]] / p0 - 1) * 100, 1)})
ev = pd.DataFrame(rows)
ev = ev.assign(일=ev.날짜.str[:10]).drop_duplicates(["일", "공시"]).drop(columns="일")   # 같은 날 같은 공시는 한 번만
ev.tail(10)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **뉴스 건수는 "그 종목이 주제인 기사"** 기준입니다(본문에 이름만 나온 기사는 빠짐). 동명 오인식 기사가 섞일 수 있습니다.
# - **이슈 태그는 제목 키워드 매칭**이라 거칩니다. '투자'처럼 넓은 단어는 묶음에서 뺐습니다.
# - 공시 후 수익률은 다른 사건과 시장 움직임이 섞인 참고값입니다. 제대로 보려면 [2-01 공시 이벤트 스터디](01_disclosure_event_study.ipynb)를 쓰세요.
