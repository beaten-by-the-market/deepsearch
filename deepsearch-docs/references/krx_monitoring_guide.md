# KRX 업무 활용 가이드 - 문서 검색 & 모니터링

한국거래소(KRX) 직원의 주요 업무 시나리오에 대한 검증된 쿼리 가이드입니다.

---

## 1. 조회공시 후보 뉴스 탐지

공시되지 않은 인수합병, 대규모 계약, 매각 등의 루머성 뉴스를 검색하여 조회공시 대상 종목을 발굴합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(인수 or 합병 or M&A or 매각) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 1,232건 (2025년 2월 기준)

**변형 쿼리:**
```
# 대규모 계약/수주 관련
DocumentSearch(["news"],[],"title:(수주 or 대규모 or 계약) and securities.market:KOSPI",count=100,page=1,date_from=20250201,date_to=20250228)

# 유상증자/무상증자
DocumentSearch(["news"],[],"title:(유상증자 or 무상증자 or 전환사채) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```

**주의:** DocumentSearch 기간은 최대 1년 이내로 제한됩니다.

---

## 2. 주가급변 종목 원인분석 (2단계)

주가가 급등/급락한 종목에 대해 관련 뉴스를 검색하고 주가 데이터를 결합 분석합니다.

**1단계 - 뉴스 검색:**
```
DocumentSearch(["news"],["economy"],"securities.name:에코프로비엠",count=100,page=1,date_from=20250201,date_to=20250228)
```
→ 69건의 뉴스에서 주요 이벤트 날짜/내용 파악

**2단계 - 주가+거래량 조회:** (deepsearch-finance 스킬 사용)
```
에코프로비엠 종가 거래량 2025-02-01-2025-02-28
```
→ 21거래일 일별 종가+거래량으로 뉴스 발생일 전후 변동 확인

**분석 포인트:**
- 뉴스 발생 전 주가/거래량 이상 변동 → 내부자거래 의심
- 뉴스 발생 후 급등/급락 → 시장 반응 확인
- 부정적 뉴스에도 주가 상승 → 추가 조사 필요

---

## 3. 시장 전반 부정 뉴스 모니터링

KOSPI/KOSDAQ 시장 전체의 부정적 뉴스를 일간 모니터링합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"securities.market:KOSPI and polarity.name:부정",count=100,page=1,date_from=20250224,date_to=20250228)
```

**결과:** 593건 (최근 1주)

**KOSDAQ 별도 모니터링:**
```
DocumentSearch(["news"],[],"securities.market:KOSDAQ and polarity.name:부정",count=100,page=1,date_from=20250224,date_to=20250228)
```

---

## 4. ESG 지배구조 이슈 감시

지배구조 관련 부정 뉴스를 모니터링하여 불공정거래 조기 감지에 활용합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"esg.category.name:지배구조 and esg.polarity.name:부정",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 970건

**환경/사회 이슈 병행 모니터링:**
```
# 환경 부정
DocumentSearch(["news"],[],"esg.category.name:환경 and esg.polarity.name:부정",count=100,page=1,date_from=20250201,date_to=20250228)

# 사회 부정
DocumentSearch(["news"],[],"esg.category.name:사회 and esg.polarity.name:부정",count=100,page=1,date_from=20250201,date_to=20250228)
```

---

## 5. 공시/IR 문서 키워드 검색

실제 공시 문서에서 특정 키워드를 직접 검색합니다.

**쿼리:**
```
DocumentSearch(["company"],["disclosure"],"인수 or 합병 or 분할",count=100,page=1,date_from=20250101,date_to=20250228)
```

**결과:** 13,780건

**공시 vs 뉴스 비교 활용:**
- 뉴스에서 인수합병 보도가 나왔는데 공시가 없으면 → 조회공시 대상
- 공시가 있는데 뉴스 보도 시점이 공시보다 앞서면 → 미공개정보 이용 의심

---

## 6. 테마/섹터 뉴스 트렌드

특정 테마(AI, 반도체, 전기차 등)에 대한 뉴스 건수 추이를 분석합니다.

**쿼리:**
```
DocumentTrends(["news"],["economy"],"AI and 반도체",interval="1w",date_from=20250101,date_to=20250228)
```

**변형:**
```
# 월별 트렌드
DocumentTrends(["news"],["economy"],"전기차",interval="1M",date_from=20240301,date_to=20250228)

