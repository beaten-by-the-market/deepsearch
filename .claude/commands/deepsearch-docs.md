# DeepSearch 문서 검색

한국 뉴스, 증권사 리포트, 공시/IR, 특허 문서를 검색하고 분석합니다.
KRX 업무(조회공시, 주가급변 원인분석, 시장 모니터링)를 위한 전문 가이드를 포함합니다.

## 사용자 요청

$ARGUMENTS

## API 키

`.env` 파일에서 `API_KEY`를 읽어 사용하세요:
```bash
source .env && echo $API_KEY
```

## 지원 기능

1. **DocumentSearch** - 문서 검색 (뉴스, 리서치, 공시, 특허)
2. **DocumentTrends** - 키워드 기반 문서 트렌드 분석
3. **DocumentAggregation** - 문서 집계 (가장 많이 언급된 기업 등)
4. **GetSentimentScore** - 감성(긍부정) 점수 추이
5. **SimilarKeywords** - 유사 키워드 탐색 (Word2Vec)
6. **SearchTrendingTopics** - 실시간 트렌딩 토픽
7. **SearchHistoricalTopics** - 과거 토픽 검색

## Instructions

### Step 1: 사용자 의도 파악

**카테고리 매핑:**
- 뉴스 → `["news"]`
- 증권사 리포트/리서치 → `["research"]`
- 공시/IR → `["company"]`
- 특허 → `["patent"]`
- 미지정 시 → `["news"]` 기본

**섹션 매핑:**
- news: economy, tech, society, politics, culture, world, entertainment, opinion
- research: market, strategy, company, industry, economy, bond
- company: ir, disclosure
- 미지정 시 → `[]` (전체)

**필드 쿼리 변환:**
- 특정 기업 → `securities.name:기업명`
- 종목코드 → `securities.symbol:코드`
- 시장 필터 → `securities.market:KOSPI`
- 긍정/부정 뉴스 → `polarity.name:긍정` 또는 `부정`
- ESG → `esg.category.name:환경` (또는 사회, 지배구조)
- ESG 감성 → `esg.polarity.name:긍정`
- 제목 검색 → `title:키워드`
- 본문 검색 → `content:키워드`
- 언론사 → `publisher.raw:('매일경제' or '한국경제')`
- 언급 인물 → `named_entities.entities.person.name:인물명`

**날짜:**
- 날짜 지정 시 → `date_from=YYYYMMDD, date_to=YYYYMMDD`
- Boolean: `and`, `or`, `!`(NOT), `()` 그룹핑
- **중요:** DocumentSearch 기간은 최대 1년 이내로 제한됩니다.

**KRX 업무 활용:**
- 조회공시 후보 → `title:(인수 or 합병 or 매각) and securities.market:(KOSPI or KOSDAQ)`
- 부정 뉴스 모니터링 → `securities.market:KOSPI and polarity.name:부정`
- ESG 지배구조 이슈 → `esg.category.name:지배구조 and esg.polarity.name:부정`
- 불공정거래 뉴스 → `title:(시세조종 or 불공정거래 or 내부자거래)`
- 대량보유/주주변동 → `title:(대량보유 or 지분 or 최대주주)`
- 뉴스 언급 상위 종목 → DocumentAggregation + `securities.name:20`
- 기업 감성 급변 → GetSentimentScore + `interval="1d"`

### Step 2: 쿼리 생성

**DocumentSearch:**
```
DocumentSearch(["카테고리"],["섹션"],"쿼리",count=100,page=1,date_from=YYYYMMDD,date_to=YYYYMMDD)
```

**DocumentTrends:**
```
DocumentTrends(["카테고리"],["섹션"],"쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
```
interval: 1y, 1M, 1w, 1d, 1h, 1m

**DocumentAggregation:**
```
DocumentAggregation(["카테고리"],["섹션"],"쿼리","groupby필드:N")
```
예: `"named_entities.entities.company.name:100"` → 가장 많이 언급된 기업 100개

**GetSentimentScore:**
```
GetSentimentScore("쿼리",interval="1d",date_from=YYYYMMDD,date_to=YYYYMMDD)
```

**SimilarKeywords:**
```
SimilarKeywords("키워드",max_count=10)
```

### Step 3: 실행

```bash
python deepsearch-docs/scripts/query_api.py "$API_KEY" "쿼리"
```

### Step 4: 결과 포맷팅

문서 검색 결과:
```
## 검색 결과 (총 N건)

### 1. [제목]
- 출처: [언론사] | 날짜: YYYY-MM-DD
- 감성: 긍정/부정/중립 | ESG: 환경/사회/지배구조
- 관련종목: 기업명(종목코드)
- 내용: [요약]
- 원문: [URL]
```

## 이 스킬이 커버하지 않는 DeepSearch 기능

이 스킬은 **문서 검색 & 트렌드** 전문입니다. 아래 기능이 필요하면 다른 명령어나 DeepSearch API 문서를 안내하세요.

**다른 명령어로 처리 가능:**
| 요청 유형 | 안내할 명령어 |
|-----------|-------------|
| 기업 재무제표, 주가, 배당, 주주/임원 정보 | `/project:deepsearch-finance` |
| 재무 조건 스크리닝, 투자 전략, 분석 함수 | `/project:deepsearch-analytics` |

**DeepSearch API에는 있으나 현재 미포함:**
| API 함수 | 설명 | 용도 예시 |
|---------|------|----------|
| FindEntityInDocuments | 문서에서 언급된 기업 추출 | "이 뉴스에 언급된 기업 목록" |
| GetTrendingTopic | 트렌딩 토픽 상세 조회 | "현재 트렌딩 토픽의 관련 문서/기업" |
| GetHistoricalTopic | 과거 토픽 상세 조회 | "과거 특정 이슈의 관련 문서" |
| GetAggregateIndustryInfo | 산업별 집계 정보 | "반도체 산업 전체 현황" |
| SearchAnalystReports | 애널리스트 리포트 검색 | "특정 애널리스트의 리포트 목록" |

**fallback 응답 템플릿:**
> "이 요청은 현재 문서검색 기능의 범위 밖입니다. 하지만 DeepSearch API의 `{함수명}` 기능으로 처리할 수 있습니다.
> - 관련 API 문서: docs/DEEPSEARCH_API_MASTER.md
> - 추가 기능이 필요하시면 해당 기능을 포함한 스킬을 생성할 수 있습니다."

## 참조 파일

쿼리 작성 시 아래 파일을 참조하세요:
- 상세 레퍼런스: `deepsearch-docs/references/doc_search_guide.md`
- 검증된 사용 사례: `deepsearch-docs/references/verified_examples.md`
- KRX 업무 가이드: `deepsearch-docs/references/krx_monitoring_guide.md`
