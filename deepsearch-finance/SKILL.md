---
name: deepsearch-finance
description: "DeepSearch API로 한국 상장기업 정보, 재무제표, 주가, 컨센서스를 조회합니다."
---

# DeepSearch 기업 & 재무 데이터 스킬

한국 상장기업 정보, 재무제표, 주가/시장 데이터를 조회합니다.

## Prerequisites

사용자에게 DeepSearch API 키를 요청하세요.

## 지원 기능

### A. 재무제표 조회 (GetFinancialStatements 필수)
매출, 영업이익, 당기순이익, 자산, 부채, 자본 등 **모든 재무제표 항목**은 반드시 GetFinancialStatements API 함수로 조회합니다.
**❌ 자연어 쿼리 금지:** `삼성전자 매출액 2020-2024` → KeyError 발생 가능

### B. 주가/시장 데이터 (자연어 쿼리 OK)
종가, 시가, 고가, 저가, 시가총액, 거래량, PER, PBR, EPS, BPS, DPS

### C. 기업 개요 (자연어 쿼리 OK)
대표이사, 종업원수, 설립일, 주거래은행, 산업분류, 홈페이지

### D. API 함수
- **GetFinancialStatements** - 재무제표 (최우선 사용)
- **GetAvailableFinancialStatements** - 조회 가능 재무제표 확인
- FindEntity - 기업 검색
- GetCompanySummary - 기업 개요
- GetCompanyDividends - 배당 정보
- GetCompanyShareholders - 주주 정보
- GetCompanyExecutives - 임원 정보
- SearchTargetPrices - 애널리스트 목표가
- SearchFirmFundamentalsForecasts - 실적 전망치
- FindConglomerateByName - 기업그룹 검색
- GetConglomerateMembers - 계열사 조회
- FindPeopleByName - 인물 검색

## Instructions

### Step 1: 쿼리 유형 결정

**재무제표 조회 (GetFinancialStatements 필수):**
```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE코드 또는 KRX코드)

# 2단계: 재무제표 조회 (507개 계정항목 한 번에 반환)
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(삼성전자, consolidated=False)       # 별도 재무제표
GetFinancialStatements(삼성전자, report_ids="BalanceSheet") # 특정 제표만
GetFinancialStatements(삼성전자, is_annual=False)           # 분기 포함
```
**❌ 기업명에 따옴표 금지:** `GetFinancialStatements("삼성전자")` → 403 오류

**❌ 자연어 재무 쿼리 금지 (KeyError 발생):**
```
삼성전자 매출액 2020-2024                    ← 금지
삼성전자 LG전자 매출 영업이익 2020-2024      ← 금지
SK하이닉스 분기 영업이익                      ← 금지
삼성전자 별도 분기 매출                       ← 금지
```

**주가/시장 데이터 (자연어 쿼리 OK):**
```
삼성전자 종가 2024-01-01-2024-12-31
삼성전자 PER
삼성전자 PBR
삼성전자 시가총액 2024-01-01-2024-12-31
```

**기업 입력 방법:**
- 이름: `삼성전자`, `LG전자 SK하이닉스`
- 종목코드: `KRX:005930`
- 사업자번호: `1248100998` (10자리, 대시 없이)
- 법인번호: `1301110006246` (13자리)

**API 함수 쿼리:**
```
FindEntity("Financial","삼성*")
GetCompanySummary("삼성전자")
GetCompanyDividends("삼성전자",date_from=20200101,date_to=20241231)
GetAvailableFinancialStatements(NICE:IX5118)
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
SearchTargetPrices("005930",date_from=20240101,date_to=20241231)
FindConglomerateByName("삼성")
GetConglomerateMembers("삼성")
FindPeopleByName("이재용")
```

**기업 검색 예약어:**
- `"키워드" 관련 기업` - 주제 관련
- `"키워드" 산업 기업` - 산업분류 기반
- `"키워드" 사업 기업` - 사업영역 기반
- `"키워드" 주소 기업` - 주소 기반
- `"주주명" 주주 기업` - 주주 기반
- `상장 기업`, `외감 기업`, `비외감 기업`

