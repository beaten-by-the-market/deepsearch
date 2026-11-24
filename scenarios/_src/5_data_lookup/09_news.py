# %% [markdown]
# # 5-09 뉴스정보 가져오기 — 키워드·섹션·언론사·시간대·종목으로 뉴스 모으기
#
# **질문 예시:** "이번 주 경제지 기사 중 HBM 기사 다 모아줘", "오늘 오전 9~12시 삼성전자 기사 뽑아줘",
# "SK하이닉스 관련 기사 1년치 CSV로 줘"
#
# `DocumentSearch(["news"], 섹션, 쿼리, count, page, date_from, date_to)` 하나로 다 됩니다. 이 노트북은
# 자주 쓰는 조건(섹션·언론사 묶음·시간 범위·종목)을 함수 하나로 묶고, 한 페이지 100건 제한과
# **검색 기간 1년 제한**을 알아서 넘깁니다.

# %%
import re
ASOF = "2026-11-24"

SECTIONS = {"전체": [], "경제": ["economy"], "기술/IT": ["tech"], "문화": ["culture"], "사설": ["opinion"],
            "사회": ["society"], "세계": ["world"], "연예": ["entertainment"], "정치": ["politics"]}
_P = {
    "중앙일간지": ["경향신문", "국민일보", "동아일보", "서울신문", "세계일보", "아시아투데이", "조선일보", "중앙일보", "한겨레", "한국일보"],
    "중앙경제지": ["뉴스토마토", "디지털타임스", "매일경제", "머니투데이", "서울경제", "아주경제", "이데일리", "이투데이",
               "전자신문", "파이낸셜뉴스", "한국경제"],
    "석간지": ["내일신문", "문화일보", "아시아경제", "지역내일신문", "헤럴드경제"],
    "종합일간지·지방지": ["메트로경제", "국제신문", "부산일보"],
}
_P["중앙일간지·경제지"] = _P["중앙일간지"] + _P["중앙경제지"]
_P["주요 언론사 전체"] = _P["중앙일간지·경제지"] + _P["석간지"] + ["중소기업뉴스"] + _P["종합일간지·지방지"]
PUBLISHER_GROUPS = _P

# %% [markdown]
# ## 1. 검색 함수
# - `publishers`: 묶음 이름이나 언론사 이름 목록 → `publisher.raw:('매일경제' or …)`
# - `time_from`/`time_to`: 시각까지 자르려면 `"2026-11-24T09:00:00"` 형식 → 쿼리에 `created_at:[… to …]`
# - `stock`: 6자리 종목코드 → `securities.symbol:005930` (그 종목이 주제인 기사)
# - 기간이 1년을 넘으면 1년씩 나눠 받고 URL로 중복을 지웁니다.

# %%
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

def news_search(keyword="", section="전체", publishers=None, date_from=None, date_to=ASOF,
                time_from=None, time_to=None, stock=None, max_pages=3, verbose=True):
    parts = [f"({keyword})"] if keyword else []
    if stock:
        parts.append(f"securities.symbol:{stock}")
    if publishers:
        names = PUBLISHER_GROUPS.get(publishers, publishers) if isinstance(publishers, str) else publishers
        parts.append("publisher.raw:(" + " or ".join(f"'{n}'" for n in names) + ")")
    if time_from and time_to:
        parts.append(f'created_at:["{time_from}" to "{time_to}"]')
    query = " and ".join(parts) or "*"
    date_from = date_from or str(pd.Timestamp(date_to).date() - timedelta(days=6))
    # 1년 한도 → 구간 나누기
    windows, s, e = [], pd.Timestamp(date_from), pd.Timestamp(date_to)
    while s <= e:
        stop = min(s + pd.DateOffset(years=1) - pd.Timedelta(days=1), e)
        windows.append((s.date(), stop.date())); s = stop + pd.Timedelta(days=1)
    frames, total = [], 0
    for a, b in windows:
        t, df = doc_pages("news", SECTIONS[section], query, a, b, pages=max_pages)
        total += t
        frames.append(df)
        if verbose:
            print(f"  {a}~{b}: 전체 {t:,}건 중 {len(df)}건 받음")
    out = pd.concat(frames, ignore_index=True).drop_duplicates("url").sort_values("created_at", ascending=False)
    if verbose:
        print(f"쿼리: {query[:150]}{'…' if len(query) > 150 else ''}\n합계 {total:,}건 중 {len(out)}건")
    return out.reset_index(drop=True)

# %% [markdown]
# ## 2. 예시 ① 경제 섹션 × 중앙경제지 × 'HBM' (최근 1주)

# %%
hbm = news_search("HBM", section="경제", publishers="중앙경제지", max_pages=2)
print(hbm.publisher.value_counts().head(6).to_dict())
hbm[["created_at", "publisher", "title", "stocks", "polarity"]].head(8)

