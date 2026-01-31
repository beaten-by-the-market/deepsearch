# DocumentSearch

### Function specification

```
DocumentSearch(category, section, query, count=10, page=None,
                date_from=None, date_to=None, use_score=False, summary=True,
                clustering=False, clustering_category=None, sample_size=None,
                uniquify=True, highlight=False, fields=None, format=None)
```

###

### Parameters

| Parameter            | Type                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category             | string or list of string | <p>국내뉴스 : news</p><p>증권사 보고서: research</p><p>공시,IR : company</p><p>특허 : patent</p><p></p>                                                                                                                                                                                                                                                                                                                                                                                                             |
| section              | string or list of string | <p>Category가 news 일 경우 </p><p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p><p></p><p>Category가 research일 경우 </p><p>시장 전망: market </p><p>투자전략: strategy </p><p>기업 보고서: company </p><p>산업 보고서: industry </p><p>경제 보고서: economy </p><p>채권 보고서: bond </p><p></p><p>Category 가 company 인 경우 </p><p>IR : ir </p><p>공시 : disclosure </p><p></p><p>Category 가 patent 인 경우 </p><p>특허 : patent</p> |
| query                | string                   | 검색 쿼리                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| count                | integer                  | 한 페이지에 표시할 문서의 최대 개수                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| page                 | integer                  | 페이지 번호                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| date\_from           | string                   | 검색 시작 시점 (YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| date\_to             | string                   | 검색 종료 시점(YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| use\_score           | boolean                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| summary              | boolean                  | 1: 문서 요약, 0: 문서 요약하지 않음 (기본값: 1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| clustering           | boolean                  | 1: 문서 클러스터링 사용, 0: 문서 클러스터링 사용 안 함 (기본값: 0)                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| clustering\_category | boolean                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| sample\_size         | integer                  | <p>클러스터링 시 사용할 샘플 문서 개수 (기본값: 30)</p><ul><li>count option을 10으로 설정하고 sample\_size를 50으로 지정하면 50개의 문서를 10개의 클러스터로 분류한다는 의미이다.</li></ul>                                                                                                                                                                                                                                                                                                                                                                |
| uniquify             | boolean                  | <p>1 : 중복 문서를 제거, 0: 중복 문서 제거 안함. (기본값: 1)</p><ul><li>기준 : content\_url이 동일한 뉴스의 경우, 동일한 뉴스로 판단하고 제외</li></ul>                                                                                                                                                                                                                                                                                                                                                                                        |
| highlight            | boolean                  | 1: 하이라이트 사용, 0: 하이라이트 사용 안 함 (기본값: 0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| fields               | list of string           | <p>결과값으로 어떤 항목을 노출한 것인지 지정한다.</p><p>예를 들어, fields=title, content\_url 로 설정하면, 결과 내역에서 제목 및 원문링크값을 리턴한다.</p>                                                                                                                                                                                                                                                                                                                                                                                           |
| format               |                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

### Result Layout

{% content-ref url="../../../result\_layout/result-documentsearchresult" %}
[result-documentsearchresult](https://help.deepsearch.com/dp/api/result_layout/result-documentsearchresult)
{% endcontent-ref %}

### 검색 쿼리 예시 - 국내 뉴스

```
경제 뉴스 검색
> DocumentSearch(["news"],["economy"],"딥서치")

...
meta: {
score: null,
version: 1
},
uid: 894663826614653200,
uid_str: "894663826614653135",
category: "news",
section: "economy",
publisher: "매일경제",
author: "김경택",
title: "딥서치-카이스트, 여의도 금융대학원 운영 기관 선정",
content: "AI 기술기반 금융 빅데이터분석 기업 빅데이터 분석 역량 적극 공유 서울시와 금융위원회는 올해 9월 개관을 앞두고 있는 여의도 금융대학원의 운영기관에 'KAIST 디지털금융 교육그룹'을 선정했다고 26일 밝혔다. 한국과학기술원(KAIST) 디지털금융 교육그룹은 KAIST 경영대학이 주관하고, AI 기술기반 금융 빅데이터분석 기업인 딥서치(DeepSearch) 등으로 구성된 컨소시엄이다. 금융 빅데이터 분석 전문 기업 딥서치는 빅데이터 및 AI 기술을 기반으로 금융·기업의 주요 의사결정을 자동화하고 있는 빅데이터 스타트업이다.",
highlight: null,
securities: [
{
type: "company",
exchange: "KRX",
market: "KOSPI",
symbol: "005940",
name: "NH투자증권",
company_rid: "110111-0098130",
business_rid: "116-81-03693"
}
],
entities: [
{
type: "company",
name: "NH투자증권"
}
],
tags: [ ],
industry: {
label: "P85",
name: "교육 서비스업",
score: 0.712
},
polarity: {
label: "0",
name: "중립",
score: 0.767
},
content_url: "http://news.mk.co.kr/newsRead.php?no=314410&year=2020",
image_urls: [ ],
attachments: [ ],
attributes: {
query_name: "딥서치",
query_string: ""딥서치""
},
created_at: "2020-03-26T13:55:00.000000",
updated_at: "2020-03-26T13:55:00.000000"
...

```

### 검색 쿼리 예시 - 공시

```
삼성전자 공시문서 검색
>>> DocumentSearch(["company"],["disclosure"],"securities.name:삼성전자")

공시문서 중 제목이 사업보고서인 공시문서만 검색
>>> DocumentSearch(["company"],["disclosure"],"title:사업보고서")

공시문서 중 제목이 사업보고서인 공시문서에 내용이 (2차전지 혹은 이차전지)가 있는 문서검색
>>> DocumentSearch(["company"],["disclosure"],"title:사업보고서 and content:(2차전지 or 이차전지)")

공시문서 중 제목이 임원ㆍ주요주주특정증권등소유상황보고서 이면서, 내용에 장내매수라는 단어가 있는 문서 검색
>>> DocumentSearch(["company"],["disclosure"],"title:임원ㆍ주요주주특정증권등소유상황보고서 and content:장내매수")
```

### 검색 쿼리 예시 - 특허

```
삼성전자 보유 특허 검색
>>> DocumentSearch(["patent"],[""],"securities.name:삼성전자")

반도체 관련 특허 검색
>>> DocumentSearch(["patent"],[""],"반도체")
```

### 검색 쿼리 예시 - Clustering 사용하기

특정 키워드 및 검색식으로 뉴스를 검색하고, 그 뉴스로 딥서치 clustering 알고리즘을 이용해서 문서를 군집화할 수 있습니다.

```
한국은행 키워드의 뉴스를 군집화
>>> DocumentSearch("news","economy","한국은행",clustering=true)

한국은행 키워드의 뉴스를 30개로 군집화
>>> DocumentSearch("news","economy","한국은행",clustering=true,count=30)

한국은행 키워드의 뉴스 50개 문서를 30개로 군집화
>>> DocumentSearch("news","economy","한국은행",clustering=true,count=30, sample_size=50)
```

# 문서 심화검색

## Field Names <a href="#field-names" id="field-names"></a>

입력한 쿼리의 검색 대상은 기본적으로 문서의 제목과 본문이지만, 다음과 같이 특정한 필드를 지정하는 것도 가능합니다. 딥서치의 문서데이터 구조는 아래와 같습니다.&#x20;

{% content-ref url="../../../../result\_layout/result-documentsearchresult" %}
[result-documentsearchresult](https://help.deepsearch.com/dp/api/result_layout/result-documentsearchresult)
{% endcontent-ref %}

| 항목         | 내용     | type        | 비고                                                                                                                                                                                                                                                                                                           |
| ---------- | ------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| publisher  | 출처     | string      |                                                                                                                                                                                                                                                                                                              |
| author     | 작성자    | string      |                                                                                                                                                                                                                                                                                                              |
| title      | 제목     | string      |                                                                                                                                                                                                                                                                                                              |
| content    | 내용     | string      | 문서 요약 정보                                                                                                                                                                                                                                                                                                     |
| securities | 관련 종목  | array       | 다수개의 관련 종목(json object) 를 array 로 리턴                                                                                                                                                                                                                                                                         |
| entities   | 관련 엔티티 | array       | 다수개의 관련 엔티티(json object) 를 array 로 리턴                                                                                                                                                                                                                                                                        |
| tags       | 태그 정보  | array       | 문서에 따라 필요한 부가 정보                                                                                                                                                                                                                                                                                             |
| industry   | 산업 정보  | json object | label:산업 코드, name:산업명, score:신뢰점수                                                                                                                                                                                                                                                                            |
| polarity   | 긍부정 정보 | json object | label:긍부정점수(0,1,-1), name:긍부정여부,score:신뢰점수                                                                                                                                                                                                                                                                   |
| esg        | esg 정보 | json object | <p>category: ESG 분류 정보(json object)</p><ul><li>label: 환경(E), 사회(S), 지배구조(G), 해당없음(U)에 대한 코드값</li><li>name: ESG 명칭</li><li>score: 신뢰점수(0.0~~1.0)</li></ul><p>polarity: ESG에 따른 긍부정 정보(json object)</p><ul><li>label: 부정(-1), 중립(0), 긍정(1)에 대한 코드값</li><li>name: 극성 명칭</li><li>score: 신뢰점수(0.0~~1.0)</li></ul> |

**제목(Title)에서 \`삼성전자\`를 검색하는 경우**

```
title:삼성전자

// 경제섹션 뉴스제목이 삼성전자인 문서를 찾는 명령어

DocumentSearch(["news"],["economy"],"title:삼성전자")
```

**제목(Title)에서 \`삼성전자\` 혹은 \`구글\`을 검색하는 경우**

```
title:(삼성전자 or 구글)

// 경제섹션 뉴스제목에 삼성전자 혹은 구글이 들어간 문서를 찾는 명령어

DocumentSearch(["news"],["economy"],"title:(삼성전자 or 구글)")
```

**언론사(Publisher) 이름으로 검색하는 경우**

```
publisher:한겨레

// 경제섹션 뉴스 언론사이름이 한겨레인 문서를 찾는 명령어

DocumentSearch(["news"],["economy"],"publisher:한겨레")
```

**관련종목(Securities)으로 검색하는 경우**

연관종목 : 상장기업명이 해당 문서에 포함되어 있으면서, 특정 상장 기업에 대한 뉴스인 것으로 판단할 때에만 맵핑됩니다.

참고 ) 관련종목은 상장기업만 맵핑됩니다.

```
securities.name:삼성전자
securities.symbol:005930 // 삼성전자 종목코드

// 활용예시

DocumentSearch(["news"],["economy"],"securities.name:삼성전자") 
DocumentSearch(["news"],["economy"],"securities.symbol:005930")
DocumentTrends(["news"],["economy"],"securities.name:대한항공") // 대한항공으로 맵핑된 뉴스수의 추이
```

**관련 회사(Named\_entities)으로 검색하는 경우**

언급 내용 : 해당 문서의 본문에서 언급하고 있는 기업, 조직, 브랜드 등이 문서데이터에 맵핑됩니다.

1. 기업(Company) : 모든 문서데이터에 맵핑되어 있으며, securities와 달리 비상장기업까지 맵핑되어 있습니다.
2. 사람(Person) : 뉴스데이터에만 맵핑되어있습니다.
3. 브랜드(Brand) : 뉴스데이터에만 맵핑되어있습니다.&#x20;
4. 사업자 등록번호(Business\_rid)
5. 법인 등록번호(Company\_rid)

```
named_entities.entities.company.name:삼성전자
named_entities.entities.person.name:이재용
named_entities.entities.brand.name:갤럭시S21
named_entities.entities.company.business_rid:'124-81-00998'

// 예시

DocumentSearch(["news"],["economy"],"named_entities.entities.brand.name:갤럭시S2")  // 갤럭시21 브랜드와 관련된 경제뉴스 검색
DocumentSearch(["news"],["economy"],"named_entities.entities.person.name:이재용")  // 이재용 인물과 관련된 경제뉴스 검색
DocumentSearch(["news"],["economy"],"named_entities.entities.company.business_rid:'124-81-00998'")  // 삼성전자 사업자 등록번호로 검색
DocumentSearch(["news"],["economy"],"named_entities.entities.company.business_rid:('124-81-00998' or '107-86-14075')")  // 삼성전자 포함 두 개의 사업자 등록번호로 검색
DocumentSearch(["news"],["economy"],"named_entities.entities.person.name:한종희" and "named_entities.entities.company.name:'삼성전자'") // 대표명과 회사명으로 검색

// 기타
DocumentAggregation(["news"],["economy"],"named_entities.entities.company.name:삼성전자", "named_entities.entities.brand.name:100")  // 삼성전자를 언급한 경제뉴스상에서 brand명을 언급한 횟수

```

**극성(polarity)기준으로 검색하는 경우**

만약 특정 뉴스가 securities가 맵핑되어 있는 경우, 긍부정 판단을 위한 분석을 시행합니다. 따라서, 삼성전자와 긍정적인 뉴스를 검색하는 등의 작업을 할 수 있습니다.

```
named_entities.entities.brand.name:갤럭시S21

// 예시

DocumentSearch(["news"],["economy"],"named_entities.entities.brand.name:갤럭시S2")  // 갤럭시21 브랜드와 관련된 경제뉴스 검색
DocumentSearch(["news"],["economy"],"named_entities.entities.person.name:이재용")  // 이재용 인물과 관련된 경제뉴스 검색

polarity.name:긍정
polarity.name:부정
polarity.name:중립

polarity.label:'1' // 긍정 - 1을 숫자로 인식하지 않기 위해서 ''를 붙여야함.
polarity.label:'-1' // 부정
polarity.label:'0' // 중립

// 예시

DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and polarity.name:긍정")
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and polarity.label:'1'")

DocumentTrends(["news"],["economy"],"securities.name:삼성전자 and polarity.name:긍정")

```

**ESG 기준으로 검색하는 경우**

만약 특정 뉴스가 securities가 맵핑되어 있는 경우, ESG 판단을 위한 분석을 시행합니다. 따라서, 삼성전자의 ESG와 관련된 뉴스를 검색하는 등의 작업을 할 수 있습니다.

```
// ESG 검색 조건 예시

esg.category.name:환경
esg.category.name:사회
esg.category.name:지배구조

esg.category.label:E
esg.category.label:S
esg.category.label:G

esg.polarity.name:긍정
esg.polarity.name:부정
esg.polarity.name:중립

esg.polarity.label:'1' // 긍정 - 1을 숫자로 인식하지 않기 위해서 ''를 붙여야함.
esg.polarity.label:'-1' // 부정
esg.polarity.label:'0' // 중립

// 예시

DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.category.name:환경")
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.category.label:E")
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.polarity.name:긍정")
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.polarity.label:'1'")

DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.category.name:환경 and esg.polarity.name:긍정")
DocumentSearch(["news"],["economy"],"securities.name:삼성전자 and esg.category.label:E and esg.polarity.name:긍정")
```

## Proximity Searches <a href="#proximity-searches" id="proximity-searches"></a>

`"`로 묶인 문장 쿼리의 경우 나열된 두 개 이상의 단어가 정확히 같은 순서로 일치하는 문서만 검색 결과에 나타납니다. 이와 달리 Proximity Query를 사용하면 쿼리에 나열된 단어가 지정한 범위 내에서 일치하는 경우에도 검색 결과에 나타납니다.&#x20;

```
"삼성전자 아이폰"~5
"반도체 공장 사고"~15
"침수 사고"~15


// DocumentSearch를 이용한 Proximity Searches 사례
// "를 입력하기 위하여 앞에 \( 백슬래시 )를 앞에 넣어주어야 합니다.

DocumentSearch("news","economy","\"삼성전자 아이폰\"~15")
DocumentSearch("news","economy","\"반도체 공장 사고\"~15")
DocumentSearch("news","economy","\"침수 사고\"~15")
```

이 경우 \`삼성전자\`와 \`아이폰\`이란 단어가 문서 내에서 5단어 이내의 거리에서 함께 나타날 경우 입력 쿼리와 일치한다고 판단하게 됩니다. 아래 예시는 Proximity Searches 기능으로 검색할 수 있는 문장의 예시입니다.:

```
소장에는 삼성전자가 아이폰의 둥근 모서리와 베젤 디자인 특허를 침해했다는 내용이 담겼다.

삼성전자는 항소심에서 아이폰 특허 중 일부가 무효판정을 받으면서 삼성의 손해배상액은 5억4817만6477달러로 줄어들었다.
```

## Boolean Operators <a href="#boolean-operators" id="boolean-operators"></a>

기본적으로 모든 단어는 **AND 연산으로 처리되므로 쿼리에 나열된 모든 단어가 일치하는 문서가 검색 결과에 나타나게 됩니다.** 하지만 딥서치는 보다 정교한 검색을 위해서 AND, OR, NOT 등의 기본적인 boolean 연산자와 쿼리 그룹핑 기능을 제공합니다.

예를 들어 삼성전자 관련 뉴스 중에서도 갤럭시 혹은 아이폰에 관련된 뉴스만을 검색하고자 하면 다음과 같은 쿼리를 사용하면 됩니다:

```
삼성전자 and (갤럭시 or 아이폰)
```

연산자를 명시하지 않은 모든 단어들은 기본적으로 AND로 처리되므로 상기 쿼리는 다음과 같이 재작성할 수 있습니다:

```
삼성전자 (갤럭시 or 아이폰)
```

이렇게 검색된 뉴스들 중에 애플 관련 소송 뉴스를 제외하고자 한다면 다음과 같이 쿼리를 개선할 수 있습니다:

```
삼성전자 (갤럭시 or 아이폰) !소송
```

상기 쿼리 그대로 제목만을 대상으로 검색하고자 하는 경우는 다음과 같이 쿼리를 재작성할 수 있습니다:

```
title:(삼성전자 (갤럭시 or 아이폰) !소송)
```

제목에서 \`소송\`이 언급된 경우만을 제외하고자 한다면 다음과 같이 쿼리를 재작성할 수 있습니다:

```
삼성전자 (갤럭시 or 아이폰) !title:소송
```

## 날짜 + 시간단위로 문서를 조회하는 방법 <a href="#named-search-query" id="named-search-query"></a>

정식으로 지원하는 date\_*from, date\_to 파라미터는 연월일만 조회할 수 있을 뿐, 시간단위로는 조회할 수 없는 단점이있습니다. 아래 기능을 이용하시면, 연월일 뿐만아니라 시간까지 넣어서 조회할 수 있습니다.*

```
// date_from, date_to를 사용하지않고, created_at을 사용합니다.

DocumentSearch(["news"], [], "삼성전자 and created_at:[\"2022-07-12T00:00:00\" to \"2022-07-12T09:00:00\"]", page=1, count=10, highlight=True)
```

# DocumentTrends

### Function specification

```
DocumentTrends(category, section, query,
                interval="1d", date_from=None, date_to=None,
                fields=None, format=None)
```

###

### Parameters

| Parameter  | Type                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category   | string or list of string | <p></p><p>국내뉴스:news</p><p>증권사 보고서: research</p><p>공시,IR : company</p><p>특허 : patent</p><p></p>                                                                                                                                                                                                                                                                                                                                                                                                       |
| section    | string or list of string | <p>Category가 news일 경우 </p><p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p><p></p><p>Category가 research일 경우 </p><p>시장 전망: market </p><p>투자전략: strategy </p><p>기업 보고서: company </p><p>산업 보고서: industry </p><p>경제 보고서: economy </p><p>채권 보고서: bond </p><p></p><p>Category 가 company 인 경우 </p><p>IR : ir </p><p>공시 : disclosure </p><p></p><p>Category 가 patent 인 경우 </p><p>특허 : patent</p> |
| query      | string                   | 검색 쿼리                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| interval   | string                   | <p></p><ul><li><p>트렌드 계산 단위</p><ul><li>1y: 1년 단위</li><li>1M: 1개월 단위</li><li>1w: 1주일 단위</li><li>1d: 1일 단위</li><li>1h : 1시간 단위</li><li>1m : 1분 단위</li></ul></li></ul>                                                                                                                                                                                                                                                                                                                                  |
| date\_from | string                   | 검색 시작 시점 (YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| date\_to   | string                   | 검색 종료 시점(YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fields     | list of string           | 결과값으로 어떤 항목을 노출한 것인지 지정한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

### Result Layout

{% content-ref url="../../../result\_layout/result-documenttrendsresult" %}
[result-documenttrendsresult](https://help.deepsearch.com/dp/api/result_layout/result-documenttrendsresult)
{% endcontent-ref %}

### Examples

```
핀테크 트렌드 검색
> DocumentTrends(["news"],[""],"핀테크")

...
query: {
query_name: "핀테크",
query_string: ""핀테크""
},
total_matches: 105447,
buckets: [
{
key: "1990-01-17",
value: 0,
count: 0,
frequencies: [ ]
},
{
key: "1990-01-18",
value: 0,
count: 0,
frequencies: [ ]
},
{
key: "1990-01-19",
value: 0,
count: 0,
frequencies: [ ]
},
{
key: "1990-01-20",
value: 0,
count: 0,
frequencies: [ ]
},
...


> DocumentTrends(["world-news"],[""],"TESLA")

```

### 활용예시

#### DocumentTrends 를 이용한 특정 주제에 대한 긍부정 점수 계산

긍부정 점수 = ( 긍정 뉴스 개수 - 부정 뉴스 개수 ) / ( 긍정 뉴스 개수 + 중립 뉴스 개수 + 부정 뉴스 개수 )

* 긍정 뉴스 개수 : api.deepsearch.com/v1/compute?input=DocumentTrends(\["news"],\[""],"키워드%20polarity.label:'1'",interval="1M",date\_from=2019-01-01)
* 부정 뉴스 개수: api.deepsearch.com/v1/compute?input=DocumentTrends(\["news"],\[""],"키워드%20polarity.label:'-1'",interval="1M",date\_from=2019-01-01)
* 중립 뉴스 개수: api.deepsearch.com/v1/compute?input=DocumentTrends(\["news"],\[""],"키워드%20polarity.label:'0'",interval="1M",date\_from=2019-01-01)

```
예시 ) 삼성전자

긍정 점수 :
api.deepsearch.com/v1/compute?input=DocumentTrends(["news"],[""],"삼성전자%20polarity.label:1",interval="1M",date_from=2019-01-01)

key: "2019-01-01",
value: 0.189542,
count: 1475,

부정 점수 :
api.deepsearch.com/v1/compute?input=DocumentTrends(["news"],[""],"삼성전자%20polarity.label:-1",interval="1M",date_from=2019-01-01)

key: "2019-01-01",
value: 44.386932,
count: 345416,

중립 점수 :
api.deepsearch.com/v1/compute?input=DocumentTrends(["news"],[""],"삼성전자%20polarity.label:0",interval="1M",date_from=2019-01-01)

key: "2019-01-01",
value: 0.230534,
count: 1794,


2019년 1월 긍부정 점수
(1475-345416)/(1475+345416+1794) = -0.98

```

# DocumentAggregation

### Function specification

```
DocumentAggregation(category, section, query, groupby, 
date_from=None, date_to=None, min_count=0)
```

###

### Parameters

| Parameter  | Type                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category   | string or list of string | <p>국내뉴스:news</p><p>증권사 보고서: research</p><p>공시,IR : company</p><p>특허 : patent</p>                                                                                                                                                                                                                                                                                                                                                                                                                     |
| section    | string or list of string | <p>Category가 news일 경우 </p><p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p><p></p><p>Category가 research일 경우 </p><p>시장 전망: market </p><p>투자전략: strategy </p><p>기업 보고서: company </p><p>산업 보고서: industry </p><p>경제 보고서: economy </p><p>채권 보고서: bond </p><p></p><p>Category 가 company 인 경우 </p><p>IR : ir </p><p>공시 : disclosure </p><p></p><p>Category 가 patent 인 경우 </p><p>특허 : patent</p> |
| query      | string                   | 검색 쿼리                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| groupby    | string                   | 어떤 조건으로 집계할 것인지 여부. 개별 문서의 결과 항목들을 기준으로 집계가 가능하다. 예를 들어, named\_entities.entities.company.symbol:100 로 지정하면, 문서를 named\_entities 의 심볼을 기준으로 최대 100개까지 집계한다는 의미이다.                                                                                                                                                                                                                                                                                                                                    |
| date\_from | string                   | 검색 시작 시점 (YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| date\_to   | string                   | 검색 종료 시점(YYYYMMDD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| min\_count | int                      | 최소 결과 개수 ( 기본값 : 0 )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

### Result Layout

{% content-ref url="../../../result\_layout/result-dataframe" %}
[result-dataframe](https://help.deepsearch.com/dp/api/result_layout/result-dataframe)
{% endcontent-ref %}

### 활용 예시

#### DocumentAggregation 을 이용한 특정 주제와 관련된 기업 리스트 추출

* DocumentAggregation("news", None, "키워드", "named\_entities.entities.company.name:100", date\_from=2020-01-01)

```
예시 ) 코로나
뉴스 문서를 기반으로, 코로나가 언급된 기업 리스트를 100 추출

> DocumentAggregation("news", None, "코로나", "named_entities.entities.company.name:100", date_from=2020-01-01)

...
key	count
더불어민주당	57,206
페이스북코리아	28,729
연합뉴스	27,555
삼성전자	25,733
현대자동차	24,515
한국은행	16,667
네이버	15,271
LG전자	13,823
대한항공	12,623
디지털타임스	10,461
한국방송공사	10,315
케이티	9,590
SBS	9,248
롯데쇼핑	9,136
기아자동차	9,036
SK	8,812
롯데지주	8,506
이데일리	8,306
애플코리아	8,047
...


```

#### DocumentAggregation 을 이용한 ESG 이슈가 발생한 기업 리스트 추출

* DocumentAggregation("news", "economy", "ESG검색조건", "securities.name:100", date\_from=2020-01-01)

```
예시 ) ESG 활용 1
뉴스 문서를 기반으로, 환경(E) & 긍정(1)으로 분류 기업 리스트를 100 추출

> DocumentAggregation(”news”,“economy”,"esg.category.name:환경 and esg.polarity.name:긍정","securities.name:100",date_from=2020-01-01)

...
key	count
POSCO	115
SK	106
롯데케미칼	90
SK이노베이션	70
현대제철	61
삼성전자	60
현대차	56
LG화학	52
대한항공	36
한국조선해양	35
한국전력	34
한화솔루션	32
DB	29
GS건설	28
두산중공업	28
풀무원	28
LG전자	27
SK케미칼	25
한국가스공사	25
...

예시 ) ESG 활용 2
뉴스 문서를 기반으로, 사회(S) & 부정(-1)으로 분류 기업 리스트를 100 추출


> DocumentAggregation(”news”,“economy”,"esg.category.label:S and esg.polarity.name:부정","securities.name:100",date_from=2020-01-01)

...
key	count
CJ대한통운	284
HDC현대산업개발	117
삼성전자	73
한국전력	53
SK	51
HDC	43
POSCO	37
삼성생명	36
현대차	31
CJ	26
NAVER	24
한화솔루션	24
일동제약	23
대한항공	22
현대중공업	21
KT	17
DB	16
오스템임플란트	15
SK텔레콤	14
...

```

#### DocumentAggregation 을 이용한 특정 주제에 대한 워드 클라우드 표시&#x20;

* DocumentAggregation("topic-news",%20None,%20"키워드",groupby="keywords.keyword:100",%20date\_from=2010-01-01)

```
예시) 삼성전자
토픽 문서를 기반으로, 삼성전자와 관련된 키워드 100개 추출

> DocumentAggregation("topic-news",%20None,%20"삼성전자",groupby="keywords.keyword:100",%20date_from=2010-01-01)

결과 : 
key: [
"삼성전자",
"출시",
"스마트폰",
"공개",
"확대",
"1위",
"글로벌",
"올해",
"가능",
"국내",
"애플",
"강화",
"LG전자",
"세계",
"미국",
"제품",
"시장",
"시작",
"본격",
"코스피",
"최고",
"최대",
"예상",
"전망",
"돌파",
"외국인",
"규모",
"반도체",
..
]
```

# GetSentimentScore

### Parameters

| Parameter  | Type   | Description                                                                                                                                                         |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| query      | string | 검색 쿼리                                                                                                                                                               |
| interval   | string | <p></p><ul><li><p>트렌드 계산 단위</p><ul><li>1y: 1년 단위</li><li>1M: 1개월 단위</li><li>1w: 1주일 단위</li><li>1d: 1일 단위</li><li>1h : 1시간 단위</li><li>1m : 1분 단위</li></ul></li></ul> |
| date\_from | string | 검색 시작 시점 (YYYYMMDD)                                                                                                                                                 |
| date\_to   | string | 검색 종료 시점(YYYYMMDD)                                                                                                                                                  |

### Result Layout

{% content-ref url="../../../result\_layout/result-documenttrendsresult" %}
[result-documenttrendsresult](https://help.deepsearch.com/dp/api/result_layout/result-documenttrendsresult)
{% endcontent-ref %}

### Examples

```
삼성전자의 2021년 1월 1일 ~ 현재까지의 1일 기준 긍부정점수조회
> GetSentimentScore("삼성전자", interval="1d", date_from=2021-01-01)


```

# SearchTrendingTopics

### Function specification

호출 시점에서 가장 최신의 이슈를 제공합니다.

```
SearchTrendingTopics(category, section, fields=None)
```

### Parameters

| Parameter | Type                     | Description                                                                                                                                                   |
| --------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category  | string or list of string | <p></p><p>국내뉴스: news</p><p></p>                                                                                                                               |
| section   | string or list of string | <p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p> |
| fields    | list of string           | 결과값으로 어떤 항목을 노출한 것인지 지정한다.                                                                                                                                    |

### Result Layout&#x20;

{% content-ref url="../../../result\_layout/result-trendingtopicssearchresult" %}
[result-trendingtopicssearchresult](https://help.deepsearch.com/dp/api/result_layout/result-trendingtopicssearchresult)
{% endcontent-ref %}

### Examples

```
트렌딩 토픽 검색
> SearchTrendingTopics(["news"],["economy"])
{
    "found": true,
    "data": {
        "timestamp": "2020-08-07T16:20:00.000000",
        "topics": {
            "news": {
                "economy": [
                    {
                        "uid": 54469154,
                        "uid_str": "54469154",
                        "category": "news",
                        "section": "economy",
                        "rank": 1,
                        "score": 7.7828,
                        "topic": "국내증시 연고점 재경신 코스피 2350선 마감",
                        "keywords": [
                            {
                                "keyword": "2350선",
                                "freq": 16
                            },
                            {
                                "keyword": "1만1000선",
                                "freq": 10
                            },
...
                            {
                                "keyword": "0.68%↑",
                                "freq": 1
                            }
                        ],
                        "statistics": {
                            "doc_count": 70,
                            "securities": [
                                {
                                    "exchange": "KRX",
                                    "market": "KOSPI",
                                    "symbol": "051910",
                                    "name": "LG화학",
                                    "company_rid": "110111-2207995",
                                    "business_rid": "107-81-98139",
                                    "doc_count": 2
                                },
                                {
                                    "exchange": "KRX",
                                    "market": "KOSPI",
                                    "symbol": "039490",
                                    "name": "키움증권",
                                    "company_rid": "110111-1867948",
                                    "business_rid": "107-81-76756",
                                    "doc_count": 1
                                },
                                {
                                    "exchange": "KRX",
                                    "market": "KOSDAQ",
                                    "symbol": "267790",
                                    "name": "배럴",
                                    "company_rid": "110111-4256924",
                                    "business_rid": "105-87-39951",
                                    "doc_count": 1
                                }
                            ],
                            "industries": [
                                {
                                    "label": "B06",
                                    "name": "금속 광업",
                                    "min": 0.837,
                                    "max": 1.0,
                                    "mean": 0.97664,
                                    "stddev": 0.04943,
                                    "doc_count": 11
                                },
                                {
                                    "label": "C14",
                                    "name": "의복, 의복 액세서리 및 모피제품 제조업",
                                    "min": 0.528,
                                    "max": 0.835,
                                    "mean": 0.6815,
                                    "stddev": 0.1535,
                                    "doc_count": 2
                                },
...
                                {
                                    "label": "C24",
                                    "name": "1차 금속 제조업",
                                    "min": 0.336,
                                    "max": 0.336,
                                    "mean": 0.336,
                                    "stddev": 0.0,
                                    "doc_count": 1
                                }
                            ],
                            "polarities": [
                                {
                                    "label": "0",
                                    "name": "중립",
                                    "min": 0.985,
                                    "max": 0.99,
                                    "mean": 0.9875,
                                    "stddev": 0.0025,
                                    "doc_count": 2
                                },
                                {
                                    "label": "1",
                                    "name": "긍정",
                                    "min": 0.756,
                                    "max": 0.89,
                                    "mean": 0.823,
                                    "stddev": 0.067,
                                    "doc_count": 2
                                }
                            ]
                        }


...

```# GetTrendingTopic

### Function specification

```
GetTrendingTopic(
                category, section, topic_uid,
                count=10, summary=True,
                highlight_query=None,
                fields=None
)
```

### Parameters

| Parameter        | Type                     | Description                                                                                                                                                   |
| ---------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category         | string or list of string | 국내뉴스: news                                                                                                                                                    |
| section          | string or list of string | <p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p> |
| topic\_uid       | integer                  | 토픽의 ID                                                                                                                                                        |
| count            | integer                  | 결과로 나타나는 docs의 문서 수                                                                                                                                           |
| summary          | bool                     | 연관 뉴스 content 를 요약할 것인지 설정                                                                                                                                    |
| highlight\_query | string                   | 검색 결과에 하이라이트 할 키워드를 지정                                                                                                                                        |
| fields           | list of string           | 결과값으로 어떤 항목을 노출한 것인지 지정한다.                                                                                                                                    |

### Result Layout&#x20;

{% content-ref url="../../../result\_layout/result-trendingtopicresult" %}
[result-trendingtopicresult](https://help.deepsearch.com/dp/api/result_layout/result-trendingtopicresult)
{% endcontent-ref %}

### Examples

```
트랜딩 토픽 문서 결과
> GetTrendingTopic(["news"],["economy"],54469154)
{
    "found": true,
    "data": {
        "scroll_id": null,
        "current_page": 0,
        "last_page": 0,
        "topics": {
            "news": {
                "economy": [
                    {
                        "uid": 54469154,
                        "uid_str": "54469154",
                        "timestamp": "2020-08-07T16:20:00.000000",
                        "category": "news",
                        "section": "economy",
                        "rank": 1,
                        "score": 7.7828,
                        "topic": "국내증시 연고점 재경신 코스피 2350선 마감",
                        "keywords": [
                            {
                                "keyword": "2350선",
                                "freq": 16
                            },
                            {
                                "keyword": "1만1000선",
                                "freq": 10
                            },
                            {
                                "keyword": "뉴욕증시",
                                "freq": 9
                            },
                            {
                                "keyword": "2360선",
                                "freq": 6
                            },
                            {
                                "keyword": "1만1000돌파",
                                "freq": 5
                            }
                        ],
                        "doc_uids": [
                            942897253075521663,
                            942897253075521670,
...
                            943258339578614137
                        ],
                        "docs": [
                            {
                                "meta": {
                                    "score": 0.0,
                                    "version": 1
                                },
                                "uid": 943258339578614137,
                                "uid_str": "943258339578614137",
                                "revision": 1,
                                "category": "news",
                                "section": "economy",
                                "publisher": "파이낸셜뉴스",
                                "author": "김서연",
                                "title": "[fn마감시황] 코스피, 2350선 돌파.. 나흘 연속 연고점 경신",
                                "content": "7일 코스피는 전거래일 대비 9.06포인트(0.39%) 오른 2351.67로 장을 마쳤다.\n\n이날 코스피는 전거래일 대비 전거래일 대비 6.64포인트(0.28%)오른 2349.25로 개장했다.\n\n지난 4일 이후 4거래일 연속 장중 고가 기준 연고점을 갈아치웠다.",
                                "highlight": null,
                                "securities": [],
                                "entities": [
                                    {
                                        "type": "company",
                                        "name": "LG화학"
                                    },
                                    {
                                        "type": "company",
                                        "name": "NAVER"
                                    },
                                    {
                                        "type": "company",
                                        "name": "SK하이닉스"
                                    },
                                    {
                                        "type": "company",
                                        "name": "삼성SDI"
                                    },
                                    {
                                        "type": "company",
                                        "name": "삼성전자"
                                    },
                                    {
                                        "type": "company",
                                        "name": "셀트리온"
                                    }
                                ],
                                "named_entities": [],
                                "tags": [],
                                "industry": {
                                    "label": "100",
                                    "name": "분류 제외, 기타",
                                    "score": 0.978
                                },
                                "polarity": null,
                                "customized_ml": null,
                                "patent": null,
                                "content_url": "http://www.fnnews.com/news/202008071613437663",
                                "image_urls": [],
                                "attachments": [],
                                "attributes": {},
                                "created_at": "2020-08-07T16:15:00.000000",
                                "updated_at": "2020-08-07T16:15:00.000000"
                            }
                        ],
                        "statistics": {
                            "doc_count": 70,
                            "securities": [
                                {
                                    "type": "company",
                                    "exchange": "KRX",
                                    "market": "KOSPI",
                                    "symbol": "051910",
                                    "name": "LG화학",
                                    "company_rid": "110111-2207995",
                                    "business_rid": "107-81-98139",
                                    "doc_count": 2
                                },
                                {
                                    "type": "company",
                                    "exchange": "KRX",
                                    "market": "KOSPI",
                                    "symbol": "039490",
                                    "name": "키움증권",
                                    "company_rid": "110111-1867948",
                                    "business_rid": "107-81-76756",
                                    "doc_count": 1
                                },
                                {
                                    "type": "company",
                                    "exchange": "KRX",
                                    "market": "KOSDAQ",
                                    "symbol": "267790",
                                    "name": "배럴",
                                    "company_rid": "110111-4256924",
                                    "business_rid": "105-87-39951",
                                    "doc_count": 1
                                }
                            ],
                            "industries": [
                                {
                                    "label": "B06",
                                    "name": "금속 광업",
                                    "min": 0.837,
                                    "max": 1.0,
                                    "mean": 0.97664,
                                    "stddev": 0.04943,
                                    "doc_count": 11
                                },
                                {
                                    "label": "C14",
                                    "name": "의복, 의복 액세서리 및 모피제품 제조업",
                                    "min": 0.528,
                                    "max": 0.835,
                                    "mean": 0.6815,
                                    "stddev": 0.1535,
                                    "doc_count": 2
                                },
...
                                {
                                    "label": "C24",
                                    "name": "1차 금속 제조업",
                                    "min": 0.336,
                                    "max": 0.336,
                                    "mean": 0.336,
                                    "stddev": 0.0,
                                    "doc_count": 1
                                }
                            ],
                            "polarities": [
                                {
                                    "label": "0",
                                    "name": "중립",
                                    "min": 0.985,
                                    "max": 0.99,
                                    "mean": 0.9875,
                                    "stddev": 0.0025,
                                    "doc_count": 2
                                },
                                {
                                    "label": "1",
                                    "name": "긍정",
                                    "min": 0.756,
                                    "max": 0.89,
                                    "mean": 0.823,
                                    "stddev": 0.067,
                                    "doc_count": 2
                                }
                            ]
                        }
...

```

# SearchHistoricalTopics

### Function specification

```
SearchHistoricalTopics(
                category, section, query,
                count=10, page=None, sort=None,
                date_from=None, date_to=None,
                fields=None
)
```

### Parameters

| Parameter  | Type                     | Description                                                                                                                                                   |
| ---------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category   | string or list of string | 국내뉴스: news                                                                                                                                                    |
| section    | string or list of string | <p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p> |
| query      | string                   | 검색 쿼리                                                                                                                                                         |
| count      | integer                  | 한 페이지에 표시할 문서의 최대 개수                                                                                                                                          |
| page       | integer                  | 페이지 번호                                                                                                                                                        |
| sort       | string                   | <p></p><ul><li>검색시 정렬의 기준이 되는 필드</li><li>필드명 앞에 "-" 를 붙이면 내림차순으로 정렬됨</li><li>여러 필드를 지정 할 수 있으며, 나열된 순서대로 정렬</li></ul>                                         |
| date\_from | string                   | 검색 시작 시점 (YYYYMMDD)                                                                                                                                           |
| date\_to   | string                   | 검색 종료 시점(YYYYMMDD)                                                                                                                                            |
| fields     | list of string           | 결과값으로 어떤 항목을 노출한 것인지 지정한다.                                                                                                                                    |

### Result Layout&#x20;

{% content-ref url="../../../result\_layout/result-historicaltopicssearchresult" %}
[result-historicaltopicssearchresult](https://help.deepsearch.com/dp/api/result_layout/result-historicaltopicssearchresult)
{% endcontent-ref %}

### Examples

```
핀테크 과거 토픽 검색
> SearchHistoricalTopics(["news"],["economy"],"핀테크",date_from="20200101", date_to="20201231")
{
...
        "total_matches": 1474,
        "max_score": null,
        "scroll_id": "2",
        "current_page": 1,
        "last_page": 100,
        "topics": [
            {
                "meta": {
                    "score": null,
                    "version": 3
                },
                "uid": 942667530709897216,
                "uid_str": "942667530709897216",
                "revision": 1,
                "date": "2020-08-05",
                "category": "news",
                "section": "economy",
                "rank": 5,
                "score": 0.63194,
                "topic": "파죽지세 카카오뱅크 상반기 순익 372%↑",
                "tags": [],
                "keywords": [
                    {
                        "keyword": "카카카오뱅크",
                        "freq": 30
                    },
                    {
                        "keyword": "268억원",
                        "freq": 12
                    },
                    {
                        "keyword": "아파트담보대출",
                        "freq": 8
                    },
                    {
                        "keyword": "순이익453억",
                        "freq": 8
                    },
...
                    {
                        "keyword": "IPO본격화",
                        "freq": 1
                    }
                ],
                "securities": [
                    {
                        "type": "company",
                        "exchange": "KRX",
                        "market": "KOSPI",
                        "symbol": "005940",
                        "name": "NH투자증권",
                        "company_rid": "110111-0098130",
                        "business_rid": "116-81-03693",
                        "freq": 19
                    },
                    {
                        "type": "company",
                        "exchange": "KRX",
                        "market": "KOSPI",
                        "symbol": "030200",
                        "name": "KT",
                        "company_rid": "110111-1468754",
                        "business_rid": "102-81-42945",
                        "freq": 4
                    },
                    {
                        "type": "company",
                        "exchange": "KRX",
                        "market": "KOSDAQ",
                        "symbol": "035720",
                        "name": "카카오",
                        "company_rid": null,
                        "business_rid": null,
                        "freq": 1
                    },
                    {
                        "type": "company",
                        "exchange": "KRX",
                        "market": "KOSPI",
                        "symbol": "039490",
                        "name": "키움증권",
                        "company_rid": "110111-1867948",
                        "business_rid": "107-81-76756",
                        "freq": 1
                    }
                ],
                "entities": [
                    {
                        "type": "company",
                        "name": "KT",
                        "freq": 10
                    },
                    {
                        "type": "company",
                        "name": "NAVER",
                        "freq": 1
                    },
                    {
                        "type": "company",
                        "name": "NH투자증권",
                        "freq": 21
                    },
                    {
                        "type": "company",
                        "name": "세틀뱅크",
                        "freq": 4
                    },
                    {
                        "type": "company",
                        "name": "카카오",
                        "freq": 2
                    },
                    {
                        "type": "company",
                        "name": "키움증권",
                        "freq": 1
                    }
                ],
                "attributes": {
                    "query_name": "핀테크",
                    "query_string": "\"핀테크\""
                }
            },

```

# GetHistoricalTopic

### Function specification

```
GetHistoricalTopic(
                category, section, topic_uid,
                sorts=None, count=10,
                summary=True,
                highlight_query=None,
                fields=None
)
```

### Parameters

| Parameter        | Type                     | Description                                                                                                                                                   |
| ---------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| category         | string or list of string | 국내뉴스: news                                                                                                                                                    |
| section          | string or list of string | <p>정치: politics </p><p>경제: economy </p><p>사회: society </p><p>문화: culture </p><p>세계: world </p><p>기술/IT: tech </p><p>연예: entertainment </p><p>사설: opinion </p> |
| topic\_uid       | integer                  | 토픽의 ID                                                                                                                                                        |
| sorts            | string                   | <p></p><ul><li>검색시 정렬의 기준이 되는 필드</li><li>필드명 앞에 "-" 를 붙이면 내림차순으로 정렬됨</li><li>여러 필드를 지정 할 수 있으며, 나열된 순서대로 정렬</li></ul>                                         |
| count            | integer                  | 한 페이지에 표시할 문서의 최대 개수                                                                                                                                          |
| summary          | bool                     | 연관 뉴스 content 를 요약할 것인지 설정                                                                                                                                    |
| highlight\_query | string                   | 검색 결과에 하이라이트 할 키워드를 지정                                                                                                                                        |
| fields           | list of string           | 결과값으로 어떤 항목을 노출한 것인지 지정한다.                                                                                                                                    |

### Result Layout

{% content-ref url="../../../result\_layout/result-historicaltopicssearchresult-1" %}
[result-historicaltopicssearchresult-1](https://help.deepsearch.com/dp/api/result_layout/result-historicaltopicssearchresult-1)
{% endcontent-ref %}

### Examples

```
핀테크 과거 토픽 문서 결과 
> GetHistoricalTopic(["news"],["economy"],942667530709897216)
{
    "found": true,
    "data": {
        "topics": {
            "news": {
                "economy": [
                    {
                        "meta": {
                            "score": 0.0,
                            "version": 1
                        },
                        "uid": 942667530709897216,
                        "uid_str": "942667530709897216",
                        "revision": 1,
                        "date": "2020-08-05",
                        "category": "news",
                        "section": "economy",
                        "rank": 5,
                        "score": 0.63194,
                        "topic": "파죽지세 카카오뱅크 상반기 순익 372%↑",
                        "tags": [],
                        "keywords": [
                            {
                                "keyword": "카카카오뱅크",
                                "freq": 30
                            },
                            {
                                "keyword": "268억원",
                                "freq": 12
                            },
                            {
                                "keyword": "아파트담보대출",
                                "freq": 8
                            },
                            
...
                            
                            {
                                "keyword": "IPO본격화",
                                "freq": 1
                            }
                        ],
                        "securities": [
                            {
                                "type": "company",
                                "exchange": "KRX",
                                "market": "KOSPI",
                                "symbol": "005940",
                                "name": "NH투자증권",
                                "company_rid": "110111-0098130",
                                "business_rid": "116-81-03693",
                                "freq": 19
                            },
                            {
                                "type": "company",
                                "exchange": "KRX",
                                "market": "KOSPI",
                                "symbol": "030200",
                                "name": "KT",
                                "company_rid": "110111-1468754",
                                "business_rid": "102-81-42945",
                                "freq": 4
                            },
                            {
                                "type": "company",
                                "exchange": "KRX",
                                "market": "KOSDAQ",
                                "symbol": "035720",
                                "name": "카카오",
                                "company_rid": null,
                                "business_rid": null,
                                "freq": 1
                            },
                            {
                                "type": "company",
                                "exchange": "KRX",
                                "market": "KOSPI",
                                "symbol": "039490",
                                "name": "키움증권",
                                "company_rid": "110111-1867948",
                                "business_rid": "107-81-76756",
                                "freq": 1
                            }
                        ],
                        "entities": [
                            {
                                "type": "company",
                                "name": "KT",
                                "freq": 10
                            },
                            {
                                "type": "company",
                                "name": "NAVER",
                                "freq": 1
                            },
                            {
                                "type": "company",
                                "name": "NH투자증권",
                                "freq": 21
                            },
                            {
                                "type": "company",
                                "name": "세틀뱅크",
                                "freq": 4
                            },
                            {
                                "type": "company",
                                "name": "카카오",
                                "freq": 2
                            },
                            {
                                "type": "company",
                                "name": "키움증권",
                                "freq": 1
                            }
                        ],
                        "attributes": {},
                        "docs": [
                            {
                                "meta": {
                                    "score": 0.0,
                                    "version": 1
                                },
                                "uid": 942289009080668208,
                                "uid_str": "942289009080668208",
                                "revision": 1,
                                "category": "news",
                                "section": "economy",
                                "publisher": "중앙일보",
                                "author": "성지원",
                                "title": "K뱅크 비대면 아파트담보대출…금리는 1.64%",
                                "content": "서류심사·대출까지 이틀만에 끝 KT 대리점서 계좌도 쉽게 개설 케이뱅크가 이달 중 ‘100% 비대면 아파트 담보대출’을 출시한다.\n\n또 이번 주부터 KT 대리점에서 QR코드를 이용해 바로 케이뱅크 계좌를 개설할 수 있는 제휴 서비스를 출시한다고 4일 밝혔다.\n\n이 행장은 “전국 2500개 KT 대리점에서 QR코드를 찍으면 쉽게 케이뱅크 계좌를 만들 수 있을 예정”이라며 “계좌를 개설하고 휴대폰을 개통하면 통신비 할인 혜택을 주는 ‘통신결합 상품’을 준비 중”이라고 밝혔다.",
                                "highlight": null,
                                "securities": [],
                                "entities": [
                                    {
                                        "type": "company",
                                        "name": "KT"
                                    },
                                    {
                                        "type": "company",
                                        "name": "NH투자증권"
                                    }
                                ],
                                "named_entities": [
                                    {
                                        "type": "organization",
                                        "name": "K뱅크",
                                        "count": 1
                                    }
                                ],
                                "tags": [],
                                "industry": {
                                    "label": "K64",
                                    "name": "금융업",
                                    "score": 0.865
                                },
                                "polarity": null,
                                "customized_ml": null,
                                "patent": null,
                                "content_url": "https://news.joins.com/article/olink/23435830",
                                "image_urls": [
                                    "https://haystack-attachments.s3-ap-northeast-1.amazonaws.com/news/economy/2020/08/05/942289009080668208/000-c9bca87400723df6c490383e8443e7c5b038828a.jpg"
                                ],
                                "attachments": [],
                                "attributes": {},
                                "created_at": "2020-08-05T00:03:00.000000",
                                "updated_at": "2020-08-05T00:03:00.000000"
                            },


...

```

# SimilarKeywords

### Function specification

```
SimilarKeywords(positive_keyword,
                negative_keyword,
                max_count = 30,
                min_score = 0.5,
                date_from = None,
                date_to = None)
```

SimilarKeywords는 [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)를 이용하여 입력된 쿼리와 유사한 키워드를 검색합니다.

각각의 단어는 분산 표현(Distributed Representation)을 통해 유사한 단어는 인접하도록 특정 공간에 사상됩니다. 특정 공간에 사상된 단어는 백터 연산을 통해 아래의 그림과 같이 새로운 단어를 유추할 수 있습니다.&#x20;

![T. Mikolov, W. T. Yih, and G. Zweig, NAACL HLT 2013](https://2002947409-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-LPJrnQiLiz9bWVBvx6Q%2F-M3nav6YNIgHV4BlcoGt%2F-M3oL8ZFVQxDavGVVFRH%2Fimage.png?alt=media\&token=170eb00d-f169-446f-acca-933a0bf5298b)

위의 오른쪽 그림의 예시는 `SimilarKeywords(positive_keyword="KINGS QUEEN", negative_keyword="KING")`와 같은 연산을 통해 `QUEENS`를 얻을 수 있습니다. 그러나 이는 이상적인 경우이며 대부분의 경우 `positive_keyword`의 토큰이 하나일 때 가장 좋은 결과를 출력합니다.

Word2Vec 모델은 연도별로  발생한 뉴스 데이터를 기반으로 각각 학습되었으며 `date_from`/`date_to`를 통해 개별 연도의 유사 키워드를 검색할 수 있습니다.

### Parameters

| Parameter           | Type    | Description                    | Required |
| ------------------- | ------- | ------------------------------ | -------- |
| positive\_keyword   | string  | 검색 쿼리, 공백을 통해 하나 이상의 토큰을 표현    | True     |
| negative\_keyword   | string  | 제외 검색 쿼리, 공백을 통해 하나 이상의 토큰을 표현 |          |
| max\_count          | integer | 최대 검색 결과 개수                    |          |
| min\_score          | float   | 최소 코사인 유사도 점수                  |          |
| date\_from/date\_to | string  | 검색 기간(YYYY)                    |          |

### Result Layout

{% content-ref url="../../../result\_layout/result-dataframe" %}
[result-dataframe](https://help.deepsearch.com/dp/api/result_layout/result-dataframe)
{% endcontent-ref %}

### Examples

```
> SimilarKeywords("자율주행", date_from="2015")

...

           keyword   score
year index                
2015 0       자율주행차  0.8541
     1       무인자동차  0.7629
     2       전기자동차  0.7410
     3         무인차  0.7386
     4         초소형  0.7284
...            ...     ...
2019 25        IoT  0.6457
     26        기술인  0.6448
     27         AR  0.6441
     28     수소연료전지  0.6437
     29        미래형  0.6435
```

```
> SimilarKeywords("자율주행 LG전자", "삼성전자", max_count=10)

...

           keyword   score
year index                
2019 0       자율주행차  0.6678
     1         지능형  0.6578
     2        모빌리티  0.6448
     3        스마트홈  0.6416
     4          로봇  0.6344
     5         융복합  0.6338
     6          상용  0.6329
     7         신기술  0.6245
     8          실증  0.6166
     9       커넥티드카  0.6121
```
