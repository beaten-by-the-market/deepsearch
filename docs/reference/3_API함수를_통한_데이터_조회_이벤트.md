<!-- 이 파일은 docs/reference/sync_from_gitbook.py로 생성합니다 (2026-11-25). 원문: https://help.deepsearch.com/dp/ — 포트폴리오 성과, 주식·채권 이벤트 분석. 직접 고치지 말고, 레포 메모는 repo-memo 마커 안에 쓰세요. -->

<!-- source: https://help.deepsearch.com/dp/api/func/event -->
# 이벤트

## 주식 포트폴리오 성과 분석

```
ComputePortfolioReturns
AnalyzePortfolioReturns
```

{% content-ref url="/pages/-M27ANGGw4RaKGflGLbv" %}
[주식 포트폴리오 성과 분석](https://help.deepsearch.com/dp/api/func/event/portfolio.md)
{% endcontent-ref %}

## 주식 시장 이벤트 분석&#x20;

```
ComputeEventDayStockReturns
ComputeStockReturnCorrelationWith
GetIndustryReturnsOnEventDates
GetCumulativeIndustryReturns
```

{% content-ref url="/pages/-M27AVI6G0-697tixJVu" %}
[주식 시장 이벤트 분석](https://help.deepsearch.com/dp/api/func/event/stock.md)
{% endcontent-ref %}

## 채권 시장 이벤트 분석

```
GetBondYieldChangesPerIssuer
GetBondYieldChangesPerClassification
GetBondYieldChangesPerIndustry
```

{% content-ref url="/pages/-M1yWAfWfbIDf5\_Ljonu" %}
[채권 시장 이벤트 분석](https://help.deepsearch.com/dp/api/func/event/bond.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/event/portfolio -->
# 주식 포트폴리오 성과 분석

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-M27xk1KShq8ORAZJ9JM" %}
[ComputePortfolioReturns](https://help.deepsearch.com/dp/api/func/event/portfolio/computeportfolioreturns.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xkrE-LQgngH4GtpC" %}
[AnalyzePortfolioReturns](https://help.deepsearch.com/dp/api/func/event/portfolio/analyzeportfolioreturns.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/event/portfolio/computeportfolioreturns -->
# ComputePortfolioReturns

포트폴리오에 대한 과거 일정 기간 동안의 수익률을 계산합니다.

### Function specification

```
ComputePortfolioReturns(entities, date_from, date_to, weight,
                rebalancing_freq="daily", rebalancing_date=0, transaction_cost=0)
```

### Parameters

| Parameter           | Type            | Description                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| entities            | list of strings | 종목명 리스                                                                                                                                                                                                                                                                                                                                                                                                        |
| date\_from/date\_to | date            | 수익률 계산 기간                                                                                                                                                                                                                                                                                                                                                                                                     |
| weight              | string          | 비중 결정 방식 ( "equal", "value", "relevance" )                                                                                                                                                                                                                                                                                                                                                                    |
| rebalancing\_freq   | string          | 리밸런싱 주기 ( "daily","monthly", "quarterly", "semi-annual", "annual", "no" )                                                                                                                                                                                                                                                                                                                                     |
| rebalancing\_date   | int             | the i-th date of portfolio rebalancing within the given frequency. For example, if (quarterly, 2) is given, it means the portfolio is to be rebalanced at the end of 2nd month in a quarter, e.g., Feb 28, May 31, Aug 31, and Nov 30. Similarly, if (monthly, 25) is given, the portfolio will be rebalaned at the 25th of every month. The default value is zero, which indicates the last date of a cycle. |
| transaction\_cost   | float           | 거래 비용 (%) ex) 1.0 -> 1.0%                                                                                                                                                                                                                                                                                                                                                                                     |

### Result

{% content-ref url="/pages/-MX0u3YRe2FnOzWXDDvW" %}
[Result:PortfolioReturns](https://help.deepsearch.com/dp/api/result_layout/result-portfolioreturns.md)
{% endcontent-ref %}

### Examples

```
> ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, 2018-12-31, "equal")
> ComputePortfolioReturns(상위(인공지능 관련 기업,10), 2013-01-01, 2018-12-31, "equal")
> ComputePortfolioReturns(시가총액 > 1000000000000, 2013-01-01, 2018-12-31, "equal")
> ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, 2018-12-31, "equal", "daily")
> ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, 2018-12-31, "equal", "no")
> ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, 2018-12-31, "equal", "monthly")
```

###

<!-- source: https://help.deepsearch.com/dp/api/func/event/portfolio/analyzeportfolioreturns -->
# AnalyzePortfolioReturns

포트폴리오에 대한 결과를 벤치마크 지수와 비교하여 분석합니다.

### Function specification

```
AnalyzePortfolioReturns(portfolio, benchmark)
```

### Parameters

| Parameter | Type             | Description                   |
| --------- | ---------------- | ----------------------------- |
| portfolio | PortfolioReturns | ComputePortfoilioReturns() 결과 |
| benchmark | string           | 벤치마크 인덱스 : KOSPI, KOSDAQ      |

### Result

{% content-ref url="/pages/-MX1W7NNFMRmLnJn42NC" %}
[Result:PortfolioAnalysis](https://help.deepsearch.com/dp/api/result_layout/result-portfolioanalysis.md)
{% endcontent-ref %}

### Examples

```
> AnalyzePortfolioReturns(ComputePortfolioReturns([삼성전자, LG전자, 네이버], 2013-01-01, \
            2018-12-31, "equal"), KOSPI)
> AnalyzePortfolioReturns(ComputePortfolioReturns(상위(인공지능 관련 기업,10), 2013-01-01, \
            2018-12-31, "equal"), KOSPI)
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 예시는 줄바꿈(`\`) 때문에 `SyntaxError`이고, 한 줄로 고쳐도 `AttributeError: 'str' object has no attribute 'date'`로 동작하지 않습니다. `ComputePortfolioReturns` 단독 호출은 정상입니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/stock -->
# 주식 시장 이벤트 분석

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-M27xmd2HdQq7J\_To4HY" %}
[ComputeEventDayStockReturns](https://help.deepsearch.com/dp/api/func/event/stock/computeeventdaystockreturns.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xmP7De-DNUel4i7w" %}
[ComputeStockReturnCorrelationWith](https://help.deepsearch.com/dp/api/func/event/stock/computestockreturncorrelationwith.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xmAlbuYmc5sHDBEf" %}
[GetIndustryReturnsOnEventDates](https://help.deepsearch.com/dp/api/func/event/stock/getindustryreturnsoneventdates.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xfVtg9oZaSC8wpNV" %}
[GetCumulativeIndustryReturns](https://help.deepsearch.com/dp/api/func/event/stock/getcumulativeindustryreturns.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/event/stock/computeeventdaystockreturns -->
# ComputeEventDayStockReturns

특정 이벤트 날짜의 종목별 수익률을 계산합니다.

### Function specification

```
ComputeEventDayStockReturns(event_dates)
```

### Parameters

| Parameter    | Type         | Description |
| ------------ | ------------ | ----------- |
| event\_dates | list of date | 이벤트 날짜      |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> ComputeEventDayStockReturns(2020-5-7)
...
symbol	entity_name	ComputeEventDayStockReturns(2020-05-07)
KRX:000020	동화약품	-0.02
KRX:000040	KR모터스	-0.02
KRX:00004217	KR모터스 1WR	0.00
KRX:000050	경방	0.04
KRX:000060	메리츠화재	0.00
KRX:000070	삼양홀딩스	0.01
KRX:000075	삼양홀딩스우	0.02
KRX:000080	하이트진로	0.02
KRX:000087	하이트진로2우B	0.01
KRX:000100	유한양행	0.00
KRX:000105	유한양행우	0.00
KRX:000120	CJ대한통운	-0.01
KRX:000140	하이트진로홀딩스	0.00
KRX:000145	하이트진로홀딩스우	-0.01
KRX:000150	두산	0.00
KRX:000155	두산우	0.00
KRX:000157	두산2우B	-0.01
KRX:000180	성창기업지주	0.00
KRX:000210	대림산업	-0.01
KRX:000215	대림산업우	-0.01
KRX:000220	유유제약	0.04
KRX:000225	유유제약1우	0.05
KRX:000227	유유제약2우B	0.05
KRX:000230	일동홀딩스	0.01
KRX:000240	한국테크놀로지그룹	0.01
KRX:000250	삼천당제약	0.00
KRX:000270	기아차	-0.01
KRX:000300	대유플러스	0.02
KRX:000320	노루홀딩스	0.02
KRX:000325	노루홀딩스우	0.00
KRX:000370	한화손해보험	0.00
KRX:000390	삼화페인트	0.02
KRX:000400	롯데손해보험	0.08
KRX:000430	대원강업	0.02
KRX:000440	중앙에너비스	0.01
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/event/stock/computestockreturncorrelationwith -->
# ComputeStockReturnCorrelationWith

특정 index 와 전체 상장 기업 주가와의 correlation 을 계산합니다.

### Function specification

```
ComputeStockReturnCorrelationWith(target=0, date_from=None, date_to=None)
```

### Parameters

| Parameter            | Type | Description          |
| -------------------- | ---- | -------------------- |
| target               | int  | target index. 하단 참조. |
| date\_from, date\_to | date | correlation 계산 기간    |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Target Index&#x20;

```
KOSPI = 0 
KOSDAQ = 1 
KOSPI200 = 2

USDKRW = 100
JPYKRW = 101
EURKRW = 102
CNYKRW = 103

BOND1Y = 200
BOND3Y = 201
BOND5Y = 202
```

### Examples

```
> ComputeStockReturnCorrelationWith(1)
...
symbol	entity_name	ComputeStockReturnCorrelationWith(1)
KRX:000020	동화약품	0.42
KRX:000040	KR모터스	0.36
KRX:0000401A	KR모터스 41R	1.00
KRX:00004217	KR모터스 1WR	0.02
KRX:000050	경방	0.41
KRX:000060	메리츠화재	0.48
KRX:000070	삼양홀딩스	0.61
KRX:000075	삼양홀딩스우	0.58
KRX:000080	하이트진로	0.52
KRX:000087	하이트진로2우B	0.62
KRX:000100	유한양행	0.56
KRX:000105	유한양행우	0.36
KRX:000120	CJ대한통운	0.36
KRX:000140	하이트진로홀딩스	0.16
KRX:000145	하이트진로홀딩스우	0.01
KRX:000150	두산	0.58
KRX:000155	두산우	0.54
KRX:000157	두산2우B	0.43
KRX:000180	성창기업지주	0.65
KRX:000210	대림산업	0.64
KRX:000215	대림산업우	0.64
KRX:000220	유유제약	0.71
KRX:000225	유유제약1우	0.71
...
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 예시 `ComputeStockReturnCorrelationWith(1)`은 90초 안에 응답이 없었고, 기간을 3개월로 줄이면 결과 pod 없이 끝났습니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/stock/getindustryreturnsoneventdates -->
# GetIndustryReturnsOnEventDates

특정 이벤트일의 산업별 수익률을 계산합니다.

### Function specification

```
GetIndustryReturnsOnEventDates(event_dates, level=0)
```

### Parameters

| Parameter    | Type         | Description |
| ------------ | ------------ | ----------- |
| event\_dates | list of date | 이벤트 날짜      |
| level        | level        | 산업 분류 레벨    |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> GetIndustryReturnsOnEventDates([2020-5-6,2020-5-7])
...
date	industry_id	ewret	vwret
2020-05-06	A	1.47	1.72
2020-05-06	B	0.37	0.61
2020-05-06	C	1.84	1.74
2020-05-06	D	0.26	-1.36
2020-05-06	E	4.72	5.12
2020-05-06	F	0.97	1.41
2020-05-06	G	1.80	2.89
2020-05-06	H	0.29	0.78
2020-05-06	I	2.60	2.88
2020-05-06	J	2.82	3.36
2020-05-06	K	1.31	1.32
2020-05-06	L	2.54	2.26
2020-05-06	M	2.52	3.15
2020-05-06	N	1.40	1.58
2020-05-06	P	1.06	2.95
2020-05-06	R	0.70	0.44
2020-05-06	S	6.15	0.51
2020-05-07	A	0.06	0.93
2020-05-07	B	-0.07	-0.12
2020-05-07	C	1.47	-0.05
2020-05-07	D	0.15	0.35
2020-05-07	E	1.00	0.60
2020-05-07	F	0.12	-0.37
2020-05-07	G	1.04	-0.88
2020-05-07	H	1.20	1.13
2020-05-07	I	5.52	6.47
2020-05-07	J	1.45	2.22
2020-05-07	K	0.33	0.06
2020-05-07	L	2.76	0.50
2020-05-07	M	1.18	1.31
2020-05-07	N	1.19	0.95
2020-05-07	P	1.51	0.15
2020-05-07	R	0.17	0.35
2020-05-07	S	-1.04	0.83
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 예시를 호출하면 서버 오류 `KeyError: industry_id`가 나서 동작하지 않습니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/stock/getcumulativeindustryreturns -->
# GetCumulativeIndustryReturns

특정 기간 동안의 산업별 수익률을 계산합니다.

### Function specification

```
GetCumulativeIndustryReturns(event_dates, level=0, industry_codes=None)
```

### Parameters

| Parameter       | Type         | Description |
| --------------- | ------------ | ----------- |
| event\_dates    | list of date | 이벤트 날짜      |
| level           | int          | 산업 분류 레벨    |
| industry\_codes | string       | 산업코드        |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> GetCumulativeIndustryReturns(2020-5-7,0,"A")
...
event_date	industry_id	date	ewval	vwval
2020-05-07	A	2020-04-02	83.54	80.64
2020-05-07	A	2020-04-03	84.33	81.52
2020-05-07	A	2020-04-06	88.45	84.16
2020-05-07	A	2020-04-07	88.26	83.42
2020-05-07	A	2020-04-08	88.58	84.35
2020-05-07	A	2020-04-09	89.51	85.38
2020-05-07	A	2020-04-10	90.79	86.79
2020-05-07	A	2020-04-13	90.31	86.38
2020-05-07	A	2020-04-14	92.01	87.40
2020-05-07	A	2020-04-16	93.41	87.00
2020-05-07	A	2020-04-17	93.61	87.96
2020-05-07	A	2020-04-20	95.46	88.80
2020-05-07	A	2020-04-21	93.09	87.94
2020-05-07	A	2020-04-22	94.08	89.93
2020-05-07	A	2020-04-23	97.70	93.80
2020-05-07	A	2020-04-24	96.33	94.62
2020-05-07	A	2020-04-27	99.29	98.55
2020-05-07	A	2020-04-28	98.77	98.28
2020-05-07	A	2020-04-29	98.71	98.13
2020-05-07	A	2020-05-04	98.49	97.41
2020-05-07	A	2020-05-06	99.94	99.08
2020-05-07	A	2020-05-07	100.00	100.00
2020-05-07	A	2020-05-08	101.45	100.80
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 예시를 호출하면 서버 오류 `KeyError: industry_id`가 나서 동작하지 않습니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/bond -->
# 채권 시장 이벤트 분석

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-M27xnGlF3qDk5UgES\_X" %}
[GetBondYieldChangesPerIssuer](https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperissuer.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xn4m-jtf9fGMtdN6" %}
[GetBondYieldChangesPerClassification](https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperclassification.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xmrrWG3UpDJOMn6B" %}
[GetBondYieldChangesPerIndustry](https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperindustry.md)
{% endcontent-ref %}

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 채권 이벤트 함수 3개는 모두 이 레포의 API 키로 `NameError: UFunction ... is not defined`입니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperissuer -->
# GetBondYieldChangesPerIssuer

특정 이벤트 날짜의 채권 발행자별 채권 수익률 변화를 조회합니다.

### Function specification

```
GetBondYieldChangesPerIssuer(event_dates)
```

### Parameters

| Parameter    | Type         | Description |
| ------------ | ------------ | ----------- |
| event\_dates | list of date | 이벤트 날짜      |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> GetBondYieldChangesPerIssuer(2010-5-17)
...
issuer_code	issuer_name	class_code	count	sum	diff
02313	국민은행	5030110	416	22,420,032,000,000	1.37
02411	기업은행	5020110	904	29,015,595,000,000	1.18
02978	삼성카드	6040111	186	4,280,000,000,000	1.35
03937	인천국제공항공사	3030110	14	1,330,000,000,000	1.93
04484	GS파워	7040112	2	320,000,000,000	2.00
20005	국고채권	1010000	130	383,961,638,700,000	3.23
20002	국민주택2종채권	1020000	159	5,047,152,230,000	2.26
20001	국민주택1종채권	1030000	61	44,310,932,320,000	0.62
30001	서울특별시	2010000	100	4,793,808,155,000	1.01
04932	광주광역시도시공사	3040111	11	136,959,000,000	1.09
30002	강원도	2020000	61	549,647,200,000	0.64
30003	대전광역시	2020000	64	508,494,420,000	0.59
30004	인천광역시	2020000	73	1,076,707,945,000	0.62
30005	광주광역시	2020000	71	487,959,470,000	0.65
30006	부산광역시	2020000	105	760,269,570,000	0.63
30007	대구광역시	2020000	122	617,920,875,000	0.64
30008	울산광역시	2020000	61	337,269,005,000	0.64
30009	충청남도	2020000	61	646,829,885,000	0.64
30010	충청북도	2020000	61	452,920,480,000	0.64
30011	경기도	2020000	61	3,064,877,450,000	0.64
30012	전라북도	2020000	61	482,692,265,000	0.64
30013	전라남도	2020000	61	655,643,445,000	0.64
30014	경상북도	2020000	61	761,848,020,000	0.64
30015	경상남도	2020000	61	1,171,466,800,000	0.64
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYieldChangesPerIssuer' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperclassification -->
# GetBondYieldChangesPerClassification

특정 이벤트 날짜의 채권 분류별 채권 수익률을 조회합니다.

### Function specification

```
GetBondYieldChangesPerClassification(event_dates)
```

### Parameters

| Parameter    | Type | Description |
| ------------ | ---- | ----------- |
| event\_dates | date | 이벤트 날짜      |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> GetBondYieldChangesPerClassification(2010-5-17)
...
class_code	count	sum	diff
1000000	92	36,492,928,700,000	3.83
1000500	1	2,674,030,000,000	5.00
1010000	37	344,794,680,000,000	1.70
1015000	9	594,711,990,000	1.00
1020000	159	5,047,152,230,000	2.26
1030000	61	44,310,932,320,000	0.62
2010000	97	3,889,808,155,000	1.04
2020000	1,094	13,206,233,065,000	0.66
3010110	106	17,180,000,000,000	1.44
3020110	167	16,678,033,000,000	1.86
3030110	1,070	107,623,849,000,000	1.26
3040111	252	6,429,839,000,000	0.50
3040112	22	675,675,700,000	0.50
3050000	23	28,930,000,000,000	0.61
4000000	98	166,030,000,000,000	0.61
5010110	915	45,348,587,250,000	1.68
5020110	904	29,015,595,000,000	1.18
5030110	814	65,240,078,000,000	1.27
5040111	410	26,134,713,900,000	1.32
5040112	85	8,039,084,000,000	1.05
5040113	9	883,000,000,000	1.56
6040111	192	5,350,000,000,000	1.45
6040112	582	17,410,492,000,000	1.28
6040113	116	3,265,000,000,000	0.96
6050111	243	6,928,000,000,000	0.96
6050112	70	2,701,282,000,000	0.84
6050113	24	622,960,000,000	0.67
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYieldChangesPerClassification' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/event/bond/getbondyieldchangesperindustry -->
# GetBondYieldChangesPerIndustry

특정 이벤트 날짜의 산업 분류별 채권 수익률을 조회합니다.

### Function specification

```
GetBondYieldChangesPerIndustry(event_dates)
```

### Parameters

| Parameter    | Type | Description |
| ------------ | ---- | ----------- |
| event\_dates | date | 이벤트 날짜      |

### Result Layout

{% content-ref url="/pages/-MX0pL3fxcn\_vXTLDQhb" %}
[Result:DataFrame](https://help.deepsearch.com/dp/api/result_layout/result-dataframe.md)
{% endcontent-ref %}

### Examples

```
> GetBondYieldChangesPerIndustry(2010-5-17)
...
industry	count	sum	diff
B05	5	450,000,000,000	1.00
C14	3	70,000,000,000	-0.67
C19	35	5,450,000,000,000	2.34
C20	22	2,250,000,000,000	1.86
C23	2	105,000,000,000	0.00
C24	13	1,000,000,000,000	2.38
C26	1	60,000,000,000	2.00
C28	5	580,000,000,000	2.80
C29	1	50,000,000,000	2.00
C30	10	370,000,000,000	1.50
C31	4	740,000,000,000	1.00
D35	69	7,820,000,000,000	2.29
E36	26	2,418,033,000,000	1.62
F41	306	28,472,859,000,000	73.54
F42	2	15,000,000,000	1.50
G46	10	910,000,000,000	1.40
G47	4	350,000,000,000	1.25
H49	85	7,160,000,000,000	1.34
H50	20	2,356,000,000,000	1.25
H52	33	2,915,000,000,000	2.06
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYieldChangesPerIndustry' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->
