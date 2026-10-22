# 4/7 공시·리서치·IR·특허·SEC·어닝콜 (12개) — 2026-10-22, Claude Haiku 4.5

공통 조건: page_size=3, detail_level=minimal, 국내=삼성전자 2026-09-01~10-21, 미국=AAPL 2026-01-01~10-21

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_search_korean_disclosure | company_name="삼성전자", 기간, page_size=3 | 성공 | 3 / 22 | id, title, content_url, published_at |
| dsrch_search_korean_research | company_name="삼성전자", 기간, page_size=3 | 성공 | 3 / 8 | id, title, content_url, published_at |
| dsrch_search_korean_ir | company_name="삼성전자", 기간, page_size=3 | 성공 | 1 / 1 | id, title, content_url, published_at |
| dsrch_search_korean_patent | company_name="삼성전자", 기간, page_size=3 | 성공 | 3 / 15 | id, title, content_url, published_at |
| dsrch_search_us_filings | symbols="NASDAQ:AAPL", 기간, page_size=3 (4회 시도) | 응답은 오지만 **symbols 필터 미작동** (전체 881,917건에서 반환) | 3 / 881,917 | title, form_type, company, company_ticker, accession_number(standard 이상) |
| dsrch_get_us_filing_detail | filing_id=AAPL과 무관한 임의 ID | data=null | — | **미검증** |
| dsrch_get_us_filing_summary | filing_id=같은 임의 ID | 실패 "Resource not found" | — | **미검증** |
| dsrch_aggregate_us_filings | groupby="company", size=3 | 성공 | 3 | key(회사명), doc_count |
| dsrch_search_earning_calls | company_name="Apple", 기간, detail_level=full (3회 시도) | 성공. 단 "Apple"이 APLE(다른 회사)도 매칭 | 3 / 6 | company_ticker, period, transcript_date, revenue_actual, eps_actual, revenue_change_rate, source |
| dsrch_get_earning_call_detail | transcript_id="AAPL-2026-Q3" | 성공 | 1 | title, company_ticker, period, revenue_actual, eps_actual, exchange, source |
| dsrch_get_earning_call_summary | transcript_id="AAPL-2026-Q3" | 성공 | 1 | 한글 요약 텍스트 |
| dsrch_aggregate_earning_calls | groupby="company", size=3 | 응답은 오지만 **SEC 집계와 같은 결과** (버그 의심) | 3 | key, doc_count |

## 파라미터 (에이전트 설명)

| 도구 | 필수 | 선택 (허용값 · 기본값) |
|---|---|---|
| dsrch_search_korean_disclosure | — | keyword, company_name, symbols, date_from, date_to, page(1), page_size(10, 최대 100), detail_level |
| dsrch_search_korean_research | — | 위와 같음 + research_insight(bool) |
| dsrch_search_korean_ir | — | keyword, company_name, symbols, date_from, date_to, page, page_size, detail_level |
| dsrch_search_korean_patent | — | keyword, company_name, applicant, date_from, date_to, page, page_size, detail_level |
| dsrch_search_us_filings | — | keyword, company_name(부분 일치 주의), symbols(**도구 설명에 "broken"**), filing_type, date_from, date_to, page, page_size, detail_level |
| dsrch_get_us_filing_detail | filing_id | — |
| dsrch_get_us_filing_summary | filing_id | — |
| dsrch_aggregate_us_filings | groupby(company\|filing_type) | keyword, company_name, date_from, date_to, size(10, 최대 100) |
| dsrch_search_earning_calls | — | keyword, company_name, symbols(**"unreliable"**), quarter(Q1~Q4), fiscal_year, date_from, date_to, page, page_size, detail_level(기본 full) |
| dsrch_get_earning_call_detail | transcript_id(`{ticker}-{period}`, 예: AAPL-2026-Q3) | — |
| dsrch_get_earning_call_summary | transcript_id | — |
| dsrch_aggregate_earning_calls | groupby(company\|quarter\|sector) | keyword, company_name, date_from, date_to, size |

## 메모
- 국내 문서 검색 4종(공시·리서치·IR·특허)은 모두 정상이고 응답 형식이 뉴스와 같다.
- SEC 공시는 symbols 필터가 깨져 있어(도구 설명에도 경고) 특정 기업으로 좁히기 어렵다. accession_number를 얻으려면 detail_level=standard 이상이 필요하다.
- SEC detail/summary는 에이전트가 AAPL 공시 ID를 못 구해 임의 ID로 호출했으므로 **동작 여부 미확인**이다.
- 어닝콜 transcript_id는 `티커-연도-분기` 형식으로 바로 만들 수 있어 검색 없이도 조회된다.
