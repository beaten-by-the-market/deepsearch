#!/usr/bin/env python3
"""DeepSearch 일일 시황분석 (Daily Market Overview)

사용법:
    python market_overview.py <YYYY-MM-DD>

예시:
    python market_overview.py 2026-02-27

출력: JSON — 7개 섹션 (출력 템플릿: references/market_overview_template.md)
  1. market_indices    시장 지수 (KOSPI/KOSDAQ/KOSPI200 + 나머지 지수)      GetMarketIndexes
  2. size_analysis     규모별 동향 (코스피·코스닥 대/중/소형주)            ↑ 같은 호출 재사용
  3. top_movers        시가총액 상위 30종목(우선주 제외) 중 상승·하락 5      GetStockSymbols + GetStockPrices
  4. most_mentioned    경제뉴스 언급 상위 상장사 20                         DocumentAggregation
  5. key_headlines     경제뉴스 상위 10건                                  DocumentSearch
  6. trending_topics   토픽 10개 (오늘: 실시간, 과거: 과거 토픽)             SearchTrendingTopics / SearchHistoricalTopics
  7. market_sentiment  긍정·부정·중립 뉴스 비율                            DocumentAggregation (polarity.name)

휴장일: 시장 섹션(1~3)은 직전 거래일, 뉴스 섹션(4~7)은 그 날짜 그대로.
API 키: .env / 환경변수 (또는 첫 인자로 키)
"""

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ds_common import (DeepSearchError, compute, fail, pop_api_key, print_json,  # noqa: E402
                        query_records, result_pod, setup_stdout)
from _ds_data import PRICE_BASIS_NOTICE, index_snapshot, parse_date, stock_snapshot, stock_universe  # noqa: E402

MAIN_INDICES = ('KRX:KOSPI', 'KRX:KOSDAQ', 'KRX:KOSPI200')
SIZE_INDICES = [('KRX:KOSPILC', 'KOSPI', '코스피 대형주'), ('KRX:KOSPIMC', 'KOSPI', '코스피 중형주'),
                ('KRX:KOSPISC', 'KOSPI', '코스피 소형주'), ('KRX:KOSDAQLC', 'KOSDAQ', '코스닥 대형주'),
                ('KRX:KOSDAQMC', 'KOSDAQ', '코스닥 중형주'), ('KRX:KOSDAQSC', 'KOSDAQ', '코스닥 소형주')]
LISTED = 'securities.market:(KOSPI or KOSDAQ)'
INDEX_FIELDS = ('open', 'high', 'low', 'close', 'volume', 'change', 'change_rate')


def news_args(day):
    d = day.strftime('%Y%m%d')
    return f'date_from={d},date_to={d}'


# ---------------------------------------------------------------- 섹션 1·2: 지수

def section_indices(api_key, day):
    trading_date, by_symbol = index_snapshot(api_key, day)
    if not by_symbol:
        return {'success': False, 'error': f'{day} 이전 7일 안에 지수 데이터가 없습니다.'}, {'success': False}

    def row(r):
        return {'symbol': r['symbol'], 'name': r.get('entity_name', ''), 'date': trading_date,
                **{f: r.get(f) for f in INDEX_FIELDS}}

    indices = {'success': True, 'date': trading_date, 'change_rate_unit': '%',
               'main_indices': [row(by_symbol[s]) for s in MAIN_INDICES if s in by_symbol],
               'sub_indices': [row(r) for s, r in by_symbol.items() if s not in MAIN_INDICES]}

    segments = [{'market': m, 'segment': label, 'close': by_symbol[s].get('close'),
                 'change_rate': by_symbol[s].get('change_rate')}
                for s, m, label in SIZE_INDICES if s in by_symbol]
    summary = ''
    rated = [x for x in segments if x['change_rate'] is not None]
    if rated:
        best = max(rated, key=lambda x: x['change_rate'])
        worst = min(rated, key=lambda x: x['change_rate'])
        summary = (f"강세: {best['segment']}({best['change_rate']:+.2f}%), "
                   f"약세: {worst['segment']}({worst['change_rate']:+.2f}%)")
    size = {'success': bool(segments), 'date': trading_date, 'segments': segments, 'summary': summary}
    return indices, size


# ---------------------------------------------------------------- 섹션 3: 시총 상위 등락

def section_top_movers(api_key, day, top=30, show=5):
    rows = stock_snapshot(api_key, day, stock_universe(api_key, ('KOSPI', 'KOSDAQ')))
    rows = sorted((r for r in rows if r['change_pct'] is not None), key=lambda r: r['market_cap'], reverse=True)[:top]
    if not rows:
        return {'success': False, 'error': '시세가 없습니다.'}
    by_change = sorted(rows, key=lambda r: r['change_pct'])
    keep = ('name', 'symbol', 'market', 'close', 'change_pct', 'market_cap', 'market_cap_display')
    pick = lambda rs: [{k: r[k] for k in keep} for r in rs]
    return {'success': True, 'date': rows[0]['date'], 'basis': f'KOSPI·KOSDAQ 시가총액 상위 {top}종목(우선주 제외)',
            'top_gainers': pick(by_change[::-1][:show]), 'top_decliners': pick(by_change[:show])}


# ---------------------------------------------------------------- 섹션 4~7: 뉴스

def section_most_mentioned(api_key, day):
    rows = query_records(api_key, f'DocumentAggregation(["news"],["economy"],"{LISTED}","securities.name:20",{news_args(day)})')
    return {'success': True, 'date': str(day),
            'companies': [{'name': r.get('key'), 'mention_count': r.get('count', 0)} for r in rows]}


