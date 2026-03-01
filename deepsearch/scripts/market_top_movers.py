#!/usr/bin/env python3
"""코스닥/코스피 시가총액 상위 N개 종목의 등락률 조회

사용법:
    python market_top_movers.py <API_KEY> <market> <top_n> <date>

예시:
    python market_top_movers.py "KEY" kosdaq 150 2025-02-27
    python market_top_movers.py "KEY" kospi 100 2025-02-27

출력: JSON (시가총액 상위 N개 중 하락률 기준 정렬)
"""

import sys
import json
import time
import re
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print(json.dumps({'success': False, 'error': 'requests 필요: pip install requests'}, ensure_ascii=False))
    sys.exit(1)

# Windows 한글 출력
sys.stdout.reconfigure(encoding='utf-8')

URL_BASE = 'https://api.deepsearch.com/v1/compute?input='


def api_call(api_key, query, max_retries=3):
    headers = {'Authorization': f'Basic {api_key}'}
    url = f'{URL_BASE}{quote(query, safe="")}'
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return None


def get_listed_companies(api_key, market):
    """코스닥/코스피 상장 기업 목록 조회"""
    market_kr = '코스닥' if market.lower() == 'kosdaq' else '코스피'
    query = f'{market_kr} 상장 기업'
    data = api_call(api_key, query)
    if not data or not data.get('success'):
        return []

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return []

    content = pods[1].get('content', {})
    inner = content.get('data', {}) if isinstance(content, dict) else {}
    if 'data' in inner:
        inner = inner['data']

    names = inner.get('entity_name', [])
    symbols = inner.get('symbol', [])
    return list(zip(names, symbols))


def get_stock_data(api_key, name, date_str):
    """개별 종목의 종가, 시가총액, 등락률 조회"""
    # 전일 포함 2일치 조회
    parts = date_str.split('-')
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    # 간단히 7일 전부터 조회 (주말/공휴일 대비)
    from datetime import date, timedelta
    target = date(y, m, d)
    start = target - timedelta(days=7)
    start_str = start.strftime('%Y-%m-%d')

    query = f'{name} 종가 시가총액 {start_str}-{date_str}'
    data = api_call(api_key, query, max_retries=2)
    if not data or not data.get('success'):
        return None

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return None

    content = pods[1].get('content', {})
    inner = content.get('data', {}) if isinstance(content, dict) else {}
    if 'data' in inner:
        inner = inner['data']

    dates = inner.get('date', [])
    if not dates:
        return None

    # 컬럼명에서 종가, 시가총액 찾기
    close_vals = None
    mktcap_vals = None
    for k, v in inner.items():
        kl = k.lower()
        if '종가' in k or 'close' in kl:
            close_vals = v
        if '시가총액' in k or 'market_cap' in kl:
            mktcap_vals = v

    if not close_vals or len(close_vals) < 2:
        return None

    # 마지막 날 = target date, 그 전날 = 전일
    last_close = close_vals[-1]
    prev_close = close_vals[-2]
    last_mktcap = mktcap_vals[-1] if mktcap_vals else 0
    last_date = dates[-1][:10] if dates else date_str

    if prev_close and prev_close > 0 and last_close is not None:
        change_pct = (last_close - prev_close) / prev_close * 100
    else:
        change_pct = 0

    return {
        'name': name,
        'date': last_date,
        'close': last_close,
        'prev_close': prev_close,
        'change_pct': round(change_pct, 2),
        'market_cap': last_mktcap,
    }


def main():
    if len(sys.argv) < 5:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python market_top_movers.py <API_KEY> <kosdaq|kospi> <top_n> <date>',
            'example': 'python market_top_movers.py "KEY" kosdaq 150 2025-02-27'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    api_key = sys.argv[1]
    market = sys.argv[2]
    top_n = int(sys.argv[3])
    target_date = sys.argv[4]

    print(f'[1/3] {market.upper()} 상장 기업 목록 조회 중...', file=sys.stderr)
    companies = get_listed_companies(api_key, market)
    if not companies:
        print(json.dumps({'success': False, 'error': f'{market} 상장 기업 목록 조회 실패'}, ensure_ascii=False))
        sys.exit(1)
    print(f'  → {len(companies)}개 기업', file=sys.stderr)

    print(f'[2/3] 시가총액+종가 일괄 조회 중 (병렬 10개)...', file=sys.stderr)
    results = []
    failed = 0

    def fetch(item):
        name, symbol = item
        return get_stock_data(api_key, name, target_date)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch, c): c for c in companies}
        done = 0
        for future in as_completed(futures):
            done += 1
            if done % 100 == 0:
                print(f'  → {done}/{len(companies)} 완료', file=sys.stderr)
            result = future.result()
            if result and result['market_cap'] and result['market_cap'] > 0:
                results.append(result)
            else:
                failed += 1

    print(f'  → 성공: {len(results)}개, 실패: {failed}개', file=sys.stderr)

    print(f'[3/3] 시가총액 상위 {top_n}개 → 등락률 정렬 중...', file=sys.stderr)
    # 시가총액 기준 상위 N개
    results.sort(key=lambda x: x['market_cap'], reverse=True)
    top_stocks = results[:top_n]

    # 등락률 기준 정렬 (하락순)
    top_stocks.sort(key=lambda x: x['change_pct'])

    output = {
        'success': True,
        'market': market.upper(),
        'date': target_date,
        'total_listed': len(companies),
        'data_available': len(results),
        'top_n': top_n,
        'most_declined': top_stocks[:10],
        'most_advanced': list(reversed(top_stocks[-10:])),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
