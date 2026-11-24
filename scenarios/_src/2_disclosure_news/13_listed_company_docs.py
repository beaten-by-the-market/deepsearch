# %% [markdown]
# # 2-13 상장사 문서 검색 — 뉴스·리포트·공시/IR·특허에서 KRX 상장사가 나온 문서만 추리기
#
# **질문 예시:** "이번 주 경제뉴스 중 수주·계약 기사에서 상장사만 뽑아 시장별로 세어줘",
# "배터리 특허를 낸 회사 중 상장사는 어디야?"
#
# 뉴스 스크랩 웹앱의 핵심 기능입니다. 키워드·카테고리로 `DocumentSearch`를 하고, 문서에 붙은 회사 정보를 **KRX 상장사 목록**과 맞춰
# 상장사(코스피·코스닥·코넥스, ETF 제외)가 나온 문서만 남긴 뒤 시장별·종목별로 집계합니다.
#
# 문서에는 회사 정보가 두 군데 있습니다.
# - `securities` — 문서의 **관련 종목**(주제 회사). 뉴스·리포트·공시는 6자리 종목코드, **특허는 출원인 회사 이름**이 들어 있습니다.
# - `named_entities` — 본문에서 인식한 **언급 회사**(비상장 포함). NICE 코드·사업자번호·법인번호가 붙어 있습니다.
#
# 두 필드를 모두 보고, 코드뿐 아니라 NICE 코드·사업자번호·법인번호로도 상장사를 찾습니다.
# 끝으로 받은 문서를 **이슈 카테고리**(계약/수주·실적 등 키워드 묶음)와 **관심종목**으로 한 번 더 거릅니다.

# %%
ASOF = "2026-11-24"
D_FROM, D_TO = "2026-11-20", ASOF      # 검색 기간 (DocumentSearch 는 1년 이내)

# 검색 프리셋: 이슈 유형별 키워드 묶음(검색 쿼리와 검색 후 필터에 같이 씀), 언론사 묶음, 관심종목
_A = lambda ws, xs: " or ".join(f"({w} and {x})" for w in ws for x in xs)
ISSUE_PRESETS = {
    "계약/수주": "(수주 and 체결) or (수주 and 공급) or (계약 and 체결) or (계약 and 공급)",
    "인수/투자": "인수 or 합병 or 분할 or 영업양도 or 영업양수 or 엠앤에이 or 출자 or 투자",
    "실적": _A(["매출", "실적", "이익", "배당"], ["발표", "공표", "결정", "기록", "달성", "공시"]),
    "증자/감자": "증자 or 감자 or 주식교환 or 주식이전 or 우회상장",
    "회계/감사": ("상장폐지 or 관리종목 or 자본잠식 or (비적정 and 감사) or (비적정 and 회계법인) or (의견거절 and 감사) "
              "or (의견거절 and 회계법인) or (회계처리 and 위반) or 분식"),
    "소송/부도/회생": "소송 or 횡령 or 배임 or 부도 or 파산 or 회생 or " + _A(["공소", "기소", "혐의"], ["대표이사", "임원", "이사"]),
}
WATCHLIST = ["005930", "000660", "035720", "251970"]   # 관심종목 서식(종목코드 한 열)의 예시 값
PUBLISHER_GROUPS = {
    "중앙일간지": "publisher.raw:('경향신문' or '국민일보' or '동아일보' or '서울신문' or '세계일보' or '아시아투데이' or '조선일보' or '중앙일보' or '한겨레' or '한국일보')",
    "중앙경제지": "publisher.raw:('뉴스토마토' or '디지털타임스' or '매일경제' or '머니투데이' or '서울경제' or '아주경제' or '이데일리' or '이투데이' or '전자신문' or '파이낸셜뉴스' or '한국경제')",
}

# %% [markdown]
# ## 1. 상장사 목록과 식별자
# `GetStockSymbols()` 한 번으로 상장사 전부의 종목코드·NICE 코드·사업자번호·법인번호를 받습니다.
# (일반법인 `1`과 공기업 `2`만 — ETF·ETN 등 `8` 제외)

