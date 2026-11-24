#!/usr/bin/env python3
"""
DeepSearch 공식 가이드(GitBook, https://help.deepsearch.com/dp)를 받아 docs/reference/*.md를 다시 만든다.

    python docs/reference/sync_from_gitbook.py                 # 웹에서 받아 생성
    python docs/reference/sync_from_gitbook.py --pages-dir DIR # 미리 받은 페이지(.md) 폴더 사용
    python docs/reference/sync_from_gitbook.py --check         # 파일은 쓰지 않고 바뀌는 페이지만 보고

- 페이지 목록과 순서: https://help.deepsearch.com/dp/llms.txt
- 페이지 본문: 각 페이지 URL + ".md" (GitBook이 마크다운으로 제공)
- 각 페이지 앞에 `<!-- source: URL -->`를 붙인다. 다음 동기화 때 이 표시로 페이지를 찾는다.
- 레포에서 덧붙인 메모는 `<!-- repo-memo:start -->` ~ `<!-- repo-memo:end -->`로 감싸 두면
  다시 생성해도 같은 페이지 아래에 그대로 남는다. 그 밖의 내용은 웹 원문으로 덮어쓴다.
- EXCLUDE의 페이지는 현재 구독 키로 쓸 수 없어 넣지 않는다(이유는 README.md).

의존성: requests
"""

import argparse
import os
import re
import sys
from datetime import date

import requests

BASE = 'https://help.deepsearch.com/dp/'
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (deepsearch-docs-sync)'}

# (파일명, 한 줄 설명, 포함할 경로 접두어들). '=경로'는 그 페이지 하나만.
FILES = [
    ('1_기본적인_데이터_조회방법.md', 'API 사용 방법, 데이터 종류(시장·개요·문서·재무), 기본 조회 방법',
     ['=api/master', '=api/howto', 'api/data', '=api/query', '=hlep-center/faq/undefined-2']),
    ('2_쿼리를_통한_데이터_조회.md', '쿼리 문법, 기업검색 예약어, 연산 함수, FAQ',
     ['api/inquiry']),
    ('3_API함수를_통한_데이터_조회_국내기업.md', '기업 검색·정보·재무제표·공시(DART)·컨센서스·이슈기업·주가',
     ['=api/func', 'api/func/company']),
    ('3_API함수를_통한_데이터_조회_채권.md', '채권 발행사·발행·수익률 함수',
     ['api/func/company/bond']),
    ('3_API함수를_통한_데이터_조회_산업검색.md', '산업 집계, 기업 주제(태그), 기업집단',
     ['api/func/industry']),
    ('3_API함수를_통한_데이터_조회_인물검색.md', '기업 임원, 주식 부자',
     ['api/func/people']),
    ('3_API함수를_통한_데이터_조회_문서검색.md', 'DocumentSearch·Trends·Aggregation, 감성, 토픽, 유사어',
     ['api/func/document']),
    ('3_API함수를_통한_데이터_조회_이벤트.md', '포트폴리오 성과, 주식·채권 이벤트 분석',
     ['api/func/event']),
    ('3_API함수를_통한_데이터_조회_경제지표.md', '한국은행·FRED·IMF·OECD·World Bank·통계청·딥서치 자체 경제지표',
     ['api/func/economy']),
    ('4_토픽인사이트.md', '토픽 인사이트·질문·답변 REST API (/v1/topic-insight)',
     ['api/topic']),
    ('5_결과레이아웃.md', 'compute 응답의 pod class별 구조',
     ['api/result_layout']),
]

# 넣지 않는 페이지: 접두어 → 이유
EXCLUDE = {
    '=undefined': '가이드 첫 화면(링크 모음)',
    'api/func/undefined': '해외기업 — api.deepsearch.com/v2 REST, 현재 구독 키로 401',
    'api/chat': '챗딥서치 — /note/v1, API 키로 401 (Session token is not provided)',
    'hlep-center': '웹 서비스 FAQ·공지 (데이터 FAQ만 1번 파일에 포함)',
}

SOURCE_RE = re.compile(r'^<!-- source: (\S+) -->$', re.M)
MEMO_RE = re.compile(r'<!-- repo-memo:start -->.*?<!-- repo-memo:end -->', re.S)


def match(path, prefix):
    if prefix.startswith('='):
        return path == prefix[1:]
    return path == prefix or path.startswith(prefix + '/')


