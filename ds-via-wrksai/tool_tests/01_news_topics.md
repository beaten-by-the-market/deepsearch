# 1/7 뉴스·토픽 (11개) — 2026-10-22, Claude Sonnet 5

공통 조건: page_size=3, detail_level=minimal, 기간 2026-10-15~2026-10-21, 국내=삼성전자, 해외=Apple

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_search_korean_articles | keyword="삼성전자", date_from/to, detail_level=minimal, page_size=3 | 성공 | 2 / 4,368 | id, title, content_url, published_at |
| dsrch_search_kr_news_section | sections="economy", company_name="삼성전자", date_from/to, page_size=3 | 성공 | 3 / 691 | id, title, content_url, published_at |
| dsrch_aggregate_korean_articles | groupby="company", company_name→keyword="삼성전자", size=3 | ok=true지만 **data=[]** (재시도 동일) | 0 | 확인 불가 |
| dsrch_search_global_articles | company_name="Apple", date_from/to, page_size=3 | 성공 | 3 / 280 | id, title, content_url, published_at |
| dsrch_search_gl_news_section | section="technology", company_name="Apple", page_size=3 | 성공 | 3 / 93 | id, title, content_url, published_at |
| dsrch_aggregate_global_articles | groupby="company", company_name→keyword="Apple", size=3 | ok=true지만 **data=[]** (재시도 동일) | 0 | 확인 불가 |
| dsrch_get_korean_trending_topics | max_topics=3, page_size=3 | 성공 | 3 / 113 | id, rank, title, score, date |
| dsrch_get_global_trending_topics | max_topics=3, page_size=3 | 성공 | 3 / 1,154 | id, rank, title (minimal이라 score/date 없음) |
| dsrch_search_korean_topics | company_name="삼성전자", date_from/to, page_size=3 | 성공 | 3 / 144 | id, rank, title, score, date |
| dsrch_search_global_topics | company_name="Apple", date_from/to, page_size=3 | 성공 | 3 / 49 | id, rank, title |
| dsrch_get_topic_insights | topic_id="1764555562999222276" (search_korean_topics 결과) | 성공 | 1 (단건) | section, content, topic_type, questions[], created_at, updated_at, id |

## 파라미터 (에이전트 설명)

| 도구 | 파라미터 |
|---|---|
| dsrch_search_korean_articles | keyword(단일 키워드 권장), company_name, symbols("KRX:005930"), date_from/date_to(YYYY-MM-DD), order("published_at"\|"score"), page(기본 1), page_size(1~50, 기본 5), detail_level("minimal"\|"standard"\|"full", 기본 minimal) — 모두 선택 |
| dsrch_search_kr_news_section | **sections(필수, 콤마 구분: politics, economy, society, culture, world, tech, entertainment, opinion)**, keyword/company_name/symbols, date_from/to, page, page_size(1~50, 기본 5), detail_level |
| dsrch_aggregate_korean_articles | **groupby(필수: company\|publisher\|section\|esg)**, keyword/company_name/symbols, date_from/to, size(1~100, 기본 10) |
| dsrch_search_global_articles | keyword/company_name/symbols, date_from/to, page, page_size(1~50, 기본 10), detail_level — 모두 선택 |
| dsrch_search_gl_news_section | **section(필수, 단일값: markets\|economy\|technology\|business\|politics\|world)**, keyword/company_name/symbols, date_from/to, page, page_size(기본 10), detail_level |
| dsrch_aggregate_global_articles | **groupby(필수: company\|publisher\|section\|esg)**, keyword/company_name/symbols, date_from/to, size(1~100, 기본 10) |
| dsrch_get_korean_trending_topics | page, page_size(1~50, 기본 5), max_topics(1~50, 기본 10), detail_level(기본 standard) — 필수 없음, 당일 토픽 고정 |
| dsrch_get_global_trending_topics | company_name/symbols/keyword(필터), order(기본 published_at), page, page_size(기본 5), max_topics(기본 10), detail_level(기본 standard) |
| dsrch_search_korean_topics | keyword/company_name/symbols, date_from/to, page, page_size(1~50, 기본 5), detail_level(기본 standard) |
| dsrch_search_global_topics | keyword/company_name/symbols, date_from/to, page, page_size(기본 5), detail_level(기본 standard) |
| dsrch_get_topic_insights | **topic_id(필수)** — 토픽 검색·트렌딩 결과의 id |

## 메모
- 국내 뉴스 섹션은 `sections`(복수, 콤마), 해외는 `section`(단일)로 이름과 형식이 다르다.
- 집계(aggregate) 2종은 기업·기간 조건에서 빈 배열. 조건 없이 또는 groupby=publisher로 재확인 필요.
- 사용량: 17% → 27% (+10%)
