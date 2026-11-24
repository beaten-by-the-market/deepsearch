<!-- 이 파일은 docs/reference/sync_from_gitbook.py로 생성합니다 (2026-11-25). 원문: https://help.deepsearch.com/dp/ — 기업 검색·정보·재무제표·공시(DART)·컨센서스·이슈기업·주가. 직접 고치지 말고, 레포 메모는 repo-memo 마커 안에 쓰세요. -->

<!-- source: https://help.deepsearch.com/dp/api/func -->
# API 함수를 통한 데이터 조회

기본 쿼리 형태 (entity - property - date range) 로 표시가 어려운 데이터의 경우엔 각 데이터 소스를 담당하는 API 함수를 사용하여 정보를 조회할 수 있습니다. API 함수를 이용하여 조회 가능한 데이터는 크게 다음과 같이 분류할 수 있습니다.

{% content-ref url="/pages/-M26Q67C4Uuqc1QpT2Tz" %}
[국내기업](https://help.deepsearch.com/dp/api/func/company.md)
{% endcontent-ref %}

{% content-ref url="/spaces/-LPJrnQiLiz9bWVBvx6Q/pages/l7YT1XumSCRnzhURR1My" %}
[해외기업](https://help.deepsearch.com/dp/api/func/undefined.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26QG5QYZtsa2buPZzc" %}
[산업](https://help.deepsearch.com/dp/api/func/industry.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26QBZtVCKZADNQwb04" %}
[인물](https://help.deepsearch.com/dp/api/func/people.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26QMgprxomtCn6IkjP" %}
[문서](https://help.deepsearch.com/dp/api/func/document.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26Qm2RlgE0Toeqq-Kj" %}
[이벤트](https://help.deepsearch.com/dp/api/func/event.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MGqe7fYCrjLV8B0V90z" %}
[경제 지표](https://help.deepsearch.com/dp/api/func/economy.md)
{% endcontent-ref %}

##

<!-- source: https://help.deepsearch.com/dp/api/func/company -->
# 국내기업

- [기업 검색](https://help.deepsearch.com/dp/api/func/company/company-search.md): 다양한 조건에 맞는 기업을 검색합니다.
- [FindEntity](https://help.deepsearch.com/dp/api/func/company/company-search/findentity.md): 기업명, 주소, 사업자 등록 번호 등을 조건으로 주고 이에 해당하는 기업들의 목록을 검색할 수 있습니다.
- [GetEntitySummary](https://help.deepsearch.com/dp/api/func/company/company-search/getentitysummary.md): 검색한 Entity 에 대한 정보를 가져옵니다.
- [FindEntityByName](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyname.md)
- [FindEntityByShareholderName](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyshareholdername.md)
- [FindEntityByIndustryID](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyindustryid.md)
- [FindEntityByBusinessArea](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybybusinessarea.md)
- [FindEntityByAddress](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyaddress.md)
- [FindEntityInDocuments](https://help.deepsearch.com/dp/api/func/company/company-search/findentityindocuments.md): 문서내에서 특정 키워드가 언급된 기업을 검색합니다.
- [FindAssociatedEntity](https://help.deepsearch.com/dp/api/func/company/company-search/findassociatedentity.md): 공시, 뉴스, 증권사리포트, IR 등 다양한 문서를 활용하여, 특정 주제와 관련된 기업을 검색합니다.
- [SearchFinancialStatementsAuditOpinion](https://help.deepsearch.com/dp/api/func/company/company-search/searchfinancialstatementsauditopinion.md): 감사의견을 바탕으로 기업을 검색합니다.
- [기업 정보 조회](https://help.deepsearch.com/dp/api/func/company/company.md): 기업 별 세부 정보를 조회합니다.
- [GetCompanySummary](https://help.deepsearch.com/dp/api/func/company/company/getcompanysummary.md): 기업이 개요 정보를 조회합니다.
- [GetCompanyHistory](https://help.deepsearch.com/dp/api/func/company/company/getcompanyhistory.md): 회사의 연혁 정보를 조회합니다.
- [GetCompanyBusinessGoal](https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinessgoal.md): 기업의 사업목적을 조회합니다.
- [GetCompanyBusinessSummary](https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinesssummary.md): 사업 개요 및 현황 정보를 조회합니다.
- [GetCompanyRelatedFirms](https://help.deepsearch.com/dp/api/func/company/company/getcompanyrelatedfirms.md): 관계사 정보를 조회합니다.
- [GetCompanyProductsSales](https://help.deepsearch.com/dp/api/func/company/company/getcompanyproductssales.md): 회사 제품별 매출 데이터를 조회합니다.
- [GetCompanyDebts](https://help.deepsearch.com/dp/api/func/company/company/getcompanydebts.md): 차입금 정보를 조회합니다.
- [GetCompanyDividends](https://help.deepsearch.com/dp/api/func/company/company/getcompanydividends.md): 기업의 배당 내역을 조회합니다.
- [GetCompanyShareholders](https://help.deepsearch.com/dp/api/func/company/company/getcompanyshareholders.md): 기업의 주주정보를 조회합니다.
- [GetCompanyEmployees](https://help.deepsearch.com/dp/api/func/company/company/getcompanyemployees.md): 종업원 현황 정보를 조회합니다.
- [GetCompanyExecutives](https://help.deepsearch.com/dp/api/func/company/company/getcompanyexecutives.md): 임원 정보를 조회합니다.
- [GetCompanyBranches](https://help.deepsearch.com/dp/api/func/company/company/getcompanybranches.md): 지점 정보를 조회합니다.
- [GetFinancialStatementsAuditOpinion](https://help.deepsearch.com/dp/api/func/company/company/getfinancialstatementsauditopinion.md): 특정 기업의 감사 의견을 조회합니다.
- [재무제표 조회](https://help.deepsearch.com/dp/api/func/company/financial.md): 분기별 재무제표를 조회합니다.
- [GetFinancialStatements](https://help.deepsearch.com/dp/api/func/company/financial/getfinancialstatements.md): 기업의 재무제표를 조회합니다.
- [GetAvailableFinancialStatements](https://help.deepsearch.com/dp/api/func/company/financial/getavailablefinancialstatements.md): 해당 기업이 발표하는 재무제표 종류를 조회합니다. ( 분기, 연간, IFRS/GAAP )
- [공시 정보 조회](https://help.deepsearch.com/dp/api/func/company/disclosure.md): Dart 공시 사업보고서 항목들을 조회합니다.
- [GetDartCapitalChange](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartcapitalchange.md): 정기보고서(사업, 분기, 반기보고서) 내에 증자(감자) 현황을 제공합니다.
- [GetDartDividends](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartdividends.md): 정기보고서(사업, 분기, 반기보고서) 내에 배당 내역을 조회합니다.
- [GetDartShareRepurchase](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartsharerepurchase.md): 정기보고서(사업, 분기, 반기보고서) 내에 자기주식 취득 및 처분 현황을 제공합니다.
- [GetDartMajorityShareholders](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholders.md): 정기보고서(사업, 분기, 반기보고서) 내에 최대주주 현황을 제공합니다.
- [GetDartMajorityShareholderChange](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholderchange.md): 정기보고서(사업, 분기, 반기보고서) 내에 최대주주 변동 현황을 제공합니다.
- [GetDartMinorityShareholders](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartminorityshareholders.md): 정기보고서(사업, 분기, 반기보고서) 내에 소액주주현황을 제공합니다.
- [GetDartExecutives](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartexecutives.md): 정기보고서(사업, 분기, 반기보고서) 내에 임원현황을 제공합니다.
- [GetDartEmployees](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartemployees.md): 정기보고서(사업, 분기, 반기보고서) 내에 직원현황을 제공합니다.
- [GetDartIndividualDirectorCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartindividualdirectorcompensation.md): 정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사의 개인별 보수 현황(5억 이상)을 제공합니다.
- [GetDartOverallDirectorCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartoveralldirectorcompensation.md): 정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사 전체의 보수현황을 제공합니다.
- [GetDartTopIndividualCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdarttopindividualcompensation.md): 정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다.
- [GetDartInvestmentInOthers](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartinvestmentinothers.md): 정기보고서(사업, 분기, 반기보고서) 내에 타법인 출자현황을 제공합니다.
- [컨센서스 정보 조회](https://help.deepsearch.com/dp/api/func/company/consensus.md): 증권사 애널리스트 컨센서스 정보를 조회합니다.
- [GetConsensusInstitutionList](https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusinstitutionlist.md): 컨센서스를 발표하는 기관 리스트를 조회합니다.
- [GetConsensusAnalystList](https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusanalystlist.md): 특정 기관의 애널리스트 정보를 조회합니다.
- [SearchAnalystReports](https://help.deepsearch.com/dp/api/func/company/consensus/searchanalystreports.md): 특정 기업에 대한 애널리스트 리포트를 조회합니다.
- [SearchTargetPrices](https://help.deepsearch.com/dp/api/func/company/consensus/searchtargetprices.md): 특정 종목에 대한 목표 주가를 조회합니다.
- [SearchFirmFundamentalsForecasts](https://help.deepsearch.com/dp/api/func/company/consensus/searchfirmfundamentalsforecasts.md): 특정 종목에 대한 예상 실적을 조회합니다.
- [이슈 기업 목록 조회](https://help.deepsearch.com/dp/api/func/company/issue-company.md)
- [GetCompanyShareholderChanges](https://help.deepsearch.com/dp/api/func/company/issue-company/getcompanyshareholderchanges.md): 최대 주주의 지분율이 변경된 기업 리스트를 조회합니다.
- [GetTargetPriceConsensusChange](https://help.deepsearch.com/dp/api/func/company/issue-company/gettargetpriceconsensuschange.md): 증권사 목표주가 변화 내역을 조회합니다.
- [GetFundamentalsConsensusChange](https://help.deepsearch.com/dp/api/func/company/issue-company/getfundamentalsconsensuschange.md): 증권사 컨센서스 실적 추정치 변화 내역을 조회합니다.
- [주가 정보 조회](https://help.deepsearch.com/dp/api/func/company/undefined.md)
- [GetStockSymbols](https://help.deepsearch.com/dp/api/func/company/undefined/getstocksymbols.md): 종목 정보를 조회합니다.
- [GetStockPrices](https://help.deepsearch.com/dp/api/func/company/undefined/getstockprices.md): 종목의 현재 가격 및 거래량 정보를 조회합니다.
- [GetMarketIndexSymbols](https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexsymbols.md): 지수에 대한 정보를 조회합니다.
- [GetMarketIndexes](https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexes.md): 현재 지수의 가격 및 거래량 등의 정보를 조회합니다.
- [채권 정보 조회](https://help.deepsearch.com/dp/api/func/company/bond.md)
- [GetBondClassificationCodeList](https://help.deepsearch.com/dp/api/func/company/bond/getbondclassificationcodelist.md): 전체 채권 종류를 조회합니다.
- [GetBondIssuerList](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlist.md): 특정 class 채권의 발행자 정보를 조회합니다.
- [GetBondIssuerListFromIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuerlistfromindustry.md): 특정 산업의 채권 발행자 리스트를 조회합니다.
- [GetBondIssuerSummaryInfo](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuersummaryinfo.md): 특정 채권의 요약 정보를 조회합니다.
- [GetBondClassSummaryInfo](https://help.deepsearch.com/dp/api/func/company/bond/getbondclasssummaryinfo.md): 특정 클래스의 채권 정보를 조회한다.
- [GetBondSummaryInfoPerIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondsummaryinfoperindustry.md): 특정 산업의 채권 정보를 조회한다.
- [GetLatestBondIssues](https://help.deepsearch.com/dp/api/func/company/bond/getlatestbondissues.md): 최근에 발행된 채권 정보를 조회합니다.
- [SearchBondIssuerByName](https://help.deepsearch.com/dp/api/func/company/bond/searchbondissuerbyname.md): 이름으로 채권 발행자를 검색합니다.
- [GetBondIssuanceHistory](https://help.deepsearch.com/dp/api/func/company/bond/getbondissuancehistory.md): 특정 채권 발행자의 과거 채권 발행 이력을 조회합니다.
- [GetBondRepaymentSchedule](https://help.deepsearch.com/dp/api/func/company/bond/getbondrepaymentschedule.md): 특정 채권 발행자의 상환 스케쥴을 조회합니다.
- [GetBondYields](https://help.deepsearch.com/dp/api/func/company/bond/getbondyields.md): 채권 수익률을 조회합니다.
- [GetBondYieldsForIndustry](https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldsforindustry.md): 특정 산업의 채권 수익률을 계산합니다.
- [GetAverageBondYieldTimeSeries](https://help.deepsearch.com/dp/api/func/company/bond/getaveragebondyieldtimeseries.md): 지정한 종류의 채권들의 평균 금리 time series를 계산 합니다.
- [GetInterpolatedBondYields](https://help.deepsearch.com/dp/api/func/company/bond/getinterpolatedbondyields.md): 지정한 종류의 채권들의 Interpolated 채권 수익률을 계산합니다.
- [GetRiskFreeYields](https://help.deepsearch.com/dp/api/func/company/bond/getriskfreeyields.md): 무위험 이자율을 조회합니다.
- [GetBondYieldPrincipalComponents](https://help.deepsearch.com/dp/api/func/company/bond/getbondyieldprincipalcomponents.md): 채권 주성분을 분석합니다.
- [ConvertBondIssuerCodeToNICESymbol](https://help.deepsearch.com/dp/api/func/company/bond/convertbondissuercodetonicesymbol.md): 채권 발행자 코드를 나이스 심볼로 변환합니다.
- [ConvertNICESymbolToBondIssuerCode](https://help.deepsearch.com/dp/api/func/company/bond/convertnicesymboltobondissuercode.md): 나이스 심볼 코드를 채권 발행자 코드로 변환합니다.

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search -->
# 기업 검색

다양한 조건에 맞는 기업을 검색합니다.

기업 이름, 주소, 사업 영역, 사업자 등록번호, 뉴스, 공시, 증권사리포트, IR, 특 등 다양한 조건을 사용하여 기업을 검색할 수 있습니다. 다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-M26uCbVc2FHPHrfdoeH" %}
[FindEntity](https://help.deepsearch.com/dp/api/func/company/company-search/findentity.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26yNpSVFGrEKUh25TG" %}
[FindEntityByName](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyname.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26yrzvKcC7AJxiRkaX" %}
[FindEntityByShareholderName](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyshareholdername.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26yu6wvID5o08CfG\_6" %}
[FindEntityByIndustryID](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyindustryid.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26yvRyIaHcw2TwExhh" %}
[FindEntityByBusinessArea](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybybusinessarea.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M26ywVWOz-G8I6\_aQDu" %}
[FindEntityByAddress](https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyaddress.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xdHharCvYej1DA8p" %}
[FindEntityInDocuments](https://help.deepsearch.com/dp/api/func/company/company-search/findentityindocuments.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27xac902s7h89fRkD4" %}
[FindAssociatedEntity](https://help.deepsearch.com/dp/api/func/company/company-search/findassociatedentity.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentity -->
# FindEntity

기업명, 주소, 사업자 등록 번호 등을 조건으로 주고 이에 해당하는 기업들의 목록을 검색할 수 있습니다.

### Function specification

```
FindEntity(entity_type, pattern, count=0, fields=None)
```

###

### Parameters

| Parameter    | Type                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/getentitysummary -->
# GetEntitySummary

검색한 Entity 에 대한 정보를 가져옵니다.

### Function specification

```
GetEntitySummary(Function)
```

### Examples

```
> GetEntitySummary(FindEntity("Financial", "삼성*"))

...

symbol	entity_name	symbol_nice	ceo	business_rid	company_rid	tel	fax	website	email	zipcode	address_land_lot	address_road_name	company_type_l1	company_type_l2	company_type_size	market_id	is_external_audit	conglomerate_id	industry_id	industry_name	fs_type	fiscal_year_end	business_area	date_founded	date_listed	is_alive	is_closed	status
KRX:000810	삼성화재	NICE:870056	최영무	2028145617	1101110005078	1588-5114	02-752-4875	www.samsungfire.com		137857	서울 서초구 서초2동 1321-20번지	서울 서초구 서초대로74길 14	1	511	1	1	TRUE	511	KRI:10K6512100	손해 보험업	DD	12	손해보험의 원수,재보험,운용자산의 투자활동	1952-01-26	1975-06-30	TRUE	N	00
KRX:001360	삼성제약	NICE:351199	김상재/김기호	2078100726	1101110032568	031-353-6681-4	031-353-6685	www.sspharm.co.kr		445937	경기 화성시 향남읍 상신리 905-3번지	경기 화성시 향남읍 제약공단4길 10	1	511	2	1	TRUE	CN4	KRI:10C2121000	완제 의약품 제조업	00	12	의약품(까스명수,쓸기담,에프킬라에어졸,액체우황청심원)  제조,도매	1954-12-07	1975-07-04	TRUE	N	00
KRX:005930	삼성전자	NICE:380725	김기남/김현석/고동진	1248100998	1301110006246	031-200-1114	031-200-1105	www.samsung.com/sec		443803	경기 수원시 영통구 매탄3동 416번지	경기 수원시 영통구 삼성로 129	1	511	1	1	TRUE	511	KRI:10C2642200	이동전화기 제조업	00	12	휴대폰,컴퓨터,네트워크시스템,핵심칩,반도체부품,디스플레이패널,가전제품,의료기기,프린터 제조	1969-01-13	1975-06-11	TRUE	N	00
KRX:006400	삼성SDI	NICE:380458	전영현	1248131282	1101110394174	031-8006-3100	031-8006-3968	www.samsungsdi.co.kr		446902	경기 용인시 기흥구 공세동 428-5번지	경기 용인시 기흥구 공세로 150-20	1	511	1	1	TRUE	511	KRI:10C2820200	축전지 제조업	00	12	2차전지,전자재료 제조,판매	1970-01-20	1979-02-27	TRUE	N	00
KRX:006660	삼성공조	NICE:381950	고호곤	6098102070	1942110000034	055-280-2733	055-282-0821	www.samsungcc.co.kr		642050	경남 창원시 성산구 내동 456-4번지	경남 창원시 성산구 연덕로 176	1	511	3	1	TRUE	519	KRI:10C3039100	자동차용 신품 조향장치 및 현가 장치 제조업	00	12	자동차부품(라디에터,오일쿨러,인터쿨러) 제조,판매	1954-05-24	1987-11-28	TRUE	N	00
KRX:009150	삼성전기	NICE:380733	경계현	1248100979	1301110001626	031-210-5114	031-210-6363	www.samsungsem.com		443803	경기 수원시 영통구 매탄3동 310번지	경기 수원시 영통구 매영로 150	1	511	1	1	TRUE	511	KRI:10C2629900	그 외 기타 전자부품 제조업	00	12	영상,음향,통신장비,모듈,다층인쇄회로기판,적층세라믹콘덴서,고주파필터,전압제어발진기,온도보상형수정발진기,칩인덕터,디지털위성방송수신기,광픽업,편향코일	1973-08-08	1979-02-27	TRUE	N	00
KRX:010140	삼성중공업	NICE:380180	정진택	1208152780	1101110168595	031-5171-7000	02-3458-6132	www.samsungshi.com		463400	경기 성남시 분당구 삼평동 615번지	경기 성남시 분당구 판교로227번길 23	1	511	1	1	TRUE	511	KRI:10C3111100	강선 건조업	00	12	선박(벌크선,원유운반선),철구조물,에너지플랜트 생산,판매/토목건축업	1974-08-05	1994-01-28	TRUE	N	00
KRX:016360	삼성증권	NICE:821616	장석훈	2028148588	1101110335649	02-2020-8000	02-2020-8316	www.samsungpop.com		137857	서울 서초구 서초2동 1320-10번지	서울 서초구 서초대로74길 11	1	511	1	1	TRUE	511	KRI:10K6612100	증권 중개업	BB	12	유가증권의 매매,위탁매매,인수주선	1982-10-19	1988-03-28	TRUE	N	00
KRX:018260	삼성에스디에스	NICE:820717	황성우	1108128774	1101110398556	02-6155-3114	02-3429-4270	www.samsungsds.com		138934	서울 송파구 잠실6동 7-13번지	서울 송파구 올림픽로35길 125	1	511	1	1	TRUE	511	KRI:10J6201000	컴퓨터 프로그래밍 서비스업	00	12	컴퓨터 프로그래밍,시스템 통합,관리/소프트웨어 개발/사무용기계장비 도매,컴퓨터임대	1985-05-01	2014-11-14	TRUE	N	00
KRX:028050	삼성엔지니어링	NICE:820040	최성안	1208156184	1101110240509	02-2053-3000	02-3458-4090	www.samsungengineering.co.kr		134090	서울 강동구 상일동 500번지	서울 강동구 상일로6길 26	1	511	1	1	TRUE	511	KRI:10M7212900	기타 엔지니어링 서비스업	00	12	산업설비,건물,구축물,토목시설의 설계,시공,공사감리	1978-10-19	1996-12-24	TRUE	N	00
KRX:028260	삼성물산	NICE:810053	고정석/오세철/한승환	2028145975	1101110015762	02-2145-5114	02-759-0919	www.samsungcnt.com		134090	서울 강동구 상일동 500번지	서울 강동구 상일로6길 26	1	511	1	1	TRUE	511	KRI:10G4674200	직물 도매업	00	12	패션,건설,레져,급식 및 식자재 유통,리조트,바이오	1963-12-23	2014-12-18	TRUE	N	00
KRX:029780	삼성카드	NICE:990345	김대환	2028145602	1101110346901	1588-8700	02-757-6056	www.samsungcard.com		100865	서울 중구 태평로2가 250번지	서울 중구 세종대로 67	1	511	1	1	TRUE	511	KRI:10K6491300	신용카드 및 할부금융업	II	12	신용카드업,상품신용판매,현금서비스,카드론,리스,기업대출,여행업무,통신판매	1983-03-24	2007-06-27	TRUE	N	00
KRX:032830	삼성생명	NICE:870021	전영묵	1048126688	1101110005953	1588-3114	02-2259-7045	www.samsunglife.com		137857	서울 서초구 서초2동 1320-10번지	서울 서초구 서초대로74길 11	1	511	1	1	TRUE	511	KRI:10K6511000	생명 보험업	CC	12	생명보험/부동산 임대	1957-04-07	2010-05-12	TRUE	N	00
KRX:068290	삼성출판사	NICE:201563	김진용	2148714287	1101112559411	02-3470-6800	02-568-9456	www.samsungbooks.com		137871	서울 서초구 서초3동 1516-2번지	서울 서초구 명달로 94	1	511	3	1	TRUE	LI2	KRI:10J5811300	일반 서적 출판업	00	12	서적 출판,인쇄,소매/부동산 임대	2002-07-03	2002-08-05	TRUE	N	00

...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyname -->
# FindEntityByName

### Function specification

```
FindEntityByName(entity_type, pattern, count=10000)
```

###

### Parameters

| Parameter    | Type                                  | Description                                            |
| ------------ | ------------------------------------- | ------------------------------------------------------ |
| entity\_type | string                                | 검색 대상이 되는 entity 의 타입을 명시합니다. 현재는 "Financial" 만 지원합니다. |
| pattern      | <p>string or</p><p>list of string</p> | 검색 하고자 하는 패턴을 지정합니다. 와일드카드 (\*) 사용이 가능합니다.             |
| count        | integer                               | 검색 결과에 포함되는 기업의 갯수를 제한합니다. 0 일 경우 전체 목록을 리턴합니다.        |

### Examples

```
> FindEntityByName("Financial", "삼성*")

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyshareholdername -->
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyindustryid -->
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentitybybusinessarea -->
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentitybyaddress -->
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findentityindocuments -->
# FindEntityInDocuments

문서내에서 특정 키워드가 언급된 기업을 검색합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/findassociatedentity -->
# FindAssociatedEntity

공시, 뉴스, 증권사리포트, IR 등 다양한 문서를 활용하여, 특정 주제와 관련된 기업을 검색합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company-search/searchfinancialstatementsauditopinion -->
# SearchFinancialStatementsAuditOpinion

감사의견을 바탕으로 기업을 검색합니다.

### Function specification

```
SearchFinancialStatementsAuditOpinion(query,date_from=None, date_to=None)
```

###

### Parameters

| Parameter           | Type   | Description        |
| ------------------- | ------ | ------------------ |
| query               | string | 검색 쿼리              |
| date\_from/date\_to | date   | 검색 범위 (YYYY-MM-DD) |

###

### Examples

```
SearchFinancialStatementsAuditOpinion("auditor:안진 and opinion:적정", date_from=2020-01-01, date_to=2022-12-31)
SearchFinancialStatementsAuditOpinion("안진 and not 적정", date_from=2020-01-01, date_to=2022-12-31)
SearchFinancialStatementsAuditOpinion("안진 and 존속의문", date_from=2020-01-01, date_to=2022-12-31)
SearchFinancialStatementsAuditOpinion("한정 or 거절", date_from=2020-01-01, date_to=2022-12-31)


```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'SearchFinancialStatementsAuditOpinion' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/company -->
# 기업 정보 조회

기업 별 세부 정보를 조회합니다.

기업의 분야별 매출, 사업 목표, 주요 주주, 임원 및 직원 정보 등을 조회할 수 있습니다. 다음과 같은 함수들이 사용 가능합니다.

{% content-ref url="/pages/-M273ktALOfhllKIlrnQ" %}
[GetCompanySummary](https://help.deepsearch.com/dp/api/func/company/company/getcompanysummary.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273eaPWKYqzbOYA0pX" %}
[GetCompanyHistory](https://help.deepsearch.com/dp/api/func/company/company/getcompanyhistory.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273g4XIGXPo07oUMjN" %}
[GetCompanyBusinessGoal](https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinessgoal.md)
{% endcontent-ref %}

{% content-ref url="/pages/7EWTCB1yF3Iu4Iiit57t" %}
[GetCompanyBusinessSummary](https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinesssummary.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273gq4yB88tMSH0o9M" %}
[GetCompanyRelatedFirms](https://help.deepsearch.com/dp/api/func/company/company/getcompanyrelatedfirms.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273ib56VeoJID0JrDV" %}
[GetCompanyDebts](https://help.deepsearch.com/dp/api/func/company/company/getcompanydebts.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273jeZKHXaIOLt5uno" %}
[GetCompanyDividends](https://help.deepsearch.com/dp/api/func/company/company/getcompanydividends.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273kH8anVCmxce7WCS" %}
[GetCompanyShareholders](https://help.deepsearch.com/dp/api/func/company/company/getcompanyshareholders.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273nn\_BV63FVQiWTQb" %}
[GetCompanyEmployees](https://help.deepsearch.com/dp/api/func/company/company/getcompanyemployees.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273oKQZN5nIc6b8oCS" %}
[GetCompanyExecutives](https://help.deepsearch.com/dp/api/func/company/company/getcompanyexecutives.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M273pKmr38y7JnywVaM" %}
[GetCompanyBranches](https://help.deepsearch.com/dp/api/func/company/company/getcompanybranches.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanysummary -->
# GetCompanySummary

기업이 개요 정보를 조회합니다.

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
| date\_established     | 설립일                                                                                                    |
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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyhistory -->
# GetCompanyHistory

회사의 연혁 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinessgoal -->
# GetCompanyBusinessGoal

기업의 사업목적을 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanybusinesssummary -->
# GetCompanyBusinessSummary

사업 개요 및 현황 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyrelatedfirms -->
# GetCompanyRelatedFirms

관계사 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyproductssales -->
# GetCompanyProductsSales

회사 제품별 매출 데이터를 조회합니다.

### Function specification

```
GetCompanyProductsSales(entities, date_from=None, date_to=None, annualize=False)
```

###

### Parameters

| Parameter  | Type                                  | Description                                                                                                              |
| ---------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| entities   | <p>string or</p><p>list of string</p> | <p>기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다.</p><p>ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] </p>        |
| date\_from | date                                  | <p>조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다.</p><p>ex) 2010-1-1</p>                                                |
| date\_to   | date                                  | <p>조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 전체 기간을 대상으로 합니다.</p><p>ex) 2010-12-31</p>                                              |
| annualize  | True / False                          | <p>annualize=False: 분기별로 주어진 데이터를 그대로 출력합니다.</p><p>annualize=True: 연도별로 데이터를 재구성하여 해당 연도에 포함된 분기 데이터의 값을 합산하여 출력합니다.</p> |

###

### Output Fields ( 단위 : 백만원 )

| Field            | Description                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| accounting\_type | <p>accounting\_type 은 아래 다섯 개의 값 중 하나를 가집니다.</p><p><br>'1' - 결산</p><p>'2' - 반기</p><p>'3' - 기타</p><p>'4' - 1/4분기</p><p>'5' - 3/4분기</p> |

### Examples

1. **삼성전자 전체 분야별 매출 데이터 조회**

```
> GetCompanyProductsSales(KRX:005930)

...
symbol	date	product_code	entity_name	accounting_type	capicity_quantity	capicity_sales	domestic_quantity	domestic_sales	exports_quantity	exports_sales	product_name	production_quantity	production_sales	quantity_unit	total_quantity	total_sales
KRX:005930	1996-06-30	01	삼성전자	2	7,240	1,931,100	0	1,329,582	0	1,307,712	가전부문	6,575	1,836,500	천대	0	2,637,294
KRX:005930	1996-06-30	02	삼성전자	2	1,189	969,600	0	792,081	0	254,016	정보통신부문	1,033	816,400	천대	0	1,046,097
KRX:005930	1996-06-30	03	삼성전자	2	2,263	3,051,100	0	124,348	0	3,490,443	반도체부문	1,797	2,985,700	천대	0	3,614,791
KRX:005930	1996-06-30	04	삼성전자	2	0	0	0	699,751	0	715,762	컴퓨터부문	0	0	천대	0	1,415,513
KRX:005930	1996-06-30	99	삼성전자	2	0	5,951,800	0	2,945,762	0	5,767,933	계	0	5,638,600		0	8,713,695
KRX:005930	1996-12-31	01	삼성전자	1	5,944	1,660,800	0	1,683,889	0	692,791	가전부문	4,809	1,481,400	천대	0	2,376,680
...

```

####

#### 2. 연도 별로 합산한 결과를 요청

```
> GetCompanyProductsSales(KRX:005930, annualize=True)
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanydebts -->
# GetCompanyDebts

차입금 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanydividends -->
# GetCompanyDividends

기업의 배당 내역을 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyshareholders -->
# GetCompanyShareholders

기업의 주주정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyemployees -->
# GetCompanyEmployees

종업원 현황 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanyexecutives -->
# GetCompanyExecutives

임원 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getcompanybranches -->
# GetCompanyBranches

지점 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/company/getfinancialstatementsauditopinion -->
# GetFinancialStatementsAuditOpinion

특정 기업의 감사 의견을 조회합니다.

### Function specification

```
GetFinancialStatementsAuditOpinion(entities, date_from, date_to)
```

### Parameters

| Parameter  | Type                                  | Description                                                                                         |
| ---------- | ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| entities   | <p>string or</p><p>list of string</p> | 기업의 심볼 혹은 이름을 입력합니다. 동시에 복수개의 기업을 호출할 수 있습니다. ex) 삼성전자, KRX:005930, \[KRX:005930,LG전자],\[삼성전자,LG전자] |
| date\_from | date                                  | 조회 시작 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기간을 대상으로 합니다. ex)2010-1-1                                      |
| date\_to   | date                                  | 조회 종료 시점을 설정합니다. 따로 지정이 없는 경우, 가장 최신 기간을 대상으로 합니다. ex)2010-12-31                                    |

### Query  Examples

```
2021 삼성전자 감사의견 
```

### Examples

```
> GetFinancialStatementsAuditOpinion([삼성전자, LG전자], date_from=2020-01-01, date_to=2022-12-31)

날짜 종목코드 기업명 auditor opinion opinion_code
2020-03-31T00:00:00	KRX:005930	삼성전자	안진회계법인	검토(적정-분기/반기만해당)	70
2020-06-30T00:00:00	KRX:005930	삼성전자	안진회계법인	검토(적정-분기/반기만해당)	70
2020-09-30T00:00:00	KRX:005930	삼성전자	안진회계법인	검토(적정-분기/반기만해당)	70
2020-12-31T00:00:00	KRX:005930	삼성전자	안진회계법인	적정	10

```

<!-- source: https://help.deepsearch.com/dp/api/func/company/financial -->
# 재무제표 조회

분기별 재무제표를 조회합니다.

기업의 분기별 재무제표 및 적용 회계 기준을 조회할 수 있습니다. 다음 함수들을 사용 가능합니다.

{% content-ref url="/pages/-M278hFh0MYEfxy2txDV" %}
[GetFinancialStatements](https://help.deepsearch.com/dp/api/func/company/financial/getfinancialstatements.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M278lpJ35Kmrmlme9An" %}
[GetAvailableFinancialStatements](https://help.deepsearch.com/dp/api/func/company/financial/getavailablefinancialstatements.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/financial/getfinancialstatements -->
# GetFinancialStatements

기업의 재무제표를 조회합니다.

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

{% file src="/files/uy75bev4jv1RU2FLYwo0" %}

<!-- repo-memo:start -->
> **[레포 검증 메모 2026-11-25 — 공식 문서 아님]**
> - 계정명(`name_ko`)은 `매출액`이 아니라 `수익`(report_id 12 / account_id 1000)입니다. 영업이익 `영업이익(손실)`(12/5000), 당기순이익 `총당기순이익`(12/8200), 지배주주 순이익 `당기순이익지배기업지분`(12/9061), `자산총계`·`부채총계`·`자본총계`(11/5000·8000·8900). report_id 11 = 재무상태표, 12 = 손익계산서, 19 = 재무비율. 삼성전자·삼성중공업 2024년으로 확인.
> - 한 회사 5년치 응답이 수백 KB입니다(삼성전자 연결 1년치 507행). 필요한 계정만 걸러 쓰세요(`skills/deepsearch/scripts/query_api.py --grep`).
> - 과거 연도 값은 원래 공시값과 재작성값이 섞여 있습니다(재작성된 회사·연도의 약 3/4이 재작성값). 근거: [research/restatement](../../research/restatement/README.md)
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/financial/getavailablefinancialstatements -->
# GetAvailableFinancialStatements

해당 기업이 발표하는 재무제표 종류를 조회합니다. ( 분기, 연간, IFRS/GAAP )

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure -->
# 공시 정보 조회

Dart 공시 사업보고서 항목들을 조회합니다.

Dart 에 공시되는 사업보고서 항목을 조회할 수 있습니다. 자본금 변화, 주요 주주 및 소액 주주, 임원과 직원 정보 등이 제공됩니다. 다음과 같은 함수들이 사용 가능합니다.

{% content-ref url="/pages/-M27EsE\_Gl-GOOhCadWD" %}
[GetDartCapitalChange](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartcapitalchange.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F8uOHuUuNB2SxPtW" %}
[GetDartDividends](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartdividends.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F8e4k98pt3k\_pG3i" %}
[GetDartShareRepurchase](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartsharerepurchase.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F8O\_ki8tzkxeEcIa" %}
[GetDartMajorityShareholders](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholders.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F88mAP1u6SFfkaCJ" %}
[GetDartMajorityShareholderChange](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholderchange.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F7uO2zLcIYL4Xf7G" %}
[GetDartMinorityShareholders](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartminorityshareholders.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F7dq4lt9QflJA078" %}
[GetDartExecutives](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartexecutives.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F7NQ-AYISPuW50r5" %}
[GetDartEmployees](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartemployees.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F74sivJpcVht0p2B" %}
[GetDartIndividualDirectorCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartindividualdirectorcompensation.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F6lB2UqsPSzeNJbN" %}
[GetDartOverallDirectorCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartoveralldirectorcompensation.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F6PXyFkOPVtruA4H" %}
[GetDartTopIndividualCompensation](https://help.deepsearch.com/dp/api/func/company/disclosure/getdarttopindividualcompensation.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27EtInBS1CZx9Cw2Nz" %}
[GetDartInvestmentInOthers](https://help.deepsearch.com/dp/api/func/company/disclosure/getdartinvestmentinothers.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartcapitalchange -->
# GetDartCapitalChange

정기보고서(사업, 분기, 반기보고서) 내에 증자(감자) 현황을 제공합니다.

### Function specification

```
GetDartCapitalChange(entities)
```

###

### Parameters

| Parameter | Type                     | Description |
| --------- | ------------------------ | ----------- |
| entities  | string or list of string | 기업명 or 종목코드 |

###

### Examples

```
> GetDartCapitalChange(동화약품)

...
symbol	date	entity_name	capital_change_type	stock_type	receipt_no	quantity	stock_face_value	stock_value
NICE:350605	2007-07-02	동화약품	주식분할	보통주	20130515000601	27,931,470	1,000	
NICE:350605	2009-07-02	동화약품	주식분할	보통주	20140328001203	27,931,470	1,000	

```

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetDartCapitalChange' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartdividends -->
# GetDartDividends

정기보고서(사업, 분기, 반기보고서) 내에 배당 내역을 조회합니다.

### Function specification

```
GetDartDividends(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

### Examples

```
> GetDartDividends(KRX:005930,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	data_type	stock_type	this_period	last_period	two_periods_ago
NICE:380725	2015-12-31	0	삼성전자	20160330003536	주당액면가액(원)	None	5,000	5,000	5,000
NICE:380725	2015-12-31	1	삼성전자	20160330003536	(연결)당기순이익(백만원)	None	18,694,628	23,082,499	29,821,215
NICE:380725	2015-12-31	2	삼성전자	20160330003536	주당순이익(원)	None	126,305	153,105	197,841
NICE:380725	2015-12-31	3	삼성전자	20160330003536	현금배당금총액(백만원)	None	3,068,737	2,999,972	2,156,969
NICE:380725	2015-12-31	10	삼성전자	20160330003536	주당 현금배당금(원)	보통주	21,000	20,000	14,300
NICE:380725	2015-12-31	11	삼성전자	20160330003536	주당 현금배당금(원)	우선주	21,050	20,050	14,350
NICE:380725	2016-03-31	0	삼성전자	20160516003174	주당액면가액(원)	None	5,000	5,000	5,000
NICE:380725	2016-03-31	1	삼성전자	20160516003174	(연결)당기순이익(백만원)	None	5,263,506	18,694,628	23,082,499
NICE:380725	2016-03-31	2	삼성전자	20160516003174	주당순이익(원)	None	36,356	126,305	153,105
NICE:380725	2016-03-31	3	삼성전자	20160516003174	현금배당금총액(백만원)	None		3,068,737	2,999,972
NICE:380725	2016-03-31	10	삼성전자	20160516003174	주당 현금배당금(원)	보통주		21,000	20,000
NICE:380725	2016-03-31	11	삼성전자	20160516003174	주당 현금배당금(원)	우선주		21,050	20,050
NICE:380725	2016-06-30	0	삼성전자	20160816001779	주당액면가액(원)	None	5,000	5,000	5,000
NICE:380725	2016-06-30	1	삼성전자	20160816001779	(연결)당기순이익(백만원)	None	11,089,684	18,694,628	23,082,499
NICE:380725	2016-06-30	2	삼성전자	20160816001779	주당순이익(원)	None	77,266	126,305	153,105
NICE:380725	2016-06-30	3	삼성전자	20160816001779	현금배당금총액(백만원)	None	141,539	3,068,737	2,999,972
NICE:380725	2016-06-30	10	삼성전자	20160816001779	주당 현금배당금(원)	보통주	1,000	21,000	20,000
NICE:380725	2016-06-30	11	삼성전자	20160816001779	주당 현금배당금(원)	우선주	1,000	21,050	20,050
NICE:380725	2016-09-30	0	삼성전자	20161114001491	주당액면가액(원)	None	5,000	5,000	5,000
NICE:380725	2016-09-30	1	삼성전자	20161114001491	(연결)당기순이익(백만원)	None	15,638,051	18,694,628	23,082,499
NICE:380725	2016-09-30	2	삼성전자	20161114001491	주당순이익(원)	None	108,728	126,305	153,105
NICE:380725	2016-09-30	3	삼성전자	20161114001491	현금배당금총액(백만원)	None	141,539	3,068,737	2,999,972
NICE:380725	2016-09-30	10	삼성전자	20161114001491	주당 현금배당금(원)	보통주	1,000	21,000	20,000
...

```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartsharerepurchase -->
# GetDartShareRepurchase

정기보고서(사업, 분기, 반기보고서) 내에 자기주식 취득 및 처분 현황을 제공합니다.

### Function specification

```
GetDartShareRepurchase(entities, date_from=None, date_to=None)
```

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartShareRepurchase(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	stock_type	method1	method2	method3	prior_quantity	repurchase_quantity	sales_quantity	retired_quantity	ending_quantity	note
NICE:350605	2013-03-31	6	동화약품	20130515000601	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2013-03-31	8	동화약품	20130515000601	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2013-06-30	6	동화약품	20130814000810	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2013-06-30	8	동화약품	20130814000810	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2013-09-30	6	동화약품	20131114001198	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2013-09-30	8	동화약품	20131114001198	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2013-12-31	6	동화약품	20140328001203	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2013-12-31	8	동화약품	20140328001203	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2014-03-31	6	동화약품	20140515000750	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2014-03-31	8	동화약품	20140515000750	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2014-06-30	6	동화약품	20140814000769	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2014-06-30	8	동화약품	20140814000769	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2014-09-30	6	동화약품	20141114001023	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2014-09-30	8	동화약품	20141114001023	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2014-12-31	6	동화약품	20150331002176	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2014-12-31	8	동화약품	20150331002176	보통주	총계	총계	총계	240			None	240	-
NICE:350605	2015-03-31	0	동화약품	20150515001111	보통주	배당가능이익범위 이내 취득	직접취득	장내직접취득		169,717		None	169,717	-
NICE:350605	2015-03-31	6	동화약품	20150515001111	보통주	기타취득	기타취득	기타취득	240			None	240	-
NICE:350605	2015-03-31	8	동화약품	20150515001111	보통주	총계	총계	총계	240	169,717		None	169,957	-
NICE:350605	2015-03-31	15	동화약품	20150515001111	보통주	배당가능이익범위 이내 취득	직접취득	소계		169,717		None	169,717	-
NICE:350605	2015-06-30	0	동화약품	20150817000659	보통주	배당가능이익범위 이내 취득	직접취득	장내직접취득		320,000	53,500	None	266,500	-
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholders -->
# GetDartMajorityShareholders

정기보고서(사업, 분기, 반기보고서) 내에 최대주주 현황을 제공합니다.

### Function specification

```
GetDartMajorityShareholders(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartMajorityShareholders(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	stock_type	name	relation	prior_shares	prior_percentage	ending_shares	ending_percentage	note
NICE:350605	2013-03-31	0	동화약품	20130515000601	보통주	윤도준	본인	1,433,085	5.13	1,433,085	5.13	-
NICE:350605	2013-03-31	1	동화약품	20130515000601	보통주	윤평준	친인척	30,790	0.11	30,790	0.11	-
NICE:350605	2013-03-31	2	동화약품	20130515000601	보통주	윤현경	친인척	15,630	0.06	15,630	0.06	-
NICE:350605	2013-03-31	3	동화약품	20130515000601	보통주	윤인호	친인척	22,425	0.08	22,425	0.08	-
NICE:350605	2013-03-31	4	동화약품	20130515000601	보통주	윤현선	친인척	15,630	0.06	15,630	0.06	-
NICE:350605	2013-03-31	5	동화약품	20130515000601	보통주	윤현진	친인척	15,630	0.06	15,630	0.06	-
NICE:350605	2013-03-31	6	동화약품	20130515000601	보통주	윤현호	친인척	22,425	0.08	22,425	0.08	-
NICE:350605	2013-03-31	7	동화약품	20130515000601	보통주	김진선	친인척	7,560	0.03	7,560	0.03	-
NICE:350605	2013-03-31	8	동화약품	20130515000601	보통주	김영옥	친인척	31,060	0.11	31,060	0.11	-
NICE:350605	2013-03-31	9	동화약품	20130515000601	보통주	박제화	임원	24,000	0.09	24,000	0.09	-
NICE:350605	2013-03-31	10	동화약품	20130515000601	보통주	원유식	임원	5,520	0.02	5,520	0.02	-
NICE:350605	2013-03-31	11	동화약품	20130515000601	보통주	강일구	친인척	223,830	0.80	223,830	0.80	-
NICE:350605	2013-03-31	12	동화약품	20130515000601	보통주	이진수	임원	2,890	0.01	2,890	0.01	-
NICE:350605	2013-03-31	13	동화약품	20130515000601	보통주	조진성	임원	3,040	0.01	3,040	0.01	-
NICE:350605	2013-03-31	14	동화약품	20130515000601	보통주	이재호	임원	410	0.00	410	0.00	-
NICE:350605	2013-03-31	15	동화약품	20130515000601	보통주	이종석	임원	2,950	0.01	2,950	0.01	-
NICE:350605	2013-03-31	16	동화약품	20130515000601	보통주	임문정	임원	1,770	0.01	1,770	0.01	-
NICE:350605	2013-03-31	17	동화약품	20130515000601	보통주	오희수	임원	1,770	0.01	1,770	0.01	-
NICE:350605	2013-03-31	18	동화약품	20130515000601	보통주	이용기	임원	1,770	0.01	1,770	0.01	-
NICE:350605	2013-03-31	19	동화약품	20130515000601	보통주	김창현	임원	2,850	0.01	2,850	0.01	-
NICE:350605	2013-03-31	20	동화약품	20130515000601	보통주	이재혁	임원	1,710	0.00	1,710	0.00	-
NICE:350605	2013-03-31	21	동화약품	20130515000601	보통주	동화개발	계열사	215,840	0.77	215,840	0.77	-
NICE:350605	2013-03-31	22	동화약품	20130515000601	보통주	윤금준	친인척	62,600	0.22	62,600	0.22	-
NICE:350605	2013-03-31	23	동화약품	20130515000601	보통주	동화지엔피	계열사	4,252,370	15.23	4,252,370	15.23	-
NICE:350605	2013-03-31	24	동화약품	20130515000601	보통주	(재)가송재단	재단	1,685,425	6.03	1,685,425	6.03	-
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartmajorityshareholderchange -->
# GetDartMajorityShareholderChange

정기보고서(사업, 분기, 반기보고서) 내에 최대주주 변동 현황을 제공합니다.

### Function specification

```
GetDartMajorityShareholderChange(entities)
```

###

### Parameters

| Parameter    | Type                     | Description |
| ------------ | ------------------------ | ----------- |
| entity\_type | string or list of string | 종목명 or 종목코드 |

###

### Examples

```
> GetDartMajorityShareholderChange(KRX:000020)
...
symbol	date	entity_name	shareholder_name	receipt_no	shares_number	shares_percentage	reason
NICE:350605	2010-12-22	동화약품	윤도준 외 24명	20150515001111	9,164,930	32.80	-
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartminorityshareholders -->
# GetDartMinorityShareholders

정기보고서(사업, 분기, 반기보고서) 내에 소액주주현황을 제공합니다.

### Function specification

```
GetDartMinorityShareholders(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartMinorityShareholders(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	shareholder_type	shareholder_cnt	shareholder_ratio	shares_cnt	shares_ratio
NICE:350605	2013-03-31	0	동화약품	20130515000601	소액주주	5,351	99.28	14,115,367	50.54
NICE:350605	2013-06-30	0	동화약품	20130814000810	소액주주	5,351	99.28	14,115,367	50.54
NICE:350605	2013-09-30	0	동화약품	20131114001198	소액주주	5,082	99.75	14,667,275	52.50
NICE:350605	2013-12-31	0	동화약품	20140328001203	소액주주	5,257	99.80	15,132,258	54.20
NICE:350605	2014-03-31	0	동화약품	20140515000750	소액주주	5,257	99.80	15,132,258	54.20
NICE:350605	2014-06-30	0	동화약품	20140814000769	소액주주	5,257	99.80	15,132,258	54.20
NICE:350605	2014-09-30	0	동화약품	20141114001023	소액주주	5,257	99.80	15,132,258	54.20
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartexecutives -->
# GetDartExecutives

정기보고서(사업, 분기, 반기보고서) 내에 임원현황을 제공합니다.

### Function specification

```
GetDartExecutives(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartExecutives(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	name	gender	birth_ym	title	executive_status	occupation_status	job_description	past_experience	relation	tenure_duration	tenure_end
NICE:350605	2013-03-31	0	동화약품	20130515000601	윤도준		1952년 02월	대표이사회장	등기임원	상근	총괄	"-경희대 의학박사(1988)
-경희대 의과대 주임교수 및 정신과과장(2003)
-동화약품 부회장(2005)
-동화약품 회장(2008)"	-	8년 1개월	2014년 03월 18일
NICE:350605	2013-03-31	1	동화약품	20130515000601	원유식		1963년 06월	이사	미등기임원	상근	생산지원	"-한양대 산업공학(1986)
-동화약품 건설본부 부장 "	-	24년	-
NICE:350605	2013-03-31	2	동화약품	20130515000601	이진수		1963년 10월	이사	미등기임원	상근	연구	"-서강대 화학박사(1999)
-동화약품 중앙연구소 부장 "	-	25년 3개월	-
NICE:350605	2013-03-31	3	동화약품	20130515000601	이종석		1959년 01월	이사	미등기임원	상근	총무	"-국민대학교 행정학(1986)
-동화약품 구매부 부장 "	-	26년 10개월	-
NICE:350605	2013-03-31	4	동화약품	20130515000601	이용기		1965년 03월	이사	미등기임원	상근	영업	"-국민대학교 화학교육과(1989)
-GSK 클리닉비지니스 부장(1997)
-한올제약 이사 (2008)"	-	3년 7개월	-
NICE:350605	2013-03-31	5	동화약품	20130515000601	김창현		1967년 02월	이사	미등기임원	상근	재경	"-고려대학교 경영대학원(2003)
-오비맥주(주) 경리팀장(2006) 
-(주)두산 FA팀 부장(2008)"	-	2년 11개월	-
NICE:350605	2013-03-31	6	동화약품	20130515000601	오희수		1968년 07월	이사	미등기임원	상근	영업	"-아주대학교 경영학과(1993)
-동화약품 약국마케팅부장
-동화약품 OTC영업기획팀장"	-	20년 4개월	-
NICE:350605	2013-03-31	7	동화약품	20130515000601	이재혁		1969년 12월	이사	미등기임원	상근	전략기획	"-美 애크런주립대 행정학사(1994)
-美 애크런주립대 행정학 석사(1997)
-美 조지타운대 정책대학원 석사(1997)
-딜로이트투쉬코리아 메니저(2002)
-삼정KPMG 회계법인 부장(2005)
-삼정KPMG FAS1본부 부장(2006)
-삼정KPMG CF본부 헬스케어팀 이사(2007)"	-	2년 10개월	-
NICE:350605	2013-03-31	8	동화약품	20130515000601	임문정		1963년 01월	이사	미등기임원	상근	개발	"-성균관대학교 약학박사(2002)
-동화약품 중앙연구소 부장"	-	24년 1개월	-
NICE:350605	2013-03-31	9	동화약품	20130515000601	윤현경		1980년 01월	이사	미등기임원	상근	BD	"-경희대 경영학사(2003)
-동화약품 광고홍보실/BD실 차장"	-	5년 1개월	-
NICE:350605	2013-03-31	10	동화약품	20130515000601	이설		1968년 03월	이사	미등기임원	상근	인사	"-서강대 경제학과(1994)
-연세대 MBA(2013)
-한국지엠㈜ 평가보상팀 부장(2008)
-한국지엠㈜ 인재관리시스템 부장(2012)"	-	2개월	-
NICE:350605	2013-03-31	11	동화약품	20130515000601	박제화		1951년 07월	대표이사부회장	등기임원	상근	총괄	"-고려대 경영대학원(1984)
-대만/홍콩 얀센 총괄사장(2007)
-중국시안 얀센 대표이사사장(2008)"	-	1년 11개월	2015년 03월 16일
NICE:350605	2013-03-31	12	동화약품	20130515000601	김문철		1959년 07월	사외이사	등기임원	비상근	사외이사	"-美 일리노이대 회계학박사(1993)
-경희대 경영대학 교수(1994)"	-	3년	2016년 04월 10일
NICE:350605	2013-03-31	13	동화약품	20130515000601	심우영		1958년 01월	사외이사	등기임원	비상근	사외이사	"-경희대 의학박사(1992) 
-경희대 의과대학 교수(2002)"	-	4년 10개월	2014년 03월 18일
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartemployees -->
# GetDartEmployees

정기보고서(사업, 분기, 반기보고서) 내에 직원현황을 제공합니다.

### Function specification

```
GetDartEmployees(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartEmployees(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	business_area	gender	prior_permanent_employee_no	prior_contract_employee_no	prior_other_employee_no	permanent_employee_no	permanent_parttime_employee_no	contract_employee_no	contract_parttime_employee_no	total_employee_no	average_tenure_duration	total_annual_salary	average_employee_salary	note
NICE:350605	2013-03-31	0	동화약품	20130515000601	의약품	남	580	17						597	9년 3개월	8,686,642,000	14,550,000	-
NICE:350605	2013-03-31	1	동화약품	20130515000601	"	여	188	4						192	6년 5개월	2,071,725,000	10,790,000	-
NICE:350605	2013-06-30	0	동화약품	20130814000810	의약품	남	571	13						584	9년 6개월	15,531,484,000	26,595,000	-
NICE:350605	2013-06-30	1	동화약품	20130814000810	"	여	178	4						182	6년 9개월	3,645,482,000	20,030,000	-
NICE:350605	2013-09-30	0	동화약품	20131114001198	의약품	남	562	13	0					575	9년 9개월	22,556,086,000	39,228,000	-
NICE:350605	2013-09-30	1	동화약품	20131114001198	"	여	174	4	0					178	7년 1개월	5,314,953,000	29,859,000	-
NICE:350605	2013-12-31	0	동화약품	20140328001203	의약품	남	546	9	0					555	10년 1개월	29,045,718,000	52,335,000	-
NICE:350605	2013-12-31	1	동화약품	20140328001203	"	여	172	1	0					173	7년 4개월	7,000,203,000	40,464,000	-
NICE:350605	2014-03-31	0	동화약품	20140515000750	의약품	남	531	8						539	10년 3개월	8,147,797,000	15,117,000	-
NICE:350605	2014-03-31	1	동화약품	20140515000750	"	여	172	1						173	7년 6개월	1,896,874,000	10,965,000	-
NICE:350605	2014-06-30	0	동화약품	20140814000769	의약품	남	538	9						547	10년 1개월	15,436,361,000	28,220,000	-
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartindividualdirectorcompensation -->
# GetDartIndividualDirectorCompensation

정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사의 개인별 보수 현황(5억 이상)을 제공합니다.

### Function specification

```
GetDartIndividualDirectorCompensation(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartIndividualDirectorCompensation(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	name	title	total_compensation	extra_compensation
NICE:350605	2016-12-31	0	동화약품	20170405001320	윤도준	대표이사 회장	553,000,000	None
NICE:350605	2016-12-31	1	동화약품	20170405001320	오희수	상무이사	600,000,000	None
NICE:350605	2017-12-31	0	동화약품	20180618000261	윤도준	대표이사 회장	646,000,000	None
NICE:350605	2018-12-31	0	동화약품	20190401001980	윤도준	대표이사 회장	766,000,000	None
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartoveralldirectorcompensation -->
# GetDartOverallDirectorCompensation

정기보고서(사업, 분기, 반기보고서) 내에 이사ㆍ감사 전체의 보수현황을 제공합니다.

### Function specification

```
GetDartOverallDirectorCompensation(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartOverallDirectorCompensation(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	count	total_compensation	average_compensation	note
NICE:350605	2013-03-31	0	동화약품	20130515000601	5	204,633,000	40,927,000	-
NICE:350605	2013-06-30	0	동화약품	20130814000810	5	409,266,000	81,853,000	-
NICE:350605	2013-09-30	0	동화약품	20131114001198	5	625,781,000	125,156,000	-
NICE:350605	2013-12-31	0	동화약품	20140328001203	5	849,633,000	169,927,000	-
NICE:350605	2014-03-31	0	동화약품	20140515000750	7	194,161,000	27,737,000	-
NICE:350605	2014-06-30	0	동화약품	20140814000769	7	454,987,000	64,998,000	-
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdarttopindividualcompensation -->
# GetDartTopIndividualCompensation

정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다.

### Function specification

```
GetDartTopIndividualCompensation(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartTopIndividualCompensation(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	name	title	total_compensation	extra_compensation
NICE:350605	2019-12-31	0	동화약품	20200330001229	윤도준	회장	899,000,000	None
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/disclosure/getdartinvestmentinothers -->
# GetDartInvestmentInOthers

정기보고서(사업, 분기, 반기보고서) 내에 타법인 출자현황을 제공합니다.

### Function specification

```
GetDartInvestmentInOthers(entities, date_from=None, date_to=None)
```

###

### Parameters

| Parameter             | Type                     | Description        |
| --------------------- | ------------------------ | ------------------ |
| entity\_type          | string or list of string | 종목명 or 종목코드        |
| date\_from / date\_to | date                     | 조회 기간 (YYYY-MM-DD) |

###

### Examples

```
> GetDartInvestmentInOthers(KRX:000020,date_from=2000-01-01, date_to=2019-12-31)
...
symbol	date	seq	entity_name	receipt_no	target_name	first_acquisition_date	investment_purpose	first_acquisition_price	prior_balance_quantity	prior_balance_percentage	prior_balance_price	diff_acquisition_quantity	diff_acquisition_price	diff_capital_gain	ending_balance_quantity	ending_balance_percentage	ending_balance_price	last_fyear_total_asset	last_fyear_netincome
NICE:350605	2013-03-31	0	동화약품	20130515000601	흥진정공(주) (비상장)	None	경영권확보	209,000,000	14,200	29.58	2,741,000,000			99,000,000	14,200	29.58	2,840,000,000	9,953,000,000	1,337,000,000
NICE:350605	2013-03-31	1	동화약품	20130515000601	동화지앤피(주) (비상장)	None	경영권확보	1,314,000,000	118,878	9.91	4,732,000,000			37,000,000	118,878	9.91	4,769,000,000	52,325,000,000	1,131,000,000
NICE:350605	2013-03-31	2	동화약품	20130515000601	(주)동화개발 (비상장)	1996-03-31	경영권확보	1,042,000,000	67,627	33.81	1,553,000,000			-8,000,000	67,627	33.81	1,545,000,000	4,935,000,000	-89,000,000
NICE:350605	2013-03-31	3	동화약품	20130515000601	부국티엔씨(주) (비상장)	2004-02-26	"단순
투자"	960,000,000	64,000	12.31	960,000,000				64,000	12.31	960,000,000		
NICE:350605	2013-03-31	4	동화약품	20130515000601	태양당인쇄(주) (비상장)	2005-11-09	"단순
투자"	1,248,000,000	2,000	10.00	1,248,000,000				2,000	10.00	1,248,000,000		
NICE:350605	2013-03-31	5	동화약품	20130515000601	충주기업도시(주) (비상장)	2007-04-01	"단순
투자"	2,000,000,000	400,000	5.00	2,000,000,000				400,000	5.00	2,000,000,000		
NICE:350605	2013-03-31	6	동화약품	20130515000601	한국노바티스(주) (비상장)	1984-09-01	"단순
투자"	325,000,000	32,500	1.76	325,000,000				32,500	1.76	325,000,000		
NICE:350605	2013-03-31	7	동화약품	20130515000601	(주)제넥신 (상장)	2000-03-31	"단순
투자"	89,000,000	32,536	0.52	586,000,000			-11,000,000	32,536	0.52	575,000,000	63,401,000,000	-2,237,000,000
NICE:350605	2013-03-31	8	동화약품	20130515000601	합계	None	-				14,145,000,000			117,000,000			14,262,000,000		
...
```

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus -->
# 컨센서스 정보 조회

증권사 애널리스트 컨센서스 정보를 조회합니다.

증권사 애널리스트들이 주요 상장사를 대상으로 발표하는 주가 및 실적 예상치의 컨센서스를 조회할 수 있습니다. 아래 함수들이 사용 가능합니다.

{% content-ref url="/pages/-M27Eu00BYDgmVlc464D" %}
[GetConsensusInstitutionList](https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusinstitutionlist.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F-7HhUwQmboyzU4Q" %}
[GetConsensusAnalystList](https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusanalystlist.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F0hL0s-c37YdsVOJ" %}
[SearchAnalystReports](https://help.deepsearch.com/dp/api/func/company/consensus/searchanalystreports.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F1MOrlSyfihxy9Wv" %}
[SearchTargetPrices](https://help.deepsearch.com/dp/api/func/company/consensus/searchtargetprices.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27F28\_VBeGZPTys6a9" %}
[SearchFirmFundamentalsForecasts](https://help.deepsearch.com/dp/api/func/company/consensus/searchfirmfundamentalsforecasts.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusinstitutionlist -->
# GetConsensusInstitutionList

컨센서스를 발표하는 기관 리스트를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus/getconsensusanalystlist -->
# GetConsensusAnalystList

특정 기관의 애널리스트 정보를 조회합니다.

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

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** `inst_code`는 `GetConsensusInstitutionList()` 결과의 기관 코드입니다. 예: `GetConsensusAnalystList("058585")` → 63행.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus/searchanalystreports -->
# SearchAnalystReports

특정 기업에 대한 애널리스트 리포트를 조회합니다.

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

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** `SearchAnalystReports(삼성전자)`는 `KernelError: Internal Server Error`. `SearchAnalystReports(KRX:005930, date_from=2025-01-01, date_to=2025-03-31)`는 오류 없이 0행입니다. 애널리스트 보고서는 `DocumentSearch(["research"],["company"],"securities.symbol:KRX:005930",...)`로 찾으세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus/searchtargetprices -->
# SearchTargetPrices

특정 종목에 대한 목표 주가를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/consensus/searchfirmfundamentalsforecasts -->
# SearchFirmFundamentalsForecasts

특정 종목에 대한 예상 실적을 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/issue-company -->
# 이슈 기업 목록 조회

주요 주주가 바뀌었거나 애널리스트 컨센서스가 변화한 기업들의 목록을 추출합니다. 다음과 같은 함수들이 사용 가능합니다.

{% content-ref url="/pages/-M275ffdN-moPAxpMYAA" %}
[GetCompanyShareholderChanges](https://help.deepsearch.com/dp/api/func/company/issue-company/getcompanyshareholderchanges.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27EzKG-5yAdepEwjqA" %}
[GetTargetPriceConsensusChange](https://help.deepsearch.com/dp/api/func/company/issue-company/gettargetpriceconsensuschange.md)
{% endcontent-ref %}

{% content-ref url="/pages/-M27ExW9DOm7hsnwyzfu" %}
[GetFundamentalsConsensusChange](https://help.deepsearch.com/dp/api/func/company/issue-company/getfundamentalsconsensuschange.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/issue-company/getcompanyshareholderchanges -->
# GetCompanyShareholderChanges

최대 주주의 지분율이 변경된 기업 리스트를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/issue-company/gettargetpriceconsensuschange -->
# GetTargetPriceConsensusChange

증권사 목표주가 변화 내역을 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/issue-company/getfundamentalsconsensuschange -->
# GetFundamentalsConsensusChange

증권사 컨센서스 실적 추정치 변화 내역을 조회합니다.

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

<!-- repo-memo:start -->
> **[레포 검증 2026-11-25 — 공식 문서 아님]** 이 레포의 API 키로 예시를 호출하면 `NameError: UFunction 'GetFundamentalsConsensusChange' is not defined`입니다. 현재 구독으로는 쓸 수 없는 함수로 보고, 분석에 쓰지 마세요.
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/undefined -->
# 주가 정보 조회

다음과 같은 함수를 사용할 수 있습니다.

{% content-ref url="/pages/-MB46YV7BfEFfRwLhTvp" %}
[GetStockSymbols](https://help.deepsearch.com/dp/api/func/company/undefined/getstocksymbols.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MB46anBT3ox9wX3qduW" %}
[GetStockPrices](https://help.deepsearch.com/dp/api/func/company/undefined/getstockprices.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MB46eDxH0BvesMZj4sU" %}
[GetMarketIndexSymbols](https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexsymbols.md)
{% endcontent-ref %}

{% content-ref url="/pages/-MB46h-JiHWUppMaDAlB" %}
[GetMarketIndexes](https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexes.md)
{% endcontent-ref %}

<!-- source: https://help.deepsearch.com/dp/api/func/company/undefined/getstocksymbols -->
# GetStockSymbols

종목 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/undefined/getstockprices -->
# GetStockPrices

종목의 현재 가격 및 거래량 정보를 조회합니다.

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

<!-- repo-memo:start -->
> **[레포 검증 메모 2026-11-25 — 공식 문서 아님]** 근거: [research/price_adjustment](../../research/price_adjustment/README.md)
> - 반환 컬럼: `open, high, low, close, volume, value, change, change_rate, shares_outstanding, market_cap, trading_halted`
> - **가격(open/high/low/close)은 수정주가뿐**입니다. 액면분할·무상증자·유상증자로 소급 수정되고 배당은 반영하지 않습니다. 원주가를 고르는 파라미터나 컬럼은 없습니다. 위 4개 외 파라미터(`adjusted=` 등)나 없는 컬럼 이름을 넣으면 400 에러입니다.
> - **volume, value, shares_outstanding, market_cap은 수정되지 않은 당일 값**입니다. 원주가 종가 = `market_cap ÷ shares_outstanding`
> - `entities`를 생략하면 전 종목(ETF 포함)의 기간 마지막 거래일 하루치가 옵니다. 목록(`[KRX:005930, KRX:000660]`)도 됩니다. `change_rate`는 비율(-0.0876 = -8.76%)입니다(지수 `GetMarketIndexes`는 퍼센트).
<!-- repo-memo:end -->

<!-- source: https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexsymbols -->
# GetMarketIndexSymbols

지수에 대한 정보를 조회합니다.

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

<!-- source: https://help.deepsearch.com/dp/api/func/company/undefined/getmarketindexes -->
# GetMarketIndexes

현재 지수의 가격 및 거래량 등의 정보를 조회합니다.

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