# %% [markdown]
# ## 3. 예시 ② 날짜+시간 범위 — 11월 24일 오전 9~12시 '삼성전자' 기사
# `date_from`/`date_to`는 날짜 단위라, 시간대는 쿼리 안의 `created_at` 범위로 자릅니다.

# %%
morning = news_search("삼성전자", date_from=ASOF, date_to=ASOF,
                      time_from=f"{ASOF}T09:00:00", time_to=f"{ASOF}T12:00:00", max_pages=3)
print("시간 범위 확인:", morning.created_at.min(), "~", morning.created_at.max())
morning.created_at.dt.floor("30min").value_counts().sort_index()

# %% [markdown]
# ## 4. 예시 ③ 종목 지정 — SK하이닉스가 주제인 기사, 1년 넘게 (자동 분할)
# 13개월을 요청하면 1년 + 1개월 두 번에 나눠 받습니다. 여기서는 구간마다 1페이지만 받아 흐름만 봅니다.

# %%
d0 = (pd.Timestamp(ASOF) - pd.DateOffset(months=13)).date()
hynix = news_search(stock="000660", date_from=d0, max_pages=1)
hynix[["created_at", "publisher", "title", "polarity"]].head(5)

# %% [markdown]
# 기사 **건수 추이**만 필요하면 문서를 받지 말고 `DocumentTrends`(기간 2년까지 한 번에)를 쓰세요.

# %%
tr = doc_trends("news", [], "securities.symbol:000660", d0, ASOF, interval="1M")
tr["월"] = tr.date.dt.strftime("%Y-%m")
ax = tr.plot.bar(x="월", y="count", figsize=(9, 3), legend=False, title="SK하이닉스 주제 기사 수 (월별)")
ax.grid(alpha=.3, axis="y"); plt.show()

# %% [markdown]
# ## 5. 기간 중 기사가 많은 언론사
# DeepSearch 뉴스 출처는 575곳가량입니다. 어떤 이름으로 들어 있는지는 집계로 확인합니다
# (`publisher.raw`는 집계에서 서버 오류가 나고, `publisher`로 하면 됩니다).

# %%
c = ds(f'DocumentAggregation(["news"],["economy"],"*","publisher:30",'
       f'date_from={pd.Timestamp(ASOF).date() - timedelta(days=6)},date_to={ASOF})')["data"]["pods"][1]["content"]
pubs = pd.DataFrame(c["data"])[["key", "count"]].rename(columns={"key": "언론사", "count": "경제 기사 수(1주)"})
pubs.head(15)

# %% [markdown]
# ## 6. DeepSearch 언론사 목록과 빅카인즈 비교
# 언론사 이름 목록은 레포 `scenarios/_data/`에 있습니다. 로컬에서는 레포 파일을, Colab에서는 GitHub에서 읽습니다.
# (2026-01-31 기준: DeepSearch 574곳, 빅카인즈 104곳, 둘 다 45곳)

# %%
DATA_URL = "https://raw.githubusercontent.com/beaten-by-the-market/deepsearch/main/scenarios/_data/"

def load_text(name):
    """scenarios/_data/<name> — 로컬 레포에 있으면 그 파일, 없으면 GitHub raw."""
    d = os.path.abspath(os.getcwd())
    while True:
        p = os.path.join(d, "scenarios", "_data", name)
        if os.path.isfile(p):
            return open(p, encoding="utf-8").read()
        if os.path.dirname(d) == d:
            break
        d = os.path.dirname(d)
    r = requests.get(DATA_URL + name, timeout=30); r.raise_for_status()
    return r.text

ds_pubs = [x.strip() for x in load_text("deepsearch_publishers.txt").splitlines() if x.strip()]
comp = load_text("publisher_comparison.txt")
sections_cmp = {m.group(1): int(m.group(2)) for m in re.finditer(r"--- \[(.+?)\] (\d+)개 ---", comp)}
print(f"DeepSearch 언론사 {len(ds_pubs)}곳 |", sections_cmp)
print("이름 찾기 예 — '경제'가 들어간 곳:", [p for p in ds_pubs if "경제" in p][:12])

# %% [markdown]
# ## 7. CSV로 저장

# %%
hbm.to_csv("news_hbm.csv", index=False, encoding="utf-8-sig")
if IN_COLAB:
    from google.colab import files
    files.download("news_hbm.csv")
print("news_hbm.csv 저장:", len(hbm), "건")

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **한 번에 100건, 검색 기간 1년**이 API 한도입니다. 위 함수가 페이지와 기간을 나눠 받지만, 수만 건이면 오래 걸립니다.
#   건수만 필요하면 `DocumentTrends`·`DocumentAggregation`을 쓰세요.
# - `securities.symbol:6자리`는 그 종목이 **주제인** 기사입니다. 본문에 이름만 나온 기사까지 원하면 종목명을 키워드로 넣으세요(수 배 많음).
# - 긍부정(`polarity`)은 기사 절반가량에만 원래 값이 있고, 나머지는 DeepSearch 보조 모델 값으로 채웠습니다.
