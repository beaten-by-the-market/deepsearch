# 검증된 사용 사례 (통합)

모든 사례는 실제 API 호출로 검증되었습니다.

---

# 문서 검색 사례

## 사례 1: 삼성전자 반도체 뉴스 (기간 지정)
```
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=100,page=1,date_from=20240601,date_to=20240630)
```
→ 1,224건

## 사례 2: ESG 환경 긍정 뉴스
```
DocumentSearch(["news"],[],"esg.category.name:환경 and esg.polarity.name:긍정",count=100,page=1,date_from=20240101,date_to=20240131)
```
→ 2,753건

## 사례 3: 감성(긍부정) 추이
```
GetSentimentScore("삼성전자",interval="1M",date_from=20240101,date_to=20241231)
```
→ 12개월 감성 데이터

## 사례 4: 전기차 뉴스 최다 언급 기업
```
DocumentAggregation(["news"],[],"전기차","named_entities.entities.company.name:10",date_from=20240101,date_to=20240630)
```
→ 현대자동차(11,626건), 테슬라코리아(10,114건) 등

## 사례 5: AI 뉴스 월별 트렌드
```
DocumentTrends(["news"],["economy"],"AI",interval="1M",date_from=20240101,date_to=20241231)
```

## 사례 6: 특정 언론사 기업 뉴스
```
DocumentSearch(["news"],[],"publisher.raw:('매일경제') and securities.name:삼성전자",count=100,page=1)
```

## 사례 7: 부정적 뉴스 필터
```
DocumentSearch(["news"],[],"securities.name:SK하이닉스 and polarity.name:부정",count=100,page=1)
```

## 사례 8: 증권사 리포트
```
DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=50,page=1)
```

---

# 기업/재무 사례

> **원칙:** 재무제표 데이터(매출, 영업이익, 자산 등)는 반드시 `GetFinancialStatements` API 함수로 조회.
> 자연어 쿼리는 주가/시장 데이터(종가, PER, PBR, 시가총액)에만 사용.

## 사례 9: 재무제표 조회 (GetFinancialStatements)
```
GetAvailableFinancialStatements(KRX:000660)
GetFinancialStatements(SK하이닉스, report_type="IFRS", consolidated=True, is_annual=False, date_from=2023-01-01, date_to=2024-12-31)
```
→ 507개 계정항목 반환, 분기 포함. 영업이익 항목 필터링하여 추출

## 사례 10: 일별 종가 (자연어 — 주가/시장 데이터)
```
삼성전자 종가 2024-06-01-2024-06-30
```
→ 20거래일

## 사례 11: 복수 기업 재무 비교 (GetFinancialStatements 개별 호출)
```
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(LG전자, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(SK하이닉스, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
```
→ 각각 507개 항목 반환, 매출·영업이익 등 필요 항목 필터링하여 비교

## 사례 12: 애널리스트 목표가
```
SearchTargetPrices("005930",date_from=20240101,date_to=20240630)
```
→ 29건

## 사례 13: 기업그룹 계열사
```
FindConglomerateByName("삼성")
```

## 사례 14: 국민연금 보유 기업
```
"국민연금" 주주 기업
```

---

# 세부 재무계정 사례

> **원칙:** 아래 모든 세부 계정은 `GetFinancialStatements`로 전체 재무제표(507개 항목)를 조회한 뒤, `name_ko` 필드에서 필터링하여 추출합니다.

## 사례 15: 건설업 세부계정 (GetFinancialStatements)
```
GetFinancialStatements(현대건설, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ 507개 항목에서 name_ko로 필터링:
  - "미청구공사" → 2.28조(2020) → 5.33조(2023) → 4.68조(2024)
  - "하자보수충당부채" → 3,287억(2020) → 4,589억(2024)
  - "초과청구공사" → 5년 데이터
  - "공사미수금" → 1.23조(2020) → 5.02조(2024)
```

## 사례 16: 금융업 세부계정 (GetFinancialStatements)
```
GetFinancialStatements(KB금융, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ 507개 항목에서 필터링:
  - "대손충당금" → 3.28조(2020) → 5.63조(2024)
  - "충당부채" → 7,641억(2020) → 9,593억(2024)
```

