"""
================================================================================
KRX 상장사 문서검색기 (DeepSearch API 기반)
================================================================================

[프로그램 개요]
- 목적: DeepSearch API를 활용하여 뉴스, 증권사보고서, 공시/IR, 특허 문서를 검색하고,
        검색 결과에서 KRX 상장사(KOSPI, KOSDAQ, KONEX)가 언급된 문서만 필터링
- 데이터 소스: DeepSearch API (https://api.deepsearch.com)
- 상장사 정보: PostgreSQL DB (Supabase) - ds_entitysummary 테이블

[주요 기능]
1. 문서 검색: 카테고리별(뉴스/보고서/공시/특허) 문서 검색
2. 조건 필터: 언론사, 키워드, 기간 등 다양한 조건 설정
3. 상장사 필터: 검색 결과에서 KRX 상장사 언급 문서만 추출
4. 결과 표시: 매칭된 상장사명과 함께 결과 표시

[실행 방법]
- 로컬: streamlit run deepsearch_query.py
- 배포: Streamlit Cloud에서 자동 실행
================================================================================
"""

import pandas as pd
import streamlit as st
import requests
import os
import time
import psycopg2
from datetime import datetime, timedelta
import plotly.graph_objects as go
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# SSL 인증서 경고 비활성화 (DeepSearch API가 self-signed 인증서 사용 시)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# ==============================================================================
# 환경 설정 (로컬/Streamlit Cloud 자동 감지)
# ==============================================================================
# [환경 설정 자동 감지]
# - Streamlit Cloud 배포 시: st.secrets에서 설정값 로드
# - 로컬 개발 시: .env 파일에서 환경변수 로드
#
# [필요한 환경변수/시크릿]
# - API_KEY: DeepSearch API 인증키 (Basic Auth, base64 인코딩)
# - DB_HOST: PostgreSQL 호스트 (예: db.xxxxx.supabase.co)
# - DB_PORT: PostgreSQL 포트 (기본값: 5432)
# - DB_NAME: 데이터베이스명 (기본값: postgres)
# - DB_USER/DB_PASSWORD: 읽기 전용 DB 접속 정보
# - DB_USER_CRUD/DB_PASSWORD_CRUD: CRUD 작업용 DB 접속 정보

def get_config():
    """
    실행 환경을 자동 감지하여 적절한 설정을 반환합니다.

    Returns:
        dict: api_key, db_config, db_config_crud를 포함하는 설정 딕셔너리

    동작 방식:
    1. 먼저 st.secrets 접근 시도 (Streamlit Cloud 환경)
    2. 실패 시 .env 파일에서 로드 (로컬 개발 환경)
    """
    try:
        # Streamlit Cloud 환경: secrets.toml에서 설정 로드
        config = {
            'api_key': st.secrets["general"]["api_key"],
            'db_config': {
                'user': st.secrets["general"]["db_user"],
                'password': st.secrets["general"]["db_password"],
                'host': st.secrets["general"]["db_host"],
                'port': st.secrets["general"]["db_port"],
                'database': st.secrets["general"]["db_name"],
            },
            'db_config_crud': {
                'user': st.secrets["crud"]["db_user"],
                'password': st.secrets["crud"]["db_password"],
                'host': st.secrets["crud"]["db_host"],
                'port': st.secrets["crud"]["db_port"],
                'database': st.secrets["general"]["db_name"],
            }
        }
        return config
    except Exception:
        # 로컬 개발 환경: .env 파일에서 환경변수 로드
        from dotenv import load_dotenv
        load_dotenv()

        config = {
            'api_key': os.getenv("API_KEY"),
            'db_config': {
                'user': os.getenv("DB_USER"),
                'password': os.getenv("DB_PASSWORD"),
                'host': os.getenv("DB_HOST"),
                'port': os.getenv("DB_PORT"),
                'database': os.getenv("DB_NAME"),
            },
            'db_config_crud': {
                'user': os.getenv("DB_USER_CRUD"),
                'password': os.getenv("DB_PASSWORD_CRUD"),
                'host': os.getenv("DB_HOST"),
                'port': os.getenv("DB_PORT"),
                'database': os.getenv("DB_NAME"),
            }
        }
        return config


# 설정 로드
config = get_config()
api_key = config['api_key']
db_config = config['db_config']
db_config_crud = config['db_config_crud']


# ==============================================================================
# API 설정
# ==============================================================================
# [DeepSearch API 설정]
# - 인증 방식: Basic Authentication (API 키를 base64 인코딩하여 전송)
# - 엔드포인트: https://api.deepsearch.com/v1/compute
# - 요청 형식: GET 요청, input 파라미터로 쿼리 함수 전달

# HTTP 요청 헤더 (인증 정보 포함)
headers = {
    'Authorization': f'Basic {api_key}'
}

# DeepSearch API 기본 URL
# 쿼리 함수는 input 파라미터로 URL 인코딩되어 전달됨
url_base = 'https://api.deepsearch.com/v1/compute?input='


# ==============================================================================
# API 요청 함수
# ==============================================================================

def generate_url(base_query, page):
    """
    페이지네이션을 위한 API 요청 URL을 생성합니다.

    [동작 설명]
    DocumentSearch API는 한 번에 최대 100건의 결과만 반환합니다.
    전체 결과를 가져오려면 page 파라미터를 변경하며 반복 요청해야 합니다.

    Args:
        base_query (str): page=1로 설정된 기본 DocumentSearch 쿼리
                         예: 'DocumentSearch(["news"], "키워드", count=100, page=1)'
        page (int): 요청할 페이지 번호 (1부터 시작)

    Returns:
        str: 완성된 API 요청 URL

    Example:
        >>> base = 'DocumentSearch(["news"], "삼성", count=100, page=1)'
        >>> generate_url(base, 3)
        'https://api.deepsearch.com/v1/compute?input=DocumentSearch(["news"], "삼성", count=100, page=3)'
    """
    # 기본 쿼리의 page 값을 원하는 페이지로 교체
    query = base_query.replace('page = 1', f'page = {page}')
    # URL에서 줄바꿈 문자 제거 (쿼리가 여러 줄로 작성된 경우 대비)
    return f'{url_base}{query}'.replace('\n', '')


