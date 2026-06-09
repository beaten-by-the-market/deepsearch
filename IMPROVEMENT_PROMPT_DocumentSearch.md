# 개선 지시 프롬프트 — DocumentSearch 뉴스 검색 클라이언트화

아래 프롬프트를 이 레포(`C:\Users\Peter\github\deepsearch`)에서 Claude Code에 그대로 입력하면 된다.

---

## 프롬프트 (복사해서 사용)

> 이 레포의 `HANDOFF_DocumentSearch_news_20260610.md`를 먼저 읽어줘. 방금 외부 작업에서 DeepSearch
> `DocumentSearch`로 KRX 상장사 뉴스를 조회하며 겪은 시행착오와 **확정된 동작 규칙**이 정리돼 있어.
> 이걸 토대로 레포를 개선해줘. 목표는 "같은 시행착오를 다시는 겪지 않게" 만드는 것.
>
> **배경 사실(핸드오프에서 검증됨)**:
> - 비로그인은 **검색 기간이 1년을 넘으면** `data.exceptions`에 `RequestEntityTooLarge`가 오고 결과가
>   통째로 비어버린다(증상은 "0건"). `fields`·`OR 괄호`는 무죄 — 1년 이내면 정상.
> - 문서 리스트 키는 `content.data["docs"]` (NOT `documents`).
> - 에러는 HTTP 200 + `data.exceptions[]`로 전달된다 → **결과가 비면 exceptions부터 확인**.
> - 한글/괄호는 `urllib.parse.quote` 필수, 콘솔은 CP949라 UTF-8 파일로 덤프해 확인.
>
> **해줄 일**:
> 1. **`newsscrap/ds_client.py`** 신규 작성 — 핸드오프 §4의 헬퍼를 정식 모듈로:
>    - `_compute(query)`: URL 인코딩 + `Authorization: Basic` + `verify=False` + 3회 retry,
>      `data.exceptions`가 있으면 `RuntimeError`로 올림.
>    - `_windows(date_from, date_to)`: `YYYYMMDD` 범위를 **≤1년 청크**로 분할.
>    - `document_search(query, category="news", section="", count=10, date_from=None, date_to=None)`:
>      1년 초과 윈도우 자동 분할·호출 후 `content_url` 기준 dedup·병합, `(docs, total_matches)` 반환.
>      파싱은 반드시 `pods[1]["content"]["data"]["docs"]`.
>    - API_KEY는 `.env`에서 로드(기존 패턴 재사용). 비밀키 하드코딩 금지.
>    - 모듈 docstring 상단에 1년 한도·`docs` 키·exceptions 4줄 gotcha 명시.
> 2. **기존 코드 일원화**: `newsscrap/deepsearch_query.py`·`deepsearch_query_api.py`에 흩어진
>    `data['pods'][1]['content']['data']` 직접 파싱과 raw `requests.get`를 `ds_client`로 교체
>    (동작 동일성 유지 — 기존 함수 시그니처/Streamlit 출력은 깨지 않게). 큰 리팩터가 위험하면
>    최소 침습으로 `document_search`만 끼워넣고 나머진 TODO 주석.
> 3. **문서화**: `docs/3_API함수를_통한_데이터_조회_문서검색.md` 하단에 "⚠️ 실전 함정" 박스를 추가
>    (1년 한도 / exceptions 먼저 보기 / `docs` 키 / URL 인코딩 / CP949). 핸드오프를 출처로 링크.
> 4. **스킬 갱신**: `deepsearch/SKILL.md`(및 해당되면 `deepsearch-docs/SKILL.md`)의 DocumentSearch
>    관련 섹션에 같은 4줄 gotcha와 "결과 0이면 `data.exceptions` 확인" 규칙을 추가.
> 5. **검증**: `ds_client`로 핸드오프 부록 A의 쿼리들을 재현하는 작은 스모크 테스트
>    (`newsscrap/test_ds_client.py` 또는 `if __name__=="__main__"` 예시)를 넣고 실제로 돌려
>    `유한양행 배당`이 1년 윈도우에서 docs를 반환하고, **2년 윈도우가 자동 분할되어 성공**하는지 확인해줘.
>    (한글 결과는 UTF-8 파일로 떨어뜨려 확인.)
>
> **제약**:
> - `.env`의 실제 키 값은 절대 커밋/출력하지 마. `.gitignore`에 `.env`가 있는지 확인.
> - DB 적재 로직(psycopg2)은 건드리지 마 — 이번 작업은 **뉴스 검색 클라이언트 + 문서화**만.
> - 기존 Streamlit 앱이 깨지지 않는지 import 단위로만 빠르게 점검(전체 실행은 불필요).
>
> 끝나면: 변경 파일 목록, `ds_client` 공개 함수 시그니처, 스모크 테스트 출력(요약), 그리고
> "기존 코드에서 교체한 곳 / TODO로 남긴 곳"을 정리해서 보고해줘.

---

## 메모 (지시자용)

- 핸드오프 §4 헬퍼는 검증된 동작 그대로다. 그대로 이식하면 안전.
- 1년 자동분할이 핵심 가치 — 분석가가 "왜 0건이지" 헤매는 일을 원천 차단한다.
- 더 욕심내면: `document_trends`(시계열 추이)·`document_aggregation`(언급 기업 집계)도 같은
  `_compute`/exceptions 패턴으로 얇게 감싸 `ds_client`에 추가(스코프 넘치면 다음 PR).
