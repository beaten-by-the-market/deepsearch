# 기업 & 재무 데이터 API 레퍼런스

## API 기본 정보
- Base URL: `https://api.deepsearch.com/v1/compute?input={쿼리}`
- 인증: `Authorization: Basic {인증키}`

## 1. 재무제표 조회 — GetFinancialStatements 필수

### ⚠️ 재무제표 데이터는 반드시 API 함수로 조회
매출액, 영업이익, 당기순이익, 자산, 부채, 자본 등 **모든 재무제표 항목**:

```python
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE코드 또는 KRX코드)

# 2단계: 재무제표 조회 (507개 계정항목 한 번에 반환)
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(삼성전자, consolidated=False)       # 별도 재무제표
GetFinancialStatements(삼성전자, report_ids="BalanceSheet") # 특정 제표만
GetFinancialStatements(삼성전자, is_annual=False)           # 분기 포함
```

| 파라미터 | 값 | 설명 |
|---------|---|------|
| report_type | "IFRS" / "GAAP" | 회계기준 |
| consolidated | True / False | 연결/별도 |
| is_annual | True / False | 연간/분기 포함 |
| report_ids | "BalanceSheet", "Income", "CashFlow", "Ratio" | 특정 제표만 |

**❌ 기업명에 따옴표 금지:** `GetFinancialStatements("삼성전자")` → 403 오류
**❌ 자연어 재무 쿼리 금지:** `삼성전자 매출액 2020-2024` → KeyError 발생 가능

## 2. 주가/시장 데이터 — 자연어 쿼리 OK

종가, 시가, 고가, 저가, 시가총액, 거래량, 거래대금, PER, PBR, EPS, BPS, DPS
```
삼성전자 종가 2024-01-01-2024-12-31
삼성전자 PER
삼성전자 시가총액 2024-01-01-2024-12-31
```

### 기업 개요 (자연어 쿼리 OK)
대표이사, 종업원수, 설립일, 주거래은행, 산업분류, 홈페이지

### 기간 형식
- `2020-2024` → 연도 범위
- `2024-01-01-2024-12-31` → 일자 범위

### 기업 입력
- 이름: `삼성전자`, `LG전자 SK하이닉스`
- Symbol: `KRX:005930`
- 사업자번호: `1248100998`
- 법인번호: `1301110006246`

## 3. 기업 검색 API

### FindEntity
```python
FindEntity(entity_type, pattern, count=0, fields=None)
```
fields: symbol, name_ko, business_rid, company_rid, industry_id, market_id, company_type_l1

### 기업 검색 예약어
| 유형 | 쿼리 | 예시 |
|------|------|------|
| 관련 기업 | `"키워드" 관련 기업` | `"반도체" 관련 기업` |
| 산업 기업 | `"산업명" 산업 기업` | `"건강기능식품" 산업 기업` |
| 사업 기업 | `"사업명" 사업 기업` | `"웹툰" 사업 기업` |
| 주소 기업 | `"주소" 주소 기업` | `"서울 마포구" 주소 기업` |
| 주주 기업 | `"주주명" 주주 기업` | `"국민연금" 주주 기업` |
| 이름 기업 | `"이름" 이름 기업` | `"자산운용" 이름 기업` |
| 상장/외감 | `상장 기업` | `상장 기업`, `외감 기업` |

## 4. 기업 정보 API

| 함수 | 설명 |
|------|------|
| `GetCompanySummary(entities)` | 기업 개요 |
| `GetCompanyHistory(entities)` | 기업 연혁 |
| `GetCompanyBusinessSummary(entities)` | 사업 요약 |
| `GetCompanyDividends(entities, date_from, date_to)` | 배당 정보 |
| `GetCompanyShareholders(entities, date_from, date_to)` | 주주 정보 |
| `GetCompanyExecutives(entities, date_from, date_to)` | 임원 정보 |
| `GetCompanyEmployees(entities, date_from, date_to)` | 종업원 정보 |

## 5. 컨센서스 API

```python
SearchTargetPrices(symbols, date_from=None, date_to=None)
SearchFirmFundamentalsForecasts(symbols, last_only=True, accounting_types=None)
SearchAnalystReports(symbols, inst_code, analyst_id, date_from, date_to)
```

## 6. 기업그룹 / 인물 API

```python
FindConglomerateByName(names)
GetConglomerateMembers(conglomerate_ids)
FindPeopleByName(name)
FindPersonBio(name, birthday)
FindRichestShareholders(count=500)
```

## 응답 구조

### DataFrame 결과
```json
{"data": {"pods": [{"class":"Input"}, {"class":"Result:DataFrame", "content":{"data":{
  "date": ["2024-03-31T00:00:00", ...],
  "symbol": ["KRX:005930", ...],
  "entity_name": ["삼성전자", ...],
  "매출액": [67780000000000, ...]
}}}]}}
```

## 주의사항
- 재무데이터(연/분기)와 시장데이터(일별)는 업데이트 주기가 달라 동시 조회 비추천
- 키워드가 기업명과 혼동되면 따옴표("") 사용
- 사업자번호/법인번호는 대시(-) 없이 숫자만
