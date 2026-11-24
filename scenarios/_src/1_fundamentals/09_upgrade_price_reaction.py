# %% [markdown]
# # 1-09 상향 이벤트 주가반응 — 전망이 오를 때 주가는 따라 올랐나
#
# **질문 예시:** "최근 상향된 종목들, 과거에 상향됐을 때 주가 반응 어땠어?", "SK하이닉스 이익 전망 오를 때마다 주가 어떻게 움직였어?"
#
# CHECK 원본(`1_기업펀더멘털/09_상향이벤트주가반응`)과 같은 흐름입니다.
# 1. 시가총액 상위 종목에서 **최근 1개월 영업이익 전망이 오른 종목**을 고르고([1-08](08_revision_screener.ipynb)과 같은 계산)
# 2. 그 종목들의 **과거 2년 동안 컨센서스가 하루에 3% 이상 오른 날**(상향 이벤트)을 찾아
# 3. 이벤트 뒤 **+1·+5·+20거래일 수익률과 승률**, 코스피 대비 초과수익을 봅니다.
#
# DeepSearch에서 달라진 점: 컨센서스 이력을 증권사별 추정치(`SearchFirmFundamentalsForecasts`)로 **직접 재구성**합니다. 종목별로 한 번씩 부릅니다.

# %%
ASOF = "2026-11-24"
UNIVERSE_TOP = 40      # 시가총액 상위 몇 종목에서 고를지 (종목당 1회 호출)
PICK = 8               # 최근 상향 상위 몇 종목을 백테스트할지
HIST_YEARS = 2         # 과거 이벤트를 찾을 기간
JUMP = 0.03            # 하루 컨센서스 상승률이 이 이상이면 상향 이벤트
GAP = 20               # 이벤트 사이 최소 간격(거래일) — 같은 재료의 연속 상향을 하나로
HORIZONS = (1, 5, 20)
STALE, LOOK = 90, 30
print(PRICE_NOTICE)

# %% [markdown]
# ## 1. 추정치 받기 (종목별 1회, 과거 2년 + 90일)

# %%
from datetime import timedelta
asof = pd.Timestamp(ASOF)
hist_start = (asof - pd.DateOffset(years=HIST_YEARS) - timedelta(days=STALE)).date()
snap = all_stocks(ASOF)
uni = snap.sort_values("market_cap", ascending=False).head(UNIVERSE_TOP)[["symbol", "name"]]
frames = []
for sym in uni["symbol"]:
    f = ds_df(f'SearchFirmFundamentalsForecasts({sym}, last_only=False, accounting_types="K", '
              f'date_from={hist_start}, date_to={ASOF})')
    if f.empty or not f.notna().any().any():
        continue
    f = f.dropna(axis=1, how="all")
    f["symbol"] = sym
    v = f["csd_operating_income"] if "csd_operating_income" in f else pd.Series(index=f.index, dtype=float)
    f["value"] = v.where(v.notna(), f.get("operating_income"))
    frames.append(f.dropna(subset=["value"])[["symbol", "date", "inst_code", "forecast_date", "value"]])
fc = pd.concat(frames, ignore_index=True)
fc["value"] = fc["value"].astype(float)
print(f"{fc['symbol'].nunique()}종목, 추정치 {len(fc):,}행, 기간 {fc['date'].min().date()} ~ {fc['date'].max().date()}")

# %% [markdown]
# ## 2. 컨센서스 함수와 최근 리비전
# 1-08과 같습니다. 시점 t의 컨센서스 = t 이전 90일 안 증권사별 최신 추정치의 평균, 중앙값의 1/3~3배 밖 입력 오류는 제외.

# %%
def consensus(df, t):
    d = df[(df["date"] <= t) & (df["date"] > t - timedelta(days=STALE))]
    last = d.sort_values("date").groupby("inst_code").tail(1)["value"]
    med = last.median()
    if len(last) >= 3 and med > 0:
        last = last[(last >= med / 3) & (last <= med * 3)]
    return (last.mean(), len(last)) if len(last) else (float("nan"), 0)

FY_NEXT = f"{asof.year + 1}12"
recent = []
for sym, g in fc[fc["forecast_date"] == FY_NEXT].groupby("symbol"):
    now, n1 = consensus(g, asof)
    prev, n0 = consensus(g, asof - timedelta(days=LOOK))
    if n1 >= 2 and n0 >= 2 and prev > 0:
        recent.append({"symbol": sym, "최근 리비전": now / prev - 1, "증권사": n1})
recent = pd.DataFrame(recent).merge(uni, on="symbol").sort_values("최근 리비전", ascending=False)
picks = recent[recent["최근 리비전"] > 0].head(PICK)
print(f"■ {FY_NEXT[:4]}년 영업이익 1개월 리비전 상향 상위 {len(picks)}종목")
picks.assign(**{"최근 리비전": (picks["최근 리비전"] * 100).round(1)})[["name", "최근 리비전", "증권사"]]

