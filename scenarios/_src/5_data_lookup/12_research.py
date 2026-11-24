# %% [markdown]
# # 5-12 증권사 리포트 가져오기 — 섹션별·종목별·키워드별 리포트와 PDF
#
# **질문 예시:** "이번 주 나온 산업 리포트 목록 줘", "SK하이닉스 최근 3개월 리포트 다 모아줘",
# "반도체 관련 리포트 최신 것 PDF 내용 보여줘"
#
# DeepSearch `["research"]`에는 증권사 리포트가 6개 섹션으로 들어 있습니다:
# `company`(기업), `industry`(산업), `market`(시황), `strategy`(투자전략), `economy`(경제), `bond`(채권).
# 문서마다 증권사(`publisher`)와 PDF 링크가 있습니다. 목표주가·의견을 엮은 분석은 [2-11 증권사 리포트 흐름](../2_disclosure_news/11_analyst_reports.ipynb)을 보세요.

# %%
ASOF = "2026-11-24"
STOCK = "000660"       # SK하이닉스
KEYWORD = "반도체"

if IN_COLAB:
    !pip -q install pymupdf

SECTIONS = {"기업": "company", "산업": "industry", "시황": "market", "투자전략": "strategy", "경제": "economy", "채권": "bond"}

# %% [markdown]
# ## 1. 섹션별 리포트 수 (최근 4주)
# 건수는 문서를 받지 않고 `total_matches`만 봅니다(섹션당 1회 호출).

# %%
d4w = (pd.Timestamp(ASOF) - pd.Timedelta(days=27)).date()
cnt = {}
for name, sec in SECTIONS.items():
    t, _ = doc_search("research", [sec], "*", d4w, ASOF, count=1)
    cnt[name] = t
pd.Series(cnt, name="리포트 수(4주)").to_frame()

# %% [markdown]
# ## 2. 증권사별 리포트 수 (최근 4주, 전 섹션)
# 집계는 `publisher:N`으로 합니다(`publisher.raw:N`은 집계에서 서버 오류 — 검색 쿼리 안에서는 `publisher.raw:('삼성증권')`처럼 씁니다).

# %%
c = ds(f'DocumentAggregation(["research"],[],"*","publisher:30",date_from={d4w},date_to={ASOF})')
pubs = pd.DataFrame(c["data"]["pods"][1]["content"]["data"])[["key", "count"]]
pubs.columns = ["증권사", "리포트 수"]
print(f"4주간 리포트를 낸 증권사 {len(pubs)}곳")
pubs.head(15)

# %% [markdown]
# ## 3. 종목별 — SK하이닉스 최근 3개월 기업 리포트
# 종목은 `securities.symbol:6자리`로 지정합니다. 리서치의 회사 이름은 공식명('에스케이하이닉스')이라
# `securities.name:SK하이닉스`로는 일부만 걸립니다.

# %%
d3m = (pd.Timestamp(ASOF) - pd.DateOffset(months=3)).date()
t, rep = doc_search("research", ["company"], f"securities.symbol:{STOCK}", d3m, ASOF, count=100)
print(f"전체 {t}건 | 증권사별:", rep.publisher.value_counts().to_dict())
rep[["created_at", "publisher", "title", "url"]].head(10)

# %% [markdown]
# ## 4. 키워드 — 산업 리포트 중 제목에 '반도체'

# %%
d2w = (pd.Timestamp(ASOF) - pd.Timedelta(days=13)).date()
t, ind = doc_search("research", ["industry"], f"title:{KEYWORD}", d2w, ASOF, count=100)
print(f"최근 2주 산업 리포트 중 제목에 '{KEYWORD}' {t}건")
ind[["created_at", "publisher", "title"]].head(10)

# %% [markdown]
# ## 5. PDF 읽기 — 최신 기업 리포트 첫 장
# 기업 리포트 첫 장에는 보통 투자의견·목표주가·요약이 있습니다.

# %%
import fitz  # PyMuPDF

def pdf_text(url, start=1, pages=1, limit=1500):
    r = requests.get(url, timeout=60); r.raise_for_status()
    doc = fitz.open(stream=r.content, filetype="pdf")
    idx = range(start - 1, min(start - 1 + pages, doc.page_count))
    text = "\n".join(doc[i].get_text() for i in idx)
    print(f"{doc.page_count}쪽 PDF, {len(text):,}자")
    return " ".join(text.split())[:limit]

latest = rep.sort_values("created_at").iloc[-1]
print(latest.created_at, latest.publisher, latest.title)
txt = pdf_text(latest.url)
print(txt)

# %%
# 첫 장에서 목표주가·투자의견 문구 찾기 (리포트 양식마다 달라 정규식은 참고용)
import re
PATTERNS = {"목표주가": r"목표주가[^0-9]{0,15}([\d,]+\s*(?:만원|원))", "투자의견": r"투자의견\s*([A-Za-z가-힣]+)"}
for name, pat in PATTERNS.items():
    m = re.search(pat, txt)
    print(name, "→", m.group(1) if m else "못 찾음")

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **증권사 커버리지가 제한적입니다.** 16개 기관(4주 기준) 리포트만 들어 있고 KB·NH·키움 등은 없습니다.
#   일부 증권사는 옛 이름('미래에셋대우', '신한금융투자', '메리츠종금증권')으로 들어 있어 증권사별로 묶을 때 주의하세요.
# - **목표주가·의견은 구조화된 값이 따로 있습니다**(`SearchTargetPrices`) — PDF 정규식보다 그쪽이 정확합니다(2-11).
# - PDF는 DeepSearch CDN 링크라 키 없이 받을 수 있습니다. 재배포에는 각 증권사 이용 조건이 적용됩니다.
