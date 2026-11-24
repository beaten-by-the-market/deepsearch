---
name: deepsearch
description: "DeepSearch API(api.deepsearch.com)로 한국 기업 데이터를 조회·분석한다. 뉴스·증권사 리포트·공시/IR·특허 검색과 트렌드·감성, 상장사·외감 비상장사 재무제표(GetFinancialStatements), 주가·PER·PBR·시가총액, 조건 스크리닝, 일일 시황 리포트, 여러 데이터를 엮은 멀티스텝 분석(뉴스+주가, 공시 vs 뉴스 등)에 사용한다. 사용자가 DeepSearch/딥서치를 언급하거나, DeepSearch API 키가 있는 프로젝트에서 KRX 상장사 문서·재무·주가 데이터를 요청하면 적용한다."
---

# DeepSearch 통합 스킬

문서검색, 기업/재무 데이터, 스크리닝/분석을 하나의 스킬로 처리합니다. **여러 데이터 소스를 연결하는 멀티스텝 분석에 특화**되어 있습니다.

## 시작하기

- **경로:** `${CLAUDE_SKILL_DIR}`는 이 SKILL.md가 있는 폴더입니다. 스킬로 설치하지 않고 레포를 클론해 직접 읽는 경우 `skills/deepsearch`로 바꿔 쓰세요.
- **설치:** `pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt` (requests, PyMuPDF)
- **API 키:** 스크립트가 환경변수 `DEEPSEARCH_API_KEY`/`API_KEY` → 현재 폴더와 상위 폴더의 `.env` → 스킬 폴더 상위의 `.env` 순서로 직접 찾습니다. raw `id:secret`도 됩니다.
  - **키 값을 화면에 내지 마세요.** `.env`를 `cat`/`echo`하거나 키를 명령 인자로 넣으면 대화 기록에 남습니다.
  - 키를 못 찾으면 스크립트가 안내 메시지를 냅니다. 그때 사용자에게 **한 번만** 요청해 프로젝트 루트 `.env`에 `API_KEY=<키>`로 저장하세요(`.gitignore`에 `.env`가 있는지 확인).
- **자료:** `references/`(호출식·검증 사례·시황 템플릿), 레포 `research/`(데이터 정의 검증 노트), 레포 `docs/reference/DEEPSEARCH_API_MASTER.md`(전체 함수와 이 구독으로의 호출 결과). `docs/reference/`의 원문 파일은 크니 grep으로만 찾아보세요.

### 실행

```bash
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "쿼리"                                   # 모든 compute 쿼리
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "쿼리" --out result.json                   # 전체 결과를 파일로
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "DocumentSearch(...)" --max-pages 3        # 기간 구간마다 3페이지
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "GetFinancialStatements(...)" --grep '^(수익|영업이익\(손실\))$'
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "/v1/topic-insight/insight?..."            # "/"로 시작하면 REST GET
```

| 스크립트 | 용도 | API 호출 |
|---|---|---|
| `query_api.py` | 모든 쿼리. DocumentSearch 1년 자동 분할, 에러 원인·힌트 표시 | 1~수 회 |
| `market_overview.py YYYY-MM-DD` | 일일 시황 7개 섹션 (규칙 2) | 8회, 약 5초 |
| `market_top_movers.py <kospi\|kosdaq\|all> N YYYY-MM-DD` | 시가총액 상위 N개 중 등락률 상·하위 | 2회 |
| `turnaround_screener.py <loss\|profit> [매출_억] [--years Y1 Y2]` | 적자·흑자 전환 기업 (최근 결산연도 자동) | 2~수 회 |
| `read_document.py <URL \| DocumentSearch(...)> [--doc N]` | 보고서·IR PDF, 뉴스 본문 | 1~2회 |

- **결과 형식:** DocumentSearch → `total_matches`, `windows`(구간별 건수), `docs[]`(title, publisher, created_at, content 300자, content_url, securities, polarity, esg). DataFrame(재무·주가·스크리닝) → `columns`, `row_count`, `rows[]`(행 dict).
- **큰 결과:** JSON이 2만 자를 넘으면 임시 폴더에 저장하고 `saved_to` 경로와 미리보기만 출력합니다. 그 파일을 Python으로 읽어 필요한 부분만 쓰고, 통째로 다시 출력하지 마세요.

## ⚠️ 핵심 규칙

