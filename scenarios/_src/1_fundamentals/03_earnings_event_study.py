# %% [markdown]
# # 1-03 실적발표 이벤트 스터디 — 발표 전후 주가 반응과 서프라이즈
#
# **질문 예시:** "삼성전자 실적발표날 주가 어떻게 움직였어?", "실적 나오기 전에 이미 올랐던 거야?"
#
# CHECK 원본(`1_기업펀더멘털/03_실적발표이벤트스터디`)은 발표일·주가·**외국인/기관 수급**을 함께 봤습니다.
# DeepSearch에는 투자자별 수급이 없어서 그 부분은 빼고, 대신 다음을 넣었습니다.
#
# | 항목 | DeepSearch |
# |---|---|
# | 발표일 | 거래소 공시 `영업(잠정)실적(공정공시)`의 접수 시각 (`DocumentSearch`, 공시) |
# | 주가 반응 | `GetStockPrices` + 코스피 지수(`GetMarketIndexes`)로 **시장 대비 초과수익** |
# | 거래량 반응 | 발표일 거래량 ÷ 직전 20거래일 평균 |
# | 서프라이즈 | 분기 실제 영업이익(`GetFinancialStatements`) vs 발표 직전 90일 증권사 추정 평균(`SearchFirmFundamentalsForecasts`) |
# | 외국인·기관 수급 | **없음** (DeepSearch 미제공, `research/data_gaps`) |

# %%
ASOF = "2026-11-24"            # 기준일
STOCK = "KRX:005930"           # 종목 (삼성전자)
NAME = "삼성전자"
LOOKBACK_START = "2025-11-25"  # 발표일을 찾을 기간 시작 (공시 검색은 1년 이내)
WINDOW = 10                    # 발표 전후 거래일 수
print(PRICE_NOTICE)

# %% [markdown]
# ## 1. 실적 발표일 찾기
# 삼성전자는 분기마다 **잠정실적(분기 첫 주)**과 **확정 실적 설명(분기 말)** 두 번 `영업(잠정)실적` 공시를 냅니다.
# `[기재정정]`은 빼고, 장 마감(15:30) 뒤 공시는 다음 거래일을 반응 첫날(D0)로 잡습니다.

# %%
total, ann = doc_search("company", ["disclosure"], f"securities.name:{NAME} and title:잠정",
                        LOOKBACK_START, ASOF, count=50)
ann = ann[ann["title"].str.contains("영업\\(잠정\\)실적") & ~ann["title"].str.contains("정정")]
ann = ann[ann["publisher"] == NAME].sort_values("created_at").reset_index(drop=True)
ann["구분"] = ann.groupby(ann["created_at"].dt.to_period("Q")).cumcount().map({0: "잠정(1차)", 1: "확정 설명(2차)"})
ann[["created_at", "구분", "title"]]

# %% [markdown]
# ## 2. 발표 전후 주가·거래량 반응
# - **발표 전 수익률**: D−11 종가 → D−1 종가 (선반영 여부)
# - **발표일 수익률**: D−1 종가 → D0 종가
# - **발표 후 수익률**: D0 종가 → D+10 종가
# - 괄호 안은 같은 구간 코스피 수익률을 뺀 **초과수익**입니다.

# %%
px = stock_prices(STOCK, "2025-10-01", ASOF, columns=["close", "volume", "change_rate"]).set_index("date")
# 지수는 꼭 지정해서 부릅니다. 지수를 생략하면 약 1,290행(11개 지수 × 117거래일)까지만 와서 앞 기간이 잘립니다.
kospi = ds_df(f"GetMarketIndexes(KRX:KOSPI, date_from=2025-10-01, date_to={ASOF})").set_index("date")["close"]
days = px.index

def d0_of(ts):
    """공시 시각 → 반응 첫 거래일 위치. 15:30 이후 공시는 다음 거래일."""
    day = ts.normalize() + (pd.Timedelta(days=1) if ts.hour * 60 + ts.minute >= 15 * 60 + 30 else pd.Timedelta(0))
    pos = days.searchsorted(day)
    return pos if pos < len(days) else None

def ret(series, a, b):
    return series.iloc[b] / series.iloc[a] - 1

rows = []
for _, a in ann.iterrows():
    p = d0_of(a["created_at"])
    if p is None or p - WINDOW - 1 < 0:
        continue
    k = kospi.reindex(days).ffill()
    post_end = min(p + WINDOW, len(days) - 1)
    r = {
        "공시 시각": a["created_at"], "구분": a["구분"], "D0": days[p].date(),
        "발표 전": ret(px["close"], p - WINDOW - 1, p - 1),
        "발표일": ret(px["close"], p - 1, p),
        "발표 후": ret(px["close"], p, post_end),
        "발표 후 거래일수": post_end - p,
    }
    for col, (s, e) in {"발표 전": (p - WINDOW - 1, p - 1), "발표일": (p - 1, p), "발표 후": (p, post_end)}.items():
        r[col + " 초과"] = r[col] - ret(k, s, e)
    r["거래량 배수"] = px["volume"].iloc[p] / px["volume"].iloc[p - 20:p].mean()
    rows.append(r)
