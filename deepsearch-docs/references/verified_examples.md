# 검증된 사용 사례 (문서 검색)

모든 사례는 실제 API 호출로 검증되었습니다.

---

## 사례 1: 삼성전자 반도체 관련 경제 뉴스 (기간 지정)

**자연어:** "삼성전자의 2024년 6월 반도체 관련 경제 뉴스를 검색해줘"

**쿼리:**
```
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=100,page=1,date_from=20240601,date_to=20240630)
```

**결과:** 총 1,224건 검색됨

---

## 사례 2: ESG 환경 긍정 뉴스

**자연어:** "2024년 1월 환경 관련 긍정적인 ESG 뉴스를 찾아줘"

**쿼리:**
```
DocumentSearch(["news"],[],"esg.category.name:환경 and esg.polarity.name:긍정",count=100,page=1,date_from=20240101,date_to=20240131)
```

**결과:** 총 2,753건 검색됨

---

## 사례 3: 삼성전자 월별 감성(긍부정) 추이

**자연어:** "2024년 삼성전자 뉴스의 월별 감성 분석 추이를 보여줘"

**쿼리:**
```
GetSentimentScore("삼성전자",interval="1M",date_from=20240101,date_to=20241231)
```

**결과:** 12개월 데이터 반환 (date, trend, total_count, no_negatives, no_neutral, no_positives)

---

## 사례 4: 반도체 유사 키워드 탐색

**자연어:** "반도체와 유사한 키워드를 찾아줘"

**쿼리:**
```
SimilarKeywords("반도체",max_count=5)
```

**결과:** 파워리, 메모리, 메모리반도체, 시스템, 시스템반도체 등

---

## 사례 5: 전기차 뉴스에서 가장 많이 언급된 기업

**자연어:** "2024년 상반기 전기차 뉴스에서 가장 많이 언급된 기업 10개를 알려줘"

**쿼리:**
```
DocumentAggregation(["news"],[],"전기차","named_entities.entities.company.name:10",date_from=20240101,date_to=20240630)
```

**결과:** 현대자동차(11,626건), 테슬라코리아(10,114건), 기아오토모빌러스(3,807건), 한국전력(3,101건), 포스코퓨처엑스(3,015건) 등

---

## 사례 6: AI 뉴스 월별 트렌드

**자연어:** "2024년 경제뉴스에서 AI 키워드 월별 트렌드를 분석해줘"

**쿼리:**
```
DocumentTrends(["news"],["economy"],"AI",interval="1M",date_from=20240101,date_to=20241231)
```

**결과:** 월별 문서 건수 트렌드 데이터 반환

---

## 사례 7: 특정 언론사의 특정 기업 뉴스

**자연어:** "매일경제에서 보도한 삼성전자 관련 뉴스를 검색해줘"

**쿼리:**
```
DocumentSearch(["news"],[],"publisher.raw:('매일경제') and securities.name:삼성전자",count=100,page=1)
```

---

## 사례 8: 제목에 특정 키워드가 포함된 뉴스

**자연어:** "제목에 '수출 호조'가 포함된 경제 뉴스를 찾아줘"

**쿼리:**
```
DocumentSearch(["news"],["economy"],"title:(수출 and 호조)",count=100,page=1)
```

---

## 사례 9: 부정적 뉴스 필터링

**자연어:** "SK하이닉스 관련 부정적 뉴스를 검색해줘"

**쿼리:**
```
DocumentSearch(["news"],[],"securities.name:SK하이닉스 and polarity.name:부정",count=100,page=1)
```

---

## 사례 10: 증권사 리포트 검색

**자연어:** "삼성전자 관련 증권사 리포트를 검색해줘"

**쿼리:**
```
DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=50,page=1)
```

---

# KRX 업무 활용 사례

---

## 사례 11: 조회공시 후보 뉴스 탐지 (인수합병/매각)

**업무:** 공시되지 않은 인수합병, 매각 관련 루머 뉴스 검색