def section_headlines(api_key, day):
    pod = result_pod(compute(api_key, f'DocumentSearch(["news"],["economy"],"{LISTED}",count=10,page=1,{news_args(day)})'))
    data = ((pod or {}).get('content') or {}).get('data') or {}
    headlines = [{
        'title': d.get('title', ''),
        'publisher': d.get('publisher', ''),
        'created_at': (d.get('created_at') or '')[:16],
        'sentiment': (d.get('polarity') or {}).get('name', ''),
        'related_companies': [f"{s.get('name', '')}({s.get('symbol', '')})" for s in (d.get('securities') or [])[:3]],
    } for d in data.get('docs') or []]
    return {'success': True, 'date': str(day), 'total_news_count': data.get('total_matches', 0), 'headlines': headlines}


def _topics(api_key, query):
    pod = result_pod(compute(api_key, query))
    data = ((pod or {}).get('content') or {}).get('data') or {}
    raw = data.get('topics')
    if isinstance(raw, dict):            # SearchTrendingTopics: topics.news.economy
        raw = (raw.get('news') or {}).get('economy') or []
    return data.get('timestamp', ''), raw or []


def section_topics(api_key, day):
    realtime = day >= date.today()
    if realtime:
        timestamp, raw = _topics(api_key, 'SearchTrendingTopics(["news"],["economy"])')
    else:
        # 과거 토픽은 검색어가 비면 결과가 없어 시장 필터를 검색어로 쓴다
        timestamp, raw = _topics(api_key, f'SearchHistoricalTopics(["news"],["economy"],"{LISTED}",count=10,{news_args(day)})')
    topics = []
    for t in raw[:10]:
        stats = t.get('statistics') if isinstance(t.get('statistics'), dict) else {}
        secs = stats.get('securities') or t.get('securities') or []
        topics.append({
            'rank': t.get('rank', 0),
            'topic': t.get('topic', ''),
            'uid': t.get('uid'),
            'score': round(t.get('score') or 0, 3),
            'doc_count': stats.get('doc_count', 0),
            'keywords': [k.get('keyword', '') if isinstance(k, dict) else str(k) for k in (t.get('keywords') or [])[:5]],
            'related_companies': [s.get('name', '') for s in secs[:3]],
        })
    return {'success': bool(topics), 'is_realtime': realtime, 'timestamp': timestamp, 'topics': topics}


def section_sentiment(api_key, day):
    rows = query_records(api_key, f'DocumentAggregation(["news"],["economy"],"{LISTED}","polarity.name:5",{news_args(day)})')
    counts = {r.get('key'): r.get('count', 0) for r in rows}
    pos, neg, neu = (counts.get(k, 0) for k in ('긍정', '부정', '중립'))
    total = pos + neg + neu
    ratio = lambda n: round(n / total * 100, 1) if total else 0
    pr, nr = ratio(pos), ratio(neg)
    if pr > nr * 2:
        label = '긍정 우세'
    elif nr > pr * 2:
        label = '부정 우세'
    elif pr != nr:
        label = f"중립 ({'긍정' if pr > nr else '부정'} 소폭 우세)"
    else:
        label = '중립'
    return {'success': total > 0, 'date': str(day), 'positive_count': pos, 'negative_count': neg, 'neutral_count': neu,
            'total_count': total, 'positive_ratio': pr, 'negative_ratio': nr, 'neutral_ratio': ratio(neu),
            'sentiment_label': label}


# ---------------------------------------------------------------- 실행

def run(name, func, *args):
    try:
        result = func(*args)
    except DeepSearchError as e:
        result = {'success': False, 'error': str(e)[:500]}
    ok = all(r.get('success') for r in (result if isinstance(result, tuple) else (result,)))
    print(f'[{name}] {"성공" if ok else "실패"}', file=sys.stderr)
    return result


def build_report(api_key, day):
    jobs = {
        'indices': section_indices, 'top_movers': section_top_movers, 'most_mentioned': section_most_mentioned,
        'key_headlines': section_headlines, 'trending_topics': section_topics, 'market_sentiment': section_sentiment,
    }
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        futures = {name: ex.submit(run, name, f, api_key, day) for name, f in jobs.items()}
        results = {name: fut.result() for name, fut in futures.items()}

    indices = results.pop('indices')
    if not isinstance(indices, tuple):            # 지수 호출 자체가 실패
        indices = (indices, dict(indices))
    sections = {'market_indices': indices[0], 'size_analysis': indices[1], **results}
    succeeded = sum(1 for s in sections.values() if s.get('success'))
    return {
        'success': succeeded > 0,
        'date': str(day),
        'trading_date': sections['market_indices'].get('date'),
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'sections': sections,
        'sections_succeeded': succeeded,
        'sections_total': len(sections),
        'data_sources': ['KRX 한국거래소 / 코스콤 시장데이터', '국내 주요 언론사 (매일경제, 한경 등)'],
        'price_basis_notice': PRICE_BASIS_NOTICE,
    }


def main():
    setup_stdout()
    api_key, args = pop_api_key(sys.argv[1:])
    if not args:
        fail('Usage: python market_overview.py <YYYY-MM-DD>')
    try:
        day = parse_date(args[0])
    except ValueError:
        fail(f'잘못된 날짜: {args[0]} (YYYY-MM-DD 형식 필요)')

    print(f'시황분석 생성 중: {day}', file=sys.stderr)
    start = time.time()
    report = build_report(api_key, day)
    print(f"완료: {report['sections_succeeded']}/{report['sections_total']}개 섹션 성공 ({time.time() - start:.1f}초)",
          file=sys.stderr)
    print_json(report)


if __name__ == '__main__':
    main()
