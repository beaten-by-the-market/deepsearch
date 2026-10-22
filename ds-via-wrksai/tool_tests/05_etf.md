# 5/7 ETF (13개) — 2026-10-22, Claude Haiku 4.5

공통 조건: 도구당 1회만 호출(재시도 없음), page_size=3, detail_level=minimal, 기간 2026-10-15~2026-10-21, ETF=KODEX 200(KRX:069500)

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_get_etfs | page_size=3 | 성공 | 3 | name, symbol |
| dsrch_search_etfs | keyword="KODEX", page_size=3 | 성공 | 3 | name, symbol, issuer_name, category, fee, trace_index_name |
| dsrch_filter_etfs | page_size=3 | 성공 | 3 | name, symbol, nav, price |
| dsrch_get_etf_detail | symbol="KRX:069500", simple_response=true | 성공 | 1 | name, symbol, issuer_name, category, fee, description, industry_weights[], etf_holdings[], market_info |
| dsrch_get_etf_holdings | symbol="KRX:069500", limit=3 | 성공 (limit 무시) | 10 | symbol, name |
| dsrch_get_etf_price | symbol="KRX:069500", 기간 | 성공, **일별 시계열이 아니라 현재 스냅샷 1건** | 1 | name, symbol, listed_shares, industry_weights[], etf_holdings[], market_info(nav, aum, trade_volume 등) |
| dsrch_get_etf_dividends | symbol="KRX:069500", limit=3 | 성공 | 3 / 4 | base_date, dividend_amount, dividend_payment_date, is_forecast |
| dsrch_get_etf_briefing | etf_symbol="KRX:069500", simple_response=true | 성공 | 3 | briefing, date, name, symbol, price, change_rate, stocks[] |
| dsrch_get_etf_news | symbol="KRX:069500", 기간, page_size=3 | 성공 | 2 / 1,910 | id, title, content_url, published_at |
| dsrch_get_etf_topics | symbol="KRX:069500", 기간, page_size=3 | 성공 | 3 / 140 | id, rank, title, score, date |
| dsrch_get_etf_global_news | symbol="KRX:069500", 기간, page_size=3 | 성공, **빈 결과** | 0 | — |
| dsrch_get_etf_global_topics | symbol="KRX:069500", 기간, page_size=3 | 성공, **빈 결과** | 0 | — |
| dsrch_get_etf_matchup | symbol="KRX:069500", limit=3 | **실패** — "Resource not found" (미구현) | 0 | — |

## 파라미터 (에이전트 설명)

| 도구 | 필수 | 선택 (허용값 · 기본값) |
|---|---|---|
| dsrch_get_etfs | — | category, issuer, page(1), page_size(1~100, 50), detail_level(minimal) |
| dsrch_search_etfs | keyword | category, issuer, page(1), page_size(1~100, 20) |
| dsrch_filter_etfs | — | category, issuer, aum_min, aum_max, expense_ratio_max, dividend_yield_min, tracking_error_max, sort_by(aum\|expense_ratio\|dividend_yield\|volume, 기본 aum), sort_order(asc\|desc, 기본 desc), page, page_size(50), detail_level |
| dsrch_get_etf_detail | symbol | simple_response(false) |
| dsrch_get_etf_holdings | symbol | limit(1~100, 20), detail_level |
| dsrch_get_etf_price | symbol | date_from, date_to |
| dsrch_get_etf_dividends | symbol | limit(1~50, 10) |
| dsrch_get_etf_briefing | **etf_symbol** (다른 ETF 도구와 이름 다름) | date(yyyyMMdd), simple_response(false), detail_level |
| dsrch_get_etf_news | symbol | date_from, date_to, page, page_size(1~50, 10), detail_level |
| dsrch_get_etf_topics | symbol | date_from, date_to, page, page_size(10), detail_level |
| dsrch_get_etf_global_news | symbol | date_from, date_to, page, page_size(10) |
| dsrch_get_etf_global_topics | symbol | date_from, date_to, page, page_size(10) |
| dsrch_get_etf_matchup | symbol | limit(1~20, 5) — 미구현 |

## 메모
- 해외 ETF 뉴스·토픽은 국내 ETF(069500)로 시험해서 빈 결과일 수 있다. 미국 ETF(예: SPY)로 확인이 필요하다.
- `get_etf_price`는 기간을 줘도 일별 가격이 아니라 현재 정보 1건을 준다.
