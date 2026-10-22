#!/usr/bin/env python3
"""
적자전환/흑자전환 기업 스크리너

사용법:
    python turnaround_screener.py <API_KEY> <방향> [매출기준(억)]

    방향: loss (적자전환) 또는 profit (흑자전환)
    매출기준: 최소 매출액 (억 단위, 기본값 1000 = 1000억)

예시:
    python turnaround_screener.py "KEY" loss           → 매출 1000억+ 적자전환 기업
    python turnaround_screener.py "KEY" profit          → 매출 1000억+ 흑자전환 기업
    python turnaround_screener.py "KEY" loss 5000       → 매출 5000억+ 적자전환 기업

원리:
    1단계: 현재 영업이익 < 0 (또는 > 0) 상장기업 스크리닝
    2단계: 각 기업의 2개년 영업이익 개별 조회
    3단계: 전년대비 부호 전환 기업 필터링

의존성: requests (pip install requests)
"""

import sys
import json
import time

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print(json.dumps({'success': False, 'error': 'requests 라이브러리가 필요합니다: pip install requests'}, ensure_ascii=False))
    sys.exit(1)

URL_BASE = 'https://api.deepsearch.com/v1/compute?input='


def api_call(api_key, query, max_retries=3):
    """API 호출 (재시도 포함)."""
    headers = {'Authorization': f'Basic {api_key}'}
    url = f'{URL_BASE}{query}'
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'Max retries exceeded'}


def get_screening_list(api_key, direction, min_revenue):
    """1단계: 현재 영업이익 기준 상장기업 리스트."""
    revenue_condition = f'매출 > {min_revenue}'

    if direction == 'loss':
        query = f'상장 기업 and 영업이익 < 0 and {revenue_condition}'
    else:
        query = f'상장 기업 and 영업이익 > 0 and {revenue_condition}'

    print(f'[1단계] 스크리닝: {query}', file=sys.stderr)
    data = api_call(api_key, query)

    if not data.get('success'):
        return []

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return []

    d = pods[1].get('content', {}).get('data', {})
    entities = []
    names = d.get('entity_name', [])
    symbols = d.get('symbol', [])
    for i in range(len(names)):
        entities.append({
            'name': names[i],
            'symbol': symbols[i] if i < len(symbols) else ''
        })

    print(f'[1단계] {len(entities)}개 기업 추출', file=sys.stderr)
    return entities


def check_turnaround(api_key, entity_name, direction):
    """2단계: 개별 기업의 2개년 영업이익 조회."""
    query = f'{entity_name} 영업이익 2023-2024'
    data = api_call(api_key, query)

    if not data.get('success'):
        return None

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return None

    d = pods[1].get('content', {}).get('data', {})
    dates = d.get('date', [])
    values_key = [k for k in d.keys() if '영업이익' in k]
    if not values_key:
        return None

    values = d[values_key[0]]

    year_data = {}
    for i, date_str in enumerate(dates):
        if i < len(values):
            year = date_str[:4]
            val = values[i]
            if isinstance(val, (int, float)):
                year_data[year] = val

    if '2023' not in year_data or '2024' not in year_data:
        return None

    v2023 = year_data['2023']
    v2024 = year_data['2024']

    if direction == 'loss' and v2023 > 0 and v2024 < 0:
        return {'2023': v2023, '2024': v2024, 'type': '적자전환'}
    elif direction == 'profit' and v2023 < 0 and v2024 > 0:
        return {'2023': v2023, '2024': v2024, 'type': '흑자전환'}

    return None


def format_value(v):
    """금액을 억/조 단위로 변환."""
    abs_v = abs(v)
    if abs_v >= 1e12:
        return f'{v/1e12:.2f}조'
    elif abs_v >= 1e8:
        return f'{v/1e8:.0f}억'
    else:
        return f'{v:,.0f}'


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python turnaround_screener.py <API_KEY> <loss|profit> [min_revenue_억]'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    api_key = sys.argv[1]
    direction = sys.argv[2].lower()
    min_revenue_eok = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    min_revenue = min_revenue_eok * 100000000  # 억 → 원

    if direction not in ('loss', 'profit'):
        print(json.dumps({'success': False, 'error': 'direction must be "loss" or "profit"'}, ensure_ascii=False))
        sys.exit(1)

    label = '적자전환' if direction == 'loss' else '흑자전환'
    print(f'[시작] {label} 기업 스크리닝 (매출 {min_revenue_eok}억 이상)', file=sys.stderr)

    # 1단계: 스크리닝
    entities = get_screening_list(api_key, direction, min_revenue)
    if not entities:
        print(json.dumps({'success': True, 'type': label, 'count': 0, 'companies': []}, ensure_ascii=False, indent=2))
        return

    # 2단계: 개별 기업 확인
    turnaround_companies = []
    total = len(entities)

    for i, entity in enumerate(entities):
        name = entity['name']
        print(f'[2단계] ({i+1}/{total}) {name} 확인 중...', file=sys.stderr)

        result = check_turnaround(api_key, name, direction)
        if result:
            turnaround_companies.append({
                'name': name,
                'symbol': entity['symbol'],
                '2023_영업이익': format_value(result['2023']),
                '2024_영업이익': format_value(result['2024']),
                '2023_raw': result['2023'],
                '2024_raw': result['2024'],
            })
            print(f'  → {label}: {name} (2023: {format_value(result["2023"])} → 2024: {format_value(result["2024"])})', file=sys.stderr)

        # API 부하 방지
        time.sleep(0.5)

    # 결과 출력
    output = {
        'success': True,
        'type': label,
        'min_revenue': f'{min_revenue_eok}억',
        'screened_count': total,
        'turnaround_count': len(turnaround_companies),
        'companies': turnaround_companies
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
