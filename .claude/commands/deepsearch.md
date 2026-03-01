# DeepSearch 통합 분석

문서검색, 기업/재무 데이터, 스크리닝/분석을 통합 처리합니다.
**여러 데이터 소스를 연결하는 멀티스텝 분석에 특화**되어 있습니다.

## 사용자 요청

$ARGUMENTS

## API 키

`.env` 파일에서 `API_KEY`를 읽어 사용하세요:
```bash
source .env && echo $API_KEY
```

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
**제한:** DocumentSearch 최대 1년, 초과 시 6개월 분할

**KRX 패턴:**
- 조회공시 → `title:(인수 or 합병 or 매각) and securities.market:(KOSPI or KOSDAQ)`
- 부정 뉴스 → `securities.market:KOSPI and polarity.name:부정`
- ESG 이슈 → `esg.category.name:지배구조 and esg.polarity.name:부정`

**실행:** `python deepsearch/scripts/query_api.py "$API_KEY" "쿼리"`

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
**❌ 기업명에 따옴표 금지:** `GetFinancialStatements("삼성전자")` → 403 오류

### 주가/시장 데이터 → 자연어 쿼리 OK
```
삼성전자 종가 2024-06-01-2024-06-30
삼성전자 PER
삼성전자 PBR
삼성전자 시가총액 2024-01-01-2024-12-31
```

### API 함수
```
FindEntity("Financial","삼성*")
GetCompanySummary("삼성전자")
GetCompanyDividends("삼성전자",date_from=20200101,date_to=20241231)
SearchTargetPrices("005930",date_from=20240101,date_to=20241231)
FindConglomerateByName("삼성")
FindPeopleByName("이재용")
```

**기업 검색:** `"반도체" 관련 기업`, `"건강기능식품" 산업 기업`, `상장 기업`, `"국민연금" 주주 기업`

**실행:** `python deepsearch/scripts/query_api.py "$API_KEY" "쿼리"`

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
python deepsearch/scripts/turnaround_screener.py "$API_KEY" loss 5000
python deepsearch/scripts/turnaround_screener.py "$API_KEY" profit 1000
python deepsearch/scripts/market_top_movers.py "$API_KEY" kosdaq 150 2025-02-27
```

**실행:** `python deepsearch/scripts/query_api.py "$API_KEY" "쿼리"`

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
- API 레퍼런스: `deepsearch/references/api_quick_reference.md`
- 검증된 사례: `deepsearch/references/verified_examples.md`
- KRX 업무 가이드: `deepsearch/references/krx_monitoring_guide.md`
- 가치투자 방법론: `deepsearch/references/value_investing.md`
