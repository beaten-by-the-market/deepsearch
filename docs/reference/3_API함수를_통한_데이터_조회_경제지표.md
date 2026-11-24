<!-- 이 파일은 docs/reference/sync_from_gitbook.py로 생성합니다 (2026-11-25). 원문: https://help.deepsearch.com/dp/ — 한국은행·FRED·IMF·OECD·World Bank·통계청·딥서치 자체 경제지표. 직접 고치지 말고, 레포 메모는 repo-memo 마커 안에 쓰세요. -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy -->
# 경제 지표

## 경제 지표 검색

```
FindEntity
```

{% content-ref url="/pages/-MGqeVAjqyFFyewYYtud" %}
[경제 지표 검색](https://help.deepsearch.com/dp/api/func/economy/economy-search.md)
{% endcontent-ref %}

## 한국은행 데이터 조회

```
QueryBankOfKoreaSeriesInfo
QueryBankOfKoreaSeriesInfoSimple
QueryBankOfKoreaSeriesData
QueryBankOfKoreaSeriesDataSimple
```

{% content-ref url="/pages/-MGqeYq32ZBo0-Y3pPTp" %}
[한국은행 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/bok.md)
{% endcontent-ref %}

## 미연방은행 데이터 (FRED) 조회

```
QueryFredSeriesInfo
QueryFredSeriesData
GetFredCategoryOfDataSeries
GetFredDataSeriesListUnderCategory
```

{% content-ref url="/pages/-MGqeaLNte1SuSt5t6W\_" %}
[미연방은행 (FRED) 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/fred.md)
{% endcontent-ref %}

## IMF 데이터 조회

```
GetImfSeriesInfo
GetImfSeriesValues
GetImfDataflowAnnotations
GetImfCountryListOfSameIndicator
GetImfIndicatorListOfSameCountry
```

{% content-ref url="/pages/-MWMSYSDn4cjHGp72SAO" %}
[IMF 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/imf.md)
{% endcontent-ref %}

## OECD 데이터 조회

```
GetOecdSeriesInfo
GetOecdSeriesValues
GetOecdDatasetAnnotations
GetOecdRelatedIndicatorList
```

{% content-ref url="/pages/-MWMSv0\_uNdXmt6iPh20" %}
[OECD 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/oecd.md)
{% endcontent-ref %}

## World Bank 데이터 조회

```
QueryWorldBankSeriesInfo
QueryWorldBankSeriesData
GetWorldBankCountryListOfIndicator
GetWorldBankIndicatorListOfSameSource
```

{% content-ref url="/pages/-MRcfbPhM9F9tIAaBKGb" %}
[World Bank 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/world-bank.md)
{% endcontent-ref %}

## 통계청 데이터 조회

```
QueryKosisTableInfo
GetKosisAvailableSampleDates
GetKosisTableCategoryItemFreqList
QueryKosisCrossSectionData
QueryKosisTimeSeriesData
```

{% content-ref url="/pages/-MRcfhuPOG5mf7EP65sg" %}
[통계청 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/kostat.md)
{% endcontent-ref %}

## 딥서치 자체 수집 데이터 조회

```
QueryDeepSearchOwnSeriesInfo
QueryDeepSearchOwnSeriesValues
QueryDeepSearchOwnDataSeriesListOfSameCategory
```

{% content-ref url="/pages/-MRcflHSIs3TDk1CyGtM" %}
[딥서치 자체 수집 데이터 조회](https://help.deepsearch.com/dp/api/func/economy/deepsearch.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/economy-search -->
# 경제 지표 검색

아래 함수를 사용하여 경제 지표를 이름으로 검색할 수 있습니다.

{% content-ref url="/pages/-MGqfZxji5ivHp105XyJ" %}
[FindEntity](https://help.deepsearch.com/dp/api/func/economy/economy-search/findentity.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/economy-search/findentity -->
# FindEntity

기업 검색에 사용되는 FindEntity 를 경제 지표 검색에도 활용할 수 있습니다.

### Function specification

```
FindEntity(entity_type, pattern, count=0, fields=None,
    score_type=None, include_matched_fields=False)
```

###

### Parameters

| Parameter                | Type                                  | Description                                                                                                                                                                                                                                                                   |
| ------------------------ | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| entity\_type             | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 경제 지표 검색을 위해선 "DataSeries" 를 파라미터로 넘겨주어야 합니다.                                                                                                                                                                                                   |
| pattern                  | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 여러 단어를 입력할 때는 중간에 공백을 넣으면 됩니다.                                                                                                                                                                                                                           |
| count                    | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.                                                                                                                                                                                                                               |
| fields                   | list of string                        | 경제 지표는 지표 이름과 symbol 만을 검색 대상으로 이용합니다. 따로 지정되지 않을 경우, 기본 값은 \["symbol", "name\_ko", "name\_en"] 입니다.                                                                                                                                                                          |
| score\_type              | string                                | <p>중요도를 계산하는 스코어 방식을 선택할 수 있습니다. 따로 지정하지 않을 경우 경제 지표 이름 전체 길이에서 패턴과 매치된 부분의 상대적인 비율을 사용합니다. "tf-idf" 라는 파라미터를 주면 tf-idf 방식에 의해서 스코어를 계산합니다.</p><p></p><p>위 두 가지 방법 중 하나로 스코어를 계산하고 나면, 여기에 각 경제 지표의 인기도 (popularity) 와 조합하여 보정 한 후 최종 스코어를 계산합니다. 스코어가 높은 지표를 우선해서 보여줍니다.</p> |
| include\_matched\_fields | boolean                               | 매치된 필드를 결과값에 별도 컬럼으로 포함시킵니다.                                                                                                                                                                                                                                                  |

###

### Examples

```
> FindEntity("DataSeries", "unemployment urban")

...

                            entity_type                   matched   score
symbol              field
FRED:UNRATE         name_en        FRED         Unemployment Rate  0.8067
FRED:UNRATENSA      name_en        FRED         Unemployment Rate  0.7059
FRED:LNU03000000    name_en        FRED        Unemployment Level  1.3333
FRED:UNEMPLOY       name_en        FRED        Unemployment Level  0.6667
FRED:LNS14000001    name_en        FRED   Unemployment Rate - Men  0.5217
...                                 ...                       ...     ...
FRED:SLUEM1524ZSARE name_en        FRED  Youth Unemployment Ra...  0.2308
FRED:SLUEM1524ZSSYR name_en        FRED  Youth Unemployment Ra...  0.2308
FRED:TNCCLAIMS      name_en        FRED  Continued Claims (Ins...  0.2308
FRED:VABEDF5URN     name_en        FRED  Unemployment Rate in ...  0.2308
FRED:WICCLAIMS      name_en        FRED  Continued Claims (Ins...  0.2308
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/bok -->
# 한국은행 데이터 조회

한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 prefix 로 시작합니다.

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MGqhDSjCpdsfdX7yLWs" %}
[QueryBankOfKoreaSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRccX8JGGv71RpiMAvh" %}
[QueryBankOfKoreaSeriesInfoSimple](https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesinfosimple.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MGqhFYBWj3zOI9qmNpn" %}
[QueryBankOfKoreaSeriesData](https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesdata.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcd1HkSLtzpVF9jK5w" %}
[QueryBankOfKoreaSeriesDataSimple](https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesdatasimple.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesinfo -->
# QueryBankOfKoreaSeriesInfo

선택된 한국은행 경제 지표의 상세 정보를 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryBankOfKoreaSeriesInfo(entity_ids=None, stat_codes=None, item_codes=None)
```

###

### Parameters

한국은행 경제지표의 entity\_id 는 "BOK:\<stat\_code>.\<item\_code>" 의 형식으로 되어있습니다. 따라서 전체 entity\_id 를 명시하거나, 또는 stat\_code / item\_code 만을 명시해도 해당 조건에 만족하는 전체 경제지표의 상세 정보를 출력하도록 만들었습니다.

| Parameter   | Type                                  | Description                                        |
| ----------- | ------------------------------------- | -------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | (예) "BOK:060Y001.010101000" 또는 "060Y001.010101000" |
| stat\_codes | <p>string or</p><p>list of string</p> | (예) "060Y001"                                      |
| item\_codes | <p>string or</p><p>list of string</p> | (예) \["010101000", "010150000"]                    |

###

### Examples

```
> QueryBankOfKoreaSeriesInfo("060Y001.010101000")

...

                               p_item_code group_name   item_name_ko              item_name_en cycle start_time  end_time  data_count        last_updated    stat_name_ko              stat_name_en
stat_code group_code item_code
060Y001   Group1     010101000   010100000       항목선택  콜금리(1일, 전체거래)  Call Rate (Overnight-...    DD   19950103  20200903        6565 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
```

```
QueryBankOfKoreaSeriesInfo(stat_codes=["060Y001"])

...

                               p_item_code group_name     item_name_ko              item_name_en cycle start_time  end_time  data_count        last_updated    stat_name_ko              stat_name_en
stat_code group_code item_code
060Y001   Group1     010101000   010100000       항목선택    콜금리(1일, 전체거래)  Call Rate (Overnight-...    DD   19950103  20200903        6565 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010102000   010100000       항목선택  콜금리(1일, 중개회사거래)  Call Rate (Overnight-...    DD   19950103  20200903        6269 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010150000                   항목선택     KORIBOR(3개월)           KORIBOR(3MONTH)    DD   19950103  20200903        3749 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010151000                   항목선택     KORIBOR(6개월)           KORIBOR(6MONTH)    DD   19950103  20200903        3621 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010152000                   항목선택    KORIBOR(12개월)          KORIBOR(12MONTH)    DD   19950103  20200903        4004 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010190000                   항목선택          국고채(1년)   Treasury Bonds (1-year)    DD   19950103  20200903        5106 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010200000                   항목선택          국고채(3년)   Treasury Bonds (3-year)    DD   19950103  20200903        5416 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010200001                   항목선택          국고채(5년)   Treasury Bonds (5-year)    DD   19950103  20200903        5127 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010210000                   항목선택         국고채(10년)  Treasury Bonds (10-year)    DD   19950103  20200903        4891 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010220000                   항목선택         국고채(20년)  Treasury Bonds (20-year)    DD   19950103  20200903        3625 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010230000                   항목선택         국고채(30년)  Treasury Bonds (30-year)    DD   19950103  20200903        1970 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010260000                   항목선택          산금채(1년)  Yields of Financial D...    DD   19950103  20200903        4206 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010300000                   항목선택      회사채(3년,AA-)  Corporate Bonds (3-ye...    DD   19950103  20200903        6566 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010310000                   항목선택  회사채(AA-, 민평)수익률     Corporate Bonds (AA-)    DD   19950103  20200903        4485 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010320000                   항목선택    회사채(3년)(BBB-)  Corporate Bonds (3-ye...    DD   19950103  20200903        5043 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010400000                   항목선택         통안증권(1년)             MSBs (1-year)    DD   19950103  20200903        6527 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010400001                   항목선택        통안증권(91일)             MSBs (91-day)    DD   19950103  20200903        3460 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010400002                   항목선택         통안증권(2년)             MSBs (2-year)    DD   19950103  20200903        5526 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010501000                   항목선택          MMF(7일)               MMF (7-day)    DD   19950103  20200903        5877 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010502000                   항목선택          CD(91일)               CD (91-day)    DD   19950103  20200903        6566 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010503000                   항목선택          CP(91일)               CP (91-day)    DD   19950103  20200903        6566 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010503500                   항목선택     국민주택채권1종(5년)  Yields of National Ho...    DD   19950103  20200903        4206 2020-09-03 17:41:28  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
                     010504000                   항목선택         CMA(수시형)              CMA(open RP)    DD   19950103  20200903        6442 2020-09-03 17:41:29  4.1.1 시장금리(일별)  4.1.1 Principal Finan...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesinfosimple -->
# QueryBankOfKoreaSeriesInfoSimple

선택된 한국은행 경제 지표의 상세 정보를 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 prefix 로 시작합니다. Redis cache 를 사용하여 데이터 조회 속도가 한층 빠릅니다.

### Function specification

```
QueryBankOfKoreaSeriesInfoSimple(entity_ids)
```

###

### Parameters

한국은행 경제지표의 entity\_id 는 "BOK:\<stat\_code>.\<item\_code>" 의 형식으로 되어있습니다. 이전 QueryBankOfKoreaSeriesInfo 함수와는 다르게 stat\_code / item\_code 을 입력으로 받을 수 없고 오직 entity\_ids 만을 파라미터로 명시할 수 있지만, 대신 redis cache 를 사용해서 데이터 조회 속도가 한층 빠릅니다.

| Parameter   | Type                                  | Description                 |
| ----------- | ------------------------------------- | --------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | (예) "BOK:060Y001.010101000" |

###

### Examples

```
> QueryBankOfKoreaSeriesInfoSimple("BOK:060Y001.010101000")

...

                                           name start_time  end_time cycle  data_count unit
entity_id
BOK:060Y001.010101000  시장금리(일별) - 콜금리(1일, 전체거래)   19950103  20210121    DD        6659   연%
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesdata -->
# QueryBankOfKoreaSeriesData

선택된 한국은행 경제 지표의 데이터 값을 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryBankOfKoreaSeriesData(entity_ids=None, stat_codes=None, item_codes=None,
                                date_from=None, date_to=None, last_only=False)
```

###

### Parameters

한국은행 경제지표의 entity\_id 는 "\<stat\_code>.\<item\_code>" 의 형식으로 되어있습니다. 따라서 전체 entity\_id 를 명시하거나, 또는 stat\_code / item\_code 만을 명시해도 해당 조건에 만족하는 전체 경제지표의 상세 정보를 출력하도록 만들었습니다.

| Parameter   | Type                                  | Description                                                                   |
| ----------- | ------------------------------------- | ----------------------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | (예) "BOK:060Y001.010101000" 또는 "060Y001.010101000"                            |
| stat\_codes | <p>string or</p><p>list of string</p> | (예) "060Y001"                                                                 |
| item\_codes | <p>string or</p><p>list of string</p> | (예) \["010101000", "010150000"]                                               |
| date\_from  | date                                  | <p>데이터 조회 기간의 시작 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p>  |
| date\_to    | date                                  | <p>데이터 조회 기간의 마지막 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p> |
| last\_only  | boolean                               | last\_only = True 로 주어질 경우 가장 최근 값만을 리턴합니다.                                   |

### Examples

```
> QueryBankOfKoreaSeriesData("060Y001.010101000")

...

                                  QueryBankOfKoreaSeriesData(060Y001.010101000)
entity_id             date
BOK:060Y001.010101000 1995-01-03                    0.1306
                      1995-01-04                    0.1163
                      1995-01-05                    0.1061
                      1995-01-06                    0.0928
                      1995-01-07                    0.1078
...                                                    ...
                      2020-08-27                    0.0050
                      2020-08-28                    0.0049
                      2020-08-31                    0.0055
                      2020-09-01                    0.0052
                      2020-09-02                    0.0049
```

```
> QueryBankOfKoreaSeriesData(stat_codes=["060Y001"], last_only=True)

...

                                  QueryBankOfKoreaSeriesData(stat_codes=[060Y001], last_only=True)
entity_id             date
BOK:060Y001.010101000 2020-09-02                    0.0049
BOK:060Y001.010102000 2020-09-02                    0.0049
BOK:060Y001.010150000 2020-09-02                    0.0062
BOK:060Y001.010151000 2020-09-02                    0.0072
BOK:060Y001.010152000 2020-09-02                    0.0088
BOK:060Y001.010190000 2020-09-02                    0.0072
BOK:060Y001.010200000 2020-09-03                    0.0092
BOK:060Y001.010200001 2020-09-03                    0.0122
BOK:060Y001.010210000 2020-09-02                    0.0154
BOK:060Y001.010220000 2020-09-02                    0.0170
BOK:060Y001.010230000 2020-09-02                    0.0169
BOK:060Y001.010260000 2020-09-02                    0.0083
BOK:060Y001.010300000 2020-09-03                    0.0226
BOK:060Y001.010310000 2020-09-02                    0.0151
BOK:060Y001.010320000 2020-09-02                    0.0861
BOK:060Y001.010400000 2020-09-03                    0.0070
BOK:060Y001.010400001 2020-09-02                    0.0065
BOK:060Y001.010400002 2020-09-02                    0.0084
BOK:060Y001.010501000 2020-09-02                    0.0068
BOK:060Y001.010502000 2020-09-03                    0.0063
BOK:060Y001.010503000 2020-09-03                    0.0130
BOK:060Y001.010503500 2020-09-02                    0.0136
BOK:060Y001.010504000 2020-09-02                    0.0024
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/bok/querybankofkoreaseriesdatasimple -->
# QueryBankOfKoreaSeriesDataSimple

선택된 한국은행 경제 지표의 데이터 값을 조회합니다. 한국은행에서 수집한 경제 지표의 symbol 은 "BOK:" 라는 prefix 로 시작합니다. Redis cache 를 사용하여 데이터 조회 속도가 한층 빠릅니다.

### Function specification

```
QueryBankOfKoreaSeriesDataSimple(entity_ids, date_from=None, date_to=None)
```

### Parameters

한국은행 경제지표의 entity\_id 는 "BOK:\<stat\_code>.\<item\_code>" 의 형식으로 되어있습니다. 이전 QueryBankOfKoreaSeriesData 함수와는 다르게 stat\_code / item\_code 을 입력으로 받을 수 없고 오직 entity\_ids 만을 파라미터로 명시할 수 있지만, 대신 redis cache 를 사용해서 데이터 조회 속도가 한층 빠릅니다.

| Parameter   | Type                                  | Description                                                                   |
| ----------- | ------------------------------------- | ----------------------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | (예) "BOK:060Y001.010101000"                                                   |
| date\_from  | date                                  | <p>데이터 조회 기간의 시작 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p>  |
| date\_to    | date                                  | <p>데이터 조회 기간의 마지막 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p> |

###

### Examples

```
> QueryBankOfKoreaSeriesDataSimple("BOK:060Y001.010101000")

...

                                  QueryBankOfKoreaSeriesDataSimple(BOK:060Y001.010101000)
entity_id             date
BOK:060Y001.010101000 1995-01-03                     13.06
                      1995-01-04                     11.63
                      1995-01-05                     10.61
                      1995-01-06                      9.28
                      1995-01-07                     10.78
...                                                    ...
                      2021-01-14                      0.49
                      2021-01-15                      0.50
                      2021-01-18                      0.51
                      2021-01-19                      0.48
                      2021-01-20                      0.48
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/fred -->
# 미연방은행 (FRED) 데이터 조회

미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는 prefix 로 시작합니다.

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MGqhI86LmiUzyPsdH5T" %}
[QueryFredSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/fred/queryfredseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MGqhKvshc2BFdg4Sr4-" %}
[QueryFredSeriesData](https://help.deepsearch.com/dp/api/func/economy/fred/queryfredseriesdata.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MGqhMqC\_piAYCecrKU\_" %}
[GetFredCategoryOfDataSeries](https://help.deepsearch.com/dp/api/func/economy/fred/getfredcategoryofdataseries.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MGqhO\_TuetQyJbOqlHO" %}
[GetFredDataSeriesListUnderCategory](https://help.deepsearch.com/dp/api/func/economy/fred/getfreddataserieslistundercategory.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/fred/queryfredseriesinfo -->
# QueryFredSeriesInfo

선택된 미연방은행 경제 지표의 상세 정보를 조회합니다.  미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryFredSeriesInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryFredSeriesInfo(["BAMLH0A0HYM2", "UNRATE", "T10Y2Y"])

...

                                      title observation_start observation_end     frequency frequency_short    units units_short      seasonal_adjustment seasonal_adjustment_short        last_updated  popularity  group_popularity                     notes
entity_id
FRED:BAMLH0A0HYM2  ICE BofA US High Yiel...        1996-12-31      2020-09-02  Daily, Close               D  Percent           %  Not Seasonally Adjusted                       NSA 2020-09-03 08:17:06         100                99  The ICE BofA Option-A...
FRED:T10Y2Y        10-Year Treasury Cons...        1976-06-01      2020-09-03         Daily               D  Percent           %  Not Seasonally Adjusted                       NSA 2020-09-03 16:01:12          99                99  Starting with the upd...
FRED:UNRATE               Unemployment Rate        1948-01-01      2020-07-01       Monthly               M  Percent           %      Seasonally Adjusted                        SA 2020-08-07 07:47:02          99               100  The unemployment rate...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/fred/queryfredseriesdata -->
# QueryFredSeriesData

선택된 미연방은행 경제 지표의 데이터 값을 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryFredSeriesData(entity_ids, date_from=None, date_to=None)
```

###

### Parameters

| Parameter   | Type                                  | Description                                                      |
| ----------- | ------------------------------------- | ---------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                               |
| date\_from  | date                                  | 데이터 조회 기간의 시작 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.  |
| date\_to    | date                                  | 데이터 조회 기간의 마지막 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다. |

###

### Examples

```
> QueryFredSeriesData(["BAMLH0A0HYM2", "UNRATE", "T10Y2Y"])

...

                              QueryFredSeriesData([BAMLH0A0HYM2, UNRATE, T10Y2Y])
entity_id         date
FRED:BAMLH0A0HYM2 1996-12-31                      3.13
                  1997-01-02                      3.06
                  1997-01-03                      3.09
                  1997-01-06                      3.10
                  1997-01-07                      3.10
...                                                ...
FRED:UNRATE       2020-03-01                      4.40
                  2020-04-01                     14.70
                  2020-05-01                     13.30
                  2020-06-01                     11.10
                  2020-07-01                     10.20
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/fred/getfredcategoryofdataseries -->
# GetFredCategoryOfDataSeries

주어진 경제지표를 포함하고 있는 카테고리 정보를 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는 prefix 로 시작합니다.

### Function specification

```
GetFredCategoryOfDataSeries(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> GetFredCategoryOfDataSeries(["BAMLH0A0HYM2", "UNRATE", "T10Y2Y"])

...

                              GetFredCategoryOfDataSeries([BAMLH0A0HYM2, UNRATE, T10Y2Y])
entity_id         category_id
FRED:BAMLH0A0HYM2 32348                 Corporate Bonds
FRED:T10Y2Y       33446           Interest Rate Spreads
FRED:UNRATE       32447               Unemployment Rate
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/fred/getfreddataserieslistundercategory -->
# GetFredDataSeriesListUnderCategory

명시된 카테고리 내에 포함된 경제 지표들의 목록을 조회합니다. 미연방은행에서 수집한 경제 지표의 symbol 은 "FRED:" 라는 prefix 로 시작합니다.

### Function specification

```
GetFredDataSeriesListUnderCategory(category_ids)
```

###

### Parameters

| Parameter     | Type                            | Description               |
| ------------- | ------------------------------- | ------------------------- |
| category\_ids | <p>int or</p><p>list of int</p> | 조회하고자 하는 카테고리의 ID 를 명시합니. |

###

### Examples

```
> GetFredDataSeriesListUnderCategory([33446])

...

                                              title observation_start observation_end frequency_short units_short seasonal_adjustment_short
category_id entity_id
33446       FRED:AAA10Y    Moody's Seasoned Aaa ...        1983-01-03      2020-09-02               D           %                       NSA
            FRED:AAA10YM   Moody's Seasoned Aaa ...        1953-04-01      2020-08-01               M           %                       NSA
            FRED:AAAFF     Moody's Seasoned Aaa ...        1983-01-03      2020-09-02               D           %                       NSA
            FRED:AAAFFM    Moody's Seasoned Aaa ...        1954-07-01      2020-08-01               M           %                       NSA
            FRED:BAA10Y    Moody's Seasoned Baa ...        1986-01-02      2020-09-02               D           %                       NSA
...                                             ...               ...             ...             ...         ...                       ...
            FRED:T6MFFM    6-Month Treasury Cons...        1982-01-01      2020-08-01               M           %                       NSA
            FRED:T7YIEM    7-year Breakeven Infl...        2003-01-01      2020-08-01               M           %                       NSA
            FRED:TB3SMFFM  3-Month Treasury Bill...        1954-07-01      2020-08-01               M           %                       NSA
            FRED:TB6SMFFM  6-Month Treasury Bill...        1958-12-01      2020-08-01               M           %                       NSA
            FRED:TEDRATE                 TED Spread        1986-01-02      2020-08-27               D           %                       NSA
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf -->
# IMF 데이터 조회

IMF 에서 수집한 경제 지표의 symbol 은 "IMF:\[dataflow id].\[item codes]" 의 구조를 가지고 있습니다. 시작 부분의 "IMF:" 는 IMF 에서 수집되었음을 나타내는 prefix 이고, dataflow 는 IMF 가 데이터셋을 관리하는 단위입니다. Item codes 의 구조는 dataflow 에 따라 다르게 나타납니다.

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MWMTY1hQ8dXii27b\_UA" %}
[GetImfSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/imf/getimfseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMTbzmBpmApiEcAN26" %}
[GetImfSeriesValues](https://help.deepsearch.com/dp/api/func/economy/imf/getimfseriesvalues.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMTe5looDKw5P8WhBE" %}
[GetImfDataflowAnnotations](https://help.deepsearch.com/dp/api/func/economy/imf/getimfdataflowannotations.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMTfA8R-V3C\_6L18Tq" %}
[GetImfIndicatorListOfSameCountry](https://help.deepsearch.com/dp/api/func/economy/imf/getimfcountrylistofsameindicator.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMTg3Gn\_sIg3b7TMtk" %}
[GetImfCountryListOfSameIndicator](https://help.deepsearch.com/dp/api/func/economy/imf/getimfindicatorlistofsamecountry.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf/getimfseriesinfo -->
# GetImfSeriesInfo

선택된 IMF 경제 지표의상세 정보를 조회합니다. IMF 에서 수집한 경제 지표의 symbol 은"IMF:" 라는 prefix 로 시작합니다.

### Function specification

```
GetImfSeriesInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetImfSeriesInfo(["IMF:BOP.A.AU.BCA_BP6_USD", "IMF:BOP.A.AR.BEFD_BP6_USD"])

...

                          dataflow_id              dataset_name                      name Frequency Geographical Areas                 Indicator     Scale Time format
entity_id
IMF:BOP.A.AR.BEFD_BP6_USD         BOP  Balance of Payments (...  Exceptional Financing...    Annual          Argentina  Exceptional Financing...  Millions      Annual
IMF:BOP.A.AU.BCA_BP6_USD          BOP  Balance of Payments (...  Current Account, Tota...    Annual          Australia  Current Account, Tota...  Millions      Annual
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf/getimfseriesvalues -->
# GetImfSeriesValues

선택된 IMF 경제 지표의 데이터 값을 조회합니다. IMF에서 수집한 경제 지표의 symbol 은 "IMF:" 라는 prefix 로 시작합니다.

### Function specification

```
GetImfSeriesValues(entity_ids, date_from=None, date_to=None)
```

###

### Parameters

| Parameter   | Type                                  | Description                                                      |
| ----------- | ------------------------------------- | ---------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                               |
| date\_from  | date                                  | 데이터 조회 기간의 시작 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.  |
| date\_to    | date                                  | 데이터 조회 기간의 마지막 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다. |

###

### Examples

```
>>> GetImfSeriesValues("IMF:BOP.A.AU.BCA_BP6_USD")

...

                                     GetImfSeriesValues(IMF:BOP.A.AU.BCA_BP6_USD)
entity_id                date
IMF:BOP.A.AU.BCA_BP6_USD 1989-12-31               -18340.0914
                         1990-12-31               -15532.3758
                         1991-12-31               -10586.1628
                         1992-12-31               -10313.3046
                         1993-12-31                -9289.5209
...                                                       ...
                         2016-12-31               -41035.4161
                         2017-12-31               -35951.6948
                         2018-12-31               -29784.7383
                         2019-12-31                 8033.4004
                         2020-12-31                33829.3207

```

```
>>> GetImfSeriesValues(["IMF:BOP.A.AU.BCA_BP6_USD", "IMF:BOP.A.AR.BEFD_BP6_USD"], date_from=2010-01-01, date_to=2016-12-31)

...

                                      GetImfSeriesValues([IMF:BOP.A.AU.BCA_BP6_USD, IMF:BOP.A.AR.BEFD_BP6_USD], date_from=2010-01-01, date_to=2016-12-31)
entity_id                 date
IMF:BOP.A.AR.BEFD_BP6_USD 2010-12-31                    0.0000
                          2011-12-31                    0.0000
                          2012-12-31                    0.0000
                          2013-12-31                    0.0000
                          2014-12-31                    0.0000
                          2015-12-31                    0.0000
                          2016-12-31                    0.0000
IMF:BOP.A.AU.BCA_BP6_USD  2010-12-31               -44714.2461
                          2011-12-31               -44431.1561
                          2012-12-31               -64482.9100
                          2013-12-31               -47872.5310
                          2014-12-31               -43397.3976
                          2015-12-31               -56958.7118
                          2016-12-31               -41035.4161
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf/getimfdataflowannotations -->
# GetImfDataflowAnnotations

IMF 는 데이터를 dataflow 라는 묶음으로 나누어 관리합니다. 이 API 함수는 지정된 데이터 시리즈가 포함된 dataflow 의 주석 정보를 불러옵니다.

### Function specification

```
GetImfDataflowAnnotations(entity_ids)
```

IMF entity\_id 는 "IMF:xxx.yyy.zzz" 과 같은 형태로 여러 코드가 dot (.) 으로 묶여있는 형태로 이루어져 있는데, 이 때 "IMF:" prefix 바로 뒤에 붙어 있는 "xxx" 가 바로 dataflow 의 ID 를 나타냅니다.

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetImfDataflowAnnotations("IMF:BOP.A.AU.BCA_BP6_USD")

...

                                GetImfDataflowAnnotations(IMF:BOP.A.AU.BCA_BP6_USD)
dataflow_id title
BOP         Code                                      BOP
            Definition           Contains balance of p...
            Geographic Coverage  Balance of payments d...
            Latest Update Date                 03/24/2021
            Methodology          <a href="http://www.i...
            Name                 Balance of Payments (...
            Sectoral Coverage    Total economy; reside...
            Temporal Coverage    Data available starti...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf/getimfcountrylistofsameindicator -->
# GetImfIndicatorListOfSameCountry

지정된 entity\_id 와 동일한 dataflow 안에서 해당 국가에 대한 다른 데이터 시리즈의 목록을 가져옵니다. 함수의 특성 상 entity\_id 의 목록이 아니라 단일 entity\_id 에 대해서만 동작합니다.

### Function specification

```
GetImfIndicatorListOfSameCountry(entity_id)
```

###

### Parameters

| Parameter  | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| entity\_id | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetImfIndicatorListOfSameCountry("IMF:BOP.A.AU.BCA_BP6_USD")

...

                          GetImfIndicatorListOfSameCountry(IMF:BOP.A.AU.BCA_BP6_USD)
entity_id
IMF:BOP.A.AU.BACK_BP6_USD  Net Lending (+) / Net...
IMF:BOP.A.AU.BACK_BP6_XDC  Net Lending (+) / Net...
IMF:BOP.A.AU.BCAXF_BP6...  Supplementary Items, ...
IMF:BOP.A.AU.BCA_BP6_USD   Current Account, Tota...
IMF:BOP.A.AU.BCA_BP6_XDC   Current Account, Tota...
...                                             ...
IMF:BOP.A.AU.ILP_BP6_XDC   Liabilities, Portfoli...
IMF:BOP.A.AU.IL_BP6_USD    Liabilities, Total, U...
IMF:BOP.A.AU.IL_BP6_XDC    Liabilities, Total, N...
IMF:BOP.A.AU.I_BP6_USD            Total, US Dollars
IMF:BOP.A.AU.I_BP6_XDC     Total, National Currency
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/imf/getimfindicatorlistofsamecountry -->
# GetImfCountryListOfSameIndicator

지정된 entity\_id 와 동일한 dataflow 안에서 해당 경제지표와 동일한 내용한 데이터를 제공하는 다른 국가들의 목록을 가져옵니다. 함수의 특성 상 entity\_id 의 목록이 아니라 단일 entity\_id 에 대해서만 동작합니다.

### Function specification

```
GetImfCountryListOfSameIndicator(entity_id)
```

###

### Parameters

| Parameter  | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| entity\_id | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetImfCountryListOfSameIndicator("IMF:BOP.A.AU.BCA_BP6_USD")

...
                          
                          GetImfCountryListOfSameIndicator(IMF:BOP.A.AU.BCA_BP6_USD)
entity_id
IMF:BOP.A.1C_355.BCA_B...     Curacao & St. Maarten
IMF:BOP.A.5Y.BCA_BP6_USD   Eastern Caribbean Cur...
IMF:BOP.A.AF.BCA_BP6_USD                Afghanistan
IMF:BOP.A.AG.BCA_BP6_USD        Antigua and Barbuda
IMF:BOP.A.AI.BCA_BP6_USD                   Anguilla
...                                             ...
IMF:BOP.A.XK.BCA_BP6_USD        Kosovo, Republic of
IMF:BOP.A.YE.BCA_BP6_USD                      Yemen
IMF:BOP.A.ZA.BCA_BP6_USD               South Africa
IMF:BOP.A.ZM.BCA_BP6_USD                     Zambia
IMF:BOP.A.ZW.BCA_BP6_USD                   Zimbabwe
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/oecd -->
# OECD 데이터 조회

OECD 에서 수집한 경제 지표의 symbol 은 "OECD:\[dataset id].\[item codes]" 의 구조를 가지고 있습니다. 시작 부분의 "OECD:" 는 OECD 에서 수집되었음을 나타내는 prefix 이고, dataset 은 OECD 가 데이터셋을 관리하는 단위입니다. Item codes 의 구조는 dataset 에 따라 다르게 나타납니다.

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MWMTw7F0u2UMgjGfdyT" %}
[GetOecdSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMU-3OGGVjr8t29yXU" %}
[GetOecdSeriesValues](https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdseriesvalues.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMU-nVqrxiFoJqZL2\_" %}
[GetOecdDatasetAnnotations](https://help.deepsearch.com/dp/api/func/economy/oecd/getoecddatasetannotations.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MWMU0JGm4KrHFmK5DTH" %}
[GetOecdRelatedIndicatorList](https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdrelatedindicatorlist.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdseriesinfo -->
# GetOecdSeriesInfo

선택된 OECD 경제 지표의상세 정보를 조회합니다. OECD 에서 수집한 경제 지표의 symbol 은"OECD:" 라는 prefix 로 시작합니다.

### Function specification

```
GetOecdSeriesInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetOecdSeriesInfo("OECD:AEA.HRV.ACG.O.TSO2")

...

                        dataset_id       item_code              dataset_name  Country                   Measure                 Activity                  Pollutant AEA_UNIT codelist AEA_POWERCODE codelist AEA_TIME_FORMAT codelist               series_name
entity_id
OECD:AEA.HRV.ACG.O.TSO2        AEA  HRV.ACG.O.TSO2  Air and greenhouse ga...  Croatia  tonnes of SO2 equivalent  Public administration...  Acidifying gases (SOX...            Tonnes                  Units                   Annual  Air and greenhouse ga...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdseriesvalues -->
# GetOecdSeriesValues

선택된 OECD 경제 지표의 데이터 값을 조회합니다. OECD 에서 수집한 경제 지표의 symbol 은 "OECD:" 라는 prefix 로 시작합니다.

### Function specification

```
GetOecdSeriesValues(entity_ids, date_from=None, date_to=None)
```

###

### Parameters

| Parameter   | Type                                  | Description                                                      |
| ----------- | ------------------------------------- | ---------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                               |
| date\_from  | date                                  | 데이터 조회 기간의 시작 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.  |
| date\_to    | date                                  | 데이터 조회 기간의 마지막 날짜를 지정합니다. 데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다. |

###

### Examples

```
>>> GetOecdSeriesValues("OECD:AEA.HRV.ACG.O.TSO2")

...

                                    GetOecdSeriesValues(OECD:AEA.HRV.ACG.O.TSO2)
entity_id               date
OECD:AEA.HRV.ACG.O.TSO2 2008-12-31                     330.0
                        2009-12-31                     323.0
                        2010-12-31                     309.0
                        2011-12-31                     273.0
                        2012-12-31                     235.0
                        2013-12-31                     236.0
                        2014-12-31                     213.0
                        2015-12-31                     217.0
                        2016-12-31                     214.0
                        2017-12-31                     238.0
                        2018-12-31                     221.0

Duration(compiler): 0.12 seconds
Duration(computing): 0.14 seconds
Duration(pods): 0.0 seconds
Duration(total): 0.26 seconds
Duration(parse): 0.0 seconds
```

```
>>> GetOecdSeriesValues(["OECD:ALFS_EMP.ESP.YW99P4L1_ST.TT.A", "OECD:FDI_FLOW_CTRY.AUT.SUB.DO.T_FA_FL.ALL.A.IMC.SGP", "OECD:FDI_FLOW_CTRY.BEL.USD.DO.T_FA_F5A.ROU.NET.IMC.BGD"], date_from=2010-01-01, date_to=2016-12-31)

...

                                      GetOecdSeriesValues([OECD:ALFS_EMP.ESP.YW99P4L1_ST.TT.A, OECD:FDI_FLOW_CTRY.AUT.SUB.DO.T_FA_FL.ALL.A.IMC.SGP, OECD:FDI_FLOW_CTRY.BEL.USD.DO.T_FA_F5A.ROU.NET.IMC.BGD], date_from=2010-01-01, date_to=2016-12-31)
entity_id                 date
OECD:ALFS_EMP.ESP.YW99... 2010-12-31                  1162.125
                          2011-12-31                  1157.800
                          2012-12-31                  1151.225
                          2013-12-31                  1105.650
                          2014-12-31                  1094.500
                          2015-12-31                  1112.900
                          2016-12-31                  1199.050
OECD:FDI_FLOW_CTRY.BEL... 2016-12-31                     0.000
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/oecd/getoecddatasetannotations -->
# GetOecdDatasetAnnotations

OECD 는 데이터를 dataset 이라는 묶음으로 나누어 관리합니다. 이 API 함수는 지정된 데이터 시리즈가 포함된 dataset 의 주석 정보를 불러옵니다.

### Function specification

```
GetOecdDatasetAnnotations(entity_ids)
```

OECD entity\_id 는 "OECD:xxx.yyy.zzz" 과 같은 형태로 여러 코드가 dot (.) 으로 묶여있는 형태로 이루어져 있는데, 이 때 "OECD:" prefix 바로 뒤에 붙어 있는 "xxx" 가 바로 dataset 의 ID 를 나타냅니다.

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetOecdDatasetAnnotations("OECD:AEA.HRV.ACG.O.TSO2")

...

                        dataset_name             database_name   classification       dataset_description                       url      database_description
dataset_id
AEA         Air and greenhouse ga...  OECD Environment Stat...  Air and climate  Air Emission Accounts...  https://www.oecd-ilib...  The OECD Environmenta...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/oecd/getoecdrelatedindicatorlist -->
# GetOecdRelatedIndicatorList

OECD entity\_id 는 "OECD:xxx.yyy.zzz" 과 같은 형태로 여러 코드가 dot (.) 으로 묶여있는 형태로 이루어져 있는데, 이 때 dot 으로 묶인 각각의 token 은 독립된 dimension 을 나타냅니다. 이 함수는 각 dimension 별로 어떤 값을 사용할 수 있는지 목록을 보여줍니다.

### Function specification

```
GetOecdRelatedIndicatorList(entity_id)
```

###

### Parameters

| Parameter  | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| entity\_id | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
>>> GetOecdRelatedIndicatorList("OECD:7HA_A_Q.BEL.AF4LI.ST.CXCE.Q")

...

                               entity_id           code_value_name
code_list_name
Country         OECD:7HA_A_Q.AUT.AF4L...                   Austria
Country         OECD:7HA_A_Q.BEL.AF4L...                   Belgium
Country         OECD:7HA_A_Q.CHL.AF4L...                     Chile
Country         OECD:7HA_A_Q.DEU.AF4L...                   Germany
Country         OECD:7HA_A_Q.DNK.AF4L...                   Denmark
...                                  ...                       ...
Transaction     OECD:7HA_A_Q.BEL.AN11...      Of which   Dwellings
Measure         OECD:7HA_A_Q.BEL.AF4L...  National currency, cu...
Measure         OECD:7HA_A_Q.BEL.AF4L...  US $, current prices,...
Frequency       OECD:7HA_A_Q.BEL.AF4L...                    Annual
Frequency       OECD:7HA_A_Q.BEL.AF4L...                 Quarterly
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/world-bank -->
# World Bank 데이터 조회

World Bank 에서 수집한 경제 지표의 symbol 은 "WB:\[indicator id]-\[country code]" 의 구조를 가지고 있습니다. 시작 부분의 "WB:" 는 World Bank 에서 수집되었음을 나타내는 prefix 이고, 마지막 세 글자는 국가별 코드를 나타냅니다.

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MRcgobgtHmjj8lZUASl" %}
[QueryWorldBankSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/world-bank/queryworldbankseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcgr3V4sIlg-xMsij\_" %}
[QueryWorldBankSeriesData](https://help.deepsearch.com/dp/api/func/economy/world-bank/queryworldbankseriesdata.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRch-FUr6yaV9wtw98P" %}
[GetWorldBankCountryListOfIndicator](https://help.deepsearch.com/dp/api/func/economy/world-bank/getworldbankcountrylistofindicator.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRch2IaNOUCi0qdI7pL" %}
[GetWorldBankIndicatorListOfSameSource](https://help.deepsearch.com/dp/api/func/economy/world-bank/getworldbankindicatorlistofsamesource.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/world-bank/queryworldbankseriesinfo -->
# QueryWorldBankSeriesInfo

선택된 World Bank 경제 지표의 상세 정보를 조회합니다.  World Bank 에서 수집한 경제 지표의 symbol 은 "WB:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryWorldBankSeriesInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryWorldBankSeriesInfo("WB:EN.ATM.CO2E.PC-KOR")

...

                         indicator_id country_id            indicator_name  source_id               source_name unit                source_org               source_note country_name capital_city
entity_id
WB:EN.ATM.CO2E.PC-KOR  EN.ATM.CO2E.PC        KOR  CO2 emissions (metric...          2  World Development Ind...       Carbon Dioxide Inform...  Carbon dioxide emissi...  Korea, Rep.        Seoul
```

```
> QueryWorldBankSeriesInfo(["WB:EN.ATM.CO2E.PC-KOR", "AG.LND.TOTL.K2-JPN", "EN.POP.DNST"])

...

                         indicator_id country_id            indicator_name  source_id               source_name unit                source_org               source_note country_name capital_city
entity_id
WB:AG.LND.TOTL.K2-JPN  AG.LND.TOTL.K2        JPN        Land area (sq. km)          2  World Development Ind...       Food and Agriculture ...  Land area is a countr...        Japan        Tokyo
WB:EN.POP.DNST            EN.POP.DNST       <NA>  Population density (p...          2  World Development Ind...       Food and Agriculture ...  Population density is...         <NA>         <NA>
WB:EN.ATM.CO2E.PC-KOR  EN.ATM.CO2E.PC        KOR  CO2 emissions (metric...          2  World Development Ind...       Carbon Dioxide Inform...  Carbon dioxide emissi...  Korea, Rep.        Seoul
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/world-bank/queryworldbankseriesdata -->
# QueryWorldBankSeriesData

선택된 World Bank 경제 지표의 데이터 값을 조회합니다.

### Function specification

```
QueryWorldBankSeriesData(entity_ids, date_from=None, date_to=None)
```

###

### Parameters

| Parameter   | Type                                  | Description                                                                   |
| ----------- | ------------------------------------- | ----------------------------------------------------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                                            |
| date\_from  | date                                  | <p>데이터 조회 기간의 시작 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p>  |
| date\_to    | date                                  | <p>데이터 조회 기간의 마지막 날짜를 지정합니다.</p><p>데이터 조회 기간이 주어지지 않을 경우 전체 기간을 대상으로 합니다.</p> |

###

### Examples

```
> QueryWorldBankSeriesData("WB:EN.ATM.CO2E.PC-KOR")

...

                                  QueryWorldBankSeriesData(WB:EN.ATM.CO2E.PC-KOR)
entity_id             date
WB:EN.ATM.CO2E.PC-KOR 1960-12-31                    0.5018
                      1961-12-31                    0.5613
                      1962-12-31                    0.6517
                      1963-12-31                    0.7741
                      1964-12-31                    0.7940
...                                                    ...
                      2012-12-31                   11.6328
                      2013-12-31                   11.7492
                      2014-12-31                   11.5703
                      2015-12-31                   11.7094
                      2016-12-31                   12.1111
```

```
> QueryWorldBankSeriesData(["WB:EN.ATM.CO2E.PC-KOR", "AG.LND.TOTL.K2-JPN"], date_from=2000-01-01, date_to=2020-12-31)

...

                                  QueryWorldBankSeriesData([WB:EN.ATM.CO2E.PC-KOR, AG.LND.TOTL.K2-JPN], date_from=2000-01-01, date_to=2020-12-31)
entity_id             date
WB:AG.LND.TOTL.K2-JPN 2000-12-31               364500.0000
                      2001-12-31               364500.0000
                      2002-12-31               364500.0000
                      2003-12-31               364500.0000
                      2004-12-31               364500.0000
...                                                    ...
WB:EN.ATM.CO2E.PC-KOR 2012-12-31                   11.6328
                      2013-12-31                   11.7492
                      2014-12-31                   11.5703
                      2015-12-31                   11.7094
                      2016-12-31                   12.1111
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/world-bank/getworldbankcountrylistofindicator -->
# GetWorldBankCountryListOfIndicator

World Bank 는 다양한 국가들에 대해 데이터를 모아 제공합니다. 본 API 함수는 선택된 경제 지표의 값을 가지고 있는 다른 국가들의 목록을 조회합니다. 동종 경제 지표에 대해 국가간 비교를 할 때 사용할 수 있습니다.

### Function specification

```
GetWorldBankCountryListOfIndicator(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> GetWorldBankCountryListOfIndicator("WB:EN.ATM.CO2E.PC-KOR")

...

                           country_name      capital_city
indicator_id   country_id
EN.ATM.CO2E.PC ABW                Aruba        Oranjestad
               AFG          Afghanistan             Kabul
               AGO               Angola            Luanda
               ALB              Albania            Tirane
               AND              Andorra  Andorra la Vella
...                                 ...               ...
               XKX               Kosovo          Pristina
               YEM          Yemen, Rep.            Sana'a
               ZAF         South Africa          Pretoria
               ZMB               Zambia            Lusaka
               ZWE             Zimbabwe            Harare
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/world-bank/getworldbankindicatorlistofsamesource -->
# GetWorldBankIndicatorListOfSameSource

World Bank 는 다양한 출처 (source) 에서 데이터를 모아 제공하고 있습니다. 본 API 함수는 선택된 경제 지표와 동일한 출처에서 수집된 다른 데이터 항목들의 목록을 보여줍니다.

### Function specification

```
GetWorldBankIndicatorListOfSameSource(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> GetWorldBankIndicatorListOfSameSource("WB:EN.ATM.CO2E.PC-KOR")

...

                                       indicator_name               source_name
source_id indicator_id
2         AG.AGR.TRAC.NO     Agricultural machiner...  World Development Ind...
          AG.CON.FERT.PT.ZS  Fertilizer consumptio...  World Development Ind...
          AG.CON.FERT.ZS     Fertilizer consumptio...  World Development Ind...
          AG.LND.AGRI.K2     Agricultural land (sq...  World Development Ind...
          AG.LND.AGRI.ZS     Agricultural land (% ...  World Development Ind...
...                                               ...                       ...
          VC.IDP.TOCV        Internally displaced ...  World Development Ind...
          VC.IHR.PSRC.FE.P5  Intentional homicides...  World Development Ind...
          VC.IHR.PSRC.MA.P5  Intentional homicides...  World Development Ind...
          VC.IHR.PSRC.P5     Intentional homicides...  World Development Ind...
          VC.PKP.TOTL.UN     Presence of peace kee...  World Development Ind...
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat -->
# 통계청 데이터 조회

통계청에서 수집한 데이터는 여타 다른 경제 지표들과는 다르게 time series 가 아닌 cross-section table 을 기본 구조로 가지고 있습니다. 통계청에서 수집한 데이터의 symbol 은 "KOSIS:" 로 시작합니다.

{% content-ref url="/pages/-MRclXvIfrRbD8y\_w8nt" %}
[QueryKosisTableInfo](https://help.deepsearch.com/dp/api/func/economy/kostat/querykosistableinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcl\_33xmyc1g9-Ik3h" %}
[GetKosisAvailableSampleDates](https://help.deepsearch.com/dp/api/func/economy/kostat/getkosisavailablesampledates.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRclc-TE9ZigD3I21\_a" %}
[GetKosisTableCategoryItemFreqList](https://help.deepsearch.com/dp/api/func/economy/kostat/getkosistablecategoryitemfreqlist.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRclgQ64aKqnXVAECoB" %}
[QueryKosisCrossSectionData](https://help.deepsearch.com/dp/api/func/economy/kostat/querykosiscrosssectiondata.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcljzdThtVyCgorqwQ" %}
[QueryKosisTimeSeriesData](https://help.deepsearch.com/dp/api/func/economy/kostat/querykosistimeseriesdata.md)
{% endcontent-ref %}

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 통계청(KOSIS) 함수 5개는 모두 이 레포의 API 키로 `NameError: UFunction ... is not defined`입니다.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat/querykosistableinfo -->
# QueryKosisTableInfo

선택된 통계청 경제 지표에 대한 상세 정보를 표시합니다. 통계청에서 수집된 데이터는 "KOSIS:" 라는 prefix 를 가지고 있습니다.

### Function specification

```
QueryKosisTableInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryKosisTableInfo("KOSIS:101.DT_1011301")

...

                     org_id    table_id org_name             table_name             table_comment unit_ko  source_name source_dept source_dept_phone
entity_id
KOSIS:101.DT_1011301    101  DT_1011301      통계청  작성기관별/담당정도별 전체 및 통계인력  통계인력 : 통계업무 비중이 담당업무의...       명  「통계인력및예산조사」                  042-481-2066
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'QueryKosisTableInfo' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat/getkosisavailablesampledates -->
# GetKosisAvailableSampleDates

선택된 통계청 경제 지표의 값이 들어있는 전체 날짜 목록을 표시합니다. 일부 경제 지표의 경우 둘 이상의 주기 (예: 월별, 분기별, 연도별) 에 데이터를 제공하고 있기 때문에, 날짜 뿐만 아니라 해당 주기도 freq 라는 컬럼에 담아 돌려줍니다.

### Function specification

```
GetKosisAvailableSampleDates(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> GetKosisAvailableSampleDates("KOSIS:101.DT_1011301")

...

                     freq       date
entity_id
KOSIS:101.DT_1011301    Y 1990-12-31
KOSIS:101.DT_1011301    Y 1992-12-31
KOSIS:101.DT_1011301    Y 1994-12-31
KOSIS:101.DT_1011301    Y 1996-12-31
KOSIS:101.DT_1011301    Y 1998-12-31
KOSIS:101.DT_1011301    Y 2000-12-31
KOSIS:101.DT_1011301    Y 2002-12-31
KOSIS:101.DT_1011301    Y 2004-12-31
KOSIS:101.DT_1011301    Y 2006-12-31
KOSIS:101.DT_1011301    Y 2008-12-31
KOSIS:101.DT_1011301    Y 2010-12-31
KOSIS:101.DT_1011301    Y 2012-12-31
KOSIS:101.DT_1011301    Y 2014-12-31
KOSIS:101.DT_1011301    Y 2016-12-31
KOSIS:101.DT_1011301    Y 2018-12-31
KOSIS:101.DT_1011301    Y 2020-12-31
```

```
> GetKosisAvailableSampleDates("KOSIS:101.DT_1EW0004")

...

                     freq       date
entity_id
KOSIS:101.DT_1EW0004    M 1990-01-31
KOSIS:101.DT_1EW0004    M 1990-02-28
KOSIS:101.DT_1EW0004    M 1990-03-31
KOSIS:101.DT_1EW0004    M 1990-04-30
KOSIS:101.DT_1EW0004    M 1990-05-31
...                   ...        ...
KOSIS:101.DT_1EW0004    Y 2015-12-31
KOSIS:101.DT_1EW0004    Y 2016-12-31
KOSIS:101.DT_1EW0004    Y 2017-12-31
KOSIS:101.DT_1EW0004    Y 2018-12-31
KOSIS:101.DT_1EW0004    Y 2019-12-31
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetKosisAvailableSampleDates' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat/getkosistablecategoryitemfreqlist -->
# GetKosisTableCategoryItemFreqList

선택된 통계청 경제 지표의 테이블을 구성하고 있는 category 와 item code, 그리고 freq 의 목록을 표시합니다. Category 는 해당 테이블의 row 를, 그리고 item code 는 column 을 구성한다고 이해할 수 있습니다. Category 의 경우 최대 8 단계까지 depth 를 두어 구성될 수 있습니다.

### Function specification

```
GetKosisTableCategoryItemFreqList(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> GetKosisTableCategoryItemFreqList("KOSIS:101.DT_1011301")

...

                       seq cat_type cat_type_name_ko    cat_id cat_id_name_ko parent_id
entity_id
KOSIS:101.DT_1011301     1        A            작성기관별      A000             합계      <NA>
KOSIS:101.DT_1011301     1        A            작성기관별      A001           정부기관      <NA>
KOSIS:101.DT_1011301     1        A            작성기관별      A002         중앙행정기관      <NA>
KOSIS:101.DT_1011301     1        A            작성기관별  A002A000            통계청      A002
KOSIS:101.DT_1011301     1        A            작성기관별  A002A001          기획재정부      A002
...                    ...      ...              ...       ...            ...       ...
KOSIS:101.DT_1011301     2        B            담당정도별      B001         통계업무전담      <NA>
KOSIS:101.DT_1011301     2        B            담당정도별      B002         주로통계업무      <NA>
KOSIS:101.DT_1011301     2        B            담당정도별      B003         주로다른업무      <NA>
KOSIS:101.DT_1011301  <NA>     ITEM   Item code list       T10             인력      <NA>
KOSIS:101.DT_1011301  <NA>     FREQ        Frequency         Y             2년      <NA>
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetKosisTableCategoryItemFreqList' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat/querykosiscrosssectiondata -->
# QueryKosisCrossSectionData

선택된 통계청 경제 지표의 데이터 값을 리턴합니다. 통계청 데이터는 횡단면 테이블 (cross-section table) 이기 때문에, 단일 날짜에 대해서만 결과 값을 구해올 수 있습니다. 날짜를 지정하지 않을 경우 가장 마지막 날짜의 값을 가져옵니다.

### Function specification

```
QueryKosisCrossSectionData(entity_id, freq=None, date=None)
```

###

### Parameters

| Parameter  | Type   | Description                                                                                                                               |
| ---------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| entity\_id | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                                                                                                        |
| freq       | string | 동일 entity\_id 가 둘 이상의 주기 (freq) 에 대해 데이터 값을 가지고 있을 수 있기 때문에, 값을 가져오고자 하는 대상 주기를 명시해주어야 합니다. 따로 명시하지 않을 경우, 가장 최근 값을 가지고 있는 날짜의 주기를 사용합니다. |
| date       | date   | 데이터를 가져오고자 하는 날짜를 지정합니다. 따로 명시하지 않을 경우, 가장 최근 날짜를 사용합니다.                                                                                  |

###

### Examples

결과 값에 포함되어 있는 category id 와 item code 의 의미는 위 GetKosisTableCategoryItemFreqList 함수의 결과 값을 사용해서 재구성해야 합니다.

```
> QueryKosisCrossSectionData("KOSIS:101.DT_1011301")

...

                                         QueryKosisCrossSectionData(KOSIS:101.DT_1011301)
freq date       category_id   item_code
Y    2020-12-31 A000|B000     T10                          6674.0
                A000|B001     T10                          3783.0
                A000|B002     T10                          1694.0
                A000|B003     T10                          1197.0
                A001|B000     T10                          5674.0
...                                                           ...
                A007A166|B003 T10                             3.0
                A007|B000     T10                          1000.0
                A007|B001     T10                           312.0
                A007|B002     T10                           315.0
                A007|B003     T10                           373.0
```

```
> QueryKosisCrossSectionData("KOSIS:101.DT_1EW0004", "M", 2018-03-31)

...

                                       QueryKosisCrossSectionData(KOSIS:101.DT_1EW0004, M, 2018-03-31)
freq date       category_id item_code
M    2018-03-31 0|0|00|0    T01                      5.3777e+05
                            T02                      4.4962e+05
                            T03                      4.0411e+04
                            T04                      4.7737e+04
                            T05                      7.0947e+08
...                                                         ...
                4|4|39|0    T06                      1.2000e+05
                4|4|39|2    T01                      3.0000e+00
                            T02                      3.0000e+00
                            T05                      1.2000e+05
                            T06                      1.2000e+05
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'QueryKosisCrossSectionData' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/kostat/querykosistimeseriesdata -->
# QueryKosisTimeSeriesData

통계청 경제 지표의 경우 기본 구조는 횡단면 테이블 (cross-section table) 이지만, category\_id 를 명시할 경우 해당 카테고리의 내용 만을 time series 형태로 가져올 수 있습니다.

### Function specification

```
QueryKosisTimeSeriesData(entity_id, category_id, item_code=None, freq=None, date_from=None, date_to=None)
```

###

### Parameters

| Parameter    | Type   | Description                                                              |
| ------------ | ------ | ------------------------------------------------------------------------ |
| entity\_id   | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다.                                       |
| category\_id | string | 값을 조회하고자 하는 테이블 내 category id 를 지정합니다.                                   |
| item\_code   | string | 값을 조회하고자 하는 테이블 내 item code 를 지정합니다. 지정되지 않을 경우, 전체 item code 의 값을 가져옵니. |
| freq         | string | 값을 조회하고자 하는 데이터 주기를 지정합니다. 지정되지 않을 경우, 해당 테이블의 전체 주기에 대해 값을 가져옵니다.       |
| date\_from   | date   | 데이터 값을 가져올 날짜 범위의 시작을 지정합니다. 지정되지 않을 경우 전체 날짜 범위의 값을 가져옵니다.              |
| date\_t      | date   | 데이터 값을 가져올 날짜 범위의 마지막을 지정합니다. 지정되지 않을 경우 전체 날짜 범위의 값을 가져옵니다.             |

###

### Examples

입력으로 사용되는 category id 와 item code 의 값은 이전 GetKosisTableCategoryItemFreqList 함수의 결과값을 가지고 재구성하여 사용해야 합니다.

```
> QueryKosisTimeSeriesData("KOSIS:101.DT_1011301", "A000|B000")

...

                           QueryKosisTimeSeriesData(KOSIS:101.DT_1011301, A000|B000)
item_code freq date
T10       Y    1990-12-31                    5148.0
               1992-12-31                    5313.0
               1994-12-31                    5494.0
               1996-12-31                    5607.0
               1998-12-31                    5266.0
               2000-12-31                    4809.0
               2002-12-31                    5038.0
               2004-12-31                    5157.0
               2006-12-31                    5744.0
               2008-12-31                    5594.0
               2010-12-31                    5655.0
               2012-12-31                    5772.0
               2014-12-31                    5906.0
               2016-12-31                    6017.0
               2018-12-31                    6038.0
               2020-12-31                    6674.0
```

```
> QueryKosisTimeSeriesData("KOSIS:101.DT_1011301", "A000|B000", "T10", "Y")

...

                           QueryKosisTimeSeriesData(KOSIS:101.DT_1011301, A000|B000, T10, Y)
item_code freq date
T10       Y    1990-12-31                    5148.0
               1992-12-31                    5313.0
               1994-12-31                    5494.0
               1996-12-31                    5607.0
               1998-12-31                    5266.0
               2000-12-31                    4809.0
               2002-12-31                    5038.0
               2004-12-31                    5157.0
               2006-12-31                    5744.0
               2008-12-31                    5594.0
               2010-12-31                    5655.0
               2012-12-31                    5772.0
               2014-12-31                    5906.0
               2016-12-31                    6017.0
               2018-12-31                    6038.0
               2020-12-31                    6674.0
```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'QueryKosisTimeSeriesData' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/economy/deepsearch -->
# 딥서치 자체 수집 데이터 조회

딥서치에서 자체 수집한 경제 지표 데이터를 조회합니다. 딥서치 자체 수집 지표의 symbol 은 "DS:" 라는 prefix 로 시작합니다.

{% content-ref url="/pages/-MRcqnkILyn9cuyiGykP" %}
[QueryDeepSearchOwnSeriesInfo](https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchownseriesinfo.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcqqRPHI9E8nQ5iLho" %}
[QueryDeepSearchOwnSeriesValues](https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchownseriesvalues.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MRcqtAG4nhNoUHBKxsD" %}
[QueryDeepSearchOwnDataSeriesListOfSameCategory](https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchowndataserieslistofsamecategory.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchownseriesinfo -->
# QueryDeepSearchOwnSeriesInfo

지정된 딥서치 자체 수집 경제 지표 데이터의 상세 정보를 조회합니다. 딥서치 자체 수집 지표의 symbol 은 "DS:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryDeepSearchOwnSeriesInfo(entity_ids)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryDeepSearchOwnSeriesInfo("DS:TOUR.001.0001")

...

                        name_ko                   name_en frequency    unit     source               source_url       description notes
entity_id
DS:TOUR.001.0001  내국인 해외여행 출국자수  Number of South Korea...   Monthly  Person  관광지식정보시스템  https://www.tour.go.kr/  한국인 해외여행 목적 출국자수
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchownseriesvalues -->
# QueryDeepSearchOwnSeriesValues

지정된 딥서치 자체 수집 경제 지표의 데이터 값을 조회합니다. 딥서치 자체 수집 지표의 symbol 은 "DS:" 라는 prefix 로 시작합니다.

### Function specification

```
QueryDeepSearchOwnSeriesValues(entity_ids, date_from=None, date_to=None)
```

###

### Parameters

| Parameter   | Type                                  | Description                        |
| ----------- | ------------------------------------- | ---------------------------------- |
| entity\_ids | <p>string or</p><p>list of string</p> | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryDeepSearchOwnSeriesValues("DS:TOUR.001.0001")

...

                             QueryDeepSearchOwnSeriesValues(DS:TOUR.001.0001)
entity_id        date
DS:TOUR.001.0001 2005-01-31                  897406.0
                 2005-02-28                  745998.0
                 2005-03-31                  707058.0
                 2005-04-30                  762096.0
                 2005-05-31                  802497.0
...                                               ...
                 2020-06-30                   48353.0
                 2020-07-31                   65936.0
                 2020-08-31                   88888.0
                 2020-09-30                   76798.0
                 2020-10-31                   71970.0
```

<!-- source: https://help.deepsearch.com/dp/api/func/economy/deepsearch/querydeepsearchowndataserieslistofsamecategory -->
# QueryDeepSearchOwnDataSeriesListOfSameCategory

지정된 딥서치 자체 수집 경제 지표와 동일한 카테고리에 속하는 다른 지표 목록을 조회합니다.

### Function specification

```
QueryDeepSearchOwnDataSeriesListOfSameCategory(entity_id)
```

###

### Parameters

| Parameter  | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| entity\_id | string | 조회하고자 하는 경제 지표의 entity id 를 명시합니다. |

###

### Examples

```
> QueryDeepSearchOwnDataSeriesListOfSameCategory("DS:TOUR.001.0003")

...

                     QueryDeepSearchOwnDataSeriesListOfSameCategory(DS:TOUR.001.0003)
entity_id
DS:TOUR.001.0003                   대륙별 국내 입국자수
DS:TOUR.001.0003.001           대륙별 국내 입국자수_아시아
DS:TOUR.001.0003.002            대륙별 국내 입국자수_중동
DS:TOUR.001.0003.003            대륙별 국내 입국자수_미주
DS:TOUR.001.0003.004            대륙별 국내 입국자수_유럽
DS:TOUR.001.0003.005           대륙별 국내 입국자수_대양주
DS:TOUR.001.0003.006          대륙별 국내 입국자수_아프리카
DS:TOUR.001.0003.007            대륙별 국내 입국자수_기타
```
