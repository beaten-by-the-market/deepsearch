# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepSearch API toolkit for KRX (Korea Exchange) listed companies. The repo holds:
- the DeepSearch Claude skill (`skills/deepsearch/`), used via Claude Code (clone the repo or copy the folder into `.claude/skills/`; no zip distribution),
- the DeepSearch API reference (`docs/reference/`),
- data verification notes (`research/`),
- analysis scenario notebooks for Colab (`scenarios/`), adapted and extended from the KOSCOM CHECK API case scenarios.

**Status (2026-11-25):** The old Streamlit news-scrap app (`newsscrap/`), its Supabase DB pipeline and the daily GitHub Actions workflow were removed; their features now live in `scenarios/` (5-08~13 data fetch, 2-13 listed-company filter, 2-14 stock dashboard). The DeepSearch API key is valid.

**To use DeepSearch data:** read `skills/deepsearch/SKILL.md` first, call `python skills/deepsearch/scripts/query_api.py "쿼리"` (reads `API_KEY` from `.env`; never echo the key), and check `docs/reference/DEEPSEARCH_API_MASTER.md` §16–17 for what this subscription can and cannot do (`research/data_gaps/` lists data DeepSearch does not have).

## Project Structure

```
deepsearch/
├── skills/
│   └── deepsearch/         # 통합 스킬 소스 (유일한 스킬)
├── docs/
│   ├── api_guide.html      # GitHub Pages (위치 고정)
│   └── reference/          # DeepSearch API 레퍼런스 (README.md 색인, MASTER 요약, GitBook 원문, sync_from_gitbook.py)
├── research/               # DeepSearch 데이터 검증 노트 (README.md 색인, 주제별 폴더)
│   ├── restatement/        # 재무제표 과거값: 원래값 vs 재작성값 (OpenDART 대조)
│   ├── pbr_bps/            # 시장데이터 PBR/BPS 정의
│   ├── price_adjustment/   # 주가 수정주가 여부 (원주가 옵션 없음, 수량은 미수정)
│   └── data_gaps/          # DeepSearch에 없는 데이터 (수급·공매도·대차·신용·선물·장중 등)
├── scenarios/              # 분석 시나리오 노트북(Colab 기준). README.md 색인
│   ├── _src/               # 노트북 원본(.py, `# %%` 셀 구분) — 여기를 고친다
│   ├── _tools/             # ds_helper.py(노트북 공통 셀), build.py(원본→실행된 .ipynb), show.py(출력 확인)
│   ├── _data/              # 노트북이 읽는 자료 (언론사 목록 등; Colab은 GitHub raw로 읽음)
│   └── <유형>/             # NN_이름.ipynb(실행 결과 포함) + NN_이름.md(설명)
├── notes/                  # 작업 기록/핸드오프 (과거 기록이라 경로가 옛것일 수 있음)
└── .claude/commands/       # /deepsearch 커맨드 (skills/deepsearch 경로 참조)
```

## Skill

- Source of truth: `skills/deepsearch/`. No build step (zip distribution was removed 2026-11-25).
- `.claude/commands/deepsearch.md` is a condensed copy of the skill for Claude Code in this repo; keep its paths pointing at `skills/deepsearch/`.
- Scripts share `skills/deepsearch/scripts/_ds_common.py` (transport/output) and `_ds_data.py` (stock universe via `GetStockSymbols()`, all-stock snapshot via `GetStockPrices` without entities, index snapshot, `format_krw`, `PRICE_BASIS_NOTICE`). No script loops per company; use list/all-stock calls. _ds_common: API key lookup (env `DEEPSEARCH_API_KEY`/`API_KEY` → `.env` in cwd/parents → skill-dir parents; a key as the first CLI arg still works), compute via POST, `data.exceptions` surfaced as errors with hints, and large results (>20k chars) saved to a temp JSON file with only a preview printed.
- Listed operating companies are `company_type_l1` "1" (일반법인) and "2" (공기업: 한국전력·기업은행 등 8종목); "8" is ETF·ETN.
- In SKILL.md, `${CLAUDE_SKILL_DIR}` means the skill folder (`skills/deepsearch` when reading the repo directly).

## Scenarios

- Edit `scenarios/_src/<유형>/<이름>.py`, then `python scenarios/_tools/build.py <유형>/<번호>` rebuilds and executes the notebook (outputs saved; runs in the git-ignored `scenarios/_tools/_run/`, local runs read `API_KEY` from `.env`, Colab reads Secrets `DEEPSEARCH_API_KEY`). Don't hand-edit `.ipynb`. Check outputs with `python scenarios/_tools/show.py <ipynb>`.
- `ds_helper.py` is pasted into every notebook's setup cell; after changing it, rebuild all notebooks (`python scenarios/_tools/build.py`) and re-check the numbers quoted in each `.md` "결과 예시".
- Numbering follows the CHECK scenario `유형-번호`; new scenarios take the next number in their type. Each `.md` says 각색 / 확장 / 기본.
- Never call the CHECK API from this repo; the CHECK scenario docs live in the sibling repo `check-api-krx-dl`.
- Colab badge links point at `main` on GitHub (`beaten-by-the-market/deepsearch`, public), so they work only after push.

## Commands

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

python skills/deepsearch/scripts/query_api.py "삼성전자 PER PBR 2026-11-01-2026-11-24"
python scenarios/_tools/build.py 5_data_lookup/07      # 노트북 하나 다시 빌드·실행
python research/data_gaps/verify_data_gaps.py           # research 노트 재현 (각 폴더에 스크립트)
```

