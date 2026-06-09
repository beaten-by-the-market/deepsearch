"""
================================================================================
ds_client.py — DeepSearch DocumentSearch 뉴스 검색 클라이언트
================================================================================

DeepSearch `DocumentSearch` API를 안전하게 호출하기 위한 재사용 모듈.
KRX 상장사 뉴스/공시/리서치 문서 검색에 사용한다.

⚠️ 실전 함정 4가지 (HANDOFF_DocumentSearch_news_20260610.md 검증됨)
--------------------------------------------------------------------------------
1. **검색 기간 1년 한도**: 비로그인(Authorization: Basic)은 검색 기간이 1년을
   넘으면 결과를 통째로 못 받는다(`RequestEntityTooLarge`). 증상이 "0건"으로만
   보여 엉뚱한 원인(fields, OR 괄호)을 의심하게 만든다 — 둘 다 무죄.
   → 이 모듈의 `document_search`는 1년 초과 윈도우를 ≤1년 청크로 자동 분할·병합한다.
2. **문서 리스트 키는 `docs`** (NOT `documents`). 직관과 어긋나 0건으로 오인하기 쉽다.
   파싱 경로: `data["pods"][1]["content"]["data"]["docs"]`.
3. **에러는 HTTP 200 + `data.exceptions[]`** 로 온다(status code로는 안 보임).
   → 결과가 비면 `data.exceptions`부터 확인. `_compute`가 있으면 RuntimeError로 올린다.
4. **한글/괄호는 `urllib.parse.quote` 필수**. 콘솔은 Windows CP949라 한글이 깨지니
   결과는 UTF-8 파일로 덤프해 확인한다.

공개 함수
--------------------------------------------------------------------------------
- document_search(query, category, section, count, date_from, date_to, api_key)
    → (docs: list[dict], total_matches: int)
- parse_search_content(response_json) → dict  (네트워크 없이 pod 파싱만)

사용 예
--------------------------------------------------------------------------------
    from ds_client import document_search
    docs, total = document_search("securities.name:유한양행 and 배당",
                                  date_from="20230101", date_to="20231231")
    # 2년 → 자동 2분할:
    docs, total = document_search("securities.name:세진중공업 and (배당 or 무상증자)",
                                  date_from="20200101", date_to="20211231")
================================================================================
"""

import os
import time
import base64
import urllib.parse
from datetime import date, timedelta

import requests

# self-signed 인증서 → verify=False 사용 시 경고 끄기
requests.packages.urllib3.disable_warnings()

BASE = "https://api.deepsearch.com/v1/compute?input="

# API 키 캐시 (최초 1회 .env 로드)
_API_KEY_CACHE = None


def _normalize_api_key(api_key):
    """API 키를 base64(Basic auth) 형식으로 정규화. raw(id:secret)면 자동 인코딩."""
    if not api_key:
        return None
    if ":" in api_key:
        return base64.b64encode(api_key.encode()).decode()
    return api_key


def _get_api_key(override=None):
    """API 키 로드. override > 캐시 > .env(API_KEY) 순. 비밀키 하드코딩 금지."""
    global _API_KEY_CACHE
    if override:
        return _normalize_api_key(override)
    if _API_KEY_CACHE:
        return _API_KEY_CACHE
    # 기존 패턴 재사용: 로컬은 .env에서 로드
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    _API_KEY_CACHE = _normalize_api_key(os.getenv("API_KEY"))
    return _API_KEY_CACHE


def _compute(query, api_key=None, retries=3, timeout=40):
    """
    DeepSearch compute 엔드포인트 호출.

    - URL 인코딩(`urllib.parse.quote`) + `Authorization: Basic` + verify=False
    - 네트워크 오류 시 최대 `retries`회 재시도(2초 간격)
    - 응답의 `data.exceptions`가 비어있지 않으면 RuntimeError로 올림
      (1년 초과 RequestEntityTooLarge 등 — 에러는 HTTP 200 + exceptions로 전달됨)

    Returns:
        dict: 파싱된 JSON 응답 (`data` 포함)

    Raises:
        RuntimeError: `data.exceptions`가 있을 때 (예: RequestEntityTooLarge)
        Exception: 재시도 소진 시 마지막 네트워크 오류
    """
    key = _get_api_key(api_key)
    url = BASE + urllib.parse.quote(query)
    headers = {"Authorization": f"Basic {key}"}

    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=timeout)
            data = resp.json()
            # 에러는 HTTP 200 + data.exceptions[]로 온다 → 먼저 확인
            exc = (data.get("data") or {}).get("exceptions") or []
            if exc:
                raise RuntimeError(f"DeepSearch exceptions: {exc}")
            return data
        except RuntimeError:
            raise  # exceptions는 재시도 무의미 — 즉시 전파
        except Exception as e:  # noqa: BLE001 (네트워크/파싱 오류 재시도)
            last_error = e
            if attempt < retries - 1:
                time.sleep(2)
    raise Exception(f"_compute 실패 (재시도 {retries}회 소진): {last_error}")


