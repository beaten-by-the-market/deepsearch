# 문서 검색 API 레퍼런스

## API 기본 정보
- Base URL: `https://api.deepsearch.com/v1/compute?input={쿼리}`
- 인증: `Authorization: Basic {인증키}`

## DocumentSearch

```python
DocumentSearch(category, section, query, count=10, page=None,
               date_from=None, date_to=None, summary=True,
               clustering=False, uniquify=True, highlight=False, fields=None)
```

### 카테고리 / 섹션

| Category | Section |
|----------|---------|
| `["news"]` | politics, economy, society, culture, world, tech, entertainment, opinion |
| `["research"]` | market, strategy, company, industry, economy, bond |
| `["company"]` | ir, disclosure |
| `["patent"]` | patent |

### 검색 필드

| 필드 | 문법 | 예시 |
|------|------|------|
| 제목 | `title:키워드` | `title:반도체` |
| 본문 | `content:키워드` | `content:수출` |
| 언론사 | `publisher.raw:('A' or 'B')` | `publisher.raw:('매일경제' or '한국경제')` |
| 관련종목 | `securities.name:기업명` | `securities.name:삼성전자` |
| 종목코드 | `securities.symbol:코드` | `securities.symbol:005930` |
| 시장 | `securities.market:시장` | `securities.market:KOSPI` |
| 언급기업 | `named_entities.entities.company.name:이름` | |
| 언급인물 | `named_entities.entities.person.name:인물명` | |
| 감성 | `polarity.name:긍정/부정/중립` | `polarity.name:긍정` |
| ESG | `esg.category.name:환경/사회/지배구조` | `esg.category.name:환경` |
| ESG감성 | `esg.polarity.name:긍정/부정` | |
| 날짜시간 | `created_at:["시작" to "끝"]` | `created_at:["2024-06-01T00:00:00" to "2024-06-30T23:59:59"]` |

### Boolean 연산자
- `and` - AND 조건
- `or` - OR 조건
- `!` 또는 `-` - NOT 조건
- `()` - 그룹핑
- `"키워드1 키워드2"~N` - N단어 이내 근접 검색

## DocumentTrends

```python
DocumentTrends(category, section, query, interval="1d", date_from=None, date_to=None)
```
interval: `1y`, `1M`, `1w`, `1d`, `1h`, `1m`

## DocumentAggregation

```python
DocumentAggregation(category, section, query, groupby, date_from=None, date_to=None, min_count=0)
```
groupby 예: `"named_entities.entities.company.name:100"`, `"securities.name:50"`

## GetSentimentScore

```python
GetSentimentScore(query, interval="1d", date_from=None, date_to=None)
```

## SimilarKeywords

```python
SimilarKeywords(positive_keyword, negative_keyword=None, max_count=30, min_score=0.5)
```

## 토픽 API

```python
SearchTrendingTopics(category, section, fields=None)
GetTrendingTopic(category, section, topic_uid, count=10, summary=True)
SearchHistoricalTopics(category, section, query, count=10, page=None, date_from=None, date_to=None)
```

## 응답 구조

```json
{
  "success": true,
  "data": {
    "pods": [
      {"class": "Input", "content": {...}},
      {"class": "Result:DocumentSearchResult", "content": {
        "data": {
          "total_matches": 1234,
          "current_page": 1,
          "last_page": 13,
          "docs": [{
            "title": "...",
            "publisher": "...",
            "created_at": "2024-01-15T09:30:00",
            "content": "...",
            "securities": [{"name":"삼성전자","symbol":"005930","market":"KOSPI"}],
            "polarity": {"name":"긍정","score":0.95},
            "esg": {"category":{"name":"환경"},"polarity":{"name":"긍정"}},
            "content_url": "..."
          }]
        }
      }}
    ]
  }
}
```

## 언론사 그룹 참조

| 그룹 | 언론사 |
|------|--------|
| 중앙일간지 | 경향신문, 국민일보, 동아일보, 서울신문, 세계일보, 아시아투데이, 조선일보, 중앙일보, 한겨레, 한국일보 |
| 중앙경제지 | 뉴스토마토, 디지털타임스, 매일경제, 머니투데이, 서울경제, 아주경제, 이데일리, 이투데이, 전자신문, 파이낸셜뉴스, 한국경제 |