## Configuration

`.env` at the repo root: `API_KEY` = DeepSearch API key (`id:secret` or base64; Basic auth). Never print it or write it into notebooks, logs or docs.

## Deployment

**GitHub Pages** - API documentation
- `docs/api_guide.html` 서비스
- Repository Settings → Pages → Source: main branch, /docs folder

## DeepSearch API Documentation

**API 문서 위치:** `docs/reference/` (색인: `docs/reference/README.md`)
- `DEEPSEARCH_API_MASTER.md` - API 종합 가이드 + §17 전체 함수 목록과 이 구독 키로의 호출 결과(✅/⚠️/❌)
- `1_기본적인_데이터_조회방법.md` ~ `5_결과레이아웃.md` - 공식 가이드(https://help.deepsearch.com/dp) 원문. 함수 그룹별 파일(국내기업, 채권, 산업, 인물, 문서, 이벤트, 경제지표, 토픽인사이트)
- 원문은 `python docs/reference/sync_from_gitbook.py`로 다시 생성합니다. 레포 메모는 `<!-- repo-memo:start -->`~`<!-- repo-memo:end -->` 안에만 쓰세요(그 밖은 덮어씀).
- 현재 구독으로 안 되는 것: v2 REST(`api-v2.deepsearch.com`, 401), 해외기업(`/v2/companies`, 401), 챗딥서치(`/note/v1`, 401), 채권·통계청 등 일부 compute 함수(`NameError`). 원문에 넣지 않았거나 페이지에 메모를 붙였습니다. 데이터 자체가 없는 것은 `research/data_gaps/`.

Base URL: `https://api.deepsearch.com/v1/compute?input=` (공식 가이드는 `https://app-api.deepsearch.com` 안내 — 둘 다 동작. POST `{"input": "..."}`도 지원)

### 주요 API 함수
- `DocumentSearch(categories, subcategories, "search_query", count=100, page=N)` - 문서 검색. 한 페이지가 100건보다 적게 와도 뒤에 더 있을 수 있으니 `total_matches`/`last_page`로 넘깁니다. Basic 인증은 기간 1년까지.
- `DocumentTrends(categories, subcategories, "query", interval="1d")` - 문서 트렌드
- `DocumentAggregation(categories, subcategories, "query", "groupby")` - 문서 집계 (예: `securities.symbol:30`, `publisher:20`; `publisher.raw:N`은 500)
- `GetStockSymbols()` - 전 종목 기본정보(시장·업종·식별자·그룹). `GetStockPrices`(종목 생략 시 전 종목 하루치)
- `GetEntitySummary(symbol)` - 기업 상세정보

### 문서 카테고리
- `["news"]` - 국내뉴스 (섹션: economy, politics, society, culture, world, tech, entertainment, opinion)
- `["research"]` - 증권사보고서 (섹션: market, strategy, company, industry, economy, bond)
- `["company"]` - 공시/IR (섹션: ir, disclosure). 공매도 과열·투자경고 같은 거래소 공시도 포함(2026-08부터 촘촘)
- `["patent"]` - 특허 (출원인은 회사 공식명과 법인번호·사업자번호로 들어 있음)

### 쿼리 필드 (심화검색)
- `title:키워드` - 제목 검색 / `!title:키워드` - 제외
- `content:키워드` - 본문 검색
- `publisher.raw:('매일경제' or '한국경제')` - 언론사 필터
- `securities.symbol:005930` - 관련종목(상장사) 종목코드. **접두어 없는 6자리가 가장 정확합니다.** `KRX:005930`은 키워드 검색으로 바뀌고, `securities.name:`은 리서치(공식명 '에스케이하이닉스')·공시(DART명 '현대자동차')에서 놓칩니다. 여러 종목: `securities.symbol:(005930 or 000660)`
- `securities.market:KOSPI` - 시장별 필터 (KOSPI, KOSDAQ, KONEX)
- `named_entities.entities.company.name:기업명` - 언급된 기업(비상장 포함)
- `polarity.name:긍정` - 긍부정 필터 (뉴스의 절반가량만 값이 있음; 나머지는 `customized_ml.kis` 모델 값)
- `esg.category.name:환경` - ESG 필터

### 쿼리 예시
```python
# 삼성전자 관련 뉴스
DocumentSearch(["news"],["economy"],"securities.symbol:005930")

# KOSPI 상장사가 언급된 뉴스 + 키워드
DocumentSearch(["news"],["economy"],"securities.market:KOSPI and 수주")

# 날짜+시간 범위 검색
DocumentSearch(["news"], [], "키워드 and created_at:[\"2022-07-12T00:00:00\" to \"2022-07-12T09:00:00\"]")
```

### Boolean 연산자
- `and` - AND 조건
- `or` - OR 조건
- `!` 또는 앞에 `-` - NOT 조건
- `()` - 그룹핑
