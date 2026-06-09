# DeepSearch DocumentSearch API — 실전 사용 핸드오프 (시행착오 & 교훈)

> 작성일 2026-06-10. 외부 분석 작업(krx-mktinfo-queries)에서 **KRX 상장사 배당 사유 뉴스**를
> DeepSearch `DocumentSearch`로 조회하며 겪은 시행착오와 확정된 동작 규칙을 정리한다.
> 목적: 이 레포(`deepsearch`)에 **재사용 가능한 뉴스 검색 클라이언트 + 함정 문서화**를 추가하기 위한 근거.

---

## 0. 한 줄 요약

`DocumentSearch`는 잘 동작하지만 **두 가지 함정**에 막혀 한참 헤맸다:
1. **비로그인은 검색 기간이 1년을 넘으면 결과를 통째로 못 받는다** (`RequestEntityTooLarge`).
   → 증상이 "결과 0건"으로만 보여 엉뚱한 원인(`fields`, `OR 괄호`)을 의심하게 만든다 (둘 다 **무죄**).
2. 문서 리스트의 JSON 키가 `documents`가 아니라 **`docs`**. (직관과 어긋나 0건으로 오인.)

이 둘만 알면 한국 중소형주 과거 뉴스(공시·배당·무상증자)를 매우 잘 찾는다. 범용 웹서치가
0건이던 종목들(세진중공업·삼보판지·세코닉스·JW홀딩스 등)을 전건 확보했다.

---

## 1. 동작하는 최소 호출 (정답 레시피)

```python
import os, urllib.parse, requests
from dotenv import load_dotenv
load_dotenv()                                  # API_KEY (.env, base64 132자)
KEY = os.getenv("API_KEY")
requests.packages.urllib3.disable_warnings()   # self-signed → verify=False 경고 끄기

query = 'DocumentSearch(["news"],[],"securities.name:유한양행 and 배당",count=3,date_from=20230101,date_to=20231231)'
url = "https://api.deepsearch.com/v1/compute?input=" + urllib.parse.quote(query)  # 한글/괄호 인코딩 필수
d = requests.get(url, headers={"Authorization": f"Basic {KEY}"}, verify=False, timeout=40).json()

# 응답 구조: data.pods[0]=Input(해석), data.pods[1]=Result:DocumentSearchResult
docs  = d["data"]["pods"][1]["content"]["data"]["docs"]          # ← 'docs' (NOT 'documents')
total = d["data"]["pods"][1]["content"]["data"]["total_matches"]
exc   = d["data"]["exceptions"]                                   # 비었으면 정상
```

### 응답 `data` 한 꺼풀
- `pods[0].class == "Input"` — 쿼리 해석(plaintext/tagged). **데이터 아님.**
- `pods[1].class == "Result:DocumentSearchResult"`, `content.data` =
  `{ profile, cluster_info, total_matches, max_score, scroll_id, current_page, last_page, docs:[...] }`
- 각 doc 필드: `title, publisher, author, created_at, content(요약), content_url, securities[], entities[],
  industry{label,name,score}, polarity{label,name,score}, esg{...}` 등.
- **에러는 HTTP 200 + `data.exceptions`** 에 담겨 온다 (status code로는 안 보임). 비면 정상.

---

## 2. 시행착오 타임라인 (무엇을 오진했나)

| 순서 | 한 일 | 결과 | 내 (당시) 진단 | 실제 |
|---|---|---|---|---|
| ① | `fields=[...]` + 3개월 윈도우 | pods 1개처럼 보임(출력 truncate) | "**fields가 결과를 깬다**" | 오진 — 출력만 잘렸음 |
| ② | `fields` 빼고 호출 | `Result` pod 나옴 | "fields 확정 범인" | 오진(상관관계 착시) |
| ③ | 파서가 `data['documents']` 조회 | 항상 0건 | "API가 0 반환" | **키가 `docs`** |
| ④ | `(배당 or 무상증자)` OR + 18개월 | pods 1개 | "**OR 괄호+date가 파서 깸**" | 오진 |
| ⑤ | 단일 키워드 + 18개월 | pods 1개 | "date 형식 문제?" | 18개월=**1년 초과** |
| ⑥ | `data.exceptions` 확인 | `RequestEntityTooLarge: "Not allowed to search more than 1 year if not logged in"` | — | **진짜 원인 확정** |

**교훈**: 결과가 비면 **가장 먼저 `data.exceptions`를 봐라.** 그러면 ①~⑤의 헛수고가 전부 사라진다.

---

## 3. 확정된 규칙 (모두 1년 이내 윈도우로 재검증 완료)

| 항목 | 결론 | 검증 |
|---|---|---|
| **검색 기간 한도** | **비로그인 ≤ 1년** (366일 OK, 15개월·18개월·24개월 FAIL) | `유한양행 배당` 20230101→20240102 OK / →20240401 FAIL |
| `fields=[...]` | **정상** (1년 내) | plain vs +fields 동일 결과 |
| `(A or B)` OR 괄호 | **정상** (1년 내) | OR이 단일보다 total↑(35 vs 29) — 정상 합집합 |
| `date_from`/`date_to` 형식 | `YYYYMMDD` (따옴표 없이), 콤마 파라미터 | 동작 |
| 문서 리스트 키 | `content.data["docs"]` | — |
| 에러 전달 | HTTP 200 + `data.exceptions[]` | RequestEntityTooLarge 등 |
| 한글/괄호 | `urllib.parse.quote` 필수 | — |
| 콘솔 출력 | Windows CP949라 한글 깨짐 → **UTF-8 파일로 덤프 후 확인** | — |
| 종목 매핑 | `securities.name:종목명` / `securities.symbol:000100` 둘 다 | 상장사 한정 매핑 |

