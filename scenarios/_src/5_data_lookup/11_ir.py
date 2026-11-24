# %% [markdown]
# # 5-11 IR정보 가져오기 — 회사가 올린 IR 자료와 PDF 본문
#
# **질문 예시:** "이번 주 IR 자료 올린 회사 목록 줘", "삼성전자 최근 1년 IR 자료랑 최신 실적발표 PDF 내용 보여줘"
#
# DeepSearch `["company"],["ir"]`에는 상장사가 올린 **IR 자료(실적발표·회사소개 PDF)**가 들어 있습니다.
# 문서마다 회사(`securities`)와 **PDF 링크**(`content_url`)가 붙어 있어, PDF를 받아 앞 장 텍스트를 바로 읽을 수 있습니다.
# (IR 개최 '안내 공시'는 공시 쪽에 있습니다 → 5-10)

# %%
import numpy as np
ASOF = "2026-11-24"
STOCK = "005930"

if IN_COLAB:
    !pip -q install pymupdf

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

def ir_docs(query, date_from, date_to, pages=1):
    total, df = doc_pages("company", ["ir"], query, date_from, date_to, pages=pages)
    print(f"IR '{query}' {date_from}~{date_to}: 전체 {total:,}건 중 {len(df)}건")
    return df

# %% [markdown]
# ## 1. 최근 2주 올라온 IR 자료 전체

# %%
d2w = (pd.Timestamp(ASOF) - pd.Timedelta(days=13)).date()
recent = ir_docs("*", d2w, ASOF, pages=4)
u = universe(); u["code"] = u.symbol.str.replace("KRX:", "", regex=False)
recent["code"] = recent.symbols.str.split(", ").str[0]
recent = recent.merge(u[["code", "market"]], on="code", how="left")
recent["자료 성격"] = np.select(
    [recent.title.str.contains("실적|결산|분기|Earnings", case=False, regex=True),
     recent.title.str.contains("회사소개|IR|사업|Company|Corporate", case=False, regex=True)],
    ["실적", "회사소개·사업"], "기타")
print("시장별:", recent.market.fillna("기타").value_counts().to_dict())
print("자료 성격(제목 기준):", recent["자료 성격"].value_counts().to_dict())
recent[["created_at", "stocks", "market", "title"]].head(10)

# %% [markdown]
# ## 2. 종목별 — 최근 1년 IR 자료

# %%
d1y = (pd.Timestamp(ASOF) - pd.DateOffset(years=1) + pd.Timedelta(days=1)).date()
one = ir_docs(f"securities.symbol:{STOCK}", d1y, ASOF)
one[["created_at", "title", "url"]]

# %% [markdown]
# ## 3. IR 자료를 많이 올린 회사 (최근 3개월)
# 건수만 필요하면 `DocumentAggregation` 한 번이면 됩니다.

# %%
d3m = (pd.Timestamp(ASOF) - pd.DateOffset(months=3)).date()
c = ds(f'DocumentAggregation(["company"],["ir"],"*","securities.symbol:200",date_from={d3m},date_to={ASOF})')
agg = pd.DataFrame(c["data"]["pods"][1]["content"]["data"])[["key", "count"]]
agg = agg.merge(u[["code", "name", "market"]], left_on="key", right_on="code", how="inner")
print(f"3개월간 IR 자료를 올린 상장사 {len(agg)}곳, 자료 {agg['count'].sum():,}건")
agg[["name", "market", "count"]].rename(columns={"count": "IR 자료 수"}).head(12)

# %% [markdown]
# ## 4. PDF 앞 장 읽기
# 가장 최근 IR 자료 PDF를 받아 텍스트를 뽑습니다(PyMuPDF). 실적발표 자료는 1~2쪽이 표지·유의사항이라 3쪽부터 읽습니다.
# 표·그림 위주 슬라이드는 텍스트가 적게 나옵니다.

# %%
import fitz  # PyMuPDF

def pdf_text(url, start=1, pages=2, limit=1500):
    """PDF의 start쪽(1부터)부터 pages쪽 텍스트."""
    r = requests.get(url, timeout=60); r.raise_for_status()
    doc = fitz.open(stream=r.content, filetype="pdf")
    idx = range(start - 1, min(start - 1 + pages, doc.page_count))
    text = "\n".join(doc[i].get_text() for i in idx)
    print(f"{doc.page_count}쪽 PDF, {start}쪽부터 {len(idx)}쪽 {len(text):,}자")
    return " ".join(text.split())[:limit]

latest = one.sort_values("created_at").iloc[-1]
print(latest.created_at, latest.title)
print(pdf_text(latest.url, start=3, pages=2))

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **IR 자료는 회사가 올린 것만** 있습니다. 모든 상장사가 올리지는 않으며, 같은 자료의 국문·영문본이 따로 잡히기도 합니다.
# - **기사형 문서가 섞입니다.** 회사 홍보 기사가 IR로 분류된 경우가 있습니다(제목으로 구분).
# - PDF 원문은 DeepSearch CDN 링크라 따로 키가 필요 없습니다. 스캔 이미지 PDF는 텍스트가 나오지 않습니다.