ev = pd.DataFrame(rows)

def pct(x):
    return f"{x * 100:+.1f}%"

show = ev[["D0", "구분"]].copy()
for c in ("발표 전", "발표일", "발표 후"):
    show[c + "(초과)"] = [f"{pct(a)} ({pct(b)})" for a, b in zip(ev[c], ev[c + " 초과"])]
show["거래량 배수"] = ev["거래량 배수"].round(2)
show

# %% [markdown]
# ## 3. 어닝 서프라이즈
# 분기 실제 영업이익(연결, 3개월)과 **발표 직전 90일 안에 낸 증권사별 최신 추정치의 평균**을 비교합니다.
# 추정치는 증권사가 낸 날짜별로 쌓여 있어서, 발표 전에 낸 것만 골라 "발표 직전 컨센서스"를 직접 계산할 수 있습니다.
# 결산월 코드: F=3월, X=6월, Y=9월, Z=12월 분기.

# %%
fs = ds_df(f'GetFinancialStatements({STOCK}, report_type="IFRS", consolidated=True, is_annual=False, '
           f'is_accumulated=False, report_ids="Income", date_from=2025-01-01, date_to={ASOF})')
op = fs[fs["name_ko"] == "영업이익(손실)"].set_index("date")["value"]
fc = ds_df(f'SearchFirmFundamentalsForecasts({STOCK}, last_only=False, date_from=2025-07-01, date_to={ASOF})')
fc = fc[fc["accounting_type"].isin(["F", "X", "Y", "Z"])].copy()

first = ann[ann["구분"] == "잠정(1차)"]
srows = []
for _, a in first.iterrows():
    q_end = (a["created_at"] - pd.offsets.QuarterEnd(1)).normalize()      # 직전 분기 말
    target = q_end.strftime("%Y%m")
    cut = a["created_at"].normalize()
    f = fc[(fc["forecast_date"] == target) & (fc["date"] < cut) & (fc["date"] >= cut - pd.Timedelta(days=90))]
    f = f.dropna(subset=["csd_operating_income"]).sort_values("date").groupby("inst_code").tail(1)
    actual = op.get(q_end)
    cons = f["csd_operating_income"].mean() if len(f) else None
    srows.append({"분기": q_end.strftime("%Y-%m"), "잠정 발표": a["created_at"].date(),
                  "실제 영업이익": krw(actual), "발표 전 컨센서스": krw(cons), "증권사 수": len(f),
                  "서프라이즈": pct(actual / cons - 1) if actual and cons else "-"})
pd.DataFrame(srows)

# %% [markdown]
# ## 4. 발표일 전후 평균 경로
# 모든 발표를 D0 기준으로 겹쳐 시장 대비 누적 초과수익의 평균을 그립니다.

# %%
k = kospi.reindex(days).ffill()
ar = (px["close"].pct_change() - k.pct_change())
paths = {}
for _, a in ann.iterrows():
    p = d0_of(a["created_at"])
    if p is None or p - WINDOW < 1 or p + WINDOW >= len(days):
        continue
    seg = ar.iloc[p - WINDOW:p + WINDOW + 1].values
    paths[str(days[p].date())] = (pd.Series(seg).cumsum() - seg[:WINDOW].sum()) * 100  # D-1 종가 기준 0
car = pd.DataFrame(paths)
car.index = range(-WINDOW, WINDOW + 1)
ax = car.mean(axis=1).plot(figsize=(8, 4), marker="o", title=f"{NAME} 실적 발표 전후 평균 누적 초과수익 (n={car.shape[1]}, %)")
ax.axvline(0, color="gray", ls="--"); ax.axhline(0, color="gray", lw=.5); ax.set_xlabel("발표 후 거래일 (D0=반응 첫날)"); ax.grid(alpha=.3)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **발표 전 상승 + 발표 후 하락**이면 선반영(sell-the-news), **발표일 초과수익이 크면** 서프라이즈에 반응한 것입니다.
# - 서프라이즈는 확정 분기 실적(재무제표) 기준입니다. 잠정 발표 수치와 조금 다를 수 있습니다.
# - 컨센서스 표본은 DeepSearch가 받는 증권사(분기 추정은 대개 5~7곳)라 시장 전체 컨센서스보다 얇습니다.
# - **외국인·기관 수급은 DeepSearch에 없어** 원본의 "누가 사고팔았나"는 재현할 수 없습니다.
# - 공시 검색은 한 번에 1년까지라 그보다 긴 기간은 나눠서 찾아야 합니다.