def best(path, table):
    """가장 긴 접두어가 이긴다. (파일 매핑, 제외 매핑 모두 비교)"""
    cands = []
    for fname, _, prefixes in FILES:
        for p in prefixes:
            if match(path, p):
                cands.append((len(p.lstrip('=')), 'file', fname))
    for p, why in EXCLUDE.items():
        if match(path, p):
            cands.append((len(p.lstrip('=')), 'exclude', why))
    if not cands:
        return None, None
    cands.sort(key=lambda c: (c[0], c[1] == 'file'), reverse=True)
    return cands[0][1], cands[0][2]


def page_list(session):
    text = session.get(BASE + 'llms.txt', headers=UA, timeout=60).text
    out = []
    for m in re.finditer(r'- \[(.*?)\]\(' + re.escape(BASE) + r'(.*?)\.md\)', text):
        out.append((m.group(2), m.group(1)))
    return out


def page_body(session, path, pages_dir):
    if pages_dir:
        with open(os.path.join(pages_dir, path + '.md'), encoding='utf-8') as f:
            text = f.read()
    else:
        r = session.get(BASE + path + '.md', headers=UA, timeout=60)
        r.raise_for_status()
        text = r.text
    lines = text.split('\n')
    if lines and lines[0].startswith('> For the complete documentation index'):
        lines = lines[1:]
    return '\n'.join(lines).strip('\n')


def existing_pages(fname):
    """기존 파일에서 source URL별 (본문, 메모 목록)."""
    path = os.path.join(HERE, fname)
    if not os.path.exists(path):
        return {}
    text = open(path, encoding='utf-8').read()
    marks = list(SOURCE_RE.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        chunk = text[m.end():end]
        memos = MEMO_RE.findall(chunk)
        body = MEMO_RE.sub('', chunk).strip('\n')
        out[m.group(1)] = (body, memos)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages-dir')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding='utf-8')
        except Exception:
            pass

    session = requests.Session()
    pages = page_list(session)
    buckets = {f[0]: [] for f in FILES}
    excluded, unmapped = [], []
    for path, title in pages:
        kind, target = best(path, FILES)
        if kind == 'file':
            buckets[target].append((path, title))
        elif kind == 'exclude':
            excluded.append((path, title, target))
        else:
            unmapped.append((path, title))

    today = date.today().isoformat()
    report = []
    for fname, desc, _ in FILES:
        old = existing_pages(fname)
        parts = [f'<!-- 이 파일은 docs/reference/sync_from_gitbook.py로 생성합니다 ({today}). '
                 f'원문: {BASE} — {desc}. 직접 고치지 말고, 레포 메모는 repo-memo 마커 안에 쓰세요. -->']
        added, changed = [], []
        for path, title in buckets[fname]:
            url = BASE + path
            body = page_body(session, path, args.pages_dir)
            prev = old.pop(url, None)
            if prev is None:
                added.append(title)
            elif prev[0].strip() != body.strip():
                changed.append(title)
            block = f'<!-- source: {url} -->\n{body}'
            if prev and prev[1]:
                block += '\n\n' + '\n\n'.join(prev[1])
            parts.append(block)
        orphan_memos = [m for _, (_, memos) in old.items() for m in memos]
        if orphan_memos:
            parts.append('# (원문 페이지가 사라진 레포 메모)\n\n' + '\n\n'.join(orphan_memos))
        removed = [u for u in old]
        report.append((fname, len(buckets[fname]), added, changed, removed))
        if not args.check:
            with open(os.path.join(HERE, fname), 'w', encoding='utf-8', newline='\n') as f:
                f.write('\n\n'.join(parts) + '\n')

    for fname, n, added, changed, removed in report:
        print(f'{fname}: {n}페이지 (새 {len(added)}, 바뀜 {len(changed)}, 사라짐 {len(removed)})')
        for t in added[:50]:
            print(f'   + {t}')
        for t in changed[:50]:
            print(f'   ~ {t}')
        for u in removed[:50]:
            print(f'   - {u}')
    print(f'제외 {len(excluded)}페이지:', ', '.join(sorted({w for _, _, w in excluded})))
    if unmapped:
        print('매핑 안 된 페이지(FILES/EXCLUDE에 추가 필요):')
        for p, t in unmapped:
            print(f'   ? {p}  {t}')


if __name__ == '__main__':
    main()
