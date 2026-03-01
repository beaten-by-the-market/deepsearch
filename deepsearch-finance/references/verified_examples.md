# 검증된 사용 사례 (기업 & 재무)

모든 사례는 실제 API 호출로 검증되었습니다.

---

## 사례 1: SK하이닉스 분기 영업이익 (GetFinancialStatements)

**자연어:** "SK하이닉스의 최근 분기별 영업이익을 알려줘"

**쿼리:**
```
GetFinancialStatements(SK하이닉스, report_type="IFRS", consolidated=True, is_annual=False, report_ids="Income", date_from=2024-01-01, date_to=2025-12-31)
```
→ 507개 계정항목에서 영업이익 필터링하여 분기별 추이 확인

**5년간 조회 시:**
```
GetFinancialStatements(SK하이닉스, report_type="IFRS", consolidated=True, is_annual=False, report_ids="Income", date_from=2020-01-01, date_to=2024-12-31)
```
→ 전체 분기 데이터 한 번에 반환

---

## 사례 2: 삼성전자 일별 종가 조회

**자연어:** "삼성전자의 2024년 6월 일별 종가를 보여줘"

**쿼리:**
```
삼성전자 종가 2024-06-01-2024-06-30
```

**결과:** 20거래일 일별 종가 데이터

---

## 사례 3: 복수 기업 재무 데이터 비교 (GetFinancialStatements)

**자연어:** "삼성전자, LG전자, SK하이닉스의 2020~2024년 매출과 영업이익을 비교해줘"

**쿼리 (기업별 개별 호출):**
```
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, report_ids="Income", date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(LG전자, report_type="IFRS", consolidated=True, report_ids="Income", date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(SK하이닉스, report_type="IFRS", consolidated=True, report_ids="Income", date_from=2020-01-01, date_to=2024-12-31)
```
→ 각 기업의 507개 계정항목에서 매출액, 영업이익 필터링하여 비교

---

## 사례 4: 반도체 관련 기업 목록

**자연어:** "반도체 관련 상장기업 목록을 보여줘"

**쿼리:**
```
"반도체" 관련 기업
```

**결과:** 85개 기업 (삼성전자, LG이노텍, 한화, 인바디, 대한유화 등)

---

## 사례 5: 삼성전자 애널리스트 목표가

**자연어:** "2024년 상반기 삼성전자 애널리스트 목표가를 조회해줘"

**쿼리:**
```
SearchTargetPrices("005930",date_from=20240101,date_to=20240630)
```

**결과:** 29건의 목표가 데이터

---

## 사례 6: 삼성그룹 계열사

**자연어:** "삼성그룹 계열사를 알려줘"

**쿼리:**
```
FindConglomerateByName("삼성")
```

**결과:** 삼성그룹 정보 반환

---

## 사례 7: 기업 검색 - 이름 패턴

**자연어:** "삼성으로 시작하는 기업을 검색해줘"

**쿼리:**
```
FindEntity("Financial","삼성*")
```

---

## 사례 8: 특정 산업 기업 + 재무

**자연어:** "건강기능식품 산업 기업들의 매출과 영업이익을 보여줘"

**쿼리:**
```
("건강기능식품" 산업 기업) and (매출 영업이익)
```

---

## 사례 9: 국민연금 보유 기업

**자연어:** "국민연금이 주주인 기업을 알려줘"

**쿼리:**
```
"국민연금" 주주 기업
```

---

## 사례 10: 삼성전자 PER / PBR 조회

**자연어:** "삼성전자의 현재 PER과 PBR을 알려줘"

**쿼리:**
```
삼성전자 PER
삼성전자 PBR
```
(시장 데이터는 개별 기업 단위로 조회)
