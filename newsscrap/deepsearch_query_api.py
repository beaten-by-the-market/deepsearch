import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import time
from tqdm import tqdm
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed


# InsecureRequestWarning 비활성화
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#-----------------------------------------------------------
# 환경변수 설정
#-----------------------------------------------------------
# 인증키 설정
import os
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 불러오기
api_key = os.getenv("API_KEY")


#접속정보-CRUD
# Database configuration
db_config_crud = {
    'user': os.getenv("DB_USER_CRUD"),
    'password': os.getenv("DB_PASSWORD_CRUD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'database': os.getenv("DB_NAME"),
}

#접속정보-일반
# Database configuration
db_config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'database': os.getenv("DB_NAME"),
}

# 인증 헤더에 API 키 적용
headers = {
    'Authorization': f'Basic {api_key}'
}

# API 호출 URL
url_base = 'https://api.deepsearch.com/v1/compute?input='


#-----------------------------------------------------------
# 딥서치로 상장사 목록 불러오기
#-----------------------------------------------------------

# 상장시장구분코드 (1=코스피, 2=코스닥, 3=코넥스, 4=제3시장, 9=대상아님)
# 빈데이터프레임
listed_df = pd.DataFrame()

for mkt in range(1, 4):
    query = f"""
    FindEntity("Financial","{mkt}" ,fields=["market_id"])
    """
    url = f'{url_base}{query}'.replace('\n','')

    # SSL 인증서 검증 비활성화하고 GET 요청 보내기
    response = requests.get(url, headers=headers, verify=False)
    
    # 응답 출력
    print(response.status_code)
    
    # 응답 데이터를 JSON으로 변환하여 저장
    response_data = response.json()
    
    # 'data' 추출
    data_dict = response_data['data']['pods'][1]['content']['data']
    loop_df = pd.DataFrame(data_dict)
    mkt_name = np.where(mkt == 1, 'KOSPI', 
                        np.where(mkt == 2, 'KOSDAQ',
                                 np.where(mkt ==3, 'KONEX',
                                          '기타시장')))
    loop_df['mkt'] = mkt_name
    listed_df = pd.concat([listed_df, loop_df])
    

# 기업별 개황 받아오는 과정(NICE코드와 사업자등록번호용)
# KeyError 발생한 symbol을 저장할 리스트
key_error_symbols = []

def fetch_entity_summary(symbol):
    """개별 symbol에 대해 API 호출하는 함수"""
    query = f"GetEntitySummary({symbol})"
    url = f'{url_base}{query}'

    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            response_data = response.json()

            if 'data' in response_data and 'pods' in response_data['data'] and len(response_data['data']['pods']) > 1:
                try:
                    data_dict = response_data['data']['pods'][1]['content']['data']
                    return pd.DataFrame(data_dict)
                except KeyError as e:
                    print(f"KeyError for {symbol}: {e}")
                    return None
            else:
                print(f"No valid data for {symbol}")
                return None

        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= max_retries:
                print(f"Failed to retrieve data for {symbol} after {max_retries} attempts. Error: {e}")
                return None
            else:
                time.sleep(2)  # 재시도 전 2초 대기

    return None

# 병렬 API 호출 (동시 10개)
print("Fetching entity summaries (parallel, max_workers=10)...")
symbols = list(listed_df['symbol'])
results = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_entity_summary, symbol): symbol for symbol in symbols}

    for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching data"):
        result = future.result()
        if result is not None:
            results.append(result)

# 결과 합치기
if results:
    summary_df = pd.concat(results, ignore_index=True)
else:
    summary_df = pd.DataFrame()

# 소속시장 정보 합쳐주기
summary_df2 = pd.merge(summary_df, listed_df[['symbol','mkt']],
                              how = 'left',
                              on = 'symbol')

#오늘날짜 설정 (한국 시간대 기준)
today = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y%m%d')

#업데이트일 추가
summary_df2['last_update'] = today

summary_df = summary_df2

#-----------------------------------------------------------
# ETF 제외 (일반법인만 필터링)
# company_type_l1: 1=일반법인, 8=기타법인(ETF 등)
#-----------------------------------------------------------
print(f"\n{'='*50}")
print(f"필터링 전 총 {len(summary_df)}개 종목")
print(f"컬럼 목록: {list(summary_df.columns)}")