**쿼리:**
```
DocumentSearch(["news"],[],"title:(인수 or 합병 or M&A or 매각) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 1,232건

---

## 사례 12: KOSPI 종목 부정 뉴스 모니터링

**업무:** 시장 전반 부정적 뉴스 일간 모니터링

**쿼리:**
```
DocumentSearch(["news"],[],"securities.market:KOSPI and polarity.name:부정",count=100,page=1,date_from=20250224,date_to=20250228)
```

**결과:** 593건 (최근 1주)

---

## 사례 13: ESG 지배구조 부정 뉴스

**업무:** 불공정거래 조기 감지를 위한 지배구조 이슈 감시

**쿼리:**
```
DocumentSearch(["news"],[],"esg.category.name:지배구조 and esg.polarity.name:부정",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 970건

---

## 사례 14: 공시 문서에서 키워드 직접 검색

**업무:** 인수/합병/분할 관련 공시 문서 검색

**쿼리:**
```
DocumentSearch(["company"],["disclosure"],"인수 or 합병 or 분할",count=100,page=1,date_from=20250101,date_to=20250228)
```

**결과:** 13,780건

---

## 사례 15: 뉴스 언급 빈도 상위 종목 (KOSPI)

**업무:** 당일/주간 가장 많이 보도된 종목 파악

**쿼리:**
```
DocumentAggregation(["news"],[],"securities.market:KOSPI","securities.name:20",date_from=20250224,date_to=20250228)
```

**결과:** 상위 20개 종목 (DB 3,582건, NAVER 2,764건, LG 862건 등)

---

## 사례 16: 기업 일별 감성 급변 감지

**업무:** 특정 기업의 뉴스 감성 급변 모니터링

**쿼리:**
```
GetSentimentScore("삼성전자",interval="1d",date_from=20250214,date_to=20250228)
```

**결과:** 15일간 일별 감성 데이터 (trend, 긍정/부정 건수)

---

## 사례 17: 불공정거래 관련 뉴스

**업무:** 시세조종, 내부자거래 관련 뉴스 검색

**쿼리:**
```
DocumentSearch(["news"],[],"title:(시세조종 or 불공정거래 or 내부자거래) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 823건 (최근 6개월)

**주의:** 기간 1년 초과 시 오류 발생. 6개월 단위로 조회 권장.

---

## 사례 18: 대량보유/주주변동 뉴스

**업무:** 지분 변동, 최대주주 변경 관련 뉴스 모니터링

**쿼리:**
```
DocumentSearch(["news"],[],"title:(대량보유 or 지분 or 주주 or 최대주주) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```

**결과:** 916건

---

## 사례 19: KOSDAQ 부정 뉴스 주별 트렌드

**업무:** KOSDAQ 시장의 부정 뉴스 추이 모니터링

**쿼리:**
```
DocumentTrends(["news"],[],"securities.market:KOSDAQ and polarity.name:부정",interval="1w",date_from=20250101,date_to=20250228)
```

**결과:** 주별 부정 뉴스 건수 추이 (1월 44→108→137건, 2월 188→336→280건)

---

## 사례 20: 횡령/배임 뉴스 모니터링

**업무:** 상장기업 관련 횡령, 배임, 사기 뉴스 검색

**쿼리:**
```
DocumentSearch(["news"],[],"title:(횡령 or 배임 or 사기) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 1,898건 (6개월)

---

## 사례 21: 관리종목/상장폐지 관련 뉴스

**업무:** 관리종목 지정/해제 및 상장폐지 관련 뉴스

**쿼리:**
```
DocumentSearch(["news"],[],"title:(관리종목 or 상장폐지) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 관리종목 34건, 상장폐지 68건

---

## 사례 22: SPAC 합병 관련 뉴스

**업무:** SPAC 합병 관련 KOSDAQ 뉴스 모니터링

**쿼리:**
```
DocumentSearch(["news"],[],"title:(SPAC or 스팩) and securities.market:KOSDAQ",count=100,page=1,date_from=20240901,date_to=20250228)
```

**결과:** 155건

---

## 사례 23: 바이오 KOSDAQ 종목 일별 뉴스 트렌드

**업무:** 바이오 테마 KOSDAQ 종목 뉴스 추이 파악

**쿼리:**
```
DocumentTrends(["news"],["economy"],"바이오 and securities.market:KOSDAQ",interval="1d",date_from=20250201,date_to=20250228)
```

**결과:** 28일간 일별 뉴스 건수 트렌드
