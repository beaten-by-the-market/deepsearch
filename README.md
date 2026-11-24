# DeepSearch KRX 상장사 문서검색

DeepSearch API를 활용한 KRX 상장사(KOSPI, KOSDAQ, KONEX) 관련 문서 검색 서비스와, DeepSearch 데이터를 Claude Code에서 쓰기 위한 스킬·레퍼런스입니다.

## 빠른 시작: DeepSearch 데이터를 쓰려면 (에이전트·처음 보는 사람용)

1. **[skills/deepsearch/SKILL.md](skills/deepsearch/SKILL.md)를 먼저 읽으세요.** 요청 유형별 호출식, 필수 규칙(재무제표는 `GetFinancialStatements`, 수정주가 안내 등), 검증된 함정이 있습니다.
2. 준비: `pip install -r skills/deepsearch/requirements.txt`, 레포 루트 `.env`에 `API_KEY=<DeepSearch 키>`
3. 호출: `python skills/deepsearch/scripts/query_api.py "쿼리"`
   - API 키는 `.env`나 환경변수에서 자동으로 읽습니다. 키를 명령에 넣거나 출력하지 마세요.
   - DocumentSearch 기간이 1년을 넘으면 자동으로 나눠 호출합니다.
   - 결과가 크면(2만 자 초과) 파일로 저장하고 경로와 미리보기만 출력합니다.
4. SKILL.md에 없는 함수는 [docs/reference/DEEPSEARCH_API_MASTER.md](docs/reference/DEEPSEARCH_API_MASTER.md)를 보세요. 17절에 전체 함수 129개와 이 키로 호출해 본 결과(✅/⚠️/❌)가 있습니다. 파라미터 상세는 [docs/reference/](docs/reference/) 원문을 grep하세요.
5. 분석·백테스트 전에 [research/](research/)를 확인하세요. 재무제표 재작성값, BPS look-ahead, 수정주가 검증 노트가 있습니다.

- **현재 구독으로 쓸 수 없는 것:** DeepSearch v2 REST(`api-v2.deepsearch.com`), 해외기업, 챗딥서치, 채권·통계청 함수
- **이 작업에는 읽지 않아도 되는 것:** `newsscrap/`(뉴스 스크랩 웹앱), `notes/`(작업 기록), `docs/api_guide.html`

## 구성

이 레포에는 두 가지 산출물이 있습니다.

### 1. newsscrap - 뉴스 스크랩 웹앱
KRX 상장사가 언급된 뉴스, 증권사보고서, 공시/IR, 특허 문서를 검색합니다.

- **웹앱**: Streamlit 기반 검색 인터페이스
- **데이터 파이프라인**: 상장사 정보를 Supabase DB에 적재 (매일 오전 7시 KST) — **2026-11 중단** (DB 미사용, Actions 비활성)

### 2. skills/deepsearch - Claude 스킬
DeepSearch API를 Claude에서 쓰기 위한 통합 스킬(문서검색, 기업재무, 스크리닝, 멀티스텝 분석).

### 3. docs/reference - DeepSearch API 레퍼런스
공식 가이드(https://help.deepsearch.com/dp)를 옮긴 원문과 요약·함수별 호출 결과. `sync_from_gitbook.py`로 다시 받을 수 있습니다([docs/reference/README.md](docs/reference/README.md)).
Claude Code에서 쓰는 방식이며, 설치 방법은 아래 "스킬 설치"를 참고하세요.

## 프로젝트 구조

```
deepsearch/
├── newsscrap/                  # 뉴스 스크랩 웹앱
│   ├── deepsearch_query.py     # Streamlit 웹앱
│   ├── deepsearch_query_api.py # 데이터 파이프라인
│   ├── ds_client.py            # DocumentSearch 클라이언트 (1년 분할, 예외 처리)
│   ├── data/                   # 언론사 목록, 관심종목 서식
│   └── tests/                  # ds_client 스모크 테스트
├── skills/
│   └── deepsearch/             # Claude 스킬 소스 (SKILL.md, references, scripts, requirements.txt)
├── docs/
│   ├── api_guide.html          # GitHub Pages
│   └── reference/              # DeepSearch API 레퍼런스 (README.md, MASTER 요약, 원문, 동기화 스크립트)
├── research/                   # DeepSearch 데이터 검증 노트 (재작성값, PBR/BPS 정의, 수정주가)
├── notes/                      # 작업 기록 (핸드오프 등)
├── .claude/commands/           # Claude Code 슬래시 커맨드 (/deepsearch)
├── .github/workflows/          # GitHub Actions
└── requirements.txt
```

## 스킬 설치 (Claude Code)

이 레포를 클론하면 `/deepsearch` 커맨드(`.claude/commands/deepsearch.md`)를 바로 쓸 수 있습니다.
다른 프로젝트에서 쓰려면 `skills/deepsearch/` 폴더를 해당 프로젝트의 `.claude/skills/deepsearch/`(또는 개인용 `~/.claude/skills/deepsearch/`)에 복사하세요.
Claude Code에게 "이 레포의 deepsearch 스킬을 설치해줘"라고 요청해도 됩니다.

프로젝트 루트에 `.env`를 만들고 DeepSearch API 키를 넣습니다(`.env`는 `.gitignore`에 추가).

```bash
API_KEY=your_base64_encoded_api_key
```

> Claude.ai 일반 채팅용 zip 업로드 방식은 더 이상 제공하지 않습니다(2026-11-25 제거, git 이력에서 복원 가능).

## 로컬 실행

```bash
# 가상환경 설정
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
API_KEY=your_deepsearch_api_key
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_USER_CRUD=your_crud_user
DB_PASSWORD_CRUD=your_crud_password

# 웹앱 실행
streamlit run newsscrap/deepsearch_query.py
```

## 배포

| 서비스 | 플랫폼 | 설명 |
|--------|--------|------|
| 웹앱 | Streamlit Cloud | `newsscrap/deepsearch_query.py` |
| API 문서 | GitHub Pages | `docs/api_guide.html` |
| 데이터 업데이트 | GitHub Actions | 매일 07:00 KST 자동 실행 — 2026-11 중단 |

## 기술 스택

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, DeepSearch API
- **Database**: PostgreSQL (Supabase) — 2026-11 중단
- **CI/CD**: GitHub Actions

## 라이선스

Private repository