> **1년 초과가 필요하면**: 윈도우를 ≤1년 청크로 쪼개 각각 호출하고 `content_url` 기준 dedup·merge.
> (로그인 세션을 쓰면 한도가 풀릴 수 있으나, 현재 파이프라인은 `Authorization: Basic` 키 only.)

---

## 4. 재사용 헬퍼 (이 레포에 정식 모듈로 승격 권장)

```python
import os, time, urllib.parse, requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv(); KEY = os.getenv("API_KEY")
requests.packages.urllib3.disable_warnings()
BASE = "https://api.deepsearch.com/v1/compute?input="

def _compute(q):
    url = BASE + urllib.parse.quote(q)
    for _ in range(3):
        try:
            return requests.get(url, headers={"Authorization": f"Basic {KEY}"},
                                verify=False, timeout=40).json()
        except Exception:
            time.sleep(2)
    return {}

def _windows(df, dt):                       # 'YYYYMMDD' 범위 → ≤1년 청크
    f = date(int(df[:4]), int(df[4:6]), int(df[6:]))
    t = date(int(dt[:4]), int(dt[4:6]), int(dt[6:]))
    out = []
    while f <= t:
        end = min(t, f.replace(year=f.year + 1) - timedelta(days=1))
        out.append((f.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
        f = end + timedelta(days=1)
    return out

def document_search(query, category="news", section="", count=10,
                    date_from=None, date_to=None):
    """docs 리스트 + total 반환. 1년 초과 윈도우는 자동 분할·병합(content_url dedup)."""
    sec = f'["{section}"]' if section else "[]"
    spans = _windows(date_from, date_to) if (date_from and date_to) else [(None, None)]
    seen, docs, total = set(), [], 0
    for df, dt in spans:
        p = f'["{category}"],{sec},"{query}",count={count}'
        if df:
            p += f",date_from={df},date_to={dt}"
        d = _compute(f"DocumentSearch({p})")
        exc = d.get("data", {}).get("exceptions") or []
        if exc:
            raise RuntimeError(exc)          # 1년 초과 등은 분할로 이미 회피됨
        pods = d.get("data", {}).get("pods", [])
        if len(pods) < 2:
            continue
        data = pods[1]["content"]["data"]
        total += data.get("total_matches", 0)
        for doc in data.get("docs", []):
            k = doc.get("content_url") or doc.get("title")
            if k not in seen:
                seen.add(k); docs.append(doc)
    docs.sort(key=lambda x: x.get("created_at", ""))
    return docs, total
```

사용 예:
```python
docs, total = document_search("securities.name:세진중공업 and (배당 or 무상증자)",
                              date_from="20200101", date_to="20211231")  # 2년 → 자동 2분할
```

---

## 5. 부가 관찰

- **결산배당 사유 뉴스 타이밍**: 무상증자는 사업연도(FY) 중, 결산배당 결정은 **FY+1년 2~3월** 공시.
  특정 FY 배당 "왜?"를 찾으려면 **FY년(무상)·FY+1년(배당) 두 윈도우**를 보는 게 정석.
- `polarity.name`(긍/부정/중립), `securities`, `entities`가 doc에 함께 와서 1차 필터에 유용.
- `count`는 페이지당 최대치(문서상 ≤100), 더 받으려면 `page`로 페이징.
- 범용 웹서치(영문권) 대비 **한국 중소형주 과거 뉴스 커버리지가 압도적**. KRX 업무에 이 API가 정답.

---

## 6. 개선 제안 (이 레포에 반영할 것)

1. **`newsscrap/ds_client.py`** (또는 `deepsearch/scripts/`)에 §4 헬퍼를 정식 모듈로 추가
   — `document_search`, `_windows`(1년 자동분할), 공통 `_compute`(retry·exceptions 처리).
2. `deepsearch_query.py`·`deepsearch_query_api.py`의 인라인 호출을 이 클라이언트로 일원화
   (현재 `data['pods'][1]['content']['data']` 파싱이 곳곳에 중복).
3. **`docs/`에 함정 문서** 추가(또는 `3_API함수를_통한_데이터_조회_문서검색.md` 하단에 박스):
   - 1년 한도 / `data.exceptions` 먼저 보기 / `docs` 키 / URL 인코딩 / CP949.
4. **`SKILL.md`(deepsearch)** 의 DocumentSearch 섹션에 위 4줄 gotcha를 명시
   — 향후 에이전트가 같은 시행착오를 반복하지 않도록.
5. (선택) `document_search`에 `to_dataframe=True` 옵션 + UTF-8 CSV 덤프 헬퍼.

---

## 부록 A — 검증 로그(요약)

```
fields/OR/경계 (모두 '유한양행 and 배당', 2023 통제):
  plain  20230101-20231231 : OK total=29 docs=2
  +fields                  : OK total=29 docs=2     # fields 무죄
  OR(배당 or 무상증자)       : OK total=35 docs=3     # OR 무죄(합집합 정상)
  OR+fields                : OK total=35 docs=3
1년 경계:
  →20240102 (366d)         : OK
  →20240401 (15m)          : FAIL  RequestEntityTooLarge
  →20240701 (18m)          : FAIL
  →20250101 (24m)          : FAIL
키:
  data['documents']        → 없음(0건 오인)
  data['docs']             → 정답
```
