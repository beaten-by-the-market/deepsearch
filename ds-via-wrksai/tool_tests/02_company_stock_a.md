# 2/7 기업·종목 A (12개) — 2026-10-22, Claude Haiku 4.5

공통 조건: page_size=3, detail_level=minimal, 기간 2026-10-15~2026-10-21, 삼성전자 KRX:005930

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_search_companies | keyword="삼성전자", page_size=3 | 성공 | 2 / 22 | symbol, name_ko, exchange, listed_date |
| dsrch_search_market | query="삼성전자", page_size=3 | 성공 | 3 / 22 | symbol, name, matched_by, market_cap |
| dsrch_get_companies | market="KOSPI", page_size=3 | 성공 | 3 / 6,416 | symbol, name, exchange, listed_date |
| dsrch_get_market_symbols | market="KOSPI", page_size=3 | 성공 | 3 | symbol만 |
| dsrch_filter_companies | per_max=10, roe_min=10, page_size=3 | 성공 | 3 / ? | symbol, market |
| dsrch_get_company_detail | symbol="KRX:005930" | 성공 | 1 | name, name_ko, PER, PBR, ROE, dividend_yield, market_cap, business_area_ko, competitors |
| dsrch_get_company_financials | symbol="KRX:005930", limit=3 | 성공 | 6 / 6 | revenue, operating_profit, net_income, fiscal_end_date |
| dsrch_get_fin_statement | symbol="KRX:005930", is_annual=true, date_from="2025-01-01", date_to="2025-12-31", detail_level="key" | 성공 | 53 / 398 | date, account_name, value, level, report_name (재무상태표·손익계산서·현금흐름표·재무비율) |
| dsrch_get_company_dividends | symbol="KRX:005930", limit=3 | 성공 | 16 / 16 (limit 무시) | base_date, dividend_amount, dividend_payment_date |
| dsrch_get_company_events | symbol="KRX:005930", 기간, page_size=3 | 성공, **빈 결과** | 0 | — |
| dsrch_get_stock_events | symbols="KRX:005930", 기간, page_size=3 | 성공, **다른 종목 이벤트 반환** | 3 / 88 | symbol, event_type, event_reason, event_start_date |
| dsrch_get_stock_metrics | symbols="KRX:005930" | 성공, **빈 결과** | 0 / 2,793 | — |

## 파라미터 (에이전트 설명 — 도구별이 아닌 공통 정리로 받음)

| 파라미터 | 형식 | 기본값 | 설명 |
|---|---|---|---|
| keyword | 문자열 | — | search_companies: 회사명·코드 부분 매칭 |
| query | 문자열 | — | search_market: 회사명·코드·키워드 |
| symbol / symbols | "KRX:005930" / 쉼표 구분 | — | 단일 / 복수 종목 |
| market | KOSPI\|KOSDAQ\|KONEX | — | get_companies, get_market_symbols |
| per_max, roe_min | 숫자 | — | filter_companies 조건 (ROE는 %) |
| is_annual | 불린 | true | fin_statement 연간/분기 |
| detail_level | minimal\|standard\|full (fin_statement는 key\|summary\|standard\|full) | standard | 응답 상세도 |
| date_from, date_to | YYYY-MM-DD | — | 기간 |
| limit | 정수 1~50 | 10 | financials, dividends |
| page, page_size | 정수 | 1 / 50 | 페이징 |

## 메모
- `get_stock_events`는 symbols 필터가 먹지 않고 다른 종목 이벤트를 준다. `get_stock_metrics`는 빈 결과(에이전트 목록 설명에도 "심볼 필터 불안정").
- `get_company_dividends`는 limit=3을 줘도 16건 전체를 반환.
- `get_fin_statement` key 모드: 398개 계정 중 53개만.
- Haiku는 파라미터 표를 도구별로 나누지 않고 공통으로 정리했고 "필수 여부"가 부정확해 보여 생략했다.
- 사용량: 27% → 35% (+8%). 모델을 Haiku로 낮춰도 Sonnet(+10%)과 차이가 작다 → 비용 대부분이 모델이 아니라 **도구 호출 건수**에서 나오는 것으로 보인다.
