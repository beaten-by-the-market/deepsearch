"""
DeepSearch 스킬 스크립트용 시장 데이터 헬퍼.

전 종목을 한 번에 받는 호출을 써서 종목별 반복 호출을 없앤다(2026-11-25 확인).
- GetStockSymbols()                         → 전 종목 기본정보 (market, company_type_l1 등). 현재 상장 종목 기준
- GetStockPrices(columns=[...], date_from, date_to)  (entities 생략) → 기간의 마지막 거래일 하루치, 전 종목
- GetMarketIndexes(date_from, date_to)      → 지수 11종, 기간 내 거래일마다 한 행

단위 주의: 종목 change_rate는 비율(-0.0876 = -8.76%), 지수 change_rate는 퍼센트(1.94 = 1.94%).
"""

from datetime import date, timedelta

from _ds_common import query_records

# SKILL.md 규칙 3의 안내문. 주가를 보여주는 결과에는 이 문구를 함께 싣는다.
PRICE_BASIS_NOTICE = ('주가 기준: 시가·고가·저가·종가는 수정주가입니다(액면분할·무상증자·유상증자를 과거 가격에 '
                      '소급 반영, 배당은 미반영). DeepSearch는 원주가를 따로 제공하지 않습니다. '
                      '거래량·거래대금·시가총액은 당일 실제 값입니다.')

MARKETS = ('KOSPI', 'KOSDAQ', 'KONEX')
LOOKBACK_DAYS = 7   # 주말·연휴를 건너 직전 거래일을 찾기 위한 조회 폭


def parse_date(text):
    """'YYYY-MM-DD' → date. 형식이 틀리면 ValueError."""
    y, m, d = (int(x) for x in text.split('-'))
    return date(y, m, d)


def format_krw(value, digits=1):
    """원 단위 금액 → '138.0조' / '5,027억' / '1,234'."""
    if value is None:
        return '-'
    a = abs(value)
    if a >= 1e12:
        return f'{value / 1e12:.{digits}f}조'
    if a >= 1e8:
        return f'{value / 1e8:,.0f}억'
    return f'{value:,.0f}'


def is_preferred(symbol):
    """KRX 종목코드 끝자리가 0이 아니면 우선주(005935 삼성전자우, 000087 하이트진로2우B 등)."""
    return not symbol.split(':')[-1].endswith('0')


def stock_universe(api_key, markets=('KOSPI', 'KOSDAQ'), include_preferred=False):
    """
    일반법인·공기업(company_type_l1='1','2') 종목 → {symbol: {'name', 'market'}}.
    ETF·ETN 등(company_type_l1='8')은 빠진다. '2'는 한국전력·기업은행·강원랜드 등 공기업 8종목이다. 현재 상장 종목 기준이라 과거 날짜에는 이후 상장폐지 종목이 없다.
    """
    wanted = {m.upper() for m in markets}
    out = {}
    for r in query_records(api_key, 'GetStockSymbols()', timeout=120):
        if r.get('company_type_l1') not in ('1', '2') or r.get('market') not in wanted:
            continue
        if not include_preferred and is_preferred(r['symbol']):
            continue
        out[r['symbol']] = {'name': r.get('entity_name', ''), 'market': r.get('market', '')}
    return out


def stock_snapshot(api_key, day, universe):
    """
    day(당일 또는 그 이전 마지막 거래일)의 universe 종목 시세 → 행 리스트.
    각 행: symbol, name, market, date, close, change_pct(%), market_cap, market_cap_display
    """
    start = day - timedelta(days=LOOKBACK_DAYS)
    rows = query_records(api_key, f'GetStockPrices(columns=["close","change_rate","market_cap"], '
                                  f'date_from={start}, date_to={day})', timeout=180)
    out = []
    for r in rows:
        info = universe.get(r.get('symbol'))
        if not info or not r.get('market_cap'):
            continue
        rate = r.get('change_rate')
        out.append({
            'symbol': r['symbol'],
            'name': info['name'],
            'market': info['market'],
            'date': (r.get('date') or '')[:10],
            'close': r.get('close'),
            'change_pct': round(rate * 100, 2) if rate is not None else None,
            'market_cap': r['market_cap'],
            'market_cap_display': format_krw(r['market_cap']),
        })
    return out


def index_snapshot(api_key, day):
    """day 이전 마지막 거래일의 지수 → (거래일 'YYYY-MM-DD', {symbol: 행}). change_rate는 퍼센트."""
    start = day - timedelta(days=LOOKBACK_DAYS)
    rows = query_records(api_key, f'GetMarketIndexes(date_from={start}, date_to={day})')
    if not rows:
        return None, {}
    last = max(r['date'] for r in rows)
    return last[:10], {r['symbol']: r for r in rows if r['date'] == last}
