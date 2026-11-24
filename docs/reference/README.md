# docs/reference — DeepSearch API 레퍼런스

DeepSearch 공식 가이드(https://help.deepsearch.com/dp)를 마크다운으로 옮긴 원문과, 그 요약입니다.

**처음 보는 사람·에이전트:** [DEEPSEARCH_API_MASTER.md](DEEPSEARCH_API_MASTER.md)부터 읽으세요. 함수별 호출 형식과, 이 레포의 API 키로 실제 호출해 본 결과(✅/⚠️/❌)가 한 표에 있습니다. 함수의 파라미터 표나 결과 예시가 필요할 때만 아래 원문 파일을 grep으로 찾으세요. 원문 파일은 크니 통째로 읽지 마세요.

## 파일

| 파일 | 내용 | 원문 위치 |
|---|---|---|
| [DEEPSEARCH_API_MASTER.md](DEEPSEARCH_API_MASTER.md) | 요약 + 전체 함수 목록과 호출 결과 (직접 관리) | — |
| [1_기본적인_데이터_조회방법.md](1_기본적인_데이터_조회방법.md) | API 사용 방법, 데이터 종류(시장·개요·문서·재무), 분기재무제표 쿼리, 데이터 FAQ | `api/master`, `api/howto`, `api/data/*`, `api/query` |
| [2_쿼리를_통한_데이터_조회.md](2_쿼리를_통한_데이터_조회.md) | 쿼리 문법, 기업검색 예약어, 연산 함수, FAQ·에러 | `api/inquiry/*` |
| [3_API함수를_통한_데이터_조회_국내기업.md](3_API함수를_통한_데이터_조회_국내기업.md) | 기업 검색·정보, 재무제표, 공시(GetDart*), 컨센서스, 이슈기업, 주가·지수 | `api/func/company/*` |
| [3_API함수를_통한_데이터_조회_채권.md](3_API함수를_통한_데이터_조회_채권.md) | 채권 함수 (전부 현재 구독으로 사용 불가) | `api/func/company/bond/*` |
| [3_API함수를_통한_데이터_조회_산업검색.md](3_API함수를_통한_데이터_조회_산업검색.md) | 산업 정보, 기업 주제(태그), 기업집단 | `api/func/industry/*` |
| [3_API함수를_통한_데이터_조회_인물검색.md](3_API함수를_통한_데이터_조회_인물검색.md) | 임원·인물, 주식 부자 | `api/func/people/*` |
| [3_API함수를_통한_데이터_조회_문서검색.md](3_API함수를_통한_데이터_조회_문서검색.md) | DocumentSearch·Trends·Aggregation, 감성, 토픽, 유사어 | `api/func/document/*` |
| [3_API함수를_통한_데이터_조회_이벤트.md](3_API함수를_통한_데이터_조회_이벤트.md) | 포트폴리오 수익률, 주식·채권 이벤트 분석 | `api/func/event/*` |
| [3_API함수를_통한_데이터_조회_경제지표.md](3_API함수를_통한_데이터_조회_경제지표.md) | 한국은행·FRED·IMF·OECD·World Bank·통계청·딥서치 자체 지표 | `api/func/economy/*` |
| [4_토픽인사이트.md](4_토픽인사이트.md) | 토픽 인사이트·질문·답변 REST API | `api/topic/*` |
| [5_결과레이아웃.md](5_결과레이아웃.md) | compute 응답의 pod class별 구조 | `api/result_layout/*` |
| [DeepSearch_재무계정체계_220706.xlsx](DeepSearch_재무계정체계_220706.xlsx) | 재무 계정 체계표 (2022-07-06) | — |
| [sync_from_gitbook.py](sync_from_gitbook.py) | 원문 파일을 다시 만드는 스크립트 | — |

원문 위치는 `https://help.deepsearch.com/dp/` 뒤의 경로입니다. 원문 파일 안의 각 페이지 앞에도 `<!-- source: URL -->`가 붙어 있습니다.

## 넣지 않은 것

현재 구독 키로 호출해 보고(2026-11-25) 쓸 수 없는 API는 원문 파일에 넣지 않았습니다.

| 대상 | 결과 |
|---|---|
| DeepSearch v2 REST (https://api-v2.deepsearch.com/v2/manual/redoc) | 401 `잘못된 API Key 입니다` |
| 가이드 "해외기업" (`api.deepsearch.com/v2/companies/...`) | 401 `잘못된 API Key 입니다` |
| 가이드 "챗딥서치" (`api.deepsearch.com/note/v1/...`) | 401 `Session token is not provided` |
| 가이드 첫 화면, 웹 서비스 FAQ·공지 | API와 무관 (데이터 FAQ만 1번 파일에 포함) |

compute 함수 중 호출이 안 되는 것(채권·통계청 등)은 원문을 남기고, 해당 페이지에 `[레포 검증 ...]` 메모를 붙였습니다. 전체 목록은 MASTER 17절에 있습니다.

## 원문 다시 받기

```bash
python docs/reference/sync_from_gitbook.py           # 웹에서 받아 원문 파일을 다시 생성
python docs/reference/sync_from_gitbook.py --check   # 파일은 그대로 두고, 새로 생기거나 바뀐 페이지만 출력
```

- 페이지 목록과 순서는 GitBook의 `llms.txt`, 본문은 각 페이지 URL 뒤에 `.md`를 붙여 받습니다.
- 레포에서 덧붙인 메모는 `<!-- repo-memo:start -->` ~ `<!-- repo-memo:end -->` 안에 쓰세요. 다시 생성해도 같은 페이지 아래에 남습니다. 마커 밖에서 고친 내용은 덮어써집니다.
- 매핑되지 않은 새 페이지가 생기면 스크립트가 알려줍니다. `FILES`나 `EXCLUDE`에 추가하세요.
- 새 함수가 생기면 이 레포 키로 호출해 보고, MASTER 17절 표와 페이지 메모를 갱신하세요.

## 변경 이력

- 2026-11-25: 가이드 전체(226페이지)를 다시 받아 재구성했습니다. 205페이지를 반영하고 21페이지는 제외했습니다.
  - 새로 들어간 내용: 공시(GetDart*) 12개, 채권 18개, 이벤트 9개, 경제지표 30여 개, 기업 주제 3개, GetEntitySummary, GetCompanyProductsSales, 감사의견, 토픽 인사이트, 결과 레이아웃 2종
  - 바로잡은 내용: 호출 주소(`app-api.deepsearch.com` 추가), 분기재무제표 표, 기존 파일에서 `FindEntity`로 잘못 붙어 있던 `FindEntityByName` 제목
  - 원문 파일 1·2번에 있던 중복 페이지도 정리했습니다.
