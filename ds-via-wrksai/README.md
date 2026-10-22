# ds-via-wrksai — 웍스AI 경유 DeepSearch 사용

웍스AI(https://wrks.ai, KRX 기업 계정)의 **금융/기업 데이터** 도구는 내부적으로 DeepSearch API를 호출한다.
이 폴더는 그 구조와 한계를 조사하고, "딥써치" 에이전트(나만의 에이전트, id 38903)의 프롬프트를 다듬기 위한 작업 공간이다.

> 조사일: 2026-10-22. Claude in Chrome으로 로그인 세션에서 직접 테스트.

---

## 1. 구조 (네트워크 확인 결과)

| 구간 | 내용 |
|------|------|
| `gateway-api.wrks.ai` | REST. 에이전트 설정(`/ai/agent/{id}`), 모델 목록, 도구 목록(`/ai/chat/internal-tools`, `/mcp/hub/available`), 사용량(`/my/usage`) |
| `ai3-api.wrks.ai` | 채팅 스트리밍. XHR/fetch 목록에 메시지 전송 요청이 안 보이고 `/health`만 보임 → **WebSocket** 채널로 추정 |
| 도구 계층 | 모델이 **MCP 도구 `dsrch_*`** 를 호출 → wrks 서버가 DeepSearch에 요청 |

- 브라우저가 DeepSearch를 직접 부르지 않는다. DeepSearch 호출은 전부 wrks 서버 쪽에서 일어난다.
- 응답 형식은 이 레포의 `compute?input=` 쿼리 API가 아니라 **DeepSearch의 신형 REST API** 형태다.
  - `{"detail": {"code": "SUCCESS", "ok": true}, "total_items", "total_pages", "page", "data": [...]}`
  - 종목 식별자는 `symbol="KRX:005930"` 형식
  - wrks가 응답을 줄여서 모델에 넘긴다: `"_meta": {"original_count": 215, "simplified_count": 48, "filter_mode": "key_only"}`
- 따라서 `DocumentSearch(...)`, `title:`/`securities.market:` 같은 **쿼리 문법과 자연어 스크리닝식("매출 > 1조 and ...")은 쓸 수 없다.** 함수별 파라미터만 쓸 수 있다.

## 2. 사용 가능한 도구 (에이전트 자체 보고, 103개)

> 79개 `dsrch_*` 도구를 하나씩 실제로 호출한 결과는 [TOOLS.md](TOOLS.md)에 있다.

에이전트에게 원문 스키마를 요청하면 "시스템 설정이라 공개 불가"라고 거부하고, 이름과 설명만 준다.

**DeepSearch `dsrch_*` (79개)**

| 분류 | 도구 |
|------|------|
| 뉴스·토픽 | `search_korean_articles`, `search_kr_news_section`, `aggregate_korean_articles`, `search_global_articles`, `search_gl_news_section`, `aggregate_global_articles`, `get_korean/global_trending_topics`, `search_korean/global_topics`, `get_topic_insights` |
| 기업·종목 | `search_companies`, `search_market`, `get_companies`, `get_market_symbols`, `filter_companies`(PER/PBR/ROE/시총 스크리닝), `get_company_detail`, `get_company_financials`, `get_fin_statement`(key/summary/standard/full), `get_company_dividends`, `get_company_events`, `get_stock_events`, `get_stock_metrics`(심볼 필터 불안정), `get_company_stock_price`(일별 OHLCV), `get_company_stock_aggregate`, `get_stock_minute_price`, `get_stock_briefing`, `get_korean/us_stock_briefing_v2`, `get_trending_companies`, `get_invest_tags`, `get_invest_tag_stocks`, `get_technical_indicators`(미구현) |
| 공시·리서치·IR·특허 | `search_korean_disclosure`(DART), `search_korean_research`(`research_insight` 옵션), `search_korean_ir`, `search_korean_patent`, `search/get_us_filing*`, `aggregate_us_filings`, `search/get_earning_call*`, `aggregate_earning_calls` |
| ETF | `get_etfs`, `search_etfs`, `filter_etfs`, `get_etf_detail/holdings/price/dividends`, `get_etf_briefing/news/topics/global_news/global_topics`, `get_etf_matchup`(미구현) |
| 산업·매크로·시장 | `get_industries`, `get_industry_detail/reports`(프리미엄), `get_industry_companies/news/topics`, `get_korean/global_industry_briefing`, `get_korean/global_macro_briefing`, `get_market_indices`, `get_market_holidays` |
| 리스크·유튜브 (프리미엄) | `get_risk_monitoring`, `get_us_risk_monitoring`, `get_stock_risk_summary`, `get_portfolio_risk`, `get_youtube_*` |

**wrks 플랫폼 (20개)**: 드라이브(8), 워크플로우(5), `run_code`(Python 샌드박스), `render_visualization`, `read_image`, `summarize_document`, `search_web`(Perplexity), `organize_facts`, `ask_user`
**메모리 (4개)**: `search_memory`, `get_memory_context`, `aggregate_ledger`, `compute_time_diff`

## 3. 테스트 결과

| # | 질문 | 호출 | 관찰 |
|---|------|------|------|
| 1 | SK하이닉스 뉴스 중 10/1~10/21 제목에 HBM 포함 5건 | `dsrch_search_korean_articles` ×4 (순차) | `page_size=20`을 요청해도 **페이지당 10건**만 온다. **제목 필터가 없어서** 결과를 받아 직접 골라야 한다. 최신순이면 앞쪽 날짜만 와서 `order=score`, `page=2`로 우회했다. 사진기사 중복도 많다. |
| 2 | 도구 목록·스키마 원문 | 없음 | 이름과 설명만 알려주고 스키마 원문은 거부했다. |
| 3 | 삼성전자 2023~25 연결 매출·영업이익 + 10/13~21 종가 | `get_company_detail`, `get_fin_statement(consolidated=true)`, `get_company_stock_price` (병렬) | 정상. 2025 매출 333.6조, 영업이익 43.6조, 10/21 종가 223,500원. `get_company_detail`은 플랫폼 규칙에 따라 기업이 언급되면 항상 먼저 호출된다. |

추가 관찰
- **사용량**: 질문 3개(Opus 5.5, 원문 출력 포함)로 개인 사용량이 0% → **8%** 가 됐다. 원문 JSON을 답변에 다시 쓰는 비용이 크다.
- 각 도구 호출 단계를 펼치면 **"원본 데이터 보기"** 에 응답 JSON이 그대로 보인다. 답변 본문에 원문을 다시 출력할 필요가 없다.
- 관리자 설정으로 **스마트 라우팅**이 켜져 있다. 에이전트에서 Opus 5.5를 골라도 다른 모델이 답할 수 있다.

## 4. 현재 프롬프트 평가

```
나는 너가 deepsearch api를 사용한다는 것을 알고 있어.
나의 질문에 대한 답변은 다음과 같이 구성해줘.
만약 deepsearch api mcp를 사용했다면
1. 호출에 사용한 deepsearch 함수를 그대로 출력
2. deepsearch에서 돌아온 응답을 그대로 출력
3. 여러개의 api를 병렬 또는 순차로 사용했다면 일련의 절차를 설명
...
```

- **잘 되는 점**: 함수명, 파라미터, 순차/병렬 절차를 정확히 밝힌다. "무엇을 어떻게 불렀나"를 보는 목적에는 충분하다.
- **문제 1 — 응답 원문 출력(2번)**: UI의 "원본 데이터 보기"와 중복된다. 답변이 길어지고 사용량을 크게 쓴다. 게다가 길면 모델이 알아서 잘라서 "그대로"가 지켜지지도 않는다.
- **문제 2 — 데이터 조회 요령이 없다**: 10건 상한, 제목 필터 없음, `KRX:` 심볼 형식, 연결/별도 구분 같은 함정을 모델이 매번 시행착오로 배운다(테스트 1에서 4회 호출).
- **문제 3 — 결론 위치**: 형식 지시가 앞서서 정작 답(결과 표)이 호출 로그 사이에 묻힌다.

개선안은 [agent_prompt.md](agent_prompt.md)에 있다. 2026-10-22에 에이전트에 적용했다(결과는 5절).

## 5. 개선 프롬프트 적용 후 재테스트

새 대화에서 테스트 1, 3번 질문을 다시 보냈다.

| | 기존 프롬프트 | 개선 프롬프트 |
|---|---|---|
| **테스트 1** (HBM 뉴스) | 4회 호출, 일반 기사 4건 + 사진기사 1건 | **9회 호출**, 1차에서 놓친 기사 2건 추가 발견(10/10 뉴시스, 10/07 디지털데일리). 일반 기사가 4건뿐이라고 밝히고 대체 후보도 제시 |
| | 사용량: 질문 3개 합계 +8% | **+6%** (8% → 14%) |
| **테스트 3** (재무·주가) | 3개 병렬 호출, 응답 원문 JSON을 본문에 옮김 | 같은 3개 병렬 호출, 수치 동일. 원문 없이 결론 → 표 → 호출 내역 → 한계. 본문 길이 약 40% 감소 |
| | | **+3%** (14% → 17%) |

- 형식은 의도대로 바뀌었다. 결론이 맨 위에 오고, 계산값이 표시되고, 잘림 여부("7건, page_size보다 적어 잘리지 않음")와 한계(수정주가 여부 미표시 등)를 적는다.
- 뉴스는 "잘린 상태에서 없다고 단정하지 말 것" 지시 때문에 **페이지를 끝까지 넘겨** 호출 수와 사용량이 늘었다. 대신 결과가 더 정확하다. 비용을 줄이려면 질문에 "호출 3회 이내" 같은 상한을 주면 된다.
- `dsrch_get_company_stock_price`는 `symbol="005930"`(접두어 없음)으로도 동작했다.

## 6. 프로그램으로 직접 호출하는 것에 대해

조사하지 않았고 권하지 않는다.
- 채팅 채널이 WebSocket + 로그인 세션 토큰이라, 재현하려면 비공개 프로토콜을 역공학해야 한다. wrks가 바뀌면 바로 깨진다.
- KRX 계정은 예산 한도가 있는 조직 계정이다(공지: "이용 한도 초과 시 신청을 통해 상향"). 자동 대량 호출은 조직 예산을 쓰고, 이용약관 위반 소지도 있다.
- 자동화가 필요하면 다음 순서로 검토한다: (1) 웍스의 공식 기능인 **워크플로우 / 대화 예약**, (2) 이 레포의 DeepSearch API 키로 직접 호출(`newsscrap/ds_client.py`, `skills/deepsearch`).
