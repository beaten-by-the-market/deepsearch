#!/usr/bin/env python3
r"""
DeepSearch API 호출 스크립트 (공통)

사용법:
    python query_api.py "쿼리" [옵션]
    python query_api.py <API_KEY> "쿼리" [옵션]     # 구 방식 (키를 직접 넘김)

API 키는 환경변수 DEEPSEARCH_API_KEY / API_KEY, 또는 현재 폴더·상위 폴더의 .env(API_KEY=...)에서 읽습니다.

옵션:
    --out PATH          전체 결과를 PATH에 JSON으로 저장 (화면에는 미리보기만)
    --max-pages N       DocumentSearch에서 기간 구간마다 가져올 페이지 수 (기본 1)
    --grep REGEX        DataFrame 결과에서 글자 칸이 REGEX에 맞는 행만 남김
                        예: --grep "^(수익|영업이익\(손실\)|총당기순이익)$"  (재무제표 계정명)
    --content-chars N   DocumentSearch 문서 요약(content) 길이 (기본 300)

동작:
    - DocumentSearch 기간이 1년을 넘으면 1년 이하 구간으로 나눠 호출하고 content_url로 중복 제거 (최신순 정렬)
    - 에러는 DeepSearch가 준 원인(data.exceptions)과 힌트를 그대로 보여줌
    - 결과 JSON이 2만 자를 넘으면 임시 폴더에 저장하고 경로·미리보기만 출력
      (Claude Code는 긴 Bash 출력을 잘라내므로)

예시:
    python query_api.py 'DocumentSearch(["news"],["economy"],"securities.name:삼성전자",count=100,page=1,date_from=20230101,date_to=20241231)'
    python query_api.py 'GetFinancialStatements(삼성전자, consolidated=True, date_from=2020-01-01, date_to=2024-12-31)' --grep "^(수익|영업이익\(손실\))$"
    python query_api.py '삼성전자 종가 2024-06-01-2024-06-30'
    python query_api.py '/v1/topic-insight/insight?type=trending&section=economy&topicId=176349687&stream=false'

"/"로 시작하면 compute가 아닌 REST 경로로 보고 https://api.deepsearch.com + 경로를 GET합니다(토픽 인사이트 등).

의존성: requests (pip install requests)
"""

import argparse
import os
import re
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ds_common import (DeepSearchError, compute, dataframe_records, emit, fail, fail_error,  # noqa: E402
                        pop_api_key, rest_get, result_pod, setup_stdout)

PREVIEW_ROWS = 10
_DATE_RE = r'(\b{name}\s*=\s*)(["\']?)(\d{{4}})(-?)(\d{{2}})-?(\d{{2}})\2'


# ---------------------------------------------------------------- DocumentSearch 기간 분할

def _find_date(query, name):
    m = re.search(_DATE_RE.format(name=name), query)
    if not m:
        return None, None
    return date(int(m.group(3)), int(m.group(5)), int(m.group(6))), m


def _set_date(query, name, value):
    def repl(m):
        dash = m.group(4)
        text = value.strftime('%Y-%m-%d') if dash else value.strftime('%Y%m%d')
        return f'{m.group(1)}{m.group(2)}{text}{m.group(2)}'
    return re.sub(_DATE_RE.format(name=name), repl, query, count=1)


def _windows(f, t):
    """[f, t]를 1년 이하 구간으로 나눔. 각 구간은 (시작, 끝)."""
    out = []
    while f <= t:
        try:
            one_year = f.replace(year=f.year + 1) - timedelta(days=1)
        except ValueError:  # 2/29
            one_year = f.replace(year=f.year + 1, day=28)
        end = min(t, one_year)
        out.append((f, end))
        f = end + timedelta(days=1)
    return out


def _set_page(query, page):
    if re.search(r'\bpage\s*=\s*\d+', query):
        return re.sub(r'\bpage\s*=\s*\d+', f'page={page}', query, count=1)
    i = query.rstrip().rfind(')')
    return query[:i] + f',page={page}' + query[i:]


def _summarize_doc(doc, content_chars):
    s = {
        'title': doc.get('title', ''),
        'publisher': doc.get('publisher', ''),
        'created_at': doc.get('created_at', ''),
        'category': doc.get('category', ''),
        'section': doc.get('section', ''),
        'content': (doc.get('content') or '')[:content_chars],
        'content_url': doc.get('content_url', ''),
    }
    secs = doc.get('securities') or []
    if secs:
        s['securities'] = [{'name': x.get('name', ''), 'symbol': x.get('symbol', ''), 'market': x.get('market', '')}
                           for x in secs]
    pol = doc.get('polarity') or {}
    if pol.get('name'):
        s['polarity'] = pol['name']
    esg = doc.get('esg') or {}
    if (esg.get('category') or {}).get('name'):
        s['esg'] = {'category': esg['category']['name'], 'polarity': (esg.get('polarity') or {}).get('name', '')}
    return s


