# DeepSearch 통합 분석

문서검색, 기업/재무 데이터, 스크리닝/분석을 통합 처리합니다.
**여러 데이터 소스를 연결하는 멀티스텝 분석에 특화**되어 있습니다.

## 사용자 요청

$ARGUMENTS

## 먼저 읽기

- 이 커맨드는 `skills/deepsearch/SKILL.md`의 요약입니다. 규칙이 다르면 SKILL.md가 맞습니다.
- **API 키:** 스크립트가 환경변수 `DEEPSEARCH_API_KEY`/`API_KEY` 또는 레포 루트 `.env`에서 직접 읽습니다. 키를 명령에 넣거나 `.env`를 출력하지 마세요. 없으면 사용자에게 한 번만 요청해 `.env`에 `API_KEY=<키>`로 저장하세요.
- **실행:** `python skills/deepsearch/scripts/query_api.py "쿼리"` (옵션: `--out 파일`, `--max-pages N`, `--grep 정규식`)
- **큰 결과:** 2만 자가 넘으면 임시 파일로 저장되고 `saved_to`와 미리보기만 출력됩니다. 그 파일을 Python으로 읽어 필요한 부분만 쓰세요.
- **여러 회사·종목은 한 번에:** `GetFinancialStatements([A, B, ...])`(50개씩), `GetStockPrices([...])`. `GetStockPrices`는 종목을 생략하면 전 종목의 마지막 거래일 시세. `change_rate`는 종목은 비율, 지수는 퍼센트.
- **쓸 수 있는 함수:** `docs/reference/DEEPSEARCH_API_MASTER.md` 17절(호출 결과 표). 채권·통계청 함수, v2 REST, 해외기업, 챗딥서치는 현재 구독으로 쓸 수 없습니다.

## 쿼리 라우팅

사용자 요청을 분석하여 적절한 유형으로 처리하세요:

| 요청 유형 | 판단 기준 | 처리 섹션 |
|-----------|----------|----------|
| **문서 검색** | 뉴스, 리포트, 공시, 트렌드, 감성분석 | Section A |
| **기업/재무** | 매출, 주가, PER, 배당, 임원 | Section B |
| **스크리닝** | 조건 필터, Top/Bottom, 전략 | Section C |
| **멀티스텝** | 위 유형 2개 이상 결합 | Section D |

---

## Section A: 문서 검색

**쿼리 형식:**
```
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=100,page=1,date_from=20240601,date_to=20240630)
DocumentTrends(["news"],["economy"],"AI",interval="1M",date_from=20240101,date_to=20241231)
DocumentAggregation(["news"],[],"전기차","securities.name:10",date_from=20240101,date_to=20240630)
GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)
SimilarKeywords("반도체",max_count=5)
```

**카테고리:** `["news"]`, `["research"]`, `["company"]`, `["patent"]`
**필드:** `securities.name:`, `securities.market:`, `polarity.name:`, `esg.category.name:`, `title:`, `publisher.raw:`
**제한:** DocumentSearch 기간 최대 1년(초과 시 HTTP 413). `query_api.py`가 1년 단위로 자동 분할·중복 제거합니다.

**KRX 패턴:**
- 조회공시 → `title:(인수 or 합병 or 매각) and securities.market:(KOSPI or KOSDAQ)`
- 부정 뉴스 → `securities.market:KOSPI and polarity.name:부정`
- ESG 이슈 → `esg.category.name:지배구조 and esg.polarity.name:부정`

**실행:** `python skills/deepsearch/scripts/query_api.py "쿼리"`

---

## Section B: 기업 & 재무/시장 데이터

### ⚠️ 재무제표 → GetFinancialStatements 필수 (자연어 쿼리 금지)

매출, 영업이익, 당기순이익, 자산, 부채, 자본 등 **모든 재무제표 항목**:
```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE코드)

# 2단계: 재무제표 조회
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(삼성전자, consolidated=False)       # 별도 재무제표
GetFinancialStatements(삼성전자, report_ids="BalanceSheet") # 특정 제표만
```
**❌ 금지:** `삼성전자 매출액 2020-2024`, `기업명 영업이익 2020-2024` (KeyError 발생)
- 기업명은 따옴표 없이 씁니다.
- **계정명(`name_ko`):** 매출액 = `수익`, 영업이익 = `영업이익(손실)`, 당기순이익 = `총당기순이익`, `자산총계`·`부채총계`·`자본총계`. 필요한 계정만 거르세요:
  `python skills/deepsearch/scripts/query_api.py 'GetFinancialStatements(삼성전자, consolidated=True, date_from=2020-01-01, date_to=2024-12-31)' --grep '^(수익|영업이익\(손실\)|총당기순이익)$'`
- 과거 연도 값은 원래값·재작성값이 섞여 있고, 시장데이터 BPS·EPS에는 look-ahead가 있습니다(SKILL.md 규칙 4).

### 주가/시장 데이터 → 자연어 쿼리 OK
```
삼성전자 종가 2024-06-01-2024-06-30
삼성전자 PER
삼성전자 PBR
삼성전자 시가총액 2024-01-01-2024-12-31
```

**⚠️ 주가 기준: 답변에서 데이터보다 먼저 안내할 것** (상세: `skills/deepsearch/SKILL.md` 규칙 3과 "주가 데이터 함정", 근거: `research/price_adjustment/README.md`)
- 시가·고가·저가·종가는 **수정주가뿐**입니다(액면분할·무상증자·유상증자 소급 반영, 배당 미반영). 원주가 옵션은 없고, `adjusted=` 같은 파라미터나 `adj_close` 같은 컬럼은 400 에러입니다.
- 거래량·거래대금·주식수·시가총액은 **수정되지 않은 당일 값**입니다. 분할 전후 거래량은 직접 비교할 수 없습니다. 원주가 = `market_cap ÷ shares_outstanding`
- 자연어 쿼리는 **2020-01-02 이후만** 나옵니다(그 이전 범위는 오류 없이 오늘 값 1행). 2020년 이전은 `GetStockPrices(KRX:005930, columns=["close"], date_from=2018-01-02, date_to=2018-12-28)`를 쓰세요.

