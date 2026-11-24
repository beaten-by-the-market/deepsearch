"""
DeepSearch 스킬 스크립트 공통 모듈.

- API 키 찾기: 명령행 첫 인자(구 방식) > 환경변수 DEEPSEARCH_API_KEY / API_KEY > .env 파일
- compute 호출: URL 인코딩, 재시도, HTTP 4xx 본문의 data.exceptions까지 읽어서 원인을 돌려줌
- 결과 출력: 작으면 그대로 출력, 크면 JSON 파일로 저장하고 미리보기만 출력
  (Claude Code는 Bash 출력을 약 3만 자에서 자르므로 큰 결과를 stdout에 그대로 내면 데이터가 사라진다)

API 키 값은 출력·로그·파일 어디에도 쓰지 않는다.
"""

import base64
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print(json.dumps({'success': False, 'error': 'requests 라이브러리가 필요합니다: pip install requests'},
                     ensure_ascii=False))
    sys.exit(1)

API_HOST = 'https://api.deepsearch.com'   # app-api.deepsearch.com도 동일하게 동작

# stdout에 그대로 내보낼 최대 글자 수. 넘으면 파일로 저장한다.
MAX_STDOUT_CHARS = 20000

_KEY_LIKE = re.compile(r'^[A-Za-z0-9+/=_\-:.]{20,}$')
_ENV_NAMES = ('DEEPSEARCH_API_KEY', 'API_KEY')


