#!/usr/bin/env python3
"""
DeepSearch 문서 본문 읽기 (애널리스트 보고서·IR PDF, 뉴스 HTML)

사용법:
    python read_document.py <URL>
    python read_document.py '<DocumentSearch(...) 쿼리>' [--doc N]     # 검색 결과의 N번째(1부터) 문서

예시:
    python read_document.py "https://ddi-cdn.deepsearch.com/.../report.pdf"
    python read_document.py 'DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=5,page=1)' --doc 1

추출:
    - PDF → PyMuPDF로 앞 20페이지 텍스트 (pip install pymupdf)
    - HTML → 태그를 지운 본문 앞 10,000자 (노이즈 포함 가능)
    - 공시(DART)는 프레임 구조라 본문이 거의 안 나온다 → DART 링크를 안내할 것
출력: 본문이 길면 전체를 파일로 저장하고 앞 4,000자만 출력
API 키: .env / 환경변수 (검색 모드에서만 필요)
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ds_common import (DeepSearchError, compute, emit, fail, fail_error, pop_api_key,  # noqa: E402
                        requests, result_pod, setup_stdout)

PDF_MAX_PAGES = 20
HTML_MAX_CHARS = 10_000
PREVIEW_CHARS = 4_000


def download(url, timeout=60):
    resp = requests.get(url, verify=False, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    return resp.content, resp.headers.get('Content-Type', '')


def pdf_text(data):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fail('PDF를 읽으려면 PyMuPDF가 필요합니다: pip install pymupdf '
             '(또는 pip install -r skills/deepsearch/requirements.txt)')
    with fitz.open(stream=data, filetype='pdf') as doc:
        pages = [p.get_text().strip() for p in doc.pages(0, min(PDF_MAX_PAGES, doc.page_count))]
        return '\n\n'.join(t for t in pages if t), doc.page_count, len(pages)


def html_text(data):
    raw = data.decode('utf-8', errors='replace')
    if raw.count('�') > 50:          # UTF-8이 아니면 EUC-KR 시도
        raw = data.decode('euc-kr', errors='replace')
    raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    return re.sub(r'\s+', ' ', text).strip()


def read_url(url):
    data, ctype = download(url)
    if url.lower().endswith('.pdf') or 'pdf' in ctype.lower() or data[:4] == b'%PDF':
        text, total, extracted = pdf_text(data)
        return {'success': True, 'type': 'pdf', 'url': url, 'total_pages': total,
                'extracted_pages': extracted, 'text_length': len(text), 'text': text}
    text = html_text(data)
    return {'success': True, 'type': 'html', 'url': url, 'text_length': len(text), 'text': text[:HTML_MAX_CHARS]}


def find_document(api_key, query, index):
    pod = result_pod(compute(api_key, query))
    docs = (((pod or {}).get('content') or {}).get('data') or {}).get('docs') or []
    if not docs:
        fail('검색 결과에 문서가 없습니다.', query=query)
    if index >= len(docs):
        fail(f'{index + 1}번 문서가 없습니다 (이 페이지 {len(docs)}건).', query=query)
    return docs[index]


def main():
    setup_stdout()
    args = sys.argv[1:]
    index = 0
    if '--doc' in args:
        i = args.index('--doc')
        try:
            index = int(args[i + 1]) - 1
        except (IndexError, ValueError):
            fail('--doc 뒤에 1부터 시작하는 번호가 필요합니다.')
        del args[i:i + 2]
    if not args:
        fail("Usage: python read_document.py <URL | 'DocumentSearch(...)'> [--doc N]")

    target = args[-1]
    try:
        if target.startswith(('http://', 'https://')):
            result, label = read_url(target), target
        else:
            api_key, _ = pop_api_key(args[:-1])
            doc = find_document(api_key, target, index)
            if not doc.get('content_url'):
                fail('문서에 content_url이 없습니다.', title=doc.get('title', ''))
            result = read_url(doc['content_url'])
            result['meta'] = {k: doc.get(k, '') for k in ('title', 'publisher', 'created_at', 'category', 'section')}
            label = doc.get('title') or doc['content_url']
    except DeepSearchError as e:
        fail_error(e, target)
    except requests.RequestException as e:
        fail(f'문서 다운로드 실패: {e}')

    preview = dict(result)
    if len(preview['text']) > PREVIEW_CHARS:
        preview['text'] = preview['text'][:PREVIEW_CHARS] + ' …(이하 생략, 전체는 saved_to 파일)'
    emit(result, preview, label=label)


if __name__ == '__main__':
    main()
