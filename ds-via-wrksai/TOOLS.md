# 웍스AI DeepSearch 도구 (`dsrch_*` 79개) 테스트 결과

> 테스트: 2026-10-22, KRX 웍스AI 계정, "딥써치" 에이전트(Sonnet 5 → Haiku 4.5).
> 도구마다 최소 파라미터로 실제 호출했다. 묶음별 상세(호출 파라미터, 응답 필드, 파라미터 정의)는 [tool_tests/](tool_tests/)에 있다.
> 파라미터 정의는 에이전트가 도구 설명을 보고 옮겨 준 것이라 원문 스키마와 다를 수 있다.

## 요약

| 상태 | 개수 | 의미 |
|---|---|---|
| ✅ 정상 | 48 | 요청한 조건대로 데이터가 옴 |
| ⚠️ 이상 | 15 | 응답은 오지만 빈 결과이거나 필터가 무시됨 |
| ❌ 사용 불가 | 12 | Premium 권한 거부 8, 미구현·엔드포인트 없음 4 |
| ❔ 미검증 | 4 | 필요한 ID를 못 구해 제대로 호출하지 못함 |

**KRX 업무에 바로 쓸 수 있는 것**: 국내 뉴스·공시·리서치·IR·특허 검색, 재무제표, 일별 주가·분봉, 배당, 종목 스크리닝, 시장 지수, 휴장일, 종목·매크로 브리핑, 테마별 종목.

## 전체 목록

| 분류 | 도구 | 상태 | 비고 |
|---|---|---|---|
| 뉴스 | search_korean_articles | ✅ | 페이지당 최대 10건, 제목 필터 없음 |
| | search_kr_news_section | ✅ | `sections` 필수(콤마 구분) |
| | aggregate_korean_articles | ⚠️ | groupby=company + 기업·기간 조건에서 빈 배열 |
| | search_global_articles | ✅ | |
| | search_gl_news_section | ✅ | `section` 필수(단일값) |
| | aggregate_global_articles | ⚠️ | 빈 배열 |
| 토픽 | get_korean_trending_topics | ✅ | 당일 고정 |
| | get_global_trending_topics | ✅ | |
| | search_korean_topics | ✅ | |
| | search_global_topics | ✅ | |
| | get_topic_insights | ✅ | topic_id 필요 |
| 기업 | search_companies | ✅ | |
| | search_market | ✅ | 종목·ETF 통합 검색 |
| | get_companies | ✅ | market=KOSPI 등 |
| | get_market_symbols | ✅ | 심볼만 |
| | filter_companies | ✅ | per_max, roe_min 등 |
| | get_company_detail | ✅ | PER·PBR·ROE·시총·경쟁사 |
| | get_company_financials | ✅ | 매출·영업이익·순이익 요약 |
| | get_fin_statement | ✅ | key 모드는 398개 중 53개 계정. **비상장 외감기업도 됨** (이나인페이 = NICE:C16181, 2021~2025 별도, `report_ids`=BalanceSheet\|Income\|CashFlow로 나눠 full 조회 시 잘림 없음 — 2026-10-22 사용자 실행) |
| | get_company_dividends | ✅ | limit 무시 |
| | get_company_events | ⚠️ | 기간 내 빈 결과(데이터 없음일 수 있음) |
| | get_stock_events | ⚠️ | symbols 필터 무시, 다른 종목 반환 |
| | get_stock_metrics | ⚠️ | 빈 결과 |
| 주가 | get_company_stock_price | ✅ | 일별 OHLCV |
| | get_company_stock_aggregate | ✅ | 기간 통계 |
| | get_stock_minute_price | ✅ | page_size 무시, 60건 |
| | get_trending_companies | ✅ | |
| | get_technical_indicators | ❌ | 미구현 |
| 브리핑·테마 | get_stock_briefing | ✅ | 종목 AI 브리핑 + 관련 기사 |
| | get_korean_stock_briefing_v2 | ⚠️ | 빈 결과 (날짜 형식 재확인 필요) |
| | get_us_stock_briefing_v2 | ⚠️ | 빈 결과 |
| | get_invest_tags | ⚠️ | symbols 지정 시 빈 결과 |
| | get_invest_tag_stocks | ✅ | tag_name="AI(인공지능)" 형식 |
| 공시·리서치 | search_korean_disclosure | ✅ | DART |
| | search_korean_research | ✅ | research_insight 옵션 |
| | search_korean_ir | ✅ | |
| | search_korean_patent | ✅ | |
| SEC | search_us_filings | ⚠️ | symbols 필터 깨짐(도구 설명에도 경고) |
| | get_us_filing_detail | ❔ | 유효한 filing_id 미확보 |
| | get_us_filing_summary | ❔ | 위와 같음 |
| | aggregate_us_filings | ✅ | |
| 어닝콜 | search_earning_calls | ✅ | company_name 부분 일치 주의 |
| | get_earning_call_detail | ✅ | transcript_id = `AAPL-2026-Q3` 형식 |
| | get_earning_call_summary | ✅ | 한글 요약 |
| | aggregate_earning_calls | ⚠️ | SEC 집계와 같은 결과(버그 의심) |
| ETF | get_etfs | ✅ | |
| | search_etfs | ✅ | |
| | filter_etfs | ✅ | 보수·AUM·배당 조건 |
| | get_etf_detail | ✅ | 구성·업종 비중 |
| | get_etf_holdings | ✅ | limit 무시 |
| | get_etf_price | ✅ | 일별이 아니라 현재 스냅샷 |
| | get_etf_dividends | ✅ | |
| | get_etf_briefing | ✅ | 파라미터 이름이 `etf_symbol` |
| | get_etf_news | ✅ | |
| | get_etf_topics | ✅ | |
| | get_etf_global_news | ⚠️ | 국내 ETF로 시험해 빈 결과 |
| | get_etf_global_topics | ⚠️ | 위와 같음 |
| | get_etf_matchup | ❌ | 미구현 |
| 산업 | get_industries | ❌ | Premium |
| | get_industry_detail | ❌ | Premium |
| | get_industry_reports | ❌ | Premium |
| | get_industry_companies | ⚠️ | industry_id를 몰라 추측값 사용, 필터 무시된 듯 |
| | get_industry_news | ⚠️ | 위와 같음 |
| | get_industry_topics | ⚠️ | 위와 같음 |
| 브리핑 | get_korean_industry_briefing | ✅ | 최대 5건 요약 |
| | get_global_industry_briefing | ✅ | 최대 5건 요약 |
| | get_korean_macro_briefing | ✅ | briefing_type CLOSE\|PRE_MARKET |
| | get_global_macro_briefing | ✅ | |
| 시장 | get_market_indices | ✅ | 85개 지수 당일 시세 |
| | get_market_holidays | ✅ | |
| 리스크 | get_risk_monitoring | ❌ | Premium |
| | get_us_risk_monitoring | ❌ | Premium |
| | get_stock_risk_summary | ❌ | Premium |
| | get_portfolio_risk | ❌ | Premium |
| 유튜브 | get_youtube_channels | ❌ | Premium |
| | get_youtube_videos | ❌ | Resource not found |
| | get_youtube_trending | ❌ | Resource not found |
| | get_youtube_channel_detail | ❔ | channel_id 없음 |
| | get_youtube_video_detail | ❔ | video_id 없음 |