def make_request(url, headers, max_retries=5):
    """
    DeepSearch API에 HTTP GET 요청을 보내고 응답을 반환합니다.

    [동작 설명]
    네트워크 오류나 서버 오류 발생 시 지수 백오프로 재시도합니다.
    최대 재시도 횟수 초과 시 예외를 발생시킵니다.

    [재시도 정책]
    - 최대 재시도: 5회 (기본값)
    - 재시도 간격: 5초 고정
    - 재시도 대상: 모든 RequestException (타임아웃, 연결 오류, HTTP 오류 등)

    Args:
        url (str): API 요청 URL
        headers (dict): HTTP 요청 헤더 (인증 정보 포함)
        max_retries (int): 최대 재시도 횟수 (기본값: 5)

    Returns:
        requests.Response: API 응답 객체

    Raises:
        Exception: 최대 재시도 횟수 초과 시

    Note:
        verify=False로 SSL 인증서 검증을 비활성화합니다.
        이는 DeepSearch API의 인증서 문제를 우회하기 위함입니다.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()  # HTTP 오류 상태 코드 확인 (4xx, 5xx)
            return response
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Request failed: {e}. Attempt {attempt} of {max_retries}. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Max retries exceeded")


# ==============================================================================
# 종목 상세 정보 API 함수
# ==============================================================================

def get_stock_prices(symbol, date_from, date_to, headers):
    """
    특정 종목의 주가 데이터를 조회합니다.

    Args:
        symbol (str): 종목 심볼 (예: KRX:005930)
        date_from (str): 시작일 (YYYY-MM-DD)
        date_to (str): 종료일 (YYYY-MM-DD)
        headers (dict): API 요청 헤더

    Returns:
        pd.DataFrame: 주가 데이터 (date, open, high, low, close, volume)
    """
    import urllib.parse
    # 날짜 파라미터 없이 호출하면 가장 최근 거래일 데이터 반환
    # 날짜가 있으면 해당 기간 조회
    if date_from and date_to:
        query = f'GetStockPrices([{symbol}],date_from={date_from},date_to={date_to})'
    else:
        query = f'GetStockPrices([{symbol}])'
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.deepsearch.com/v1/compute?input={encoded_query}"

    try:
        response = make_request(url, headers, max_retries=3)
        data = response.json()

        if 'data' in data and 'pods' in data['data']:
            for pod in data['data']['pods']:
                if pod.get('class') == 'Result:DataFrame' and 'content' in pod:
                    content = pod['content']
                    if 'data' in content:
                        df_data = content['data']
                        # 응답 형식: {'date': [...], 'symbol': [...], ...}
                        if isinstance(df_data, dict) and 'close' in df_data:
                            df = pd.DataFrame(df_data)
                            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"주가 조회 오류: {e}")
        return pd.DataFrame()


def get_disclosure_documents(symbol, date_from, date_to, headers, count=50):
    """
    특정 종목의 공시 문서를 조회합니다.

    Args:
        symbol (str): 종목 심볼 (예: KRX:005930)
        date_from (str): 시작일 (YYYY-MM-DD)
        date_to (str): 종료일 (YYYY-MM-DD)
        headers (dict): API 요청 헤더
        count (int): 조회할 문서 수

    Returns:
        list: 공시 문서 목록
    """
    import urllib.parse
    query = f'DocumentSearch(["company"],["disclosure"],"securities.symbol:{symbol}", count={count}, date_from={date_from}, date_to={date_to})'
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.deepsearch.com/v1/compute?input={encoded_query}"

    try:
        response = make_request(url, headers, max_retries=3)
        data = response.json()

        if 'data' in data and 'pods' in data['data']:
            for pod in data['data']['pods']:
                if 'content' in pod and 'data' in pod['content']:
                    content_data = pod['content']['data']
                    if 'docs' in content_data:
                        return content_data['docs']
        return []
    except Exception as e:
        print(f"공시 조회 오류: {e}")
        return []


def get_ir_documents(symbol, date_from, date_to, headers, count=50):
    """
    특정 종목의 IR 자료를 조회합니다.

    Args:
        symbol (str): 종목 심볼 (예: KRX:005930)
        date_from (str): 시작일 (YYYY-MM-DD)
        date_to (str): 종료일 (YYYY-MM-DD)
        headers (dict): API 요청 헤더
        count (int): 조회할 문서 수

    Returns:
        list: IR 문서 목록
    """
    import urllib.parse
    query = f'DocumentSearch(["company"],["ir"],"securities.symbol:{symbol}", count={count}, date_from={date_from}, date_to={date_to})'
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.deepsearch.com/v1/compute?input={encoded_query}"

    try:
        response = make_request(url, headers, max_retries=3)
        data = response.json()

        if 'data' in data and 'pods' in data['data']:
            for pod in data['data']['pods']:
                if 'content' in pod and 'data' in pod['content']:
                    content_data = pod['content']['data']
                    if 'docs' in content_data:
                        return content_data['docs']
        return []
    except Exception as e:
        print(f"IR 조회 오류: {e}")
        return []


def get_analyst_reports(symbol, date_from, date_to, headers, count=50):
    """
    특정 종목의 애널리스트 보고서를 조회합니다.

    Args:
        symbol (str): 종목 심볼 (예: KRX:005930)
        date_from (str): 시작일 (YYYY-MM-DD)
        date_to (str): 종료일 (YYYY-MM-DD)
        headers (dict): API 요청 헤더
        count (int): 조회할 문서 수

    Returns:
        list: 애널리스트 보고서 목록
    """
    import urllib.parse
    query = f'DocumentSearch(["research"],["company"],"securities.symbol:{symbol}", count={count}, date_from={date_from}, date_to={date_to})'
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.deepsearch.com/v1/compute?input={encoded_query}"

    try:
        response = make_request(url, headers, max_retries=3)
        data = response.json()

        if 'data' in data and 'pods' in data['data']:
            for pod in data['data']['pods']:
                if 'content' in pod and 'data' in pod['content']:
                    content_data = pod['content']['data']
                    if 'docs' in content_data:
                        return content_data['docs']
        return []
    except Exception as e:
        print(f"애널리스트 보고서 조회 오류: {e}")
        return []


# ==============================================================================
# Streamlit UI 초기 설정
# ==============================================================================
# [UI 구성]
# - 페이지 제목: KRX 검색기
# - 레이아웃: wide (넓은 화면 활용)
# - 구성 요소:
#   1. 제목 및 데이터 업데이트 정보
#   2. 검색 조건 설정 (Expander)
#   3. 검색 결과 표시
#   4. 필터링 기능

st.set_page_config(page_title='KRX 검색기', layout="wide")
st.markdown('<h1>KRX 상장사 뉴스 검색기 <span style="font-size: 0.5em; font-weight: normal;">(뉴스검색과 연계한 공시/IR/애널보고서/주가 분석)</span></h1>', unsafe_allow_html=True)
st.caption('※본 서비스는 Deepsearch의 공식서비스가 아니며, 정재광 과장이 Deepsearch API 문서를 참고하여 제작해본 서비스 예시입니다.')
st.markdown("### [📚 (참고링크) DeepSearch를 KRX 업무에 활용하는 방안 예시](https://beaten-by-the-market.github.io/deepsearch/api_guide.html)")


# ==============================================================================
# 데이터베이스 함수
# ==============================================================================

def get_last_update_time():
    """
    DB에서 상장사 데이터의 마지막 업데이트 시간을 조회합니다.

    [동작 설명]
    ds_entitysummary 테이블의 last_update 컬럼에서 최대값을 조회하여
    데이터가 언제 마지막으로 갱신되었는지 확인합니다.

    [데이터 갱신 주기]
    - GitHub Actions에서 매일 오전 7시(KST)에 자동 갱신
    - deepsearch_query_api.py 스크립트 실행

    Returns:
        str or None: "YYYY년 MM월 DD일" 형식의 날짜 문자열
                    조회 실패 시 None 반환

    Example:
        >>> get_last_update_time()
        '2024년 01월 15일'
    """
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # last_update 컬럼의 최대값 조회 (YYYYMMDD 형식으로 저장됨)
        cursor.execute("SELECT MAX(last_update) FROM ds_entitysummary")
        result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if result:
            # YYYYMMDD 문자열을 한국어 날짜 형식으로 변환
            update_date = datetime.strptime(str(result), "%Y%m%d")
            return update_date.strftime("%Y년 %m월 %d일")
        return None
    except Exception:
        return None


@st.cache_data
def load_data_from_db():
    """
    PostgreSQL DB에서 KRX 상장사 정보를 로드합니다.

    [동작 설명]
    ds_entitysummary 테이블에서 전체 상장사 정보를 조회합니다.
    Streamlit의 @st.cache_data 데코레이터로 결과를 캐싱하여
    앱 재실행 시에도 DB 재조회 없이 캐시된 데이터를 사용합니다.

    [테이블 구조: ds_entitysummary]
    - symbol: 종목 코드 (예: '005930')
    - symbol_nice: NICE 심볼 (예: 'NICE:380725')
    - entity_name: 기업명 (예: '삼성전자')
    - business_rid: 사업자등록번호 (하이픈 제거된 10자리)
    - company_rid: 법인등록번호 (하이픈 제거된 13자리)
    - mkt: 시장 구분 (KOSPI, KOSDAQ, KONEX)
    - last_update: 데이터 갱신일 (YYYYMMDD)

    [성능 최적화]
    - pd.read_sql_query 사용으로 한 번에 전체 데이터 로드
    - @st.cache_data로 캐싱하여 반복 조회 방지

    Returns:
        pd.DataFrame: 상장사 정보 DataFrame
                     조회 실패 시 빈 DataFrame 반환
    """
    connection = None
    try:
        connection = psycopg2.connect(**db_config)

        if connection:
            print("Connected to PostgreSQL database")

            # pd.read_sql_query로 한 번에 전체 데이터 로드 (성능 최적화)
            # 기존: fetchmany + pd.concat 반복 -> 비효율적
            # 개선: read_sql_query로 단일 호출
            df = pd.read_sql_query("SELECT * FROM ds_entitysummary", connection)
            return df

    except psycopg2.Error as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")


# 마지막 업데이트 시간 표시
last_update = get_last_update_time()
if last_update:
    st.caption(f"📅 상장종목 정보 업데이트: {last_update} (매일 오전 7시 자동 갱신)")

# 상장사 데이터 로드 (캐싱됨)
search_list_df_original = load_data_from_db()


# ==============================================================================
# 검색 조건 선택지 정의
# ==============================================================================
# [검색 조건 데이터 구조]
# 각 선택지는 DataFrame으로 관리되며, 사용자가 선택한 한글 레이블을
# API 쿼리 파라미터로 변환하는 데 사용됩니다.

# 국내뉴스 섹션 선택지
# 뉴스 문서의 세부 카테고리 (section 파라미터)
domestic_news_dict = {
    '국내뉴스': ['전체', '경제', '기술/IT', '문화', '사설', '사회', '세계', '연예', '정치'],
    'news': ['[""]', '["economy"]', '["tech"]', '["culture"]', '["opinion"]',
             '["society"]', '["world"]', '["entertainment"]', '["politics"]']
}
df_domestic_news = pd.DataFrame(domestic_news_dict)

# 언론사 그룹 선택지
# publisher.raw 필드를 사용한 Elasticsearch 쿼리 구문
# 각 그룹에 포함된 언론사 목록은 미리 정의되어 있음
news_comp_dict = {
    '언론사': [
        '전체', '중앙일간지', '중앙경제지',
        '중앙일간지 및 경제지', '석간지', '종합일간지, 지방지'
    ],
    'publisher': [
        # 전체: 모든 주요 언론사 포함
        "publisher.raw :('경향신문' or '국민일보' or '동아일보' or '서울신문' or '세계일보' or '아시아투데이' or '조선일보' or '중앙일보' or '한겨레' or '한국일보' or '뉴스토마토' or '디지털타임스' or '매일경제' or '머니투데이' or '서울경제' or '아주경제' or '이데일리' or '이투데이' or '전자신문' or '파이낸셜뉴스' or '한국경제' or '내일신문' or '문화일보' or '아시아경제' or '지역내일신문' or '헤럴드경제' or '중소기업뉴스' or '메트로경제' or '국제신문' or '부산일보')",
        # 중앙일간지: 주요 종합 일간지
        "publisher.raw :('경향신문' or '국민일보' or '동아일보' or '서울신문' or '세계일보' or '아시아투데이' or '조선일보' or '중앙일보' or '한겨레' or '한국일보')",
        # 중앙경제지: 경제 전문 일간지
        "publisher.raw :('뉴스토마토' or '디지털타임스' or '매일경제' or '머니투데이' or '서울경제' or '아주경제' or '이데일리' or '이투데이' or '전자신문' or '파이낸셜뉴스' or '한국경제')",
        # 중앙일간지 및 경제지: 위 두 그룹 합집합
        "publisher.raw :('경향신문' or '국민일보' or '동아일보' or '서울신문' or '세계일보' or '아시아투데이' or '조선일보' or '중앙일보' or '한겨레' or '한국일보' or '뉴스토마토' or '디지털타임스' or '매일경제' or '머니투데이' or '서울경제' or '아주경제' or '이데일리' or '이투데이' or '전자신문' or '파이낸셜뉴스' or '한국경제')",
        # 석간지
        "publisher.raw :('내일신문' or '문화일보' or '아시아경제' or '지역내일신문' or '헤럴드경제')",
        # 종합일간지, 지방지
        "publisher.raw :('메트로경제' or '국제신문' or '부산일보')"
    ]
}
df_news_comp = pd.DataFrame(news_comp_dict)

# 시장 구분 선택지 (필터링용 멀티셀렉트)
MARKET_OPTIONS = {
    '유가증권': 'KOSPI',
    '코스닥': 'KOSDAQ',
    '코넥스': 'KONEX'
}

# 이슈 카테고리 프리셋 정의
# 각 카테고리별로 관련 키워드 조합을 미리 정의
# 검색 후 필터링 단계에서 사용됨
ISSUE_CATEGORIES = {
    '전체': None,  # 필터 없음
    '계약/수주': '(수주 and 체결) or (수주 and 공급) or (계약 and 체결) or (계약 and 공급)',
    '인수/투자': '인수 or 합병 or 분할 or 영업양도 or 영업양수 or 엠앤에이 or 출자 or 투자',
    '실적': '(매출 and 발표) or (매출 and 공표) or (매출 and 결정) or (매출 and 기록) or (매출 and 달성) or (매출 and 공시) or (실적 and 발표) or (실적 and 공표) or (실적 and 결정) or (실적 and 기록) or (실적 and 달성) or (실적 and 공시) or (이익 and 발표) or (이익 and 공표) or (이익 and 결정) or (이익 and 기록) or (이익 and 달성) or (이익 and 공시) or (배당 and 발표) or (배당 and 공표) or (배당 and 결정) or (배당 and 기록) or (배당 and 달성) or (배당 and 공시)',
    '증자/감자': '증자 or 감자 or 주식교환 or 주식이전 or 우회상장',
    '회계/감사': '상장폐지 or 관리종목 or 자본잠식 or (비적정 and 감사) or (비적정 and 회계법인) or (의견거절 and 감사) or (의견거절 and 회계법인) or (회계처리 and 위반) or 분식',
    '소송/부도/회생': '소송 or 횡령 or 배임 or 부도 or 파산 or 회생 or (공소 and 대표이사) or (공소 and 임원) or (공소 and 이사) or (기소 and 대표이사) or (기소 and 임원) or (기소 and 이사) or (혐의 and 대표이사) or (혐의 and 임원) or (혐의 and 이사)'
}

# 이슈 카테고리별 키워드 리스트 생성 (필터링용)
def parse_keywords_from_query(query_str):
    """쿼리 문자열에서 키워드 목록 추출"""
    if query_str is None:
        return []
    # or로 분리하고 정리
    keywords = query_str.split(" or ")
    return [kw.strip() for kw in keywords]

ISSUE_KEYWORD_LISTS = {
    cat: parse_keywords_from_query(query)
    for cat, query in ISSUE_CATEGORIES.items()
}


# ==============================================================================
# 검색 조건 설정 UI
# ==============================================================================
# [검색 조건 UI 구성]
# 사용자가 검색 조건을 설정하는 영역입니다.
#
# [입력 항목]
# 1. 언론사 구분 / 뉴스 섹션 (한 행)
# 2. 추가할 언론사 입력
# 3. 선택된 언론사 표시
# 4. 기간 설정: 날짜 기준 또는 날짜+시간 기준
#
# [Session State 사용]
# Streamlit은 UI 상호작용 시 스크립트를 재실행하므로,
# 사용자 선택값을 유지하기 위해 st.session_state를 활용합니다.

with st.expander("🔍 검색 조건", expanded=True):

    # --------------------------------------------------------------------------
    # 1. 언론사/섹션 선택 (한 행으로 구성)
    # --------------------------------------------------------------------------
    st.subheader('언론사 및 섹션')

    col_pub, col_sec = st.columns(2)

    with col_pub:
        # 언론사 그룹 선택
        news_comp_selection = st.selectbox('언론사 구분', df_news_comp['언론사'])

    with col_sec:
        # 뉴스 섹션 선택
        domestic_news_selection = st.selectbox('뉴스 섹션', df_domestic_news['국내뉴스'])

    domestic_news_query = df_domestic_news[df_domestic_news['국내뉴스'] == domestic_news_selection]['news'].values[0]

    # 전체 언론사 목록 추출 (multiselect의 옵션으로 사용)
    all_publishers = df_news_comp[df_news_comp['언론사'] == '전체']['publisher'].values[0]
    all_publisher_list = all_publishers.replace("publisher.raw :(", "").replace(")", "").replace("'", "").split(" or ")

    # Session State: 언론사 그룹 변경 시 선택 목록 초기화
    if 'last_news_comp_selection' not in st.session_state or st.session_state.last_news_comp_selection != news_comp_selection:
        # 선택된 그룹의 언론사 목록 추출
        publishers = df_news_comp[df_news_comp['언론사'] == news_comp_selection]['publisher'].values[0]
        publisher_list = publishers.replace("publisher.raw :(", "").replace(")", "").replace("'", "").split(" or ")

        st.session_state.publisher_options = all_publisher_list
        # 전체 선택 시 모든 언론사를 디폴트로
        if news_comp_selection == '전체':
            st.session_state.selected_publishers = all_publisher_list.copy()
            st.session_state.publisher_multiselect = all_publisher_list.copy()
        else:
            st.session_state.selected_publishers = publisher_list
            st.session_state.publisher_multiselect = publisher_list.copy()
        st.session_state.last_news_comp_selection = news_comp_selection

    # 전체 선택 시: 안내 메시지와 언론사 목록 expander 표시
    # 그 외: 기존 multiselect 방식 유지
    if news_comp_selection == '전체':
        st.info('전체 언론사(약 575개)를 대상으로 합니다.')

        # 언론사 상세 정보 expander (접힌 상태)
        with st.expander('Deepsearch 제공 언론사 상세 및 [빅카인즈(BIG KINDS)](https://www.bigkinds.or.kr) 비교'):
            st.markdown('''
| 구분 | 딥서치 | 빅카인즈 |
|:---:|:---:|:---:|
| 총 언론사 | 약 575개 | 104개 |
| 중복 | 45개 | 45개 |
| 독점 | 529개 | 59개 |

**딥서치 독점:** 연합뉴스, 뉴스1, 뉴시스, JTBC, 채널A, TV조선, MBN, 조선비즈 등
**빅카인즈 독점 (딥서치 미제공):** 아시아투데이, 아주경제, 이투데이, 대한경제, 브릿지경제, OBS, 지역일보 다수
''')
            # 딥서치 언론사 목록
            st.markdown('---')
            st.caption('딥서치 제공 언론사 목록 (약 575개)')
            try:
                import os
                publishers_file = os.path.join(os.path.dirname(__file__), 'publishers_575.txt')
                with open(publishers_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                cols = st.columns(3)
                for i, line in enumerate(lines):
                    name = line.strip()
                    if name:
                        cols[i % 3].write(f"{i+1}. {name}")
            except Exception as e:
                st.write("언론사 목록을 불러올 수 없습니다.")

        # 전체 선택 시 쿼리는 빈 문자열 (필터 없음)
        news_comp_query = ''
        selected_publishers = []
    else:
        # 언론사 추가 콜백 함수
        def add_publisher_callback():
            publisher = st.session_state.add_publisher_input
            if publisher:
                if publisher not in st.session_state.publisher_options:
                    st.session_state.publisher_options.append(publisher)
                # multiselect 상태에 직접 추가
                if 'publisher_multiselect' in st.session_state:
                    current_selected = list(st.session_state.publisher_multiselect)
                    if publisher not in current_selected:
                        current_selected.append(publisher)
                    st.session_state.publisher_multiselect = current_selected
                # 입력 필드 초기화
                st.session_state.add_publisher_input = ''

        # 사용자 정의 언론사 추가
        st.text_input(
            "추가할 언론사 입력",
            key='add_publisher_input',
            on_change=add_publisher_callback
        )

        # 언론사 multiselect (session state로 값 관리)
        selected_publishers = st.multiselect(
            '선택된 언론사',
            options=st.session_state.publisher_options,
            key='publisher_multiselect'
        )
        st.session_state.selected_publishers = selected_publishers

        # 선택된 언론사를 API 쿼리 형식으로 변환
        # 형식: publisher.raw :('언론사1' or '언론사2' or ...)
        if selected_publishers:
            news_comp_query = " or ".join([f"'{publisher}'" for publisher in selected_publishers])
            news_comp_query = f"publisher.raw :({news_comp_query})"
        else:
            news_comp_query = ''

    # --------------------------------------------------------------------------
    # 2. 날짜/시간 설정
    # --------------------------------------------------------------------------
    # [기간 설정]
    # 검색할 문서의 기간을 설정합니다.
    #
    # [날짜 기준]
    # - date_from, date_to 파라미터 사용
    # - 형식: YYYYMMDD
    # - 문서의 발행일 기준으로 필터링
    #
    # [날짜 및 시간 기준]
    # - created_at 필드에 대한 범위 쿼리
    # - 형식: YYYY-MM-DDTHH:MM:SS
    # - 더 정밀한 시간 기반 필터링 가능
    st.subheader("날짜 및 시간 설정")

    # 날짜 기준 선택 라디오 버튼
    date_option = st.radio(
        '기간 필터',
        options=['날짜기준', '날짜+시간기준'],
        horizontal=True,
        key='date_option_radio'
    )

    use_date = (date_option == '날짜기준')
    use_datetime = (date_option == '날짜+시간기준')

    # 날짜 기준 입력 UI
    if use_date:
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date = st.date_input('시작일', key='start_date')
        with date_col2:
            end_date = st.date_input('종료일', key='end_date')

        if start_date and end_date:
            # DocumentSearch의 date_from, date_to 파라미터 형식
            date_query = f'date_from={start_date.strftime("%Y%m%d")} , date_to={end_date.strftime("%Y%m%d")}'
        else:
            date_query = ''
    else:
        date_query = ''

    # 날짜+시간 기준 입력 UI
    if use_datetime:
        datetime_col1, datetime_col2 = st.columns(2)
        with datetime_col1:
            datetime_start_date = st.date_input('시작 날짜', key='datetime_start_date')
            datetime_start_time = st.slider('시작 시간', 0, 24, 0, key='datetime_start_time')
        with datetime_col2:
            datetime_end_date = st.date_input('종료 날짜', key='datetime_end_date')
            datetime_end_time = st.slider('종료 시간', 0, 24, 0, key='datetime_end_time')

        if datetime_start_date and datetime_end_date:
            # created_at 필드에 대한 범위 쿼리 형식
            datetime_start = f"{datetime_start_date}T{datetime_start_time:02}:00:00"
            datetime_end = f"{datetime_end_date}T{datetime_end_time:02}:00:00"
            datetime_query = f'created_at:[\\"{datetime_start}\\" to \\"{datetime_end}\\"]'
        else:
            datetime_query = ''
    else:
        datetime_query = ''

    # 검색 버튼
    search_clicked = st.button('🔍 검색', type='primary', use_container_width=True)


# ==============================================================================
# 검색 실행
# ==============================================================================
# [검색 실행 로직]
# 1. 사용자가 설정한 조건들을 조합하여 DocumentSearch 쿼리 생성
# 2. API 호출하여 첫 페이지 결과 획득
# 3. 전체 페이지 수 확인 후 나머지 페이지 순차 요청
# 4. 결과를 DataFrame으로 병합하여 session_state에 저장
#
# [DocumentSearch 쿼리 구조]
# DocumentSearch(
#     ["news"],            # 뉴스 카테고리 고정
#     sections,            # 세부 섹션 (선택적)
#     "search_query",      # 검색어 및 필터 조건
#     date_from=YYYYMMDD,  # 시작일 (선택적)
#     date_to=YYYYMMDD,    # 종료일 (선택적)
#     count=100,           # 페이지당 결과 수 (최대 100)
#     page=N               # 페이지 번호
# )

if search_clicked:
    # 기간 필수 체크
    if not use_date and not use_datetime:
        st.error("기간은 반드시 선택해야 합니다. 짧을 수록 빨리 검색됩니다.")
    else:
        # 쿼리 파트 조합
        # query_parts: 카테고리, 섹션 등 쉼표로 구분되는 파라미터
        # query_parts_and: 검색어 부분 (and로 연결)
        # query_parts_comma: date_from, date_to 등 쉼표로 구분되는 파라미터
        query_parts = ['["news"]']  # 뉴스 카테고리 고정
        query_parts_and = []
        query_parts_comma = []

        # 뉴스 섹션 조건 추가
        if domestic_news_query:
            query_parts.append(domestic_news_query)

        # 언론사 조건 추가
        if news_comp_query:
            query_parts_and.append(news_comp_query)

        # 날짜 조건 추가
        if date_query:
            query_parts_comma.append(date_query)

        # 날짜+시간 조건 추가
        if datetime_query:
            query_parts_and.append(datetime_query)

        # None 값 및 빈 문자열 제거
        query_parts = [part for part in query_parts if part and part != 'None']
        query_parts_and = [part for part in query_parts_and if part and part != 'None']
        query_parts_comma = [part for part in query_parts_comma if part and part != 'None']

        # 최종 쿼리 조합
        intro = 'DocumentSearch('
        outro = ', count = 100, page = 1)'
        final_query_category = ' , '.join(query_parts)
        final_query_condition = ' and '.join(query_parts_and)
        final_query_comma = ' , '.join(query_parts_comma)

        # 완성된 DocumentSearch 쿼리
        final_query_all = (
            intro +
            final_query_category +
            (' , "' + final_query_condition + '"' if final_query_condition else '') +
            ((' , ' if final_query_comma else '') + final_query_comma) +
            outro
        )

        # 페이지네이션 처리
        current_page = 1
        url = generate_url(final_query_all, current_page)

        # 첫 페이지 요청
        response = make_request(url, headers)
        response_data = response.json()

        # API 응답에서 문서 데이터 추출
        # 응답 구조: data.pods[1].content.data.docs
        docs = response_data['data']['pods'][1]['content']['data']['docs']
        df_list = [pd.json_normalize(docs)]

        # 전체 페이지 수 확인
        last_page = response_data['data']['pods'][1]['content']['data']['last_page']

        # 진행률 표시
        st.caption('📡 DeepSearch API 호출중입니다. (하루 기준 약 1분 소요)')
        progress_bar = st.progress(0)

        # 나머지 페이지 순차 요청
        while current_page < last_page:
            current_page += 1
            url = generate_url(final_query_all, current_page)
            response = make_request(url, headers)
            response_data = response.json()

            docs = response_data['data']['pods'][1]['content']['data']['docs']
            df_list.append(pd.json_normalize(docs))

            # 진행률 업데이트
            progress = int(current_page / last_page * 100)
            progress_bar.progress(progress)

        # 전체 결과 병합
        df = pd.concat(df_list, ignore_index=True)

        # 중복 컬럼 제거
        df_show = df.loc[:, ~df.columns.duplicated()]

        # 결과 요약 표시
        if not df.empty and all(col in df.columns for col in ['section', 'publisher', 'author', 'title', 'content', 'content_url']):
            df_show = df[['section', 'publisher', 'author', 'title', 'content', 'content_url']]
            count = len(df_show)
            st.success(f"총 {count}건의 뉴스가 검색되었습니다. 아래 필터를 적용하여 결과를 확인하세요.")
        else:
            st.warning("선택한 기간에 해당 검색 결과가 없습니다. 검색 기간을 늘려보세요.")

        # 결과를 session_state에 저장 (필터링에서 사용)
        st.session_state.df = df


# ==============================================================================
# 결과 필터링 기능
# ==============================================================================
# [필터링 로직]
# 검색된 문서에서 조건에 맞는 문서만 추출합니다.
#
# [필터 조건]
# 1. 시장: KOSPI/KOSDAQ/KONEX (멀티셀렉트)
# 2. 종목: 특정 종목명 검색 (자동완성)
# 3. 이슈 카테고리: 계약/수주, 인수/투자, 실적 등
#
# [상장사 매칭 방식]
# 문서의 securities, entities, named_entities 필드에서 매칭

if 'df' in st.session_state:
    df = st.session_state.df

    with st.expander("📋 결과 필터", expanded=True):

        # ----------------------------------------------------------------------
        # 1. 시장/종목 필터 (라디오 버튼으로 선택)
        # ----------------------------------------------------------------------
        col_title1, col_help1 = st.columns([10, 1])
        with col_title1:
            st.subheader('시장 또는 종목')
        with col_help1:
            with st.popover('ℹ️'):
                st.markdown('DeepSearch가 자연어처리를 통해 기사주제가 해당종목에 대한 것으로 식별한 기사를 필터합니다. 例) 유가 상장사 "대상", "남성"은 단순히 "대상", "남성"이 있으면 매칭하지 않고, 기사가 해당 상장사에 대한 것일 때 식별됩니다.')

        filter_type = st.radio(
            '필터 유형',
            options=['시장별 필터', '종목별 필터', '내 관심종목'],
            horizontal=True,
            key='filter_type'
        )

        if filter_type == '시장별 필터':
            # 시장 필터
            selected_markets = st.multiselect(
                '시장 선택',
                options=list(MARKET_OPTIONS.keys()),
                default=list(MARKET_OPTIONS.keys()),
                key='filter_markets'
            )
            selected_market_codes = [MARKET_OPTIONS[m] for m in selected_markets]
            # 종목 필터 초기화
            st.session_state.selected_stocks = []

        elif filter_type == '종목별 필터':
            # 종목별 필터
            selected_market_codes = list(MARKET_OPTIONS.values())  # 전체 시장에서 검색

            col_stock_input, col_stock_select = st.columns([1, 1])

            with col_stock_input:
                stock_search_input = st.text_input(
                    '종목명 입력',
                    key='stock_search_input',
                    placeholder='예: 삼성전자'
                )
                st.caption('→ 종목명을 입력하면 오른쪽에서 종목코드 확인 후 선택')

            with col_stock_select:
                if stock_search_input:
                    filtered_stocks = search_list_df_original[
                        search_list_df_original['entity_name'].str.contains(stock_search_input, case=False, na=False)
                    ][['symbol', 'entity_name', 'mkt']].head(10)

                    if not filtered_stocks.empty:
                        stock_options = [f"{row['entity_name']} ({row['symbol']}, {row['mkt']})"
                                        for _, row in filtered_stocks.iterrows()]

                        selected_stock_display = st.selectbox(
                            '종목 선택',
                            options=['선택 안함'] + stock_options,
                            key='stock_select'
                        )

                        if selected_stock_display != '선택 안함':
                            selected_stock_name = selected_stock_display.split(' (')[0]
                            if 'selected_stocks' not in st.session_state:
                                st.session_state.selected_stocks = []
                            if selected_stock_name not in st.session_state.selected_stocks:
                                st.session_state.selected_stocks.append(selected_stock_name)
                    else:
                        st.selectbox('종목 선택', options=['검색 결과 없음'], disabled=True, key='stock_select_empty')
                else:
                    st.selectbox('종목 선택', options=['종목명을 입력하세요'], disabled=True, key='stock_select_placeholder')

            # 선택된 종목 표시 및 제거
            if 'selected_stocks' in st.session_state and st.session_state.selected_stocks:
                st.caption('선택된 종목:')
                stock_cols = st.columns(min(len(st.session_state.selected_stocks), 5))
                stocks_to_remove = []
                for i, stock in enumerate(st.session_state.selected_stocks):
                    with stock_cols[i % 5]:
                        if st.button(f'❌ {stock}', key=f'remove_{stock}'):
                            stocks_to_remove.append(stock)

                for stock in stocks_to_remove:
                    st.session_state.selected_stocks.remove(stock)
                    st.rerun()

        else:  # 내 관심종목
            selected_market_codes = list(MARKET_OPTIONS.values())  # 전체 시장에서 검색

            # 업로드 서식 다운로드 버튼
            import io
            template_df = pd.DataFrame({'종목코드': ['005930', '000660', '035720']})
            buffer = io.BytesIO()
            template_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            col_download, col_upload = st.columns([1, 2])

            with col_download:
                st.download_button(
                    label='📥 업로드 서식 다운로드',
                    data=buffer,
                    file_name='관심종목_서식.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

            with col_upload:
                uploaded_file = st.file_uploader(
                    '관심종목 엑셀 업로드',
                    type=['xlsx', 'xls'],
                    key='watchlist_upload',
                    help='종목코드 컬럼이 포함된 엑셀 파일을 업로드하세요'
                )

            # 안내 문구 강조
            st.info('⚠️ **종목코드는 6자리 숫자**로 입력해주세요. (예: 005930, 000660)\n\n'
                   '5930처럼 입력해도 자동으로 005930으로 변환됩니다.')

            # 업로드된 파일 처리
            if uploaded_file is not None:
                try:
                    watchlist_df = pd.read_excel(uploaded_file)

                    # 종목코드 컬럼 찾기
                    code_col = None
                    for col in watchlist_df.columns:
                        if '종목' in col or 'code' in col.lower() or '코드' in col:
                            code_col = col
                            break

                    if code_col is None and len(watchlist_df.columns) > 0:
                        code_col = watchlist_df.columns[0]  # 첫 번째 컬럼 사용

                    if code_col:
                        # 종목코드 추출 및 6자리로 변환 (앞에 0 채우기)
                        codes = watchlist_df[code_col].dropna().astype(str)
                        codes = codes.apply(lambda x: x.split('.')[0])  # 소수점 제거
                        codes = codes.apply(lambda x: x.zfill(6))  # 6자리로 zero-fill

                        # DB symbol 형식 처리 (KRX:000000 또는 000000 형식 모두 지원)
                        # symbol에서 순수 코드만 추출하여 비교
                        db_symbols = search_list_df_original['symbol'].dropna()
                        db_codes_only = db_symbols.apply(lambda x: x.split(':')[-1] if ':' in str(x) else str(x))

                        # 유효한 종목코드만 필터링 (DB에 있는 것만)
                        valid_codes = codes[codes.isin(db_codes_only.values)]

                        if not valid_codes.empty:
                            # 종목코드로 종목명 찾기 (DB symbol 형식에 맞춰서)
                            matching_mask = db_codes_only.isin(valid_codes.values)
                            watchlist_stocks = search_list_df_original[matching_mask.values]['entity_name'].tolist()

                            st.session_state.selected_stocks = watchlist_stocks

                            st.success(f'✅ {len(watchlist_stocks)}개 종목이 로드되었습니다.')

                            # 로드된 종목 표시
                            with st.expander(f'로드된 종목 목록 ({len(watchlist_stocks)}개)', expanded=False):
                                loaded_df = search_list_df_original[matching_mask.values][['symbol', 'entity_name', 'mkt']].copy()
                                loaded_df.columns = ['종목코드', '종목명', '시장']
                                st.dataframe(loaded_df, use_container_width=True, hide_index=True)

                            # 유효하지 않은 코드 표시
                            invalid_codes = codes[~codes.isin(db_codes_only.values)]
                            if not invalid_codes.empty:
                                st.warning(f'⚠️ {len(invalid_codes)}개 종목코드가 인식되지 않았습니다: {", ".join(invalid_codes.head(10).tolist())}')
                        else:
                            st.error('유효한 종목코드가 없습니다. 종목코드를 확인해주세요.')
                    else:
                        st.error('종목코드 컬럼을 찾을 수 없습니다.')

                except Exception as e:
                    st.error(f'파일 처리 중 오류가 발생했습니다: {str(e)}')

        # ----------------------------------------------------------------------
        # 2. 이슈 카테고리 필터
        # ----------------------------------------------------------------------
        col_title2, col_help2 = st.columns([10, 1])
        with col_title2:
            st.subheader('이슈 카테고리')
        with col_help2:
            with st.popover('ℹ️'):
                st.markdown('단순 키워드 매칭 된 기사를 필터합니다.')

        col_issue, col_add_keyword = st.columns([1, 1])

        with col_issue:
            selected_issue = st.selectbox(
                '카테고리 선택',
                options=list(ISSUE_CATEGORIES.keys()),
                key='filter_issue'
            )

        # 카테고리 변경 시 키워드 목록 초기화
        if 'last_selected_issue' not in st.session_state or st.session_state.last_selected_issue != selected_issue:
            issue_query = ISSUE_CATEGORIES.get(selected_issue, None)
            if issue_query:
                st.session_state.issue_keywords = issue_query.split(' or ')
                st.session_state.issue_keywords = [kw.strip() for kw in st.session_state.issue_keywords]
            else:
                st.session_state.issue_keywords = []
            st.session_state.last_selected_issue = selected_issue
            # 카테고리 변경 시 multiselect 상태 직접 업데이트
            st.session_state.issue_keyword_select = st.session_state.issue_keywords.copy()

        # 키워드 추가 콜백 함수
        def add_keyword_callback():
            keyword = st.session_state.add_issue_keyword
            if keyword:
                if 'issue_keywords' not in st.session_state:
                    st.session_state.issue_keywords = []
                if keyword not in st.session_state.issue_keywords:
                    st.session_state.issue_keywords.append(keyword)
                    # multiselect 상태를 업데이트하여 새 키워드 포함
                    if 'issue_keyword_select' in st.session_state:
                        current_selected = list(st.session_state.issue_keyword_select)
                        if keyword not in current_selected:
                            current_selected.append(keyword)
                        st.session_state.issue_keyword_select = current_selected
                # 입력 필드 초기화
                st.session_state.add_issue_keyword = ''

        with col_add_keyword:
            st.text_input(
                '키워드 추가',
                key='add_issue_keyword',
                placeholder='예: (횡령 and 대표이사)',
                on_change=add_keyword_callback
            )

        # 선택된 키워드 표시 (전체 선택 시 제외)
        if selected_issue != '전체' and 'issue_keywords' in st.session_state and st.session_state.issue_keywords:
            selected_keywords = st.multiselect(
                '적용할 키워드 (수정 가능)',
                options=st.session_state.issue_keywords,
                key='issue_keyword_select'
            )
            st.session_state.selected_issue_keywords = selected_keywords
        else:
            st.session_state.selected_issue_keywords = []

        # ----------------------------------------------------------------------
        # 필터 적용 버튼
        # ----------------------------------------------------------------------
        filter_clicked = st.button('🔍 필터 적용', type='primary', use_container_width=True)

    # ==========================================================================
    # 필터 실행
    # ==========================================================================
    if filter_clicked:
        # 필터 유형에 따라 상장사 목록 필터링
        if filter_type == '시장별 필터':
            if not selected_market_codes:
                st.error("시장을 하나 이상 선택해주세요.")
                st.stop()
            search_list_df = search_list_df_original[
                search_list_df_original['mkt'].isin(selected_market_codes)
            ]
        elif filter_type == '종목별 필터':
            if 'selected_stocks' not in st.session_state or not st.session_state.selected_stocks:
                st.error("종목을 하나 이상 선택해주세요.")
                st.stop()
            search_list_df = search_list_df_original[
                search_list_df_original['entity_name'].isin(st.session_state.selected_stocks)
            ]
        else:  # 내 관심종목
            if 'selected_stocks' not in st.session_state or not st.session_state.selected_stocks:
                st.error("관심종목 엑셀 파일을 업로드해주세요.")
                st.stop()
            search_list_df = search_list_df_original[
                search_list_df_original['entity_name'].isin(st.session_state.selected_stocks)
            ]

        if search_list_df.empty:
            st.write("선택한 조건에 맞는 상장사가 없습니다.")
        else:
                # 조회용 Set 생성 (O(1) in 연산을 위해)
                symbol_set = set(search_list_df['symbol'].dropna())
                symbol_nice_set = set(search_list_df['symbol_nice'].dropna())
                entity_name_set = set(search_list_df['entity_name'].dropna())
                business_rid_set = set(search_list_df['business_rid'].dropna())
                company_rid_set = set(search_list_df['company_rid'].dropna())

                # 식별자 -> 기업명 매핑 Dict 생성
                symbol_to_name = dict(zip(search_list_df['symbol'].dropna(),
                                          search_list_df.loc[search_list_df['symbol'].notna(), 'entity_name']))
                symbol_nice_to_name = dict(zip(search_list_df['symbol_nice'].dropna(),
                                               search_list_df.loc[search_list_df['symbol_nice'].notna(), 'entity_name']))
                business_rid_to_name = dict(zip(search_list_df['business_rid'].dropna(),
                                                search_list_df.loc[search_list_df['business_rid'].notna(), 'entity_name']))
                company_rid_to_name = dict(zip(search_list_df['company_rid'].dropna(),
                                               search_list_df.loc[search_list_df['company_rid'].notna(), 'entity_name']))

                def filter_df(row):
                    """각 문서 행에서 KRX 상장사 언급 여부를 확인"""
                    identified_list = []
                    matched = False

                    for col in ['securities', 'entities', 'named_entities']:
                        if col not in row or row[col] is None:
                            continue

                        for entry in row[col]:
                            identified = None

                            if 'symbol' in entry:
                                symbol = entry['symbol']
                                if symbol in symbol_set:
                                    matched = True
                                    identified = symbol_to_name.get(symbol)
                                elif symbol in symbol_nice_set:
                                    matched = True
                                    identified = symbol_nice_to_name.get(symbol)

                            elif 'name' in entry:
                                name = entry['name']
                                if name in entity_name_set:
                                    matched = True
                                    identified = name

                            elif 'business_rid' in entry:
                                brid = entry['business_rid'].replace('-', '')
                                if brid in business_rid_set:
                                    matched = True
                                    identified = business_rid_to_name.get(brid)

                            elif 'company_rid' in entry:
                                crid = entry['company_rid'].replace('-', '')
                                if crid in company_rid_set:
                                    matched = True
                                    identified = company_rid_to_name.get(crid)

                            if identified:
                                identified_list.append(identified)

                    identified_list = list(set(filter(None, identified_list)))
                    return pd.Series([matched, identified_list])

                # 전체 DataFrame에 필터 함수 적용
                filtered_df = df.apply(filter_df, axis=1)
                filtered_df.columns = ['matched', 'identified_symbols']

                # 매칭된 행만 추출
                filtered_df2 = df[filtered_df['matched']].copy()
                filtered_df2['identified_symbols'] = filtered_df['identified_symbols']

                # 이슈 카테고리 필터링
                def check_issue_category(row, issue_query):
                    """문서가 선택된 이슈 카테고리에 해당하는지 확인"""
                    if issue_query is None:
                        return True

                    text_fields = ['title', 'content', 'description', 'body', 'summary', 'text']
                    text_parts = []
                    for field in text_fields:
                        if field in row and row[field] is not None:
                            text_parts.append(str(row[field]))
                    text = ' '.join(text_parts).lower()

                    conditions = issue_query.split(' or ')
                    for condition in conditions:
                        condition = condition.strip()
                        if condition.startswith('(') and condition.endswith(')'):
                            inner = condition[1:-1]
                            if ' and ' in inner:
                                parts = [p.strip().lower() for p in inner.split(' and ')]
                                if all(p in text for p in parts):
                                    return True
                            else:
                                if inner.lower() in text:
                                    return True
                        else:
                            if condition.lower() in text:
                                return True
                    return False

                # 이슈 카테고리 필터 적용 (사용자가 선택한 키워드 사용)
                selected_keywords = st.session_state.get('selected_issue_keywords', [])
                if selected_keywords:
                    # 선택된 키워드를 쿼리 형식으로 변환
                    issue_query = ' or '.join(selected_keywords)
                    filtered_df2 = filtered_df2[
                        filtered_df2.apply(lambda row: check_issue_category(row, issue_query), axis=1)
                    ]

                # 매칭된 이슈 키워드 찾기
                def find_matched_issue_keywords(row):
                    """문서에서 매칭된 이슈 키워드 추출"""
                    matched_kws = []
                    keywords = st.session_state.get('selected_issue_keywords', [])
                    if not keywords:
                        return matched_kws

                    text_fields = ['title', 'content', 'description', 'body', 'summary', 'text']
                    text_parts = []
                    for field in text_fields:
                        if field in row and row[field] is not None:
                            text_parts.append(str(row[field]))
                    text = ' '.join(text_parts).lower()

                    for condition in keywords:
                        condition = condition.strip()
                        if condition.startswith('(') and condition.endswith(')'):
                            inner = condition[1:-1]
                            if ' and ' in inner:
                                parts = [p.strip().lower() for p in inner.split(' and ')]
                                if all(p in text for p in parts):
                                    matched_kws.append(condition)
                            else:
                                if inner.lower() in text:
                                    matched_kws.append(condition)
                        else:
                            if condition.lower() in text:
                                matched_kws.append(condition)
                    return matched_kws

                filtered_df2['matched_keywords'] = filtered_df2.apply(find_matched_issue_keywords, axis=1)

                # 긍부정 점수 추출 (json_normalize 후 평탄화된 컬럼 사용)
                # polarity.name, polarity.score 컬럼이 이미 존재함
                if 'polarity.name' in filtered_df2.columns:
                    filtered_df2['polarity_name'] = filtered_df2['polarity.name'].fillna('')
                else:
                    filtered_df2['polarity_name'] = ''

                if 'polarity.score' in filtered_df2.columns:
                    filtered_df2['polarity_score'] = filtered_df2['polarity.score'].fillna(0)
                else:
                    filtered_df2['polarity_score'] = 0

                # 결과를 session state에 저장 (특정 종목 필터 사용 시 유지)
                st.session_state.filtered_df2 = filtered_df2

    # ==========================================================================
    # 결과 표시 (session state에 데이터가 있으면 표시)
    # ==========================================================================
    if 'filtered_df2' in st.session_state:
        filtered_df2 = st.session_state.filtered_df2
        result_count = len(filtered_df2)
        if result_count > 0:
            st.success(f"검색 결과: {len(filtered_df2)}건")

            # --------------------------------------------------------------
            # 종목별 기사 통계 시각화 (원본 결과 기준)
            # --------------------------------------------------------------
            col_title3, col_help3 = st.columns([10, 1])
            with col_title3:
                st.subheader('📊 종목별 기사 통계')
            with col_help3:
                with st.popover('ℹ️'):
                    st.markdown('긍부정점수 및 신뢰도는 DeepSearch 제공')

            # identified_symbols 리스트를 개별 행으로 풀어서 집계
            stock_counts = {}
            for symbols in filtered_df2['identified_symbols']:
                if symbols:
                    for symbol in symbols:
                        stock_counts[symbol] = stock_counts.get(symbol, 0) + 1

            if stock_counts:
                # 종목별 긍부정 집계
                stock_polarity = {}
                for _, row in filtered_df2.iterrows():
                    symbols = row.get('identified_symbols', [])
                    polarity = row.get('polarity_name', '')
                    if symbols:
                        for symbol in symbols:
                            if symbol not in stock_polarity:
                                stock_polarity[symbol] = {'긍정': 0, '중립': 0, '부정': 0, '없음': 0}
                            if polarity == '긍정':
                                stock_polarity[symbol]['긍정'] += 1
                            elif polarity == '중립':
                                stock_polarity[symbol]['중립'] += 1
                            elif polarity == '부정':
                                stock_polarity[symbol]['부정'] += 1
                            else:
                                stock_polarity[symbol]['없음'] += 1

                # 전체 종목 표시 (기사수 내림차순)
                sorted_stocks = sorted(stock_counts.items(), key=lambda x: x[1], reverse=True)
                stock_data = []
                for stock, count in sorted_stocks:
                    pol = stock_polarity.get(stock, {'긍정': 0, '중립': 0, '부정': 0, '없음': 0})
                    stock_data.append({
                        '종목': stock,
                        '기사수': count,
                        '긍정': pol['긍정'],
                        '중립': pol['중립'],
                        '부정': pol['부정'],
                        '없음': pol['없음']
                    })
                stock_df = pd.DataFrame(stock_data)

                # 종목별 기사수 테이블
                st.caption(f'종목별 기사수 (총 {len(stock_df)}개 종목)')
                # 기사수 최대값을 모든 컬럼의 기준으로 사용
                max_count = int(stock_df['기사수'].max()) if not stock_df.empty else 1

                st.dataframe(
                    stock_df,
                    column_config={
                        '기사수': st.column_config.ProgressColumn(
                            '기사수',
                            min_value=0,
                            max_value=max_count,
                            format='%d'
                        ),
                        '긍정': st.column_config.ProgressColumn(
                            '긍정',
                            min_value=0,
                            max_value=max_count,
                            format='%d'
                        ),
                        '중립': st.column_config.ProgressColumn(
                            '중립',
                            min_value=0,
                            max_value=max_count,
                            format='%d'
                        ),
                        '부정': st.column_config.ProgressColumn(
                            '부정',
                            min_value=0,
                            max_value=max_count,
                            format='%d'
                        ),
                        '없음': st.column_config.ProgressColumn(
                            '없음',
                            min_value=0,
                            max_value=max_count,
                            format='%d'
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )

            st.divider()

            # --------------------------------------------------------------
            # 결과 테이블
            # --------------------------------------------------------------
            st.subheader('📰 검색 결과')

            # 표시할 컬럼 선택 (순서: 원문, 언론사, 섹션, 제목, 관련종목, 매칭키워드, 긍부정, 신뢰도)
            display_columns = ['content_url', 'publisher', 'section', 'title', 'identified_symbols', 'polarity_name', 'polarity_score']
            if st.session_state.get('selected_issue_keywords', []):
                display_columns.insert(5, 'matched_keywords')

            filtered_df3 = filtered_df2[[col for col in display_columns if col in filtered_df2.columns]]

            # 컬럼명 한글화
            column_names = {
                'section': '섹션',
                'publisher': '언론사',
                'title': '제목',
                'content': '내용',
                'matched_keywords': '매칭 키워드',
                'polarity_name': '긍부정',
                'polarity_score': '신뢰도',
                'identified_symbols': '관련 종목',
                'content_url': '원문'
            }
            filtered_df3 = filtered_df3.rename(columns=column_names)

            # 긍부정 색상 매핑 함수
            def color_polarity(val):
                if val == '긍정':
                    return 'background-color: #d4edda; color: #155724'
                elif val == '부정':
                    return 'background-color: #f8d7da; color: #721c24'
                else:
                    return 'background-color: #fff3cd; color: #856404'

            # 결과 테이블 표시
            st.dataframe(
                filtered_df3.reset_index(drop=True),
                column_config={
                    '원문': st.column_config.LinkColumn(display_text='원문'),
                    '긍부정': st.column_config.TextColumn(
                        '긍부정',
                        help='긍정/중립/부정'
                    ),
                    '신뢰도': st.column_config.ProgressColumn(
                        '신뢰도',
                        help='AI 분석 신뢰도 (0~1)',
                        min_value=0,
                        max_value=1,
                        format='%.2f'
                    )
                },
                use_container_width=True,
                column_order=['원문', '언론사', '섹션', '제목', '관련 종목', '매칭 키워드', '긍부정', '신뢰도']
            )

            # --------------------------------------------------------------
            # 특정 종목 필터 (검색 결과 아래에 추가 섹션으로 표시)
            # --------------------------------------------------------------
            st.divider()
            st.subheader('🔎 종목별 뉴스필터 및 최근 공시/IR/애널리스트 보고서 비교확인')

            # 검색 결과에서 발견된 모든 종목 추출
            all_found_stocks = set()
            for symbols in filtered_df2['identified_symbols']:
                if symbols:
                    all_found_stocks.update(symbols)

            all_found_stocks = sorted(list(all_found_stocks))

            if all_found_stocks:
                # 이전에 선택한 종목이 현재 옵션에 없으면 초기화
                if 'result_stock_filter' in st.session_state:
                    current_selection = st.session_state.result_stock_filter
                    if current_selection and current_selection not in all_found_stocks:
                        st.session_state.result_stock_filter = None

                # 단일 선택 드롭다운 (selectbox)
                stock_options = [''] + all_found_stocks  # 빈 옵션 추가
                selected_stock = st.selectbox(
                    '종목 선택',
                    options=stock_options,
                    key='result_stock_filter',
                    format_func=lambda x: '종목을 선택하세요' if x == '' else x
                )

                # 선택한 종목이 있으면 상세 정보 표시
                if selected_stock:
                    st.subheader(f'📈 {selected_stock} 상세 정보')

                    # 공통 변수 설정
                    today = datetime.now()
                    one_year_ago = (today - timedelta(days=365)).strftime('%Y-%m-%d')
                    today_str = today.strftime('%Y-%m-%d')

                    # 종목 심볼 조회 (공시/보고서/주가 API용)
                    stock_symbol_for_docs = None
                    stock_match_for_docs = search_list_df_original[
                        search_list_df_original['entity_name'] == selected_stock
                    ]
                    if not stock_match_for_docs.empty:
                        stock_symbol_for_docs = stock_match_for_docs.iloc[0]['symbol']

                    # ----------------------------------------------------------
                    # 4개 컬럼 레이아웃: 뉴스, 공시, IR, 애널리스트 보고서
                    # ----------------------------------------------------------
                    col_news, col_disclosure, col_ir, col_research = st.columns(4)

                    # 컬럼 1: 뉴스 기사
                    with col_news:
                        st.markdown('#### 📰 관련 뉴스')
                        st.caption('위의 검색 결과에서 필터합니다')

                        stock_filtered_df = filtered_df2[
                            filtered_df2['identified_symbols'].apply(
                                lambda x: selected_stock in (x or [])
                            )
                        ]

                        if stock_filtered_df.empty:
                            st.info('해당 종목의 뉴스가 없습니다.')
                        else:
                            st.caption(f'총 {len(stock_filtered_df)}건')
                            news_display = stock_filtered_df[['content_url', 'publisher', 'title', 'polarity_name']].copy()
                            news_display = news_display.rename(columns={
                                'content_url': '원문',
                                'publisher': '언론사',
                                'title': '제목',
                                'polarity_name': '긍부정'
                            })
                            st.dataframe(
                                news_display.reset_index(drop=True),
                                column_config={
                                    '원문': st.column_config.LinkColumn(display_text='원문')
                                },
                                hide_index=True,
                                height=400
                            )

                    # 컬럼 2: 공시
                    with col_disclosure:
                        st.markdown('#### 📋 최근 공시')
                        st.caption('DeepSearch 제공, 原소스: DART')

                        with st.spinner('공시 조회 중...'):
                            if stock_symbol_for_docs:
                                disclosures = get_disclosure_documents(
                                    stock_symbol_for_docs, one_year_ago, today_str, headers, count=50
                                )
                            else:
                                disclosures = []

                        if not disclosures:
                            st.info('최근 1년간 공시가 없습니다.')
                        else:
                            st.caption(f'최근 1년 {len(disclosures)}건')
                            disclosure_data = []
                            for doc in disclosures:
                                disclosure_data.append({
                                    '원문': doc.get('content_url', '#'),
                                    '일자': doc.get('created_at', '')[:10] if doc.get('created_at') else '',
                                    '제목': doc.get('title', '제목 없음')
                                })
                            disclosure_df = pd.DataFrame(disclosure_data)
                            st.dataframe(
                                disclosure_df,
                                column_config={
                                    '원문': st.column_config.LinkColumn(display_text='원문')
                                },
                                hide_index=True,
                                height=400
                            )

                    # 컬럼 3: IR
                    with col_ir:
                        st.markdown('#### 📢 최근 IR 자료')
                        st.caption('DeepSearch 제공')

                        with st.spinner('IR 조회 중...'):
                            if stock_symbol_for_docs:
                                ir_docs = get_ir_documents(
                                    stock_symbol_for_docs, one_year_ago, today_str, headers, count=50
                                )
                            else:
                                ir_docs = []

                        if not ir_docs:
                            st.info('최근 1년간 배포한 IR자료가 없습니다. 투자자와 소통을 하지 않습니다.')
                        else:
                            st.caption(f'최근 1년 {len(ir_docs)}건')
                            ir_data = []
                            for doc in ir_docs:
                                ir_data.append({
                                    '원문': doc.get('content_url', '#'),
                                    '일자': doc.get('created_at', '')[:10] if doc.get('created_at') else '',
                                    '제목': doc.get('title', '제목 없음')
                                })
                            ir_df = pd.DataFrame(ir_data)
                            st.dataframe(
                                ir_df,
                                column_config={
                                    '원문': st.column_config.LinkColumn(display_text='원문')
                                },
                                hide_index=True,
                                height=400
                            )

                    # 컬럼 4: 애널리스트 보고서
                    with col_research:
                        st.markdown('#### 📊 최근 애널리스트 보고서')
                        st.caption('DeepSearch 제공')

                        with st.spinner('보고서 조회 중...'):
                            if stock_symbol_for_docs:
                                reports = get_analyst_reports(
                                    stock_symbol_for_docs, one_year_ago, today_str, headers, count=50
                                )
                            else:
                                reports = []

                        if not reports:
                            st.info('최근 1년간 보고서가 없습니다.')
                        else:
                            st.caption(f'최근 1년 {len(reports)}건')
                            report_data = []
                            for doc in reports:
                                report_data.append({
                                    '원문': doc.get('content_url', '#'),
                                    '일자': doc.get('created_at', '')[:10] if doc.get('created_at') else '',
                                    '증권사': doc.get('publisher', ''),
                                    '제목': doc.get('title', '제목 없음')
                                })
                            report_df = pd.DataFrame(report_data)
                            st.dataframe(
                                report_df,
                                column_config={
                                    '원문': st.column_config.LinkColumn(display_text='원문')
                                },
                                hide_index=True,
                                height=400
                            )

                    st.divider()

                    # ----------------------------------------------------------
                    # 주가 차트 섹션
                    # ----------------------------------------------------------
                    st.markdown('#### 📈 주가 정보')
                    st.caption('DeepSearch 제공, 原소스: KOSCOM')

                    # 기간 선택 라디오 버튼
                    period_options = {
                        '1개월': 30,
                        '6개월': 180,
                        '52주': 365
                    }

                    selected_period = st.radio(
                        '기간 선택',
                        options=list(period_options.keys()),
                        horizontal=True,
                        key='stock_price_period'
                    )

                    # 날짜 계산 (today는 이미 위에서 정의됨)
                    date_from_52w = (today - timedelta(days=365)).strftime('%Y-%m-%d')
                    date_to = today.strftime('%Y-%m-%d')

                    # 종목이 바뀌었거나 데이터가 없으면 52주 데이터 로드
                    if ('loaded_stock' not in st.session_state or
                        st.session_state.loaded_stock != selected_stock or
                        'full_price_df' not in st.session_state):

                        with st.spinner('주가 데이터 조회 중...'):
                            # 심볼 조회 (stock_symbol_for_docs는 이미 위에서 정의됨)
                            if stock_symbol_for_docs:
                                st.session_state.full_price_df = get_stock_prices(stock_symbol_for_docs, date_from_52w, date_to, headers)
                            else:
                                st.session_state.full_price_df = get_stock_prices(selected_stock, date_from_52w, date_to, headers)
                            st.session_state.loaded_stock = selected_stock

                    # 선택된 기간에 맞게 데이터 필터링
                    full_df = st.session_state.full_price_df
                    if not full_df.empty:
                        days_back = period_options[selected_period]
                        cutoff_date = (today - timedelta(days=days_back)).strftime('%Y-%m-%d')
                        if 'date' in full_df.columns:
                            price_df = full_df[full_df['date'].astype(str) >= cutoff_date].copy()
                        else:
                            price_df = full_df.tail(days_back).copy()
                    else:
                        price_df = pd.DataFrame()

                    if not price_df.empty and 'close' in price_df.columns:
                        # 주가 요약 정보 (차트 위에 표시)
                        if len(price_df) > 0:
                            latest = price_df.iloc[-1]
                            col_price1, col_price2, col_price3, col_price4 = st.columns(4)
                            with col_price1:
                                st.metric('현재가', f"{int(latest.get('close', 0)):,}원")
                            with col_price2:
                                change = latest.get('change', 0)
                                change_rate = latest.get('change_rate', 0)
                                st.metric('전일 대비', f"{int(change):,}원", f"{change_rate:.2f}%")
                            with col_price3:
                                st.metric('고가', f"{int(latest.get('high', 0)):,}원")
                            with col_price4:
                                st.metric('저가', f"{int(latest.get('low', 0)):,}원")

                        # Plotly 차트 생성
                        fig = go.Figure()

                        # 캔들스틱 차트
                        # 날짜에서 시간 부분 제거 (T00:00:00 제거)
                        if 'date' in price_df.columns:
                            x_data = price_df['date'].astype(str).str[:10]
                        else:
                            x_data = price_df.index.astype(str).str[:10]

                        # 기간별 레이블 표시 간격 설정
                        tick_interval = {
                            '1주일': 1,    # 모든 레이블 표시
                            '1개월': 5,    # 5개마다
                            '6개월': 30,   # 30개마다
                            '52주': 60     # 60개마다
                        }.get(selected_period, 1)

                        fig.add_trace(go.Candlestick(
                            x=x_data,
                            open=price_df['open'],
                            high=price_df['high'],
                            low=price_df['low'],
                            close=price_df['close'],
                            name='주가',
                            increasing_line_color='#EF5350',  # 상승: 빨강
                            decreasing_line_color='#1976D2'   # 하락: 파랑
                        ))

                        # 거래량 바 차트 (보조 축)
                        if 'volume' in price_df.columns:
                            fig.add_trace(go.Bar(
                                x=x_data,
                                y=price_df['volume'],
                                name='거래량',
                                yaxis='y2',
                                opacity=0.3,
                                marker_color='#aec7e8'
                            ))

                        fig.update_layout(
                            title=f'{selected_stock} 주가 차트 ({selected_period})',
                            xaxis=dict(
                                title='날짜',
                                type='category',  # 카테고리 타입: 데이터 있는 날짜만 표시
                                dtick=tick_interval,  # 레이블 표시 간격
                                rangeslider=dict(visible=False)  # 범위 슬라이더 숨김
                            ),
                            yaxis=dict(
                                title='주가 (원)',
                                tickformat=','  # 전체 숫자 표시 (k 약어 사용 안함)
                            ),
                            yaxis2=dict(
                                title='거래량',
                                overlaying='y',
                                side='right',
                                showgrid=False,
                                tickformat='.2s'  # M 단위 사용
                            ),
                            hovermode='x unified',
                            height=400,
                            legend=dict(
                                orientation='h',
                                yanchor='bottom',
                                y=1.02,
                                xanchor='right',
                                x=1
                            )
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info('주가 데이터를 불러올 수 없습니다.')

            else:
                st.info("검색 결과에서 관련 종목이 식별되지 않았습니다.")
        else:
            st.warning("필터 조건에 맞는 결과가 없습니다.")

else:
    st.write("먼저 '검색' 버튼을 눌러 데이터를 불러오세요.")


# ==============================================================================
# 실행 방법 (참고용 주석)
# ==============================================================================
# [로컬 실행]
# 1. 가상환경 활성화:
#    python -m venv venv
#    venv\Scripts\activate  # Windows
#    source venv/bin/activate  # Mac/Linux
#
# 2. 의존성 설치:
#    pip install -r requirements.txt
#
# 3. 환경변수 설정 (.env 파일 생성):
#    API_KEY=your_deepsearch_api_key
#    DB_HOST=db.xxxxx.supabase.co
#    DB_PORT=5432
#    DB_NAME=postgres
#    DB_USER=your_db_user
#    DB_PASSWORD=your_db_password
#
# 4. 실행:
#    streamlit run deepsearch_query.py
#
# [Streamlit Cloud 배포]
# 1. GitHub 저장소에 코드 푸시
# 2. Streamlit Cloud에서 앱 생성
# 3. Secrets 설정 (secrets.toml 형식):
#    [general]
#    api_key = "your_api_key"
#    db_user = "your_db_user"
#    db_password = "your_db_password"
#    db_host = "db.xxxxx.supabase.co"
#    db_port = "5432"
#    db_name = "postgres"
#
#    [crud]
#    db_user = "your_crud_user"
#    db_password = "your_crud_password"
#    db_host = "db.xxxxx.supabase.co"
#    db_port = "5432"