# %%
sym = ds_df("GetStockSymbols()")
listed = sym[sym.company_type_l1.isin(["1", "2"]) & sym.market.isin(["KOSPI", "KOSDAQ", "KONEX"])].copy()
listed["code"] = listed.symbol.str.replace("KRX:", "", regex=False)
INFO = listed.set_index("code")[["entity_name", "market"]].to_dict("index")
# 식별번호는 보통주와 우선주가 같은 회사라 겹친다 → 회사 식별용 지도는 보통주(코드 끝자리 0)로만 만든다
common = listed[listed.code.str.endswith("0")]
BY_NICE = dict(zip(common.symbol_nice.dropna(), common.code))
BY_BRID = dict(zip(common.business_rid.dropna().str.replace("-", ""), common.code))
BY_CRID = dict(zip(common.company_rid.dropna().str.replace("-", ""), common.code))
BY_NAME = dict(zip(common.entity_name, common.code))
print(f"상장사 {len(listed):,}개 — NICE {len(BY_NICE):,} · 사업자번호 {len(BY_BRID):,} · 법인번호 {len(BY_CRID):,}")
print(listed.market.value_counts().to_dict())

# %% [markdown]
# ## 2. 검색과 매칭 함수

# %%
def fetch_docs(category, sections, query, date_from=D_FROM, date_to=D_TO, pages=1):
    """DocumentSearch 원문(회사 필드 포함) → (총건수, 문서 목록). 한 페이지 100건."""
    docs, total = [], 0
    for p in range(1, pages + 1):
        q = (f'DocumentSearch(["{category}"],{json.dumps(sections)},{json.dumps(query, ensure_ascii=False)},'
             f'count=100,page={p},date_from={date_from},date_to={date_to})')
        c = ds(q)["data"]["pods"][1]["content"]
        d = c.get("data") if isinstance(c.get("data"), dict) else c
        total = d.get("total_matches") or 0
        batch = d.get("docs") or []
        docs += batch
        if not batch or p * 100 >= total:   # 페이지가 100건보다 짧게 와도 뒤에 더 있을 수 있음
            break
    return total, docs


def to_code(e):
    """회사 항목 하나 → 상장 종목코드(6자리) 또는 None. 코드 → NICE → 사업자번호 → 법인번호 → 이름 순."""
    s = str(e.get("symbol") or "")
    code = s.split(":")[-1]
    if code in INFO:
        return code
    if s in BY_NICE:
        return BY_NICE[s]
    for key, table in (("business_rid", BY_BRID), ("company_rid", BY_CRID)):
        v = str(e.get(key) or "").replace("-", "")
        if v in table:
            return table[v]
    return BY_NAME.get(e.get("name"))


def match_listed(category, sections, query, date_from=D_FROM, date_to=D_TO, pages=1):
    total, docs = fetch_docs(category, sections, query, date_from, date_to, pages)
    rows = []
    for x in docs:
        rel = {c for c in (to_code(e) for e in (x.get("securities") or [])) if c}
        men = {c for c in (to_code(e) for e in (x.get("named_entities") or []) if isinstance(e, dict)) if c} - rel
        rows.append({"created_at": str(x.get("created_at"))[:16], "publisher": x.get("publisher"),
                     "title": " ".join(str(x.get("title") or "").split())[:70],
                     "관련종목": [INFO[c]["entity_name"] for c in sorted(rel)],
                     "언급종목": [INFO[c]["entity_name"] for c in sorted(men)],
                     "_rel": sorted(rel), "_men": sorted(men), "url": x.get("content_url")})
    df = pd.DataFrame(rows, columns=["created_at", "publisher", "title", "관련종목", "언급종목", "_rel", "_men", "url"])
    n_rel = int((df._rel.str.len() > 0).sum()) if len(df) else 0
    n_any = int(((df._rel.str.len() > 0) | (df._men.str.len() > 0)).sum()) if len(df) else 0
    print(f"[{category} {sections}] '{query[:50]}' 총 {total:,}건 중 {len(df)}건 받음 → "
          f"관련종목에 상장사 {n_rel}건, 언급까지 포함하면 {n_any}건 (+{n_any - n_rel})")
    return df[(df._rel.str.len() > 0) | (df._men.str.len() > 0)].reset_index(drop=True)


