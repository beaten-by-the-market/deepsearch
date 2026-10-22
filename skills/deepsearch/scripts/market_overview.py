#!/usr/bin/env python3
"""DeepSearch 일일 시황분석 (Daily Market Overview)

사용법:
    python market_overview.py <API_KEY> <DATE>

예시:
    python market_overview.py "KEY" 2026-02-27

출력: JSON - 7개 섹션의 종합 시황 리포트
  1. 시장 지수 (KOSPI/KOSDAQ/대형/중형/소형주)
  2. 시장 규모별 동향 (대형주 vs 중형주 vs 소형주)
  3. 시가총액 상위 등락 (상승 5 + 하락 5)
  4. 뉴스 언급 상위 종목 (Top 20)
  5. 주요 시장 뉴스 (Top 10)
  6. 트렌딩 토픽 (Top 10)
  7. 시장 감성 (긍정/부정/중립 비율)

의존성: requests (pip install requests)
"""

import sys
import json
import time
import base64
from datetime import date, timedelta, datetime
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print(json.dumps({'success': False, 'error': 'requests 필요: pip install requests'}, ensure_ascii=False))
    sys.exit(1)

sys.stdout.reconfigure(encoding='utf-8')

URL_BASE = 'https://api.deepsearch.com/v1/compute?input='


def _normalize_api_key(api_key):
    """API 키를 base64 형식으로 정규화. raw(id:secret) 형식이면 자동 인코딩."""
    if ':' in api_key:
        return base64.b64encode(api_key.encode()).decode()
    return api_key


def api_call(api_key, query, max_retries=3):
    """API 호출 + 재시도"""
    headers = {'Authorization': f'Basic {_normalize_api_key(api_key)}'}
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
                raise


def parse_pods(data):
    """API 응답에서 result pod 추출"""
    if not data or not data.get('success'):
        excs = data.get('data', {}).get('exceptions', []) if data else []
        return None, excs
    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return None, ['No result pod']
    return pods[1].get('content', {}), None


def date_to_api(date_str):
    """YYYY-MM-DD → YYYYMMDD"""
    return date_str.replace('-', '')


def format_value(v):
    """숫자를 억/조 단위로 변환"""
    if v is None:
        return '-'
    abs_v = abs(v)
    if abs_v >= 1e12:
        return f'{v/1e12:.1f}조'
    elif abs_v >= 1e8:
        return f'{v/1e8:.0f}억'
    else:
        return f'{v:,.0f}'


# =====================================================================
# Section 1: 시장 지수
# =====================================================================
def fetch_market_indices(api_key, date_str):
    """KOSPI/KOSDAQ 및 규모별 지수 조회"""
    query = f'GetMarketIndexes(date_from={date_str},date_to={date_str})'
    data = api_call(api_key, query)
    content, err = parse_pods(data)
    if err:
        # date_from/date_to로 실패하면 파라미터 없이 재시도 (최신 거래일)
        data = api_call(api_key, 'GetMarketIndexes()')
        content, err = parse_pods(data)
        if err:
            return {'success': False, 'error': str(err)}

    inner = content.get('data', content)
    symbols = inner.get('symbol', [])
    names = inner.get('entity_name', [])
    dates = inner.get('date', [])

    indices = []
    for i in range(len(symbols)):
        indices.append({
            'symbol': symbols[i] if i < len(symbols) else '',
            'name': names[i] if i < len(names) else '',
            'date': dates[i][:10] if i < len(dates) and dates[i] else date_str,
            'open': inner.get('open', [])[i] if i < len(inner.get('open', [])) else None,
            'high': inner.get('high', [])[i] if i < len(inner.get('high', [])) else None,
            'low': inner.get('low', [])[i] if i < len(inner.get('low', [])) else None,
            'close': inner.get('close', [])[i] if i < len(inner.get('close', [])) else None,
            'volume': inner.get('volume', [])[i] if i < len(inner.get('volume', [])) else None,
            'change': inner.get('change', [])[i] if i < len(inner.get('change', [])) else None,
            'change_rate': inner.get('change_rate', [])[i] if i < len(inner.get('change_rate', [])) else None,
        })

    # 주요 지수만 선별
    main_symbols = ['KRX:KOSPI', 'KRX:KOSDAQ', 'KRX:KOSPI200']
    main_indices = [idx for idx in indices if idx['symbol'] in main_symbols]
    sub_indices = [idx for idx in indices if idx['symbol'] not in main_symbols]

    actual_date = indices[0]['date'] if indices else date_str

    return {
        'success': True,
        'date': actual_date,
        'main_indices': main_indices,
        'sub_indices': sub_indices,
    }


