# DeepSearch API 통합 레퍼런스

## API 기본 정보
- Base URL: `https://api.deepsearch.com/v1/compute?input={쿼리}`
- 인증: `Authorization: Basic {인증키}`

---

## 1. 문서 검색 API

### DocumentSearch
```python
DocumentSearch(category, section, query, count=10, page=None,
               date_from=None, date_to=None, summary=True,
               clustering=False, uniquify=True, highlight=False, fields=None)
```

**카테고리/섹션:**
| Category | Section |
|----------|---------|
| `["news"]` | politics, economy, society, culture, world, tech, entertainment, opinion |
| `["research"]` | market, strategy, company, industry, economy, bond |
| `["company"]` | ir, disclosure |
| `["patent"]` | patent |

**검색 필드:**
| 필드 | 문법 | 예시 |
|------|------|------|
| 제목 | `title:키워드` | `title:반도체` |
| 본문 | `content:키워드` | `content:수출` |
| 언론사 | `publisher.raw:('A' or 'B')` | `publisher.raw:('매일경제')` |
| 관련종목 | `securities.name:기업명` | `securities.name:삼성전자` |
| 시장 | `securities.market:시장` | `securities.market:KOSPI` |
| 감성 | `polarity.name:긍정/부정` | `polarity.name:긍정` |
| ESG | `esg.category.name:환경/사회/지배구조` | `esg.category.name:환경` |
| ESG감성 | `esg.polarity.name:긍정/부정` | |

**Boolean:** `and`, `or`, `!`(NOT), `()` 그룹핑

### DocumentTrends
```python
DocumentTrends(category, section, query, interval="1d", date_from=None, date_to=None)
```
interval: `1y`, `1M`, `1w`, `1d`, `1h`, `1m`

### DocumentAggregation
```python
DocumentAggregation(category, section, query, groupby, date_from=None, date_to=None)
```
groupby: `"securities.name:20"`, `"named_entities.entities.company.name:100"`

### GetSentimentScore
```python
GetSentimentScore(query, interval="1d", date_from=None, date_to=None)
```

### SimilarKeywords
```python
SimilarKeywords(positive_keyword, negative_keyword=None, max_count=30)
```

### 토픽 API
```python
SearchTrendingTopics(category, section)
SearchHistoricalTopics(category, section, query, count=10, page=None, date_from=None, date_to=None)
```

---

## 2. 기업/재무 데이터

### ⚠️ 재무제표 조회 — GetFinancialStatements 우선 사용 (필수)

**재무제표 조회 시 자연어 쿼리 대신 반드시 GetFinancialStatements API 함수를 우선 사용하세요.**
자연어 쿼리("기업명 연결 매출액 2020-2024")는 내부 계정코드 매핑에서 KeyError가 발생할 수 있습니다.

```python
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
| report_ids | "BalanceSheet", "Income", "CashFlow", "Ratio" | 특정 제표만 (미지정시 전체) |

**❌ 기업명에 따옴표 금지:** `GetFinancialStatements("삼성중공업")` → 403. `GetFinancialStatements(삼성중공업)` → 정상

### 자연어 쿼리 (주가/시장 데이터 전용)

**자연어 쿼리는 주가/시장 데이터에만 사용하세요. 재무제표(매출, 영업이익 등)에는 사용 금지:**
```
삼성전자 종가 2024-06-01-2024-06-30 → 일별 종가 (OK)
삼성전자 PER                       → 현재 PER (OK)
삼성전자 PBR                       → 현재 PBR (OK)
삼성전자 시가총액 2024-01-01-2024-12-31 → 일별 시가총액 (OK)
```

**❌ 아래는 사용 금지 (KeyError 발생 가능):**
```
삼성전자 매출액 2020-2024              ← GetFinancialStatements 사용
기업명 연결 매출액 2020-2024           ← GetFinancialStatements 사용
기업명 매출액 영업이익 당기순이익       ← GetFinancialStatements 사용
```

**데이터 유형:**
- 주가/시장 (자연어 OK): 종가, 시가, 고가, 저가, 시가총액, 거래량, PER, PBR, EPS, BPS, DPS
- 재무제표 (**GetFinancialStatements 필수**): 매출액, 영업이익, 당기순이익, 자산, 부채, 자본 등
- 기업 개요: 대표이사, 종업원수, 설립일, 주거래은행, 산업분류

### 기업 검색 API
```python
FindEntity(entity_type, pattern, count=0, fields=None)
```
예약어: `"반도체" 관련 기업`, `"건강기능식품" 산업 기업`, `상장 기업`, `"국민연금" 주주 기업`

### 기업 정보 API
| 함수 | 설명 |
|------|------|
| `GetCompanySummary(entities)` | 기업 개요 |
| `GetCompanyDividends(entities, date_from, date_to)` | 배당 |
| `GetCompanyShareholders(entities, date_from, date_to)` | 주주 |
| `GetCompanyExecutives(entities, date_from, date_to)` | 임원 |

### 컨센서스 API
```python
SearchTargetPrices(symbols, date_from=None, date_to=None)
SearchFirmFundamentalsForecasts(symbols, last_only=True)
```

### 기업그룹/인물
```python
FindConglomerateByName(names)
GetConglomerateMembers(conglomerate_ids)
FindPeopleByName(name)
```

---

## 3. 스크리닝 & 분석 함수

### 스크리닝 조건
```
매출 > 1000000000000                   → 매출 1조 이상
영업이익 / 매출 > 0.15                  → 영업이익률 15%+
2023 매출 > 2022 매출 * 1.5            → 전년대비 50% 성장
("반도체" 관련 기업) and (매출액 영업이익) → 테마 + 재무 결합
```

### 분석 함수
| 함수 | 예시 |
|------|------|
| `Top(query, n)` | `Top(매출액, 10)` |
| `Bottom(query, n)` | `Bottom(시가총액, 10)` |
| `Max(query)` | `Max(삼성전자 매출액 2015-2024)` |
| `Min(query)` | `Min(LG전자 영업이익 2015-2024)` |
| `Mean(query)` | `Mean(삼성전자 종가 2024-01-01-2024-12-31)` |
| `Sort(query, ascending)` | `Sort(매출액 > 1조, ascending=False)` |

---

## 4. 주의사항

| 제한 | 설명 |
|------|------|
| 기간 제한 | DocumentSearch **최대 1년**, 초과 시 6개월 단위 분할 |
| 영업이익 연도비교 | `2024 영업이익 < 0 and 2023 영업이익 > 0` 불가 → turnaround_screener.py 사용 |
| 복수기업+연도범위 | `삼성전자 LG전자 영업이익 2020-2024` 불가 → `GetFinancialStatements` 개별 호출 |
| 한글 근접검색 | `"인수 합병"~5` 불가 |
| 인물 엔티티 | `named_entities.entities.person.name:인물명` 빈 결과 가능 → `content:인물명` 대체 |
| created_at 필드 | 직접 사용 시 문법 오류 → `date_from`/`date_to` 파라미터 사용 |

---

## 5. 언론사 참조

| 그룹 | 언론사 |
|------|--------|
| 중앙일간지 | 경향신문, 국민일보, 동아일보, 서울신문, 조선일보, 중앙일보, 한겨레, 한국일보 |
| 중앙경제지 | 매일경제, 머니투데이, 서울경제, 아주경제, 이데일리, 파이낸셜뉴스, 한국경제 |
