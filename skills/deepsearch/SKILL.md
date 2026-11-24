---
name: deepsearch
description: "DeepSearch API(api.deepsearch.com)로 한국 기업 데이터를 조회·분석한다. 뉴스·증권사 리포트·공시/IR·특허 검색과 트렌드·감성, 상장사·외감 비상장사 재무제표(GetFinancialStatements), 주가·PER·PBR·시가총액, 조건 스크리닝, 일일 시황 리포트, 여러 데이터를 엮은 멀티스텝 분석(뉴스+주가, 공시 vs 뉴스 등)에 사용한다. 사용자가 DeepSearch/딥서치를 언급하거나, DeepSearch API 키가 있는 프로젝트에서 KRX 상장사 문서·재무·주가 데이터를 요청하면 적용한다."
---

# DeepSearch 통합 스킬

문서검색, 기업/재무 데이터, 스크리닝/분석을 하나의 스킬로 처리합니다.
**특히 여러 데이터 소스를 연결하는 멀티스텝 분석에 특화**되어 있습니다.

## 시작하기 (먼저 읽기)

- **경로:** 이 문서의 `${CLAUDE_SKILL_DIR}`는 이 SKILL.md가 있는 폴더입니다. 스킬로 설치하지 않고 레포를 클론해 직접 읽는 경우 `skills/deepsearch`로 바꿔 쓰세요.
- **설치:** `pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt` (requests, PyMuPDF)
- **호출:** `python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "쿼리"`. API 키는 스크립트가 직접 찾습니다(아래 "API 키").
- **큰 결과는 파일로 저장됩니다.** 결과 JSON이 2만 자를 넘으면 스크립트가 임시 폴더에 저장하고 `saved_to` 경로와 미리보기만 출력합니다. 그 파일을 Python으로 읽어 필요한 부분만 쓰세요. 파일 내용을 통째로 다시 출력하지 마세요.
- **다른 자료:** `references/`(호출식·검증 사례), 레포 `research/`(데이터 정의 검증 노트). 레포 `docs/reference/`의 원본 API 문서는 크니 이 문서에 없는 함수를 찾을 때만 grep으로 검색하세요.

## ⚠️ 최우선 라우팅 규칙

### 규칙 1: 재무제표 조회 → GetFinancialStatements 필수 (자연어 쿼리 절대 금지)

**매출, 영업이익, 자산, 부채, 자본, 현금흐름, 재무제표, 재무 데이터** 등 모든 재무제표 항목 조회 시:

**❌ 절대 하지 마세요 — 아래 형태의 자연어 쿼리는 모두 금지:**
```
기업명 매출액 2020-2024                    ← 금지 (KeyError 발생)
기업명 매출액 영업이익 당기순이익 2020-2024 ← 금지
기업명 연결 매출액 2020-2024               ← 금지 (KeyError 빈발)
기업명 별도 매출액 2020-2024               ← 금지
기업명 자산 부채 자본 2020-2024            ← 금지
```

**✅ 반드시 이렇게 하세요 — GetFinancialStatements API 함수 사용:**
```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE코드 또는 KRX코드)

# 2단계: 전체 재무제표 조회 (507개 계정항목 한 번에 반환)
GetFinancialStatements(기업명, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
```
- 기업명은 따옴표 없이 씁니다: `GetFinancialStatements(삼성중공업)`
- 수백 개 계정이 연도별로 한 번에 반환됩니다(삼성전자 1년치 507행, 원본 응답 수백 KB). **`--grep`으로 필요한 계정만 남기세요.**
- **계정명은 `매출액`이 아닙니다.** `name_ko` 기준으로 아래 이름을 쓰세요. `--grep 매출`처럼 부분일치로 걸면 매출원가·매출채권까지 섞입니다.

| 찾는 항목 | `name_ko` | report_id / account_id |
|---|---|---|
| 매출액 | `수익` | 12 / 1000 |
| 매출원가 · 매출총이익 | `매출원가` · `매출총이익(손실)` | 12 / 2000 · 3000 |
| 영업이익 | `영업이익(손실)` | 12 / 5000 |
| 당기순이익 | `총당기순이익` (지배주주분: `당기순이익지배기업지분`) | 12 / 8200 (9061) |
| 자산·부채·자본총계 | `자산총계` · `부채총계` · `자본총계` | 11 / 5000 · 8000 · 8900 |

report_id 11 = 재무상태표, 12 = 손익계산서, 19 = 재무비율. (삼성전자·삼성중공업 2024년 값으로 확인, 2026-11-25)

```bash
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py 'GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)' --grep '^(수익|영업이익\(손실\)|총당기순이익)$'
```
- 자연어 쿼리는 **주가/PER/PBR/시가총액** 등 시장 데이터에만 사용하세요

### 규칙 2: 시황 분석 → market_overview.py 필수

사용자가 시황, 시장 분석, 마켓 리포트, 시장 동향, 장 마감 정리, 오늘 장 등을 요청하면:

**❌ 절대 하지 마세요 (WRONG):**
- DocumentSearch로 뉴스 검색
- GetMarketIndexes로 지수 조회
- DocumentAggregation으로 종목 집계
- 위 API들을 병렬 호출해서 시황을 직접 조합