# =====================================================================
# Section 2: 시장 규모별 동향
# =====================================================================
def fetch_size_analysis(api_key, date_str):
    """대형/중형/소형주 지수 비교 분석"""
    # GetMarketIndexes에서 이미 데이터를 가져왔으므로
    # 별도 호출 대신 fetch_market_indices 결과를 재활용할 수 있지만
    # 독립 실행을 위해 별도 호출
    query = f'GetMarketIndexes(date_from={date_str},date_to={date_str})'
    data = api_call(api_key, query)
    content, err = parse_pods(data)
    if err:
        data = api_call(api_key, 'GetMarketIndexes()')
        content, err = parse_pods(data)
        if err:
            return {'success': False, 'error': str(err)}

    inner = content.get('data', content)
    symbols = inner.get('symbol', [])
    names = inner.get('entity_name', [])
    change_rates = inner.get('change_rate', [])
    closes = inner.get('close', [])

    size_map = {}
    for i in range(len(symbols)):
        size_map[symbols[i]] = {
            'name': names[i] if i < len(names) else '',
            'close': closes[i] if i < len(closes) else None,
            'change_rate': change_rates[i] if i < len(change_rates) else None,
        }

    analysis = []
    # KOSPI 규모별
    for sym, label in [('KRX:KOSPILC', '코스피 대형주'), ('KRX:KOSPIMC', '코스피 중형주'), ('KRX:KOSPISC', '코스피 소형주')]:
        if sym in size_map:
            analysis.append({'market': 'KOSPI', 'segment': label, **size_map[sym]})
    # KOSDAQ 규모별
    for sym, label in [('KRX:KOSDAQLC', '코스닥 대형주'), ('KRX:KOSDAQMC', '코스닥 중형주'), ('KRX:KOSDAQSC', '코스닥 소형주')]:
        if sym in size_map:
            analysis.append({'market': 'KOSDAQ', 'segment': label, **size_map[sym]})

    # 어느 규모가 강세/약세인지 분석
    if analysis:
        best = max(analysis, key=lambda x: x.get('change_rate', 0) or 0)
        worst = min(analysis, key=lambda x: x.get('change_rate', 0) or 0)
        summary = f"강세: {best['segment']}({best.get('change_rate',0):+.2f}%), 약세: {worst['segment']}({worst.get('change_rate',0):+.2f}%)"
    else:
        summary = ''

    return {
        'success': True,
        'segments': analysis,
        'summary': summary,
    }


