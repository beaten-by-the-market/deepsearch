# DeepSearch API Master Reference

이 문서는 DeepSearch API의 모든 함수와 사용법을 정리한 마스터 레퍼런스입니다.

---

## 1. API 기본 정보

### API 호출 주소
```
https://api.deepsearch.com/v1/compute?input={쿼리}
```

### 인증 방식
- HTTP 헤더에 `Authorization: Basic {인증키}` 추가
- GET/POST 방식 모두 지원

### curl 예제
```bash
curl -H 'Authorization: Basic {인증키}' -XGET 'https://api.deepsearch.com/v1/compute?input={쿼리}'
```

---

## 2. 데이터 조회 방법

### 2.1 쿼리 형태의 데이터 조회

기본 구조: `기업 + 속성 + 기간`

```
삼성전자 매출액
삼성전자 매출액 2010-2020
삼성전자 주가 2020-01-01-2020-12-31
```

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
FindEntity(entity_type, pattern, count=0, fields=None)
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

### 5.2 FindEntityByShareholderName

주주명으로 기업 검색

```python
FindEntityByShareholderName(entity_type, shareholder_name,
                            date_from=None, date_to=None, last_only=False)
```

### 5.3 FindEntityByIndustryID

산업분류코드로 기업 검색

```python
FindEntityByIndustryID(entity_type, pattern, count=100)
```

### 5.4 FindEntityByBusinessArea

사업영역으로 기업 검색

```python
FindEntityByBusinessArea(entity_type, pattern, count=0)
```

### 5.5 FindEntityByAddress

주소로 기업 검색

```python
FindEntityByAddress(entity_type, pattern, count=0)
```

### 5.6 FindEntityInDocuments

문서 기반 기업 검색

```python
FindEntityInDocuments(category, section, query, count=None,
                      date_from=None, date_to=None)
```

### 5.7 FindAssociatedEntity

주제 관련 기업 검색 (관련도 점수 포함)

```python
FindAssociatedEntity(query, count, min_score=0, date_from=None, date_to=None)
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

### 6.6 GetCompanyDebts

차입금 정보

```python
GetCompanyDebts(entities, date_from=None, date_to=None)
```

### 6.7 GetCompanyDividends

배당 정보

```python
GetCompanyDividends(entities, date_from=None, date_to=None)
```

### 6.8 GetCompanyShareholders

주주 정보

```python
GetCompanyShareholders(entities, date_from=None, date_to=None)
```

### 6.9 GetCompanyEmployees

종업원 정보

```python
GetCompanyEmployees(entities, date_from=None, date_to=None)
```

### 6.10 GetCompanyExecutives

임원 정보

```python
GetCompanyExecutives(entities, date_from=None, date_to=None)
```

### 6.11 GetCompanyBranches

사업장 정보

```python
GetCompanyBranches(entities)
```

---

## 7. 재무 데이터 API

### 7.1 GetFinancialStatements

재무제표 조회

```python
GetFinancialStatements(entities, report_type="IFRS", consolidated=True,
                       is_annual=True, is_accumulated=False,
                       report_ids=None, date_from=None, date_to=None)
```

**report_type:** IFRS, GAAP
**report_ids:** Income, CashFlow, BalanceSheet, Ratio

### 7.2 GetAvailableFinancialStatements

조회 가능한 재무제표 목록

```python
GetAvailableFinancialStatements(entities, date_from=None, date_to=None)
```

### 7.3 분기 재무제표 쿼리

| 쿼리 | 회계기준 | 연결/별도 | 연도/분기 | 누적/증분 |
|------|----------|----------|----------|----------|
| 매출 | IFRS | 연결 | 연 | - |
| 2021 분기 매출 | IFRS | 연결 | 분기 | 증분 |
| 2021 분기 누적 매출 | IFRS | 연결 | 분기 | 누적 |
| 삼성전자 별도 분기 매출 | IFRS | 별도 | 분기 | 증분 |

---

## 8. 컨센서스 API

### 8.1 GetConsensusInstitutionList

증권사 목록

```python
GetConsensusInstitutionList()
```

### 8.2 GetConsensusAnalystList

애널리스트 목록

```python
GetConsensusAnalystList(inst_code)
```

### 8.3 SearchAnalystReports

애널리스트 리포트 검색

```python
SearchAnalystReports(symbols=None, inst_code=None, analyst_id=None,
                     date_from=None, date_to=None)