### API 함수
```
FindEntity("Financial","삼성*")
GetCompanySummary("삼성전자")
GetCompanyDividends("삼성전자",date_from=20200101,date_to=20241231)
SearchTargetPrices("005930",date_from=20240101,date_to=20241231)
GetDartDividends(KRX:005930, date_from=2020-01-01, date_to=2024-12-31)
GetDartMajorityShareholders(KRX:005930, date_from=2024-01-01, date_to=2024-12-31)
FindConglomerateByName("삼성")
FindPeopleByName("이재용")
```

**기업 검색:** `"반도체" 관련 기업`, `"건강기능식품" 산업 기업`, `상장 기업`, `"국민연금" 주주 기업`

**실행:** `python skills/deepsearch/scripts/query_api.py "쿼리"`

---

## Section C: 스크리닝 & 분석

**스크리닝:**
```
매출 > 1000000000000 and 영업이익 / 매출 > 0.15
자본 < 0 and 매출 > 10000000000
상장 기업 and 2024 매출 < 2023 매출 * 0.7
("반도체" 관련 기업) and (매출액 영업이익)
코스닥 상장 기업 and 매출액 > 100000000000    → 코스닥 매출 1000억+ (한글 필수)
코스피 상장 기업                              → 코스피 전체
```

**분석 함수:** `Top(매출액, 10)`, `Max(삼성전자 매출액 2015-2024)`, `Mean(삼성전자 종가 2024-01-01-2024-12-31)`

**스크리닝 제한:** `Top(시가총액,N)` 불가(시장데이터), `코스닥 상장 기업 and Top()` 조합 불가, `KOSDAQ` 영문 불가→`코스닥` 한글 사용

**전용 스크립트:**
```bash
python skills/deepsearch/scripts/turnaround_screener.py loss 5000
python skills/deepsearch/scripts/turnaround_screener.py profit 1000
python skills/deepsearch/scripts/market_top_movers.py kosdaq 150 2025-02-27
```

**실행:** `python skills/deepsearch/scripts/query_api.py "쿼리"`

---

## Section D: 멀티스텝 분석 (핵심)

### 패턴 1: 뉴스 + 주가 결합 (원인분석)
```
[1단계: 문서검색]
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=5,page=1,date_from=20240601,date_to=20240630)
→ 뉴스 이벤트 날짜 파악

[2단계: 주가 조회]
삼성전자 종가 거래량 2024-06-01-2024-06-30
→ 뉴스 전후 주가/거래량 변동 확인

[3단계: 분석]
※ 분할·증자 직후 거래량 급증은 미수정 거래량 때문일 수 있음
뉴스 발생 전 거래량 급증 → 내부자거래 의심
부정 뉴스 + 주가 상승 → 추가 조사
```

### 패턴 2: 스크리닝 + 밸류에이션 (가치투자)
```
[1단계: 스크리닝]
매출 > 1000000000000 and 영업이익 / 매출 > 0.1 and 당기순이익 > 0
→ 우량 기업 리스트

[2단계: PER/PBR 확인]
SK하이닉스 PER
SK하이닉스 PBR
→ PER < 15, PBR < 1.5 충족 여부
```

### 패턴 3: 스크리닝 + 주가 (포트폴리오)
```
[1단계: 기업 선정]
매출 > 1조 and 영업이익률 > 15%

[2단계: 종가 조회]
SK하이닉스 종가 2024-01-02-2024-01-02
SK하이닉스 종가 2024-12-30-2024-12-30

[3단계: 수익률]
(연말-연초)/연초 × 100
→ 배당 제외 가격수익률임을 명시
```

### 패턴 4: 감성 + 주가 (이상거래 감지)
```
[1단계: 감성]
GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)

[2단계: 주가]
삼성전자 종가 거래량 2025-02-14-2025-02-28

[3단계: 괴리 분석]
감성 급락 + 주가 상승 → 이상거래 의심
```

### 패턴 5: 트렌드 + 기업 스크리닝 (테마투자)
```
[1단계: 트렌드]
DocumentTrends(["news"],["economy"],"AI and 반도체",interval="1M",date_from=20240101,date_to=20241231)

[2단계: 관련 기업]
("AI" 관련 기업) and (매출액 영업이익)

[3단계: 우량 필터]
("AI" 관련 기업) and 매출 > 100000000000 and 영업이익 > 0
```

### 패턴 6: 공시 vs 뉴스 교차검증 (미공개정보)
```
[1단계: 뉴스]
DocumentSearch(["news"],[],"title:(인수 or 합병) and securities.name:대상기업",...)

[2단계: 공시]
DocumentSearch(["company"],["disclosure"],"인수 or 합병",...)

[3단계: 시점 비교]
뉴스가 공시보다 앞서면 → 미공개정보 이용 의심
```

---

## 참조 파일

쿼리 작성 시 아래 파일을 참조하세요:
- API 레퍼런스: `skills/deepsearch/references/api_quick_reference.md`
- 검증된 사례: `skills/deepsearch/references/verified_examples.md`
- KRX 업무 가이드: `skills/deepsearch/references/krx_monitoring_guide.md`
- 가치투자 방법론: `skills/deepsearch/references/value_investing.md`
