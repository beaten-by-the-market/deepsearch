# 5-02 지표·코드 찾기 — "이 지표 DeepSearch에 있어? 무슨 코드로 봐?"

[노트북](02_find_indicator.ipynb) · [Colab에서 열기](https://colab.research.google.com/github/beaten-by-the-market/deepsearch/blob/main/scenarios/5_data_lookup/02_find_indicator.ipynb) · CHECK 원본: `5_데이터조회/02_지표코드찾기` · 구분: **각색**

## 한 줄 요약
종목코드·지수 코드·경제지표 시리즈 ID를 찾고, 그 지표가 **지금도 갱신되는지**(마지막 날짜)와 DeepSearch에 아예 있는지를 판정합니다.

## 이렇게 물어보세요
- "삼성전자 종목코드 알려줘", "코스피 지수 코드 뭐야?"
- "원/달러 환율은 어떤 코드로 봐?"
- "한국 관련 FRED 지표 뭐 있어? 금리만"
- "베이시스 데이터 있어?", "신용융자 잔고 어디서 봐?"

## CHECK 원본과 달라진 점
| 항목 | CHECK | DeepSearch |
|---|---|---|
| 지표 검색 | 코드 카탈로그·필드 검색 | 시리즈 검색 `FindEntity("DataSeries", …)`가 **모든 검색어 0건**이라 못 씀 |
| 대안 | — | FRED 카테고리 따라가기, 한국은행 통계표 항목 조회, IMF·OECD 목록 펼치기, 자연어 질의 판정 |
| 종목·지수 코드 | 코드 카탈로그 | `GetStockSymbols`(전 종목), `GetMarketIndexSymbols`(11종) |

## 결과 예시 (2026-11-25 확인, 노트북 실행값)
| 지표 | 결과 |
|---|---|
| 삼성전자 / 코스피 | `KRX:005930` / `KRX:KOSPI` |
| 원/달러 | FRED `DEXKOUS` (11-20까지) — 한국은행 `731Y001`은 2024-04-26에서 끝남 |
| FRED 한국 카테고리(32286) | 시리즈 2,395개 중 2026년까지 갱신 729개. 금리는 콜·3개월·10년(월, 2026-10까지) |
| 신용융자 잔고·투자자예탁금 | 한국은행 `901Y056` S23E·S23A — 2024-03에서 끝남 |
| 한국 경상수지(IMF BOP) | 2021년에서 끝남 |
| 자연어 판정 | 종가·시가총액·PER·PBR·배당수익률·EPS·BPS ✅ / 외국인보유비율·공매도·신용잔고·베이시스·VKOSPI·투자자예탁금 ❌ |

## 결과 읽는 법
- 시리즈를 찾으면 **마지막 관측일을 먼저** 보세요. 한국은행·IMF BOP처럼 오류 없이 오래된 값만 주는 경우가 있습니다.
- 자연어 질의에서 `ceo`·`business_rid` 같은 컬럼(기업 개요 표)이 나오면 그 지표는 없는 것입니다.

## 주의·한계
- FRED 카테고리 탐색은 출발 시리즈를 하나 알아야 합니다. 노트북에 자주 쓰는 출발점(`DEXKOUS`, `IRLTLT01KRM156N`)을 넣어 두었습니다.
- 딥서치 자체 지표(`DS:`)는 ID를 알아야 조회되고, 검색 수단이 없습니다.
- 종목 이름 검색에는 그 종목을 담은 ETF도 함께 걸립니다(`company_type_l1`=8).

## 쓰는 DeepSearch 함수
`GetStockSymbols`, `GetMarketIndexSymbols`, `GetFredCategoryOfDataSeries`, `GetFredDataSeriesListUnderCategory`, `QueryFredSeriesInfo`, `QueryBankOfKoreaSeriesInfo`, `GetImfIndicatorListOfSameCountry`, `GetImfSeriesValues`, compute 자연어 질의