# =====================================================================
# Section 3: 시가총액 상위 등락
# =====================================================================
def fetch_top_movers(api_key, date_str):
    """매출 5조 이상 대형주의 시총/등락률 조회"""
    # Step 1: 대형주 필터
    query = '상장 기업 and 매출 > 5000000000000'
    data = api_call(api_key, query)
    content, err = parse_pods(data)
    if err:
        return {'success': False, 'error': f'대형주 목록 조회 실패: {err}'}

    inner = content.get('data', content)
    if 'data' in inner and isinstance(inner['data'], dict):
        inner = inner['data']

    names = inner.get('entity_name', [])
    symbols = inner.get('symbol', [])
    companies = list(zip(names, symbols))

    if not companies:
        return {'success': False, 'error': '대형주 목록이 비어있습니다'}

    # Step 2: 개별 종목 시총/종가 병렬 조회
    parts = date_str.split('-')
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    target = date(y, m, d)
    start = target - timedelta(days=7)
    start_str = start.strftime('%Y-%m-%d')

    results = []
    failed = 0

    def fetch_stock(item):
        name, symbol = item
        q = f'{name} 종가 시가총액 {start_str}-{date_str}'
        try:
            d = api_call(api_key, q, max_retries=2)
            if not d or not d.get('success'):
                return None
            pods = d.get('data', {}).get('pods', [])
            if len(pods) < 2:
                return None
            c = pods[1].get('content', {})
            ci = c.get('data', c)
            if 'data' in ci and isinstance(ci['data'], dict):
                ci = ci['data']

            close_vals = None
            mktcap_vals = None
            for k, v in ci.items():
                if '종가' in k or 'close' in k.lower():
                    close_vals = v
                if '시가총액' in k or 'market_cap' in k.lower():
                    mktcap_vals = v

            if not close_vals or len(close_vals) < 2:
                return None

            last_close = close_vals[-1]
            prev_close = close_vals[-2]
            last_mktcap = mktcap_vals[-1] if mktcap_vals else 0

            change_pct = 0
            if prev_close and prev_close > 0 and last_close is not None:
                change_pct = (last_close - prev_close) / prev_close * 100

            return {
                'name': name,
                'symbol': symbol,
                'close': last_close,
                'change_pct': round(change_pct, 2),
                'market_cap': last_mktcap,
                'market_cap_display': format_value(last_mktcap) if last_mktcap else '-',
            }
        except:
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_stock, c): c for c in companies}
        for future in as_completed(futures):
            result = future.result()
            if result and result['market_cap'] and result['market_cap'] > 0:
                results.append(result)
            else:
                failed += 1

    # 시총 상위 30개
    results.sort(key=lambda x: x['market_cap'], reverse=True)
    top30 = results[:30]

    # 상승/하락 정렬
    gainers = sorted(top30, key=lambda x: x['change_pct'], reverse=True)[:5]
    decliners = sorted(top30, key=lambda x: x['change_pct'])[:5]

    return {
        'success': True,
        'date': date_str,
        'total_queried': len(companies),
        'data_available': len(results),
        'top_gainers': gainers,
        'top_decliners': decliners,
    }


# =====================================================================
# Section 4: 뉴스 언급 상위 종목
# =====================================================================
def fetch_most_mentioned(api_key, date_str):
    """해당 날짜 뉴스에서 가장 많이 언급된 상장사 20개"""
    date_api = date_to_api(date_str)
    query = f'DocumentAggregation(["news"],["economy"],"securities.market:(KOSPI or KOSDAQ)","securities.name:20",date_from={date_api},date_to={date_api})'
    data = api_call(api_key, query)
    content, err = parse_pods(data)
    if err:
        return {'success': False, 'error': str(err)}

    inner = content.get('data', content)
    keys = inner.get('key', [])
    counts = inner.get('count', [])

    companies = []
    for i in range(len(keys)):
        companies.append({
            'name': keys[i],
            'mention_count': counts[i] if i < len(counts) else 0,
        })

    return {
        'success': True,
        'date': date_str,
        'companies': companies,
    }


# =====================================================================
# Section 5: 주요 시장 뉴스
# =====================================================================
def fetch_key_headlines(api_key, date_str):
    """해당 날짜 경제 뉴스 상위 10건"""
    date_api = date_to_api(date_str)
    query = f'DocumentSearch(["news"],["economy"],"securities.market:(KOSPI or KOSDAQ)",count=10,page=1,date_from={date_api},date_to={date_api})'
    data = api_call(api_key, query)

    # query_api.py 스타일로 파싱
    if not data or not data.get('success'):
        return {'success': False, 'error': 'API 요청 실패'}

    pods = data.get('data', {}).get('pods', [])
    if len(pods) < 2:
        return {'success': False, 'error': '검색 결과 없음'}

    content = pods[1].get('content', {})
    doc_data = content.get('data', {})
    docs = doc_data.get('docs', [])
    total = doc_data.get('total_matches', 0)

    headlines = []
    for doc in docs[:10]:
        secs = doc.get('securities', [])
        related = [f"{s.get('name','')}({s.get('symbol','')})" for s in secs[:3]]
        pol = doc.get('polarity', {})
        headlines.append({
            'title': doc.get('title', ''),
            'publisher': doc.get('publisher', ''),
            'created_at': doc.get('created_at', '')[:16],
            'sentiment': pol.get('name', '') if isinstance(pol, dict) else '',
            'related_companies': related,
        })

    return {
        'success': True,
        'date': date_str,
        'total_news_count': total,
        'headlines': headlines,
    }