def run_document_search(api_key, query, max_pages, content_chars):
    d_from, _ = _find_date(query, 'date_from')
    d_to, _ = _find_date(query, 'date_to')
    if d_from and d_to and d_from > d_to:
        fail(f'date_from({d_from})이 date_to({d_to})보다 늦습니다.', query=query)
    spans = _windows(d_from, d_to) if (d_from and d_to) else [(None, None)]

    m = re.search(r'\bpage\s*=\s*(\d+)', query)
    start_page = int(m.group(1)) if m else 1

    seen, docs, windows, total = set(), [], [], 0
    for f, t in spans:
        q = query
        if f:
            q = _set_date(_set_date(q, 'date_from', f), 'date_to', t)
        info = {'date_from': f.isoformat() if f else None, 'date_to': t.isoformat() if t else None}
        page, last_page = start_page, start_page
        while page < start_page + max_pages and page <= last_page:
            pod = result_pod(compute(api_key, _set_page(q, page)))
            data = ((pod or {}).get('content') or {}).get('data') or {}
            if page == start_page:
                info['total_matches'] = data.get('total_matches', 0)
                total += info['total_matches']
                last_page = data.get('last_page', start_page) or start_page
                info['last_page'] = last_page
            for doc in data.get('docs') or []:
                key = doc.get('content_url') or (doc.get('title'), doc.get('created_at'))
                if key not in seen:
                    seen.add(key)
                    docs.append(_summarize_doc(doc, content_chars))
            info['fetched_pages'] = page - start_page + 1
            page += 1
        windows.append(info)

    docs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    result = {
        'success': True,
        'query': query,
        'pod_class': 'Result:DocumentSearchResult',
        'total_matches': total,
        'doc_count': len(docs),
        'windows': windows,
        'docs': docs,
    }
    if len(spans) > 1:
        result['split_note'] = f'기간이 1년을 넘어 {len(spans)}개 구간으로 나눠 조회했습니다(비로그인 한도).'
    preview = {k: v for k, v in result.items() if k != 'docs'}
    preview['docs_preview'] = [
        {'created_at': d['created_at'], 'title': d['title'], 'publisher': d['publisher'],
         'securities': [s['name'] for s in d.get('securities', [])][:5]}
        for d in docs[:PREVIEW_ROWS]
    ]
    return result, preview


# ---------------------------------------------------------------- 그 밖의 쿼리

def run_rest(api_key, path):
    """'/v1/...' REST 경로 (토픽 인사이트 등)."""
    body = rest_get(api_key, path)
    if not isinstance(body, dict):
        body = {'data': body}
    result = {'success': bool(body.get('success', True)), 'query': path, 'data': body.get('data', body)}
    return result, {**result, 'data': str(result['data'])[:3000]}


def run_generic(api_key, query, grep):
    body = compute(api_key, query)
    pod = result_pod(body)
    if pod is None:
        pods = (body.get('data') or {}).get('pods') or []
        result = {'success': True, 'query': query, 'note': '결과 pod가 없습니다(쿼리 해석만 반환됨). 쿼리 문법을 확인하세요.',
                  'pods': pods}
        return result, result

    pod_class = pod.get('class', '')
    content = pod.get('content', {})
    records = dataframe_records(content) if pod_class == 'Result:DataFrame' else None

    if records is None:
        result = {'success': True, 'query': query, 'pod_class': pod_class, 'data': content}
        preview = {'success': True, 'query': query, 'pod_class': pod_class,
                   'data_preview': str(content)[:3000]}
        return result, preview

    total_rows = len(records)
    if grep:
        records = [r for r in records if any(isinstance(v, str) and grep.search(v) for v in r.values())]
    columns = list(records[0].keys()) if records else list(content.get('columns') or [])
    result = {'success': True, 'query': query, 'pod_class': pod_class, 'columns': columns,
              'row_count': len(records), 'rows': records}
    if grep:
        result['grep'] = grep.pattern
        result['rows_before_grep'] = total_rows
    preview = {k: v for k, v in result.items() if k != 'rows'}
    preview['rows_preview'] = records[:PREVIEW_ROWS]
    return result, preview


def main():
    setup_stdout()
    api_key, rest = pop_api_key(sys.argv[1:])

    p = argparse.ArgumentParser(description='DeepSearch compute 쿼리 실행')
    p.add_argument('query')
    p.add_argument('--out')
    p.add_argument('--max-pages', type=int, default=1)
    p.add_argument('--grep')
    p.add_argument('--content-chars', type=int, default=300)
    args = p.parse_args(rest)
    query = args.query.replace('\n', ' ').strip()
    try:
        grep = re.compile(args.grep) if args.grep else None
    except re.error as e:
        fail(f'--grep 정규식 오류: {e}')

    try:
        if query.startswith('/'):
            result, preview = run_rest(api_key, query)
        elif re.match(r'\s*DocumentSearch\s*\(', query):
            result, preview = run_document_search(api_key, query, max(1, args.max_pages), args.content_chars)
        else:
            result, preview = run_generic(api_key, query, grep)
    except DeepSearchError as e:
        fail_error(e, query)

    emit(result, preview, out=args.out, label=query)


if __name__ == '__main__':
    main()