def by_stock(df, include_mentions=True):
    """문서 → 종목별 건수(관련/언급)와 시장."""
    rel = pd.Series([c for cs in df._rel for c in cs]).value_counts().rename("관련 문서")
    men = pd.Series([c for cs in df._men for c in cs]).value_counts().rename("언급만 된 문서")
    t = pd.concat([rel, men], axis=1).fillna(0).astype(int)
    if not include_mentions:
        t = t[t["관련 문서"] > 0]
    t["종목"] = [INFO[c]["entity_name"] for c in t.index]
    t["시장"] = [INFO[c]["market"] for c in t.index]
    t["합계"] = t["관련 문서"] + t["언급만 된 문서"]
    return t.sort_values(["관련 문서", "합계"], ascending=False)[["종목", "시장", "관련 문서", "언급만 된 문서", "합계"]]

# %% [markdown]
# ## 3. 예시 ① 경제뉴스 '계약/수주' 기사 × 중앙경제지 — 상장사만
# 앱의 이슈 프리셋과 언론사 묶음을 그대로 씁니다. 300건(3페이지)까지 받습니다.

# %%
q1 = f"({ISSUE_PRESETS['계약/수주']}) and {PUBLISHER_GROUPS['중앙경제지']}"
news = match_listed("news", ["economy"], q1, pages=3)
stocks = by_stock(news)
print("\n시장별 종목 수(관련+언급):", stocks.시장.value_counts().to_dict())
stocks.head(15)

# %%
news[["created_at", "publisher", "title", "관련종목", "언급종목"]].head(12)

# %% [markdown]
# ## 4. 예시 ② 증권사 리포트 '반도체' — 업종·시황 리포트도 상장사 언급으로 잡힌다
# 기업 리포트는 `securities`에 종목이 붙지만, 시황·산업 리포트는 대개 비어 있고 본문 언급(`named_entities`)에만 회사가 있습니다.

# %%
rep = match_listed("research", [], "반도체", pages=2)
by_stock(rep).head(12)

# %% [markdown]
# ## 5. 예시 ③ 공시 '단일판매·공급계약' — 시장별 건수
# 공시는 거의 모두 `securities`에 회사가 붙어 있습니다.

# %%
disc = match_listed("company", ["disclosure"], "title:단일판매", pages=2)
s3 = by_stock(disc, include_mentions=False)
print("시장별 공시 건수:", disc._rel.explode().map(lambda c: INFO.get(c, {}).get("market")).value_counts().to_dict())
s3.head(10)

# %% [markdown]
# ## 6. 예시 ④ 특허 '배터리'(2025년) — 출원인 중 상장사
# 특허의 `securities.symbol`에는 종목코드 대신 **출원인 회사 이름**(예: '엘지에너지솔루션', '현대자동차')이 들어 있어
# 이름만으로는 상장사 목록('LG에너지솔루션', '현대차')과 맞지 않습니다. 같은 항목에 있는 **법인번호·사업자번호**로 맞춥니다.
# 특허는 공개까지 시차가 있어 최근 몇 달 건수가 적습니다.

# %%
pat = match_listed("patent", [], "배터리", date_from="2025-01-01", date_to="2025-12-31", pages=3)
by_stock(pat).head(12)

# %%
# 이름 매칭만 했을 때와 비교 — 식별번호 매칭이 왜 필요한지
_, raw = fetch_docs("patent", [], "배터리", "2025-01-01", "2025-12-31", pages=1)
apps = [e for x in raw for e in (x.get("securities") or [])]
by_name = sum(1 for e in apps if e.get("name") in BY_NAME or str(e.get("symbol", "")).split(":")[-1] in INFO)
by_id = sum(1 for e in apps if to_code(e))
print(f"출원인 항목 {len(apps)}개 중 상장사로 판정: 이름·코드만 {by_name}개 → 식별번호까지 {by_id}개")