# =====================================================================
# Section 6: 트렌딩 토픽
# =====================================================================
def fetch_trending_topics(api_key, date_str):
    """경제 뉴스 트렌딩 토픽"""
    # 오늘 vs 과거 판단
    today = date.today().strftime('%Y-%m-%d')
    is_realtime = date_str >= today

    if is_realtime:
        query = 'SearchTrendingTopics(["news"],["economy"])'
    else:
        date_api = date_to_api(date_str)
        # SearchHistoricalTopics는 검색어가 비어있으면 결과 없음 → 시장 필터 사용
        query = f'SearchHistoricalTopics(["news"],["economy"],"securities.market:(KOSPI or KOSDAQ)",count=10,date_from={date_api},date_to={date_api})'

    data = api_call(api_key, query)
    content, err = parse_pods(data)
    if err:
        # 실시간 폴백
        if not is_realtime:
            data = api_call(api_key, 'SearchTrendingTopics(["news"],["economy"])')
            content, err = parse_pods(data)
            is_realtime = True
        if err:
            return {'success': False, 'error': str(err)}

    # SearchTrendingTopics vs SearchHistoricalTopics 응답 구조가 다름
    topics_data = content.get('data', {})
    timestamp = topics_data.get('timestamp', '')

    raw_topics = []
    if 'topics' in topics_data:
        topics_val = topics_data['topics']
        if isinstance(topics_val, list):
            # SearchHistoricalTopics: topics가 바로 리스트
            raw_topics = topics_val
        elif isinstance(topics_val, dict):
            # SearchTrendingTopics: topics.news.economy = [리스트]
            news = topics_val.get('news', {})
            raw_topics = news.get('economy', [])

    topics = []
    for t in raw_topics[:10]:
        keywords = t.get('keywords', [])

        # SearchTrendingTopics: securities가 statistics.securities에 있음
        # SearchHistoricalTopics: securities가 최상위에 있음
        secs = t.get('securities', [])
        stats = t.get('statistics', {})
        if isinstance(stats, dict) and stats.get('securities'):
            secs = stats['securities']

        doc_count = stats.get('doc_count', 0) if isinstance(stats, dict) else 0

        topics.append({
            'rank': t.get('rank', 0),
            'topic': t.get('topic', ''),
            'score': round(t.get('score', 0), 3),
            'doc_count': doc_count,
            'keywords': [kw.get('keyword', '') if isinstance(kw, dict) else str(kw) for kw in keywords[:5]],
            'related_companies': [s.get('name', '') for s in secs[:3]] if isinstance(secs, list) else [],
        })

    return {
        'success': True,
        'is_realtime': is_realtime,
        'timestamp': timestamp,
        'topics': topics,
    }


# =====================================================================
# Section 7: 시장 감성
# =====================================================================
def fetch_market_sentiment(api_key, date_str):
    """긍정/부정/중립 뉴스 비율로 시장 감성 분석"""
    date_api = date_to_api(date_str)
    base_query = 'securities.market:(KOSPI or KOSDAQ)'

    counts = {}
    for polarity in ['긍정', '부정', '중립']:
        query = f'DocumentSearch(["news"],["economy"],"{base_query} and polarity.name:{polarity}",count=1,page=1,date_from={date_api},date_to={date_api})'
        try:
            data = api_call(api_key, query)
            if data and data.get('success'):
                pods = data.get('data', {}).get('pods', [])
                if len(pods) >= 2:
                    total = pods[1].get('content', {}).get('data', {}).get('total_matches', 0)
                    counts[polarity] = total
                else:
                    counts[polarity] = 0
            else:
                counts[polarity] = 0
        except:
            counts[polarity] = 0

    total = sum(counts.values())

    if total > 0:
        pos_ratio = round(counts.get('긍정', 0) / total * 100, 1)
        neg_ratio = round(counts.get('부정', 0) / total * 100, 1)
        neu_ratio = round(counts.get('중립', 0) / total * 100, 1)
    else:
        pos_ratio = neg_ratio = neu_ratio = 0

    # 감성 라벨
    if pos_ratio > neg_ratio * 2:
        label = '긍정 우세'
    elif neg_ratio > pos_ratio * 2:
        label = '부정 우세'
    elif pos_ratio > neg_ratio:
        label = '중립 (긍정 소폭 우세)'
    elif neg_ratio > pos_ratio:
        label = '중립 (부정 소폭 우세)'
    else:
        label = '중립'

    return {
        'success': True,
        'date': date_str,
        'positive_count': counts.get('긍정', 0),
        'negative_count': counts.get('부정', 0),
        'neutral_count': counts.get('중립', 0),
        'total_count': total,
        'positive_ratio': pos_ratio,
        'negative_ratio': neg_ratio,
        'neutral_ratio': neu_ratio,
        'sentiment_label': label,
    }


