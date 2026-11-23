"""재작성 검증 공통 모듈: 키 로드, OpenDART / DeepSearch 호출(캐시·재시도).

키:
- DeepSearch: 레포 루트 .env 의 API_KEY
- OpenDART : 환경변수 DART_API_KEY (없으면 레포 루트 .env 의 DART_API_KEY)
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

requests.packages.urllib3.disable_warnings()

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = HERE / "data"
CACHE = DATA / "cache"          # 원시 응답 캐시 (git 제외)
CACHE.mkdir(parents=True, exist_ok=True)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _env_file() -> dict[str, str]:
    env = {}
    p = REPO / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


_ENV = _env_file()


def _key(name: str) -> str:
    v = os.environ.get(name) or _ENV.get(name)
    if not v:
        raise SystemExit(f"{name} 가 환경변수나 .env 에 없습니다.")
    return v


def _cache_get(kind: str, key: str):
    p = CACHE / kind / (hashlib.sha1(key.encode()).hexdigest() + ".json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _cache_put(kind: str, key: str, obj) -> None:
    d = CACHE / kind
    d.mkdir(exist_ok=True)
    (d / (hashlib.sha1(key.encode()).hexdigest() + ".json")).write_text(
        json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _get_json(url, params=None, headers=None, retries=4, timeout=180):
    last = None
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, verify=False, timeout=timeout)
            if r.status_code in (400, 401, 403):
                r.raise_for_status()
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code in (400, 401, 403):
                raise
            last = e
        except Exception as e:  # 네트워크/JSON 오류
            last = e
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"요청 실패: {last}")


# ---------------------------------------------------------------- OpenDART
DART = "https://opendart.fss.or.kr/api"


def dart(endpoint: str, **params) -> dict:
    key = endpoint + json.dumps(params, sort_keys=True)
    hit = _cache_get("dart", key)
    if hit is not None:
        return hit
    j = _get_json(f"{DART}/{endpoint}", params={"crtfc_key": _key("DART_API_KEY"), **params})
    # 000 정상, 013 데이터 없음 → 둘 다 캐시. 020(한도초과) 등은 예외
    if j.get("status") not in ("000", "013"):
        raise RuntimeError(f"OpenDART {endpoint} {params.get('bsns_year')}: {j.get('status')} {j.get('message')}")
    _cache_put("dart", key, j)
    return j


# -------------------------------------------------------------- DeepSearch
DS = "https://api.deepsearch.com/v1/compute?input="


def _ds_headers():
    k = _key("API_KEY")
    if ":" in k:
        k = base64.b64encode(k.encode()).decode()
    return {"Authorization": f"Basic {k}"}


def ds(query: str) -> dict | None:
    """DeepSearch compute 호출. 결과 DataFrame dict({col: [..]}) 또는 None."""
    hit = _cache_get("ds", query)
    if hit is None:
        j = _get_json(DS + quote(query, safe=""), headers=_ds_headers())
        hit = {"success": j.get("success"),
               "exceptions": (j.get("data") or {}).get("exceptions"),
               "data": None}
        pods = (j.get("data") or {}).get("pods") or []
        if j.get("success") and len(pods) > 1:
            hit["data"] = pods[1].get("content", {}).get("data")
        _cache_put("ds", query, hit)
    return hit["data"]


def to_num(s):
    """'1,234' / '-1,234' / '' → float | None"""
    if s is None:
        return None
    s = str(s).replace(",", "").strip()
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None