# %% [markdown]
# ## 7. 종목별 문서 수를 한 번에 — `DocumentAggregation`
# 문서를 받지 않고 종목별 건수만 필요하면 집계 한 번이면 됩니다. 위에서 받은 300건이 아니라 **검색 결과 전체**를 셉니다.
# 키는 대개 6자리 종목코드지만, 검색어·카테고리에 따라 DART 고유번호(8자리)·NICE 코드·회사 이름(특허)이 섞이므로
# 상장 종목코드인 것만 남깁니다.

# %%
c = ds(f'DocumentAggregation(["news"],["economy"],{json.dumps(q1, ensure_ascii=False)},"securities.symbol:200",'
       f'date_from={D_FROM},date_to={D_TO})')["data"]["pods"][1]["content"]
agg = pd.DataFrame(c["data"])[["key", "count"]]
agg["상장사"] = agg.key.isin(INFO.keys())
print(f"집계 키 {len(agg)}개 중 상장 종목코드 {agg.상장사.sum()}개, 그 밖(비상장·고유번호 등) {(~agg.상장사).sum()}개")
top = agg[agg.상장사].head(15).copy()
top["종목"] = top.key.map(lambda c: INFO[c]["entity_name"])
top["시장"] = top.key.map(lambda c: INFO[c]["market"])
top[["종목", "시장", "count"]].rename(columns={"count": "관련 기사 수"}).reset_index(drop=True)

# %% [markdown]
# ## 8. 받은 문서를 이슈 카테고리·관심종목으로 거르기
# 검색은 넓게 하고, 받은 뒤 **제목**에 이슈 키워드 묶음이 맞는 문서만 남깁니다(`a and b`는 둘 다, `or`는 하나라도).
# 관심종목 필터는 관련·언급 종목 중 하나라도 관심종목이면 남깁니다.

# %%
def issue_match(title, preset):
    """ISSUE_PRESETS 식('(a and b) or c')을 제목에 적용 → 맞은 항목 목록."""
    hits = []
    for term in preset.split(" or "):
        words = [w.strip(" ()") for w in term.split(" and ")]
        if all(w and w in title for w in words):
            hits.append("+".join(words))
    return hits

wide = match_listed("news", ["economy"], "*", pages=3)        # 같은 기간 경제뉴스 300건, 상장사 문서만
counts = {}
for name, preset in ISSUE_PRESETS.items():
    counts[name] = int(wide.title.map(lambda t: bool(issue_match(t, preset))).sum())
print(f"상장사 경제뉴스 {len(wide)}건 중 이슈별 제목 매칭:", counts)
wide["이슈"] = wide.title.map(lambda t: [n for n, p in ISSUE_PRESETS.items() if issue_match(t, p)])
wide[wide.이슈.str.len() > 0][["created_at", "title", "이슈", "관련종목"]].head(8)

# %%
watch = set(WATCHLIST)
mine = wide[wide.apply(lambda r: bool(watch & (set(r._rel) | set(r._men))), axis=1)]
print(f"관심종목 {[INFO[c]['entity_name'] for c in WATCHLIST if c in INFO]} 관련·언급 문서 {len(mine)}건")
mine[["created_at", "publisher", "title", "관련종목", "언급종목"]].head(8)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **관련 종목(`securities`)은 문서의 주제 회사, 언급 종목(`named_entities`)은 본문에 나온 회사**입니다. 언급까지 넣으면
#   뉴스에서 상장사 문서가 20~30% 더 잡히지만, 지나가듯 언급된 경우도 섞입니다.
# - **동명 오인식**이 있습니다(예: 'DB', '미래산업', '엠비디'). 의심스러운 종목은 제목으로 다시 확인하세요.
# - **현재 상장 종목 기준**입니다. 그 사이 상장폐지된 회사는 상장사로 잡히지 않습니다.
# - 특허는 공개 시차 때문에 최근 건수가 적고, 출원인 이름이 공식명이라 식별번호 매칭이 필요합니다.