**✅ 반드시 이렇게 하세요 (RIGHT):**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/market_overview.py "YYYY-MM-DD"
```
이 스크립트 **하나만 실행**하면 지수·규모별·시총등락·뉴스언급·헤드라인·토픽·감성 7개 섹션이 자동 생성됩니다.
스크립트 실행 후 JSON 결과를 아래 마크다운 템플릿으로 변환하여 사용자에게 보여주세요.

### 규칙 3: 주가 데이터를 쓰면 → 수정주가 안내를 데이터보다 먼저

DeepSearch 주가(시가·고가·저가·종가)는 **수정주가뿐이고 원주가 옵션이 없습니다.** 거래량·거래대금·시가총액은 수정되지 않은 당일 값입니다. 주가·거래량·수익률을 보여주는 답변에서는 **표나 수치보다 먼저** 아래 안내를 넣으세요. 시황 리포트도 마찬가지입니다. `market_overview.py`·`market_top_movers.py` 결과 JSON에 들어 있는 `price_basis_notice` 문구를 그대로 써도 됩니다.

```
> ℹ️ 주가 기준: 시가·고가·저가·종가는 수정주가입니다(액면분할·무상증자·유상증자를 과거 가격에 소급 반영, 배당은 미반영). DeepSearch는 원주가를 따로 제공하지 않습니다. 거래량·거래대금·시가총액은 당일 실제 값입니다.
```

상황에 따라 한 줄을 덧붙이세요:
- **조회 기간에 분할·증자가 끼어 있으면:** "○월 ○일 액면분할(또는 증자) 전후로 거래량은 직접 비교할 수 없습니다." (확인 방법은 Section B "주가 데이터 함정" 참고)
- **기간 수익률을 보여주면:** "배당을 뺀 가격수익률입니다."
- **사용자가 원주가(당시 실제 가격)를 원하면:** `market_cap ÷ shares_outstanding`으로 계산했다고 밝히세요.
- **2020년 이전 주가:** 자연어 쿼리로는 나오지 않습니다. `GetStockPrices`로 조회하세요(Section B).

### 규칙 4: 과거 재무값·BPS/EPS로 백테스트하거나 시점을 따지면 → 한계를 먼저 밝힘

- **과거 재무제표 값의 기준이 섞여 있습니다.** `GetFinancialStatements`의 과거 연도 값은 원래 공시값인지, 다음 해 보고서의 재작성값인지 일관되지 않습니다. 재작성된 회사·연도의 약 3/4은 재작성값, 1/4은 원래값이고, 구분 필드나 옵션은 없습니다. IFRS17 보험사의 2022년은 대부분 재작성 전 값입니다. "그 시점에 알 수 있던 값"이 꼭 필요하면 OpenDART에서 받으세요.
- **시장데이터 BPS·EPS(따라서 PBR·PER)에는 look-ahead가 있습니다.** FY N 값이 N+1년 첫 거래일부터 붙어 있는데, 그때는 아직 결산 공시 전입니다. 백테스트에서는 사업보고서 공시 시점(보통 3월 말) 이후로 밀어 쓰세요.
- **BPS 정의는 하나뿐입니다.** 연결 지배기업소유주지분 ÷ (보통주+우선주 − 자기주식), 직전 연말 기준. `별도`·`분기` 같은 단어를 붙여도 무시됩니다. 다른 정의가 필요하면 `GetFinancialStatements`로 직접 계산하세요.

근거: 레포 `research/restatement/`, `research/pbr_bps/` (검증 2026-11-20)

## API 키

- **스크립트가 직접 찾습니다.** 순서: 환경변수 `DEEPSEARCH_API_KEY` 또는 `API_KEY` → 현재 폴더와 상위 폴더의 `.env` → 스킬 폴더 상위의 `.env`. raw `id:secret` 형식이면 base64로 자동 변환합니다.
- **키 값을 화면에 내지 마세요.** `.env`를 `cat`/`echo`하거나 키를 명령 인자로 넣으면 대화 기록에 남습니다. (첫 인자로 키를 넘기는 구 방식도 동작은 합니다)
- 키를 못 찾으면 스크립트가 안내 메시지를 냅니다. 그때 사용자에게 **한 번만** 요청하고, 프로젝트 루트 `.env`에 `API_KEY=<키>` 한 줄로 저장하세요(`.gitignore`에 `.env`가 있는지 확인).

## 데이터 출처

DeepSearch API는 아래 **공신력 있는 기관의 공식 데이터**를 수집·가공하여 제공합니다.

| 데이터 유형 | 원천 기관 | 비고 |
|------------|----------|------|
| 재무제표·기업정보 | **NICE평가정보** (나이스평가정보㈜) | 외감기업 재무데이터, 기업개요, 산업분류. 심볼이 `NICE:` 접두어 |
| 주가·시장데이터 | **KRX 한국거래소** / **코스콤(KOSCOM)** | 종가, 시가총액, 거래량, PER, PBR 등 일별 시장데이터 |
| 공시·IR | **금융감독원 DART** (전자공시시스템) | 사업보고서, 분기보고서, 주요사항보고서 등 |
| 뉴스 | **각 언론사** (매일경제, 한경, 이데일리 등) | 국내 주요 언론사 기사 원문 |
| 증권사 리포트 | **각 증권사** (미래에셋, 삼성증권 등) | 기업분석, 산업분석, 시장전략 리포트 |
| 특허 | **특허정보원 KIPRIS** | 국내 특허·실용신안 공개/등록 정보 |

**결과 출력 시 반드시 데이터 출처를 표기하세요.** 아래 결과 포맷팅 섹션의 출처 표기 규칙을 따르세요.

## 쿼리 라우팅

사용자 요청을 분석하여 아래 유형 중 하나 또는 복합으로 처리하세요:

| 요청 유형 | 판단 기준 | 처리 방법 |
|-----------|----------|----------|
| **⚡ 시황분석** | 시장 현황, 시황, 마켓 리포트, 장 마감 정리 | **market_overview.py 실행** |
| **문서 검색** | 뉴스, 리포트, 공시, 트렌드, 감성분석 | Section A |
| **재무제표** | 매출, 영업이익, 자산, 부채, 재무제표 | Section B → **GetFinancialStatements 필수** |
| **주가/시장** | 종가, PER, PBR, 시가총액, 거래량 | Section B → 자연어 쿼리 OK (2020년 이후만). **규칙 3 수정주가 안내 필수** |
| **기업정보** | 배당, 주주, 임원, 기업개요 | Section B → API 함수 |
| **스크리닝/분석** | 조건 필터링, Top/Bottom, 전략, 비교 | Section C |
| **멀티스텝 분석** | 위 유형 2개 이상 결합 필요 | Section D |

## Section A: 문서 검색

### 쿼리 형식
```
DocumentSearch(["카테고리"],["섹션"],"쿼리",count=100,page=1,date_from=YYYYMMDD,date_to=YYYYMMDD)
DocumentTrends(["카테고리"],["섹션"],"쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
DocumentAggregation(["카테고리"],["섹션"],"쿼리","groupby필드:N")
GetSentimentScore("쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
SimilarKeywords("키워드",max_count=10)
```

### 카테고리/섹션
- 뉴스 → `["news"]` (economy, tech, society, politics, culture, world, entertainment, opinion)
- 리서치 → `["research"]` (market, strategy, company, industry, economy, bond)
- 공시/IR → `["company"]` (ir, disclosure)
- 특허 → `["patent"]`
- 미지정 → `["news"]` 기본, 섹션은 `[]`

### 필드 쿼리
- 기업 → `securities.name:기업명` / 시장 → `securities.market:KOSPI`
- 감성 → `polarity.name:긍정` / ESG → `esg.category.name:환경`
- 제목 → `title:키워드` / 본문 → `content:키워드`
- 언론사 → `publisher.raw:('매일경제')` / Boolean: `and`, `or`, `!`, `()`

### 날짜+시간 기준 검색
특정 시간대의 뉴스를 검색할 때 `created_at` 필드를 사용합니다:
```
DocumentSearch(["news"],["economy"],"securities.market:KOSPI and created_at:[\"2025-02-28T09:00:00\" to \"2025-02-28T12:00:00\"]",count=100,page=1)
```
→ 2025년 2월 28일 오전 9시~12시 코스피 상장사 관련 뉴스

### 이슈 카테고리별 검색 키워드
사용자가 특정 이슈 유형을 요청할 때 아래 키워드 패턴을 활용하세요:

| 이슈 카테고리 | 검색 키워드 패턴 |
|-------------|----------------|
| **계약/수주** | `(수주 and 체결) or (수주 and 공급) or (계약 and 체결) or (계약 and 공급)` |
| **인수/투자** | `인수 or 합병 or 분할 or 영업양도 or 영업양수 or 출자 or 투자` |
| **실적** | `(매출 and 발표) or (실적 and 공시) or (이익 and 달성) or (배당 and 결정)` |
| **증자/감자** | `증자 or 감자 or 주식교환 or 주식이전 or 우회상장` |
| **회계/감사** | `상장폐지 or 관리종목 or 자본잠식 or (비적정 and 감사) or (의견거절 and 감사) or 분식` |
| **소송/부도** | `소송 or 횡령 or 배임 or 부도 or 파산 or 회생 or (기소 and 대표이사)` |

예시: 코스피 상장사 관련 인수/투자 뉴스 → `securities.market:KOSPI and (인수 or 합병 or 출자 or 투자)`

### 종목별 공시/IR/애널리스트 보고서 조회
특정 종목의 문서를 카테고리별로 조회할 수 있습니다:
```
# 공시 (금감원 DART)
DocumentSearch(["company"],["disclosure"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)

# IR 자료
DocumentSearch(["company"],["ir"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)

# 애널리스트 보고서 (증권사 리서치)
DocumentSearch(["research"],["company"],"securities.symbol:KRX:005930",count=50,page=1,date_from=20240101,date_to=20241231)
```

### KRX 문서검색 패턴
- 조회공시 후보 → `title:(인수 or 합병 or 매각) and securities.market:(KOSPI or KOSDAQ)`
- 부정 뉴스 → `securities.market:KOSPI and polarity.name:부정`
- ESG 이슈 → `esg.category.name:지배구조 and esg.polarity.name:부정`
- 불공정거래 → `title:(시세조종 or 불공정거래 or 내부자거래)`
- 뉴스 언급 상위 → `DocumentAggregation` + `securities.name:20`

### 문서 본문 읽기 (애널리스트 보고서, IR자료)

DocumentSearch 결과의 `content` 필드는 100~500자 요약만 포함됩니다. **사용자가 특정 문서의 상세 내용을 요청하면** `read_document.py`로 원문(PDF/HTML)을 다운로드하여 전체 텍스트를 추출합니다.

**동작 방식:**
1. DocumentSearch로 문서 목록 조회 → 결과에서 `content_url` 확보
2. `read_document.py`로 해당 URL의 PDF/HTML 원문 텍스트 추출
3. 추출된 전체 텍스트를 기반으로 사용자 질문에 답변

**문서 유형별 추출 결과:**
| 문서 유형 | 형식 | 추출 결과 | 비고 |
|----------|------|----------|------|
| 애널리스트 보고서 | PDF | 전체 텍스트 (수천~수만 자) | 표, 차트 텍스트 포함 |
| IR 자료 | PDF | 전체 텍스트 (수천~수만 자) | 경영설명회 등 |
| 뉴스 기사 | HTML | 기사 본문 (최대 10,000자) | 일부 노이즈 포함 가능 |
| 공시 (DART) | HTML | 인덱스만 추출 (프레임 구조) | 본문 추출 제한적 |

**사용 패턴:**
```bash
# 방법 1: content_url을 직접 지정
python ${CLAUDE_SKILL_DIR}/scripts/read_document.py "https://ddi-cdn.deepsearch.com/.../report.pdf"

# 방법 2: 검색 후 N번째 문서 본문 읽기
python ${CLAUDE_SKILL_DIR}/scripts/read_document.py 'DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=5,page=1)' --doc 1
```

**활용 시나리오:**
- "삼성전자 최근 애널리스트 보고서에서 목표주가 근거를 알려줘" → 보고서 PDF 본문 추출 후 답변
- "이 IR 자료에서 가이던스 내용 요약해줘" → IR PDF 본문 추출 후 답변
- 문서 목록 표시 후 → "2번 보고서 내용을 자세히 알려줘" → 해당 문서 본문 추출

**주의:** 공시(DART) 문서는 iframe 구조로 인해 전체 본문 추출이 제한적입니다. 공시 상세 내용은 DART 링크를 사용자에게 제공하세요.

### ⚠️ DocumentSearch 실전 함정 (검증됨 — 같은 시행착오 금지)

> 출처: `notes/HANDOFF_DocumentSearch_news_20260610.md`

1. **기간 1년 한도**: Basic auth로는 DocumentSearch 기간이 **1년을 넘으면 결과를 못 받습니다**(HTTP 413, `RequestEntityTooLarge: Not allowed to search more than 1 year if not logged in`). fields나 OR 괄호 문제가 아닙니다.
   → **`query_api.py`가 1년 이하 구간으로 자동 분할**하고 `content_url`로 중복 제거해 최신순으로 합칩니다. 구간별 건수는 결과의 `windows`에 있습니다. DocumentTrends는 2년 범위도 정상입니다(2026-11-25 확인).
2. **에러 원인은 `data.exceptions[]`에 있습니다**(HTTP 200이어도 올 수 있음). `query_api.py`는 이를 `error`와 `hint`로 보여줍니다. 결과가 0건이면 이것부터 보세요.
3. **페이지:** 기본은 쿼리의 `page` 한 페이지만 가져옵니다. 더 필요하면 `--max-pages N`(구간마다 N페이지). `count`는 최대 100.
4. 직접 호출할 때만: 문서 리스트 키는 `docs`(NOT `documents`, 경로 `data["pods"][1]["content"]["data"]["docs"]`), 쿼리는 `urllib.parse.quote(query, safe="")`로 인코딩(한글·괄호·`&`), Windows 콘솔은 CP949라 결과는 UTF-8 파일로 확인.

### 제한사항
- **DocumentSearch 기간은 최대 1년.** `query_api.py`가 자동 분할합니다.
- interval: `1y`, `1M`, `1w`, `1d`, `1h`, `1m`

---

## Section B: 기업 & 재무/시장 데이터

### ⚠️ 재무제표 조회 — 반드시 GetFinancialStatements 사용 (자연어 쿼리 금지)

**재무제표(매출, 영업이익, 자산, 부채, 자본, 현금흐름 등)를 조회할 때는 자연어 쿼리를 사용하지 마세요.**
**반드시 아래 2단계 절차를 따르세요:**

```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE:IX5118)
# → type(IFRS/GAAP), consolidated(True/False), converted(True/False) 확인

# 2단계: 전체 재무제표 조회 (507개 계정항목 한 번에 반환)
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(삼성전자, consolidated=False)       # 별도 재무제표
GetFinancialStatements(삼성전자, report_ids="BalanceSheet") # 특정 제표만
```

| 파라미터 | 값 | 설명 |
|---------|---|------|
| report_type | "IFRS" / "GAAP" | 회계기준 |
| consolidated | True / False | 연결/별도 |
| is_annual | True / False | 연간/분기 포함 |
| report_ids | "BalanceSheet", "Income", "CashFlow", "Ratio" | 특정 제표만 조회 (미지정시 전체) |

**계정명:** 매출액은 `수익`, 영업이익은 `영업이익(손실)`, 당기순이익은 `총당기순이익`입니다(규칙 1의 표).

**❌ 자연어 쿼리로 재무제표를 조회하지 마세요:**
```
# 아래는 모두 WRONG — KeyError 발생 가능
삼성전자 매출액 2020-2024              ← 사용 금지
마키나락스 연결 매출액 2020-2024       ← 사용 금지
삼성전자 매출액 영업이익 당기순이익     ← 사용 금지
```

**활용 예시:**
```
# 전체 재무제표를 받은 뒤 필요한 항목만 필터링
GetFinancialStatements(삼성중공업, consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ 반환된 507개 항목에서 name_ko에 "미청구" 포함된 계정 필터링
→ 매출액, 영업이익 등 주요 항목도 여기서 추출
```

### 주가/시장 데이터 조회 (자연어 쿼리 사용)

**주가, PER, PBR 등 시장 데이터는 자연어 쿼리로 조회합니다** (재무제표와 다릅니다):
```
삼성전자 종가 2024-06-01-2024-06-30   → 일별 종가
삼성전자 PER                          → 현재 PER
삼성전자 PBR                          → 현재 PBR
삼성전자 시가총액 2024-01-01-2024-12-31 → 일별 시가총액
```

**데이터 유형:**
- **주가/시장 (일별, 자연어 OK):** 종가, 시가, 고가, 저가, 시가총액, 거래량, PER, PBR, EPS, BPS, DPS
- **재무제표 (연/분기, GetFinancialStatements 필수):** 매출액, 영업이익, 당기순이익, 자산, 부채, 자본 등
- **기업 개요:** 대표이사, 종업원수, 설립일, 주거래은행, 산업분류

### ⚠️ 주가 데이터 함정 (검증됨, 2026-11-25)

> 근거: 레포 `research/price_adjustment/README.md` (삼성전자·NAVER·카카오 분할, 유한양행 무상증자, 대한항공 유상증자로 검증)

1. **수정주가만 나온다. 원주가 옵션은 없다.** `GetStockPrices`의 파라미터는 `entities, columns, date_from, date_to`뿐입니다. `adjusted=`, `raw=`, `columns=["adj_close"]`, `["수정종가"]` 같은 이름은 모두 400 에러입니다(없는 이름이면 무엇이든 400). 이런 옵션을 찾느라 호출을 반복하지 마세요.
2. **가격만 수정되고 수량은 수정되지 않는다.** open/high/low/close는 액면분할·무상증자·유상증자 권리락에 맞춰 소급 수정됩니다(배당은 미반영). volume·value(거래대금)·shares_outstanding·market_cap은 당일 실제 값입니다. 그래서 수정 이벤트 이전 날짜에서는 다음 계산이 틀립니다.
   - `close × shares_outstanding` ≠ 시가총액 → `market_cap`을 그대로 쓰세요
   - `close × volume` ≠ 거래대금 → `value`를 그대로 쓰세요
   - 분할 전후 거래량은 분할 비율만큼 계단이 생깁니다(삼성전자 50배). 거래량 급증 감지에서 분할일을 이벤트로 오인하지 마세요.
3. **원주가가 필요하면** `원주가 종가 = market_cap ÷ shares_outstanding`으로 구합니다. 시가·고가·저가는 그날의 수정계수(`원주가 ÷ close`)를 곱합니다. **명목 분할비율을 곱하면 틀립니다.** 재상장 기준가의 호가단위 반올림 때문에 NAVER 5:1 분할의 계수는 4.99291이었습니다.
4. **수정 이벤트 확인법:** 같은 기간을 `GetStockPrices(종목, columns=["close","shares_outstanding","market_cap"], date_from=..., date_to=...)`로 받아 날마다 `market_cap ÷ shares_outstanding ÷ close`를 계산합니다. 이 값이 바뀌는 날이 수정 이벤트(권리락·분할)일입니다. 기간 끝까지 1이면 그 구간에는 이벤트가 없습니다.
5. **자연어 쿼리는 2020-01-02 이후만 나온다(오류 없이).** `삼성전자 종가 2018-04-25-2018-05-08`은 **오늘 값 1행**을 돌려주고, `2019-12-23-2020-01-10`은 2020-01-02부터 잘려 나옵니다. 컬럼명에는 요청한 범위가 그대로 붙어 있어 결과만 보고는 알 수 없습니다. 결과 첫 행의 날짜가 요청 시작일 근처인지 반드시 확인하고, 2020년 이전은 `GetStockPrices(..., date_from=..., date_to=...)`를 쓰세요. 값은 두 경로가 같습니다.
6. **매매정지일에도 행이 있다.** 분할을 위한 거래정지 기간 등에는 거래량 0, 가격은 직전 값이 반복됩니다(`trading_halted` 컬럼). 일별 수익률·변동성 계산 시 0%가 끼어듭니다.
7. **과거 값이 나중에 바뀔 수 있다.** 수정주가는 "오늘 주식수 기준"이라, 새 분할·증자가 생기면 그 이전 가격이 모두 다시 계산됩니다. 저장·비교할 때는 조회일을 함께 남기세요.

```
GetStockPrices(KRX:005930, columns=["open","high","low","close","volume","value","shares_outstanding","market_cap"], date_from=2018-04-25, date_to=2018-05-08)
→ 2018-04-26: close 52,140 (원주가 2,607,000 ÷ 50), volume 360,931 (분할 전 실제 주식 수 기준), market_cap 334.7조
```

### 분기 데이터 규칙
- 분기 데이터도 `GetFinancialStatements(기업명, is_annual=False)`로 조회하세요
- 자연어 분기 쿼리("삼성전자 분기 매출")는 보조 수단으로만 사용

### API 함수
```
FindEntity("Financial","삼성*")
GetCompanySummary("삼성전자")
GetCompanyDividends("삼성전자",date_from=20200101,date_to=20241231)
GetCompanyShareholders("삼성전자")
GetCompanyExecutives("삼성전자")
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2024-01-01, date_to=2024-12-31)
GetAvailableFinancialStatements(KRX:005930)
GetStockPrices(KRX:005930, columns=["close","volume","market_cap"], date_from=2018-01-01, date_to=2018-12-31)
GetDartDividends(KRX:005930, date_from=2020-01-01, date_to=2024-12-31)      # 공시(정기보고서) 배당
GetDartMajorityShareholders(KRX:005930, date_from=2024-01-01, date_to=2024-12-31)
GetCompanyProductsSales(KRX:005930)                                         # 제품별 매출
SearchTargetPrices("005930",date_from=20240101,date_to=20241231)
FindConglomerateByName("삼성")
GetConglomerateMembers("삼성")
FindPeopleByName("이재용")
```

### 기업 검색 예약어
- `"반도체" 관련 기업` / `"건강기능식품" 산업 기업` / `"웹툰" 사업 기업`
- `"서울 마포구" 주소 기업` / `"국민연금" 주주 기업` / `상장 기업`

### 비상장사 재무제표 조회 (외감 기업)

비상장사도 외부감사 대상이면 재무제표 조회 가능합니다. **상장사와 동일하게 GetFinancialStatements를 사용하세요.**

**기본 규칙:**
| 항목 | 상장사 | 비상장사 (외감) |
|------|--------|----------------|
| 연결 재무제표 | 대부분 있음 | **대부분 없음** (별도만 존재) |
| 기본 조회 | 연결 우선 | 별도 자동 반환 |
| 데이터 시작 연도 | 상장일 기준 | 외감 시작일 기준 (보통 최근 5~9년) |
| 분기 데이터 | 최근 ~7분기 | **매우 제한적** (최근 1~2건) |
| GetCompanySummary | 상세 정보 | 최소 정보만 반환 |

**조회 절차 (상장사와 동일):**
```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE:IX5118)
# → consolidated=False만 있으면 별도만 존재

# 2단계: 재무제표 조회
GetFinancialStatements(채비, consolidated=False, date_from=2020-01-01, date_to=2024-12-31)
```

**주의사항:**
- 비상장사는 `GetCompanySummary`가 거의 빈 결과를 반환합니다. 재무 데이터는 `GetFinancialStatements`로 조회하세요.
- 데이터 시작 연도를 모르면 넓은 범위(예: 2010-2024)로 먼저 조회하여 실제 데이터 범위를 확인하세요.
- 재무 데이터를 사용자에게 보여줄 때 **반드시 회계기준과 연결/별도 여부를 명시**하세요 (예: "K-IFRS 연결 기준", "K-GAAP 별도 기준").

---

## Section C: 스크리닝 & 분석

### 재무 조건 스크리닝
```
매출 > 1000000000000                              → 매출 1조 이상
영업이익 / 매출 > 0.15                             → 영업이익률 15% 이상
2023 매출 > 2022 매출 * 1.5                       → 전년대비 50% 성장
매출 > 1000000000000 and 영업이익 / 매출 > 0.15   → 복합 조건
설립일 > 2020-01-01                               → 2020년 이후 설립
```

### 시장별 스크리닝 (KOSDAQ/KOSPI 필터)
```
코스닥 상장 기업                                   → 코스닥 전체 (1,820개)
코스피 상장 기업                                   → 코스피 전체 (2,404개)
코스닥 상장 기업 and 매출액 > 100000000000         → 코스닥 매출 1000억+ (697개)
코스닥 상장 기업 and 영업이익 < 0 and 매출 > 500000000000 → 코스닥 적자 대형
```
**주의:** `코스닥`/`코스피`는 한글로 써야 합니다 (KOSDAQ/KOSPI 영문은 안 됨).

### 시가총액 상위 종목 + 등락률 (전용 스크립트)
```bash
python ${CLAUDE_SKILL_DIR}/scripts/market_top_movers.py kosdaq 150 2025-02-27
python ${CLAUDE_SKILL_DIR}/scripts/market_top_movers.py kospi 100 2025-02-27
```
**용도:** "코스닥 시가총액 상위 150개 중 가장 많이 하락한 종목", "코스피 시총 상위 100개 등락률" 등
내부에서 전체 종목 조회 → 개별 시가총액/종가 병렬 수집 → 시가총액 정렬 → 등락률 계산을 자동 수행합니다.

### KRX 재무위험 스크리닝
```
영업이익 < 0 and 매출 > 500000000000              → 영업적자 대형 (152개)
자본 < 0 and 매출 > 10000000000                   → 자본잠식 (1,567개)
부채 / 자본 > 5 and 매출 > 100000000000           → 고부채비율 (512개)
상장 기업 and 2024 매출 < 2023 매출 * 0.7         → 매출 30%+ 급감 (26개)
```

### 분석 함수
```
Top(매출액, 10)                    → 매출 상위 10개
Bottom(영업이익, 10)               → 영업이익 하위 10개
Max(삼성전자 매출액 2015-2024)     → 최대 매출액
Mean(삼성전자 종가 2024-01-01-2024-12-31) → 평균 종가
```

### 스크리닝 제한사항 (중요)
| 제한 | 설명 | 대안 |
|------|------|------|
| `Top(시가총액, N)` 불가 | 시가총액은 일별 시장데이터라 Top/Bottom 불가 | `market_top_movers.py` 스크립트 사용 |
| `코스닥 상장 기업 and Top(매출액, N)` 불가 | 시장필터 + Top() 조합 불가 | 조건식으로 대체: `코스닥 상장 기업 and 매출 > X` |
| `복수종목 시장데이터 일괄조회` 불가 | `삼성전자 SK하이닉스 종가 날짜` 안 됨 | 개별 종목 순차 조회 |
| `영업이익 연도비교` 불가 | `2024 영업이익 < 0 and 2023 영업이익 > 0` 안 됨 | `turnaround_screener.py` 사용 |
| `KOSDAQ`/`KOSPI` 영문 필터 불가 | 스크리닝에서 영문 시장명 안 됨 | `코스닥`/`코스피` 한글 사용 |

### 기업 발굴 + 재무 결합
```
("반도체" 관련 기업) and (매출액 영업이익)
(매출 영업이익) in ("건강기능식품" 산업 기업)
```

### 적자전환/흑자전환 스크리닝 (전용 스크립트)
```bash
python ${CLAUDE_SKILL_DIR}/scripts/turnaround_screener.py loss 5000   # 적자전환, 매출 5000억+
python ${CLAUDE_SKILL_DIR}/scripts/turnaround_screener.py profit 1000 # 흑자전환, 매출 1000억+
```
원리: `영업이익`의 연도간 비교가 API에서 불가하여 2단계 자동화 (현재 적자/흑자 추출 → 개별 2개년 조회 → 부호 전환 필터)

### ⚡ 일일 시황분석 (Daily Market Overview) - 전용 스크립트

> **이 스크립트를 반드시 사용하세요.** 시황 관련 요청 시 DocumentSearch, GetMarketIndexes 등을 개별 호출하지 마세요.
> 이 스크립트 하나가 7개 섹션(지수, 규모별, 시총 등락, 뉴스 언급, 헤드라인, 토픽, 감성)을 자동 병렬 수집합니다.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/market_overview.py "YYYY-MM-DD"
```

**트리거 예시:** "오늘 시장 어때?", "2월 27일 시황 분석해줘", "마켓 리포트 만들어줘", "장 마감 정리", "시장 동향 알려줘"

날짜를 지정하면 **7개 섹션**의 종합 시황 리포트를 자동 생성합니다:

| 섹션 | 내용 | API 소스 |
|------|------|----------|
| **시장 지수** | KOSPI/KOSDAQ/KOSPI200 시고저종, 등락률 | `GetMarketIndexes` |
| **규모별 동향** | 대형/중형/소형주 지수 비교 (강세/약세 구간) | `GetMarketIndexes` |
| **시총 상위 등락** | 매출 5조+ 대형주 중 상승 Top5/하락 Top5 | 자연어 쿼리 (병렬) |
| **뉴스 언급 상위** | 당일 경제뉴스에서 가장 많이 언급된 상장사 20개 | `DocumentAggregation` |
| **주요 뉴스** | 당일 경제뉴스 상위 10건 (제목, 감성, 관련종목) | `DocumentSearch` |
| **트렌딩 토픽** | 경제 뉴스 핫토픽 10개 (키워드, 관련종목) | `SearchTrendingTopics` / `SearchHistoricalTopics` |
| **시장 감성** | 긍정/부정/중립 뉴스 비율로 시장 분위기 판단 | `DocumentSearch` (감성 필터) |

**주말/공휴일:** 시장 데이터는 직전 거래일 기준, 뉴스/토픽은 해당 날짜 그대로 조회됩니다.

**출력 형식:** JSON → 아래 마크다운 템플릿으로 변환하여 표시

**출력 템플릿:** [references/market_overview_template.md](references/market_overview_template.md)를 읽고 그 형식(종합해석 → 지수 → 규모별 → 시총 등락 → 업종 → 뉴스 언급 → 주요 뉴스 → 토픽 → 감성)으로 변환하세요. 맨 앞에 규칙 3의 수정주가 안내를 넣습니다.

---

## Section D: 멀티스텝 분석 (핵심)

**하나의 질문에 여러 데이터 소스를 결합하는 패턴입니다. 각 단계를 순차 실행하세요.**

### 패턴 1: 뉴스 + 주가 결합 (원인분석)

**사용 상황:** "삼성전자 뉴스가 주가에 미친 영향", "주가 급변 원인", KRX 주가급변 원인분석

```
[1단계: 문서검색 - Section A]
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=5,page=1,date_from=20240601,date_to=20240630)
→ 뉴스 발생 날짜, 주요 이벤트 내용 파악

[2단계: 주가 조회 - Section B]
삼성전자 종가 거래량 2024-06-01-2024-06-30
→ 뉴스 발생일 전후 주가/거래량 변동 확인

[3단계: 분석]
※ 거래량 급증이 액면분할·증자 직후라면 수정되지 않은 거래량 때문일 수 있음 (Section B "주가 데이터 함정" 2번)
- 뉴스 발생 전 거래량 급증 → 내부자거래 의심
- 부정 뉴스에도 주가 상승 → 추가 조사 필요
- 뉴스 발생 후 급락 → 정상적 시장 반응
```

### 패턴 2: 스크리닝 + 재무 상세 (가치투자)

**사용 상황:** "저평가 우량주 찾기", "Graham 기준 스크리닝", "Buffett 스타일 투자"

```
[1단계: 스크리닝 - Section C]
매출 > 1000000000000 and 영업이익 / 매출 > 0.1 and 당기순이익 > 0
→ 60개 우량 기업 리스트 추출

[2단계: 밸류에이션 확인 - Section B]
SK하이닉스 PER
SK하이닉스 PBR
→ PER < 15, PBR < 1.5, PER × PBR < 22.5 기준 충족 여부 확인

[3단계: 최종 선별]
조건 충족 기업만 필터하여 최종 추천 목록 작성
```

### 패턴 3: 스크리닝 + 주가 (포트폴리오 시뮬레이션)

**사용 상황:** "이 전략으로 투자했으면 수익률이 얼마?", "백테스트"

```
[1단계: 기업 선정 - Section C]
매출 > 1000000000000 and 영업이익 / 매출 > 0.15
→ 기업 리스트 추출 (KRX 종목코드 확인)

[2단계: 주가 조회 - Section B]
SK하이닉스 종가 2024-01-02-2024-01-02
SK하이닉스 종가 2024-12-30-2024-12-30
삼양식품 종가 2024-01-02-2024-01-02
삼양식품 종가 2024-12-30-2024-12-30
→ 연초/연말 종가 확보

[3단계: 수익률 계산]
(종가_연말 - 종가_연초) / 종가_연초 × 100 = 수익률(%)
→ 개별 + 평균 포트폴리오 수익률 산출
→ 종가가 수정주가라 분할·증자가 있어도 수익률은 맞음. 단 배당 제외 가격수익률임을 결과에 명시 (규칙 3)
→ 2020년 이전 시점이 들어가면 자연어 대신 GetStockPrices 사용
```

### 패턴 4: 감성분석 + 주가 (이상거래 감지)

**사용 상황:** KRX 이상거래 감시, "감성 변화와 주가 괴리"

```
[1단계: 감성 추이 - Section A]
GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)
→ 일별 감성 점수 (trend, 긍정/부정 건수)

[2단계: 주가 조회 - Section B]
삼성전자 종가 거래량 2025-02-14-2025-02-28
→ 동일 기간 주가/거래량

[3단계: 괴리 분석]
- 감성 급락 + 주가 상승 → 이상거래 의심
- 감성 급등 + 주가 하락 → 추가 조사
- 감성↔주가 동조 → 정상적 시장 반응
```

### 패턴 5: 뉴스 트렌드 + 기업 스크리닝 (테마 투자)

**사용 상황:** "AI 테마 주목 기업 + 재무 건전성", "뉴스에서 뜨는 테마의 실제 수혜 기업"

```
[1단계: 트렌드 확인 - Section A]
DocumentTrends(["news"],["economy"],"AI and 반도체",interval="1M",date_from=20240101,date_to=20241231)
→ 뉴스 트렌드 확인 (어느 시기에 화제였는지)

[2단계: 관련 기업 + 재무 - Section C]
("AI" 관련 기업) and (매출액 영업이익)
→ AI 관련 기업의 재무 현황

[3단계: 우량 기업 필터 - Section C]
("AI" 관련 기업) and 매출 > 100000000000 and 영업이익 > 0
→ 실질적으로 매출과 이익이 있는 기업만 선별
```

### 패턴 6: IPO Peer 비교 분석 (비상장사 상장 심사)

**사용 상황:** "채비 IPO 시 주요 재무 확인", "비상장사 동종업종 상장사와 비교", "상장 적정성 판단"

```
[1단계: 기업 프로필 확인 - Section B]
GetCompanySummary(채비)
→ 업종(전기차 충전기 제조), 업종코드, 설립일, 외감여부 확인

[2단계: 동종업종 Peer 후보 탐색 - Section A]
DocumentSearch(["news"],[],"전기차 충전기 제조 상장 IPO",count=20,page=1)
→ 뉴스에서 동종업종 최근 상장사 후보 파악

[3단계: Peer사 재무 조회 - Section B → GetFinancialStatements 사용]
GetFinancialStatements(에스트래픽, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(그리드위즈, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(위츠, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)

[4단계: 대상 기업 + Peer 세부 계정 비교 - Section B → GetFinancialStatements 사용]
GetFinancialStatements(채비, consolidated=False, date_from=2020-01-01, date_to=2024-12-31)
→ 반환된 507개 항목에서 매출원가, 매출총이익, 재고자산, 매출채권 등 필터링
→ 매출총이익률, 원가율, 자본잠식 여부, 차입금의존도 등 산출

[5단계: 종합 판단]
- 매출총이익률: 채비(3%) vs Peer 평균(19%) → 원가 구조 우려
- 자본잠식: 2023년 -958억 → 2024년 +968억 (유상증자)
- 유형자산 효율: 1,312억 투자 대비 매출 850억 (선투자 모델)
- 영업CF 적자 지속: 3년 연속 (-163→-371→-119억)
```

### 패턴 7: 공시 vs 뉴스 교차검증 (KRX 불공정거래 감지)

**사용 상황:** "미공개정보 이용 의심", "공시 전 뉴스 유출 확인"

```
[1단계: 뉴스 검색 - Section A]
DocumentSearch(["news"],[],\"title:(인수 or 합병) and securities.name:대상기업\",count=100,page=1,date_from=20250101,date_to=20250228)
→ 뉴스 보도 시점 파악

[2단계: 공시 검색 - Section A]
DocumentSearch(["company"],["disclosure"],"인수 or 합병",count=100,page=1,date_from=20250101,date_to=20250228)
→ 공시 시점 파악

[3단계: 시점 비교]
- 뉴스가 공시보다 앞서면 → 미공개정보 이용 의심
- 공시 후 뉴스 → 정상적 보도
```

---

## 실행

```bash
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "쿼리"                        # 기본
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "쿼리" --out result.json        # 전체 결과를 파일로
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "DocumentSearch(...)" --max-pages 3   # 페이지 더 받기
python ${CLAUDE_SKILL_DIR}/scripts/query_api.py "GetFinancialStatements(...)" --grep '^(수익|영업이익\(손실\))$'  # 계정 필터
```

- 결과 형식: DocumentSearch는 `total_matches`, `windows`, `docs[]`(title, publisher, created_at, content 300자, content_url, securities, polarity, esg). DataFrame 결과(재무·주가·스크리닝)는 `columns`, `row_count`, `rows[]`(행 단위 dict).
- 출력에 `saved_to`가 있으면 전체 결과가 그 파일에 있습니다.
- 멀티스텝 분석은 단계별로 위 스크립트를 순차 호출하세요.

### 대량 반복 조회 시 사용자 확인 필수

특정 계정을 전체 상장사(또는 업종 전체)에 대해 조회하는 경우, **개별 기업마다 API를 호출**해야 합니다.
이런 경우 반드시 사용자에게 **예상 API 호출 수와 소요 시간을 안내**하고 진행 여부를 확인받으세요.

**안내 문구 예시:**
> "전체 코스피 상장사(약 2,400개)의 미청구공사를 조회하려면 약 2,400건의 API를 개별 호출해야 합니다.
> 병렬 처리(10건 동시)로 약 4~8분이 소요될 수 있습니다. 진행할까요?
> 건설업만 필터하면 약 50~100건으로 줄일 수 있습니다."

**대량조회 판단 기준:**
| 조회 대상 | 예상 API 호출 | 확인 필요 |
|----------|-------------|----------|
| 단일 기업 세부계정 | 1건 | 불필요 |
| 5~10개 기업 | 5~10건 | 불필요 |
| 특정 업종 전체 (50~200개) | 50~200건 | **확인 권장** |
| 코스닥/코스피 전체 (1,800~2,400개) | 1,800~2,400건 | **반드시 확인** |

**대안 제시:**
- 스크리닝 조건으로 대상 기업 수를 먼저 줄이기: `코스닥 상장 기업 and 매출 > 100000000000`
- 업종 키워드로 필터: `"건설" 산업 기업` → 건설업만 추출 후 개별 조회
- `market_top_movers.py` 같은 전용 스크립트 사용 (병렬 처리 내장)

## 결과 포맷팅

### 데이터 출처 표기 (필수)

**모든 결과 하단에 출처를 반드시 표기하세요.** 사용자가 데이터의 신뢰성을 즉시 확인할 수 있어야 합니다.

```
📌 데이터 출처: NICE평가정보 재무데이터 | KRX 한국거래소 시장데이터
```

데이터 유형별 표기:
| 조회 내용 | 출처 표기 |
|----------|----------|
| 재무제표 (매출, 이익, 자산 등) | `NICE평가정보 재무데이터` |
| 주가·시가총액·PER 등 | `KRX 한국거래소 / 코스콤 시장데이터 (주가는 수정주가)` |
| 기업개요 (설립일, 업종 등) | `NICE평가정보 기업정보` |
| 공시·IR 문서 | `금융감독원 DART 전자공시` |
| 뉴스 기사 | `국내 주요 언론사 (매일경제, 한경 등)` |
| 증권사 리포트 | `증권사 리서치센터 리포트` |
| 특허 | `특허정보원 KIPRIS` |

여러 유형의 데이터를 함께 사용한 경우 출처를 모두 나열하세요:
```
📌 데이터 출처: NICE평가정보 재무데이터 | 금융감독원 DART 전자공시 | 국내 주요 언론사
```

### 결과 형식

**문서 검색:**
```
## 검색 결과 (총 N건)
### 1. [제목]
- 출처: [언론사] | 날짜: YYYY-MM-DD | 감성: 긍정/부정
- 관련종목: 기업명(종목코드)

📌 데이터 출처: 국내 주요 언론사 (매일경제, 한경 등)
```

**재무/주가:**
표 형식, 금액은 억/조 단위 변환 + 하단에 출처 표기

**스크리닝:**
| 기업명 | 종목코드 | 매출액 | 영업이익률 | 형식 + 하단에 출처 표기

**멀티스텝 분석:**
각 단계 결과를 요약하고 → 최종 종합 분석/인사이트 제시 + 사용된 전체 데이터 출처 표기

### 후속 분석 제안 (필수)

**모든 답변 끝에 관련된 후속 분석을 제안하세요.** 사용자가 다음으로 확인하면 좋을 내용을 안내합니다.

아래 상황별 제안 템플릿을 따르세요:

**뉴스 검색 결과를 보여준 후:**
> 추가로 검토해드릴 수 있는 내용입니다:
> - 특정 종목의 **최근 공시(DART)**나 **IR 자료**를 확인해드릴까요?
> - 해당 종목의 **애널리스트 보고서**를 조회해드릴까요?
> - 특정 기사나 보고서의 **전체 본문**을 읽어서 상세 내용을 알려드릴까요?
> - 해당 종목의 **최근 주가 흐름**을 함께 보여드릴까요?
> - **이슈 카테고리별** (계약/수주, 인수/투자, 실적, 소송/부도 등)로 분류해드릴까요?

**기업 재무 조회 후:**
> 추가로 검토해드릴 수 있는 내용입니다:
> - 이 기업의 **최근 뉴스**에서 실적 관련 이슈를 확인해드릴까요?
> - **동종업종 Peer 비교** (매출/이익률/자본구조)를 해드릴까요?
> - **세부 재무계정** (재고자산, 매출채권, 차입금, 현금흐름 등)을 더 살펴볼까요?
> - **공시 내역**이나 **애널리스트 목표가**를 조회해드릴까요?
> - 최근 **애널리스트 보고서 본문**에서 투자 의견과 근거를 확인해드릴까요?

**주가 조회 후:**
> 추가로 검토해드릴 수 있는 내용입니다:
> - 이 기간의 **뉴스/공시**에서 주가 변동 원인을 분석해드릴까요?
> - **감성 분석**(긍부정 추이)과 주가를 비교해드릴까요?
> - **거래량 급변** 구간의 관련 뉴스를 찾아드릴까요?
> - 해당 날짜의 **전체 시황분석 리포트**를 생성해드릴까요?

**스크리닝 결과 후:**
> 추가로 검토해드릴 수 있는 내용입니다:
> - 특정 기업의 **상세 재무**를 더 살펴볼까요?
> - 이 기업들의 **최근 뉴스 동향**을 확인해드릴까요?
> - **주가 수익률 시뮬레이션**을 해볼까요?

## 이 스킬에 예시가 없는 DeepSearch 기능

아래 함수는 이 레포의 API 키로 동작을 확인했습니다(2026-11-25). 호출 형식은 레포 `docs/reference/DEEPSEARCH_API_MASTER.md`(17절에 전체 함수표와 호출 결과)에 있습니다. 사용자가 요청하면 `query_api.py`로 바로 호출하세요.

| 분야 | 함수 | 용도 |
|---|---|---|
| 기업 정보 | `GetCompanyHistory`, `GetCompanyBusinessSummary`, `GetCompanyRelatedFirms`, `GetCompanyDebts`, `GetCompanyBranches`, `GetCompanyProductsSales`, `GetFinancialStatementsAuditOpinion` | 연혁, 사업 요약, 관계사, 차입금, 사업장, 제품별 매출, 감사의견 |
| 공시(DART 정기보고서) | `GetDartDividends`, `GetDartShareRepurchase`, `GetDartMajorityShareholders`, `GetDartMajorityShareholderChange`, `GetDartMinorityShareholders`, `GetDartExecutives`, `GetDartEmployees`, `GetDartIndividualDirectorCompensation`, `GetDartOverallDirectorCompensation`, `GetDartTopIndividualCompensation`, `GetDartInvestmentInOthers` | 배당, 자사주, 최대주주·변동, 소액주주, 임직원, 임원 보수, 타법인 출자 |
| 컨센서스·이슈 | `GetConsensusInstitutionList`, `GetConsensusAnalystList(inst_code)`, `SearchFirmFundamentalsForecasts`, `GetTargetPriceConsensusChange`, `GetCompanyShareholderChanges` | 증권사·애널리스트, 실적 전망, 목표가 변화, 주주 변동 기업 |
| 주가·지수 | `GetStockPrices`, `GetStockSymbols`, `GetMarketIndexes`, `GetMarketIndexSymbols` | 2020년 이전 주가, 지수 (규칙 3 수정주가 안내) |
| 기업 주제·집단 | `GetEntityTags`, `FindEntityByTag`, `GetConditionalTagMetadata`, `FindConglomerateByID`, `GetConglomerateFinancialStatements` | 테마 태그, 그룹 재무 |
| 인물 | `FindPersonBio(name, birthday)` | 인물 경력 |
| 이벤트 | `ComputePortfolioReturns`, `ComputeEventDayStockReturns` | 포트폴리오 수익률, 이벤트일 종목 수익률 |
| 경제지표 | 한국은행 `QueryBankOfKoreaSeries*`, FRED `QueryFredSeries*`, IMF `GetImf*`, OECD `GetOecd*`, World Bank `QueryWorldBank*`, 딥서치 자체 `QueryDeepSearchOwn*` (시리즈 검색 `FindEntity("DataSeries", "검색어")`) | 거시 지표. **기간을 꼭 지정**하세요(전체 시계열은 수 MB) |
| 토픽 인사이트 (REST) | `query_api.py "/v1/topic-insight/insight?type=trending&section=economy&topicId={uid}&stream=false"` | 토픽 요약·질문. `topicId`는 `SearchTrendingTopics` 결과의 `uid` |

**쓰지 마세요** (현재 구독으로 안 되거나 고장, 2026-11-25 확인):
- 미제공(`NameError: UFunction ... is not defined`): 채권 함수 전부, 통계청(KOSIS) 전부, 채권 이벤트, `GetDartCapitalChange`, `GetFundamentalsConsensusChange`, `GetAggregateIndustryInfo`, `GetAggregateIndustryConsensus`, `SearchFinancialStatementsAuditOpinion`
- 서버 오류·타임아웃: `GetMarketSummaryInfoByIndustry`·`GetIndustryReturnsOnEventDates`·`GetCumulativeIndustryReturns`(`KeyError: industry_id`), `AnalyzePortfolioReturns`(AttributeError), `FindPeopleByBirthday`·`FindRichestShareholders`·`ComputeStockReturnCorrelationWith`(타임아웃), `SearchAnalystReports`(500 → 애널리스트 보고서는 `DocumentSearch(["research"],["company"],...)`)
- compute 밖 API: DeepSearch v2 REST(`api-v2.deepsearch.com`), 해외기업(`/v2/companies`), 챗딥서치(`/note/v1`) — 이 키로 401

**fallback 응답:**
> "이 요청은 현재 DeepSearch 구독으로 조회할 수 없습니다(`{함수명}`: {이유}). 대신 {대안}으로 확인할 수 있습니다."
> 대안이 없으면 그렇다고 말하고, OpenDART 등 다른 출처를 제안하세요.

## Resources

API 레퍼런스: [references/api_quick_reference.md](references/api_quick_reference.md)
검증된 사용 사례: [references/verified_examples.md](references/verified_examples.md)
KRX 업무 가이드: [references/krx_monitoring_guide.md](references/krx_monitoring_guide.md)
가치투자 방법론: [references/value_investing.md](references/value_investing.md)
