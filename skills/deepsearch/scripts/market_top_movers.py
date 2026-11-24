#!/usr/bin/env python3
"""시가총액 상위 N개 종목의 등락률 (코스피/코스닥/전체)

사용법:
    python market_top_movers.py <kospi|kosdaq|all> <top_n> <date> [--include-preferred]

예시:
    python market_top_movers.py kosdaq 150 2025-02-27
    python market_top_movers.py kospi 100 2025-02-27

동작: API 2번 호출 (GetStockSymbols로 일반법인 목록 → GetStockPrices로 전 종목 당일 시세).
      date가 휴장일이면 직전 거래일 기준. 우선주는 기본 제외.
출력: JSON — 시가총액 상위 N개 중 하락률·상승률 상위 10개씩
API 키: .env / 환경변수 (또는 첫 인자로 키)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ds_common import DeepSearchError, fail, fail_error, pop_api_key, print_json, setup_stdout  # noqa: E402
from _ds_data import PRICE_BASIS_NOTICE, parse_date, stock_snapshot, stock_universe  # noqa: E402

MARKET_ARG = {'kospi': ('KOSPI',), 'kosdaq': ('KOSDAQ',), 'all': ('KOSPI', 'KOSDAQ')}
USAGE = 'python market_top_movers.py <kospi|kosdaq|all> <top_n> <YYYY-MM-DD> [--include-preferred]'


def main():
    setup_stdout()
    api_key, args = pop_api_key(sys.argv[1:])
    include_preferred = '--include-preferred' in args
    args = [a for a in args if a != '--include-preferred']
    if len(args) < 3 or args[0].lower() not in MARKET_ARG:
        fail(f'Usage: {USAGE}')
    try:
        top_n, day = int(args[1]), parse_date(args[2])
    except ValueError:
        fail(f'top_n은 정수, 날짜는 YYYY-MM-DD 형식이어야 합니다. Usage: {USAGE}')

    try:
        universe = stock_universe(api_key, MARKET_ARG[args[0].lower()], include_preferred)
        rows = stock_snapshot(api_key, day, universe)
    except DeepSearchError as e:
        fail_error(e)
    if not rows:
        fail(f'{day} 이전 7일 안에 시세가 없습니다.')

    rows.sort(key=lambda r: r['market_cap'], reverse=True)
    top = [r for r in rows[:top_n] if r['change_pct'] is not None]
    by_change = sorted(top, key=lambda r: r['change_pct'])
    print_json({
        'success': True,
        'market': args[0].upper(),
        'requested_date': str(day),
        'trading_date': max(r['date'] for r in rows),
        'universe_count': len(universe),
        'priced_count': len(rows),
        'top_n': top_n,
        'preferred_included': include_preferred,
        'most_declined': by_change[:10],
        'most_advanced': by_change[::-1][:10],
        'price_basis_notice': PRICE_BASIS_NOTICE,
    })


if __name__ == '__main__':
    main()