# %% [markdown]
# ## 3. 과거 상향 이벤트 찾기
# 거래일마다 **그해 결산(FY = 그 날짜의 연도)** 컨센서스를 계산하고, 전 거래일보다 3% 이상 오른 날을 이벤트로 잡습니다.
# 같은 연도끼리만 비교하므로 연초에 대상 연도가 바뀌는 날은 이벤트가 되지 않습니다.

# %%
prices = stock_prices(list(picks["symbol"]), hist_start, ASOF, columns=["close"])
px = prices.pivot_table(index="date", columns="symbol", values="close").sort_index()
kospi = ds_df(f"GetMarketIndexes(KRX:KOSPI, date_from={hist_start}, date_to={ASOF})").set_index("date")["close"]
days = px.index[px.index >= asof - pd.DateOffset(years=HIST_YEARS)]

events = []
for sym in picks["symbol"]:
    g = fc[fc["symbol"] == sym]
    prev_val, prev_fy, last_pos = None, None, -10 ** 9
    for pos, t in enumerate(days):
        fy = f"{t.year}12"
        val, n = consensus(g[g["forecast_date"] == fy], t)
        if prev_fy == fy and prev_val and prev_val > 0 and n >= 2 and val / prev_val - 1 >= JUMP and pos - last_pos >= GAP:
            events.append({"symbol": sym, "date": t, "FY": fy, "상향폭": val / prev_val - 1, "증권사": n})
            last_pos = pos
        prev_val, prev_fy = val, fy
ev = pd.DataFrame(events).merge(uni, on="symbol")
print(f"이벤트 {len(ev)}건")
ev.groupby("name").size().rename("이벤트 수").to_frame().T

# %% [markdown]
# ## 4. 이벤트 뒤 수익률
# 이벤트일 종가 → +N거래일 종가. 괄호 안은 같은 구간 코스피 대비 초과수익 평균입니다. 아직 N일이 지나지 않은 이벤트는 그 지평선에서 빠집니다.

# %%
k = kospi.reindex(px.index).ffill()
rows = []
for _, e in ev.iterrows():
    s = px[e["symbol"]].dropna()
    i = s.index.get_loc(e["date"])
    r = {"name": e["name"], "date": e["date"].date(), "상향폭": e["상향폭"]}
    for h in HORIZONS:
        if i + h < len(s):
            r[f"+{h}D"] = s.iloc[i + h] / s.iloc[i] - 1
            r[f"+{h}D 초과"] = r[f"+{h}D"] - (k.loc[s.index[i + h]] / k.loc[s.index[i]] - 1)
    rows.append(r)
res = pd.DataFrame(rows)

def summary(g):
    out = {}
    for h in HORIZONS:
        c = g[f"+{h}D"].dropna()
        x = g[f"+{h}D 초과"].dropna()
        out[f"+{h}D"] = f"{c.mean() * 100:+.1f}% ({len(c)}건, 승률 {(c > 0).mean() * 100:.0f}%, 초과 {x.mean() * 100:+.1f}%)" if len(c) else "-"
    return pd.Series(out)

tbl = res.groupby("name").apply(summary, include_groups=False)
tbl = picks.set_index("name")[["최근 리비전"]].join(tbl)
tbl["최근 리비전"] = (tbl["최근 리비전"] * 100).map(lambda x: f"{x:+.1f}%")
tbl

# %% [markdown]
# ## 5. 한 종목 이벤트 상세
# 표에서 궁금한 종목의 이벤트를 날짜별로 봅니다.

# %%
DETAIL = picks["name"].iloc[0]
d = res[res["name"] == DETAIL].copy()
for c in ["상향폭"] + [f"+{h}D" for h in HORIZONS]:
    d[c] = (d[c] * 100).round(1)
d[["date", "상향폭"] + [f"+{h}D" for h in HORIZONS]]

# %% [markdown]
# ## 결과 읽는 법과 한계
# - `평균(건수, 승률, 초과)` 순입니다. **건수가 6건 이하면 통계로 보기 어렵습니다.**
# - 이 기간(2025~2026)은 반도체 등 일부 업종이 크게 오른 시기라 절대수익보다 **코스피 대비 초과수익**을 같이 보세요.
# - 컨센서스 이력은 DeepSearch가 받는 증권사(대형주 4~7곳)로 재구성한 것이라, 증권사 한 곳의 추정 변경이 3% 이벤트를 만들 수 있습니다.
# - 이벤트일 종가 기준이라 장중에 나온 리포트는 이벤트일 수익률 일부를 놓칠 수 있습니다.
