# 3/7 주가·브리핑·테마 (10개) — 2026-10-22, Claude Haiku 4.5

공통 조건: page_size=3, detail_level=minimal, 기간 2026-10-15~2026-10-21, 분봉은 2026-10-21, 국내=KRX:005930, 미국=AAPL

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_get_company_stock_price | symbol=KRX:005930, date_from/to, page_size=3 | 성공 | 3 | date, close, volume (minimal) |
| dsrch_get_company_stock_aggregate | symbol=KRX:005930, date_from/to | 성공 | 1 | symbol, open, high, low, close, volume, change, change_percent, market_cap |
| dsrch_get_stock_minute_price | symbol=005930, date=20261021, page_size=3 | 성공 (page_size 무시, 60건, `_truncated=true`) | 60 | close, volume |
| dsrch_get_stock_briefing | symbol=KRX:005930, date=20261021 | 성공 | 1 | date, symbol, company_name, change_rate, briefing, article{id, title, author, section, summary, publisher, created_at, content_url, image_urls} |
| dsrch_get_korean_stock_briefing_v2 | date=20261021, symbol=KRX:005930 | **빈 결과** (data=[], total_count=0) | 0 | — |
| dsrch_get_us_stock_briefing_v2 | date=20261021, symbol=NASDAQ:AAPL | **빈 결과** | 0 | — |
| dsrch_get_trending_companies | country_code=kr, page_size=3 | 성공 | 3 / 100 | symbol |
| dsrch_get_invest_tags | country_code=kr, symbols=KRX:005930 | **빈 결과** | 0 | — |
| dsrch_get_invest_tag_stocks | tag_name="AI(인공지능)", country_code=kr, page_size=3 | 성공 | 3 / 225 | country_code, exchange, symbol, name, name_ko, market_cap, invest_tags[] |
| dsrch_get_technical_indicators | symbol=KRX:005930 | **실패** — "Resource not found" (미구현) | 0 | — |

## 파라미터 (에이전트 설명)

| 도구 | 필수 | 선택 (허용값 · 기본값) |
|---|---|---|
| dsrch_get_company_stock_price | symbol | period(기본 1y), date_from, date_to, page(1), page_size(10), detail_level(standard) |
| dsrch_get_company_stock_aggregate | symbol | period(1y), date_from, date_to, detail_level(standard) |
| dsrch_get_stock_minute_price | symbol | interval(1\|5\|15\|30\|60, 기본 1), date, page(1), page_size(100), detail_level(minimal) |
| dsrch_get_stock_briefing | symbol | date, simple_response(false), detail_level(minimal) |
| dsrch_get_korean_stock_briefing_v2 | date | briefing_type, symbol, detail_level(standard) |
| dsrch_get_us_stock_briefing_v2 | date | briefing_type, symbol, detail_level(standard) |
| dsrch_get_trending_companies | — | country_code(kr\|us, 기본 kr), page, page_size(10), include_briefing(false), detail_level(minimal) |
| dsrch_get_invest_tags | country_code(기본 kr) | exchange, symbols, detail_level(standard) |
| dsrch_get_invest_tag_stocks | tag_name | country_code(kr\|us), page, page_size(50) |
| dsrch_get_technical_indicators | symbol | indicators, period(1m\|3m\|6m\|1y, 기본 3m) — 미구현 |

## 메모
- 브리핑 v2 두 종은 `date=20261021`(YYYYMMDD)로만 시도하고 재시도하지 않았다. 날짜 형식(YYYY-MM-DD)이나 `briefing_type` 지정으로 다시 확인할 필요가 있다.
- `get_invest_tags`에 symbols를 주면 빈 배열. 태그 이름은 "AI(인공지능)" 형식으로 `get_invest_tag_stocks`에 바로 넣으면 동작했다.
- 분봉은 page_size를 무시하고 60건을 반환하며 잘림 표시가 붙는다.