if 'company_type_l1' in summary_df.columns:
    print(f"company_type_l1 고유값: {summary_df['company_type_l1'].unique()}")
    print(f"company_type_l1 데이터타입: {summary_df['company_type_l1'].dtype}")
    print(f"company_type_l1 값별 개수:")
    print(summary_df['company_type_l1'].value_counts())

    # 문자열로 변환 후 필터링
    summary_df['company_type_l1'] = summary_df['company_type_l1'].astype(str)
    summary_df = summary_df[summary_df['company_type_l1'] == '1']
    print(f"필터링 후 총 {len(summary_df)}개 종목 (company_type_l1='1' 일반법인만)")
else:
    print("⚠️ company_type_l1 컬럼이 없습니다!")
print(f"{'='*50}\n")

#-----------------------------------------------------------
#판다스를 SQL로 저장하기
#-----------------------------------------------------------


# Initialize connection variable
connection = None

# 집어넣기
try:
    # Create a connection to the database
    connection = psycopg2.connect(**db_config_crud)

    if connection:
        print("Connected to PostgreSQL database")

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Drop the table if it exists
        drop_table_query = "DROP TABLE IF EXISTS ds_entitysummary"
        cursor.execute(drop_table_query)
        print("Table 'ds_entitysummary' dropped")
    
        # Define the SQL CREATE TABLE statement (PostgreSQL 문법)
        create_table_query = """
        CREATE TABLE ds_entitysummary (
            symbol VARCHAR(100),
            entity_name VARCHAR(100),
            symbol_nice VARCHAR(100),
            ceo VARCHAR(100),
            business_rid VARCHAR(100),
            company_rid VARCHAR(100),
            tel VARCHAR(100),
            fax VARCHAR(100),
            website VARCHAR(100),
            email VARCHAR(100),
            zipcode VARCHAR(100),
            address_land_lot VARCHAR(200),
            address_road_name VARCHAR(200),
            company_type_l1 VARCHAR(100),
            company_type_l2 VARCHAR(100),
            company_type_size VARCHAR(100),
            market_id VARCHAR(100),
            is_external_audit VARCHAR(100),
            conglomerate_id VARCHAR(100),
            industry_id VARCHAR(100),
            industry_name VARCHAR(100),
            fs_type VARCHAR(100),
            fiscal_year_end VARCHAR(100),
            business_area VARCHAR(200),
            date_founded VARCHAR(100),
            date_listed VARCHAR(100),
            is_alive VARCHAR(100),
            is_closed VARCHAR(100),
            status VARCHAR(100),
            mkt VARCHAR(10),
            last_update VARCHAR(8)
        )
        """

        # Create the table
        cursor.execute(create_table_query)
        print("Table 'ds_entitysummary' created successfully")

        # Insert the data from the DataFrame into the table using executemany (batch insert)
        insert_query = """INSERT INTO ds_entitysummary (
        symbol, entity_name, symbol_nice, ceo, business_rid, company_rid, tel,
        fax, website, email, zipcode, address_land_lot, address_road_name,
        company_type_l1, company_type_l2, company_type_size, market_id,
        is_external_audit, conglomerate_id, industry_id, industry_name, fs_type,
        fiscal_year_end, business_area, date_founded, date_listed, is_alive,
        is_closed, status, mkt, last_update
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # DataFrame을 튜플 리스트로 변환
        columns = ['symbol', 'entity_name', 'symbol_nice', 'ceo', 'business_rid',
                   'company_rid', 'tel', 'fax', 'website', 'email', 'zipcode',
                   'address_land_lot', 'address_road_name', 'company_type_l1',
                   'company_type_l2', 'company_type_size', 'market_id',
                   'is_external_audit', 'conglomerate_id', 'industry_id',
                   'industry_name', 'fs_type', 'fiscal_year_end', 'business_area',
                   'date_founded', 'date_listed', 'is_alive', 'is_closed',
                   'status', 'mkt', 'last_update']

        data = [tuple(row[col] for col in columns) for _, row in summary_df.iterrows()]

        # execute_values로 빠른 배치 삽입
        print(f"Inserting {len(data)} rows using execute_values...")
        insert_query_fast = """INSERT INTO ds_entitysummary (
            symbol, entity_name, symbol_nice, ceo, business_rid, company_rid, tel,
            fax, website, email, zipcode, address_land_lot, address_road_name,
            company_type_l1, company_type_l2, company_type_size, market_id,
            is_external_audit, conglomerate_id, industry_id, industry_name, fs_type,
            fiscal_year_end, business_area, date_founded, date_listed, is_alive,
            is_closed, status, mkt, last_update
        ) VALUES %s"""
        execute_values(cursor, insert_query_fast, data, page_size=1000)

        # Commit the changes
        connection.commit()
        print("Data inserted successfully")

except psycopg2.Error as e:
    print(f"Error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

print("✅ 상장사 데이터 적재 완료!")

