# 인물

## 기업 임원 검색

```
FindPersonBio
FindPeopleByName
FindPeopleByBirthday
```

{% content-ref url="people/undefined" %}
[undefined](https://help.deepsearch.com/dp/api/func/people/undefined)
{% endcontent-ref %}

## 주식 부자 목록 추출

```
FindRichestShareholders
```

{% content-ref url="people/undefined-1" %}
[undefined-1](https://help.deepsearch.com/dp/api/func/people/undefined-1)
{% endcontent-ref %}

# 기업 임원 검색

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="undefined/findpersonbio" %}
[findpersonbio](https://help.deepsearch.com/dp/api/func/people/undefined/findpersonbio)
{% endcontent-ref %}

{% content-ref url="undefined/findpeoplebyname" %}
[findpeoplebyname](https://help.deepsearch.com/dp/api/func/people/undefined/findpeoplebyname)
{% endcontent-ref %}

{% content-ref url="undefined/findpeoplebybirthday" %}
[findpeoplebybirthday](https://help.deepsearch.com/dp/api/func/people/undefined/findpeoplebybirthday)
{% endcontent-ref %}

# FindPersonBio

### Function specification

```
FindPersonBio(name, birthday)
```

###

### Parameters

| Parameter | Type   | Description     |
| --------- | ------ | --------------- |
| name      | string | 이름              |
| birthday  | string | 생년일(YYYY-MM-DD) |

###

### Examples

```
> FindPersonBio("이재용", 1968-06-23)

...
symbol	date	entity_name	FindPersonBio(이재용, 1968-06-23)
NICE:380725	2012-12-31	삼성전자	부회장
NICE:380725	2013-03-31	삼성전자	부회장
NICE:380725	2013-06-30	삼성전자	부회장
NICE:380725	2013-09-30	삼성전자	부회장
NICE:380725	2013-12-31	삼성전자	부회장
NICE:380725	2014-03-31	삼성전자	부회장
NICE:380725	2014-06-30	삼성전자	부회장
NICE:380725	2014-09-30	삼성전자	부회장
NICE:380725	2014-12-31	삼성전자	부회장
NICE:380725	2015-03-31	삼성전자	부회장
NICE:380725	2015-06-30	삼성전자	부회장
NICE:380725	2015-09-30	삼성전자	부회장
...
```

# FindPeopleByName

### Function specification

```
FindPeopleByName(name)
```

###

### Parameters

| Parameter | Type   | Description |
| --------- | ------ | ----------- |
| name      | string | 이름          |

###

### Examples

```
> FindPeopleByName("이재용")

...
name	birthday	symbol	entity_name	last_date	position
이재용	1993-01-30	NICE:HG4121	코리아아트빌리티체임버사회적협동조합	2015-06-18	이사
이재용	1989-10-22	NICE:CC7342	우진	2015-01-20	감사
이재용	1987-07-04	NICE:046165	에이치엘비파워	2015-03-31	사외이사
이재용	1981-07-04	NICE:046165	에이치엘비파워	2013-06-30	사외이사
이재용	1986-08-14	NICE:192816	월산	2017-01-02	이사
이재용	1984-08-04	NICE:714712	화천윤활유	2019-05-16	대표이사
이재용	1984-06-21	NICE:M39878	메르티엘씨	2014-12-09	사장(대표)
이재용	1984-03-01	NICE:HO2726	스피드대구	2017-03-14	이사
이재용	1983-07-19	NICE:HC7395	아름다운정원	2015-04-23	사장(대표)
이재용	1980-03-20	NICE:FN8266	다원메탈	2015-03-30	이사
이재용	1979-11-30	NICE:CC3852	대림이앤아이	2015-01-12	사장(대표)
이재용	1978-07-30	NICE:M23507	지메디컨설팅	2014-10-08	이사
이재용	1970-01-01	NICE:L88996	삼도문화재연구원	2019-06-21	이사
이재용	1977-11-28	NICE:F34228	삼우다이캐스트	2014-07-26	생산관리
이재용	1977-07-23	NICE:HC8575	비누스엔터테인먼트	2015-04-28	사장(대표)
이재용	1970-01-01	NICE:341711	아이이	2018-09-30	사내이사
이재용	1977-03-29	NICE:G24591	한국교육리더십센터	2019-11-14	대표이사
이재용	1977-01-19	NICE:I26630	백제관광	2015-05-26	대표이사
...
```

# FindPeopleByBirthday

### Function specification

```
FindPeopleByBirthday(birth_month, birth_day)
```

###

### Parameters

| Parameter    | Type    | Description |
| ------------ | ------- | ----------- |
| birth\_month | integer | 월           |
| birth\_day   | integer | 일           |

###

### Examples

```
> FindPeopleByBirthday(3,15)

...
name	birthday	symbol	entity_name	last_date	position
후루타미치아키	1960-03-15	NICE:H82218	제이디아이코리아	2012-04-18	대표이사 사장
황희옥	1952-03-15	NICE:368980	우양테크	2005-06-10	감사
황철규	1956-03-15	NICE:777862	청우국제운송	2001-04-12	이사
황정근	1961-03-15	NICE:CC5870	통합정책연구원	2015-01-15	이사
황재활	1971-03-15	NICE:M14354	해피앤쿡	2014-08-25	사장(대표)
이선희	1969-03-15	NICE:M14354	해피앤쿡	2014-08-25	감사
황재연	1970-03-15	NICE:M40260	하나로이앤씨	2014-12-09	사장(대표)
황일홍	1976-03-15	NICE:034162	아라랏	2003-04-29	감사
황인호	1976-03-15	NICE:CC0475	나비투어여행사	2014-12-26	이사
황인수	1972-03-15	NICE:952079	성림첨단산업	2017-06-19	상무이사
황인선	1976-03-15	NICE:M09170	신영엔지니어링	2014-08-18	이사
황인석	1960-03-15	NICE:C64097	유빈스	2012-09-19	전무이사
황인갑	1961-03-15	NICE:C19776	중부엘리베이터	2011-04-29	대표이사 사장
황인갑	1960-03-15	NICE:C19776	중부엘리베이터	2016-08-16	대표이사
황익순	1952-03-15	NICE:M20346	농업회사법인희연	2014-09-25	이사
황완규	1959-03-15	NICE:235247	예성이엠씨	2004-05-04	이사
황영목	1952-03-15	NICE:M02350	금호전력	2014-08-04	사장(대표)
황승재	1965-03-15	NICE:HD2452	보스케넷	2015-05-11	사장(대표)
황설혜	1961-03-15	NICE:HC7298	태성기업	2015-04-23	이사
황선경	1947-03-15	NICE:HF9861	우성에이앤엘	2015-05-29	사장(대표)
황석렬	1960-03-15	NICE:149971	대현산업	2007-04-18	비상근 감사
...
```

# 주식 부자 목록 추출

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="undefined-1/findrichestshareholders" %}
[findrichestshareholders](https://help.deepsearch.com/dp/api/func/people/undefined-1/findrichestshareholders)
{% endcontent-ref %}

# FindRichestShareholders

### Function specification

```
FindRichestShareholders(count=500, date_from=None, date_to=None)
```

###

### Parameters

| Parameter          | Type    | Description                                                                 |
| ------------------ | ------- | --------------------------------------------------------------------------- |
| count              | integer | 최대 검색 결과 숫자                                                                 |
| dat\_from/date\_to | sting   | 검색할 주주목록의 기간을 지정합니다(YYYYMMDD). 기간이 주어지지 않았을 경우 과거 1년 동안 각 기업별 최근 데이터 사용합니다. |

###

### Examples

```
> FindRichestShareholders(count=500, date_from="2010-01-01", date_to="2010-12-31")

...
name	FindRichestShareholders(count=500, date_from=2010-01-01, date_to=2010-12-31)
국민연금공단	31,097,687,760,010.90
LG	19,165,277,617,741.70
삼성생명보험	15,547,957,182,910.40
SK	11,154,461,815,528.30
삼성전자	10,126,381,949,235.90
Citibank N.A	9,709,254,597,980.80
이건희	9,481,481,614,836.80
현대모비스	8,871,856,408,684.38
Bank of New York Mellon	8,186,285,810,756.00
한국정책금융공사	7,643,732,823,383.34
삼성물산	7,139,434,833,537.06
현대자동차	7,109,277,180,110.51
기획재정부	7,029,553,722,975.00
...
```