1. **재무제표는 `GetFinancialStatements`로만** 조회합니다. `삼성전자 매출액 2020-2024` 같은 자연어 재무 쿼리는 금지입니다(KeyError). 계정명은 `매출액`이 아니라 `수익`입니다. → [Section B-1](#b-1-재무제표)
2. **시황 요청은 `market_overview.py` 하나로** 처리합니다. DocumentSearch·GetMarketIndexes 등을 따로 불러 조합하지 마세요. → [Section C-3](#c-3-전용-스크립트)
3. **주가를 보여주면 수정주가 안내를 데이터보다 먼저** 넣습니다. 시황 리포트도 같습니다. 스크립트 결과의 `price_basis_notice`를 그대로 써도 됩니다.
   ```
   > ℹ️ 주가 기준: 시가·고가·저가·종가는 수정주가입니다(액면분할·무상증자·유상증자를 과거 가격에 소급 반영, 배당은 미반영). DeepSearch는 원주가를 따로 제공하지 않습니다. 거래량·거래대금·시가총액은 당일 실제 값입니다.
   ```
   상황에 따라 한 줄을 덧붙이세요.
   - 기간에 분할·증자가 끼어 있으면: "○월 ○일 액면분할 전후로 거래량은 직접 비교할 수 없습니다."
   - 기간 수익률이면: "배당을 뺀 가격수익률입니다."
   - 원주가를 원하면: `market_cap ÷ shares_outstanding`으로 계산했다고 밝힙니다.
   → [Section B-2](#b-2-주가시장-데이터)
4. **과거 재무값·BPS/EPS로 백테스트하거나 시점을 따지면 한계를 먼저** 밝힙니다. 근거: 레포 `research/restatement/`, `research/pbr_bps/` (검증 2026-11-20)
   - 과거 재무제표 값은 원래 공시값과 재작성값이 섞여 있습니다. 재작성된 회사·연도의 약 3/4은 재작성값, 1/4은 원래값이고, 구분 필드나 옵션은 없습니다. IFRS17 보험사 2022년은 대부분 재작성 전 값입니다. 그 시점 값이 꼭 필요하면 OpenDART에서 받으세요.
   - 시장데이터 BPS·EPS(따라서 PBR·PER)는 FY N 값이 N+1년 첫 거래일부터 붙어 있습니다. 결산 공시 전이라 look-ahead가 생기니, 사업보고서 공시 시점(보통 3월 말) 이후로 밀어 쓰세요.
   - BPS 정의는 하나뿐입니다: 연결 지배기업소유주지분 ÷ (보통주+우선주 − 자기주식), 직전 연말. `별도`·`분기`를 붙여도 무시됩니다.
5. **여러 회사·종목은 한 번에** 조회합니다. `GetFinancialStatements([A, B, ...])`, `GetStockPrices([...])`는 목록을 받고, `GetStockPrices`는 종목을 생략하면 전 종목이 옵니다. 회사마다 반복 호출하지 마세요. → [Section C-4](#c-4-대량-조회)

## 쿼리 라우팅

| 요청 유형 | 판단 기준 | 처리 |
|---|---|---|
| **시황분석** | 시장 현황, 시황, 마켓 리포트, 장 마감 정리, 오늘 장 | `market_overview.py` (규칙 2) |
| **문서 검색** | 뉴스, 리포트, 공시, 트렌드, 감성 | Section A |
| **재무제표** | 매출, 영업이익, 자산, 부채, 재무제표 | Section B-1 (`GetFinancialStatements`) |
| **주가/시장** | 종가, PER, PBR, 시가총액, 거래량 | Section B-2 (규칙 3 안내) |
| **기업정보** | 배당, 주주, 임원, 기업개요, 공시 표 | Section B-3 |
| **스크리닝/분석** | 조건 필터, Top/Bottom, 시총 순위, 전환 기업 | Section C |
| **멀티스텝** | 위 유형 2개 이상 결합 | Section D |
| 그 밖의 함수 | 경제지표, 태그, 이벤트, 토픽 인사이트 등 | [예시가 없는 기능](#이-스킬에-예시가-없는-deepsearch-기능) |

## 데이터 출처

DeepSearch는 아래 기관의 공식 데이터를 수집·가공해 제공합니다. **결과에는 출처를 반드시 표기하세요**([결과 포맷팅](#결과-포맷팅)).

| 데이터 유형 | 원천 기관 | 비고 |
|---|---|---|
| 재무제표·기업정보 | **NICE평가정보** | 외감기업 재무, 기업개요, 산업분류. 심볼 `NICE:` 접두어 |
| 주가·시장데이터 | **KRX 한국거래소** / **코스콤** | 종가, 시가총액, 거래량, PER, PBR 등 일별 |
| 공시·IR | **금융감독원 DART** | 사업·분기보고서, 주요사항보고서 등 |
| 뉴스 | **각 언론사** | 국내 주요 언론사 기사 |
| 증권사 리포트 | **각 증권사** | 기업·산업·시장전략 리포트 |
| 특허 | **특허정보원 KIPRIS** | 국내 특허·실용신안 |

---

## Section A: 문서 검색

### 쿼리 형식
```
DocumentSearch(["카테고리"],["섹션"],"쿼리",count=100,page=1,date_from=YYYYMMDD,date_to=YYYYMMDD)
DocumentTrends(["카테고리"],["섹션"],"쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
DocumentAggregation(["카테고리"],["섹션"],"쿼리","groupby필드:N",date_from=YYYYMMDD,date_to=YYYYMMDD)
GetSentimentScore("쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
SimilarKeywords("키워드",max_count=10)
```
- 카테고리/섹션: 뉴스 `["news"]`(economy, tech, society, politics, culture, world, entertainment, opinion), 리서치 `["research"]`(market, strategy, company, industry, economy, bond), 공시/IR `["company"]`(ir, disclosure), 특허 `["patent"]`. 미지정이면 `["news"]`, 섹션 `[]`.
- 필드: 기업 `securities.name:기업명`, 종목코드 `securities.symbol:KRX:005930`, 시장 `securities.market:(KOSPI or KOSDAQ)`, 감성 `polarity.name:긍정`, ESG `esg.category.name:환경`, 제목 `title:`, 본문 `content:`, 언론사 `publisher.raw:('매일경제')`. Boolean `and`, `or`, `!`, `()`.
- interval: `1y`, `1M`, `1w`, `1d`, `1h`, `1m`
- 집계 groupby 예: `securities.name:20`(언급 상위 종목), `polarity.name:5`(긍정·부정·중립 건수)
- 시간 범위: `created_at:[\"2025-02-28T09:00:00\" to \"2025-02-28T12:00:00\"]`를 쿼리에 넣습니다(date_from/to는 날짜 단위만).

### ⚠️ 실전 함정 (검증됨)
1. **기간 1년 한도:** Basic 인증으로는 DocumentSearch 기간이 1년을 넘으면 HTTP 413입니다(`RequestEntityTooLarge: Not allowed to search more than 1 year if not logged in`). fields나 OR 괄호 문제가 아닙니다. **`query_api.py`가 1년 이하 구간으로 자동 분할**하고 `content_url`로 중복 제거해 최신순으로 합칩니다. DocumentTrends는 2년도 정상입니다.
2. **에러 원인은 `data.exceptions[]`에 있습니다**(HTTP 200이어도 올 수 있음). `query_api.py`는 이를 `error`·`hint`로 보여줍니다. 0건이면 이것부터 보세요.
3. **페이지:** 기본은 한 페이지입니다. `count`는 최대 100이고, 더 필요하면 `--max-pages N`을 쓰세요.
4. 직접 호출할 때만 해당: 문서 리스트 키는 `docs`(NOT `documents`)입니다. 쿼리는 POST `{"input": ...}`로 보내거나 `quote(query, safe="")`로 인코딩하세요(한글·괄호·`&`).

출처: 레포 `notes/HANDOFF_DocumentSearch_news_20260610.md`

### 이슈 카테고리별 검색 키워드

| 이슈 | 키워드 패턴 |
|---|---|
| 계약/수주 | `(수주 and 체결) or (수주 and 공급) or (계약 and 체결) or (계약 and 공급)` |
| 인수/투자 | `인수 or 합병 or 분할 or 영업양도 or 영업양수 or 출자 or 투자` |
| 실적 | `(매출 and 발표) or (실적 and 공시) or (이익 and 달성) or (배당 and 결정)` |
| 증자/감자 | `증자 or 감자 or 주식교환 or 주식이전 or 우회상장` |
| 회계/감사 | `상장폐지 or 관리종목 or 자본잠식 or (비적정 and 감사) or (의견거절 and 감사) or 분식` |
| 소송/부도 | `소송 or 횡령 or 배임 or 부도 or 파산 or 회생 or (기소 and 대표이사)` |

예: 코스피 상장사 인수/투자 뉴스 → `securities.market:KOSPI and (인수 or 합병 or 출자 or 투자)`

### 종목별 공시/IR/애널리스트 보고서
```
DocumentSearch(["company"],["disclosure"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)   # 공시
DocumentSearch(["company"],["ir"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)           # IR
DocumentSearch(["research"],["company"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)     # 애널리스트
```

### KRX 문서검색 패턴
- 조회공시 후보 → `title:(인수 or 합병 or 매각) and securities.market:(KOSPI or KOSDAQ)`
- 부정 뉴스 → `securities.market:KOSPI and polarity.name:부정`
- ESG 이슈 → `esg.category.name:지배구조 and esg.polarity.name:부정`
- 불공정거래 → `title:(시세조종 or 불공정거래 or 내부자거래)`
- 뉴스 언급 상위 → `DocumentAggregation(..., "securities.name:20")`

더 많은 패턴: [references/krx_monitoring_guide.md](references/krx_monitoring_guide.md)

### 문서 본문 읽기

검색 결과의 `content`는 100~500자 요약입니다. 사용자가 특정 문서의 상세 내용을 원하면 `read_document.py`로 원문을 읽으세요.
```bash
python ${CLAUDE_SKILL_DIR}/scripts/read_document.py "https://ddi-cdn.deepsearch.com/.../report.pdf"
python ${CLAUDE_SKILL_DIR}/scripts/read_document.py 'DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=5,page=1)' --doc 1
```

| 문서 | 형식 | 추출 결과 |
|---|---|---|
| 애널리스트 보고서 · IR | PDF | 앞 20페이지 전체 텍스트 (수천~수만 자, 표 텍스트 포함) |
| 뉴스 | HTML | 본문 앞 10,000자 (메뉴 등 노이즈 포함 가능) |
| 공시 (DART) | HTML | 프레임 구조라 본문이 거의 안 나옴 → DART 링크를 안내 |

예: "삼성전자 최근 보고서의 목표주가 근거" → 보고서 PDF 본문을 읽고 답합니다.

---

## Section B: 기업 & 재무/시장 데이터

### B-1. 재무제표

```
GetAvailableFinancialStatements(KRX:005930)        # 1단계: 회계기준(IFRS/GAAP)·연결/별도 확인
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(삼성전자, consolidated=False)            # 별도
GetFinancialStatements(삼성전자, report_ids="Income")          # BalanceSheet / Income / CashFlow / Ratio
GetFinancialStatements(삼성전자, is_annual=False)              # 분기 포함 (is_accumulated=True면 누적)
GetFinancialStatements([KRX:005930, KRX:000660, KRX:035420], report_ids="Income", date_from=2023-01-01, date_to=2025-12-31)   # 여러 회사 한 번에
```
- 기업명은 따옴표 없이 씁니다. 결과는 행 단위(`date, symbol, entity_name, report_id, account_id, name_ko, value`)이고 회사·연도당 수백 행입니다. **`--grep`으로 필요한 계정만 남기세요.**
- **계정명(`name_ko`):** 부분일치(`--grep 매출`)는 매출원가·매출채권까지 섞이니 정확히 거세요.

| 찾는 항목 | `name_ko` | report_id / account_id |
|---|---|---|
| 매출액 | `수익` | 12 / 1000 |
| 매출원가 · 매출총이익 | `매출원가` · `매출총이익(손실)` | 12 / 2000 · 3000 |
| 영업이익 | `영업이익(손실)` | 12 / 5000 |
| 당기순이익 | `총당기순이익` (지배주주분 `당기순이익지배기업지분`) | 12 / 8200 (9061) |
| 자산·부채·자본총계 | `자산총계` · `부채총계` · `자본총계` | 11 / 5000 · 8000 · 8900 |

report_id 11 = 재무상태표, 12 = 손익계산서, 19 = 재무비율. 삼성전자·삼성중공업 2024년으로 확인(2026-11-25). 세부 계정(미청구공사, 재고자산 등)도 같은 결과에서 `name_ko`로 찾습니다.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py 'GetFinancialStatements(삼성전자, consolidated=True, date_from=2020-01-01, date_to=2024-12-31)' --grep '^(수익|영업이익\(손실\)|총당기순이익)$'
```
- **❌ 금지:** `삼성전자 매출액 2020-2024`, `기업명 연결 매출액 2020-2024`, `기업명 자산 부채 자본 2020-2024` 같은 자연어 재무 쿼리 (KeyError)
- 결과를 보여줄 때는 **회계기준과 연결/별도를 명시**하세요(예: "K-IFRS 연결 기준").
- 과거 연도 값의 한계는 규칙 4.

**비상장사(외감):** 상장사와 같은 방법으로 조회합니다.

| 항목 | 상장사 | 비상장사 (외감) |
|---|---|---|
| 연결 재무제표 | 대부분 있음 | **대부분 없음** (별도만) → `consolidated=False` |
| 데이터 시작 | 상장일 기준 | 외감 시작 (보통 최근 5~9년). 모르면 넓은 범위로 먼저 조회 |
| 분기 데이터 | 최근 ~7분기 | 매우 제한적 (1~2건) |
| `GetCompanySummary` | 상세 | 거의 빈 결과 |

### B-2. 주가/시장 데이터

```
삼성전자 종가 2024-06-01-2024-06-30          # 자연어: 일별 종가 (2020-01-02 이후만)
삼성전자 PER / 삼성전자 PBR                   # 현재 값
삼성전자 시가총액 2024-01-01-2024-12-31
GetStockPrices(KRX:005930, columns=["open","high","low","close","volume","value","shares_outstanding","market_cap"], date_from=2018-04-25, date_to=2018-05-08)
GetStockPrices([KRX:005930, KRX:000660], columns=["close","change_rate"], date_from=2024-01-02, date_to=2024-12-30)   # 여러 종목
GetStockPrices(columns=["close","change_rate","market_cap"], date_from=2025-11-14, date_to=2025-11-21)               # 종목 생략 = 전 종목, 기간의 마지막 거래일 하루치
GetMarketIndexes(date_from=2025-11-17, date_to=2025-11-21)                                                            # 지수 11종, 거래일마다
```
- 시장데이터(종가·시가·고가·저가·시가총액·거래량·PER·PBR·EPS·BPS·DPS)는 자연어로 됩니다. 재무제표는 B-1을 보세요.
- `GetStockPrices` 컬럼: `open, high, low, close, volume, value, change, change_rate, shares_outstanding, market_cap, trading_halted`

**⚠️ 주가 데이터 함정 (검증됨, 2026-11-25)** — 근거: 레포 `research/price_adjustment/README.md`
1. **수정주가만 나옵니다.** 파라미터는 `entities, columns, date_from, date_to`뿐이고, `adjusted=`, `adj_close` 같은 이름은 400입니다. 이런 옵션을 찾느라 호출을 반복하지 마세요.
2. **가격만 수정되고 수량은 수정되지 않습니다.** open/high/low/close는 분할·무상증자·유상증자에 맞춰 소급 수정됩니다(배당 미반영). volume·value·shares_outstanding·market_cap은 당일 실제 값입니다. 그래서 수정 이벤트 이전에는 `close × shares_outstanding` ≠ 시가총액, `close × volume` ≠ 거래대금입니다(`market_cap`·`value`를 그대로 쓰세요). 분할 전후 거래량에는 계단이 생깁니다(삼성전자 50배).
3. **원주가:** `market_cap ÷ shares_outstanding`. 시가·고가·저가는 그날의 수정계수(`원주가 ÷ close`)를 곱합니다. 명목 분할비율을 곱하면 틀립니다(NAVER 5:1 분할의 계수는 4.99291).
4. **수정 이벤트 찾기:** 날마다 `market_cap ÷ shares_outstanding ÷ close`를 계산해 값이 바뀌는 날을 봅니다.
5. **자연어 주가 쿼리는 2020-01-02 이후만 나옵니다(오류 없이).** 그 이전 범위는 오늘 값 1행이 오고, 걸치는 범위는 잘립니다. 첫 행 날짜를 확인하고, 2020년 이전은 `GetStockPrices`를 쓰세요.
6. **매매정지일에도 행이 있습니다**(거래량 0, 가격 반복, `trading_halted`). 일별 수익률·변동성 계산 때 주의하세요.
7. **과거 값이 나중에 바뀔 수 있습니다.** 새 분할·증자가 생기면 그 이전 가격이 다시 계산되니, 저장할 때 조회일을 남기세요.
8. **`change_rate` 단위가 다릅니다.** 종목(`GetStockPrices`)은 비율(-0.0876 = -8.76%), 지수(`GetMarketIndexes`)는 퍼센트(1.94 = 1.94%)입니다.

### B-3. 기업정보·공시 함수
```
FindEntity("Financial","삼성*")                         # 기업 검색 (이름·사업자번호·주소 등)
GetStockSymbols(KRX:005930)                            # 종목 기본정보 (생략하면 전 종목: market, company_type_l1 등)
GetCompanySummary(삼성전자)
GetCompanyDividends(삼성전자, date_from=20200101, date_to=20241231)
GetCompanyShareholders(삼성전자) / GetCompanyExecutives(삼성전자)
GetDartDividends(KRX:005930, date_from=2020-01-01, date_to=2024-12-31)            # 정기보고서 배당 표
GetDartMajorityShareholders(KRX:005930, date_from=2024-01-01, date_to=2024-12-31)  # 정기보고서 최대주주
GetCompanyProductsSales(KRX:005930)                                               # 제품별 매출
SearchTargetPrices("005930", date_from=20240101, date_to=20241231)                # 목표주가 (opinion_code 1~2 부정, 3 중립, 4~5 긍정)
FindConglomerateByName("삼성") / GetConglomerateMembers("삼성")
FindPeopleByName("이재용")
```
기업 검색 예약어: `"반도체" 관련 기업`, `"건강기능식품" 산업 기업`, `"웹툰" 사업 기업`, `"서울 마포구" 주소 기업`, `"국민연금" 주주 기업`, `상장 기업`, `코스닥 상장 기업`

---

## Section C: 스크리닝 & 분석

### C-1. 조건 스크리닝
```
매출 > 1000000000000                                 → 매출 1조 이상
영업이익 / 매출 > 0.15                                → 영업이익률 15% 이상
2023 매출 > 2022 매출 * 1.5                          → 전년대비 50% 성장
설립일 > 2020-01-01                                  → 2020년 이후 설립
코스닥 상장 기업 and 매출액 > 100000000000            → 코스닥 매출 1000억+
상장 기업 and 2024 매출 < 2023 매출 * 0.7            → 매출 30%+ 급감
영업이익 < 0 and 매출 > 500000000000                 → 영업적자 대형
자본 < 0 and 매출 > 10000000000                      → 자본잠식
부채 / 자본 > 5 and 매출 > 100000000000              → 고부채비율
("반도체" 관련 기업) and (매출액 영업이익)              → 테마 + 재무
(매출 영업이익) in ("건강기능식품" 산업 기업)
```
- 시장 필터는 **한글**로 씁니다: `코스닥 상장 기업`, `코스피 상장 기업` (KOSDAQ/KOSPI 영문은 안 됨).
- 스크리닝 결과(기업 목록)는 자연어 조건이 맞지만, 개별 회사의 재무 수치를 보여줄 때는 B-1으로 다시 받으세요.

### C-2. 분석 함수와 제한
```
Top(매출액, 10)   Bottom(영업이익, 10)   Max(삼성전자 매출액 2015-2024)   Mean(삼성전자 종가 2024-01-01-2024-12-31)
```

| 안 되는 것 | 대안 |
|---|---|
| `Top(시가총액, N)` (시장데이터는 Top/Bottom 불가) | `market_top_movers.py`, 또는 전 종목 `GetStockPrices` 후 정렬 |
| `코스닥 상장 기업 and Top(매출액, N)` | `코스닥 상장 기업 and 매출 > X` |
| `2024 영업이익 < 0 and 2023 영업이익 > 0` (연도 비교) | `turnaround_screener.py` |
| `삼성전자 SK하이닉스 종가 날짜` (자연어 복수 종목) | `GetStockPrices([KRX:005930, KRX:000660], ...)` |
| 영문 시장명 필터 | 한글 `코스닥`/`코스피` |

### C-3. 전용 스크립트

**일일 시황 (규칙 2):** "오늘 시장 어때?", "2월 27일 시황", "장 마감 정리", "마켓 리포트" 등
```bash
python ${CLAUDE_SKILL_DIR}/scripts/market_overview.py YYYY-MM-DD
```

| 섹션 | 내용 | 소스 |
|---|---|---|
| market_indices | KOSPI·KOSDAQ·KOSPI200 시고저종·등락률(%) + 나머지 지수 | `GetMarketIndexes` |
| size_analysis | 코스피·코스닥 대/중/소형주 등락, 강세·약세 요약 | 같은 호출 |
| top_movers | KOSPI·KOSDAQ 시가총액 상위 30종목(우선주 제외) 중 상승·하락 5 | `GetStockSymbols` + `GetStockPrices` |
| most_mentioned | 경제뉴스 언급 상위 상장사 20 | `DocumentAggregation` |
| key_headlines | 경제뉴스 상위 10건 (제목·감성·관련종목) | `DocumentSearch` |
| trending_topics | 토픽 10개 (오늘은 실시간, 과거는 과거 토픽) | `SearchTrendingTopics` / `SearchHistoricalTopics` |
| market_sentiment | 긍정·부정·중립 비율과 판정 | `DocumentAggregation`(polarity) |

- 휴장일이면 시장 섹션은 직전 거래일(`trading_date`) 기준이고, 뉴스 섹션은 그 날짜 그대로입니다.
- **출력:** [references/market_overview_template.md](references/market_overview_template.md) 형식으로 바꿉니다(종합해석 → 지수 → 규모별 → 시총 등락 → 업종 → 뉴스 언급 → 주요 뉴스 → 토픽 → 감성). 맨 앞에 규칙 3 안내를 넣습니다. 실패한 섹션은 "데이터 조회 실패"로 표시하고 나머지는 그대로 보여주세요.

**시가총액 상위 등락:** "코스닥 시총 상위 150개 중 가장 많이 하락한 종목" 등
```bash
python ${CLAUDE_SKILL_DIR}/scripts/market_top_movers.py kosdaq 150 2025-02-27      # kospi / kosdaq / all, --include-preferred
```

**적자·흑자 전환:** 최근 결산연도와 전년의 영업이익 부호가 바뀐 상장사
```bash
python ${CLAUDE_SKILL_DIR}/scripts/turnaround_screener.py loss 5000              # 적자전환, 매출 5000억+
python ${CLAUDE_SKILL_DIR}/scripts/turnaround_screener.py profit 1000 --years 2023 2024
```
스크리닝으로 후보를 좁히고 → `GetFinancialStatements`를 50개사씩 묶어 영업이익을 받아(연결, 없으면 별도) → 부호 전환을 거릅니다.

### C-4. 대량 조회

여러 회사 데이터는 **목록으로 한 번에** 받으세요(규칙 5).
- 재무: `GetFinancialStatements([심볼 50개 정도], report_ids="Income", ...)` — 3개사 3년 손익이 약 900행·2초입니다. 수백 개사면 50개씩 나눠 호출하세요.
- 주가: `GetStockPrices([...])`, 전 종목이면 종목을 생략합니다(4,300여 종목·3초). 일반법인만 남기려면 `GetStockSymbols()`의 `company_type_l1 == "1"`로 거르세요(ETF·ETN은 8). 우선주는 종목코드 끝자리가 0이 아닙니다.
- **전체 상장사(수천 개사) 재무처럼 호출이 수십 회를 넘으면** 예상 호출 수와 시간을 먼저 알리고 진행 여부를 물으세요. 업종(`"건설" 산업 기업`)이나 조건(`매출 > X`)으로 대상을 줄이는 방법도 함께 제안하세요.

---

## Section D: 멀티스텝 분석

하나의 질문에 여러 데이터를 결합하는 패턴입니다. 단계별로 `query_api.py`를 순차 호출하세요. 상세 사례: [references/verified_examples.md](references/verified_examples.md)

**패턴 1: 뉴스 + 주가 (주가급변 원인분석)**
```
[1] DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=5,page=1,date_from=20240601,date_to=20240630)  → 이벤트 날짜
[2] 삼성전자 종가 거래량 2024-06-01-2024-06-30                                                                              → 전후 주가·거래량
[3] 뉴스 전 거래량 급증 → 내부자거래 의심 / 부정 뉴스에도 상승 → 추가 조사 / 뉴스 후 급락 → 정상 반응
    ※ 분할·증자 직후 거래량 급증은 미수정 거래량 때문일 수 있음 (B-2 함정 2)
```

**패턴 2: 스크리닝 + 밸류에이션 (가치투자)** — 방법론: [references/value_investing.md](references/value_investing.md)
```
[1] 매출 > 1000000000000 and 영업이익 / 매출 > 0.1 and 당기순이익 > 0     → 우량 기업 목록
[2] SK하이닉스 PER / SK하이닉스 PBR                                       → PER < 15, PBR < 1.5, PER × PBR < 22.5
[3] 조건 충족 기업만 추천. 과거 시점 PER·PBR이면 규칙 4 look-ahead 안내
```

**패턴 3: 스크리닝 + 주가 (포트폴리오 수익률)**
```
[1] 매출 > 1000000000000 and 영업이익 / 매출 > 0.15                       → 기업·종목코드
[2] GetStockPrices([KRX:000660, KRX:003230, ...], columns=["close"], date_from=2024-01-02, date_to=2024-12-30)   → 한 번에
[3] (연말 종가 − 연초 종가) / 연초 종가 → 개별·평균 수익률
    종가는 수정주가라 분할·증자가 있어도 수익률은 맞음. 배당 제외 가격수익률임을 명시 (규칙 3)
```

**패턴 4: 감성 + 주가 (이상거래 감지)**
```
[1] GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)
[2] 삼성전자 종가 거래량 2025-02-14-2025-02-28
[3] 감성 급락 + 주가 상승 → 이상거래 의심 / 감성 급등 + 주가 하락 → 추가 조사
```

**패턴 5: 뉴스 트렌드 + 기업 (테마)**
```
[1] DocumentTrends(["news"],["economy"],"AI and 반도체",interval="1M",date_from=20240101,date_to=20241231)
[2] ("AI" 관련 기업) and 매출 > 100000000000 and 영업이익 > 0
```

**패턴 6: IPO Peer 비교 (비상장사 상장 심사)**
```
[1] GetCompanySummary(채비)                                                  → 업종, 설립일, 외감 여부
[2] DocumentSearch(["news"],[],"전기차 충전기 제조 상장 IPO",count=20,page=1)  → Peer 후보
[3] GetFinancialStatements([에스트래픽, 그리드위즈, 위츠], consolidated=True, date_from=2020-01-01, date_to=2024-12-31)   → 한 번에
[4] GetFinancialStatements(채비, consolidated=False, date_from=2020-01-01, date_to=2024-12-31)
[5] 매출총이익률·원가율·자본잠식·차입금의존도·영업CF 비교 (예: 채비 매출총이익률 3% vs Peer 평균 19%)
```

**패턴 7: 공시 vs 뉴스 교차검증 (미공개정보)**
```
[1] DocumentSearch(["news"],[],"title:(인수 or 합병) and securities.name:대상기업",count=100,page=1,date_from=20250101,date_to=20250228)
[2] DocumentSearch(["company"],["disclosure"],"securities.name:대상기업 and (인수 or 합병)",count=100,page=1,date_from=20250101,date_to=20250228)
[3] 뉴스가 공시보다 앞서면 → 미공개정보 이용 의심
```

---

## 결과 포맷팅

**출처 표기 (필수):** 모든 결과 하단에 씁니다. 여러 유형이면 모두 나열합니다.
```
📌 데이터 출처: NICE평가정보 재무데이터 | KRX 한국거래소 / 코스콤 시장데이터 (주가는 수정주가) | 국내 주요 언론사
```

| 조회 내용 | 출처 표기 |
|---|---|
| 재무제표 | `NICE평가정보 재무데이터` |
| 주가·시가총액·PER 등 | `KRX 한국거래소 / 코스콤 시장데이터 (주가는 수정주가)` |
| 기업개요 | `NICE평가정보 기업정보` |
| 공시·IR | `금융감독원 DART 전자공시` |
| 뉴스 | `국내 주요 언론사 (매일경제, 한경 등)` |
| 증권사 리포트 | `증권사 리서치센터 리포트` |
| 특허 | `특허정보원 KIPRIS` |

**형식:**
- **문서 검색:** `## 검색 결과 (총 N건)` → 문서마다 `### 1. [제목]`, `- 출처: 언론사 | 날짜 | 감성`, `- 관련종목: 기업명(종목코드)`
- **재무/주가:** 표. 금액은 억/조 단위로 바꾸고, 회계기준·연결/별도(재무)나 수정주가 안내(주가)를 붙입니다.
- **스크리닝:** `| 기업명 | 종목코드 | 매출액 | 영업이익률 |` 표
- **멀티스텝:** 단계별 요약 → 종합 분석/인사이트

**후속 분석 제안 (필수):** 답변 끝에 관련 후속 분석을 2~4개 제안하세요. 예:
- 뉴스 검색 후: 해당 종목의 공시·IR, 애널리스트 보고서, 기사·보고서 전문, 최근 주가, 이슈 카테고리별 분류
- 재무 조회 후: 실적 관련 뉴스, 동종업종 Peer 비교, 세부 계정(재고·매출채권·차입금·현금흐름), 목표가·보고서 본문
- 주가 조회 후: 변동 구간의 뉴스·공시, 감성 추이 비교, 거래량 급변 구간 뉴스, 그날 시황 리포트
- 스크리닝 후: 개별 기업 상세 재무, 최근 뉴스, 수익률 시뮬레이션

---

## 이 스킬에 예시가 없는 DeepSearch 기능

아래 함수는 이 레포의 API 키로 동작을 확인했습니다(2026-11-25). 호출 형식은 레포 `docs/reference/DEEPSEARCH_API_MASTER.md`(17절 전체 함수표)에 있습니다. 요청이 있으면 `query_api.py`로 바로 호출하세요.

| 분야 | 함수 | 용도 |
|---|---|---|
| 기업 정보 | `GetCompanyHistory`, `GetCompanyBusinessSummary`, `GetCompanyRelatedFirms`, `GetCompanyDebts`, `GetCompanyBranches`, `GetCompanyProductsSales`, `GetFinancialStatementsAuditOpinion` | 연혁, 사업 요약, 관계사, 차입금, 사업장, 제품별 매출, 감사의견 |
| 공시(DART 정기보고서) | `GetDartDividends`, `GetDartShareRepurchase`, `GetDartMajorityShareholders`, `GetDartMajorityShareholderChange`, `GetDartMinorityShareholders`, `GetDartExecutives`, `GetDartEmployees`, `GetDartIndividualDirectorCompensation`, `GetDartOverallDirectorCompensation`, `GetDartTopIndividualCompensation`, `GetDartInvestmentInOthers` | 배당, 자사주, 최대주주·변동, 소액주주, 임직원, 임원 보수, 타법인 출자 |
| 컨센서스·이슈 | `GetConsensusInstitutionList`, `GetConsensusAnalystList(inst_code)`, `SearchFirmFundamentalsForecasts`, `GetTargetPriceConsensusChange`, `GetCompanyShareholderChanges` | 증권사·애널리스트, 실적 전망, 목표가 변화, 주주 변동 기업 |
| 주가·지수 | `GetStockPrices`, `GetStockSymbols`, `GetMarketIndexes`, `GetMarketIndexSymbols` | B-2 참고 |
| 기업 주제·집단 | `GetEntityTags`, `FindEntityByTag`, `GetConditionalTagMetadata`, `FindConglomerateByID`, `GetConglomerateFinancialStatements` | 테마 태그, 그룹 재무 |
| 인물 | `FindPersonBio(name, birthday)` | 인물 경력 |
| 이벤트 | `ComputePortfolioReturns`, `ComputeEventDayStockReturns` | 포트폴리오 수익률, 이벤트일 종목 수익률 |
| 경제지표 | 한국은행 `QueryBankOfKoreaSeries*`, FRED `QueryFredSeries*`, IMF `GetImf*`, OECD `GetOecd*`, World Bank `QueryWorldBank*`, 딥서치 자체 `QueryDeepSearchOwn*` (시리즈 검색 `FindEntity("DataSeries", "검색어")`) | 거시 지표. **기간을 꼭 지정**하세요(전체 시계열은 수 MB) |
| 토픽 인사이트 (REST) | `query_api.py "/v1/topic-insight/insight?type=trending&section=economy&topicId={uid}&stream=false"` (`questions`도 있음) | 토픽 요약·질문. `topicId`는 `SearchTrendingTopics`의 `uid` |

**쓰지 마세요** (현재 구독으로 안 되거나 고장, 2026-11-25 확인):
- 미제공(`NameError: UFunction ... is not defined`): 채권 함수 전부, 통계청(KOSIS) 전부, 채권 이벤트, `GetDartCapitalChange`, `GetFundamentalsConsensusChange`, `GetAggregateIndustryInfo`, `GetAggregateIndustryConsensus`, `SearchFinancialStatementsAuditOpinion`
- 서버 오류·타임아웃: `GetMarketSummaryInfoByIndustry`·`GetIndustryReturnsOnEventDates`·`GetCumulativeIndustryReturns`(`KeyError: industry_id`), `AnalyzePortfolioReturns`(AttributeError), `FindPeopleByBirthday`·`FindRichestShareholders`·`ComputeStockReturnCorrelationWith`(타임아웃), `SearchAnalystReports`(500 → 애널리스트 보고서는 `DocumentSearch(["research"],["company"],...)`)
- compute 밖 API: DeepSearch v2 REST(`api-v2.deepsearch.com`), 해외기업(`/v2/companies`), 챗딥서치(`/note/v1`) — 이 키로 401

이런 요청에는 "이 요청은 현재 DeepSearch 구독으로 조회할 수 없습니다(`{함수명}`: {이유}). 대신 {대안}으로 확인할 수 있습니다."라고 답하세요. 대안이 없으면 그렇다고 말하고 OpenDART 등 다른 출처를 제안하세요.

## Resources

- [references/api_quick_reference.md](references/api_quick_reference.md) — 함수 호출식 요약
- [references/verified_examples.md](references/verified_examples.md) — 검증된 사용 사례
- [references/krx_monitoring_guide.md](references/krx_monitoring_guide.md) — KRX 업무 문서검색 패턴
- [references/value_investing.md](references/value_investing.md) — 가치투자 방법론
- [references/market_overview_template.md](references/market_overview_template.md) — 시황 리포트 출력 템플릿