## 사례 17: 재무상태표 세부항목 (GetFinancialStatements)
```
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, report_ids="BalanceSheet", date_from=2020-01-01, date_to=2024-12-31)
→ 재무상태표에서 필터링:
  - "재고자산", "매출채권", "유형자산" → 유형자산 128.9조(2020) → 205.9조(2024)
  - "현금및현금성자산", "단기차입금", "장기차입금"
  - "이익잉여금" → 271조(2020), "자본잉여금" → 4.4조 (불변)
  - "유동자산", "유동부채", "비유동부채" → 유동자산 198~227조
```

## 사례 18: 손익계산서 / 현금흐름표 (GetFinancialStatements)
```
GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, report_ids="Income", date_from=2020-01-01, date_to=2024-12-31)
→ "매출원가", "판매비와관리비", "매출총이익"

GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, report_ids="CashFlow", date_from=2020-01-01, date_to=2024-12-31)
→ "영업활동현금흐름" 65.2조, "투자활동현금흐름" -53.6조, "재무활동현금흐름" -8.3조 (2020)
```

## 사례 19: 바이오 세부계정 (GetFinancialStatements)
```
GetFinancialStatements(셀트리온, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ "개발비" 1.09~1.39조, "경상연구개발비" 1,714~1,997억

GetFinancialStatements(삼성바이오로직스, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ "개발비" 2.59~2.74조 (3년)
```

## 사례 20: IT 세부계정 (GetFinancialStatements)
```
GetFinancialStatements(카카오, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ "영업권" 2.69~3.70조, "선수수익" 1,445~1,501억
→ "전환사채" 827~4,609억(3년)
→ "이연법인세자산" 518~4,981억, "이연법인세부채" 2,452~7,262억
```

---

# 스크리닝/분석 사례

## 사례 32: 고수익 대형 기업 (Buffett 스타일)
```
매출 > 1000000000000 and 영업이익 / 매출 > 0.15
```
→ 60개 기업

## 사례 33: 매출 상위 10개
```
Top(매출액, 10)
```

## 사례 34: 전년대비 매출 50% 성장
```
2023 매출 > 2022 매출 * 1.5
```
→ 4,620개 기업

## 사례 35: 적자전환 스크리닝
```bash
python scripts/turnaround_screener.py "API_KEY" loss 5000
```
→ 32개 적자전환 (현대건설, 한화솔루션, 에코프로비엠, 엔씨소프트 등)

## 사례 36: 흑자전환 스크리닝
```bash
python scripts/turnaround_screener.py "API_KEY" profit 1000
```
→ SK바이오팜, SK스퀘어, 이마트, 금호석유 등

## 사례 37: 매출 급감 상장기업
```
상장 기업 and 2024 매출 < 2023 매출 * 0.7 and 매출 > 100000000000
```
→ 26개 기업

## 사례 38: 코스닥 전체 상장기업 목록
```
코스닥 상장 기업
```
→ 1,820개 (한글 `코스닥`으로 써야 함, `KOSDAQ` 안 됨)

## 사례 39: 코스피 전체 상장기업 목록
```
코스피 상장 기업
```
→ 2,404개

## 사례 40: 코스닥 매출 1000억 이상 기업
```
코스닥 상장 기업 and 매출액 > 100000000000
```
→ 697개

## 사례 41: 코스닥 시가총액 상위 150개 등락률 (전용 스크립트)
```bash
python scripts/market_top_movers.py "API_KEY" kosdaq 150 2025-02-27
```
→ 시가총액 상위 150개 중 최다 하락/상승 10개씩 출력
→ 내부: 전체 종목 조회 → 병렬 시가총액 수집 → 정렬

---

# 비상장사 재무제표 사례

> **원칙:** 비상장사도 상장사와 동일하게 `GetFinancialStatements` API 함수로 조회합니다.

## 사례 42: 비상장사 엔티티 검색
```
FindEntity("Financial","채비*")
```
→ 12개 엔티티 검색됨 (비상장 외감 기업)

