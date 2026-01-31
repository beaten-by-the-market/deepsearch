# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KRX (Korea Exchange) listed company document search tool using the DeepSearch API. Searches news, research reports, disclosures/IR, and patents, then filters results to identify mentions of KRX-listed companies (KOSPI, KOSDAQ, KONEX).

## Project Structure

```
deepsearch/
├── newsscrap/              # 뉴스 스크랩 서비스
│   ├── deepsearch_query.py
│   ├── deepsearch_query_api.py
│   └── *.txt, *.xlsx
├── docs/                   # API 문서 (GitHub Pages)
├── .github/workflows/      # GitHub Actions
└── (향후 다른 서비스 폴더 추가)
```

## Architecture (newsscrap)

Two main components:

**newsscrap/deepsearch_query.py** - Streamlit web application
- User-facing search interface with expander-based filters (mobile-friendly)
- Loads company entity data from PostgreSQL (`ds_entitysummary` table) on startup with caching
- Displays last data update time from database
- Builds DeepSearch query strings dynamically from user selections
- Filters search results by matching entities against KRX listed companies via symbol, NICE code, business registration number, or company registration number

**newsscrap/deepsearch_query_api.py** - Data pipeline script
- Fetches all KRX listed companies from DeepSearch `FindEntity` API (KOSPI, KOSDAQ, KONEX)
- Retrieves entity summaries via `GetEntitySummary` for each company
- Uses parallel API calls with `ThreadPoolExecutor` (max_workers=10)
- Filters out ETFs: only keeps `company_type_l1='1'` (일반법인, excludes ETF/기타법인)
- Stores results in PostgreSQL `ds_entitysummary` table using `execute_values()` batch insert (psycopg2.extras)
- Table is dropped and recreated on each run

## Commands

Run Streamlit app:
```bash
streamlit run newsscrap/deepsearch_query.py
```

Run data pipeline:
```bash
python newsscrap/deepsearch_query_api.py
```

Setup virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Database

**PostgreSQL (Supabase)**
- Uses `psycopg2` for database connectivity
- Free tier: 500MB storage, unlimited API calls, 5GB/month bandwidth
- Connection via Supabase project URL

## Configuration

**Local development:** Uses `.env` file with `python-dotenv`
- `API_KEY` - DeepSearch API key (Basic auth, base64 encoded)
- `DB_HOST` - Supabase host (e.g., `db.xxxxx.supabase.co`)
- `DB_PORT` - PostgreSQL port (5432)
- `DB_NAME` - Database name (postgres)
- `DB_USER`, `DB_PASSWORD` - Read-only DB access
- `DB_USER_CRUD`, `DB_PASSWORD_CRUD` - CRUD operations DB access

**Streamlit Cloud deployment:** Uses `st.secrets` with sections:
- `[general]` - api_key, db_user, db_password, db_host, db_port, db_name
- `[crud]` - db_user, db_password, db_host, db_port (for write operations)

**GitHub Actions:** Uses repository secrets for automated daily updates

## Deployment

**Streamlit Cloud** - Web application hosting
- URL: https://share.streamlit.io (배포 후 생성)
- `deepsearch_query.py` 실행
- Secrets 설정 필요 (Settings → Secrets)

**GitHub Pages** - API documentation
- `docs/api_guide.html` 서비스
- Repository Settings → Pages → Source: main branch, /docs folder

**GitHub Actions** - Automated data pipeline
- `deepsearch_query_api.py` 매일 오전 7시(KST) 자동 실행
- Repository Secrets 설정 필요

## GitHub Actions

