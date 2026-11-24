# %% [markdown]
# # 5-02 지표·코드 찾기 — "이 지표 DeepSearch에 있어? 무슨 코드로 봐?"
#
# **질문 예시:** "삼성전자 종목코드 알려줘", "코스피 지수 코드 뭐야?", "원/달러 환율은 어떤 코드로 봐?",
# "베이시스 데이터 있어?", "신용융자 잔고 어디서 봐?", "한국 관련 FRED 지표 뭐 있어?"
#
# CHECK 원본(`5_데이터조회/02_지표코드찾기`)은 코드 카탈로그와 응답 필드까지 뒤져 "어디서 보는지"를 찾았습니다.
# DeepSearch에는 시리즈 검색 함수 `FindEntity("DataSeries", 검색어)`가 있지만 **어떤 검색어든 0건**이라 쓸 수 없습니다(2026-11-25 확인).
# 대신 아래 방법을 씁니다.
#
# | 찾는 것 | 방법 | 함수 |
# |---|---|---|
# | 종목코드 | 전 종목 목록에서 이름 검색 | `GetStockSymbols` |
# | 지수 코드 | 지수 목록(11종) | `GetMarketIndexSymbols` |
# | FRED 지표 | 아는 시리즈 → 속한 카테고리 → 같은 카테고리 시리즈 목록 | `GetFredCategoryOfDataSeries`, `GetFredDataSeriesListUnderCategory`, `QueryFredSeriesInfo` |
# | 한국은행 지표 | 통계표 코드로 항목·**마지막 시점** 확인 | `QueryBankOfKoreaSeriesInfo` |
# | IMF·OECD 지표 | 한 시리즈에서 같은 국가·같은 지표 목록 펼치기 | `GetImfIndicatorListOfSameCountry`, `GetOecdRelatedIndicatorList` |
# | 시세·밸류 지표 이름 | 자연어 질의가 데이터로 해석되는지 확인 | compute 자연어 |

# %%
ASOF = "2026-11-24"

# %% [markdown]
# ## 1. 종목코드 찾기
# `universe()`는 `GetStockSymbols()` 전 종목(4,400여 개, ETF 포함) 표입니다. 이름 일부로 찾습니다.

# %%
u = universe()

def find_stock(text):
    hit = u[u["name"].str.contains(text, case=False, regex=False)]
    return hit[["symbol", "name", "market", "company_type_l1", "industry_name"]].head(10)

display(find_stock("삼성전자"))
find_stock("하이닉스")

# %% [markdown]
# ## 2. 지수 코드
# DeepSearch 지수는 코스피·코스닥 계열 11종뿐입니다. KRX 섹터지수·테마지수·KRX300·VKOSPI는 없습니다.

# %%
ds_df("GetMarketIndexSymbols()")[["symbol", "name_ko", "name_en", "index_id"]]

# %% [markdown]
# ## 3. FRED 지표 찾기 — 카테고리 따라가기
# 아는 시리즈 하나에서 출발해 그 시리즈가 속한 카테고리를 보고, 같은 카테고리의 다른 시리즈를 펼칩니다.
# 펼친 목록을 제목 키워드로 거르고, **마지막 관측일**로 지금도 갱신되는지 확인합니다.
# 예: 한국 10년 금리(`IRLTLT01KRM156N`)와 원/달러(`DEXKOUS`)에서 출발.

# %%
cats = ds_df('GetFredCategoryOfDataSeries(["IRLTLT01KRM156N", "DEXKOUS"])')
cats

# %%
def fred_category(cat_ids, keyword=None, fresh_after="2026-01-01"):
    ids = ", ".join(str(int(c)) for c in cat_ids)
    df = ds_df(f"GetFredDataSeriesListUnderCategory([{ids}])")
    if keyword:
        df = df[df["title"].str.contains(keyword, case=False, regex=True)]
    df = df.assign(최신=pd.to_datetime(df["observation_end"]) >= pd.Timestamp(fresh_after))
    return df[["entity_id", "title", "frequency_short", "observation_end", "최신"]].sort_values(
        ["최신", "observation_end"], ascending=False).drop_duplicates("entity_id").reset_index(drop=True)

korea_cat = cats.loc[cats["name"].str.startswith("Korea, Republic"), "category_id"].unique().tolist()
kr = fred_category(korea_cat)
print(f"'Korea, Republic of' 카테고리 시리즈 {len(kr)}개, 이 중 2026년까지 갱신되는 것 {kr['최신'].sum()}개")
kr[kr["최신"]].head(20)

# %% [markdown]
# 키워드로 좁히기: 같은 카테고리에서 금리(`Interest|Yield`)만, 일별 환율 카테고리(`Daily Rates`)에서 원·엔·위안만 봅니다.

# %%
display(fred_category(korea_cat, keyword="Interest|Yield"))
daily_fx = cats.loc[cats["name"].eq("Daily Rates"), "category_id"].tolist()
fred_category(daily_fx, keyword="Korea|Japan|China")

# %% [markdown]
# 찾은 시리즈의 정의(단위·주기·최근 갱신)는 `QueryFredSeriesInfo`로 확인합니다.

# %%
info = ds_df('QueryFredSeriesInfo(["DEXKOUS", "IRLTLT01KRM156N", "DCOILBRENTEU"])')
info[["entity_id", "title", "frequency_short", "units_short", "observation_end", "last_updated"]]

