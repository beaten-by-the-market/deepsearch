# API 함수를 통한 데이터 조회

기본 쿼리 형태 (entity - property - date range) 로 표시가 어려운 데이터의 경우엔 각 데이터 소스를 담당하는 API 함수를 사용하여 정보를 조회할 수 있습니다. API 함수를 이용하여 조회 가능한 데이터는 크게 다음과 같이 분류할 수 있습니다.

{% content-ref url="func/company" %}
[company](https://help.deepsearch.com/dp/api/func/company)
{% endcontent-ref %}

{% content-ref url="func/undefined" %}
[undefined](https://help.deepsearch.com/dp/api/func/undefined)
{% endcontent-ref %}

{% content-ref url="func/industry" %}
[industry](https://help.deepsearch.com/dp/api/func/industry)
{% endcontent-ref %}

{% content-ref url="func/people" %}
[people](https://help.deepsearch.com/dp/api/func/people)
{% endcontent-ref %}

{% content-ref url="func/document" %}
[document](https://help.deepsearch.com/dp/api/func/document)
{% endcontent-ref %}

{% content-ref url="func/event" %}
[event](https://help.deepsearch.com/dp/api/func/event)
{% endcontent-ref %}

{% content-ref url="func/economy" %}
[economy](https://help.deepsearch.com/dp/api/func/economy)
{% endcontent-ref %}

##

# FindEntity

### Function specification

```
FindEntity(entity_type, pattern, count=0, fields=None)
```

###

### Parameters

|
| ------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| fields       | list of string                        | <p>검색 대상이 되는 항목을 명시합니다. 아래 항목 등 기업 개요에 나오는 전체 정보를 사용할 수 있습니다. ( 전체 기업 개요는 <a href="https://help.deepsearch.com/dp/deepsearch/api/2.1./company/getcompanysummary">여기</a>를 참고하세요 )<br></p><ul><li>기업 코드: symbol</li><li>기업 이름: name\_ko, name\_en, name\_short</li><li>사업자 등록번호: business\_rid</li><li>법인 등록번호: company\_rid</li><li>산업 분류코드: industry\_id</li><li>주소: land\_lot\_en, land\_lot\_ko, road\_name\_en, road\_name\_ko</li><li>전화번호: tel, fax</li><li>기업형태 : company\_type\_l1 (01=주식, 02=합자, 03=합명, 04=유한, 05=조합, 06=정부투자기관,07=개인, 08=학교, 09=병원, 10=단체/협회, 15=유한책임회사,51=협동조합, 94=합자조합, 99=기타) </li><li>기업상세코드 : company\_type\_l2</li><li>기업규모 : company\_type\_size (1=대기업, 2=중소기업, 3=중견기업, 0=기타)</li></ul><p>비어있을 경우 \["symbol", "name\_ko", "name\_en"] 을 기본 값으로 사용합니다.</p> |

###

### Examples

#### 1. 이름으로 검색

```
> FindEntity("Financial", "삼성*")

...

            entity_name
symbol                 
KRX:000810         삼성화재
KRX:001360         삼성제약
KRX:005930         삼성전자
KRX:006400        삼성SDI
KRX:006660         삼성공조
...                 ...
NICE:527988        삼성금속
NICE:528387       삼성고주파
NICE:528418      삼성화물운수
NICE:528557    삼성전자벧엘상사
NICE:529440          삼성
```

#### 2. 사업자 등록 번호로 검색

```
> FindEntity("Financial", ["1248100998", "1268103725"], fields=["business_rid"])

...

           entity_name
symbol                
KRX:000660      SK하이닉스
KRX:005930        삼성전자
```

Note: 사업자 등록 번호 또는 법인 등록 번호를 이용해 기업을 검색할 땐 dash (-) 구분자 없이 숫자만 입력해야 합니다.

#### 3. 주소로 검색

```
> FindEntity("Financial", "*울산*", fields=["road_name_ko", "land_lot_ko"])

...

            entity_name
symbol                 
KRX:001390        KG케미칼
KRX:004000       롯데정밀화학
KRX:004430         송원산업
KRX:007340     디티알오토모티브
KRX:009580        무림P&P
...                 ...
NICE:160779        레베산업
NICE:161033      금용종합건설
NICE:161235         엠알시
NICE:161472        갑부건설
NICE:161672          삼종
```

#### 4. 전화번호로 검색

```
> FindEntity("Financial", "02-2005-1114", fields=["tel"])

...

            entity_name
symbol                 
KRX:007070        GS리테일
NICE:352705      지에스칼텍스
NICE:380679      LG정보통신
```

# FindEntity

### Function specification

```
FindEntity(entity_type, pattern, count=0, fields=None)
```

###

### Parameters

|
| ------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| fields       | list of string                        | <p>검색 대상이 되는 항목을 명시합니다. 아래 항목 등 기업 개요에 나오는 전체 정보를 사용할 수 있습니다. ( 전체 기업 개요는 <a href="https://help.deepsearch.com/dp/deepsearch/api/2.1./company/getcompanysummary">여기</a>를 참고하세요 )<br></p><ul><li>기업 코드: symbol</li><li>기업 이름: name\_ko, name\_en, name\_short</li><li>사업자 등록번호: business\_rid</li><li>법인 등록번호: company\_rid</li><li>산업 분류코드: industry\_id</li><li>주소: land\_lot\_en, land\_lot\_ko, road\_name\_en, road\_name\_ko</li><li>전화번호: tel, fax</li><li>기업형태 : company\_type\_l1 (01=주식, 02=합자, 03=합명, 04=유한, 05=조합, 06=정부투자기관,07=개인, 08=학교, 09=병원, 10=단체/협회, 15=유한책임회사,51=협동조합, 94=합자조합, 99=기타) </li><li>기업상세코드 : company\_type\_l2</li><li>기업규모 : company\_type\_size (1=대기업, 2=중소기업, 3=중견기업, 0=기타)</li></ul><p>비어있을 경우 \["symbol", "name\_ko", "name\_en"] 을 기본 값으로 사용합니다.</p> |

###

### Examples

#### 1. 이름으로 검색

```
> FindEntity("Financial", "삼성*")

...

            entity_name
symbol                 
KRX:000810         삼성화재
KRX:001360         삼성제약
KRX:005930         삼성전자
KRX:006400        삼성SDI
KRX:006660         삼성공조
...                 ...
NICE:527988        삼성금속
NICE:528387       삼성고주파
NICE:528418      삼성화물운수
NICE:528557    삼성전자벧엘상사
NICE:529440          삼성
```

#### 2. 사업자 등록 번호로 검색

```
> FindEntity("Financial", ["1248100998", "1268103725"], fields=["business_rid"])

...

           entity_name
symbol                
KRX:000660      SK하이닉스
KRX:005930        삼성전자
```

Note: 사업자 등록 번호 또는 법인 등록 번호를 이용해 기업을 검색할 땐 dash (-) 구분자 없이 숫자만 입력해야 합니다.

#### 3. 주소로 검색

```
> FindEntity("Financial", "*울산*", fields=["road_name_ko", "land_lot_ko"])

...

            entity_name
symbol                 
KRX:001390        KG케미칼
KRX:004000       롯데정밀화학
KRX:004430         송원산업
KRX:007340     디티알오토모티브
KRX:009580        무림P&P
...                 ...
NICE:160779        레베산업
NICE:161033      금용종합건설
NICE:161235         엠알시
NICE:161472        갑부건설
NICE:161672          삼종
```

#### 4. 전화번호로 검색

```
> FindEntity("Financial", "02-2005-1114", fields=["tel"])

...

            entity_name
symbol                 
KRX:007070        GS리테일
NICE:352705      지에스칼텍스
NICE:380679      LG정보통신
```

# FindEntityByShareholderName

### Function specification

```
FindEntityByShareholderName(entity_type, shareholder_name,
                                date_from=None, date_to=None, last_only=False)
```

###

### Parameters

| Parameter         | Type                                  | Description                                                                |
| ----------------- | ------------------------------------- | -------------------------------------------------------------------------- |
| entity\_type      | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다.                     |
| shareholder\_name | <p>string or</p><p>list of string</p> | 검색하고자 하는 주주명을 입력합니다.                                                       |
| date\_from        | date                                  | 대상이 되는 주주명부 시작 시점을 설정합니다. 따로 지정이 없는 경우, 최신의 주주명부를 대상으로 합니다. ex)2010-1-1    |
| date\_to          | date                                  | 대상이 되는 주주명부 종료 시점을 설정합니다. 따로 지정이 없는 경우, 최신의 주주명부를 대상으로 합니다.  ex)2010-12-31 |
| last\_only        | boolean                               | 검색이 된 주주명부가 복수 시점일 경우, 가장 최신의 주주명부만을 사용할 것인지 지정합니다. 기본값은 False 입니다.        |

###

### Examples

```
> FindEntityByShareholderName("Financial","이건희",2010-01-01,2010-12-31,True)

...

date	symbol	entity_name	name	no_shares	ownership_percentage
2010-04-21	NICE:514983	해든건설	이건희	15	8.00
2010-06-04	NICE:153594	일조산업개발	이건희	29	15.40
2010-08-19	NICE:005169	아이피코리아	이건희	22	55.00
2010-12-31	KRX:005930	삼성전자	이건희	4,985	3.38
2010-12-31	KRX:018260	삼성에스디에스	이건희	9	0.01
2010-12-31	KRX:032830	삼성생명	이건희	41,519	20.76
2010-12-31	NICE:201495	세창테크	이건희	20	10.00
2010-12-31	NICE:610232	삼성물산	이건희	2,206	1.41

```

####

# FindEntityByIndustryID

### Function specification

```
FindEntityByIndustryID(entity_type, pattern, count=100)
```

###

### Parameters

| Parameter    | Type                                  | Description                                            |
| ------------ | ------------------------------------- | ------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다. |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.             |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.        |

###

### Examples

```
> FindEntityByIndustryID("Financial","*자동차*",10)

...

symbol	entity_name	industry_id	industry_name
NICE:003387	태가통상	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:003700	스프레이시스템코리아	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:003883	마산금속	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:004131	대덕산업	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:004510	현대특수금속	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:005343	남광정밀	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:012145	우리정공	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:013018	신성금속공업	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:015236	국제상역엔지니어링	KRI:10C2591300	자동차용 금속 압형제품 제조업
NICE:017514	안진산업	KRI:10C2591300	자동차용 금속 압형제품 제조업

```

####

####

# FindEntityByBusinessArea

### Function specification

```
FindEntityByBusinessArea(entity_type, pattern, count=0)
```

###

### Parameters

| Parameter    | Type                                  | Description                                            |
| ------------ | ------------------------------------- | ------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다. |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.             |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.        |

###

### Examples

```
> FindEntityByBusinessArea("Financial","*반도체*",10)

...

symbol	entity_name	FindEntityByBusinessArea(Financial, *반도체*, 10)
KRX:000660	SK하이닉스	반도체,컴퓨터,통신기기 제조,도매
KRX:000910	유니온	백시멘트,타일시멘트,알루미나시멘트,용융알루미나,급결제,냉각유닛,슬러리스스템,드라이가스스크러버(반도체제조장비) 제조,도매
KRX:000990	DB하이텍	반도체 제조
KRX:003160	디아이	반도체검사장비,전자부품,레저용품,석제품 제조,판매,오파,부동산임대
KRX:004870	티웨이홀딩스	반도체,레미콘,콘크리트파일 제조
KRX:005290	동진쎄미켐	반도체,LCD용재료(감광제,봉지제),발포제 제조,판매
KRX:005930	삼성전자	휴대폰,컴퓨터,네트워크시스템,핵심칩,반도체부품,디스플레이패널,가전제품,의료기기,프린터 제조
KRX:008060	대덕전자	산업용 인쇄회로기판,다층 인쇄회로기판,빌드업기판,반도체패키지기판,메모리모듈기판 제조
KRX:009310	참엔지니어링	FPD Repair장비,반도체장비 제조
KRX:011560	세보엠이씨	냉난방공사,기계설비공사,철물공사/반도체생산시설,산업기계,하역운반기계 제조

```

####

####

# FindEntityByAddress

### Function specification

```
FindEntityByAddress(entity_type, pattern, count=0)
```

### Parameters

| Parameter    | Type                                  | Description                                            |
| ------------ | ------------------------------------- | ------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다. |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.             |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.        |

### Examples

```
> FindEntityByAddress("Financial", "*울산*")

...

            entity_name
symbol                 
KRX:001390        KG케미칼
KRX:004000       롯데정밀화학
KRX:004430         송원산업
KRX:007340     디티알오토모티브
KRX:009580        무림P&P
...                 ...
NICE:160779        레베산업
NICE:161033      금용종합건설
NICE:161235         엠알시
NICE:161472        갑부건설
NICE:161672          삼종
```

# FindEntityInDocuments

### Function specification

```
FindEntityInDocuments(category, section, query, count=None,
                                date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category   | string or list of string | <p></p><p>뉴스: news</p><p>증권사 보고서: research</p><p>공시,IR : company</p><p>특허 : patent</p><p></p>                                                                                                                                                                                                                                                                                                                                                                                                        |
| section    | string or list of string | <p>Category가 news일 경우 </p><p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p><p></p><p>Category가 research일 경우 </p><p>시장 전망: market </p><p>투자전략: strategy </p><p>기업 보고서: company </p><p>산업 보고서: industry </p><p>경제 보고서: economy </p><p>채권 보고서: bond </p><p></p><p>Category 가 company 인 경우 </p><p>IR : ir </p><p>공시 : disclosure </p><p></p><p>Category 가 patent 인 경우 </p><p>특허 : patent</p> |
| query      | string                   | 검색 쿼리                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| count      | integer                  | 최대 기업 개수                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| date\_from | string                   | 검색 시작 시점 (YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| date\_to   | string                   | 검색 종료 시점(YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

###

### Examples

```
> FindEntityInDocuments("company", "disclosure", "2차전지")


...
date	symbol	entity_name	FindEntityInDocuments(company, disclosure, 2차전지)
2020-03-27	KRX:034730	SK	28
2020-03-27	NICE:860263	케이비증권	20
2020-03-27	KRX:005420	코스모화학	18
2020-03-27	KRX:051910	LG화학	18
2020-03-27	KRX:005490	POSCO	17
2020-03-27	KRX:003670	포스코케미칼	13
2020-03-27	KRX:303030	지니틱스	13
2020-03-27	KRX:254120	자비스	13
2020-03-27	KRX:005070	코스모신소재	13
2020-03-27	KRX:035290	더블유에프엠	13
2020-03-27	KRX:000150	두산	12
2020-03-27	KRX:006800	미래에셋대우	12
2020-03-27	KRX:196490	디에이테크놀로지	12
2020-03-27	KRX:160600	에스엔텍비엠	12
2020-03-27	KRX:036830	솔브레인	12
...
```

# FindAssociatedEntity

### Function specification

```
FindAssociatedEntity(query, count, min_score=0,
                date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type    | Description                   |
| ------------------- | ------- | ----------------------------- |
| query               | string  | 관련 주제                         |
| count               | integer | 최대 검색 결과 개수                   |
| min\_score          | float   | 주제 관련도                        |
| date\_from/date\_to | string  | 관련 근거가 되는 문서 검색 범위 (YYYYMMDD) |

### Logics

관련 기업을 추출하기 위하여, 뉴스, 공시, 증권사리포트, IR 문서를 활용합니다. 공시에서 해당 주제에 대해서 언급하고 있는 기업 중 뉴스, 증권사리포트, IR 등 다른 문서에서 언급된 빈도가 높은 기업을 관련 기업으로 추출하며, 언급된 정도를 바탕으로 관련도를 계산합니다. ( 관련도는 최대 100 점으로 구성 )

### Examples

```
> FindAssociatedEntity("2차전지",10,60)


...
date	symbol	entity_name	FindAssociatedEntity(2차전지, 10, 60)
2020-03-30	KRX:051910	LG화학	100.00
2020-03-30	KRX:006400	삼성SDI	99.82
2020-03-30	KRX:282880	코윈테크	99.18
2020-03-30	KRX:025900	동화기업	99.09
2020-03-30	KRX:278280	천보	98.82
2020-03-30	KRX:247540	에코프로비엠	98.36
2020-03-30	KRX:131390	피앤이솔루션	98.27
2020-03-30	KRX:047310	파워로직스	97.55
2020-03-30	KRX:091580	상신이디피	95.45
2020-03-30	KRX:290670	대보마그네틱	95.45
...
```

# GetCompanySummary

### Function specification

```
GetCompanySummary(entities)
```

###

### Parameters

| Parameter | Type                                  | Description                                                                                         |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities  | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |

### Output Fields

| Field                  | Description                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| symbol                 | 종목 심볼                                                                                                  |
| entity\_name           | 업체명                                                                                                    |
| bank\_branch\_name\_en | 은행 지점(영문)                                                                                              |
| bank\_branch\_name\_ko | 은행 지점(한글)                                                                                              |
| business\_area\_en     | 사업 개요(영문)                                                                                              |
| business\_area\_ko     | 사업 개요(한글)                                                                                              |
| business\_rid          | 사업자번호                                                                                                  |
| ceo\_en                | 대표자명(영문)                                                                                               |
| ceo\_ko                | 대표자명(한글)                                                                                               |
| company\_rid           | 법인등록번호                                                                                                 |
| company\_type\_l1      | 기업형태 ( 1: 일반법인 2: 공공기관, 3: 비영리법인,  8:기타법인, 9:개인, 이외:기타 )                                               |
| company\_type\_l2      | 기업상세코드(하단의 기업 상세 코드 정보 참조)                                                                             |
| company\_type\_size    | 기업규모(1=대기업, 2=중소기업, 3=중견기업, 0=기타)                                                                      |
| conglomerate\_id       | 그룹ID                                                                                                   |
| date\_employees        | 종업원 숫자 기준일                                                                                             |
| date\_established| 설립일                                                                                                    |
| date\_founded          | 창업일                                                                                                    |
| email                  | 대표이메일                                                                                                  |
| employee\_no           | 종업원수                                                                                                   |
| fiscal\_year\_end      | 결산                                                                                                     |
| fs\_type               | 재무제표구분 (00=제조, AA=은행, BB=증권, CC=생보, DD=손보, EE=신용금고, FF=종금, GG=투신, HH=리스, II=카드, JJ=창투, KK=할부금융, ZZ=기타) |
| industry\_id           | 산업분류 (10차 통계청 산업분류 기)                                                                                  |
| is\_alive              | 기업존속여부 (True/False)                                                                                    |
| is\_closed             | 기업폐쇄여부                                                                                                 |
| is\_external\_audit    | 외부감사여부                                                                                                 |
| is\_supervision        | 관리종목여부                                                                                                 |
| market\_id             | 상장시장구분코드 (1=코스피, 2=코스닥, 3=코넥스, 4=제3시장, 9=대상아님)                                                         |
| name\_en               | 회사명(영문)                                                                                                |
| name\_ko               | 회사명(한글)                                                                                                |
| name\_short            | 약식업체명                                                                                                  |
| primary\_bank\_symbol  | 은행코드                                                                                                   |
| status                 | 상태                                                                                                     |
| website                | 홈페이지                                                                                                   |

### Examples

```
> GetCompanySummary([삼성전자,LG전자])

...

symbol	entity_name	bank_branch_name_en	bank_branch_name_ko	business_area_en	business_area_ko	business_rid	ceo_en	ceo_ko	company_rid	company_type_l1	company_type_l2	company_type_size	conglomerate_id	date_employees	date_established	date_founded	email	employee_no	fiscal_year_end	fs_type	industry_id	is_alive	is_closed	is_external_audit	is_supervision	market_id	name_en	name_ko	name_short	primary_bank_symbol	status	website
KRX:066570	LG전자	Twin Tower	트윈타워	C-TV, V.C.R, Conputer, PDP-TV, CDMA Mobile communication, Electronic exchanger	이동통신단말기,C-TV,V.C.R.,컴퓨터,완전평면 TV,플라즈마 디스플레이 패널 TV,전자제품(세탁기외),CDMA(코드분할다중접속)이동통신,전자교환기,전송기기	1078614075	Jo,Seong Jin/Jeong,Do Hyeon	조성진/정도현	1101112487050	1	511	1	282	20190930	20020401			40,418	12	00	KRI:10C2642200	TRUE	N	TRUE	FALSE	1	LG Electronics Inc.	LG전자(주)	LG전자	KRBank:019	00	www.lge.co.kr
KRX:005930	삼성전자	Samsung Center	삼성센터	Comm.& Semiconductor/Computer,Display/Consumer Electronics,Rambus DRAM,FLASH & SMART MADIA	휴대폰,컴퓨터,네트워크시스템,핵심칩,반도체부품,디스플레이패널,가전제품,의료기기,프린터 제조	1248100998	Kim,Gi Nam/Kim,Hyeon Seok/Go,Dong Jin	김기남/김현석/고동진	1301110006246	1	511	1	511	20190930	19690113			105,342	12	00	KRI:10C2642200	TRUE	N	TRUE	FALSE	1	Samsung Electronics Co.,Ltd.	삼성전자(주)	삼성전자	KRBank:019	00	www.samsung.com/sec

```

### 기업상세코드

000 미분류\
110 공기업\
111 준정부기관\
119 기타공공기관\
201 국립학교\
202 공립학교\
203 사립학교\
299 기타학교\
301 국립병원\
302 국립대학병원\
303 사립대학병원\
304 공립병원\
305 시립병원\
306 공사볍원\
307 의료법인병원\
308 특수법인병원\
309 사회복지법인병원\
399 기타병원\
401 종교단체\
402 복지단체\
403 학회/연구회\
404 문화재단\
405 장학재단\
499 기타단체협회\
511 주식회사\
512 합명회사\
513 합자회사\
514 유한회사\
521 사단법인\
522 재단법인\
531 학교법인\
532 사회복지법인\
533 의료법인\
534 회계법인\
535 특별법에의한 은행\
536 농업협동조합\
537 축산업협동조합\
538 수산업협동조합\
539 산립조합\
540 중소기업협종조합\
541 신용협종조합\
542 농지개량조합\
543 노동조합\
544 새마을금고(연합회)\
545 의료보험조합\
546 법무법인\
547 상공회의소\
548 상호신용금고\
549 자동차운송사업조합\
550 공업협동조합\
571 기타법인\
580 외국법인\
581 외국주식회사\
582 외국합명회사\
583 외국합자회사\
584 외국유한회사\
585 외국기타특수\
586 외국유한책임회사\
594 합자조합회사\
999 기타 (비영리)

### 은행 코드

001한국은행 Bank Of Korea\
002한국산업은행 The Korea Development Bank\
003농업협동조합 National Agricultural Cooperative Federation\
004중소기업은행 Industrial Bank Of Korea\
005국민은행 Kookmin Bank\
006한국외환은행 Korea Exchange Bank\
007국민은행(한국주택은행) Kookmin Bank(Housing & Commercial Bank)\
008수산업협동조합 National Federation Of Fisheries Cooperatives\
009한국수출입은행 The Export-Import Bank Of Korea\
010국민은행(장기) Kookmin Bank(Korea Long Term Credit Bank)\
011축산업협동조합 NATIONAL LIVESTOCK COOPERATIVES FEDERATION\
016조흥은행 Chohung Bank\
017우리은행(한빛) Woori Bank(hanvit)\
018한국스탠다드차타드제일은행 Standard Chartered First Bank Korea Limited\
019우리은행 Woori Bank\
020하나은행(서울) Hana Bank(Seoul Bank)\
021신한은행 Shinhan Bank\
022한국씨티은행 Korea CITI Bank\
024신한생명 Shinhan Life Insurance Co.,Ltd.\
031대구은행 The Daegu Bank Ltd.\
032부산은행 Pusan Bank\
033충청하나은행 The Chung Chong Bank\
034광주은행 The Kwangju Bank Ltd.\
035제주은행 Cheju Bank\
036한미(경기) Koram Bank(Kyungki Bank)\
037전북은행 Jeonbuk Bank\
038강원은행 Kangwon Bank\
039경남은행 Kyongnam Bank\
040조흥(충북)은행 Chohung Bank(Chungbuk Bank)\
041새마을금고 Korea Federation Of Community Credit Cooratives\
042우체국 Korea Post\
051체이스맨하탄은행 THE CHASE MANHATTAN BANK,N.A.SEOUL BRANCH\
052씨티은행 CITI Bank,N.A.Seoul Branch\
053아메리카은행 BANK OF AMERICA\
054도꾜은행 THE BANK OF TOKYO,LTD.\
055미쓰비시은행 THE MITSUBISHI BANK LTD.\
056차타드은행 Standard Chartered Bank\
057다이이찌강교은행(제일권업은행) THE DAI-ICHI KANGYO BANK, LTD.\
058후지은행 THE FUJI BANK LTD.\
059체이스맨하탄은행(부산) THE CHASE MANHATTAN BANK, N.Y.\
060씨티은행(부산) CITI BANK(PUSAN)\
061아메리카은행(부산) BANK OF AMERICA(PUSAN)\
062앵도수에즈은행 BANQUE INDOSUEZ\
063퍼스트내쇼날시카고은행 THE FIRST NATIONAL BANK OF CHICAGO\
064파리국립은행 BANQUE NATIONAL DE PARIS\
065아멕스은행 American Express Bank\
066로이즈국제은행 Lloydts Bank\
067바크레이즈은행 BARCLAYS BANK\
068인도해외은행 INDIAN OVERSEAS BANK\
069파리바은행 BANQUE PARIBAS\
070비씨씨아이국제은행 Canandian Imperial Bank of Commerce\
072싱가폴국제은행 INTERNATIONAL BANK OF SINGAPORE\
073노바스코서은행 THE BANK OF NOVASCOTIA\
074콘티넨탈은행 Continental Savings Bank\
075모간은행 Morgan Stanley Bank\
076크레디리요네은행 CREDIT LYONNAIS\
077유러피안아시안은행 European Asian Bank\
078케미칼은행 CHEMICAL BANK\
079몬트리얼은행 BANK OF MONTREAL\
081뱅커스트러스트은행 BANKERS TRUST COMPANY\
082알지메느은행 Allgemeine Privatkundenbank AG\
083유바프은행 UNION DE BANQUES ARABES ET FRACAISES\
087싱가폴개발은행 THE DEVELOPMENT BANK OF SINGAPORE,LTD.\
088스미또모은행 THE SUMITOMO BANK,LTD.\
089상와은행 THE SANWA BANK CO.,LTD.\
090시큐리티패시픽내셔날 Security Pacific Asia Bank Limited\
091홍콩상하이은행 THE HONG KONG AND SHANGHAI BANKING CO.,LTD.\
092보스톤은행 Boston Bank\
093캐나다로얄은행 ROYAL BANK OF CANADA\
094동해은행 Tokai Bank\
095소시에테제네랄은행 SOCIETE GENERALE\
096도꾜은행(부산) THE BANK OF TOKYO,LTD.(PUSAN)\
097차타드은행(부산) Standard Chartered Bank(PUSAN)\
098유러피안아시안은행(부산) European Asian Bank\
099웰스파고은행 Wel ls Fargo Bank\
100홍콩상하이은행(서울) THE HONG KONG AND SHANGHAI BANKING CO.,LTD.\
101대화은행 UNITED OVERSEAS BANK,LTD.\
103미쓰이은행 Mitsui Trust & Banking Co.,Ltd.\
104주택(동남) Kookmin Bank(DONGNAM BANK)\
105국민(대동) Kookmin Bank(DAEDONG BANK)\
106신한(동화) Shinhan Bank(DONGHWA BANK)\
107캘리포니아은행 THE BANK OF CALIFORNIA N.A.\
109하나은행(보람) HANA BANK(Boram)\
110하나은행 HANA BANK\
111우리은행(평화) Woori Bank(Pyung Hwa)\
114도이치은행 Deutsche Bank AG\
115HSBC은행 Deutsche Bank AG\
116뱅크원은행 Bank One\
117제이피모건체이스은행 JP Morgan Chase\
118캘리포니아유니온은행 Union Bank of California\
119뉴욕은행 Bank of New York\
120와코비아은행 Wachovia Bank\
121스테이트스트리트은행 State Street Bank and Trust\
122바클레이즈은행 Barclays Bank\
123크레디아그리꼴엥도수에즈은행 Credit Agricole\
124에이비엔암로은행 ABN Amro Bank\
125아이엔지은행 ING Bank\
126CSFB은행 CSFB\
127UBS은행 UBS\
128멜라트은행 Bank of Mellat\
129칼리온은행 Calyon Bank\
130메트로은행 Metropolitan Bank and Trust\
131중국은행 Bank of China\
132중국공상은행 Industrial and Commercial Bank of China\
133DBS은행 DBS Bank\
134OCBC은행 Oversea-Chinese Banking\
135도쿄미쓰비시은행 Bank of Tokyo-Mitsubishi\
136미즈호코퍼레이트은행 Mizuho Corporate Bank\
137미쓰이스미또모은행 Sumitomo Mitsui Banking\
138UFJ은행 UFJ Bank\
139야마구찌은행 Yamaguchi Bank\
140호주뉴질랜드은행 Australia and New Zealand Banking Group\
141내쇼날호주은행 National Austraila Bank\
142신용협동조합 Credit Union\
143뱅크오브아메리카 Bank of America Corporation\
025농협은행 NONGHYEOP BANK CO.,LTD.

# GetCompanyHistory

### Function specification

```
GetCompanyHistory(entities)
```

###

### Parameters

| Parameter | Type                                  | Description                                                                                         |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities  | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |

### Examples

```
> GetCompanyHistory(KRX:005930)

...
symbol	date	seq	entity_name	GetCompanyHistory(삼성전자)
KRX:005930	1969-01-13	1	삼성전자	삼성전자공업(주) 설립
KRX:005930	1970-01-01	1	삼성전자	QUALCOMM과 CDMA 관련 기술도입
KRX:005930	1970-01-01	1	삼성전자	수출 100억불 돌파
KRX:005930	1970-01-01	1	삼성전자	22인치 대형 TFT-LCD개발
KRX:005930	1970-01-01	1	삼성전자	I.D.C와 GSM 관련 기술도입
KRX:005930	1970-01-01	1	삼성전자	미국INTEL사와 PC기술관련계약
KRX:005930	1972-11-03	1	삼성전자	흑백TV 생산개시
KRX:005930	1973-04-16	1	삼성전자	흑백TV 수출개시
KRX:005930	1974-03-02	1	삼성전자	냉장고 생산개시
KRX:005930	1974-12-16	1	삼성전자	세탁기 생산개시
KRX:005930	1975-06-30	1	삼성전자	기업공개
...
KRX:005930	2018-03-23	1	삼성전자	대표이사 변경 : 김기남, 김현석, 고동진
KRX:005930	2018-05-17	1	삼성전자	종속기업인 NexusDX, Inc.사 지분 매각
KRX:005930	2019-01-28	1	삼성전자	종속기업인 SEBN(Samsung Electronics Benelux B.V.)의 Corephotonics Ltd.사 지분 인수
KRX:005930	2019-06-01	1	삼성전자	관계기업인 삼성전기(주)로부터 PLP 사업 양수
```

# GetCompanyBusinessGoal

### Function specification

```
GetCompanyBusinessGoal(entities)
```

###

### Parameters

| Parameter | Type                                  | Description                                                                                         |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities  | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |

###

### Examples

```
> GetCompanyBusinessGoal(KRX:005930)

...
symbol	seq	entity_name	GetCompanyBusinessGoal(삼성전자)
KRX:005930	1	삼성전자	전자전기기계기구 및 관련기기와 그 부품의 제작, 판매, 수금대행 및 임대,서비스업
KRX:005930	2	삼성전자	통신기계기구 및 관련기기와 그 부품의 제작, 판매, 수금대행 및 임대, 서비스업
KRX:005930	3	삼성전자	의료기기의 제작 및 판매업
KRX:005930	4	삼성전자	광디스크 및 광원응용기계기구와 그 부품의 제작, 판매, 서비스업
KRX:005930	5	삼성전자	광섬유, 케이블 및 관련기기의 제조, 판매, 임대, 서비스업
KRX:005930	6	삼성전자	전자계산조직 및 동 관련제품의 제조, 판매, 수금대행 및 임대, 서비스업
KRX:005930	7	삼성전자	저작물, 컴퓨터프로그램 등의 제작, 판매, 임대업
KRX:005930	8	삼성전자	노우하우 기술의 판매, 임대업
KRX:005930	9	삼성전자	정보통신시스템에 관련된 구성 및 운영과 역무의 제공
KRX:005930	10	삼성전자	자동제어기기 및 응용설비의 제작, 판매, 임대, 서비스업
KRX:005930	11	삼성전자	공작기계 및 부품의 제작, 판매, 임대, 서비스업
KRX:005930	12	삼성전자	계량기, 측정기 등의 교정검사업 및 제작, 판매업
KRX:005930	13	삼성전자	반도체 및 관련제품의 제조, 판매업
KRX:005930	14	삼성전자	반도체 제조장치의 제조, 판매업
KRX:005930	15	삼성전자	반도체제조를 위한 원부자재의 제조, 판매업
KRX:005930	16	삼성전자	전 각항의 기술용역, 정보통신공사업 및 전기공사업
KRX:005930	17	삼성전자	기타 기계기구의 제작 및 판매업
KRX:005930	18	삼성전자	합성수지의 제조, 가공 및 판매업
KRX:005930	19	삼성전자	금을 제외한 금속의 제련가공 및 판매업
KRX:005930	20	삼성전자	수출입업 및 동 대행업
KRX:005930	21	삼성전자	경제성식물의 재배 및 판매업
KRX:005930	22	삼성전자	부동산업
KRX:005930	23	삼성전자	물품매도 확약서 발행업
KRX:005930	24	삼성전자	주택사업 임대 및 분양
KRX:005930	25	삼성전자	운동, 경기 및 기타 관련사업
KRX:005930	26	삼성전자	전동기, 발전기 및 전기변환장치 제조업
KRX:005930	27	삼성전자	전기공급 및 제어장치 제조업
KRX:005930	28	삼성전자	교육 서비스업 및 사업관련 서비스업
KRX:005930	29	삼성전자	각항에 관련된 부대사업 및 투자
```

####

# GetCompanyBusinessSummary

### Function specification

```
GetCompanyBusinessSummary(entities)
```

###

### Parameters

| Parameter | Type                                  | Description                                                                                         |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities  | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |

###

### Examples

```
> GetCompanyBusinessSummary(KRX:005930)

...
종목코드	기업명	summary_title	summary_content_1	summary_content_2	summary_content_3	status_title	status_content_1	status_content_2	status_content_3	updated_at
KRX:005930	삼성전자	글로벌 스마트폰 판매 점유율 1위 업체	- 동사의 사업부문은 CE(TV, 모니터, 에어컨, 냉장고 등), IM(휴대폰, 통신 시스템, 컴퓨터), DS(메모리 반도체, 시스템LSI), Harman 부문으로 구성되어 있음.	- 글로벌 IT기업으로, 한국과 CE, IM 부문 해외 9개 지역총괄 및 DS 부문 해외 5개 지역총괄의 생산/판매법인, Harman 부문 종속기업 등 228개의 종속기업 보유.	- TV, 스마트폰, 반도체 및 디스플레이 패널 부문 등에서 글로벌 우위의 경쟁력을 확보한바 양호한 사업 포트폴리오로 안정적 이익창출력 확보하고 있음.	외형 성장, 수익률 상승	- Neo QLED TV, 비스포크 등 프리미엄 제품과 플래그십 휴대폰, 고용량 메모리와 OLED 패널 판매확대로 전 부문 고른 성장과 하만 매출 증가에 따라 전년대비 외형 성장.	- 프리미엄 제품 판매 확대로 원가율 하락과 판관비 부담 완화, 하만의 수익 개선에 따라 전년대비 영업이익률 상승한 가운데 기타수지 개선으로 법인세 부담에서 순이익률 상승.	- 스마트폰의 출하량 증가와 DRAM과 NAND 비트그로스 확대, LSI의 매출 증가, 오스틴 공장 가동 중단 기저효과 및 TSMC의 효과로 파운드리 매출 증가하여 매출 성장 전망.	2022-03-16T00:00:00


```

# GetCompanyRelatedFirms

### Function specification

```
GetCompanyRelatedFirms(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 최신의 정보를 바탕으로 합니다. ex)2010-1-1                                        |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 최신의 정보를 바탕으로 합니다. ex)2010-12-31                                      |

### Output Fields ( 단위 : 백만원 )&#x20;

| Field            | Description                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| accounting\_type | <p>accounting\_type 은 아래 다섯 개의 값 중 하나를 가집니다.</p><p><br>'1' - 결산</p><p>'2' - 반기</p><p>'3' - 기타</p><p>'4' - 1/4분기</p><p>'5' - 3/4분기</p> |

### Examples

```
> GetCompanyRelatedFirms(KRX:005930)

...
symbol	date	seq	entity_name	accounting_month	accounting_type	accounting_year	business_area	capital	dividend_rate	founded_date	holding_ratio	net_income	ordinary_profit	related_firm_code	related_firm_name	revenue	total_asset	total_capital
KRX:005930	2019-09-30	1	삼성전자	12	3	2,018	폴리머전지(2차전지),칼라브라운관,PDP,평판표시관,모	356,712	0	Jan 20 1	19.60	525,836	666,749	380458	삼성SDI(주)	8,186,909	15,306,118	10,761,026
KRX:005930	2019-09-30	2	삼성전자	12	3	2,018	영상,음향,통신장비,모듈,다층인쇄회로기판,적층세라	388,003	0	Aug  8 1	23.70	317,643	416,761	380733	삼성전기(주)	5,682,105	5,448,882	3,977,569
KRX:005930	2019-09-30	3	삼성전자	12	3	2,018	선박(벌크선,원유운반선),철구조물,에너지플랜트 생산	3,150,574	0	Aug  5 1	16.00	-436,189	-577,933	380180	삼성중공업(주)	4,819,075	13,669,099	6,565,051
KRX:005930	2019-09-30	4	삼성전자	12	3	2,018	면세판매,관광숙박,외식사업,예식업	200,000	0	May  9 1	5.10	92,575	125,965	630039	(주)호텔신라	3,643,940	2,244,199	863,302
KRX:005930	2019-09-30	5	삼성전자	12	3	2,018	광고 대행/광고물,영화 제작,인쇄,출판	23,008	0	Jan 17 1	25.20	79,285	100,041	820032	(주)제일기획	1,198,292	1,220,020	668,309
KRX:005930	2019-09-30	6	삼성전자	12	3	2,018	컴퓨터 프로그래밍,시스템 통합,관리/소프트웨어 개발	38,688	0	May  1 1	22.60	534,496	747,236	820717	삼성에스디에스(주)	5,083,718	6,178,103	5,170,648
...

```

####

# GetCompanyDebts

### Function specification

```
GetCompanyDebts(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-1-1                                         |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-12-31                                       |

### Output Fields ( 단위 : 백만원 )

| Field      | Description                                                                                                                                                      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| debt\_type | 01=당좌차월,03=외화단기차입금,04=어음차입금, 05=특수관계자단기차입금,06=기타단기차입금, 07=단기차입금합계,08=장기차입금,09=외화장기차입금, 10=기타장기차입금,11=장기차입금합계,12=(유동성장기차입금), 13=회사채,14=(유동성사채),15=금융리스부채,16=차입금총계 |

### Examples

```
> GetCompanyDebts(KRX:005930)

...
symbol	date	debt_type	entity_name	amount	debt_type_name
KRX:005930	1996-12-31	01	삼성전자	4,949	당좌차월
KRX:005930	1996-12-31	03	삼성전자	381,897	외화단기차입금
KRX:005930	1996-12-31	04	삼성전자	0	어음차입금
KRX:005930	1996-12-31	05	삼성전자	0	특수관계자단기차입금
KRX:005930	1996-12-31	06	삼성전자	383,822	기타단기차입금
KRX:005930	1996-12-31	07	삼성전자	770,669	단기차입금합계
KRX:005930	1996-12-31	08	삼성전자	879,547	장기차입금
KRX:005930	1996-12-31	09	삼성전자	2,040,418	외화장기차입금
KRX:005930	1996-12-31	10	삼성전자	0	기타장기차입금
KRX:005930	1996-12-31	11	삼성전자	2,919,964	장기차입금합계
KRX:005930	1996-12-31	12	삼성전자	286,606	(유동성장기차입금)
KRX:005930	1996-12-31	13	삼성전자	2,101,856	회사채
KRX:005930	1996-12-31	14	삼성전자	25,326	(유동성사채)
...

```

####

# GetCompanyDividends

### Function specification

```
GetCompanyDividends(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-1-1                                         |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-12-31                                       |

###

### Examples

```
> GetCompanyDividends(KRX:005930)

...
symbol	date	type	entity_name	accounting_type	amount	dividend_type_name
KRX:005930	1996-12-31	00	삼성전자	1	28.00	회기
KRX:005930	1996-12-31	01	삼성전자	1	164,155,481.00	당기순이익(천원)
KRX:005930	1996-12-31	02	삼성전자	1	1,784.00	주당순이익(원)
KRX:005930	1996-12-31	03	삼성전자	1	35.70	주당순이익률(%)
KRX:005930	1996-12-31	04	삼성전자	1	600.00	주당현금배당액(소주주,보통주)(원)
KRX:005930	1996-12-31	05	삼성전자	1	12.00	주당현금배당률(소주주,보통주)(%)
KRX:005930	1996-12-31	06	삼성전자	1	0.00	주당무상배당액(소주주,보통주)(원)
KRX:005930	1996-12-31	07	삼성전자	1	0.00	주당무상배당률(소주주,보통주)(%)
KRX:005930	1996-12-31	08	삼성전자	1	39.20	배당성향(%)
KRX:005930	1996-12-31	09	삼성전자	1	44,326.00	주당순자산(원)
KRX:005930	1997-12-31	00	삼성전자	1	29.00	회기
KRX:005930	1997-12-31	01	삼성전자	1	123,504,909.00	당기순이익(천원)
KRX:005930	1997-12-31	02	삼성전자	1	1,232.00	주당순이익(원)
KRX:005930	1997-12-31	03	삼성전자	1	24.60	주당순이익률(%)
KRX:005930	1997-12-31	04	삼성전자	1	500.00	주당현금배당액(소주주,보통주)(원)
KRX:005930	1997-12-31	05	삼성전자	1	10.00	주당현금배당률(소주주,보통주)(%)
KRX:005930	1997-12-31	06	삼성전자	1	0.00	주당무상배당액(소주주,보통주)(원)
KRX:005930	1997-12-31	07	삼성전자	1	0.00	주당무상배당률(소주주,보통주)(%)
KRX:005930	1997-12-31	08	삼성전자	1	48.60	배당성향(%)
KRX:005930	1997-12-31	09	삼성전자	1	47,800.00	주당순자산(원)
...
```

####

# GetCompanyShareholders

### Function specification

```
GetCompanyShareholders(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기간을 대상으로 합니다. ex)2010-1-1                                      |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기을 대상으로 합니다. ex)2010-12-31                                     |

### Output Fields

| Field            | Description                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| stock\_type      | 주식 구분 ( 1=보통주, 2=우선주, 3=합계, 4=기타주식 )                                                                                                  |
| accounting\_type | <p>accounting\_type 은 아래 다섯 개의 값 중 하나를 가집니다.</p><p><br>'1' - 결산</p><p>'2' - 반기</p><p>'3' - 기타</p><p>'4' - 1/4분기</p><p>'5' - 3/4분기</p> |

### Examples

```
> GetCompanyShareholders(KRX:005930)

...
symbol	date	seq	stock_type	accounting_type	entity_name	name	no_shares	ownership_percentage	relation_to_company	relation_to_largest_shareholder	stock_type_name
KRX:005930	2019-09-30	1	1	5	삼성전자	국민연금공단	626,094,383	10.49			보통주
KRX:005930	2019-09-30	2	1	5	삼성전자	삼성생명보험(주)	508,157,148	8.51			보통주
KRX:005930	2019-09-30	3	1	5	삼성전자	BlackRock Fund Advisors	300,391,061	5.03			보통주
KRX:005930	2019-09-30	4	1	5	삼성전자	삼성물산(주)	298,818,100	5.01			보통주
KRX:005930	2019-09-30	5	1	5	삼성전자	이건희	249,273,200	4.18			보통주
KRX:005930	2019-09-30	6	1	5	삼성전자	삼성화재해상보험(주)	88,802,052	1.49			보통주
KRX:005930	2019-09-30	7	1	5	삼성전자	홍라희	54,153,600	0.91			보통주
KRX:005930	2019-09-30	8	1	5	삼성전자	이재용	42,020,150	0.70			보통주
KRX:005930	2019-09-30	9	1	5	삼성전자	삼성생명보험(주)(특별계정)	19,329,524	0.32			보통주
KRX:005930	2019-09-30	10	1	5	삼성전자	(재)삼성복지재단	4,484,150	0.08			보통주
KRX:005930	2019-09-30	11	1	5	삼성전자	(재)삼성문화재단	1,880,750	0.03			보통주
KRX:005930	2019-09-30	12	1	5	삼성전자	김기남	200,000	0.00			보통주
...

```

####

# GetCompanyEmployees

### Function specification

```
GetCompanyEmployees(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-1-1                                         |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다. ex)2010-12-31                                       |

###

### Examples

```
> GetCompanyEmployees(KRX:005930)

...
symbol	date	employee_type	entity_name	accounting_type	average_monthly_salary	no_employees	employee_type_name
KRX:005930	1996-06-30	01	삼성전자	2	0	0	임원
KRX:005930	1996-06-30	02	삼성전자	2	2,034	37,659	사무직
KRX:005930	1996-06-30	03	삼성전자	2	0	0	기술직
KRX:005930	1996-06-30	04	삼성전자	2	1,691	24,013	생산직
KRX:005930	1996-06-30	05	삼성전자	2	0	0	기타
KRX:005930	1996-06-30	06	삼성전자	2	1,900	61,672	합계
KRX:005930	1996-12-31	01	삼성전자	1	0	0	임원
KRX:005930	1996-12-31	02	삼성전자	1	1,972	33,650	사무직
KRX:005930	1996-12-31	03	삼성전자	1	0	0	기술직
KRX:005930	1996-12-31	04	삼성전자	1	1,640	25,436	생산직
KRX:005930	1996-12-31	05	삼성전자	1	0	0	기타
KRX:005930	1996-12-31	06	삼성전자	1	1,829	59,086	합계
KRX:005930	1997-06-30	01	삼성전자	2	0	0	임원
KRX:005930	1997-06-30	02	삼성전자	2	0	8,444	사무직
KRX:005930	1997-06-30	03	삼성전자	2	0	0	기술직
KRX:005930	1997-06-30	04	삼성전자	2	0	21,074	생산직
KRX:005930	1997-06-30	05	삼성전자	2	0	31,702	기타
KRX:005930	1997-06-30	06	삼성전자	2	0	61,220	합계
KRX:005930	1997-12-31	01	삼성전자	1	0	59	임원
KRX:005930	1997-12-31	02	삼성전자	1	0	13,320	사무직
KRX:005930	1997-12-31	03	삼성전자	1	0	0	기술직
KRX:005930	1997-12-31	04	삼성전자	1	0	22,097	생산직
KRX:005930	1997-12-31	05	삼성전자	1	0	22,341	기타
KRX:005930	1997-12-31	06	삼성전자	1	0	57,817	합계
KRX:005930	1998-06-30	01	삼성전자	2	0	19	임원
KRX:005930	1998-06-30	02	삼성전자	2	0	11,183	사무직
KRX:005930	1998-06-30	03	삼성전자	2	0	0	기술직
KRX:005930	1998-06-30	04	삼성전자	2	0	21,887	생산직
...

```

###

####

# GetCompanyExecutives

### Function specification

```
GetCompanyExecutives(entities, date_from=None, date_to=None)
```

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기간을 대상으로 합니다. ex)2010-1-1                                      |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기간을 대상으로 합니다. ex)2010-12-31                                    |

###

### Examples

```
> GetCompanyExecutives(KRX:005930)

...
symbol	date	seq	entity_name	birthday	experiences	name	position
KRX:005930	2019-09-30	1	삼성전자	19580414	ㆍ삼성전자 DS부문장	김기남	대표이사
KRX:005930	2019-09-30	2	삼성전자	19610123	ㆍ삼성전자 CE부문장	김현석	대표이사
KRX:005930	2019-09-30	3	삼성전자	19610326	ㆍ삼성전자 IM부문장	고동진	대표이사
KRX:005930	2019-09-30	4	삼성전자	19550615	ㆍ(전)삼성전자 경영지원실장	이상훈	사내이사
KRX:005930	2019-09-30	5	삼성전자	19680623	ㆍ삼성전자 부회장	이재용	사내이사
KRX:005930	2019-09-30	6	삼성전자	19550124	ㆍ성균관대 행정학과 교수	박재완	사외이사
KRX:005930	2019-09-30	7	삼성전자	19521221	ㆍ이화여대 명예교수	김선욱	사외이사
KRX:005930	2019-09-30	8	삼성전자	19590400	ㆍ서울대 전기ㆍ정보공학부 교수	박병국	사외이사
KRX:005930	2019-09-30	9	삼성전자	19600800	ㆍKiswe Mobile 회장	김종훈	사외이사
KRX:005930	2019-09-30	10	삼성전자	19550300	ㆍ서울대 의과대학 신장내과 교수	안규리	사외이사
KRX:005930	2019-09-30	11	삼성전자	19560700	ㆍ하나금융나눔재단 이사장	김한조	사외이사
KRX:005930	2019-09-30	12	삼성전자	19420109	대표이사 회장	이건희	회장
KRX:005930	2019-09-30	13	삼성전자	19521015	대표이사 부회장	권오현	회장
KRX:005930	2019-09-30	14	삼성전자	19560116	대표이사 사장	신종균	부회장
KRX:005930	2019-09-30	15	삼성전자	19530206	대표이사 사장	윤부근	부회장
KRX:005930	2019-09-30	16	삼성전자	19580708	준법경영실장	김상균	사장
KRX:005930	2019-09-30	17	삼성전자	19580801	삼성에스디에스 대표이사	전동수	사장
KRX:005930	2019-09-30	18	삼성전자	19570103	정밀화학 대표이사	성인희	사장
KRX:005930	2019-09-30	19	삼성전자	19600306	디지털이미징사업부장	정현호	사장
...

```

####

# GetCompanyBranches

### Function specification

```
GetCompanyBranches(entities)
```

###

### Parameters

| Parameter | Type                                  | Description                                                                                         |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities  | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |

###

### Examples

```
> GetCompanyBranches(KRX:005930)

...
symbol	seq	entity_name	address_en	address_ko	branch_code	business_name	business_rid	date_closed	date_open	fax	industry_name	is_closed	name_en	name_ko	tel	zipcode
KRX:005930	1	삼성전자	129, Samseong-ro Yeongtong-gu Suwon-si Gyeonggi	경기 수원시 영통구 삼성로 129	01		1248100998		19690113	031-200-1105		TRUE		본사	031-200-1114	16677
KRX:005930	11	삼성전자	129, Samseong-ro Yeongtong-gu Suwon-si Gyeonggi	경기 수원시 영통구 삼성로 129	02				19690113	031-200-1105		TRUE		공장/연구소	031-200-1114	16677
KRX:005930	12	삼성전자	11, Seocho-daero 74-gil Seocho-gu Seoul	서울 서초구 서초대로74길 11	03				19690113	02-2255-0117		TRUE		영업소	02-2255-0114	06620
KRX:005930	13	삼성전자	107, Hanamsandan 6beon-ro Gwangsan-gu Gwangju	광주 광산구 하남산단6번로 107	03				19690113	062-950-6114		TRUE		광주사업장	062-950-6114	62218
KRX:005930	14	삼성전자	88, Seosomun-ro Jung-gu Seoul	서울 중구 서소문로 88	03				19690113			TRUE		사무소	02-751-6114	04511
KRX:005930	15	삼성전자		광주광산구	05		4108506566	20071231				TRUE		하남사업장		
KRX:005930	16	삼성전자		경북구미시임수동941	05		5138504630	20071231				TRUE		구미2공장		
KRX:005930	17	삼성전자		경기수원매탄4의16	05		1308508009	19990413				TRUE		지점		
KRX:005930	18	삼성전자		경기용인시기흥읍농서리24	05		1358500360	20071231				TRUE		기흥공장		
KRX:005930	19	삼성전자	158, Baebang-ro Baebang-eup Asan-si Chungnam	충남 아산시 배방읍 배방로 158	05		3128505185	20071231				TRUE		온양공장		31489
KRX:005930	20	삼성전자		경기수원매탄4의16	05		5138503664	20071231				TRUE		구미공장		
KRX:005930	22	삼성전자	181, Samseong-ro Tangjeong-myeon Asan-si Chungnam	충남 아산시 탕정면 삼성로 181	05		3128527587	20071231				TRUE		탕정공장		31454
...


```

# GetFinancialStatements

### Function specification

```
GetFinancialStatements(entities, report_type="IFRS", consolidated=True,
                is_annual=True, is_accumulated =False, report_ids=None, date_from=None, date_to=None))
```

###

### Parameters

| Parameter           | Type                     | Description                                                                                            |
| ------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------ |
| entities            | string or list of string | 재무제표 조회 대상 기업 리스트                                                                                      |
| report\_type        | string                   | IFRS, GAAP                                                                                             |
| consolidated        | boolean                  | 연결 여부                                                                                                  |
| is\_annual          | boolean                  | <p>연간 재무제표만 조회할지, 분기 재무제표를 포함할</p><p>지 선택</p>                                                          |
| is\_accumulated     | boolean                  | 분기 재무제표의 경우, 분기 누적 데이터를 조회할지, 3개월 증분 데이터를 조회할지 선택 ( 손익계산서, 현금흐름표에 대하여 적용 )                             |
| report\_ids         | string                   | <p>조회 대상 재무제표. 특별한 지정이 없으면 전체 재무제표를 조회합니다. </p><ul><li>Income, CashFlow, BalanceSheet, Ratio</li></ul> |
| date\_from/date\_to | date                     | 조회 기준 재무제표 기준 일자 ( ex) 2015-01-01 )                                                                    |

### Examples

```
> GetFinancialStatements(삼성전자, report_type="IFRS",date_from=2015-01-01, date_to=2015-12-31)
                
...                
date	symbol	entity_name	type_id	report_id	account_id	name_ko	value
2015-12-31	KRX:005930	삼성전자	K	11	1100	현금및현금성자산	22,636,744,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1110	현금	40,337,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1130	예금	22,596,407,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1134	기타예금	22,596,407,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1141	[수익증권]	1,606,320,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1143	[채무증권]	3,021,210,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1147	원화매출채권	25,168,026,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1148	[기타단기투자자산]	44,228,800,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1150	매출채권	25,168,026,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1156	매출채권및기타채권	28,520,689,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1162	매도가능금융자산	4,627,530,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1180	미수금	3,352,663,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1183	기타미수금	3,352,663,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1200	기타당좌자산	1,035,460,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1220	단기금융상품	44,228,800,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1221	[사용제한단기금융상품]	14,032,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1225	기타단기금융상품	44,228,800,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1230	당기손익인식금융자산	44,228,800,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1232	기타당기손익인식금융자산	44,228,800,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1233	단기투자자산	48,856,330,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1259	투자자산	77,073,000,000
2015-12-31	KRX:005930	삼성전자	K	11	1320	제품	5,769,460,000,000
...
```

### 재무 계정 코드&#x20;

{% file src="<https://2002947409-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LPJrnQiLiz9bWVBvx6Q%2Fuploads%2FcTeK5z7vt2eyjM42IWId%2FDeepSearch_%E1%84%8C%E1%85%A2%E1%84%86%E1%85%AE%E1%84%80%E1%85%A8%E1%84%8C%E1%85%A5%E1%86%BC%E1%84%8E%E1%85%A6%E1%84%80%E1%85%A8_220706.xlsx?alt=media&token=069a055a-18d7-46f8-bad0-f8361310f6b9>" %}

# GetAvailableFinancialStatements

### Function specification

```
GetAvailableFinancialStatements(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type                     | Description              |
| ------------------- | ------------------------ | ------------------------ |
| entities            | string or list of string | 조회할 기업                   |
| date\_from/date\_to | date                     | 조회 기간 ( ex) 2010-01-01 ) |

###

### Examples

```
> GetAvailableFinancialStatements(KRX:005930)

...
date	symbol	entity_name	type	type_id	consolidated	converted
2018-12-31	KRX:005930	삼성전자	IFRS	K	TRUE	FALSE
2018-12-31	KRX:005930	삼성전자	IFRS	K	FALSE	FALSE
2018-12-31	KRX:005930	삼성전자	GAAP	K	TRUE	TRUE
2018-12-31	KRX:005930	삼성전자	GAAP	K	FALSE	TRUE
2019-03-31	KRX:005930	삼성전자	IFRS	F	TRUE	FALSE
2019-03-31	KRX:005930	삼성전자	IFRS	F	FALSE	FALSE
2019-03-31	KRX:005930	삼성전자	GAAP	F	TRUE	TRUE
2019-03-31	KRX:005930	삼성전자	GAAP	F	FALSE	TRUE
2019-06-30	KRX:005930	삼성전자	IFRS	B	TRUE	FALSE
2019-06-30	KRX:005930	삼성전자	IFRS	B	FALSE	FALSE
2019-06-30	KRX:005930	삼성전자	GAAP	B	TRUE	TRUE
2019-06-30	KRX:005930	삼성전자	GAAP	B	FALSE	TRUE
2019-09-30	KRX:005930	삼성전자	IFRS	T	TRUE	FALSE
2019-09-30	KRX:005930	삼성전자	IFRS	T	FALSE	FALSE
2019-09-30	KRX:005930	삼성전자	GAAP	T	TRUE	TRUE
2019-09-30	KRX:005930	삼성전자	GAAP	T	FALSE	TRUE
2019-12-31	KRX:005930	삼성전자	IFRS	K	TRUE	FALSE
2019-12-31	KRX:005930	삼성전자	IFRS	K	FALSE	FALSE
2019-12-31	KRX:005930	삼성전자	GAAP	K	TRUE	TRUE
2019-12-31	KRX:005930	삼성전자	GAAP	K	FALSE	TRUE



```

# GetConsensusInstitutionList

### Function specification

```
GetConsensusInstitutionList()
```

###

### Examples

```
> GetConsensusInstitutionList()
...
inst_code	foreign	name_en	name_ko
058585	0	KB INVESTMENT & SECURITIES CO.,LTD.	KB투자증권
073227	1	JP MORGAN SECURITIES	제이피모간증권
074704	0	SHINHAN BNP PARIBAS INVESTMENT ASSET MANAGEMENT CO.,LTD.	신한BNP파리바증권
080169	1	CITY GROUP GLOBAL MARKET SECURITIES	씨티그룹글로벌마켓증권
098988	1	Lehman Brothers International Securities Seoul Branch	리먼브러더스인터내셔날증권서울지점
108972	1	PRUDENTIAL INVESTMENT & SECURITIES	푸르덴셜투자증권
126106	0	HI INVESTMENT & SECURITIES	하이투자증권
127283	0	EBEST INVESTMENT SECURITIES CO.,LTD.	이베스트투자증권
128110	0	MIRAE ASSET SECURITIES	미래에셋증권
128814	0	KIWOOM.COM SECURITIES	키움증권
147568	0	Hana Financial Investment Co., Ltd.	하나금융투자
167342	0	LEADING INVESTMENT & SECURITIES	리딩투자증권
178872	0	HEUNGKUK SECURITIES CO.,LTD.	흥국증권
178879	1	DEUTSCHE SECURITIES KOREA CO.,LTD.	도이치증권
198351	1	GOLDMAN SACHS	골드만삭스증권
466752	1	MACQUARIE SECURITIES KOREA LIMITED	맥쿼리증권
486706	1	UBS SECURITIES LIMITED CO.,LTD.	유비에스증권리미티드
591092	1	DAIWA SECURITIES CO.,LTD. SEOUL BRANCH	다이와증권서울지점
591106	1	MORGAN STANLEY INT'L	모간스탠리인터내셔날증권
591246	1	MERRILLYNCH INTERNATIONAL	메릴린치인터내셔날증권
591327	1	THE NOMURA SECURITY CO.,LTD. SEOUL BRANCH	노무라증권서울지점
591483	1	CREDIT SUISSE SECURITIES LTD. SEOUL BRANCH	크레디트스위스증권서울지점
591572	1	R.B.S ASIA SECURITY LTD.	알비에스아시아증권
591645	1	HSBC	에이치에스비씨
...
```

# GetConsensusAnalystList

### Function specification

```
GetConsensusAnalystList(inst_code)
```

###

### Parameters

| Parameter  | Type   | Description |
| ---------- | ------ | ----------- |
| inst\_code | string | 기관 코드       |

###

### Examples

```
> GetConsensusAnalystList(inst_code)
...
analyst_id	email	inst_code	name	tel
1	bcpark@goodi.com	860280	박병칠	3772-1567
19		860280	권재민	
29	kdjsteel@goodi.com	860280	김동준	(02)3772-1543
33		860280	김미영	
49		860280	김영진	
68		860280	김태형	
75	hwkim@goodi.com	860280	김효원	3772-1596
78		860280	남권오	
98		860280	박성미	
143		860280	손종원	
144		860280	손현호	
157		860280	송지현	
159		860280	신기영	
179		860280	오재원	
208	skleebz@goodi.com	860280	이성권	3772-2603
218		860280	이승호	
280		860280	정연구	
283		860280	정용래	
301	baiyan@goodi.com	860280	조중재	3772-1536
345		860280	황폴	
346		860280	황형석	
359	joylee@goodi.com	860280	이주영	3772-1573
```

# SearchAnalystReports

### Function specification

```
SearchAnalystReports(symbols=None, inst_code=None, analyst_id=None,
                                date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type                     | Description        |
| ------------------- | ------------------------ | ------------------ |
| symbols             | string or list of string | 종목 코드 or 종목        |
| inst\_code          | string                   | 기관 코드              |
| analyst\_id         | string                   | 애널리스트 코드           |
| date\_from/date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> SearchAnalystReports(삼성전자)
...
date	symbol	entity_name	analyst_id1	analyst_id2	analyst_id3	class	industry_code1	industry_code2	industry_code3	inst_code	language	seq	subclass	title	inst_name_en	inst_name_ko	analyst_email1	analyst_name1	analyst_tel1	analyst_email2	analyst_name2	analyst_tel2	analyst_email3	analyst_name3	analyst_tel3
2002-02-04	KRX:005930	삼성전자	269	0	0	01				860123	0	5	01	삼성전자(05930/Outperform/300,500원)	SK SECURITIES	SK증권		전우종		None	None	None	None	None	None
2002-02-21	KRX:005930	삼성전자	0	0	0	01				860182	0	1	01	삼성전자우선주 전화관련 이슈에 대한 Comments	KOREA INVESTMENT & SECURITIES	한국투자증권	None	None	None	None	None	None	None	None	None
2002-03-04	KRX:005930	삼성전자	0	0	0	01				860034	0	1	01	삼성전자(05930) 반도체부문의 강력한 실적호전으로 2002년 영업이익 6조원 상회할 전 망 -	EUGENE INVESTMENT & SECURITIES	유진투자증권	None	None	None	None	None	None	None	None	None
2002-03-07	KRX:005930	삼성전자	0	0	0	01				821616	0	10	01	路發하는 중국 H/W IT, 두려워만 할 것인가!	SAMSUNG SECURITIES	삼성증권	None	None	None	None	None	None	None	None	None
2002-03-18	KRX:005930	삼성전자	269	0	0	01				860123	0	7	01	삼성전자(05930/Outperform/344,000원)	SK SECURITIES	SK증권		전우종		None	None	None	None	None	None
2002-03-18	KRX:005930	삼성전자	0	0	0	01				860255	0	3	01	삼성전자 05930 buy	YUANTA SECURITIES KOERA CO., LTD.	유안타증권	None	None	None	None	None	None	None	None	None
2002-03-19	KRX:005930	삼성전자	287	0	0	01				860085	0	1	01	삼성전자(A0593/적극매수/333,000원) : 지금은 오히려 사야 할 때	MIRAE ASSET DAEWOO	미래에셋대우		정창원		None	None	None	None	None	None
2002-03-21	KRX:005930	삼성전자	0	0	0	01				860220	0	1	01	Samsung Electronics(05930) - 영문자료	(Merged)DONGWON SECURITIES	(구)동원증권	None	None	None	None	None	None	None	None	None
...

```

# SearchTargetPrices

### Function specification

```
SearchTargetPrices(symbols, date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type                     | Description          |
| ------------------- | ------------------------ | -------------------- |
| symbols             | string or list of string | 종목 코드 or 종목          |
| date\_from/date\_to | date                     | 조회 기간 ( YYYY-MM-DD ) |

### Results

* opinion\_code : 1\~2 는 부정, 3 은 중립, 4\~5는 긍정으로 표현 ( 5로 갈수록 강한 긍정 )

### Examples

```
> SearchTargetPrices(삼성전자)
...
date	symbol	entity_name	analyst_id1	analyst_id2	analyst_id3	current_price	current_price_date	inst_code	opinion_code	target_price	name_ko	name_en
2004-01-05	KRX:005930	삼성전자	287	0	0	449,000	20040102	860085	4	570,000	미래에셋대우	MIRAE ASSET DAEWOO
2004-01-07	KRX:005930	삼성전자	202	0	0	460,000	20040106	821640	3	501,000	DB금융투자	DB Financial Investment
2004-01-07	KRX:005930	삼성전자	147	0	0	465,000	20040107	860204	4	524,000	메리츠증권	MERITZ SECURITIES
2004-01-08	KRX:005930	삼성전자	307	0	0	465,000	20040107	860077	4	580,000	대신증권	DAISHIN SECURITIES
2004-01-09	KRX:005930	삼성전자	202	0	0	469,000	20040108	821640	3	501,000	DB금융투자	DB Financial Investment
2004-01-12	KRX:005930	삼성전자	170	0	0	508,000	20040109	860026	4	600,000	한화투자증권	HANWHA SECURITIES
2004-01-14	KRX:005930	삼성전자	56	0	0	503,000	20040113	860263	4	570,000	케이비증권	KB SECURITIES CO.,LTD.
2004-01-15	KRX:005930	삼성전자	256	0	0	494,500	20040114	821616	4	495,000	삼성증권	SAMSUNG SECURITIES
2004-01-16	KRX:005930	삼성전자	256	0	0	496,500	20040115	821616	4	660,000	삼성증권	SAMSUNG SECURITIES
2004-01-16	KRX:005930	삼성전자	202	0	0	496,500	20040115	821640	3	501,000	DB금융투자	DB Financial Investment
2004-01-16	KRX:005930	삼성전자	307	0	0	496,500	20040115	860077	4	580,000	대신증권	DAISHIN SECURITIES
2004-01-16	KRX:005930	삼성전자	287	0	0	494,500	20040114	860085	4	570,000	미래에셋대우	MIRAE ASSET DAEWOO
2004-01-16	KRX:005930	삼성전자	47	0	0	496,500	20040115	860115	4	531,000	교보증권	KYOBO SECURITIES
2004-01-16	KRX:005930	삼성전자	128	0	0	506,000	20040116	860182	4	590,000	한국투자증권	KOREA INVESTMENT & SECURITIES
2004-01-16	KRX:005930	삼성전자	314	0	0	496,500	20040115	860190	4	590,000	(구)우리증권	(Merged)WOORI SECURITIES
2004-01-16	KRX:005930	삼성전자	147	0	0	496,500	20040115	860204	4	600,000	메리츠증권	MERITZ SECURITIES
2004-01-16	KRX:005930	삼성전자	56	0	0	496,500	20040115	860263	4	670,000	케이비증권	KB SECURITIES CO.,LTD.
2004-01-19	KRX:005930	삼성전자	118	0	0	506,000	20040116	126106	4	670,000	하이투자증권	HI INVESTMENT & SECURITIES
2004-01-19	KRX:005930	삼성전자	202	0	0	506,000	20040116	821640	3	524,000	DB금융투자	DB Financial Investment
...
```

# SearchFirmFundamentalsForecasts

### Function specification

```
SearchFirmFundamentalsForecasts(symbols, last_only=True, accounting_types=None,
                                date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type                     | Description                                                  |
| ------------------- | ------------------------ | ------------------------------------------------------------ |
| symbols             | string or list of string | 종목 코드 or 종목명                                                 |
| last\_only          | boolean                  | 최신 데이터만 조회 여부                                                |
| accounting\_types   | string                   | K - annual, F - March, X - June, Y - September, Z - December |
| date\_from/date\_to | date                     | 조회 기간 ( YYYY-MM-DD )                                         |

### 비고

* 결과 파라미터의 csd\_ prefix 는 연결 재무제표 항목임을 표현합니다.

### Examples

```
> SearchFirmFundamentalsForecasts(삼성전자)
...
stock_code	forecast_date	accounting_type	inst_code	name_ko	name_en	bps	continuing_profit	csd_bps	csd_continuing_profit	csd_ebitda	csd_eps	csd_ev_ebitda	csd_net_income	csd_operating_income	csd_pbr	csd_per	csd_revenue	csd_roe	date	ebitda	eps	ev_ebitda	net_income	operating_income	ordinary_profit	pbr	per	revenue	revenue_growth	roe	seq	unit_code
005930	201909	Y	860034	유진투자증권	EUGENE INVESTMENT & SECURITIES				8,300,000,000				6,300,000,000	7,730,000,000			62,250,000,000		2019-10-10												6	02
005930	201909	Y	860204	메리츠증권	MERITZ SECURITIES								6,300,000,000	7,800,000,000			62,000,000,000		2019-11-19												11	02
005930	201909	Y	860301	엔에이치투자증권	NH INVESTMENT & SECURITIES CO.,LTD.				8,449,000,000				5,936,000,000	7,705,000,000			61,855,000,000		2019-10-10												7	02
005930	201909	Y	C17557	IBK투자증권	IBK INVESTMENT & SECURITIES CO.,LTD.									7,713,000,000			62,542,000,000		2019-10-10												4	02
005930	201909	Y	C47004	KTB투자증권	KTB SECURITIES CO.,LTD.									7,700,000,000			62,000,000,000		2019-10-10												6	02
005930	201912	K	126106	하이투자증권	HI INVESTMENT & SECURITIES			37,090	30,432,000,000		3,166	4.70	21,505,000,000	27,769,000,000	1.50	18.10	230,401,000,000	8.70	2020-01-31												8	02
...

```

* **예시 : 삼성전자 및 LG전자의 2020년의 당기순이익에 대한 컨센서스 평균 계산**&#x20;

1\. API 호출&#x20;

* `SearchFirmFundamentalsForecasts([KRX:005930, KRX:066570],True,"K",2020-04-16)`
* last\_only=true -> 증권사별로 6개월 동안 여러번 컨센데이터를 발표한 경우 가장 마지막것을 사용
* 2020-4-16 : 오늘이 2020-10-16인 경우, 이전 6개월 날짜를 지정

2\. API 결과 처리

* `forecast_date` 날짜 별로 컨센서스 결과 값 그룹핑
  * 재무변수 앞에 `csd_` 가 붙었을 경우 `연결` 없는 경우 `개별`
* `forecast_date` 로 그룹핑된 리스트의 특정 재무데이터의 평균을 구함
  * 증권사에 예측값이 없을 경우 포함하지 않음
* forecast\_date 가 202012 인 값들의 `csd_revenue` 값의 평균을 계산&#x20;

# GetCompanyShareholderChanges

### Function specification

```
GetCompanyShareholderChanges(date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type | Description                 |
| ------------------- | ---- | --------------------------- |
| date\_from/date\_to | date | 최대 주주 변경 기준 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetCompanyShareholderChanges(date_from=2019-1-1, date_to=2019-12-31)
...
symbol	entity_name	GetCompanyShareholderChanges(2019-01-01, 2019-12-31)
NICE:I10851	프론테오코리아	100.00
NICE:355151	태평양밸브공업	100.00
NICE:I10865	마키노코리아	100.00
NICE:388491	한국엔에스케이	100.00
NICE:143412	엔티티코리아	100.00
NICE:223085	한영회계법인	100.00
NICE:098344	파나소닉코리아	100.00
NICE:J06559	우리카드	100.00
NICE:JH7897	창성인더스트리	100.00
NICE:C83772	에더트로닉스코리아	100.00
NICE:JD8491	크린시티	100.00
NICE:466754	존슨매티카탈리스트코리아	100.00
NICE:048524	한국야스카와전기	100.00
NICE:381949	제이더블유메디칼	100.00
NICE:941972	한국브라운포맨	100.00
NICE:HN2923	하늘내린항공	90.91
NICE:384002	퀀텀헬스케어코리아	89.33
NICE:F45662	누리절전시스템	88.86
NICE:H84401	담우	87.18
NICE:F85714	우리티엠에스	87.18
NICE:H81587	대덕환경산업	86.27
NICE:F18579	에이탑이엔지	86.00
NICE:IR2272	이코어	82.43
NICE:933449	케이디디아이코리아	82.37
NICE:065658	한능전자	81.65
NICE:JF3200	대연엘리베이터	80.00
NICE:154698	자이에스앤디	77.75
NICE:380938	쌍용자동차	74.65
NICE:985953	에스앤씨엔지니어링	71.61
...

```

####

# GetTargetPriceConsensusChange

### Function specification

```
GetTargetPriceConsensusChange(relative_to=1, duration=6)
```

###

### Parameters

| Parameter    | Type    | Description                                                    |
| ------------ | ------- | -------------------------------------------------------------- |
| relative\_to | integer | 비교 대상 시기를 지정합니다. 예를 들어, 1을 입력하면, 1개월전이 기준 기간이 됩니다.             |
| duration     | integer | 컨센서스 평균을 계산하는 기간을 지정합니다. 예를 들어, 6을 입력하면, 최근 6개월간의 평균 값을 이용합니다. |

### Examples

```
> GetTargetPriceConsensusChange(relative_to=3)
...
           entity_name  mean_before  count_before   mean_after  count_after
symbol                                                                     
KRX:000060       메리츠화재   27166.6667             9   24166.6667            9
KRX:000080       하이트진로   23318.1818            11   24666.6667            9
KRX:000100        유한양행  311250.0000            16  305384.6154           13
KRX:000120      CJ대한통운  197357.1429            14  195357.1429           14
KRX:000150          두산  140777.7778             9  143000.0000            9
KRX:298050      효성첨단소재  167000.0000             6  172000.0000            5
KRX:299900     위지윅스튜디오   21200.0000             1   20000.0000            1
KRX:316140      우리금융지주   19523.0769            13   19200.0000           14
KRX:950110  SBI핀테크솔루션즈   20000.0000             1   20000.0000            1
KRX:950170         JTC   10000.0000             1   10000.0000            1
...
```

# GetFundamentalsConsensusChange

### Function specification

```
GetFundamentalsConsensusChange(field="operating_income", relative_to=1,
                                duration=6, forecast_target=0)
```

###

### Parameters

| Parameter        | Type    | Description                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| field            | string  | <p>조회 항목.  </p><p>revenue, revenue\_growth, operating\_income, ordinary\_profit, net\_income, eps, per, ebitda, ev\_ebitda, roe, pbr, bps, continuing\_profit, csd\_revenue, csd\_operating\_income, csd\_net\_income, csd\_continuing\_profit, csd\_eps, csd\_per, csd\_ebitda, csd\_ev\_ebitda, csd\_roe, csd\_pbr, csd\_bps</p> |
| relative\_to     | integer | 비교 대상 시기를 지정합니다. 예를 들어, 1을 입력하면, 1개월전이 기준 기간이 됩니다.                                                                                                                                                                                                                                                                                 |
| duration         | integer | 컨센서스 평균을 계산하는 기간을 지정합니다. 예를 들어, 6을 입력하면, 최근 6개월간의 평균 값을 이용합니다.                                                                                                                                                                                                                                                                     |
| forecast\_target | integer | 추정 년도. 예를 들어, 1을 입력하면 내년도 추정치를 조회합니다.                                                                                                                                                                                                                                                                                              |

### Examples

```
> GetFundamentalsConsensusChange(relative_to=3)                                                           
...
 entity_name  mean_before  count_before  mean_after  count_after
symbol                                                                    
KRX:000020        동화약품   1.1800e+07             1  1.1800e+07            1
KRX:000060       메리츠화재   4.1209e+08             7  3.7372e+08            9
KRX:000080       하이트진로   9.3700e+07             1  9.3700e+07            1
KRX:000100        유한양행   6.7480e+07             5  5.6367e+07            3
KRX:000370      한화손해보험   1.5046e+08             8  8.9950e+07            4
...
         
```
# GetStockSymbols

### Function specification

```
GetStockSymbols(entities=None)
```

### Parameters

| Parameter | Type                     | Description                       |
| --------- | ------------------------ | --------------------------------- |
| entities  | string or list of string | <p></p><p>종목코드 or 종목명 </p><p></p> |

### Examples

```
> GetStockSymbols(KRX:005930)

date symbol entity_name exchange market symbol_nice ceo business_rid company_rid           tel           fax              website email zipcode       address_land_lot   address_road_name company_type_l1 company_type_l2 company_type_size conglomerate_id     industry_id industry_name fs_type  fiscal_year_end             business_area date_founded date_listed  shares_outstanding
2020-06-30 KRX:005930        삼성전자      KRX  KOSPI  NICE:380725  김기남/김현석/고동진   1248100998  1301110006246  031-200-1114  031-200-1105  www.samsung.com/sec        443803  경기 수원시 영통구 매탄3동 416번지  경기 수원시 영통구 삼성로 129               1             511                 1             511  KRI:10C2642200     이동전화기 제조업      00               12  휴대폰,컴퓨터,네트워크시스템,핵심칩,반...   1969-01-13  1975-06-11          5969782550

```

# GetStockPrices

### Function specification

```
GetStockPrices(entities=None, columns=None, date_from=None, date_to=None)
```

### Parameters

| Parameter           | Type                     | Description                               |
| ------------------- | ------------------------ | ----------------------------------------- |
| entities            | string or list of string | 종목코드 or 종목명                               |
| columns             | string or list of string | 어떤 정보를 조회할것인지 지정. 별도 지정이 없으면 전체 항목에 대해 조회 |
| date\_from/date\_to | Date                     | 거래일. 별도 지정이 없으면 가장 최근의 거래일                |

### Examples

```
> GetStockPrices([삼성전자, NAVER], columns=["close"])
                     
date       symbol      entity_name   close                        
2020-06-30 KRX:005930        삼성전자   53700
           KRX:035420       NAVER  265000

```

# GetMarketIndexSymbols

### Function specification

```
GetMarketIndexSymbols(entities=None)
```

###

### Parameters

| Parameter | Type                     | Description                       |
| --------- | ------------------------ | --------------------------------- |
| entities  | string or list of string | <p></p><p>지수명 or 지수코드 </p><p></p> |

### Examples

```
> GetMarketIndexSymbols()

...
     entity_name exchange  market index_id  name_ko           name_en
date       symbol                                                                       
2020-06-30 KRX:KOSPI            코스피      KRX   KOSPI      001      코스피             KOSPI
           KRX:KOSPILC      코스피 대형주      KRX   KOSPI      002  코스피 대형주   KOSPI Large Cap
           KRX:KOSPIMC      코스피 중형주      KRX   KOSPI      003  코스피 중형주     KOSPI Mid Cap
           KRX:KOSPISC      코스피 소형주      KRX   KOSPI      004  코스피 소형주   KOSPI Small Cap
           KRX:KOSPI200     코스피 200      KRX   KOSPI      029  코스피 200         KOSPI 200
           KRX:KOSPI100     코스피 100      KRX   KOSPI      035  코스피 100         KOSPI 100
           KRX:KOSPI50       코스피 50      KRX   KOSPI      036   코스피 50          KOSPI 50
           KRX:KOSDAQ           코스닥      KRX  KOSDAQ      001      코스닥            KOSDAQ
           KRX:KOSDAQLC     코스닥 대형주      KRX  KOSDAQ      002  코스닥 대형주  KOSDAQ Large Cap
           KRX:KOSDAQMC     코스닥 중형주      KRX  KOSDAQ      003  코스닥 중형주    KOSDAQ Mid Cap
           KRX:KOSDAQSC     코스닥 소형주      KRX  KOSDAQ      004  코스닥 소형주  KOSDAQ Small Cap

```

# GetMarketIndexes

### Function specification

```
GetMarketIndexes(entities=None, columns=None, date_from=None, date_to=None)
```

### Parameters

| Parameter           | Type                     | Description                               |
| ------------------- | ------------------------ | ----------------------------------------- |
| entities            | string or list of string | 지수코드 or 지수명                               |
| columns             | string or list of string | 어떤 정보를 조회할것인지 지정. 별도 지정이 없으면 전체 항목에 대해 조회 |
| date\_from/date\_to | Date                     | 거래일. 별도 지정이 없으면 가장 최근의 거래일                |

###

### Examples

```
> GetMarketIndexes()

...
                        entity_name     open     high      low    close  volume    value  change  change_rate
date       symbol                                                                                            
2020-06-30 KRX:KOSDAQ           코스닥   744.54   744.54   737.44   740.07  372119  2602306    5.38         0.73
           KRX:KOSDAQLC     코스닥 대형주  1593.56  1593.56  1571.71  1579.73   31974   952933    6.83         0.43
           KRX:KOSDAQMC     코스닥 중형주   698.65   698.83   692.92   694.91   76411   686407    7.27         1.06
           KRX:KOSDAQSC     코스닥 소형주  2331.00  2333.23  2320.35  2326.87  229444   843180   20.41         0.88
           KRX:KOSPI            코스피  2124.38  2127.17  2116.12  2122.60  191813  2879690   29.12         1.39
           KRX:KOSPI100     코스피 100  2174.41  2178.79  2165.47  2173.24   25941  1656446   33.25         1.55
           KRX:KOSPI200     코스피 200   282.55   283.13   281.44   282.36   45593  2119226    4.32         1.55
           KRX:KOSPI50       코스피 50  1978.46  1981.71  1968.77  1976.52   18214  1500226   29.86         1.53
           KRX:KOSPILC      코스피 대형주  2109.68  2113.11  2100.48  2108.14   26229  1675703   30.61         1.47
           KRX:KOSPIMC      코스피 중형주  2113.36  2115.07  2107.39  2110.06   33328   589599   20.35         0.97
           KRX:KOSPISC      코스피 소형주  1726.50  1729.11  1721.92  1724.70  128118   468522   15.45         0.90

```