`.github/workflows/update_data.yml` - Automated data refresh
- Runs daily at 7:00 AM KST (22:00 UTC)
- Manual trigger available via `workflow_dispatch`
- Uses Python 3.11, actions/checkout@v4, actions/setup-python@v5
- Requires secrets: `API_KEY`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_USER_CRUD`, `DB_PASSWORD_CRUD`

## DeepSearch API Documentation

**API 문서 위치:** `docs/` 폴더 내 마크다운 파일들
- `DEEPSEARCH_API_MASTER.md` - API 종합 가이드
- `3_API함수를_통한_데이터_조회_문서검색.md` - DocumentSearch, DocumentTrends, DocumentAggregation 등
- `3_API함수를_통한_데이터_조회_국내기업.md` - FindEntity, GetEntitySummary 등
- `2_쿼리를_통한_데이터_조회.md` - 쿼리 문법

Base URL: `https://api.deepsearch.com/v1/compute?input=`

### 주요 API 함수
- `DocumentSearch(categories, subcategories, "search_query", count=100, page=N)` - 문서 검색
- `DocumentTrends(categories, subcategories, "query", interval="1d")` - 문서 트렌드
- `DocumentAggregation(categories, subcategories, "query", "groupby")` - 문서 집계
- `FindEntity("Financial", "market_id", fields=[...])` - 상장사 조회
- `GetEntitySummary(symbol)` - 기업 상세정보

### 문서 카테고리
- `["news"]` - 국내뉴스 (섹션: economy, politics, society, culture, world, tech, entertainment, opinion)
- `["research"]` - 증권사보고서 (섹션: market, strategy, company, industry, economy, bond)
- `["company"]` - 공시/IR (섹션: ir, disclosure)
- `["patent"]` - 특허

### 쿼리 필드 (심화검색)
문서 검색 시 특정 필드를 지정하여 검색 가능:
- `title:키워드` - 제목 검색
- `content:키워드` - 본문 검색
- `publisher:언론사명` - 언론사 필터
- `securities.name:기업명` - 관련종목(상장사) 이름으로 검색
- `securities.symbol:종목코드` - 관련종목 종목코드로 검색
- `securities.market:KOSPI` - 시장별 필터 (KOSPI, KOSDAQ, KONEX)
- `named_entities.entities.company.name:기업명` - 언급된 기업(비상장 포함)
- `polarity.name:긍정` - 긍부정 필터
- `esg.category.name:환경` - ESG 필터

### 쿼리 예시
```python
# 삼성전자 관련 뉴스
DocumentSearch(["news"],["economy"],"securities.name:삼성전자")

# KOSPI 상장사가 언급된 뉴스 + 키워드
DocumentSearch(["news"],["economy"],"securities.market:KOSPI and 수주")

# 복수 시장 필터
DocumentSearch(["news"],["economy"],"securities.market:(KOSPI or KOSDAQ) and 실적")

# 날짜+시간 범위 검색
DocumentSearch(["news"], [], "키워드 and created_at:[\"2022-07-12T00:00:00\" to \"2022-07-12T09:00:00\"]")
```

### Boolean 연산자
- `and` - AND 조건
- `or` - OR 조건
- `!` 또는 앞에 `-` - NOT 조건
- `()` - 그룹핑

## Performance Optimizations

**API calls:**
- Parallel fetching with `ThreadPoolExecutor` (10 concurrent requests)
- Retry logic with exponential backoff (max 5 retries, 2s delay)

**Database:**
- `execute_values()` from `psycopg2.extras` for fast batch inserts (page_size=1000)
- `@st.cache_data` for caching entity data in Streamlit

## Key Data Structures

Company matching uses these fields from `ds_entitysummary`:
- `symbol` - Stock symbol
- `symbol_nice` - NICE symbol
- `entity_name` - Company name
- `business_rid` - Business registration number
- `company_rid` - Corporate registration number
- `mkt` - Market (KOSPI/KOSDAQ/KONEX)
- `company_type_l1` - Company type (1=일반법인, 8=기타법인/ETF) - filtered to '1' only
- `last_update` - Data update date (YYYYMMDD format)

Document results contain `securities`, `entities`, `named_entities` arrays for entity matching.

## Dependencies

See `requirements.txt`:
- pandas, numpy - Data manipulation
- streamlit - Web UI
- requests - HTTP client
- psycopg2-binary - PostgreSQL driver
- tqdm - Progress bars
- python-dotenv - Environment variables
