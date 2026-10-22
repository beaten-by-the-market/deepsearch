# 6/7 산업·매크로·시장 (12개) — 2026-10-22, Claude Haiku 4.5

공통 조건: 도구당 1회만 호출(재시도 없음), page_size=3, detail_level=minimal, 기간 2026-10-15~2026-10-21

## 호출 결과

| 도구 | 호출 파라미터 | 결과 | 건수 / 전체 | 응답 data 주요 필드 |
|---|---|---|---|---|
| dsrch_get_industries | (없음) | **실패 — Premium 제한** | — | — |
| dsrch_get_industry_detail | industry_id="semiconductor" | **실패 — Premium 제한** | — | — |
| dsrch_get_industry_reports | industry_id="semiconductor", 기간, page_size=3 | **실패 — Premium 제한** | — | — |
| dsrch_get_industry_companies | industry_id="semiconductor", page_size=3 | 응답 옴, **필터 미적용 의심** | 3 / 6,416 | name, name_ko, symbol, exchange, listed_date |
| dsrch_get_industry_news | industry_id="semiconductor", 기간, page_size=3 | 응답 옴, **필터 미적용 의심** | 3 / 221,675 | id, title, content_url, published_at |
| dsrch_get_industry_topics | industry_id="semiconductor", 기간, page_size=3 | 응답 옴, **필터 미적용 의심** | 3 / 6,958 | id, rank, title, score, date |
| dsrch_get_korean_industry_briefing | industry_id="semiconductor", 기간 | 성공 (최대 5건으로 잘림) | 5 | id, short_briefing |
| dsrch_get_global_industry_briefing | industry_id="semiconductor", 기간 | 성공 (최대 5건) | 5 | id, short_briefing |
| dsrch_get_korean_macro_briefing | date_from=date_to=2026-10-21 | 성공 (최대 5건) | 5 | id, short_briefing |
| dsrch_get_global_macro_briefing | date_from=date_to=2026-10-21 | 성공 (최대 5건) | 5 | id, short_briefing |
| dsrch_get_market_indices | (없음) | 성공 | 85 | type, symbol, name_ko, open, high, low, close, volume, change, change_percent, date |
| dsrch_get_market_holidays | country_code="kr", year=2026 | 성공 | 20 / 126 | date, country_code, exchange, name |

## 파라미터 (에이전트 설명)

| 도구 | 필수 | 선택 (허용값 · 기본값) |
|---|---|---|
| dsrch_get_industries | — | — (Premium) |
| dsrch_get_industry_detail | industry_id | — (Premium) |
| dsrch_get_industry_reports | industry_id | keyword, date_from, date_to, page(1), page_size(10) (Premium) |
| dsrch_get_industry_companies | industry_id | sort_by, page(1), page_size(50) |
| dsrch_get_industry_news | industry_id | date_from, date_to, page, page_size(10), detail_level |
| dsrch_get_industry_topics | industry_id | date_from, date_to, page, page_size(10), detail_level |
| dsrch_get_korean_industry_briefing | — | industry_id, date_from, date_to, simple_response(true), detail_level |
| dsrch_get_global_industry_briefing | — | industry_id, date_from, date_to, simple_response(true), detail_level |
| dsrch_get_korean_macro_briefing | — | briefing_type(CLOSE\|PRE_MARKET), category, date_from, date_to, simple_response(true), detail_level |
| dsrch_get_global_macro_briefing | — | briefing_type(CLOSE\|PRE_MARKET), category, date_from, date_to, simple_response(true), detail_level |
| dsrch_get_market_indices | — | — |
| dsrch_get_market_holidays | — | country_code(kr\|us, 기본 kr), year(기본 올해) |

## 메모
- 산업 목록(`get_industries`)이 Premium이라 실제 industry_id를 얻을 수 없다. 에이전트가 "semiconductor"를 추측해서 넣었고, 결과 건수(6,416 = 전체 상장사 수 수준)로 보아 **필터가 무시된 것으로 보인다.** 산업별 기능은 사실상 쓰기 어렵다.
- 매크로·산업 브리핑은 wrks 응답 최적화로 최대 5건, 각 `short_briefing` 요약만 온다.
- `get_market_indices`는 파라미터 없이 85개 지수의 당일 시세를 준다.