# %% [markdown]
# ## 4. 한국은행 지표 — 있지만 2024년 4월에 멈춤
# 통계표 코드를 알면 항목 목록과 **마지막 시점(`end_time`)**을 볼 수 있습니다. 원/달러(`731Y001`)와 증시주변자금(`901Y056`)을 보면
# 둘 다 2024년 3~4월에서 끝납니다. 한국은행 시리즈를 쓸 땐 반드시 이 값을 먼저 보세요.

# %%
def bok_items(stat_code, n=8):
    df = ds_df(f'QueryBankOfKoreaSeriesInfo(stat_codes="{stat_code}")')
    df = df.sort_values("end_time").drop_duplicates("item_code", keep="last").sort_values(["end_time", "item_code"], ascending=[False, True])
    print(f"{df['stat_name_ko'].iloc[0]} — 항목 {len(df)}개, 가장 늦은 마지막 시점: {df['end_time'].max()}")
    return df[["item_code", "item_name_ko", "cycle", "end_time"]].head(n).reset_index(drop=True)

display(bok_items("731Y001", 4))
bok_items("901Y056")

# %% [markdown]
# ## 5. IMF·OECD — 한 시리즈에서 펼치기
# IMF·OECD 시리즈 ID는 `기관:데이터셋.국가.지표` 구조입니다. 시리즈 하나만 알면 같은 국가의 다른 지표,
# 같은 지표의 다른 국가 목록을 펼칠 수 있습니다. 예: 호주 경상수지(IMF BOP)에서 한국(KR) 지표로 바꾸기.
# **주의:** IMF 국제수지(BOP)는 한국 연간 경상수지가 2021년에서 끝나고 분기 시리즈는 비어 있습니다(2026-11-25 확인). IMF·OECD 시리즈도 마지막 날짜를 꼭 보세요.

# %%
imf = ds_df('GetImfIndicatorListOfSameCountry("IMF:BOP.A.AU.BCA_BP6_USD")')
imf.columns = ["entity_id", "지표"]
print(f"IMF BOP 데이터셋, 같은 국가 지표 {len(imf):,}개 중 'Current Account' 앞부분:")
display(imf[imf["지표"].str.startswith("Current Account")].head(5))
kr_ca = ds_df('GetImfSeriesValues(["IMF:BOP.A.KR.BCA_BP6_USD"], date_from=2015-01-01)')
kr_ca.columns = ["entity_id", "date", "경상수지(백만 달러)"]
print("국가 코드만 KR로 바꾼 한국 경상수지(연간). 마지막:", kr_ca["date"].max().date())
kr_ca.tail(4)

# %% [markdown]
# ## 6. "이 지표 있어?" 판정표
# 시세·밸류 지표는 자연어 질의(`삼성전자 지표 기간`)가 **데이터 컬럼**으로 오는지, 아니면 **기업 개요 표**(`ceo` 등 컬럼)로
# 빠지는지로 판정합니다. 기업 개요 표로 빠지면 오류 없이 "없음"이라는 뜻입니다.

# %%
TERMS = ["종가", "시가총액", "PER", "PBR", "배당수익률", "EPS", "BPS",
         "외국인보유비율", "공매도", "신용잔고", "베이시스", "VKOSPI", "투자자예탁금"]
rows = []
for term in TERMS:
    df = ds_df(f"삼성전자 {term} 2026-11-20-{ASOF}")
    ok = "ceo" not in df.columns and len(df) > 0
    last = df.iloc[-1, -1] if ok else None
    rows.append({"지표": term, "자연어로 나옴": "✅" if ok else "❌ (기업 개요 표로 빠짐)",
                 "삼성전자 최근 값": f"{float(last):,.2f}" if ok and pd.notna(last) else ""})
pd.DataFrame(rows)

# %% [markdown]
# ## 7. 정리 — 자주 묻는 지표의 위치
#
# | 지표 | DeepSearch에서 | 상태 |
# |---|---|---|
# | 삼성전자 종목코드 | `KRX:005930` (`GetStockSymbols`) | ✅ |
# | 코스피 종합 지수 | `KRX:KOSPI` (`GetMarketIndexes`) | ✅ |
# | 원/달러 환율 | FRED `DEXKOUS` (일별, 1~3일 늦음) | ✅ — 한국은행 `731Y001.0000001`은 2024-04 중단 |
| 한국 경상수지 | IMF `IMF:BOP.A.KR.BCA_BP6_USD` | ⚠️ 2021년에서 끝남 |
# | PER·PBR·배당수익률 | 자연어 `삼성전자 PER PBR 기간`, 전 종목은 `상장 기업 and PER 날짜` | ✅ (CHECK에선 일별 필드 없음) |
# | 브렌트유 | FRED `DCOILBRENTEU` | ✅ (CHECK에선 범위 밖) |
# | 한국 10년 금리 | FRED `IRLTLT01KRM156N` (OECD, 월평균) | ⚠️ 월별만 |
# | 신용융자 잔고 | 한국은행 `901Y056` S23E (시장 합계, 월) | ⚠️ 2024-03 중단, 종목별 없음 |
# | 투자자예탁금 | 한국은행 `901Y056` S23A | ⚠️ 2024-03 중단 |
# | 베이시스·미결제약정·외국인보유비율·공매도·VKOSPI | 없음 | ❌ (`research/data_gaps`) |
