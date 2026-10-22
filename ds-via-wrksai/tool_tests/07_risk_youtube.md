# 7/7 리스크·유튜브 (9개) — 2026-10-22, Claude Haiku 4.5

공통 조건: 도구당 1회만 호출(재시도 없음), page_size=3, 기간 2026-10-15~2026-10-21

## 호출 결과

| 도구 | 호출 파라미터 | 결과 |
|---|---|---|
| dsrch_get_risk_monitoring | symbols="KRX:005930", 기간, page_size=3 | **실패 — Access denied (Premium)** |
| dsrch_get_us_risk_monitoring | symbols="NASDAQ:AAPL", 기간, page_size=3 | **실패 — Access denied (Premium)** |
| dsrch_get_stock_risk_summary | symbol="KRX:005930" | **실패 — Access denied (Premium)** |
| dsrch_get_portfolio_risk | symbols="KRX:005930,KRX:000660" | **실패 — Access denied (Premium)** |
| dsrch_get_youtube_channels | page_size=3 | **실패 — Access denied (Premium)** |
| dsrch_get_youtube_channel_detail | — | **미호출** (채널 목록 실패로 channel_id 없음) |
| dsrch_get_youtube_videos | page_size=3 | **실패 — Resource not found** |
| dsrch_get_youtube_video_detail | — | **미호출** (video_id 없음) |
| dsrch_get_youtube_trending | page_size=3 | **실패 — Resource not found** |

## 파라미터 (에이전트 설명)

| 도구 | 필수 | 선택 (허용값 · 기본값) |
|---|---|---|
| dsrch_get_risk_monitoring | symbols(쉼표 구분) | risk_level(high\|medium\|low), category(disclosure\|news\|price\|volume), date_from, date_to, page(1), page_size(1~100, 20) |
| dsrch_get_us_risk_monitoring | symbols | risk_level, category(filing\|news\|price\|volume), date_from, date_to, page, page_size(20) |
| dsrch_get_stock_risk_summary | symbol | detail_level |
| dsrch_get_portfolio_risk | symbols | — |
| dsrch_get_youtube_channels | — | category, page, page_size(1~50, 20) |
| dsrch_get_youtube_channel_detail | channel_id | — |
| dsrch_get_youtube_videos | — | keyword, channel_id, company_name, symbols, date_from, date_to, page, page_size(20) |
| dsrch_get_youtube_video_detail | video_id | — |
| dsrch_get_youtube_trending | — | category, period(1d\|7d\|1m\|3m\|1y, 기본 1d), page, page_size(20) |

## 메모
- 이 묶음은 전부 KRX 계정 플랜에서 쓸 수 없다. 리스크 4종과 유튜브 채널은 Premium 권한 거부, 유튜브 영상·트렌딩은 엔드포인트 자체가 없음(Resource not found).
