#!/usr/bin/env python3
"""
적자전환/흑자전환 상장기업 스크리너

사용법:
    python turnaround_screener.py <loss|profit> [매출기준_억=1000] [--years 이전연도 최근연도]

예시:
    python turnaround_screener.py loss              → 매출 1000억+ 적자전환 (최근 결산연도 자동)
    python turnaround_screener.py profit 5000       → 매출 5000억+ 흑자전환
    python turnaround_screener.py loss 1000 --years 2023 2024

원리:
    1. 스크리닝: `상장 기업 and 영업이익 < 0 (또는 > 0) and 매출 > X` (현재 기준 후보)
       → 영업이익의 연도 간 비교는 스크리닝 쿼리로 안 되기 때문에 후보만 먼저 좁힌다.
    2. GetFinancialStatements를 50개사씩 묶어 손익계산서 영업이익(`영업이익(손실)`, account_id 5000)을 받는다.
       연결이 없는 회사는 별도로 다시 받는다.
    3. 최근 결산연도(후보의 절반 이상이 값을 가진 가장 최근 연도)와 그 전년의 부호가 바뀐 회사만 남긴다.
API 키: .env / 환경변수 (또는 첫 인자로 키)
"""

import os
import sys
from collections import Counter
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ds_common import DeepSearchError, fail, fail_error, pop_api_key, print_json, query_records, setup_stdout  # noqa: E402
from _ds_data import format_krw  # noqa: E402

BATCH = 50
OP_INCOME = ('12', '5000')   # (report_id, account_id) = 손익계산서 / 영업이익(손실)
USAGE = 'python turnaround_screener.py <loss|profit> [매출기준_억=1000] [--years 이전연도 최근연도]'


def screen(api_key, direction, min_revenue):
    sign = '<' if direction == 'loss' else '>'
    query = f'상장 기업 and 영업이익 {sign} 0 and 매출 > {min_revenue}'
    print(f'[1/3] 스크리닝: {query}', file=sys.stderr)
    rows = query_records(api_key, query)
    return {r['symbol']: r.get('entity_name', '') for r in rows if r.get('symbol')}


def operating_income(api_key, symbols, year_from, year_to, consolidated):
    """{symbol: {year: 영업이익}} (연간)."""
    out = {}
    for i in range(0, len(symbols), BATCH):
        chunk = symbols[i:i + BATCH]
        q = (f'GetFinancialStatements([{", ".join(chunk)}], report_ids="Income", consolidated={consolidated}, '
             f'date_from={year_from}-01-01, date_to={year_to}-12-31)')
        for r in query_records(api_key, q, timeout=180):
            if (r.get('report_id'), r.get('account_id')) == OP_INCOME and r.get('value') is not None:
                out.setdefault(r['symbol'], {})[int(r['date'][:4])] = r['value']
        print(f'  → {"연결" if consolidated else "별도"} {min(i + BATCH, len(symbols))}/{len(symbols)}', file=sys.stderr)
    return out


def latest_common_year(values):
    """후보의 절반 이상이 값을 가진 가장 최근 연도."""
    counts = Counter(y for v in values.values() for y in v)
    if not counts:
        return None
    need = len(values) / 2
    ok = [y for y, n in counts.items() if n >= need]
    return max(ok) if ok else max(counts)


def main():
    setup_stdout()
    api_key, args = pop_api_key(sys.argv[1:])
    years = None
    if '--years' in args:
        i = args.index('--years')
        try:
            years = (int(args[i + 1]), int(args[i + 2]))
        except (IndexError, ValueError):
            fail(f'--years 뒤에 연도 두 개가 필요합니다. Usage: {USAGE}')
        del args[i:i + 3]
    if not args or args[0].lower() not in ('loss', 'profit'):
        fail(f'Usage: {USAGE}')
    direction = args[0].lower()
    try:
        min_revenue_eok = int(args[1]) if len(args) > 1 else 1000
    except ValueError:
        fail(f'매출기준은 억 단위 정수입니다. Usage: {USAGE}')
    label = '적자전환' if direction == 'loss' else '흑자전환'

    try:
        candidates = screen(api_key, direction, min_revenue_eok * 100_000_000)
        if not candidates:
            print_json({'success': True, 'type': label, 'screened_count': 0, 'companies': []})
            return
        print(f'  → 후보 {len(candidates)}개사', file=sys.stderr)

        y_from, y_to = (years[0], years[1]) if years else (date.today().year - 3, date.today().year)
        print('[2/3] 영업이익 조회 (연결 → 없으면 별도)', file=sys.stderr)
        symbols = sorted(candidates)
        values = operating_income(api_key, symbols, y_from, y_to, True)
        basis = {s: '연결' for s in values}
        missing = [s for s in symbols if s not in values]
        if missing:
            separate = operating_income(api_key, missing, y_from, y_to, False)
            values.update(separate)
            basis.update({s: '별도' for s in separate})
    except DeepSearchError as e:
        fail_error(e)

    latest = years[1] if years else latest_common_year(values)
    if latest is None:
        fail('후보 기업의 영업이익 데이터를 받지 못했습니다.')
    prev = years[0] if years else latest - 1

    print(f'[3/3] {prev} → {latest} 부호 전환 확인', file=sys.stderr)
    companies = []
    for s in symbols:
        v = values.get(s, {})
        a, b = v.get(prev), v.get(latest)
        if a is None or b is None:
            continue
        if (direction == 'loss' and a > 0 > b) or (direction == 'profit' and a < 0 < b):
            companies.append({
                'name': candidates[s], 'symbol': s, 'basis': basis.get(s, ''),
                f'{prev}_영업이익': format_krw(a, 2), f'{latest}_영업이익': format_krw(b, 2),
                f'{prev}_raw': a, f'{latest}_raw': b,
            })
    companies.sort(key=lambda c: c[f'{latest}_raw'])

    print_json({
        'success': True,
        'type': label,
        'min_revenue': f'{min_revenue_eok:,}억',
        'years': [prev, latest],
        'screened_count': len(candidates),
        'compared_count': sum(1 for s in symbols if prev in values.get(s, {}) and latest in values.get(s, {})),
        'turnaround_count': len(companies),
        'companies': companies,
        'note': '영업이익은 GetFinancialStatements 손익계산서 `영업이익(손실)`. 과거 연도 값은 재작성값일 수 있음(SKILL.md 규칙 4).',
    })


if __name__ == '__main__':
    main()
