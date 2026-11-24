# %% [markdown]
# # 5-01 아무 데이터나 조회 — 시세·지수·순위·밸류에이션·재무를 표와 CSV로
#
# **질문 예시:** "삼성전자 최근 한 달 일별 시세랑 거래량 뽑아줘", "코스피 거래대금 상위 20종목", "반도체 3사 종가 나란히",
# "삼성전자 PER·PBR 추이", "삼성전자 최근 분기 실적", "CSV로 저장해줘"
#
# CHECK 원본(`5_데이터조회/01_아무데이터나조회`)과 같은 "그냥 데이터 좀 줘" 시나리오입니다. DeepSearch로 되는 것과 안 되는 것은 아래와 같습니다.
#
# | 분류 | DeepSearch | 함수 |
# |---|---|---|
# | 종목 일별 시세·거래량·시가총액 | ✅ | `GetStockPrices` |
# | 여러 종목 한 번에 | ✅ | `GetStockPrices([...])` |
# | 지수(코스피·코스닥 계열 11종) | ✅ | `GetMarketIndexes` |
# | 거래대금·등락률·시총 순위 | ✅ 전 종목 하루치를 받아 정렬 | `GetStockPrices` (종목 생략) |
# | PER·PBR·배당수익률 | ✅ CHECK에선 일별 필드가 없던 항목 | 자연어 질의 `삼성전자 PER PBR 기간` |
# | 분기·연간 재무 | ✅ | `GetFinancialStatements` |
# | 환율·미국 금리 | ✅ FRED | `QueryFredSeriesData` |
# | **외국인 보유율·투자자 수급·선물·ETF NAV·국고채** | ❌ 없음 | `research/data_gaps` |

# %%
ASOF = "2026-11-24"
START = "2026-10-24"   # 약 1개월

# %% [markdown]
# ## 1. 한 종목 일별 시세
# `KRX:종목코드`로 지정합니다. 이름만 알면 5-02 노트북처럼 `universe()`에서 코드를 찾습니다.

# %%
px = stock_prices("KRX:005930", START, ASOF)
px = px.assign(등락률=(px["change_rate"] * 100).round(2))[
    ["date", "open", "high", "low", "close", "등락률", "volume", "value", "market_cap"]]
px.columns = ["일자", "시가", "고가", "저가", "종가", "등락률(%)", "거래량", "거래대금(원)", "시가총액(원)"]
print(PRICE_NOTICE)
px.tail(10)

# %% [markdown]
# ## 2. 여러 종목 종가 나란히
# 종목 목록을 한 번에 넣으면 한 번의 호출로 옵니다.

# %%
names = {"KRX:005930": "삼성전자", "KRX:000660": "SK하이닉스", "KRX:042700": "한미반도체"}
multi = stock_prices(list(names), START, ASOF, columns=["close"])
wide = multi.pivot(index="date", columns="symbol", values="close")[list(names)].rename(columns=names)
display(wide.tail(5))
ax = (wide / wide.iloc[0] * 100).plot(figsize=(8, 3.5), title=f"종가 지수화 ({wide.index[0].date()} = 100)")
ax.grid(alpha=.3)

# %% [markdown]
# ## 3. 지수
# 지수 `change_rate`는 퍼센트, `value`는 백만원 단위입니다.

# %%
ix = index_prices(START, ASOF)
kospi = ix[ix["symbol"] == "KRX:KOSPI"][["date", "close", "change", "change_rate", "value"]].copy()
kospi["거래대금"] = (kospi["value"] * 1e6).map(krw)
kospi.drop(columns="value").tail(5)

# %% [markdown]
# ## 4. 순위 — 코스피 거래대금 상위 20
# 종목을 지정하지 않으면 **전 종목 하루치**가 한 번에 옵니다. ETF가 거래대금 상위를 차지하므로 기본은 일반 종목만 보고,
# ETF 포함 순위도 함께 보여 줍니다.

# %%
allx = all_stocks(ASOF, common_only=False)
allx = allx[allx["date"] == allx["date"].max()]
def rank(df, n=20):
    out = df.nlargest(n, "value")
    return pd.DataFrame({"종목": out["name"], "종가": out["close"].map("{:,.0f}".format),
                         "등락률(%)": (out["change_rate"] * 100).round(2), "거래대금": out["value"].map(krw)}).reset_index(drop=True)