# =====================================================================
# 오케스트레이터
# =====================================================================
def build_report(api_key, date_str):
    """7개 섹션을 병렬 + 순차 실행하여 종합 리포트 생성"""
    report = {
        'success': True,
        'date': date_str,
        'generated_at': datetime.now().isoformat(),
        'sections': {},
    }

    # Phase 1: 빠른 섹션 6개 병렬 실행
    fast_sections = [
        ('market_indices', fetch_market_indices),
        ('size_analysis', fetch_size_analysis),
        ('most_mentioned', fetch_most_mentioned),
        ('key_headlines', fetch_key_headlines),
        ('trending_topics', fetch_trending_topics),
        ('market_sentiment', fetch_market_sentiment),
    ]

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {}
        for name, func in fast_sections:
            print(f'[{name}] 조회 시작...', file=sys.stderr)
            futures[executor.submit(func, api_key, date_str)] = name

        for future in as_completed(futures):
            name = futures[future]
            try:
                report['sections'][name] = future.result()
                status = '성공' if report['sections'][name].get('success') else '실패'
                print(f'[{name}] {status}', file=sys.stderr)
            except Exception as e:
                report['sections'][name] = {'success': False, 'error': str(e)[:500]}
                print(f'[{name}] 에러: {str(e)[:100]}', file=sys.stderr)

    # Phase 2: top_movers (내부에서 ThreadPoolExecutor 사용)
    print('[top_movers] 조회 시작 (대형주 병렬 조회)...', file=sys.stderr)
    try:
        report['sections']['top_movers'] = fetch_top_movers(api_key, date_str)
        status = '성공' if report['sections']['top_movers'].get('success') else '실패'
        print(f'[top_movers] {status}', file=sys.stderr)
    except Exception as e:
        report['sections']['top_movers'] = {'success': False, 'error': str(e)[:500]}
        print(f'[top_movers] 에러: {str(e)[:100]}', file=sys.stderr)

    # 성공률 집계
    succeeded = sum(1 for s in report['sections'].values() if s.get('success'))
    report['sections_succeeded'] = succeeded
    report['sections_total'] = len(fast_sections) + 1
    if succeeded == 0:
        report['success'] = False

    report['data_sources'] = [
        'KRX 한국거래소 / 코스콤 시장데이터',
        'NICE평가정보 재무데이터',
        '국내 주요 언론사 (매일경제, 한경 등)',
    ]

    return report


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python market_overview.py <API_KEY> <DATE>',
            'example': 'python market_overview.py "KEY" 2026-02-27'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    api_key = sys.argv[1]
    date_str = sys.argv[2]

    # 날짜 형식 검증
    try:
        y, m, d = date_str.split('-')
        date(int(y), int(m), int(d))
    except:
        print(json.dumps({'success': False, 'error': f'잘못된 날짜: {date_str} (YYYY-MM-DD 형식 필요)'}, ensure_ascii=False))
        sys.exit(1)

    print(f'시황분석 생성 중: {date_str}', file=sys.stderr)
    start_time = time.time()

    report = build_report(api_key, date_str)

    elapsed = round(time.time() - start_time, 1)
    print(f'완료: {report["sections_succeeded"]}/{report["sections_total"]}개 섹션 성공 ({elapsed}초)', file=sys.stderr)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
