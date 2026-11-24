# %% [markdown]
# # 5-07 글로벌 금리 — 각국 정책금리·미국 국채 커브·한미 금리차
#
# **질문 예시:** "각국 기준금리랑 한미 금리차 비교해줘", "미국 국채 커브 지금 어때?"
#
# CHECK 원본(`5_데이터조회/07_글로벌금리`)은 KOSCOM economic 코드(USFEDRATED 등)를 썼습니다.
# DeepSearch에서는 **FRED**(`QueryFredSeriesData`)로 같은 그림을 그립니다.
#
# | 항목 | FRED 시리즈 | 주기 |
# |---|---|---|
# | 미국 연방기금 목표 상단 / 실효금리 | `DFEDTARU` / `DFF` | 일 |
# | ECB 예금금리 | `ECBDFR` | 일 |
# | 미국 국채 1개월~30년 | `DGS1MO` … `DGS30` | 일 |
# | 한국·일본·영국 콜금리, 한국 3개월(CD), 각국 10년물 | `IRSTCI01KRM156N` 등 OECD 시리즈 | **월** |
# | 원/달러, 엔/달러, 달러지수 | `DEXKOUS`, `DEXJPUS`, `DTWEXBGS` | 일 |
#
# **각색한 점:** 한국은행 시리즈(기준금리·국고채)는 DeepSearch에서 2024-04에 멈춰 있어 쓰지 않습니다.
# 한국 금리는 OECD 월별 시리즈(전월까지)로 대신합니다. 한은 기준금리 자체는 없고 콜금리(월평균)가 가장 가깝습니다.

# %%
ASOF = "2026-11-24"          # 기준일 (바꿔서 다시 실행하면 됩니다)
START = "2025-01-01"         # 추이 시작일

# %% [markdown]
# ## 1. 정책금리와 단기금리
# 일별(미국·유로)과 월별(한국·일본·영국 콜금리) 시리즈를 함께 받아, 각 시리즈의 **가장 최근 값**을 표로 정리합니다.

# %%
POLICY = {
    "DFEDTARU": "미국 연방기금 목표 상단",
    "DFF": "미국 연방기금 실효금리",
    "ECBDFR": "ECB 예금금리",
    "IRSTCI01KRM156N": "한국 콜금리(월평균)",
    "IR3TIB01KRM156N": "한국 3개월 금리(CD, 월평균)",
    "IRSTCI01JPM156N": "일본 콜금리(월평균)",
    "IRSTCI01GBM156N": "영국 콜금리(월평균)",
}
pol = fred(list(POLICY), START, ASOF)

def latest(df, names):
    rows = []
    for sid, name in names.items():
        s = df[sid].dropna()
        rows.append({"항목": name, "시리즈": sid, "기준일": s.index[-1].date(), "값(%)": round(s.iloc[-1], 3),
                     "1년 전 대비(%p)": round(s.iloc[-1] - s[s.index <= s.index[-1] - pd.DateOffset(years=1)].iloc[-1], 2)
                     if (s.index <= s.index[-1] - pd.DateOffset(years=1)).any() else None})
    return pd.DataFrame(rows)

latest(pol, POLICY)

# %% [markdown]
# ## 2. 한미 금리차
# 한국은 월평균 콜금리, 미국은 같은 달의 연방기금 실효금리 월평균으로 맞춰 비교합니다.
# 10년물도 OECD 월별 시리즈(`IRLTLT01KRM156N` vs `IRLTLT01USM156N`)로 같은 방식입니다.

# %%
lt = fred(["IRLTLT01KRM156N", "IRLTLT01USM156N"], START, ASOF)
m = pd.DataFrame({
    "한국 콜금리": pol["IRSTCI01KRM156N"].dropna(),
    "미국 실효금리(월평균)": pol["DFF"].resample("MS").mean(),
    "한국 10년": lt["IRLTLT01KRM156N"],
    "미국 10년": lt["IRLTLT01USM156N"],
}).dropna()
m["단기 금리차(한-미)"] = m["한국 콜금리"] - m["미국 실효금리(월평균)"]
m["10년 금리차(한-미)"] = m["한국 10년"] - m["미국 10년"]
m.index = m.index.strftime("%Y-%m")
m.round(2).tail(8)

# %% [markdown]
# ## 3. 미국 국채 수익률 곡선
# 최근 거래일과 3개월 전·1년 전 곡선을 겹쳐 그립니다. 장단기 역전 여부는 `10년 − 2년`(`T10Y2Y`)으로 봅니다.

# %%
TENORS = {"DGS1MO": "1M", "DGS3MO": "3M", "DGS6MO": "6M", "DGS1": "1Y", "DGS2": "2Y",
          "DGS5": "5Y", "DGS10": "10Y", "DGS30": "30Y"}
ust = fred(list(TENORS) + ["T10Y2Y"], START, ASOF).dropna(subset=["DGS10"])
last = ust.index[-1]
picks = {"최근 " + str(last.date()): last}
for label, off in (("3개월 전", pd.DateOffset(months=3)), ("1년 전", pd.DateOffset(years=1))):
    d = ust.index[ust.index <= last - off]
    if len(d):
        picks[f"{label} {d[-1].date()}"] = d[-1]
curve = pd.DataFrame({k: ust.loc[v, list(TENORS)].values for k, v in picks.items()}, index=list(TENORS.values()))
print("10년-2년 스프레드(%p):", round(ust["T10Y2Y"].dropna().iloc[-1], 2))
curve.round(2)

# %%
ax = curve.plot(marker="o", figsize=(8, 4), title="미국 국채 수익률 곡선")
ax.set_ylabel("%"); ax.grid(alpha=.3)

# %% [markdown]
# ## 4. 환율과 달러지수

# %%
fx = fred(["DEXKOUS", "DEXJPUS", "DTWEXBGS"], START, ASOF).dropna(how="all")
fx.columns = ["원/달러", "엔/달러", "달러지수(광의)"]
print(fx.dropna().tail(1).round(2).to_string())
axes = fx.plot(subplots=True, figsize=(8, 6), title="환율·달러지수", legend=True)
for a in axes:
    a.grid(alpha=.3)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **미국 시리즈는 1~3 영업일 늦게** 들어옵니다(FRED 공표 일정). 국채 금리는 조회일 기준 직전 금요일까지일 수 있습니다.
# - **한국·일본·영국 금리는 월평균**이라 지난달까지만 있습니다. 한은 기준금리 결정 당일 반영이 필요하면 한국은행 ECOS를 직접 써야 합니다.
# - **국고채 만기별 곡선은 DeepSearch로 만들 수 없습니다**(채권 함수 미제공, 한국은행 시리즈 2024-04 중단). 근거: `research/data_gaps`.
