# DeepSearch Claude Code Skills 설치 가이드

DeepSearch API를 Claude Code(VSCode 확장)에서 슬래시 커맨드로 사용할 수 있는 스킬 패키지입니다.

---

## 1. 다운로드

GitHub 저장소에서 `deepsearch.zip` 파일을 다운로드합니다.

1. GitHub 저장소의 `deepsearch-claude-skills배포` 폴더로 이동
2. `deepsearch.zip` 파일 클릭
3. 우측 상단 `···` 버튼 클릭 → **Download** 선택

---

## 2. 압축 해제

다운로드한 `deepsearch.zip`을 **사용할 프로젝트의 루트 폴더**에 압축 해제합니다.

```
# 예시: 프로젝트 폴더가 C:\Users\사용자\my-project 인 경우
# deepsearch.zip을 해당 폴더에 풀면 아래 구조가 됩니다:

my-project/
├── .env                              ← API 키 설정 (직접 생성)
├── .claude/                          ← 슬래시 커맨드 등록
│   ├── commands/
│   │   ├── deepsearch.md             ← /deepsearch
│   │   ├── deepsearch-finance.md     ← /deepsearch-finance
│   │   ├── deepsearch-analytics.md   ← /deepsearch-analytics
│   │   └── deepsearch-docs.md        ← /deepsearch-docs
│   └── settings.local.json
├── deepsearch/                       ← 메인 스킬 (통합)
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── deepsearch-finance/               ← 기업·재무 전용
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── deepsearch-analytics/             ← 분석·스크리닝 전용
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── deepsearch-docs/                  ← 문서검색 전용
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── docs/                             ← API 원본 문서
│   ├── DEEPSEARCH_API_MASTER.md
│   ├── api_guide.html
│   └── ...
└── (기존 프로젝트 파일들)
```

> **참고:** 이미 `.claude` 폴더가 있는 프로젝트라면, `commands/` 폴더 안의 파일만 기존 `.claude/commands/`에 복사하세요.

---

## 3. API 키 설정

프로젝트 루트에 `.env` 파일을 만들고 DeepSearch API 키를 입력합니다.

```bash
# .env 파일 내용
API_KEY=your_base64_encoded_api_key
```

API 키는 두 가지 형식 모두 사용 가능합니다:

```bash
# 형식 1: Base64 인코딩된 키 (그대로 입력)
API_KEY=dXNlcjpwYXNzd29yZA==

# 형식 2: user:password 형식 (자동으로 Base64 변환됨)
API_KEY=user:password
```

> **주의:** `.env` 파일은 `.gitignore`에 추가하여 Git에 커밋되지 않도록 하세요.

---

## 4. VSCode에서 사용하기

### 사전 요구사항

- **Claude Code VSCode 확장** 설치
- **`.env` 파일에 API 키 설정** (위 3단계)

### 슬래시 커맨드

VSCode에서 Claude Code 채팅창을 열고 슬래시 커맨드를 입력합니다:

| 커맨드 | 용도 | 사용 예시 |
|--------|------|----------|
| `/deepsearch` | 통합 (재무+문서+분석) | 삼성전자 최근 뉴스와 재무 분석해줘 |
| `/deepsearch-finance` | 기업·재무 데이터 조회 | SK하이닉스 5년간 영업이익 추이 보여줘 |
| `/deepsearch-analytics` | 스크리닝·밸류에이션 | 매출 1조 이상, 영업이익률 15% 이상 기업 찾아줘 |
| `/deepsearch-docs` | 뉴스·공시·리포트 검색 | 반도체 관련 최근 뉴스 검색해줘 |

### 사용 흐름

```
1. Claude Code 채팅창에서 슬래시(/) 입력
2. deepsearch 선택 (또는 직접 타이핑)
3. 질문 입력 (API 키는 .env에서 자동으로 읽힘)
4. Claude가 DeepSearch API를 호출하여 결과 반환
```

### 사용 예시

```
/deepsearch
삼성전자의 최근 3년간 매출과 영업이익 추이를 분석하고,
관련 최신 뉴스도 함께 정리해줘.
```

```
/deepsearch-analytics
벤자민 그레이엄 방법론으로 가치주를 스크리닝해줘.
매출 1조 이상, 영업이익률 10% 이상, 흑자 기업 조건으로.
```

```
/deepsearch-docs
최근 1주일간 KOSPI 상장사 관련 부정적 뉴스를 검색해줘.
```

---

## 5. 스킬별 상세 기능

### deepsearch (통합)
- 기업·재무 + 문서검색 + 분석 기능 모두 포함
- 복합적인 질문에 적합
- 시황분석 리포트 생성 (`market_overview.py`)

### deepsearch-finance (기업·재무)
- `GetFinancialStatements` — 재무제표 조회
- 주가/PER/PBR 등 시장 데이터 조회
- 기업 개요, 배당, 주주, 임원 정보

### deepsearch-analytics (분석·스크리닝)
- 가치투자 스크리닝 (Graham, Buffett 방법론)
- 턴어라운드 기업 발굴
- 포트폴리오 백테스팅
- Top/Bottom/Sort/Rank 분석 함수

### deepsearch-docs (문서검색)
- `DocumentSearch` — 뉴스/공시/리포트/특허 검색
- `DocumentTrends` — 키워드 트렌드 분석
- `DocumentAggregation` — 문서 집계
- KRX 상장사 모니터링

---

## 6. API 문서 참고

`docs/` 폴더에 DeepSearch API 원본 문서가 포함되어 있습니다:

| 파일 | 내용 |
|------|------|
| `DEEPSEARCH_API_MASTER.md` | API 전체 레퍼런스 (함수, 파라미터, 응답 구조) |
| `api_guide.html` | KRX 실무 활용 가이드 (브라우저에서 열기) |
| `1_기본적인_데이터_조회방법.md` | 기본 쿼리 문법 |
| `2_쿼리를_통한_데이터_조회.md` | 심화 쿼리 (스크리닝, 연산 함수) |
| `3_API함수를_통한_데이터_조회_*.md` | API 함수별 상세 문서 |

---

## 주의사항

- 재무제표 데이터는 반드시 `GetFinancialStatements` 함수로 조회하세요 (자연어 쿼리 사용 시 오류 발생 가능)
- `GetFinancialStatements` 호출 시 기업명에 **따옴표를 넣지 마세요** (`"삼성전자"` → 403 오류)
- 주가, PER, PBR, 시가총액 등 시장 데이터는 자연어 쿼리 사용 가능