# 일별 트렌드 (단기 급증 감지)
DocumentTrends(["news"],[],"securities.name:삼성전자",interval="1d",date_from=20250201,date_to=20250228)
```

**활용:** 뉴스 급증 테마 → 해당 테마 관련 종목의 주가/거래량 이상 여부 점검

---

## 7. 뉴스 언급 빈도 상위 종목

당일 또는 주간 가장 많이 보도된 종목을 집계합니다.

**KOSPI:**
```
DocumentAggregation(["news"],[],"securities.market:KOSPI","securities.name:20",date_from=20250224,date_to=20250228)
```

**KOSDAQ:**
```
DocumentAggregation(["news"],[],"securities.market:KOSDAQ","securities.name:20",date_from=20250224,date_to=20250228)
```

**결과 예시 (KOSPI, 2025-02-24~28):**
| 순위 | 종목 | 뉴스 건수 |
|------|------|----------|
| 1 | DB | 3,582 |
| 2 | NAVER | 2,764 |
| 3 | LG | 862 |

**전체 시장 (경제 뉴스 한정):**
```
DocumentAggregation(["news"],["economy"],"securities.market:(KOSPI or KOSDAQ)","securities.name:30",date_from=20250227,date_to=20250228)
```

**활용:** 뉴스 언급량 급증 종목 → 주가/거래량 이상 여부 크로스체크

---

## 8. 기업 감성 추이 모니터링

특정 기업에 대한 뉴스 감성(긍정/부정) 변화를 일별/월별로 추적합니다.

**월별 추이:**
```
GetSentimentScore("삼성전자",interval="1M",date_from=20240701,date_to=20250228)
```

**일별 추이 (단기 급변 감지):**
```
GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)
```

**결과 예시 (일별):**
| 날짜 | 감성트렌드 | 긍정 | 부정 |
|------|-----------|------|------|
| 2025-02-14 | 4.063 | 15 | 4 |
| 2025-02-17 | 3.440 | 38 | 4 |
| 2025-02-18 | 6.546 | 113 | 7 |

**활용:**
- 감성 점수 급락일 → 해당일 뉴스 내용 확인
- 감성 하락 + 주가 하락 → 정상적 시장 반응
- 감성 하락 + 주가 상승 → 이상 거래 의심

---

## 9. 불공정거래 관련 뉴스

시세조종, 내부자거래, 불공정거래 관련 뉴스를 검색합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(시세조종 or 불공정거래 or 내부자거래) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 823건 (최근 6개월)

**주의:** 기간이 1년을 초과하면 오류 발생. 6개월 단위로 조회 권장.

---

## 10. 대량보유/주주변동 뉴스

지분 변동, 최대주주 변경 관련 뉴스를 모니터링합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(대량보유 or 지분 or 주주 or 최대주주) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 916건

---

## 11. 증권사 리포트 검색

특정 종목에 대한 증권사 분석 리포트를 조회합니다.

**쿼리:**
```
DocumentSearch(["research"],["company"],"securities.name:SK하이닉스",count=50,page=1,date_from=20250101,date_to=20250228)
```

**결과:** 8건

---

## 12. KOSDAQ 부정 뉴스 주별 트렌드

KOSDAQ 시장의 부정적 뉴스 추이를 주 단위로 모니터링합니다.

**쿼리:**
```
DocumentTrends(["news"],[],"securities.market:KOSDAQ and polarity.name:부정",interval="1w",date_from=20250101,date_to=20250228)
```

**결과 예시:**
| 주차 | 건수 |
|------|------|
| 2025-01-06 | 44 |
| 2025-01-13 | 108 |
| 2025-02-03 | 188 |
| 2025-02-10 | 336 |
| 2025-02-24 | 280 |

**활용:** 부정 뉴스 급증 주차 → 해당 주의 종목별 상세 검색으로 원인 파악

---

## 13. 경영진 관련 뉴스

특정 경영진/인물과 기업을 결합하여 뉴스를 검색합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"이재용 and securities.name:삼성전자",count=100,page=1,date_from=20250101,date_to=20250228)
```

**결과:** 1,347건

---

## 14. 횡령/배임 관련 뉴스

상장기업 관련 횡령, 배임 뉴스를 검색합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(횡령 or 배임 or 사기) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 1,898건 (6개월)

---

## 15. 관리종목 지정 관련 뉴스

관리종목 지정/해제 관련 뉴스를 모니터링합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:관리종목 and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 34건

---

## 16. 감사의견 관련 뉴스

감사의견 비적정(한정/거절) 관련 뉴스를 검색합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(감사의견 or 한정의견 or 의견거절) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 3건

---

## 17. SPAC 합병 관련 뉴스

SPAC(기업인수목적회사) 합병 관련 뉴스를 모니터링합니다.

**쿼리:**
```
DocumentSearch(["news"],[],"title:(SPAC or 스팩) and securities.market:KOSDAQ",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 155건

---

## 18. 배당 관련 뉴스

상장기업의 배당 결정/변경 관련 뉴스를 모니터링합니다.

**쿼리:**
```
DocumentSearch(["news"],["economy"],"title:배당 and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250101,date_to=20250228)
```

**결과:** 974건

---

## API 제한사항 (중요)

| 제한 | 설명 |
|------|------|
| 기간 제한 | DocumentSearch는 **최대 1년** 이내 기간만 검색 가능 |
| 시간대 필터 | `created_at` 필드를 query 내에서 직접 사용하면 문법 오류 발생. `date_from`/`date_to` 파라미터 사용 권장 |
| 근접 검색 | `"키워드1 키워드2"~N` 형식의 근접검색은 한글 키워드에서 오류 가능 |
| 인물 엔티티 | `named_entities.entities.person.name` 필드는 일부 인물에 대해 빈 결과 반환 가능. 본문 검색(`content:인물명`)으로 대체 |

---

## 일일 모니터링 루틴 (권장)

```
1. 장 시작 전 (08:00)
   - 전일 부정 뉴스 확인 (시나리오 3)
   - 뉴스 언급 상위 종목 확인 (시나리오 7)
   - 조회공시 후보 뉴스 검색 (시나리오 1)

2. 장중 (09:00~15:30)
   - 특정 날짜 경제 뉴스 실시간 확인
   - 주가급변 종목 뉴스 검색 (시나리오 2)
   - 불공정거래 관련 뉴스 확인 (시나리오 9)

3. 장 마감 후 (16:00)
   - 당일 뉴스 트렌드 정리 (시나리오 6)
   - 기업 감성 변화 확인 (시나리오 8)
   - 공시 vs 뉴스 비교 (시나리오 5)
```
