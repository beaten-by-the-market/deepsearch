#!/usr/bin/env python3
"""
DeepSearch 문서 본문 읽기 스크립트

사용법:
    python read_document.py <API_KEY> <URL_OR_QUERY>

모드 1 - URL 직접 지정:
    python read_document.py "KEY" "https://ddi-cdn.deepsearch.com/.../report.pdf"

모드 2 - 검색 후 본문 읽기 (검색쿼리 + 문서번호):
    python read_document.py "KEY" 'DocumentSearch(["research"],["company"],"securities.name:삼성전자",count=5,page=1)' --doc 1

지원 형식:
    - PDF (애널리스트 보고서, IR자료, 공시) → PyMuPDF로 텍스트 추출
    - HTML (뉴스 기사) → 웹페이지 텍스트 추출

의존성: requests, PyMuPDF (pip install pymupdf)
"""

import sys
import json
import os
import tempfile
import re
from urllib.parse import quote


def install_pymupdf():
    """PyMuPDF가 없으면 설치"""
    try:
        import fitz
        return True
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymupdf', '-q'])
        return True


def download_file(url, timeout=60):
    """URL에서 파일 다운로드"""
    import requests
    requests.packages.urllib3.disable_warnings()
    resp = requests.get(url, verify=False, timeout=timeout)
    resp.raise_for_status()
    return resp.content, resp.headers.get('Content-Type', '')


def extract_pdf_text(pdf_bytes, max_pages=20):
    """PDF에서 텍스트 추출"""
    import fitz
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text = page.get_text().strip()
        if text:
            pages.append({
                'page': i + 1,
                'text': text
            })
    total_pages = doc.page_count
    doc.close()
    return pages, total_pages


def extract_html_text(html_bytes, url):
    """HTML에서 본문 텍스트 추출 (간단한 태그 제거)"""
    try:
        text = html_bytes.decode('utf-8', errors='replace')
    except:
        text = html_bytes.decode('euc-kr', errors='replace')

    # HTML 태그 제거
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # HTML 엔티티 디코딩
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return text


def search_and_get_url(api_key, query, doc_index=0):
    """DocumentSearch 실행 후 특정 문서의 URL과 메타데이터 반환"""
    import requests
    requests.packages.urllib3.disable_warnings()

    headers = {'Authorization': f'Basic {api_key}'}
    clean_query = query.replace('\n', '').strip()
    url = f'https://api.deepsearch.com/v1/compute?input={quote(clean_query, safe="")}'

    resp = requests.get(url, headers=headers, verify=False, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if not data.get('success', False):
        return None, "API 요청 실패"

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return None, "검색 결과 없음"

    content = pods[1].get('content', {})
    docs = content.get('data', {}).get('docs', [])

    if not docs:
        return None, "문서가 없습니다"

    if doc_index >= len(docs):
        return None, f"문서 {doc_index + 1}번이 없습니다 (총 {len(docs)}건)"

    doc = docs[doc_index]
    return doc, None


def read_document(url):
    """URL에서 문서 다운로드 및 텍스트 추출"""
    content_bytes, content_type = download_file(url)

    is_pdf = (
        url.lower().endswith('.pdf') or
        'pdf' in content_type.lower() or
        content_bytes[:4] == b'%PDF'
    )

    if is_pdf:
        install_pymupdf()
        pages, total_pages = extract_pdf_text(content_bytes)
        full_text = '\n\n'.join([p['text'] for p in pages])
        return {
            'success': True,
            'type': 'pdf',
            'url': url,
            'total_pages': total_pages,
            'extracted_pages': len(pages),
            'text_length': len(full_text),
            'text': full_text
        }
    else:
        text = extract_html_text(content_bytes, url)
        return {
            'success': True,
            'type': 'html',
            'url': url,
            'text_length': len(text),
            'text': text[:10000]  # HTML은 노이즈가 많으므로 10K로 제한
        }


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 3:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python read_document.py <API_KEY> <URL_OR_QUERY> [--doc N]'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    api_key = sys.argv[1]
    target = sys.argv[2]

    # --doc 옵션 파싱
    doc_index = 0
    if '--doc' in sys.argv:
        idx = sys.argv.index('--doc')
        if idx + 1 < len(sys.argv):
            doc_index = int(sys.argv[idx + 1]) - 1  # 1-based → 0-based

    try:
        if target.startswith('http://') or target.startswith('https://'):
            # 모드 1: URL 직접 지정
            result = read_document(target)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 모드 2: 검색 후 읽기
            doc, error = search_and_get_url(api_key, target, doc_index)
            if error:
                print(json.dumps({'success': False, 'error': error}, ensure_ascii=False, indent=2))
                sys.exit(1)

            meta = {
                'title': doc.get('title', ''),
                'publisher': doc.get('publisher', ''),
                'created_at': doc.get('created_at', ''),
                'category': doc.get('category', ''),
                'section': doc.get('section', ''),
            }

            content_url = doc.get('content_url', '')
            if not content_url:
                print(json.dumps({
                    'success': False,
                    'error': '문서 URL이 없습니다',
                    'meta': meta
                }, ensure_ascii=False, indent=2))
                sys.exit(1)

            result = read_document(content_url)
            result['meta'] = meta
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
