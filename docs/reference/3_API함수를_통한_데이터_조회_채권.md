<!-- 이 파일은 docs/reference/sync_from_gitbook.py로 생성합니다 (2026-11-25). 원문: https://help.deepsearch.com/dp/ — 채권 발행사·발행·수익률 함수. 직접 고치지 말고, 레포 메모는 repo-memo 마커 안에 쓰세요. -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond -->
# 채권 정보 조회

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-M27xzPYvWDPNi8FJNU6" %}
[GetBondClassificationCodeList](https://help.deepsearch.com/dp/api/func/company/bond/getbondclassificationcodelist.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xzA-ShFhRIn655Md" %}
[GetBondIssuerList](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlist.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xytvwoh77qdNb8-j" %}
[GetBondIssuerListFromIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlistfromindustry.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xydq7KO0D-l1hCo6" %}
[GetBondIssuerSummaryInfo](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuersummaryinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xyQ2sgR2p2CZfzXt" %}
[GetBondClassSummaryInfo](https://help.deepsearch.com/dp/api/func/company/bond/getbondclasssummaryinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xyAsZGRLM9z0AneC" %}
[GetBondSummaryInfoPerIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondsummaryinfoperindustry.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xxxfCfB5Foj\_UEMm" %}
[GetLatestBondIssues](https://help.deepsearch.com/dp/api/func/company/bond/getlatestbondissues.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xxjczCkDWD0AA0LD" %}
[SearchBondIssuerByName](https://help.deepsearch.com/dp/api/func/company/bond/searchbondissuerbyname.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xxW4Gsqww4U85G8y" %}
[GetBondIssuanceHistory](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuancehistory.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xxHEX5eOqR6S5Wgd" %}
[GetBondRepaymentSchedule](https://help.deepsearch.com/dp/api/func/company/bond/getbondrepaymentschedule.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27y6GzgI2lHQuMunvw" %}
[GetBondYields](https://help.deepsearch.com/dp/api/func/company/bond/getbondyields.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27y61pKa2qN6TqMQr6" %}
[GetBondYieldsForIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldsforindustry.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27y5ipazzKB57YK2Of" %}
[GetAverageBondYieldTimeSeries](https://help.deepsearch.com/dp/api/func/company/bond/getaveragebondyieldtimeseries.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27y4u0FBVivF5pJhwY" %}
[GetInterpolatedBondYields](https://help.deepsearch.com/dp/api/func/company/bond/getinterpolatedbondyields.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xx2bGmJRHFuWkHiW" %}
[GetRiskFreeYields](https://help.deepsearch.com/dp/api/func/company/bond/getriskfreeyields.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xwoiZdWSWxkWIiYf" %}
[GetBondYieldPrincipalComponents](https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldprincipalcomponents.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xng2j6L2iHPoSU4O" %}
[ConvertBondIssuerCodeToNICESymbol](https://help.deepsearch.com/dp/api/func/company/bond/convertbondissuercodetonicesymbol.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xnT\_x72tMs-ZiJXz" %}
[ConvertNICESymbolToBondIssuerCode](https://help.deepsearch.com/dp/api/func/company/bond/convertnicesymboltobondissuercode.md)
{% endcontent-ref %}

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 폴더의 채권 함수 18개는 모두 이 레포의 API 키로 `NameError: UFunction ... is not defined`입니다. 현재 구독으로는 쓸 수 없습니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondclassificationcodelist -->
# GetBondClassificationCodeList

전체 채권 종류를 조회합니다.

### Function specification

```
GetBondClassificationCodeList()
```

### Examples

```
> GetBondClassificationCodeList()
...
class_code	bond_type1	bond_type2	public	rating
1000000	국채	국고채분리채권		국고채분리채권
1000500	국채	물가지수연동국채		물가지수연동국채
1010000	국채	국고채		양곡/외평
1015000	국채	국민주택3종		국민주택3종
1020000	국채	국민주택2종		국민주택2종
1030000	국채	국민주택1종		국민주택1종
2010000	지방채	서울도시철도		서울도시철도
2020000	지방채	지역개발		기타지방채
3030110	특수채	공사채		AAA
3040111	특수채	공사채		AA+
3040112	특수채	공사채		AA
3040113	특수채	공사채		AA-
3050000	특수채	정부보증		정부보증
4000000	통안증권	통안증권		통안증권
5010110	금융채1	산금채	공모	AAA
5020110	금융채1	중금채	공모	AAA
5030110	금융채1	은행채	공모	AAA
5040111	금융채1	은행채	공모	AA+
5040112	금융채1	은행채	공모	AA
5040113	금융채1	은행채	공모	AA-
5050111	금융채1	은행채	공모	A+
5050112	금융채1	은행채	공모	A
5050113	금융채1	은행채	공모	A-
6030110	금융채2	카드채	공모	AAA
6040111	금융채2	카드채	공모	AA+
6040112	금융채2	카드채	공모	AA
6040113	금융채2	카드채	공모	AA-
6050111	금융채2	카드채	공모	A+
6050112	금융채2	카드채	공모	A
6050113	금융채2	카드채	공모	A-
6060111	금융채2	카드채	공모	BBB+
6060112	금융채2	카드채	공모	BBB
6060113	금융채2	카드채	공모	BBB-
6070111	금융채2	카드채	공모	BB+
6070112	금융채2	카드채	공모	BB
6070113	금융채2	카드채	공모	BB-
6080111	금융채2	카드채	공모	B+
6080112	금융채2	카드채	공모	B0
6080113	금융채2	카드채	공모	B-
7030110	회사채	회사채 (무보증)	공모	AAA
7040111	회사채	회사채 (무보증)	공모	AA+
7040112	회사채	회사채 (무보증)	공모	AA
7040113	회사채	회사채 (무보증)	공모	AA-
7050111	회사채	회사채 (무보증)	공모	A+
7050112	회사채	회사채 (무보증)	공모	A
7050113	회사채	회사채 (무보증)	공모	A-
7060111	회사채	회사채 (무보증)	공모	BBB+
7060112	회사채	회사채 (무보증)	공모	BBB
7060113	회사채	회사채 (무보증)	공모	BBB-
7070111	회사채	회사채 (무보증)	공모	BB+
7070112	회사채	회사채 (무보증)	공모	BB
7070113	회사채	회사채 (무보증)	공모	BB-
7080111	회사채	회사채 (무보증)	공모	B+
7080112	회사채	회사채 (무보증)	공모	B0
7080113	회사채	회사채 (무보증)	공모	B-
7090110	회사채	회사채 (무보증)	공모	CCC
7090111	회사채	회사채 (무보증)	공모	CCC+
7090112	회사채	회사채 (무보증)	공모	CCC0
7090113	회사채	회사채 (무보증)	공모	CCC-
7090120	회사채	회사채 (무보증)	공모	CC
7090130	회사채	회사채 (무보증)	공모	C
7130110	회사채	회사채 (보증)	공모	AAA
7140111	회사채	회사채 (보증)	공모	AA+
7140112	회사채	회사채 (보증)	공모	AA
7140113	회사채	회사채 (보증)	공모	AA-
7150111	회사채	회사채 (보증)	공모	A+
7150112	회사채	회사채 (보증)	공모	A
7150113	회사채	회사채 (보증)	공모	A-
7430110	MBS	MBS	공모	AAA
8030110	사모사채	사모회사채	사모	AAA
8040111	사모사채	사모회사채	사모	AA+
8040112	사모사채	사모회사채	사모	AA
8040113	사모사채	사모회사채	사모	AA-
8050111	사모사채	사모회사채	사모	A+
8050112	사모사채	사모회사채	사모	A
8050113	사모사채	사모회사채	사모	A-
8060111	사모사채	사모회사채	사모	BBB+
8060112	사모사채	사모회사채	사모	BBB
8060113	사모사채	사모회사채	사모	BBB-
8070111	사모사채	사모회사채	사모	BB+
8070112	사모사채	사모회사채	사모	BB
8070113	사모사채	사모회사채	사모	BB-
8080111	사모사채	사모회사채	사모	B+
8080112	사모사채	사모회사채	사모	B0
8080113	사모사채	사모회사채	사모	B-
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondClassificationCodeList' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlist -->
# GetBondIssuerList

특정 class 채권의 발행자 정보를 조회합니다.

### Function specification

```
GetBondIssuerList(class_code)
```

###

### Parameters

| Parameter   | Type   | Description   |
| ----------- | ------ | ------------- |
| class\_code | string | 채권 class code |

### Examples

```
> GetBondIssuerList("1000000")
...
class_code	issuer_code	issuer_name	count	avg_ytm	avg_maturity	total_issue_size
1000000	20005	국고채권	203	1.36	17.48	95,072,313,510,000
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondIssuerList' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlistfromindustry -->
# GetBondIssuerListFromIndustry

특정 산업의 채권 발행자 리스트를 조회합니다.

### Function specification

```
GetBondIssuerListFromIndustry(industries)
```

###

### Parameters

| Parameter  | Type           | Description |
| ---------- | -------------- | ----------- |
| industries | list of string | 통계청 산업코드    |

###

### Examples

```
> GetBondIssuerListFromIndustry("C21")
...
class_code	issuer_code	count	avg_ytm	avg_maturity	total_issue_size	issuer_name
7040113	00628	5	1.62	1.86	360,000,000,000	녹십자
7050111	06989	4	1.66	1.52	380,000,000,000	대웅제약
7050111	17662	4	1.80	2.49	290,000,000,000	한미약품
7050112	00929	1	1.62	1.05	10,000,000,000	광동제약
7050113	00849	2	1.81	1.62	100,000,000,000	서흥
7050113	44919	2	1.98	2.48	200,000,000,000	에이치케이이노엔
7060111	00239	1	2.25	0.35	50,000,000,000	한독
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondIssuerListFromIndustry' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondissuersummaryinfo -->
# GetBondIssuerSummaryInfo

특정 채권의 요약 정보를 조회합니다.

### Function specification

```
GetBondIssuerSummaryInfo(composite_codes)
```

###

### Parameters

| Parameter        | Type   | Description                                   |
| ---------------- | ------ | --------------------------------------------- |
| composite\_codes | string | 채권의 class code 와 issuer code 를 : 로 조합하여 만든 코드 |

###

### Examples

```
> GetBondIssuerSummaryInfo("7040113:00628")
...
class_code	issuer_code	issuer_name	count	avg_ytm	avg_maturity	total_issue_size
7040113	00628	녹십자	5	1.62	1.86	360,000,000,000


```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondIssuerSummaryInfo' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondclasssummaryinfo -->
# GetBondClassSummaryInfo

특정 클래스의 채권 정보를 조회한다.

### Function specification

```
GetBondClassSummaryInfo(class_codes)
```

###

### Parameters

| Parameter    | Type   | Description |
| ------------ | ------ | ----------- |
| class\_codes | string | 채권 클래스 코드   |

###

### Examples

```
> GetBondClassSummaryInfo("7040113")
...
class_code	count	avg_ytm	avg_maturity	total_issue_size
7040113	335	1.74	2.55	34,778,000,000,000

```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondClassSummaryInfo' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondsummaryinfoperindustry -->
# GetBondSummaryInfoPerIndustry

특정 산업의 채권 정보를 조회한다.

### Function specification

```
GetBondSummaryInfoPerIndustry(industries)
```

###

### Parameters

| Parameter  | Type           | Description  |
| ---------- | -------------- | ------------ |
| industries | list of string | 통계청 산업 분류 코드 |

###

### Examples

```
> GetBondSummaryInfoPerIndustry(["C21","C22"])
...
industry_id	count	avg_ytm	avg_maturity	total_issue_size
C21	19	1.76	1.84	1,390,000,000,000
C22	17	1.71	2.31	1,370,000,000,000

```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondSummaryInfoPerIndustry' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getlatestbondissues -->
# GetLatestBondIssues

최근에 발행된 채권 정보를 조회합니다.

### Function specification

```
GetLatestBondIssues()
```

###

### Examples

```
> GetLatestBondIssues()
...
bond_code	class_code	clean_price	coupon_duration	coupon_rate	issue_date	issue_size	issuer_code	maturity_date	ytm
KR103502GA67	1010000	9,898.16	6	1.38	2020-06-10	1,488,000,000,000	20005	2030-06-10	1.47
KR103501GA68	1010000	10,006.35	6	1.00	2020-06-10	2,349,000,000,000	20005	2023-06-10	0.95
KR2088012A57	2020000	9,814.57	12	1.05	2020-05-31	3,145,825,000	30015	2025-05-31	1.41
KR2006012A59	2020000	9,814.57	12	1.05	2020-05-31	1,137,705,000	30006	2025-05-31	1.41
KR353601DA53	3030110	9,962.63	12	1.18	2020-05-31	73,200,000	04130	2023-05-31	1.28
KR2006014A57	2020000	9,814.57	12	1.05	2020-05-31	3,603,360,000	30006	2025-05-31	1.41
KR2099012A54	2020000	9,814.57	12	1.05	2020-05-31	1,757,500,000	30016	2025-05-31	1.41
...
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetLatestBondIssues' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/searchbondissuerbyname -->
# SearchBondIssuerByName

이름으로 채권 발행자를 검색합니다.

### Function specification

```
SearchBondIssuerByName(name)
```

###

### Parameters

| Parameter | Type   | Description |
| --------- | ------ | ----------- |
| name      | string | 발행자 이름      |

###

### Examples

```
> SearchBondIssuerByName("녹십자")
...
class_code	issuer_code	issuer_name	count	avg_ytm	avg_maturity	total_issue_size
7040113	00628	녹십자	5	1.62	1.86	360,000,000,000

```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'SearchBondIssuerByName' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondissuancehistory -->
# GetBondIssuanceHistory

특정 채권 발행자의 과거 채권 발행 이력을 조회합니다.

### Function specification

```
GetBondIssuanceHistory(issuer_codes)
```

###

### Parameters

| Parameter     | Type   | Description |
| ------------- | ------ | ----------- |
| issuer\_codes | string | 채권 발행자 코드   |

###

### Examples

```
> GetBondIssuanceHistory("00628")
...
issuer_code	date	count	sum
00628	2016-05-31	2	150,000,000,000
00628	2017-06-30	2	150,000,000,000
00628	2019-05-31	2	120,000,000,000
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondIssuanceHistory' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondrepaymentschedule -->
# GetBondRepaymentSchedule

특정 채권 발행자의 상환 스케쥴을 조회합니다.

### Function specification

```
GetBondRepaymentSchedule(issuer_codes)
```

###

### Parameters

| Parameter     | Type           | Description |
| ------------- | -------------- | ----------- |
| issuer\_codes | list of string | 채권 발행자 코드   |

###

### Examples

```
> GetBondRepaymentSchedule("00628")
...
issuer_code	date	count	sum
00628	2019-05-31	1	60,000,000,000
00628	2020-06-30	1	90,000,000,000
00628	2021-05-31	1	90,000,000,000
00628	2022-05-31	1	60,000,000,000
00628	2022-06-30	1	60,000,000,000
00628	2024-05-31	1	60,000,000,000
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondRepaymentSchedule' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondyields -->
# GetBondYields

채권 수익률을 조회합니다.

### Function specification

```
GetBondYields(composite_codes=None, class_codes=None, issuer_codes=None,
                date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type   | Description |
| ------------------- | ------ | ----------- |
| composite\_codes    | string | 채권 컴포지트 코드  |
| class\_codes        | string | 채권 클래스 코드   |
| issuer\_codes       | string | 채권 발행자 코드   |
| date\_from/date\_to | date   | 수익률 조회 기간   |

###

### Examples

```
> GetBondYields("7040113:00628","7040113","00628",2010-1-1,2018-12-31) 
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYields' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldsforindustry -->
# GetBondYieldsForIndustry

특정 산업의 채권 수익률을 계산합니다.

### Function specification

```
GetBondYieldsForIndustry(industries, date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type           | Description |
| ------------------- | -------------- | ----------- |
| industries          | list of string | 통계청 산업 코드   |
| date\_from/date\_to | date           | 수익률 계산 기간   |

###

### Examples

```
> GetBondYieldsForIndustry("C21", 2010-1-1, 2018-12-31)
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYieldsForIndustry' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getaveragebondyieldtimeseries -->
# GetAverageBondYieldTimeSeries

지정한 종류의 채권들의 평균 금리 time series를 계산 합니다.

### Function specification

```
GetAverageBondYieldTimeSeries(code_type=0, codes=None, date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type   | Description                                     |
| ------------------- | ------ | ----------------------------------------------- |
| code\_type          | int    | COMPOSITE = 0 ISSUER = 1 CLASS = 2 INDUSTRY = 3 |
| codes               | string | 채권 구분 코드값                                       |
| date\_from/date\_to | date   | 계산 기간                                           |

###

### Examples

```
> GetAverageBondYieldTimeSeries(1, "14727", date_from=2019-05-01, date_to=2019-05-30)

> GetAverageBondYieldTimeSeries(3, "C30", date_from=2019-05-01, date_to=2019-05-30)

```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetAverageBondYieldTimeSeries' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getinterpolatedbondyields -->
# GetInterpolatedBondYields

지정한 종류의 채권들의 Interpolated 채권 수익률을 계산합니다.

### Function specification

```
GetInterpolatedBondYields(maturities, code_type=0, codes=None,
                date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type        | Description                                     |
| ------------------- | ----------- | ----------------------------------------------- |
| maturities          | list of int | 만기                                              |
| code\_type          | int         | COMPOSITE = 0 ISSUER = 1 CLASS = 2 INDUSTRY = 3 |
| codes               | string      | 채권 구분 코드값                                       |
| date\_from/date\_to | date        | 계산 기간                                           |

###

### Examples           &#x20;

```
> GetInterpolatedBondYields(maturities=[1,2], code_type=1, codes="14727", date_from=2019-05-01, date_to=2019-05-30)
```

###

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetInterpolatedBondYields' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getriskfreeyields -->
# GetRiskFreeYields

무위험 이자율을 조회합니다.

### Function specification

```
GetRiskFreeYields(date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type | Description |
| ------------------- | ---- | ----------- |
| date\_from/date\_to | date | 조회기간        |

###

### Examples

```
> GetRiskFreeYields(date_from=2020-1-1, date_to=2020-12-31)
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetRiskFreeYields' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldprincipalcomponents -->
# GetBondYieldPrincipalComponents

채권 주성분을 분석합니다.

### Function specification

```
GetBondYieldPrincipalComponents(composite_codes=None, class_codes=None,
                issuer_codes=None, date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type   | Description |
| ------------------- | ------ | ----------- |
| composite\_codes    | string | 채권 컴포지트 코드  |
| class\_codes        | string | 채권 클래스 코드   |
| issuer\_codes       | string | 채권 발행자 코드   |
| date\_from/date\_to | date   | 수익률 조회 기간   |

###

### Examples

```
> GetBondYieldPrincipalComponents(composite_codes=["7030110:05773","7030110:05537"],date_from=2019-01-01,date_to=2019-07-29)
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetBondYieldPrincipalComponents' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/convertbondissuercodetonicesymbol -->
# ConvertBondIssuerCodeToNICESymbol

채권 발행자 코드를 나이스 심볼로 변환합니다.

### Function specification

```
ConvertBondIssuerCodeToNICESymbol(issuer_codes)
```

###

### Parameters

| Parameter    | Type   | Description |
| ------------ | ------ | ----------- |
| issuer\_code | string | 채권 발행자 코드   |

###

### Examples

```
> ConvertBondIssuerCodeToNICESymbol("00628")
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'ConvertBondIssuerCodeToNICESymbol' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/bond/convertnicesymboltobondissuercode -->
# ConvertNICESymbolToBondIssuerCode

나이스 심볼 코드를 채권 발행자 코드로 변환합니다.

### Function specification

```
ConvertNICESymbolToBondIssuerCode(symbols)
```

###

### Parameters

| Parameter | Type   | Description |
| --------- | ------ | ----------- |
| symbols   | string | 나이스 심볼 코    |

###

### Examples

```
> ConvertNICESymbolToBondIssuerCode("355399")
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'ConvertNICESymbolToBondIssuerCode' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->