## 사례 43: 비상장사 재무제표 확인 및 조회
```
# 1단계: 사용 가능한 재무제표 확인
GetAvailableFinancialStatements(NICE:HQ4658)
→ consolidated=False만 존재 (별도 재무제표만 있음)

# 2단계: 재무제표 조회
GetFinancialStatements(채비, consolidated=False, date_from=2020-01-01, date_to=2024-12-31)
```
→ 507개 항목 반환. 매출 375억(2020) → 850억(2024)
→ 2022년부터 영업적자 전환
→ 자본: 2023년 -958억(자본잠식) → 2024년 968억 회복 (유상증자)

## 사례 44: 비상장사 넓은 범위 조회 (데이터 시작 연도 확인)
```
GetFinancialStatements(채비, consolidated=False, date_from=2010-01-01, date_to=2024-12-31)
```
→ 실제 데이터는 2016년부터 반환 (외감 시작 연도). 2010~2015 데이터 없음

## 사례 45: 비상장사 분기 데이터 (제한적)
```
GetFinancialStatements(채비, consolidated=False, is_annual=False)
```
→ 비상장사는 분기 데이터 매우 제한적 (1~2건만 반환될 수 있음)

---

# 멀티스텝 분석 사례

## 사례 50: 뉴스+주가 결합 (삼성전자 반도체)

**1단계:**
```
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and 반도체",count=5,page=1,date_from=20240601,date_to=20240630)
```
→ 1,224건 뉴스 확인

**2단계:**
```
삼성전자 종가 2024-06-01-2024-06-30
```
→ 20거래일 종가로 뉴스 전후 주가 변동 확인

## 사례 51: Graham 가치투자 (2단계)

**1단계:**
```
매출 > 1000000000000 and 영업이익 / 매출 > 0.1 and 당기순이익 > 0
```

**2단계:**
```
SK하이닉스 PER
SK하이닉스 PBR
```
→ PER < 15, PBR < 1.5 충족 여부 확인

## 사례 52: 포트폴리오 수익률 시뮬레이션 (3단계)

**1단계:** `매출 > 1조 and 영업이익률 > 15%` → 60개 기업
**2단계:** 각 기업 연초/연말 종가 조회
**3단계:** (연말-연초)/연초 × 100 = 수익률

## 사례 53: IPO Peer 비교 분석 (채비 vs EV 충전 상장사, 5단계)

**배경:** 채비(NICE:HQ4658) - 전기차 급속/완속 충전기 제조, 2025.07 코스닥 상장예비심사 신청

**1단계: 기업 프로필**
```
GetCompanySummary(채비)
```
→ 업종: 전기차 충전기/배전반 제조 | 업종코드: KRI:10C2811900 | 설립: 2016.05 | 직원 319명

**2단계: Peer 후보 탐색**
```
DocumentSearch(["news"],[],"전기차 충전기 제조 상장 IPO and created_at:[\"2021-01-01\" to \"2025-12-31\"]",count=20,page=1)
```
→ 에스트래픽(KRX:234300), 그리드위즈(KRX:453450, IPO 2024.06), 위츠(KRX:459100, IPO 2024.11) 확인

**3단계: 기본 재무 비교 (GetFinancialStatements, 2024년, 억원)**
```
GetFinancialStatements(채비, consolidated=False, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(에스트래픽, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(그리드위즈, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
GetFinancialStatements(위츠, report_type="IFRS", consolidated=True, date_from=2020-01-01, date_to=2024-12-31)
→ 각 507개 항목에서 매출액, 영업이익, 당기순이익 필터링
```
| 기업 | 매출 | 영업이익 | 순이익 | 영업이익률 |
|------|------|---------|--------|----------|
| 채비 | 850 | -275 | -544 | -32.5% |
| 에스트래픽 | 1,890 | 113 | 59 | 6.0% |
| 그리드위즈 | 1,246 | -43 | -27 | -3.5% |
| 위츠 | 907 | 21 | 15 | 2.4% |

