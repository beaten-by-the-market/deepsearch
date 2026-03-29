# DeepSearch 스킬 설치 가이드

DeepSearch API를 Claude에서 사용할 수 있는 스킬 패키지입니다.
문서검색, 기업재무 조회, 스크리닝, 멀티스텝 분석을 지원합니다.

---

## 1. 다운로드

GitHub 저장소에서 `deepsearch.zip` 파일을 다운로드합니다.

1. GitHub 저장소의 `deepsearch-claude-skills배포` 폴더로 이동
2. `deepsearch.zip` 파일 클릭
3. 우측 상단 `···` 버튼 클릭 → **Download** 선택

---

## 2. Claude Web에서 사용하기

1. [claude.ai](https://claude.ai) 접속
2. 설정 → **Skills** → **Add Skill**
3. 다운로드한 `deepsearch.zip` 파일 업로드
4. 채팅에서 DeepSearch 관련 질문을 하면 스킬이 자동으로 활성화됩니다

### API 키 전달

Claude Web에서는 `.env` 파일을 사용할 수 없으므로, 채팅에서 직접 API 키를 전달합니다:

```
API키: {본인의_API_키}
삼성전자의 최근 3년간 매출과 영업이익 추이를 분석하고,
관련 최신 뉴스도 함께 정리해줘.
```

---

## 3. Claude Code (VSCode)에서 사용하기

### 설치

다운로드한 `deepsearch.zip`을 프로젝트 루트 폴더에 압축 해제합니다.

```
my-project/
├── .env              ← API 키 설정 (직접 생성)
├── deepsearch/       ← 압축 해제된 스킬 폴더
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── (기존 프로젝트 파일들)
```

### API 키 설정

프로젝트 루트에 `.env` 파일을 만들고 DeepSearch API 키를 입력합니다.

```bash
# .env
API_KEY=your_base64_encoded_api_key
```

> **주의:** `.env` 파일은 `.gitignore`에 추가하여 Git에 커밋되지 않도록 하세요.

### 사용법

Claude Code 채팅창에 `/deepsearch`를 입력한 뒤 질문을 작성합니다.

```
/deepsearch
삼성전자의 최근 3년간 매출과 영업이익 추이를 분석하고,
관련 최신 뉴스도 함께 정리해줘.
```

API 키는 `.env`에서 자동으로 읽힙니다.

---

## ZIP 내용물

```
deepsearch.zip
└── deepsearch/
    ├── SKILL.md                    ← 스킬 정의 (라우팅 규칙, API 사용법)
    ├── references/
    │   ├── api_quick_reference.md  ← API 함수 레퍼런스
    │   ├── krx_monitoring_guide.md ← KRX 모니터링 가이드
    │   ├── value_investing.md      ← 가치투자 분석 가이드
    │   └── verified_examples.md    ← 검증된 사용 예시
    └── scripts/
        ├── query_api.py            ← API 호출 스크립트
        ├── market_overview.py      ← 시황 분석
        ├── market_top_movers.py    ← 등락률 상위 종목
        ├── read_document.py        ← 문서 원문 조회
        └── turnaround_screener.py  ← 턴어라운드 스크리닝
```