### Step 2: 실행

```bash
python {baseDir}/scripts/query_api.py "API_KEY" "쿼리"
```

### Step 3: 결과 포맷팅

- 재무 데이터 → 표 형식, 금액은 억/조 단위로 변환
- 주가 데이터 → 표 또는 요약
- 기업 목록 → 기업명, 종목코드, 시장 포함

## 이 스킬이 커버하지 않는 DeepSearch 기능

이 스킬은 **기업 정보 & 재무/시장 데이터** 전문입니다. 아래 기능이 필요하면 다른 스킬이나 DeepSearch API 문서를 안내하세요.

**다른 스킬로 처리 가능:**
| 요청 유형 | 안내할 스킬 |
|-----------|-----------|
| 뉴스/공시/리서치 문서 검색, 감성분석, 트렌드 | **deepsearch-docs** 스킬 |
| 재무 조건 스크리닝, 투자 전략, Top/Bottom 분석 | **deepsearch-analytics** 스킬 |

**DeepSearch API에는 있으나 현재 스킬에 미포함:**
| API 함수 | 설명 | 용도 예시 |
|---------|------|----------|
| GetCompanyHistory | 기업 연혁 | "삼성전자 설립 이후 주요 연혁" |
| GetCompanyBusinessGoal | 사업 목적 (정관) | "삼성전자 정관상 사업 목적" |
| GetCompanyBusinessSummary | 사업 요약 | "삼성전자 사업 내용 요약" |
| GetCompanyRelatedFirms | 관계사 정보 | "삼성전자의 자회사/관계사 목록" |
| GetCompanyDebts | 차입금 정보 | "삼성전자 차입금 상세 현황" |
| GetCompanyEmployees | 종업원 정보 | "삼성전자 종업원 수 추이" |
| GetCompanyBranches | 사업장 정보 | "삼성전자 사업장 위치 목록" |
| GetConglomerateFinancialStatements | 그룹 재무제표 | "삼성그룹 전체 재무제표" |
| GetConsensusInstitutionList | 증권사 목록 | "컨센서스 제공 증권사 리스트" |
| GetConsensusAnalystList | 애널리스트 목록 | "특정 증권사 소속 애널리스트" |
| SearchAnalystReports | 애널리스트 리포트 | "특정 애널리스트의 리포트 이력" |
| FindPersonBio | 인물 경력 조회 | "이재용 경력 및 약력" |
| FindPeopleByBirthday | 생일 기반 인물 검색 | "특정 생년월일 인물 검색" |
| FindRichestShareholders | 주식 부자 순위 | "보유 주식 가치 상위 인물" |
| GetAggregateIndustryInfo | 산업별 집계 | "반도체 산업 전체 매출 합계" |
| GetAggregateIndustryConsensus | 산업별 컨센서스 | "반도체 산업 실적 전망" |
| GetMarketSummaryInfoByIndustry | 산업별 시장 요약 | "산업별 시가총액, PER 비교" |

**fallback 응답 템플릿:**
사용자 질문이 이 스킬의 범위 밖이지만 DeepSearch API로 가능한 경우:
> "이 요청은 제가 현재 학습한 기업/재무 스킬의 범위 밖입니다. 하지만 DeepSearch API의 `{함수명}` 기능으로 처리할 수 있습니다.
> - 관련 API 문서: DeepSearch API 마스터 가이드 (docs/DEEPSEARCH_API_MASTER.md)
> - 추가 스킬이 필요하시면 해당 기능을 포함한 스킬을 생성할 수 있습니다."

## Resources

상세 레퍼런스: [{baseDir}/references/finance_guide.md](references/finance_guide.md)
검증된 사용 사례: [{baseDir}/references/verified_examples.md](references/verified_examples.md)