## 공통 규칙

- **응답 형식**: `{"detail": {"code": "SUCCESS", "ok": true}, "total_items", "total_pages", "page", "page_size", "data": [...]}`. 권한이 없으면 "Access denied", 없는 기능은 "Resource not found".
- **종목**: `symbol="KRX:005930"`, 미국은 `NASDAQ:AAPL`. 일부 도구는 `005930`만 넣어도 동작.
- **날짜**: 대부분 `YYYY-MM-DD`. 브리핑 계열 일부는 `yyyyMMdd`.
- **detail_level**: `minimal | standard | full` (재무제표는 `key | summary | standard | full`). minimal이면 필드가 크게 줄어든다.
- **응답 축소**: wrks가 응답을 줄여 모델에 넘긴다 (`_meta.simplified_count`, `_truncated`). 뉴스는 페이지당 10건, 브리핑은 최대 5건.
- **필터 신뢰도**: `symbols` 필터는 여러 도구(SEC, 종목 이벤트, 종목 지표, 어닝콜)에서 무시되거나 불안정하다. 기업은 `company_name`이나 `symbol`(단수)로 좁히는 편이 낫다.

## 기존 스킬(`skills/deepsearch`) 기능과의 대응

DeepSearch API 키가 만료되어, 스킬 기능을 웍스로 옮길 수 있는지 정리했다.

| 스킬 기능 | 웍스 대응 | 차이 |
|---|---|---|
| DocumentSearch (뉴스) | search_korean_articles, search_kr_news_section | `title:`, `securities.market:`, `polarity.name:` 같은 필드 쿼리 불가. 키워드 하나 + 기업명만 |
| DocumentSearch (리포트·공시·IR·특허) | search_korean_research / disclosure / ir / patent | 같은 제약 |
| DocumentTrends | 대응 없음 | 토픽 도구로 일부 대체 |
| DocumentAggregation | aggregate_korean_articles | 테스트에서 빈 결과 |
| GetSentimentScore | 대응 없음 | |
| GetFinancialStatements | get_fin_statement, get_company_financials | 동작함 |
| 주가 자연어 쿼리 | get_company_stock_price, get_company_stock_aggregate | 동작함 |
| GetCompanyDividends | get_company_dividends | 동작함 |
| GetCompanyShareholders / Executives | 대응 없음 | |
| SearchTargetPrices (목표가) | 대응 없음 | 리서치 검색으로 일부 대체 |
| FindConglomerate / GetConglomerateMembers | 대응 없음 | |
| 조건 스크리닝 (`매출 > 1조 and ...`) | filter_companies | PER·PBR·ROE·시총 등 정해진 필터만 |
| market_overview.py (시황) | get_market_indices + get_trending_companies + get_korean_macro_briefing | 조합하면 비슷하게 구성 가능 |
| (스킬에 없음) | 해외 뉴스, ETF, 어닝콜, 종목·매크로 브리핑, 분봉 | 웍스에서만 확인됨 |

## 테스트 비용

| 묶음 | 모델 | 사용량 |
|---|---|---|
| 1 뉴스·토픽 | Sonnet 5 | 17% → 27% |
| 2 기업·종목 A | Haiku 4.5 | 27% → 35% |
| 3 주가·브리핑·테마 | Haiku 4.5 | 35% → 42% |
| 4 공시·SEC·어닝콜 | Haiku 4.5 | 42% → 54% (재시도 많음) |
| 5 ETF | Haiku 4.5 | 54% → 63% |
| 6 산업·매크로·시장 | Haiku 4.5 | 63% → 70% |
| 7 리스크·유튜브 | Haiku 4.5 | 70% → 75% |

모델을 Sonnet에서 Haiku로 바꿔도 묶음당 비용 차이가 작았다. 비용은 주로 **도구 호출 횟수**에 비례하는 것으로 보인다.