kospi_all = allx[allx["market"] == "KOSPI"]
print("기준일:", allx["date"].max().date())
print("[일반 종목만 (ETF·ETN 제외)]"); display(rank(kospi_all[kospi_all["company_type_l1"] != "8"]))
print("[ETF 포함 상위 10]"); display(rank(kospi_all, 10))

# %% [markdown]
# ## 5. PER·PBR·배당수익률
# 자연어 질의(`종목 지표 기간`)로 받습니다. 결과 컬럼 이름에 질의 문구가 붙어 나오므로 정리해서 씁니다.
# - PER = 시가총액 ÷ 당기순이익, PBR = 시가총액 ÷ 자본(지배지분). FY N 값이 N+1년 첫 거래일부터 쓰입니다(`research/pbr_bps`).
# - 배당수익률 단위는 %입니다.

# %%
def nl(query):
    df = ds_df(query)
    df.columns = [c.split(" ")[0] if " 20" in c else c for c in df.columns]   # "PER 2026-11-18-…" → "PER"
    return df

val = nl(f"삼성전자 PER PBR {START}-{ASOF}")
display(val.tail(5))
peer = nl(f"삼성전자 SK하이닉스 한미반도체 PER PBR 배당수익률 {ASOF}-{ASOF}")
peer

# %% [markdown]
# 전 종목 PER도 한 번에 받을 수 있습니다(`상장 기업 and PER 날짜`, 4,000여 행). 아래는 시가총액 1조 원 이상 보통주 중 PER이 낮은 종목입니다
# (적자 기업은 PER이 음수라 뺐고, 우선주는 뺐습니다). PER이 아주 낮으면 일회성 이익 때문일 수 있으니 실적을 함께 보세요.

# %%
per_all = nl(f"상장 기업 and PER {ASOF}")
per_all = per_all.merge(allx[["symbol", "market", "market_cap", "company_type_l1"]], on="symbol")
low = per_all[(per_all["company_type_l1"] == "1") & per_all["symbol"].str.endswith("0") & (per_all["market_cap"] >= 1e12) & (per_all["PER"] > 0)].nsmallest(10, "PER")
low.assign(시가총액=low["market_cap"].map(krw))[["entity_name", "market", "PER", "시가총액"]].reset_index(drop=True)

# %% [markdown]
# ## 6. 재무 — 분기 실적
# `GetFinancialStatements`의 계정 이름은 매출액이 `수익`, 영업이익이 `영업이익(손실)`, 지배주주 순이익이 `당기순이익지배기업지분`입니다.
# `is_accumulated=False`(기본)이면 분기 3개월 값입니다.

# %%
fs = ds_df(f'GetFinancialStatements(삼성전자, report_type="IFRS", consolidated=True, is_annual=False, '
           f'report_ids="Income", date_from=2025-01-01, date_to={ASOF})')
ACC = {"수익": "매출액", "영업이익(손실)": "영업이익", "당기순이익지배기업지분": "지배순이익"}
q = fs[fs["name_ko"].isin(ACC)].pivot_table(index="date", columns="name_ko", values="value").rename(columns=ACC)
q = (q[list(ACC.values())] / 1e12).round(2)
q["영업이익률(%)"] = (q["영업이익"] / q["매출액"] * 100).round(1)
q.index = q.index.strftime("%Y-%m")
print("단위: 조원 (연결, 분기 3개월)")
q

# %% [markdown]
# ## 7. CSV로 저장
# Colab에서는 저장한 파일을 바로 내려받습니다. 로컬에서는 현재 폴더에 저장됩니다.

# %%
out = "samsung_daily.csv"
px.to_csv(out, index=False, encoding="utf-8-sig")   # 엑셀에서 한글이 깨지지 않게 utf-8-sig
print("저장:", out, f"({len(px)}행)")
if IN_COLAB:
    from google.colab import files
    files.download(out)
else:
    import os
    os.remove(out)   # 로컬 빌드에서는 남기지 않음

# %% [markdown]
# ## 없는 데이터
# 외국인 보유율, 투자자별 수급, 공매도·대차·신용, 지수선물, ETF NAV, 국고채 금리는 DeepSearch에 없습니다.
# 자연어로 물으면 오류 없이 **기업 개요 표**가 돌아오니, 결과 컬럼을 꼭 확인하세요(근거: `research/data_gaps`).

# %%
chk = ds_df(f"삼성전자 외국인보유비율 {START}-{ASOF}")
print("'외국인보유비율' 질의 결과 컬럼:", list(chk.columns)[:6], "… →", "기업 개요 표(데이터 없음)" if "ceo" in chk.columns else "데이터 있음")
