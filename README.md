# DeepSearch KRX 상장사 문서검색

DeepSearch API를 활용한 KRX 상장사(KOSPI, KOSDAQ, KONEX) 관련 문서 검색 서비스입니다.

## 서비스

### newsscrap - 뉴스 스크랩
KRX 상장사가 언급된 뉴스, 증권사보고서, 공시/IR, 특허 문서를 검색합니다.

- **웹앱**: Streamlit 기반 검색 인터페이스
- **데이터 파이프라인**: 상장사 정보 자동 업데이트 (매일 오전 7시 KST)

## 프로젝트 구조

```
deepsearch/
├── newsscrap/                  # 뉴스 스크랩 서비스
│   ├── deepsearch_query.py     # Streamlit 웹앱
│   └── deepsearch_query_api.py # 데이터 파이프라인
├── docs/                       # API 문서
│   └── api_guide.html          # GitHub Pages
├── .github/workflows/          # GitHub Actions
└── requirements.txt
```

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
| 데이터 업데이트 | GitHub Actions | 매일 07:00 KST 자동 실행 |

## 기술 스택

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, DeepSearch API
- **Database**: PostgreSQL (Supabase)
- **CI/CD**: GitHub Actions

## 라이선스

Private repository