def setup_stdout():
    """Windows 콘솔(CP949)에서 한글이 깨지지 않게 stdout/stderr를 UTF-8로."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except Exception:
            pass


def fail(message, **extra):
    print(json.dumps({'success': False, 'error': message, **extra}, ensure_ascii=False, indent=2))
    sys.exit(1)


# ---------------------------------------------------------------- API 키

def normalize_api_key(api_key):
    """raw(id:secret) 형식이면 base64로 인코딩, 이미 base64면 그대로."""
    api_key = api_key.strip().strip('"').strip("'")
    if ':' in api_key:
        return base64.b64encode(api_key.encode()).decode()
    return api_key


def _read_env_file(path):
    values = {}
    try:
        with open(path, encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                if k.startswith('export '):
                    k = k[len('export '):].strip()
                values[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def _env_file_candidates():
    """현재 폴더와 그 상위, 스크립트 폴더와 그 상위(스킬 폴더·레포 루트)의 .env."""
    seen = []
    for start in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        d = os.path.abspath(start)
        while True:
            p = os.path.join(d, '.env')
            if p not in seen:
                seen.append(p)
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return seen


def find_api_key():
    for name in _ENV_NAMES:
        if os.environ.get(name):
            return normalize_api_key(os.environ[name])
    for path in _env_file_candidates():
        if os.path.isfile(path):
            values = _read_env_file(path)
            for name in _ENV_NAMES:
                if values.get(name):
                    return normalize_api_key(values[name])
    return None


def pop_api_key(args):
    """
    args(sys.argv[1:] 복사본)에서 API 키를 꺼낸다.

    구 방식 호환: 첫 인자가 키처럼 생겼으면(영숫자·base64 문자 20자 이상, URL 아님) 키로 쓴다.
    아니면 환경변수/.env에서 찾는다. 못 찾으면 안내 메시지를 내고 종료.
    """
    if args and _KEY_LIKE.match(args[0]) and not args[0].lower().startswith('http'):
        return normalize_api_key(args.pop(0)), args
    key = find_api_key()
    if not key:
        fail('DeepSearch API 키를 찾지 못했습니다. 프로젝트 루트 .env에 API_KEY=<키>를 넣거나 '
             '환경변수 DEEPSEARCH_API_KEY를 설정하세요. (키 값을 화면에 출력하지 마세요)')
    return key, args


# ---------------------------------------------------------------- 호출

class DeepSearchError(Exception):
    def __init__(self, message, exceptions=None, status=None):
        super().__init__(message)
        self.exceptions = exceptions or []
        self.status = status


def _exception_text(exceptions):
    parts = []
    for e in exceptions:
        if isinstance(e, dict):
            args = e.get('args') or []
            parts.append(f"{e.get('class', 'Error')}: {' / '.join(str(a) for a in args)}")
        else:
            parts.append(str(e))
    return '; '.join(parts)


def hint_for(exceptions_text):
    t = exceptions_text or ''
    if 'more than 1 year' in t or 'RequestEntityTooLarge' in t:
        return ('검색 기간이 1년을 넘었습니다(비로그인 한도). DocumentSearch는 query_api.py가 1년 단위로 '
                '자동 분할합니다. 다른 함수는 기간을 1년 이하로 나눠 호출하세요.')
    if 'NameError' in t:
        if 'UFunction' in t:
            return ('이 이름의 함수가 없습니다. 오타가 아니면 현재 구독으로 쓸 수 없는 함수입니다(채권·통계청 등). '
                    '쓸 수 있는 함수 목록: 레포 docs/reference/DEEPSEARCH_API_MASTER.md 17절, SKILL.md "쓰지 마세요".')
        return '인자 이름이 정의되지 않았습니다. 자리표시자(inst_code 등) 대신 실제 값을 넣으세요.'
    return None


def compute(api_key, query, max_retries=3, retry_delay=3, timeout=60):
    """
    compute 엔드포인트 호출 → 응답 JSON(dict).

    - POST {"input": query}로 보낸다(URL 길이·인코딩 문제 없음. GET과 결과 동일, 2026-11-25 확인).
    - HTTP 4xx여도 본문의 data.exceptions를 읽어 원인을 DeepSearchError로 올린다(재시도 안 함).
    - HTTP 200 + data.exceptions도 DeepSearchError.
    - 네트워크 오류·5xx는 재시도.
    """
    return _request(api_key, 'POST', API_HOST + '/v1/compute',
                    {'input': query.replace('\n', ' ').strip()}, max_retries, retry_delay, timeout)


def rest_get(api_key, path, max_retries=2, retry_delay=3, timeout=120):
    """compute가 아닌 REST 경로(예: /v1/topic-insight/insight?...)를 GET으로 호출."""
    return _request(api_key, 'GET', API_HOST + path, None, max_retries, retry_delay, timeout)


def _request(api_key, method, url, body_json, max_retries, retry_delay, timeout):
    headers = {'Authorization': f'Basic {api_key}'}
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.request(method, url, json=body_json, headers=headers, verify=False, timeout=timeout)
        except Exception as e:  # 네트워크 오류
            last_error = e
        else:
            try:
                body = resp.json()
            except ValueError:
                body = None
            data = (body or {}).get('data') if isinstance(body, dict) else None
            exceptions = (data.get('exceptions') if isinstance(data, dict) else None) or []
            if exceptions:
                raise DeepSearchError(_exception_text(exceptions), exceptions, resp.status_code)
            if resp.status_code in (401, 403):
                detail = json.dumps(body, ensure_ascii=False)[:200] if body is not None else resp.reason
                raise DeepSearchError(f'{resp.status_code} 인증 실패: API 키를 확인하세요. 응답: {detail}',
                                      status=resp.status_code)
            if 400 <= resp.status_code < 500 and isinstance(body, dict) and body.get('error'):
                raise DeepSearchError(f"{resp.status_code}: {json.dumps(body['error'], ensure_ascii=False)[:200]}",
                                      status=resp.status_code)
            if 400 <= resp.status_code < 500:
                raise DeepSearchError(f'{resp.status_code} {resp.reason}: 쿼리 문법·함수 인자를 확인하세요.',
                                      status=resp.status_code)
            if resp.status_code < 400 and body is not None:
                return body
            last_error = f'{resp.status_code} {resp.reason}'
        if attempt < max_retries:
            print(f'[retry {attempt}/{max_retries}] {str(last_error)[:200]}', file=sys.stderr)
            time.sleep(retry_delay)
    raise DeepSearchError(f'재시도 {max_retries}회 실패: {last_error}')


def result_pod(body):
    pods = (body.get('data') or {}).get('pods') or []
    return pods[1] if len(pods) >= 2 else None


# ---------------------------------------------------------------- 출력

def dataframe_records(content):
    """Result:DataFrame content({columns, data:{col:[...]}}) → 행 리스트."""
    data = content.get('data') if isinstance(content, dict) else None
    if not isinstance(data, dict) or not data:
        return None
    cols = list(content.get('columns') or data.keys())
    cols = [c for c in cols if c in data]
    if not cols or not all(isinstance(data[c], list) for c in cols):
        return None
    n = len(data[cols[0]])
    return [{c: data[c][i] if i < len(data[c]) else None for c in cols} for i in range(n)]


def default_out_path(label):
    folder = os.path.join(tempfile.gettempdir(), 'deepsearch')
    os.makedirs(folder, exist_ok=True)
    slug = re.sub(r'[^0-9A-Za-z가-힣]+', '_', label)[:40].strip('_') or 'result'
    return os.path.join(folder, f"{datetime.now():%Y%m%d_%H%M%S}_{slug}.json")


def emit(result, preview, out=None, label='result'):
    """
    result 전체가 작고 out 지정이 없으면 그대로 출력.
    아니면 result 전체를 파일로 저장하고 preview(+saved_to)만 출력.
    """
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if out is None and len(text) <= MAX_STDOUT_CHARS:
        print(text)
        return
    path = os.path.abspath(out) if out else default_out_path(label)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    summary = dict(preview)
    summary['saved_to'] = path
    summary['saved_chars'] = len(text)
    summary['note'] = ('전체 결과는 saved_to 파일(UTF-8 JSON)에 있습니다. 화면에는 미리보기만 냈습니다. '
                       '필요한 항목은 파일을 Python으로 읽어 걸러 쓰세요.')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