def _windows(date_from, date_to):
    """
    'YYYYMMDD' 범위를 ≤1년(366일 미만) 청크 리스트로 분할.

    비로그인 1년 한도를 회피하기 위함. 각 청크는 (date_from, date_to) 튜플.

    >>> _windows("20200101", "20211231")
    [('20200101', '20201231'), ('20210101', '20211231')]
    """
    f = date(int(date_from[:4]), int(date_from[4:6]), int(date_from[6:8]))
    t = date(int(date_to[:4]), int(date_to[4:6]), int(date_to[6:8]))
    out = []
    while f <= t:
        # f 로부터 1년 - 1일 (윤년 안전하게 replace 사용)
        try:
            one_year = f.replace(year=f.year + 1) - timedelta(days=1)
        except ValueError:  # 2/29 → 다음해 2/28 보정
            one_year = f.replace(year=f.year + 1, day=28) - timedelta(days=1)
        end = min(t, one_year)
        out.append((f.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
        f = end + timedelta(days=1)
    return out


def parse_search_content(response_json):
    """
    DocumentSearch 응답에서 결과 content 딕셔너리를 추출(네트워크 없음).

    응답 구조: data.pods[0]=Input(해석), data.pods[1]=Result:DocumentSearchResult
    반환 dict 키: docs, total_matches, last_page, current_page 등.

    Returns:
        dict: pods[1]["content"]["data"]. pod가 없으면 빈 dict.

    Raises:
        RuntimeError: `data.exceptions`가 있을 때.
    """
    data = response_json.get("data") or {}
    exc = data.get("exceptions") or []
    if exc:
        raise RuntimeError(f"DeepSearch exceptions: {exc}")
    pods = data.get("pods") or []
    if len(pods) < 2:
        return {}
    return pods[1].get("content", {}).get("data", {}) or {}


def document_search(query, category="news", section="", count=10,
                    date_from=None, date_to=None, api_key=None):
    """
    DocumentSearch 호출 후 docs 리스트 + total_matches 반환.

    1년 초과 윈도우는 자동으로 ≤1년 청크로 분할·호출한 뒤 `content_url` 기준으로
    중복 제거(dedup)·병합한다. 결과는 created_at 오름차순 정렬.

    Args:
        query (str): 검색 쿼리. 예: "securities.name:유한양행 and 배당"
        category (str): 문서 카테고리. news / research / company / patent. 기본 "news".
        section (str): 섹션(예: "economy"). 빈 문자열이면 전체("[]").
        count (int): 윈도우(페이지)당 결과 수(≤100). 기본 10.
        date_from (str|None): 시작일 'YYYYMMDD'. None이면 기간 미지정.
        date_to (str|None): 종료일 'YYYYMMDD'. None이면 기간 미지정.
        api_key (str|None): 명시적 API 키. None이면 .env의 API_KEY 사용.

    Returns:
        tuple[list[dict], int]: (docs, total_matches)

    Raises:
        RuntimeError: 분할로도 회피 못한 data.exceptions 발생 시.
    """
    sec = f'["{section}"]' if section else "[]"
    spans = _windows(date_from, date_to) if (date_from and date_to) else [(None, None)]

    seen, docs, total = set(), [], 0
    for df, dt in spans:
        params = f'["{category}"],{sec},"{query}",count={count}'
        if df:
            params += f",date_from={df},date_to={dt}"
        resp = _compute(f"DocumentSearch({params})", api_key=api_key)
        content = parse_search_content(resp)
        if not content:
            continue
        total += content.get("total_matches", 0)
        for doc in content.get("docs", []):
            key = doc.get("content_url") or doc.get("title")
            if key not in seen:
                seen.add(key)
                docs.append(doc)
    docs.sort(key=lambda x: x.get("created_at", ""))
    return docs, total


if __name__ == "__main__":
    # 간단한 수동 점검 (test_ds_client.py가 정식 스모크 테스트)
    d, t = document_search("securities.name:유한양행 and 배당",
                           date_from="20230101", date_to="20231231", count=3)
    print(f"docs={len(d)} total={t}")
