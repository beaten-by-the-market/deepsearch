# DeepSearch API Master Reference

DeepSearch compute API의 함수와 사용법을 한 문서로 요약한 레퍼런스입니다. 함수별 상세(파라미터 표·예시·결과)는 같은 폴더의 원문 파일을 보세요([README.md](README.md)).

- 원문: DeepSearch 가이드 https://help.deepsearch.com/dp (2026-11-25 동기화)
- **호출 결과** 열과 ⚠️ 표시는 이 레포의 API 키(현재 구독)로 2026-11-25에 직접 호출해 본 결과입니다. 공식 문서 내용이 아닙니다.
- 현재 구독으로 쓸 수 없는 API(v2 REST, 해외기업, 챗딥서치)는 [16절](#16-현재-구독으로-쓸-수-없는-api)에 따로 적었고 본문에는 넣지 않았습니다.

---

## 1. API 기본 정보

### API 호출 주소
```
https://api.deepsearch.com/v1/compute?input={쿼리}
https://app-api.deepsearch.com/v1/compute?input={쿼리}     ← 공식 가이드가 현재 안내하는 주소
```
두 주소 모두 같은 키로 같은 결과를 돌려줍니다(2026-11-25 확인).

### 인증 방식
- HTTP 헤더에 `Authorization: Basic {인증키}` 추가 (`{인증키}` = `id:secret`의 base64)
- GET과 POST 모두 지원. 쿼리가 길거나 특수문자가 많으면 POST가 안전합니다.
  - GET: `input`을 `urllib.parse.quote(query, safe="")`로 인코딩 (`&` 등이 깨지지 않게)
  - POST: 본문 `{"input": "쿼리"}`(JSON) 또는 `input=쿼리`(form) — 둘 다 확인

### curl 예제
```bash
curl -H 'Authorization: Basic {인증키}' -XGET 'https://api.deepsearch.com/v1/compute?input={쿼리}'
curl -H 'Authorization: Basic {인증키}' -H 'Content-Type: application/json' \
     -d '{"input": "삼성전자 종가 2024-06-03-2024-06-04"}' https://api.deepsearch.com/v1/compute
```

### 에러 확인
- 에러 원인은 응답 본문의 `data.exceptions[]`에 있습니다. HTTP 200이어도 올 수 있고, 400·413 같은 4xx 본문에도 들어 있습니다.
  - 없는 함수: `NameError: UFunction 'X' is not defined` (HTTP 400)
  - DocumentSearch 1년 초과: `RequestEntityTooLarge: Not allowed to search more than 1 year if not logged in` (HTTP 413)

---

## 2. 데이터 조회 방법

### 2.1 쿼리 형태의 데이터 조회

기본 구조: `기업 + 속성 + 기간`

```
삼성전자 주가 2020-01-01-2020-12-31
삼성전자 PER
삼성전자 시가총액
```

> **⚠️ 참고:** 재무제표 항목(매출액, 영업이익, 당기순이익, 자산, 부채, 자본 등)은 자연어 쿼리보다 `GetFinancialStatements` 함수([7.1절](#71-getfinancialstatements))가 더 안정적입니다. 자연어 재무 쿼리(`삼성전자 매출액 2020-2024`)는 KeyError가 발생할 수 있으므로, 주가/시장 데이터(종가, PER, PBR, 시가총액 등)에만 자연어 쿼리를 사용하세요.
>
> **⚠️ 자연어 주가 쿼리는 2020-01-02 이후만 나옵니다.** 그 이전 범위는 오류 없이 오늘 값 1행을 돌려줍니다. 과거 주가는 `GetStockPrices`([7.6절](#76-주가지수))를 쓰세요.

### 2.2 기업 입력 방법

| 구분 | 형식 | 예시 |
|------|------|------|
| 이름 | 기업1 기업2 | LG전자 삼성전자 넷마블 |
| Symbol | KRX:종목코드 | KRX:005930 KRX:000660 |
| 사업자번호 | 10자리숫자 | 1248100998 |
| 법인번호 | 13자리숫자 | 1301110006246 |

### 2.3 기업 검색 예약어

| 검색 유형 | 쿼리 형식 | 예시 |
|----------|----------|------|
| 관련 기업 | "키워드" 관련 기업 | "전기차" 관련 기업 |
| 뉴스 기업 | "키워드" 뉴스 기업 | "갑질" 뉴스 기업 |
| 주주 기업 | "주주명" 주주 기업 | "국민연금" 주주 기업 |
| 산업 기업 | "산업명" 산업 기업 | "건강기능식품" 산업 기업 |
| 사업 기업 | "사업명" 사업 기업 | "웹툰" 사업 기업 |
| 주소 기업 | "주소" 주소 기업 | "서울 마포구" 주소 기업 |
| 이름 기업 | "이름" 이름 기업 | "자산운용" 이름 기업 |
| 상장 기업 | 상장 기업 | 상장 기업 |
| 외감 기업 | 외감 기업 / 비외감 기업 | 외감 기업 |
| 폐업 기업 | 폐업 기업 | 폐업 기업 |

### 2.4 데이터 조회 결합

```
// and 연산자 사용
("건강기능식품" 산업 기업) and (매출 영업이익 당기순이익)

// in 연산자 사용
(매출 영업이익 당기순이익) in ("건강기능식품" 산업 기업)

// 복합 조건
"전기차" 관련 기업 and "자율주행" 관련 기업 and 매출액 > 10000000000
```

---

## 3. 연산 함수

| 함수 | 설명 | 예시 |
|------|------|------|
| Max() | 최대값 | Max(삼성전자 매출액 2010-2018) |
| Min() | 최소값 | Min(LG전자 영업이익 2010-2018) |
| Abs() | 절대값 | Abs(영업이익 < 0) |
| Mean() | 평균 | Mean(삼성전자 2018 주가) |
| Sum() | 합계 | Sum(Select(비트코인 관련 기업 and 2017 매출액, 1)) |
| Top() | 상위 N개 | Top(dps/주가, 10) |
| Bottom() | 하위 N개 | Bottom(시가총액, 10) |
| Rank() | 순위 | Rank(토지) |
| Sort() | 정렬 | Sort(매출액 > 1000000000, ascending=False) |
| Select() | 특정 컬럼 선택 | Select(반도체 관련 기업 and 시가총액, [1,2]) |

---

## 4. 문서 검색 API

### 4.1 DocumentSearch

문서(뉴스, 공시, 리포트, 특허) 검색

```python
DocumentSearch(category, section, query, count=10, page=None,
               date_from=None, date_to=None, use_score=False,
               summary=True, clustering=False, uniquify=True,
               highlight=False, fields=None)
```

**Category / Section 값:**

| Category | Section |
|----------|---------|
| news | politics, economy, society, culture, world, tech, entertainment, opinion |
| research | market, strategy, company, industry, economy, bond |
| company | ir, disclosure |
| patent | patent |

**검색 필드:**
- `title:키워드` - 제목 검색
- `content:키워드` - 내용 검색
- `publisher:언론사명` - 출처 검색
- `securities.name:기업명` - 관련 종목 검색
- `securities.symbol:종목코드` - 종목코드 검색
- `named_entities.entities.company.name:회사명` - 언급 회사 검색
- `named_entities.entities.person.name:인물명` - 언급 인물 검색
- `polarity.name:긍정/부정/중립` - 극성 검색
- `esg.category.name:환경/사회/지배구조` - ESG 검색

**예시:**
```python
# 경제 뉴스 검색
DocumentSearch(["news"],["economy"],"딥서치")

# 삼성전자 공시 검색
DocumentSearch(["company"],["disclosure"],"securities.name:삼성전자")

# 시간 범위 검색
DocumentSearch(["news"], [], "삼성전자 and created_at:[\"2022-07-12T00:00:00\" to \"2022-07-12T09:00:00\"]")

# Proximity Search (근접 검색)
DocumentSearch("news","economy","\"삼성전자 아이폰\"~15")
```

**⚠️ 기간 1년 한도 (레포 검증):** Basic 인증으로는 `date_from`~`date_to`가 1년을 넘으면 HTTP 413 `RequestEntityTooLarge`입니다. 1년 이하 구간으로 나눠 호출하고 `content_url`로 중복을 제거하세요. `skills/deepsearch/scripts/query_api.py`가 자동으로 처리합니다. DocumentTrends는 2년 범위도 정상입니다.

### 4.2 DocumentTrends

문서 트렌드 분석

```python
DocumentTrends(category, section, query, interval="1d",
               date_from=None, date_to=None)
```

**interval 값:** 1y, 1M, 1w, 1d, 1h, 1m

### 4.3 DocumentAggregation

문서 집계

```python
DocumentAggregation(category, section, query, groupby,
                    date_from=None, date_to=None, min_count=0)
```

**예시:**
```python
# 특정 주제 관련 기업 추출
DocumentAggregation("news", None, "코로나", "named_entities.entities.company.name:100")

# ESG 환경-긍정 기업 추출
DocumentAggregation("news","economy","esg.category.name:환경 and esg.polarity.name:긍정","securities.name:100")
```

### 4.4 GetSentimentScore

긍부정 점수 조회

```python
GetSentimentScore(query, interval="1d", date_from=None, date_to=None)
```

### 4.5 SimilarKeywords

유사 키워드 검색 (Word2Vec 기반)

```python
SimilarKeywords(positive_keyword, negative_keyword=None,
                max_count=30, min_score=0.5, date_from=None, date_to=None)
```

---

## 5. 기업 검색 API

### 5.1 FindEntity

기업 검색 (이름, 사업자번호, 주소, 전화번호 등)

```python
FindEntity(entity_type, pattern, count=0, fields=None, score_type=None, include_matched_fields=False)
```

**fields 값:**
- symbol, name_ko, name_en, name_short
- business_rid, company_rid
- industry_id
- road_name_ko, land_lot_ko
- tel, fax
- company_type_l1, company_type_l2, company_type_size

**예시:**
```python
FindEntity("Financial", "삼성*")
FindEntity("Financial", ["1248100998", "1268103725"], fields=["business_rid"])
FindEntity("Financial", "*울산*", fields=["road_name_ko", "land_lot_ko"])
```

경제지표 시리즈도 `FindEntity("DataSeries", "검색어")`로 찾습니다([12절](#12-경제지표)).

### 5.2 GetEntitySummary

검색한 엔티티의 요약 정보(심볼, 이름, 사업자·법인번호, 시장, 기업형태 등)

```python
GetEntitySummary(FindEntity("Financial", "삼성*"))
```
⚠️ 결과가 큽니다(`삼성*` 5,841행, 약 1.6MB). 패턴을 좁히세요.

### 5.3 FindEntityByName

이름 패턴으로 기업 검색

```python
FindEntityByName(entity_type, pattern, count=10000)
```
⚠️ 공식 예시 `FindEntityByName("Financial", "삼성*")`가 오류 없이 0행을 돌려줍니다(레포 검증). 이름 검색은 `FindEntity`를 쓰세요.

### 5.4 FindEntityByShareholderName

주주명으로 기업 검색

```python
FindEntityByShareholderName(entity_type, shareholder_name,
                            date_from=None, date_to=None, last_only=False)
```

### 5.5 FindEntityByIndustryID

산업분류코드로 기업 검색

```python
FindEntityByIndustryID(entity_type, pattern, count=100)
```

### 5.6 FindEntityByBusinessArea

사업영역으로 기업 검색

```python
FindEntityByBusinessArea(entity_type, pattern, count=0)
```

### 5.7 FindEntityByAddress

주소로 기업 검색

```python
FindEntityByAddress(entity_type, pattern, count=0)
```

### 5.8 FindEntityInDocuments

문서 기반 기업 검색

```python
FindEntityInDocuments(category, section, query, count=None,
                      date_from=None, date_to=None)
```

### 5.9 FindAssociatedEntity

주제 관련 기업 검색 (관련도 점수 포함)

```python
FindAssociatedEntity(query, count, min_score=0, date_from=None, date_to=None)
```

### 5.10 기업 주제(태그)

```python
GetEntityTags(entities)                         # 기업에 붙은 주제 태그 (tag_uid, category, name, expr)
FindEntityByTag(tag_uids, format=None)          # 태그로 기업 검색. tag_uids는 GetEntityTags의 tag_uid 리스트
GetConditionalTagMetadata(tag_uids=None, format=None)   # 태그 정의 목록 (234개)
```

---

## 6. 기업 정보 조회 API

### 6.1 GetCompanySummary

기업 개요 정보

```python
GetCompanySummary(entities)
```

**반환 필드:** symbol, entity_name, business_rid, company_rid, ceo_ko, industry_id, market_id, is_alive, employee_no, website 등

### 6.2 GetCompanyHistory

기업 연혁

```python
GetCompanyHistory(entities)
```

### 6.3 GetCompanyBusinessGoal

사업 목적

```python
GetCompanyBusinessGoal(entities)
```

### 6.4 GetCompanyBusinessSummary

사업 요약

```python
GetCompanyBusinessSummary(entities)
```

### 6.5 GetCompanyRelatedFirms

관계사 정보

```python
GetCompanyRelatedFirms(entities, date_from=None, date_to=None)
```

### 6.6 GetCompanyProductsSales

제품별 매출

```python
GetCompanyProductsSales(entities, date_from=None, date_to=None, annualize=False)
```

### 6.7 GetCompanyDebts

차입금 정보

```python
GetCompanyDebts(entities, date_from=None, date_to=None)
```

### 6.8 GetCompanyDividends

배당 정보

```python
GetCompanyDividends(entities, date_from=None, date_to=None)
```

### 6.9 GetCompanyShareholders

주주 정보

```python
GetCompanyShareholders(entities, date_from=None, date_to=None)
```

### 6.10 GetCompanyEmployees

종업원 정보

```python
GetCompanyEmployees(entities, date_from=None, date_to=None)
```

### 6.11 GetCompanyExecutives

임원 정보

```python
GetCompanyExecutives(entities, date_from=None, date_to=None)
```

### 6.12 GetCompanyBranches

사업장 정보

```python
GetCompanyBranches(entities)
```

### 6.13 GetFinancialStatementsAuditOpinion

감사의견 조회

```python
GetFinancialStatementsAuditOpinion(entities, date_from, date_to)
```
감사의견으로 기업을 검색하는 `SearchFinancialStatementsAuditOpinion`은 현재 구독으로 쓸 수 없습니다(`NameError`).

---

## 7. 재무·공시·시장 데이터 API

### 7.1 GetFinancialStatements

매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계 등 **모든 재무제표 항목**은 이 함수로 조회하는 것이 권장됩니다.

```python
GetFinancialStatements(entities, report_type="IFRS", consolidated=True,
                       is_annual=True, is_accumulated=False,
                       report_ids=None, date_from=None, date_to=None)
```

| 파라미터 | 값 | 설명 |
|---------|---|------|
| report_type | "IFRS" / "GAAP" | 회계기준 |
| consolidated | True / False | 연결/별도 |
| is_annual | True / False | 연간/분기 포함 |
| is_accumulated | True / False | 분기일 때 누적/3개월 증분 (손익·현금흐름) |
| report_ids | "BalanceSheet", "Income", "CashFlow", "Ratio" | 특정 제표만 |

**⭕ 사용 예:** `GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)`
- 기업명은 따옴표 없이 쓰는 형태를 권장합니다. (이전에 따옴표를 붙이면 403이 났다는 기록이 있었으나, 2026-11-25에는 `GetFinancialStatements("삼성중공업")`도 정상이었습니다)
- **❌ 자연어 재무 쿼리 비권장:** `삼성전자 매출액 2020-2024` → KeyError 발생 가능

**계정명 (레포 검증, 삼성전자·삼성중공업 2024):** 결과는 행 단위(`date, symbol, entity_name, type_id, report_id, account_id, name_ko, value`)이고 1년에 500행 안팎입니다.

| 찾는 항목 | `name_ko` | report_id / account_id |
|---|---|---|
| 매출액 | `수익` | 12 / 1000 |
| 매출원가 · 매출총이익 | `매출원가` · `매출총이익(손실)` | 12 / 2000 · 3000 |
| 영업이익 | `영업이익(손실)` | 12 / 5000 |
| 당기순이익 | `총당기순이익` (지배주주분 `당기순이익지배기업지분`) | 12 / 8200 (9061) |
| 자산·부채·자본총계 | `자산총계` · `부채총계` · `자본총계` | 11 / 5000 · 8000 · 8900 |

report_id 11 = 재무상태표, 12 = 손익계산서, 19 = 재무비율. 과거 연도 값은 원래 공시값과 재작성값이 섞여 있습니다([research/restatement](../../research/restatement/README.md)).

### 7.2 GetAvailableFinancialStatements

조회 가능한 재무제표 목록

```python
GetAvailableFinancialStatements(entities, date_from=None, date_to=None)
```

### 7.3 분기 재무제표 쿼리

> **권장:** 분기 재무제표는 `GetFinancialStatements` 함수에서 `is_annual=False`로 설정하여 조회하는 것이 더 안정적입니다.

```python
# 분기 재무제표 조회 (권장 방법)
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, is_annual=False, report_ids="Income", date_from=2024-01-01, date_to=2025-12-31)
```

자연어 쿼리 규칙(회계기준·업종·연결/별도·연도/분기·누적/증분 기본값과 선택 예시)은 [1_기본적인_데이터_조회방법.md](1_기본적인_데이터_조회방법.md)의 "분기재무제표 쿼리"에 있습니다. 자연어 쿼리는 KeyError가 날 수 있습니다.

### 7.4 공시(DART) 정기보고서 데이터

사업·분기·반기보고서에 실린 표를 그대로 조회합니다. 형식은 모두 `(entities, date_from=None, date_to=None)`입니다(최대주주 변동은 `entities`만).

| 함수 | 내용 |
|---|---|
| `GetDartDividends` | 배당 내역 |
| `GetDartShareRepurchase` | 자기주식 취득·처분 |
| `GetDartMajorityShareholders` | 최대주주 현황 |
| `GetDartMajorityShareholderChange` | 최대주주 변동 |
| `GetDartMinorityShareholders` | 소액주주 현황 |
| `GetDartExecutives` | 임원 현황 |
| `GetDartEmployees` | 직원 현황 |
| `GetDartIndividualDirectorCompensation` | 이사·감사 개인별 보수(5억 이상) |
| `GetDartOverallDirectorCompensation` | 이사·감사 전체 보수 |
| `GetDartTopIndividualCompensation` | 개인별 보수 상위 5인(5억 이상) |
| `GetDartInvestmentInOthers` | 타법인 출자 현황 |

예: `GetDartDividends(KRX:005930, date_from=2000-01-01, date_to=2019-12-31)` → 115행. 증자(감자) 현황 `GetDartCapitalChange`는 현재 구독으로 쓸 수 없습니다(`NameError`).

### 7.5 컨센서스·이슈 기업

```python
GetConsensusInstitutionList()                       # 컨센서스 발표 기관 (60곳)
GetConsensusAnalystList(inst_code)                  # 기관의 애널리스트. 예: GetConsensusAnalystList("058585")
SearchTargetPrices(symbols, date_from=None, date_to=None)
SearchFirmFundamentalsForecasts(symbols, last_only=True, accounting_types=None, date_from=None, date_to=None)
GetCompanyShareholderChanges(date_from=None, date_to=None)      # 기간 중 주주 변동 기업
GetTargetPriceConsensusChange(relative_to=1, duration=6)        # 목표주가 컨센서스 변화
```
- `SearchTargetPrices`의 **opinion_code:** 1~2 부정, 3 중립, 4~5 긍정
- `SearchFirmFundamentalsForecasts`의 **accounting_types:** K(연간), F(3월), X(6월), Y(9월), Z(12월)
- ⚠️ `SearchAnalystReports(symbols=None, inst_code=None, analyst_id=None, date_from=None, date_to=None)`: 기업명만 넣으면 `KernelError: Internal Server Error`, 심볼+기간은 0행(레포 검증). 애널리스트 보고서는 `DocumentSearch(["research"],["company"],"securities.symbol:KRX:005930",...)`로 찾으세요.
- `GetFundamentalsConsensusChange`는 현재 구독으로 쓸 수 없습니다(`NameError`).

### 7.6 주가·지수

```python
GetStockSymbols(entities=None)                                          # 종목 정보
GetStockPrices(entities=None, columns=None, date_from=None, date_to=None)  # 일별 가격·거래량
GetMarketIndexSymbols(entities=None)                                    # 지수 정보
GetMarketIndexes(entities=None, columns=None, date_from=None, date_to=None) # 지수 가격·거래량
```
- `GetStockPrices` 컬럼: `open, high, low, close, volume, value, change, change_rate, shares_outstanding, market_cap, trading_halted`
- **여러 종목·전 종목 (레포 검증 2026-11-25):** `GetStockPrices([KRX:005930, KRX:000660], ...)`처럼 목록을 받습니다. `entities`를 생략하면 **전 종목**(4,300여 개, ETF 포함)의 **기간 마지막 거래일 하루치**가 3초 안에 옵니다. `GetStockSymbols()`도 생략하면 전 종목 기본정보(`market`, `company_type_l1`: 1 일반법인 / 8 ETF 등)를 줍니다.
- **`change_rate` 단위:** 종목은 비율(-0.0876 = -8.76%), `GetMarketIndexes`는 퍼센트(1.94 = 1.94%)입니다.
- `GetMarketIndexes(date_from, date_to)`는 지수 11종을 거래일마다 돌려줍니다. `GetFinancialStatements`도 기업 목록을 받습니다(3개사 3년 손익 약 900행).
- 가격은 **수정주가뿐**이고 원주가 옵션이 없습니다. 거래량·거래대금·주식수·시가총액은 당일 실제 값입니다([15절](#15-주의사항) 7번).

---

## 8. 산업·기업집단 API

### 8.1 산업 정보

| 함수 | 호출 결과 (레포 검증) |
|---|---|
| `GetAggregateIndustryInfo(mode=0, date_from=None, date_to=None)` | ❌ `NameError` — 현재 구독으로 쓸 수 없음 |
| `GetAggregateIndustryConsensus(industry_type=0, fields=None, date=None, consensus_duration=3)` | ❌ `NameError` — 현재 구독으로 쓸 수 없음 |
| `GetMarketSummaryInfoByIndustry(level=0)` | ❌ 서버 오류 `KeyError: industry_id` |

### 8.2 기업 집단

```python
FindConglomerateByName(names)                       # 그룹명으로 검색
FindConglomerateByID(conglomerate_ids)              # 예: FindConglomerateByID("511") → 삼성
GetConglomerateMembers(conglomerate_ids)            # 계열사
GetConglomerateFinancialStatements(conglomerate_ids, query, date_from=None, date_to=None)  # 그룹 재무
```

---

## 9. 인물 검색 API

```python
FindPersonBio(name, birthday)                       # 인물 경력
FindPeopleByName(name)                              # 이름으로 검색
FindPeopleByBirthday(birth_month, birth_day)        # ⚠️ 내부 타임아웃 (레포 검증)
FindRichestShareholders(count=500, date_from=None, date_to=None)   # ⚠️ 내부 타임아웃 (레포 검증)
```

---

## 10. 토픽 API

```python
SearchTrendingTopics(category, section, fields=None)                 # 실시간 트렌딩 토픽 (토픽 ID = uid)
GetTrendingTopic(category, section, topic_uid, count=10, summary=True, highlight_query=None, fields=None)
SearchHistoricalTopics(category, section, query, count=10, page=None, sort=None, date_from=None, date_to=None, fields=None)
GetHistoricalTopic(category, section, topic_uid, sorts=None, count=10, summary=True, highlight_query=None, fields=None)
```

### 10.1 토픽 인사이트 (REST)

compute가 아닌 별도 REST API입니다. 같은 Basic 인증으로 동작합니다(레포 검증). 상세는 [4_토픽인사이트.md](4_토픽인사이트.md).

```
GET https://api.deepsearch.com/v1/topic-insight/insight?type={trending|historical}&section={section}&topicId={uid}&stream=false
GET https://api.deepsearch.com/v1/topic-insight/questions?type=...&section=...&topicId=...&stream=false
```
→ `{"success": true, "data": "요약/질문 텍스트"}`. `topicId`는 `SearchTrendingTopics`의 `uid`입니다.

---

## 11. 이벤트·포트폴리오 API

```python
ComputePortfolioReturns(entities, date_from, date_to, weight, rebalancing_freq="daily", ...)
# 예: ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, 2018-12-31, "equal")
ComputeEventDayStockReturns(event_dates)            # 이벤트일 종목별 수익률. 예: ComputeEventDayStockReturns(2020-5-7)
```
- ⚠️ `AnalyzePortfolioReturns(portfolio, benchmark)`: `AttributeError`로 동작하지 않음 (레포 검증)
- ⚠️ `ComputeStockReturnCorrelationWith(target=0, date_from=None, date_to=None)`: 응답 없음/타임아웃
- ❌ `GetIndustryReturnsOnEventDates`, `GetCumulativeIndustryReturns`: 서버 오류 `KeyError: industry_id`
- ❌ 채권 이벤트 함수 3개(`GetBondYieldChangesPer*`): 현재 구독으로 쓸 수 없음

---

## 12. 경제지표

시리즈 ID 형식: 한국은행 `BOK:통계코드.항목코드`, FRED `시리즈ID`, IMF `IMF:...`, OECD `OECD:...`, World Bank `WB:지표-국가`, 딥서치 자체 `DS:...`. 시리즈 검색은 `FindEntity("DataSeries", "검색어")`.

| 출처 | 정보 조회 | 값 조회 | 예시 |
|---|---|---|---|
| 한국은행 | `QueryBankOfKoreaSeriesInfo` | `QueryBankOfKoreaSeriesData`, `...DataSimple` | `QueryBankOfKoreaSeriesData("060Y001.010101000")` |
| FRED | `QueryFredSeriesInfo`, `GetFredCategoryOfDataSeries` | `QueryFredSeriesData` | `QueryFredSeriesData(["UNRATE"])` |
| IMF | `GetImfSeriesInfo`, `GetImfDataflowAnnotations` | `GetImfSeriesValues` | `GetImfSeriesValues("IMF:BOP.A.AU.BCA_BP6_USD")` |
| OECD | `GetOecdSeriesInfo`, `GetOecdDatasetAnnotations` | `GetOecdSeriesValues` | `GetOecdSeriesValues("OECD:AEA.HRV.ACG.O.TSO2")` |
| World Bank | `QueryWorldBankSeriesInfo` | `QueryWorldBankSeriesData` | `QueryWorldBankSeriesData("WB:EN.ATM.CO2E.PC-KOR")` |
| 딥서치 자체 | `QueryDeepSearchOwnSeriesInfo` | `QueryDeepSearchOwnSeriesValues` | `QueryDeepSearchOwnSeriesValues("DS:TOUR.001.0001")` |
| 통계청(KOSIS) | — | — | ❌ 5개 함수 모두 현재 구독으로 쓸 수 없음 |

⚠️ 기간을 주지 않으면 전체 시계열이 옵니다(한국은행 예시 7,467행, FRED 3개 시리즈 21,353행 약 1MB). `date_from`/`date_to`를 주세요.

---

## 13. 결과 레이아웃

### 13.1 공통 구조

```json
{
  "success": true/false,
  "data": {
    "profile": { "compile": ms, "interpreter": ms, "pods": ms, "total": ms },
    "exceptions": [],
    "pods": [
      {
        "class": "Result:XXX",
        "position": -1,
        "title": "Result",
        "content": {...}
      }
    ]
  }
}
```

### 13.2 Pod 클래스 유형

| 클래스 | 설명 |
|--------|------|
| Input | 입력 해석 결과 |
| Result:DataFrame | 테이블 형식 결과 (`content.data` = `{컬럼: [값...]}`) |
| Result:SingleValue | 단일 값 결과 |
| Result:DocumentSearchResult | 문서 검색 결과 (`content.data.docs`) |
| Result:DocumentTrendsResult | 문서 트렌드 결과 |
| Result:TrendingTopicsSearchResult | 트렌딩 토픽 검색 결과 |
| Result:TrendingTopicResult | 트렌딩 토픽 상세 |
| Result:HistoricalTopicsSearchResult | 과거 토픽 검색/상세 결과 |
| Result:PortfolioReturns | 포트폴리오 수익률 |
| Result:PortfolioAnalysis | 포트폴리오 분석 |

### 13.3 문서 검색 결과 필드

| 필드 | 설명 | 타입 |
|------|------|------|
| uid/uid_str | 문서 ID | number/string |
| category | 문서 타입 | string |
| section | 문서 섹션 | string |
| publisher | 출처 | string |
| author | 작성자 | string |
| title | 제목 | string |
| content | 내용 요약 | string |
| securities | 관련 종목 | array |
| entities | 관련 엔티티 | array |
| industry | 산업 정보 | object |
| polarity | 긍부정 정보 | object |
| esg | ESG 정보 | object |
| content_url | 원문 링크 | string |
| created_at | 생성 일시 | string |

---

## 14. 주요 코드값

### 14.1 시장 구분 (market_id)

| 코드 | 시장 |
|------|------|
| 1 | KOSPI |
| 2 | KOSDAQ |
| 3 | KONEX |
| 4 | 제3시장 |
| 9 | 대상아님 |

### 14.2 기업규모 (company_type_size)

| 코드 | 규모 |
|------|------|
| 1 | 대기업 |
| 2 | 중소기업 |
| 3 | 중견기업 |
| 0 | 기타 |

### 14.3 극성 (polarity)

| 코드 | 명칭 |
|------|------|
| 1 | 긍정 |
| 0 | 중립 |
| -1 | 부정 |

### 14.4 ESG 분류

| 코드 | 명칭 |
|------|------|
| E | 환경 |
| S | 사회 |
| G | 지배구조 |
| U | 해당없음 |

---

## 15. 주의사항

1. **키워드 검색 시 따옴표 사용**
   - 서울, 울산 등 기업명과 혼동될 수 있는 키워드는 반드시 `"서울"` 형태로 사용

2. **재무/시장 데이터 혼합 주의**
   - 재무데이터(연/분기)와 시장데이터(일별)는 업데이트 주기가 다르므로 별도 조회 권장

3. **사업자번호/법인번호 입력**
   - 대시(-) 없이 숫자만 입력

4. **연결/개별 재무제표**
   - 컨센서스 데이터의 `csd_` prefix는 연결 재무제표 항목

5. **Boolean 연산자**
   - 기본 AND 연산, OR/NOT 명시 가능
   - 예: `삼성전자 (갤럭시 or 아이폰) !소송`

6. **재무제표 조회 시 GetFinancialStatements 권장**
   - 자연어 쿼리(`삼성전자 매출액 2020-2024`)보다 `GetFinancialStatements` 함수가 안정적
   - 주가/시장 데이터(종가, PER, PBR, 시가총액)는 자연어 쿼리 사용 가능
   - 계정명은 `매출액`이 아니라 `수익`입니다(7.1절 표)

7. **주가는 수정주가뿐 (원주가 옵션 없음)** — 검증 2026-11-25, [research/price_adjustment](../../research/price_adjustment/README.md)
   - 시가·고가·저가·종가는 액면분할·무상증자·유상증자로 소급 수정된 값입니다(배당은 미반영). `GetStockPrices`에 원주가를 고르는 파라미터나 컬럼은 없습니다.
   - 거래량·거래대금·상장주식수·시가총액은 수정되지 않은 당일 값입니다. 원주가 = `market_cap ÷ shares_outstanding`
   - 자연어 주가 쿼리는 2020-01-02 이후만 나옵니다. 그 이전 범위는 오류 없이 오늘 값 1행을 돌려줍니다. 과거는 `GetStockPrices`를 쓰세요.
   - 주가를 사용자에게 보여줄 때는 수정주가라는 점을 먼저 안내합니다.

8. **BPS·EPS의 look-ahead** — 검증 2026-11-20, [research/pbr_bps](../../research/pbr_bps/README.md)
   - 시장데이터 BPS·EPS(따라서 PBR·PER)는 FY N 값이 N+1년 첫 거래일부터 붙어 있습니다. 백테스트에서는 공시 시점 이후로 밀어 쓰세요.
   - BPS 정의는 연결 지배기업소유주지분 ÷ (보통주+우선주 − 자기주식), 직전 연말 기준 하나뿐입니다.

9. **결과 크기**
   - 재무제표 5년치, 경제지표 전체 시계열, `GetEntitySummary(FindEntity(...))` 등은 수백 KB~수 MB입니다. 기간·대상을 좁히거나 결과를 파일로 저장해 걸러 쓰세요.

---

## 16. 현재 구독으로 쓸 수 없는 API

2026-11-25에 이 레포의 API 키로 호출해 확인했습니다. 원문 파일에도 넣지 않았습니다.

| API | 주소 | 결과 |
|---|---|---|
| DeepSearch v2 REST (https://api-v2.deepsearch.com/v2/manual/redoc, 215개 경로: 뉴스·기업·시장·ETF·브리핑·소셜 등) | `https://api-v2.deepsearch.com/v1/...`, `/v2/...` | 401 `잘못된 API Key 입니다` (Basic 헤더, `api_key` 쿼리 모두) |
| 해외기업 (가이드 "해외기업" 5페이지) | `https://api.deepsearch.com/v2/companies/...` | 401 `잘못된 API Key 입니다` |
| 챗딥서치 (문서 QA, Function Call) | `https://api.deepsearch.com/note/v1/...` | 401 `Session token is not provided` |

compute 함수 중 사용 불가로 확인된 것: 채권 18개, 통계청 5개, 채권 이벤트 3개, `GetDartCapitalChange`, `GetFundamentalsConsensusChange`, `GetAggregateIndustryInfo`, `GetAggregateIndustryConsensus`, `SearchFinancialStatementsAuditOpinion` (모두 `NameError: UFunction ... is not defined`). 원문 파일에는 남겨 두고 각 페이지에 검증 메모를 붙였습니다.

**데이터 자체가 없는 것:** 종목별 투자자 수급, 공매도, 대차, 신용융자, 프로그램매매, 지수선물, ETF NAV, 장중 분봉·틱·호가, NXT, 대량매매. 자연어 질의는 오류 없이 기업 개요 표로 빠지고, `GetStockPrices`의 허용 컬럼 15개에도 없습니다. 한국은행 시리즈(국고채·콜·CD, 시장 수급, 신용융자 잔고)는 2024-03~04에서 멈춰 있습니다. 근거와 CHECK API 시나리오별 원데이터 대조: [research/data_gaps](../../research/data_gaps/README.md)

---

## 17. 전체 함수 목록과 호출 결과

원문 파일의 함수 페이지별 첫 예시를 그대로 호출한 결과입니다(2026-11-25). ✅ 정상, ⚠️ 주의(0행·타임아웃 등), ❌ 사용 불가. 예시 인자가 자리표시자였던 함수는 실제 값으로 다시 확인했습니다.

#### 국내기업 (`3_API함수를_통한_데이터_조회_국내기업.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 기업 검색 | `FindEntity` | `FindEntity(entity_type, pattern, count=0, fields=None)` | 기업명, 주소, 사업자 등록 번호 등을 조건으로 주고 이에 해당하는 기업들의 목록을 검색할 수 있습니다. | ✅ |
| 기업 검색 | `GetEntitySummary` | `GetEntitySummary(Function)` | 검색한 Entity 에 대한 정보를 가져옵니다. | ✅ |
| 기업 검색 | `FindEntityByName` | `FindEntityByName(entity_type, pattern, count=10000)` |  | ⚠️ 예시가 오류 없이 0행 |
| 기업 검색 | `FindEntityByShareholderName` | `FindEntityByShareholderName(entity_type, shareholder_name, date_from=None, date_to=None, last_only=False)` |  | ✅ |
| 기업 검색 | `FindEntityByIndustryID` | `FindEntityByIndustryID(entity_type, pattern, count=100)` |  | ⚠️ 예시가 오류 없이 0행 |
| 기업 검색 | `FindEntityByBusinessArea` | `FindEntityByBusinessArea(entity_type, pattern, count=0)` |  | ✅ |
| 기업 검색 | `FindEntityByAddress` | `FindEntityByAddress(entity_type, pattern, count=0)` |  | ✅ |
| 기업 검색 | `FindEntityInDocuments` | `FindEntityInDocuments(category, section, query, count=None, date_from=None, date_to=None)` | 문서내에서 특정 키워드가 언급된 기업을 검색합니다. | ✅ |
| 기업 검색 | `FindAssociatedEntity` | `FindAssociatedEntity(query, count, min_score=0, date_from=None, date_to=None)` | 공시, 뉴스, 증권사리포트, IR 등 다양한 문서를 활용하여, 특정 주제와 관련된 기업을 검색합니다. | ✅ |
| 기업 검색 | `SearchFinancialStatementsAuditOpinion` | `SearchFinancialStatementsAuditOpinion(query,date_from=None, date_to=None)` | 감사의견을 바탕으로 기업을 검색합니다. | ❌ 미제공 |
| 기업 정보 조회 | `GetCompanySummary` | `GetCompanySummary(entities)` | 기업이 개요 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyHistory` | `GetCompanyHistory(entities)` | 회사의 연혁 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyBusinessGoal` | `GetCompanyBusinessGoal(entities)` | 기업의 사업목적을 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyBusinessSummary` | `GetCompanyBusinessSummary(entities)` | 사업 개요 및 현황 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyRelatedFirms` | `GetCompanyRelatedFirms(entities, date_from=None, date_to=None)` | 관계사 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyProductsSales` | `GetCompanyProductsSales(entities, date_from=None, date_to=None, annualize=False)` | 회사 제품별 매출 데이터를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyDebts` | `GetCompanyDebts(entities, date_from=None, date_to=None)` | 차입금 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyDividends` | `GetCompanyDividends(entities, date_from=None, date_to=None)` | 기업의 배당 내역을 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyShareholders` | `GetCompanyShareholders(entities, date_from=None, date_to=None)` | 기업의 주주정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyEmployees` | `GetCompanyEmployees(entities, date_from=None, date_to=None)` | 종업원 현황 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyExecutives` | `GetCompanyExecutives(entities, date_from=None, date_to=None)` | 임원 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetCompanyBranches` | `GetCompanyBranches(entities)` | 지점 정보를 조회합니다. | ✅ |
| 기업 정보 조회 | `GetFinancialStatementsAuditOpinion` | `GetFinancialStatementsAuditOpinion(entities, date_from, date_to)` | 특정 기업의 감사 의견을 조회합니다. | ✅ |
| 재무제표 조회 | `GetFinancialStatements` | `GetFinancialStatements(entities, report_type="IFRS", consolidated=True, is_annual=True, is_accumulated =Fal...` | 기업의 재무제표를 조회합니다. | ✅ |
| 재무제표 조회 | `GetAvailableFinancialStatements` | `GetAvailableFinancialStatements(entities, date_from=None, date_to=None)` | 해당 기업이 발표하는 재무제표 종류를 조회합니다. ( 분기, 연간, IFRS/GAAP ) | ✅ |
| 공시 정보 조회 | `GetDartCapitalChange` | `GetDartCapitalChange(entities)` | 정기보고서(사업, 분기, 반기보고서) 내에 증자(감자) 현황을 제공합니다. | ❌ 미제공 |
| 공시 정보 조회 | `GetDartDividends` | `GetDartDividends(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 배당 내역을 조회합니다. | ✅ |
| 공시 정보 조회 | `GetDartShareRepurchase` | `GetDartShareRepurchase(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 자기주식 취득 및 처분 현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartMajorityShareholders` | `GetDartMajorityShareholders(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 최대주주 현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartMajorityShareholderChange` | `GetDartMajorityShareholderChange(entities)` | 정기보고서(사업, 분기, 반기보고서) 내에 최대주주 변동 현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartMinorityShareholders` | `GetDartMinorityShareholders(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 소액주주현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartExecutives` | `GetDartExecutives(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 임원현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartEmployees` | `GetDartEmployees(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 직원현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartIndividualDirectorCompensation` | `GetDartIndividualDirectorCompensation(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사의 개인별 보수 현황(5억 이상)을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartOverallDirectorCompensation` | `GetDartOverallDirectorCompensation(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사 전체의 보수현황을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartTopIndividualCompensation` | `GetDartTopIndividualCompensation(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다. | ✅ |
| 공시 정보 조회 | `GetDartInvestmentInOthers` | `GetDartInvestmentInOthers(entities, date_from=None, date_to=None)` | 정기보고서(사업, 분기, 반기보고서) 내에 타법인 출자현황을 제공합니다. | ✅ |
| 컨센서스 정보 조회 | `GetConsensusInstitutionList` | `GetConsensusInstitutionList()` | 컨센서스를 발표하는 기관 리스트를 조회합니다. | ✅ |
| 컨센서스 정보 조회 | `GetConsensusAnalystList` | `GetConsensusAnalystList(inst_code)` | 특정 기관의 애널리스트 정보를 조회합니다. | ✅ (inst_code 필요) |
| 컨센서스 정보 조회 | `SearchAnalystReports` | `SearchAnalystReports(symbols=None, inst_code=None, analyst_id=None, date_from=None, date_to=None)` | 특정 기업에 대한 애널리스트 리포트를 조회합니다. | ⚠️ 기업명만 넣으면 500, 심볼+기간은 0행 |
| 컨센서스 정보 조회 | `SearchTargetPrices` | `SearchTargetPrices(symbols, date_from=None, date_to=None)` | 특정 종목에 대한 목표 주가를 조회합니다. | ✅ |
| 컨센서스 정보 조회 | `SearchFirmFundamentalsForecasts` | `SearchFirmFundamentalsForecasts(symbols, last_only=True, accounting_types=None, date_from=None, date_to=None)` | 특정 종목에 대한 예상 실적을 조회합니다. | ✅ |
| 이슈 기업 목록 조회 | `GetCompanyShareholderChanges` | `GetCompanyShareholderChanges(date_from=None, date_to=None)` | 최대 주주의 지분율이 변경된 기업 리스트를 조회합니다. | ✅ |
| 이슈 기업 목록 조회 | `GetTargetPriceConsensusChange` | `GetTargetPriceConsensusChange(relative_to=1, duration=6)` | 증권사 목표주가 변화 내역을 조회합니다. | ✅ |
| 이슈 기업 목록 조회 | `GetFundamentalsConsensusChange` | `GetFundamentalsConsensusChange(field="operating_income", relative_to=1, duration=6, forecast_target=0)` | 증권사 컨센서스 실적 추정치 변화 내역을 조회합니다. | ❌ 미제공 |
| 주가 정보 조회 | `GetStockSymbols` | `GetStockSymbols(entities=None)` | 종목 정보를 조회합니다. | ✅ |
| 주가 정보 조회 | `GetStockPrices` | `GetStockPrices(entities=None, columns=None, date_from=None, date_to=None)` | 종목의 현재 가격 및 거래량 정보를 조회합니다. | ✅ |
| 주가 정보 조회 | `GetMarketIndexSymbols` | `GetMarketIndexSymbols(entities=None)` | 지수에 대한 정보를 조회합니다. | ✅ |
| 주가 정보 조회 | `GetMarketIndexes` | `GetMarketIndexes(entities=None, columns=None, date_from=None, date_to=None)` | 현재 지수의 가격 및 거래량 등의 정보를 조회합니다. | ✅ |

#### 채권 (`3_API함수를_통한_데이터_조회_채권.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 채권 정보 조회 | `GetBondClassificationCodeList` | `GetBondClassificationCodeList()` | 전체 채권 종류를 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondIssuerList` | `GetBondIssuerList(class_code)` | 특정 class 채권의 발행자 정보를 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondIssuerListFromIndustry` | `GetBondIssuerListFromIndustry(industries)` | 특정 산업의 채권 발행자 리스트를 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondIssuerSummaryInfo` | `GetBondIssuerSummaryInfo(composite_codes)` | 특정 채권의 요약 정보를 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondClassSummaryInfo` | `GetBondClassSummaryInfo(class_codes)` | 특정 클래스의 채권 정보를 조회한다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondSummaryInfoPerIndustry` | `GetBondSummaryInfoPerIndustry(industries)` | 특정 산업의 채권 정보를 조회한다. | ❌ 미제공 |
| 채권 정보 조회 | `GetLatestBondIssues` | `GetLatestBondIssues()` | 최근에 발행된 채권 정보를 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `SearchBondIssuerByName` | `SearchBondIssuerByName(name)` | 이름으로 채권 발행자를 검색합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondIssuanceHistory` | `GetBondIssuanceHistory(issuer_codes)` | 특정 채권 발행자의 과거 채권 발행 이력을 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondRepaymentSchedule` | `GetBondRepaymentSchedule(issuer_codes)` | 특정 채권 발행자의 상환 스케쥴을 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondYields` | `GetBondYields(composite_codes=None, class_codes=None, issuer_codes=None, date_from=None, date_to=None)` | 채권 수익률을 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondYieldsForIndustry` | `GetBondYieldsForIndustry(industries, date_from=None, date_to=None)` | 특정 산업의 채권 수익률을 계산합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetAverageBondYieldTimeSeries` | `GetAverageBondYieldTimeSeries(code_type=0, codes=None, date_from=None, date_to=None)` | 지정한 종류의 채권들의 평균 금리 time series를 계산 합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetInterpolatedBondYields` | `GetInterpolatedBondYields(maturities, code_type=0, codes=None, date_from=None, date_to=None)` | 지정한 종류의 채권들의 Interpolated 채권 수익률을 계산합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetRiskFreeYields` | `GetRiskFreeYields(date_from=None, date_to=None)` | 무위험 이자율을 조회합니다. | ❌ 미제공 |
| 채권 정보 조회 | `GetBondYieldPrincipalComponents` | `GetBondYieldPrincipalComponents(composite_codes=None, class_codes=None, issuer_codes=None, date_from=None, ...` | 채권 주성분을 분석합니다. | ❌ 미제공 |
| 채권 정보 조회 | `ConvertBondIssuerCodeToNICESymbol` | `ConvertBondIssuerCodeToNICESymbol(issuer_codes)` | 채권 발행자 코드를 나이스 심볼로 변환합니다. | ❌ 미제공 |
| 채권 정보 조회 | `ConvertNICESymbolToBondIssuerCode` | `ConvertNICESymbolToBondIssuerCode(symbols)` | 나이스 심볼 코드를 채권 발행자 코드로 변환합니다. | ❌ 미제공 |

#### 산업 (`3_API함수를_통한_데이터_조회_산업검색.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 산업 정보 조회 | `GetAggregateIndustryInfo` | `GetAggregateIndustryInfo(mode=0, date_from=None, date_to=None)` | 산업분류별 포괄 정보를 조회한다. | ❌ 미제공 |
| 산업 정보 조회 | `GetAggregateIndustryConsensus` | `GetAggregateIndustryConsensus(industry_type=0, fields=None, date=None, consensus_duration=3)` | 산업별 컨센서스를 조회합니다. | ❌ 미제공 |
| 산업 정보 조회 | `GetMarketSummaryInfoByIndustry` | `GetMarketSummaryInfoByIndustry(level=0)` | 산업별 기업개수, 시가총액 및 PER를 조회한다. | ❌ KeyError industry_id |
| 기업 주제 조회 | `GetConditionalTagMetadata` | `GetConditionalTagMetadata(tag_uids=None, format=None)` | 태그 메타 정보를 가지고 옵니다. | ✅ |
| 기업 주제 조회 | `FindEntityByTag` | `FindEntityByTag(tag_uids, format=None)` | 특정 태그 조건에 해당하는 기업 리스트를 조회합니다. | ✅ (tag_uid 리스트 필요) |
| 기업 주제 조회 | `GetEntityTags` | `GetEntityTags(entities)` | 특정 기업과 관련된 태그 리스트를 가지고 온다. 이를 통하여 해당 기업이 관련된 주제 등을 정리하여 노출할 수 있다. | ✅ |
| 기업 집단 정보 조회 | `FindConglomerateByName` | `FindConglomerateByName(names)` | 이름으로 기업 집단을 검색한다. | ✅ |
| 기업 집단 정보 조회 | `FindConglomerateByID` | `FindConglomerateByID(conglomerate_ids)` | 기업 집단 ID로 기업 집단을 검색한다. | ✅ |
| 기업 집단 정보 조회 | `GetConglomerateMembers` | `GetConglomerateMembers(conglomerate_ids)` | 특정 기업 집단에 속한 기업 정보를 조회한다. | ✅ |
| 기업 집단 정보 조회 | `GetConglomerateFinancialStatements` | `GetConglomerateFinancialStatements(conglomerate_ids, query, date_from=None, date_to=None)` | 특정 기업 집단의 재무정보를 조회합니다. | ⚠️ 예시가 오류 없이 0행 |

#### 인물 (`3_API함수를_통한_데이터_조회_인물검색.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 기업 임원 검색 | `FindPersonBio` | `FindPersonBio(name, birthday)` | 이름과 생년월일을 입력하면 해당 인물의 전체 이력을 꺼내옵니다. | ✅ |
| 기업 임원 검색 | `FindPeopleByName` | `FindPeopleByName(name)` |  | ✅ |
| 기업 임원 검색 | `FindPeopleByBirthday` | `FindPeopleByBirthday(birth_month, birth_day)` | 생일로 인물을 검색합니다. 오늘 생일을 맞은 인물, 또는 앞으로 일주일 이내 생일이 다가오는 인물을 보여주는 용도로 활용할 수 | ⚠️ 타임아웃 |
| 주식 부자 목록 추출 | `FindRichestShareholders` | `FindRichestShareholders(count=500, date_from=None, date_to=None)` | 주어진 기간 (date_from ~ date_to) 내에서 각 기업별 가장 마지막 주주 목록 사용하여, 현재 보유 주식의 가치 | ⚠️ 타임아웃 |

#### 문서 (`3_API함수를_통한_데이터_조회_문서검색.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 문서 검색 | `DocumentSearch` | `DocumentSearch(category, section, query, count=10, page=None, date_from=None, date_to=None, use_score=False...` | 뉴스, 공시, IR, 증권사 보고서, 특허 문서를 검색합니다. | ✅ |
| 문서 심화검색 | `DocumentTrends` | `DocumentTrends(category, section, query, interval="1d", date_from=None, date_to=None, fields=None, format=N...` | 문서를 기반으로 특정 주제의 트렌드 추이를 조회합니다. | ✅ |
| 문서 심화검색 | `DocumentAggregation` | `DocumentAggregation(category, section, query, groupby, date_from=None, date_to=None, min_count=0)` | 문서를 기반으로 다양한 조건으로 집계하여 처리한다. | ✅ |
| 문서 심화검색 | `GetSentimentScore` | `` | 문서의 긍부정점수를 조회합니다. | ✅ |
| 토픽 검색 | `SearchTrendingTopics` | `` | 현재 시장에서 벌어지고 있는 주요 이슈를 추출하여 제공합니다. | ✅ |
| 토픽 검색 | `GetTrendingTopic` | `GetTrendingTopic( category, section, topic_uid, count=10, summary=True, highlight_query=None, fields=None )` | 현재 시장에서 벌어지고 있는 주요 이슈에 대한 문서를 가져옵니다. | ✅ |
| 토픽 검색 | `SearchHistoricalTopics` | `SearchHistoricalTopics( category, section, query, count=10, page=None, sort=None, date_from=None, date_to=N...` | 과거의 주요 주제를 조회합니다. | ✅ |
| 토픽 검색 | `GetHistoricalTopic` | `GetHistoricalTopic( category, section, topic_uid, sorts=None, count=10, summary=True, highlight_query=None,...` | 과거의 주요 주제에 대한 문서를 가져옵니다. | ✅ |
| 유사 단어 추출 | `SimilarKeywords` | `SimilarKeywords(positive_keyword, negative_keyword, max_count = 30, min_score = 0.5, date_from = None, date...` | 입력된 쿼리와 유사한 키워드를 검색합니다. | ✅ |

#### 이벤트 (`3_API함수를_통한_데이터_조회_이벤트.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 주식 포트폴리오 성과 분석 | `ComputePortfolioReturns` | `ComputePortfolioReturns(entities, date_from, date_to, weight, rebalancing_freq="daily", rebalancing_date=0,...` | 포트폴리오에 대한 과거 일정 기간 동안의 수익률을 계산합니다. | ✅ |
| 주식 포트폴리오 성과 분석 | `AnalyzePortfolioReturns` | `AnalyzePortfolioReturns(portfolio, benchmark)` | 포트폴리오에 대한 결과를 벤치마크 지수와 비교하여 분석합니다. | ❌ AttributeError |
| 주식 시장 이벤트 분석 | `ComputeEventDayStockReturns` | `ComputeEventDayStockReturns(event_dates)` | 특정 이벤트 날짜의 종목별 수익률을 계산합니다. | ✅ |
| 주식 시장 이벤트 분석 | `ComputeStockReturnCorrelationWith` | `ComputeStockReturnCorrelationWith(target=0, date_from=None, date_to=None)` | 특정 index 와 전체 상장 기업 주가와의 correlation 을 계산합니다. | ⚠️ 타임아웃 |
| 주식 시장 이벤트 분석 | `GetIndustryReturnsOnEventDates` | `GetIndustryReturnsOnEventDates(event_dates, level=0)` | 특정 이벤트일의 산업별 수익률을 계산합니다. | ❌ KeyError industry_id |
| 주식 시장 이벤트 분석 | `GetCumulativeIndustryReturns` | `GetCumulativeIndustryReturns(event_dates, level=0, industry_codes=None)` | 특정 기간 동안의 산업별 수익률을 계산합니다. | ❌ KeyError industry_id |
| 채권 시장 이벤트 분석 | `GetBondYieldChangesPerIssuer` | `GetBondYieldChangesPerIssuer(event_dates)` | 특정 이벤트 날짜의 채권 발행자별 채권 수익률 변화를 조회합니다. | ❌ 미제공 |
| 채권 시장 이벤트 분석 | `GetBondYieldChangesPerClassification` | `GetBondYieldChangesPerClassification(event_dates)` | 특정 이벤트 날짜의 채권 분류별 채권 수익률을 조회합니다. | ❌ 미제공 |
| 채권 시장 이벤트 분석 | `GetBondYieldChangesPerIndustry` | `GetBondYieldChangesPerIndustry(event_dates)` | 특정 이벤트 날짜의 산업 분류별 채권 수익률을 조회합니다. | ❌ 미제공 |

#### 경제지표 (`3_API함수를_통한_데이터_조회_경제지표.md`)

| 분류 | 함수 | 호출 형식 | 설명 | 호출 결과 |
|---|---|---|---|---|
| 경제 지표 검색 | `FindEntity` | `FindEntity(entity_type, pattern, count=0, fields=None, score_type=None, include_matched_fields=False)` | 기업 검색에 사용되는 FindEntity 를 경제 지표 검색에도 활용할 수 있습니다. | ⚠️ 예시가 오류 없이 0행 |
| 한국은행 데이터 조회 | `QueryBankOfKoreaSeriesInfo` | `QueryBankOfKoreaSeriesInfo(entity_ids=None, stat_codes=None, item_codes=None)` | 선택된 한국은행 경제 지표의 상세 정보를 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 pre | ✅ |
| 한국은행 데이터 조회 | `QueryBankOfKoreaSeriesInfoSimple` | `QueryBankOfKoreaSeriesInfoSimple(entity_ids)` | 선택된 한국은행 경제 지표의 상세 정보를 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 pre | ⚠️ 예시가 오류 없이 0행 |
| 한국은행 데이터 조회 | `QueryBankOfKoreaSeriesData` | `QueryBankOfKoreaSeriesData(entity_ids=None, stat_codes=None, item_codes=None, date_from=None, date_to=None,...` | 선택된 한국은행 경제 지표의 데이터 값을 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 pre | ✅ |
| 한국은행 데이터 조회 | `QueryBankOfKoreaSeriesDataSimple` | `QueryBankOfKoreaSeriesDataSimple(entity_ids, date_from=None, date_to=None)` | 선택된 한국은행 경제 지표의 데이터 값을 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 pre | ✅ |
| 미연방은행 (FRED) 데이터 조회 | `QueryFredSeriesInfo` | `QueryFredSeriesInfo(entity_ids)` | 선택된 미연방은행 경제 지표의 상세 정보를 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는  | ✅ |
| 미연방은행 (FRED) 데이터 조회 | `QueryFredSeriesData` | `QueryFredSeriesData(entity_ids, date_from=None, date_to=None)` | 선택된 미연방은행 경제 지표의 데이터 값을 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는  | ✅ |
| 미연방은행 (FRED) 데이터 조회 | `GetFredCategoryOfDataSeries` | `GetFredCategoryOfDataSeries(entity_ids)` | 주어진 경제지표를 포함하고 있는 카테고리 정보를 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:"  | ✅ |
| 미연방은행 (FRED) 데이터 조회 | `GetFredDataSeriesListUnderCategory` | `GetFredDataSeriesListUnderCategory(category_ids)` | 명시된 카테고리 내에 포함된 경제 지표들의 목록을 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" | ✅ |
| IMF 데이터 조회 | `GetImfSeriesInfo` | `GetImfSeriesInfo(entity_ids)` | 선택된 IMF 경제 지표의상세 정보를 조회합니다. IMF 에서 수집한 경제 지표의 symbol 은"IMF:" 라는 prefix | ✅ |
| IMF 데이터 조회 | `GetImfSeriesValues` | `GetImfSeriesValues(entity_ids, date_from=None, date_to=None)` | 선택된 IMF 경제 지표의 데이터 값을 조회합니다. IMF에서 수집한 경제 지표의 symbol 은 "IMF:" 라는 prefi | ✅ |
| IMF 데이터 조회 | `GetImfDataflowAnnotations` | `GetImfDataflowAnnotations(entity_ids)` | IMF 는 데이터를 dataflow 라는 묶음으로 나누어 관리합니다. 이 API 함수는 지정된 데이터 시리즈가 포함된 data | ✅ |
| IMF 데이터 조회 | `GetImfIndicatorListOfSameCountry` | `GetImfIndicatorListOfSameCountry(entity_id)` | 지정된 entity_id 와 동일한 dataflow 안에서 해당 국가에 대한 다른 데이터 시리즈의 목록을 가져옵니다. 함수의  | ✅ |
| IMF 데이터 조회 | `GetImfCountryListOfSameIndicator` | `GetImfCountryListOfSameIndicator(entity_id)` | 지정된 entity_id 와 동일한 dataflow 안에서 해당 경제지표와 동일한 내용한 데이터를 제공하는 다른 국가들의 목록 | ✅ |
| OECD 데이터 조회 | `GetOecdSeriesInfo` | `GetOecdSeriesInfo(entity_ids)` | 선택된 OECD 경제 지표의상세 정보를 조회합니다. OECD 에서 수집한 경제 지표의 symbol 은"OECD:" 라는 pre | ✅ |
| OECD 데이터 조회 | `GetOecdSeriesValues` | `GetOecdSeriesValues(entity_ids, date_from=None, date_to=None)` | 선택된 OECD 경제 지표의 데이터 값을 조회합니다. OECD 에서 수집한 경제 지표의 symbol 은 "OECD:" 라는 p | ✅ |
| OECD 데이터 조회 | `GetOecdDatasetAnnotations` | `GetOecdDatasetAnnotations(entity_ids)` | OECD 는 데이터를 dataset 이라는 묶음으로 나누어 관리합니다. 이 API 함수는 지정된 데이터 시리즈가 포함된 dat | ✅ |
| OECD 데이터 조회 | `GetOecdRelatedIndicatorList` | `GetOecdRelatedIndicatorList(entity_id)` | OECD entity_id 는 "OECD:xxx.yyy.zzz" 과 같은 형태로 여러 코드가 dot (.) 으로 묶여있는 형태 | ✅ |
| World Bank 데이터 조회 | `QueryWorldBankSeriesInfo` | `QueryWorldBankSeriesInfo(entity_ids)` | 선택된 World Bank 경제 지표의 상세 정보를 조회합니다. World Bank 에서 수집한 경제 지표의 symbol 은  | ✅ |
| World Bank 데이터 조회 | `QueryWorldBankSeriesData` | `QueryWorldBankSeriesData(entity_ids, date_from=None, date_to=None)` | 선택된 World Bank 경제 지표의 데이터 값을 조회합니다. | ✅ |
| World Bank 데이터 조회 | `GetWorldBankCountryListOfIndicator` | `GetWorldBankCountryListOfIndicator(entity_ids)` | World Bank 는 다양한 국가들에 대해 데이터를 모아 제공합니다. 본 API 함수는 선택된 경제 지표의 값을 가지고 있는 | ✅ |
| World Bank 데이터 조회 | `GetWorldBankIndicatorListOfSameSource` | `GetWorldBankIndicatorListOfSameSource(entity_ids)` | World Bank 는 다양한 출처 (source) 에서 데이터를 모아 제공하고 있습니다. 본 API 함수는 선택된 경제 지표 | ✅ |
| 통계청 데이터 조회 | `QueryKosisTableInfo` | `QueryKosisTableInfo(entity_ids)` | 선택된 통계청 경제 지표에 대한 상세 정보를 표시합니다. 통계청에서 수집된 데이터는 "KOSIS:" 라는 prefix 를 가지 | ❌ 미제공 |
| 통계청 데이터 조회 | `GetKosisAvailableSampleDates` | `GetKosisAvailableSampleDates(entity_ids)` | 선택된 통계청 경제 지표의 값이 들어있는 전체 날짜 목록을 표시합니다. 일부 경제 지표의 경우 둘 이상의 주기 (예: 월별,  | ❌ 미제공 |
| 통계청 데이터 조회 | `GetKosisTableCategoryItemFreqList` | `GetKosisTableCategoryItemFreqList(entity_ids)` | 선택된 통계청 경제 지표의 테이블을 구성하고 있는 category 와 item code, 그리고 freq 의 목록을 표시합니다 | ❌ 미제공 |
| 통계청 데이터 조회 | `QueryKosisCrossSectionData` | `QueryKosisCrossSectionData(entity_id, freq=None, date=None)` | 선택된 통계청 경제 지표의 데이터 값을 리턴합니다. 통계청 데이터는 횡단면 테이블 (cross-section table) 이기 | ❌ 미제공 |
| 통계청 데이터 조회 | `QueryKosisTimeSeriesData` | `QueryKosisTimeSeriesData(entity_id, category_id, item_code=None, freq=None, date_from=None, date_to=None)` | 통계청 경제 지표의 경우 기본 구조는 횡단면 테이블 (cross-section table) 이지만, category_id 를  | ❌ 미제공 |
| 딥서치 자체 수집 데이터 조회 | `QueryDeepSearchOwnSeriesInfo` | `QueryDeepSearchOwnSeriesInfo(entity_ids)` | 지정된 딥서치 자체 수집 경제 지표 데이터의 상세 정보를 조회합니다. 딥서치 자체 수집 지표의 symbol 은 "DS:" 라는 | ✅ |
| 딥서치 자체 수집 데이터 조회 | `QueryDeepSearchOwnSeriesValues` | `QueryDeepSearchOwnSeriesValues(entity_ids, date_from=None, date_to=None)` | 지정된 딥서치 자체 수집 경제 지표의 데이터 값을 조회합니다. 딥서치 자체 수집 지표의 symbol 은 "DS:" 라는 pre | ✅ |
| 딥서치 자체 수집 데이터 조회 | `QueryDeepSearchOwnDataSeriesListOfSameCategory` | `QueryDeepSearchOwnDataSeriesListOfSameCategory(entity_id)` | 지정된 딥서치 자체 수집 경제 지표와 동일한 카테고리에 속하는 다른 지표 목록을 조회합니다. | ✅ |
