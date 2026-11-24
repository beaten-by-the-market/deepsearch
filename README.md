# DeepSearch KRX 상장사 데이터 도구

DeepSearch API로 KRX 상장사(KOSPI, KOSDAQ, KONEX) 데이터를 다루기 위한 Claude Code 스킬, API 레퍼런스, 데이터 검증 노트, Colab 분석 시나리오 노트북입니다.

## 빠른 시작: DeepSearch 데이터를 쓰려면 (에이전트·처음 보는 사람용)

1. **[skills/deepsearch/SKILL.md](skills/deepsearch/SKILL.md)를 먼저 읽으세요.** 요청 유형별 호출식, 필수 규칙(재무제표는 `GetFinancialStatements`, 수정주가 안내 등), 검증된 함정이 있습니다.
2. 준비: `pip install -r skills/deepsearch/requirements.txt`, 레포 루트 `.env`에 `API_KEY=<DeepSearch 키>`
3. 호출: `python skills/deepsearch/scripts/query_api.py "쿼리"`
   - API 키는 `.env`나 환경변수에서 자동으로 읽습니다. 키를 명령에 넣거나 출력하지 마세요.
   - DocumentSearch 기간이 1년을 넘으면 자동으로 나눠 호출합니다.
   - 결과가 크면(2만 자 초과) 파일로 저장하고 경로와 미리보기만 출력합니다.
4. SKILL.md에 없는 함수는 [docs/reference/DEEPSEARCH_API_MASTER.md](docs/reference/DEEPSEARCH_API_MASTER.md)를 보세요. 17절에 전체 함수 129개와 이 키로 호출해 본 결과(✅/⚠️/❌)가 있습니다. 파라미터 상세는 [docs/reference/](docs/reference/) 원문을 grep하세요.
5. 분석·백테스트 전에 [research/](research/)를 확인하세요. 재무제표 재작성값, BPS look-ahead, 수정주가, DeepSearch에 없는 데이터를 검증한 노트가 있습니다.
6. 바로 돌려 볼 분석 예시는 [scenarios/](scenarios/README.md)에 있습니다(Colab에서 열기 배지).

- **현재 구독으로 쓸 수 없는 것:** DeepSearch v2 REST(`api-v2.deepsearch.com`), 해외기업, 챗딥서치, 채권·통계청 함수
- **DeepSearch에 없는 데이터:** 투자자별 수급, 공매도·대차·신용, 지수선물, ETF NAV, 장중 데이터([research/data_gaps](research/data_gaps/README.md))
- **이 작업에는 읽지 않아도 되는 것:** `notes/`(작업 기록), `docs/api_guide.html`

## 구성

| 폴더 | 내용 |
|---|---|
| [skills/deepsearch](skills/deepsearch/SKILL.md) | DeepSearch API를 Claude Code에서 쓰는 통합 스킬(문서검색, 기업재무, 스크리닝, 멀티스텝 분석) |
| [docs/reference](docs/reference/README.md) | 공식 가이드(https://help.deepsearch.com/dp) 원문과 요약·함수별 호출 결과. `sync_from_gitbook.py`로 다시 받음 |
| [research](research/README.md) | DeepSearch 값이 정확히 무엇인지 실제 호출로 검증한 노트 |
| [scenarios](scenarios/README.md) | 분석 시나리오 노트북(Colab 기준, 실행 결과 포함). KOSCOM CHECK API 케이스 시나리오를 DeepSearch로 각색·확장했고, 뉴스·공시·IR·리포트·특허 가져오기와 상장사로 거르기, 종목 한 장 보기도 들어 있음 |

## 프로젝트 구조

```
deepsearch/
├── skills/
│   └── deepsearch/             # Claude 스킬 소스 (SKILL.md, references, scripts, requirements.txt)
├── docs/
│   ├── api_guide.html          # GitHub Pages
│   └── reference/              # DeepSearch API 레퍼런스 (README.md, MASTER 요약, 원문, 동기화 스크립트)
├── research/                   # DeepSearch 데이터 검증 노트
├── scenarios/                  # 분석 시나리오 노트북 (README.md 색인, _src 원본, _tools 빌더)
├── notes/                      # 작업 기록 (핸드오프 등)
├── .claude/commands/           # Claude Code 슬래시 커맨드 (/deepsearch)
└── requirements.txt            # 스크립트·research·노트북 빌드용
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

## 시나리오 노트북

- **Colab:** [scenarios/README.md](scenarios/README.md)의 노트북을 열고 "Colab에서 열기"를 누릅니다. Secrets에 `DEEPSEARCH_API_KEY`를 넣으면 됩니다.
- **로컬에서 다시 빌드:** 아래 명령으로 노트북을 다시 만들고 실행합니다.

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python scenarios/_tools/build.py 5_data_lookup/07   # 원본(_src) → 실행된 .ipynb
```

## 배포

| 서비스 | 플랫폼 | 설명 |
|--------|--------|------|
| API 문서 | GitHub Pages | `docs/api_guide.html` |

예전의 Streamlit 뉴스 스크랩 웹앱(`newsscrap/`)과 Supabase 적재 파이프라인·GitHub Actions는 2026-11-25에 제거했습니다(git 이력에서 복원 가능). 기능은 시나리오 5-08~13, 2-13, 2-14로 옮겼고, 각 문서에 웹앱으로 다시 만들 때의 방향을 적었습니다.

## 라이선스

Private repository