```

### 8.4 SearchTargetPrices

목표가 검색

```python
SearchTargetPrices(symbols, date_from=None, date_to=None)
```

**opinion_code:** 1~2 부정, 3 중립, 4~5 긍정

### 8.5 SearchFirmFundamentalsForecasts

실적 전망치 검색

```python
SearchFirmFundamentalsForecasts(symbols, last_only=True,
                                accounting_types=None,
                                date_from=None, date_to=None)
```

**accounting_types:** K(연간), F(3월), X(6월), Y(9월), Z(12월)

---

## 9. 산업 데이터 API

### 9.1 GetAggregateIndustryInfo

산업별 집계 정보

```python
GetAggregateIndustryInfo(mode=0, date_from=None, date_to=None)
```

### 9.2 GetAggregateIndustryConsensus

산업별 컨센서스

```python
GetAggregateIndustryConsensus(industry_type=0, fields=None,
                              date=None, consensus_duration=3)
```

### 9.3 GetMarketSummaryInfoByIndustry

산업별 시장 요약

```python
GetMarketSummaryInfoByIndustry(level=0)
```

---

## 10. 기업 그룹 API

### 10.1 FindConglomerateByName

그룹명으로 검색

```python
FindConglomerateByName(names)
```

### 10.2 FindConglomerateByID

그룹ID로 검색

```python
FindConglomerateByID(conglomerate_ids)
```

### 10.3 GetConglomerateMembers

그룹 계열사 조회

```python
GetConglomerateMembers(conglomerate_ids)
```

### 10.4 GetConglomerateFinancialStatements

그룹 재무제표

```python
GetConglomerateFinancialStatements(conglomerate_ids, query,
                                   date_from=None, date_to=None)
```

---

## 11. 인물 검색 API

### 11.1 FindPersonBio

인물 경력 조회

```python
FindPersonBio(name, birthday)
```

### 11.2 FindPeopleByName

이름으로 인물 검색

```python
FindPeopleByName(name)
```

### 11.3 FindPeopleByBirthday

생일로 인물 검색

```python
FindPeopleByBirthday(birth_month, birth_day)
```

### 11.4 FindRichestShareholders

주식 부자 목록

```python
FindRichestShareholders(count=500, date_from=None, date_to=None)
```

---

## 12. 토픽 API

### 12.1 SearchTrendingTopics

실시간 트렌딩 토픽

```python
SearchTrendingTopics(category, section, fields=None)
```

### 12.2 GetTrendingTopic

트렌딩 토픽 상세

```python
GetTrendingTopic(category, section, topic_uid, count=10,
                 summary=True, highlight_query=None, fields=None)
```

### 12.3 SearchHistoricalTopics

과거 토픽 검색

```python
SearchHistoricalTopics(category, section, query, count=10,
                       page=None, sort=None, date_from=None,
                       date_to=None, fields=None)
```

### 12.4 GetHistoricalTopic

과거 토픽 상세

```python
GetHistoricalTopic(category, section, topic_uid, sorts=None,
                   count=10, summary=True, highlight_query=None,
                   fields=None)
```

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
| Result:DataFrame | 테이블 형식 결과 |
| Result:SingleValue | 단일 값 결과 |
| Result:DocumentSearchResult | 문서 검색 결과 |
| Result:DocumentTrendsResult | 문서 트렌드 결과 |
| Result:TrendingTopicsSearchResult | 트렌딩 토픽 검색 결과 |
| Result:HistoricalTopicsSearchResult | 과거 토픽 검색 결과 |

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
