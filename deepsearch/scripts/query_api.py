#!/usr/bin/env python3
"""
DeepSearch API 호출 스크립트 (공통)

사용법:
    python query_api.py <API_KEY> <QUERY>

예시:
    python query_api.py "KEY" 'DocumentSearch(["news"],["economy"],"삼성전자",count=10,page=1)'
    python query_api.py "KEY" '삼성전자 매출액 2020-2024'

의존성: requests (pip install requests)
"""

import sys
import json
import time
import re
import base64
from urllib.parse import quote

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print(json.dumps({'success': False, 'error': 'requests 라이브러리가 필요합니다: pip install requests'}, ensure_ascii=False))
    sys.exit(1)

URL_BASE = 'https://api.deepsearch.com/v1/compute?input='


def _normalize_api_key(api_key):
    """API 키를 base64 형식으로 정규화. raw(id:secret) 형식이면 자동 인코딩."""
    if ':' in api_key:
        return base64.b64encode(api_key.encode()).decode()
    return api_key


def make_request(url, headers, max_retries=3, retry_delay=5):
    """API 요청. 실패 시 재시도. 4xx 클라이언트 에러는 즉시 실패."""
    attempt = 0
    last_error = None
    while attempt < max_retries:
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            if resp.status_code in (400, 403, 413):
                raise Exception(f"{resp.status_code} {resp.reason}: URL이 너무 길거나 인증 실패. 쿼리를 줄이거나 API 키를 확인하세요.")
            last_error = e
            attempt += 1
            if attempt < max_retries:
                print(f"[retry {attempt}/{max_retries}] {str(e)[:200]}", file=sys.stderr)
                time.sleep(retry_delay)
        except Exception as e:
            last_error = e
            attempt += 1
            if attempt < max_retries:
                print(f"[retry {attempt}/{max_retries}] {str(e)[:200]}", file=sys.stderr)
                time.sleep(retry_delay)
    raise Exception(f"Max retries exceeded: {last_error}")


def execute_query(api_key, query):
    """DeepSearch API 쿼리 실행."""
    headers = {'Authorization': f'Basic {_normalize_api_key(api_key)}'}
    clean_query = query.replace('\n', '').strip()
    url = f'{URL_BASE}{quote(clean_query, safe="")}'

    response_data = make_request(url, headers)

    if not response_data.get('success', False):
        exceptions = response_data.get('data', {}).get('exceptions', [])
        return {'success': False, 'error': exceptions or 'API 요청 실패', 'query': clean_query}

    pods = response_data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return {'success': True, 'query': clean_query, 'pods': pods}

    result_pod = pods[1]
    pod_class = result_pod.get('class', '')

    if pod_class == 'Result:DocumentSearchResult':
        return handle_doc_search(result_pod, clean_query, headers)

    return {
        'success': True,
        'query': clean_query,
        'pod_class': pod_class,
        'data': result_pod.get('content', {})
    }


def handle_doc_search(result_pod, original_query, headers):
    """DocumentSearch 결과 + 자동 페이지네이션 (최대 5페이지)."""
    content = result_pod.get('content', {})
    data = content.get('data', {}) if isinstance(content, dict) else {}
    total_matches = data.get('total_matches', 0)
    last_page = data.get('last_page', 1)
    current_page = data.get('current_page', 1)
    all_docs = data.get('docs', [])
    max_pages = min(last_page, 5)

    while current_page < max_pages:
        current_page += 1
        paged_query = re.sub(r'page\s*=\s*\d+', f'page={current_page}', original_query)
        url = f'{URL_BASE}{quote(paged_query, safe="")}'
        try:
            page_data = make_request(url, headers)
            if page_data.get('success'):
                pp = page_data.get('data', {}).get('pods', [])
                if len(pp) >= 2:
                    docs = pp[1].get('content', {}).get('data', {}).get('docs', [])
                    all_docs.extend(docs)
        except Exception as e:
            print(f"[page {current_page}] failed: {str(e)[:200]}", file=sys.stderr)
            break

    summarized = []
    for doc in all_docs:
        s = {
            'title': doc.get('title', ''),
            'publisher': doc.get('publisher', ''),
            'created_at': doc.get('created_at', ''),
            'category': doc.get('category', ''),
            'section': doc.get('section', ''),
            'content': doc.get('content', '')[:500],
            'content_url': doc.get('content_url', ''),
        }
        secs = doc.get('securities', [])
        if secs:
            s['securities'] = [{'name': x.get('name',''), 'symbol': x.get('symbol',''), 'market': x.get('market','')} for x in secs]
        pol = doc.get('polarity', {})
        if pol:
            s['polarity'] = pol.get('name', '')
        esg = doc.get('esg', {})
        if esg and esg.get('category', {}).get('name'):
            s['esg'] = {'category': esg['category'].get('name',''), 'polarity': esg.get('polarity',{}).get('name','')}
        summarized.append(s)

    return {
        'success': True,
        'query': original_query,
        'pod_class': 'Result:DocumentSearchResult',
        'total_matches': total_matches,
        'total_pages': last_page,
        'fetched_pages': min(current_page, max_pages),
        'doc_count': len(summarized),
        'docs': summarized
    }


def main():
    # Windows 환경에서 한글 출력 깨짐 방지
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 3:
        print(json.dumps({'success': False, 'error': 'Usage: python query_api.py <API_KEY> <QUERY>'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    api_key = sys.argv[1]
    query = sys.argv[2]

    try:
        result = execute_query(api_key, query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e), 'query': query}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