**4단계: 세부 계정 비교 (GetFinancialStatements, 2024년, 억원)**
```
→ 3단계에서 받은 507개 항목에서 매출원가, 매출총이익, 재고자산, 매출채권 등 필터링
```
| 항목 | 채비 | 에스트래픽 | 그리드위즈 | 위츠 |
|------|------|----------|----------|------|
| 매출총이익률 | 3.4% | 19.1% | 16.6% | 22.2% |
| 자본총계 | 968 | 984 | 1,303 | 408 |
| 영업CF | -119 | 141 | 25 | -40 |
| 유형자산 | 1,312 | 414 | 239 | 244 |
| 차입금합계 | 449 | 130 | 5 | 344 |

**5단계: 종합 분석**
- 매출총이익률: 채비(3.4%)가 Peer 평균(19%)의 1/5 → 원가 경쟁력 취약
- 유형자산 1,312억(Peer 대비 3~5배) → 충전인프라 선투자 모델, 수확기 미도달
- 2023년 자본잠식(-958억) → 2024년 유상증자로 회복(+968억)
- 영업CF 3년 연속 적자 → 투자 자금 외부 조달 의존

## 사례 54: 주가급변 원인분석 (KRX, 2단계)

**1단계:**
```
DocumentSearch(["news"],["economy"],"securities.name:에코프로비엠",count=100,page=1,date_from=20250201,date_to=20250228)
```
→ 69건 뉴스

**2단계:**
```
에코프로비엠 종가 거래량 2025-02-24-2025-02-28
```
→ 뉴스 발생 전 거래량 급증 → 내부자거래 의심

---

# KRX 업무 사례

## 사례 55: 조회공시 후보 뉴스
```
DocumentSearch(["news"],[],"title:(인수 or 합병 or M&A or 매각) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20250201,date_to=20250228)
```
→ 1,232건

## 사례 56: KOSPI 부정 뉴스 모니터링
```
DocumentSearch(["news"],[],"securities.market:KOSPI and polarity.name:부정",count=100,page=1,date_from=20250224,date_to=20250228)
```
→ 593건

## 사례 57: ESG 지배구조 부정
```
DocumentSearch(["news"],[],"esg.category.name:지배구조 and esg.polarity.name:부정",count=100,page=1,date_from=20250201,date_to=20250228)
```
→ 970건

## 사례 58: 영업적자 대형 상장기업
```
영업이익 < 0 and 매출 > 500000000000
```
→ 152개 기업

## 사례 59: 자본잠식 우려
```
자본 < 0 and 매출 > 10000000000
```
→ 1,567개 기업

## 사례 60: 불공정거래 뉴스
```
DocumentSearch(["news"],[],"title:(시세조종 or 불공정거래 or 내부자거래) and securities.market:(KOSPI or KOSDAQ)",count=100,page=1,date_from=20240901,date_to=20250228)
```
→ 823건

---

# 시황분석 (Daily Market Overview) 사례

## 사례 61: 일일 시황분석 리포트 생성
```bash
python {baseDir}/scripts/market_overview.py "API_KEY" 2026-02-27
```
→ 7/7 섹션 성공 (28초)
- 시장 지수: KOSPI 6,244.13 (-1.00%), KOSDAQ 1,192.78 (+0.39%), KOSPI200 933.34 (-1.13%)
- 규모별 동향: 강세 코스닥 대형주(+1.20%), 약세 코스닥 소형주(-1.08%)
- 시총 상위 등락: 상승 현대차(+10.67%), LG화학(+7.05%) / 하락 한국전력(-7.58%), SK스퀘어(-5.01%)
- 뉴스 언급 상위: 현대차(116건), 삼성전자(103건), NAVER(89건)
- 주요 뉴스: 1,794건 (국민연금 수익률, 코인 유출, 구글 지도 반출 등)
- 트렌딩 토픽: 한전 13.5조 이익, 갤럭시 S26, 쿠팡 과징금 등 10개
- 시장 감성: 긍정 우세 (긍정 37.1%, 부정 4.6%, 중립 58.3%)

## 사례 62: 주말 날짜 시황분석 (비거래일 처리)
```bash
python {baseDir}/scripts/market_overview.py "API_KEY" 2026-02-22
```
→ 7/7 섹션 성공
- 시장 데이터: 직전 거래일(2026-02-20 금요일) 기준으로 자동 조회
- 뉴스/토픽: 2026-02-22 (일요일) 날짜 그대로 조회 (465건)
