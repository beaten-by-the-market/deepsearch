# %% [markdown]
# # 5-10 공시 가져오기 — 종목별·키워드별 공시와 거래소 시장 공시
#
# **질문 예시:** "삼성전자 최근 3개월 공시 목록 줘", "이번 주 유상증자 공시 낸 회사 뽑아줘",
# "오늘 거래소가 낸 투자경고·공매도 과열 공시 보여줘"
#
# DeepSearch 공시(`["company"],["disclosure"]`)에는 **DART 공시**(회사가 낸 공시)와 **KIND 공시**(거래소 시장본부·
# 시장감시위원회가 낸 시장조치)가 함께 들어 있습니다. 문서에는 제목·시각·회사·원문 링크만 있고 본문은 없습니다.
# 본문의 표·숫자가 필요하면 링크를 따라가 읽습니다 → [2-05 공시 본문](../2_disclosure_news/05_disclosure_text.ipynb).

# %%
ASOF = "2026-11-24"
STOCK = "005930"          # 종목별 공시
KEYWORD = "유상증자"       # 키워드별 공시
EXCHANGE = ["시장감시위원회", "유가증권시장본부", "코스닥시장본부", "코넥스시장본부"]

def link_type(url):
    u = str(url or "")
    return "DART" if "dart.fss.or.kr" in u else ("KIND" if "kind.krx.co.kr" in u else "기타")

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

def disclosures(query, date_from, date_to, pages=1):
    total, df = doc_pages("company", ["disclosure"], query, date_from, date_to, pages=pages)
    df["원문"] = df.url.map(link_type)
    print(f"'{query[:80]}' {date_from}~{date_to}: 전체 {total:,}건 중 {len(df)}건")
    return df

# %% [markdown]
# ## 1. 종목별 — 최근 3개월
# 종목 지정은 `securities.symbol:6자리`입니다(`KRX:` 접두어를 붙이면 키워드 검색으로 바뀝니다).

# %%
d3m = (pd.Timestamp(ASOF) - pd.DateOffset(months=3)).date()
one = disclosures(f"securities.symbol:{STOCK}", d3m, ASOF, pages=2)
print(one.원문.value_counts().to_dict())
one[["created_at", "publisher", "title", "원문", "url"]].head(10)

# %% [markdown]
# ## 2. 키워드별 — 최근 2주 '유상증자'가 제목에 든 공시
# `title:키워드`로 제목만 봅니다. 결정 공시뿐 아니라 정정·발행가 확정 같은 후속 공시도 함께 걸립니다.

# %%
d2w = (pd.Timestamp(ASOF) - pd.Timedelta(days=13)).date()
kw = disclosures(f"title:{KEYWORD}", d2w, ASOF, pages=3)
u = universe()
u["code"] = u.symbol.str.replace("KRX:", "", regex=False)
kw["code"] = kw.symbols.str.split(", ").str[0].str.replace("KRX:", "", regex=False)
kw = kw.merge(u[["code", "market"]], on="code", how="left")
kw["유형"] = kw.title.str.replace(r"\s+", "", regex=True).str.extract(r"^(\[[^\]]+\])?(.{0,14})")[1]
print("시장별:", kw.market.fillna("비상장·기타").value_counts().to_dict())
kw.유형.value_counts().head(8)

# %%
kw[["created_at", "stocks", "market", "title", "원문"]].head(10)

# %% [markdown]
# ## 3. 거래소 시장 공시 — 시장감시위원회·시장본부
# 투자주의·경고·위험 지정, 공매도 과열종목 지정, 단기과열, 매매거래정지, 관리종목 등은 거래소가 냅니다.
# `publisher.raw`로 발행기관을 지정합니다. (이 공시들은 2026-08부터 촘촘하게 들어 있습니다.)

# %%
pq = "publisher.raw:(" + " or ".join(f"'{p}'" for p in EXCHANGE) + ")"
ex = disclosures(pq, d2w, ASOF, pages=5)
ex["조치"] = (ex.title.str.replace(r"\s+", " ", regex=True)
              .str.replace(r"\(.*?\)|\[.*?\]", "", regex=True).str.strip().str[:22])
print("발행기관:", ex.publisher.value_counts().to_dict())
ex.조치.value_counts().head(12)

# %%
ex[ex.title.str.contains("투자경고|공매도 과열", regex=True)][["created_at", "publisher", "stocks", "title"]].head(10)

# %% [markdown]
# ## 4. 기간 중 공시가 많은 발행기관
# 문서를 받지 않고 건수만 볼 때는 `DocumentAggregation`을 씁니다(`publisher`로 묶음).

# %%
c = ds(f'DocumentAggregation(["company"],["disclosure"],"*","publisher:20",date_from={d2w},date_to={ASOF})')
agg = pd.DataFrame(c["data"]["pods"][1]["content"]["data"])[["key", "count"]]
agg.columns = ["발행기관", "공시 수(2주)"]
agg.head(12)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **원문 링크:** DART(`dart.fss.or.kr`) 또는 KIND(`kind.krx.co.kr`)입니다. 본문은 DeepSearch에 없고 링크로 읽어야 합니다(2-05).
# - **회사 이름:** 공시의 회사 이름은 DART 등록명(예: '현대자동차')이라 `securities.name:현대차`로는 안 걸립니다. 종목코드로 지정하세요.
# - **유형 분류:** 제목 앞부분으로 거칠게 나눈 것입니다. 정확한 공시 유형 코드는 DeepSearch에 없습니다.
