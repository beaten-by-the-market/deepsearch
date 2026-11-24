# %% [markdown]
# # 1-08 추정 상향 스크리너 — 요즘 실적 전망이 오르는 종목 찾기
#
# **질문 예시:** "최근 예측치 상향된 종목 뭐야?", "요즘 영업이익 전망 내려가는 종목은?"
#
# CHECK 원본(`1_기업펀더멘털/08_추정상향스크리너`)은 컨센서스 스냅샷을 날짜별로 받아 시가총액 상위 60종목의 1개월 리비전을 순위로 냈습니다.
# DeepSearch에는 시장 전체 리비전 함수(`GetFundamentalsConsensusChange`)가 이 구독에서 막혀 있어서, **종목별로 증권사 추정치를 받아 직접 계산**합니다.
#
# | 단계 | DeepSearch |
# |---|---|
# | 유니버스 | 전 종목 시세 1회 호출(`GetStockPrices`)로 시가총액 상위 N |
# | 증권사별 추정치 | `SearchFirmFundamentalsForecasts` — **종목별 1회씩** (목록을 넣으면 첫 종목만 옵니다) |
# | 컨센서스 | 시점 t에서 "90일 안에 낸 증권사별 최신 추정치"의 평균 (직접 계산) |
# | 리비전 | 컨센서스(기준일) ÷ 컨센서스(30일 전) − 1 |
#
# 시장 전체 **목표주가** 변화는 한 번 호출로 나옵니다 → [1-11 목표주가·투자의견](11_target_price_opinion.ipynb).

# %%
ASOF = "2026-11-24"
UNIVERSE_TOP = 60            # 시가총액 상위 몇 종목을 볼지 (종목당 1회 호출)
METRIC = "operating_income"  # operating_income, net_income, revenue, eps 중 하나
FY = ["202612", "202712"]    # 결산연월. 11월이면 올해(2026)는 거의 확정이라 내년(2027) 리비전을 주로 봅니다
SORT_FY = "202712"
LOOK = 30                    # 리비전 비교 기간(일)
STALE = 90                   # 이보다 오래된 증권사 추정치는 컨센서스에서 뺌(일)
print(PRICE_NOTICE)

# %% [markdown]
# ## 1. 유니버스: 시가총액 상위 종목

# %%
snap = all_stocks(ASOF)
uni = snap.sort_values("market_cap", ascending=False).head(UNIVERSE_TOP)[["symbol", "name", "market", "industry_name", "market_cap", "close"]]
print(f"기준 {snap['date'].max().date()} — 시가총액 상위 {len(uni)}종목 (일반법인 보통주)")
uni.head(5).assign(market_cap=uni["market_cap"].head(5).map(krw))

# %% [markdown]
# ## 2. 증권사별 추정치 받기
# 기준일 30일 전 시점의 컨센서스도 계산해야 하므로 `LOOK + STALE`일 전부터 받습니다. 종목마다 한 번씩 부릅니다(약 0.5초/종목).

# %%
from datetime import timedelta
asof = pd.Timestamp(ASOF)
start = (asof - timedelta(days=LOOK + STALE)).date()
frames, failed = [], []  # noqa
for sym in uni["symbol"]:
    try:
        f = ds_df(f'SearchFirmFundamentalsForecasts({sym}, last_only=False, accounting_types="K", '
                  f'date_from={start}, date_to={ASOF})')
    except DSError as e:
        failed.append((sym, str(e)[:80]))
        continue
    if not f.empty and f.notna().any().any():
        f["symbol"] = sym
        frames.append(f.dropna(axis=1, how="all"))
fc = pd.concat(frames, ignore_index=True)
# 연결 추정치(csd_)가 없으면 별도 추정치를 씁니다 (예: 삼성바이오로직스는 csd_ 영업이익이 비어 있음)
fc["value"] = fc[f"csd_{METRIC}"].where(fc[f"csd_{METRIC}"].notna(), fc[METRIC]) if f"csd_{METRIC}" in fc else fc[METRIC]
fc = fc[fc["forecast_date"].isin(FY)].dropna(subset=["value"])
print(f"추정치 {len(fc):,}행, 종목 {fc['symbol'].nunique()}개, 증권사 {fc['inst_code'].nunique()}곳, 실패 {len(failed)}")

# %% [markdown]
# ## 3. 컨센서스와 리비전 계산
# - **컨센서스(t)** = t 이전 `STALE`일 안에 낸 증권사별 최신 추정치의 평균, **증권사 수**도 함께
# - **리비전** = 컨센서스(기준일) ÷ 컨센서스(30일 전) − 1. 두 시점 모두 증권사 2곳 이상일 때만 계산
# - **마지막 상향일**: 어떤 증권사가 같은 연도 추정치를 직전보다 올린 가장 최근 날짜
# - **⚠**: 30일 전 컨센서스가 0 이하이거나 변화가 ±30%를 넘음(적자·흑자 전환 근처라 %가 과장될 수 있음)
# - **이상치 제거**: 증권사 추정치에는 입력 오류가 섞여 있습니다(예: 카카오 2027 영업이익을 한 증권사가 12.2조로 10배 입력,
#   대한항공은 한 증권사 영업이익 칸에 매출 20.9조). 같은 시점 증권사들의 **중앙값의 1/3~3배를 벗어난 값은 빼고** 평균을 냅니다.

# %%
def clean(values):
    """중앙값의 1/3~3배 밖 값 제거 (중앙값이 양수이고 3곳 이상일 때만)."""
    med = values.median()
    if len(values) >= 3 and med > 0:
        return values[(values >= med / 3) & (values <= med * 3)]
    return values

def consensus(df, t):
    d = df[(df["date"] <= t) & (df["date"] > t - timedelta(days=STALE))]
    last = d.sort_values("date").groupby("inst_code").tail(1)["value"]
    kept = clean(last)
    return kept.mean(), len(kept), len(last) - len(kept)

def last_change(df, up=True):
    d = df.sort_values("date").copy()
    d["prev"] = d.groupby("inst_code")["value"].shift()
    hit = d[(d["value"] > d["prev"]) if up else (d["value"] < d["prev"])]
    return hit["date"].max() if len(hit) else pd.NaT

rows = []
for (sym, fy), g in fc.groupby(["symbol", "forecast_date"]):
    now, n_now, x_now = consensus(g, asof)
    prev, n_prev, x_prev = consensus(g, asof - timedelta(days=LOOK))
    rev = now / prev - 1 if n_now >= 2 and n_prev >= 2 and prev else None
    rows.append({"symbol": sym, "FY": fy, "컨센서스": now, "증권사": n_now, "30일전": prev, "30일전 증권사": n_prev,
                 "리비전": rev, "이상치 제외": x_now + x_prev, "마지막 상향일": last_change(g, True), "마지막 하향일": last_change(g, False),
                 "⚠": "⚠" if rev is not None and (prev <= 0 or abs(rev) > 0.3) else ""})
rv = pd.DataFrame(rows).merge(uni, on="symbol")
wide = rv.pivot_table(index="symbol", columns="FY", values="리비전")
print("리비전 계산 가능 종목:", {fy: int(wide[fy].notna().sum()) for fy in FY if fy in wide})
print("이상치로 뺀 추정치가 있는 종목:", ", ".join(rv.loc[rv["이상치 제외"] > 0, "name"].unique()))

# %% [markdown]
# ## 4. 상향 상위 / 하향 상위 (내년 영업이익 기준)

# %%
def table(df):
    out = df[["name", "industry_name", "리비전", "⚠", "컨센서스", "증권사", "이상치 제외", "마지막 상향일", "마지막 하향일"]].copy()
    out["리비전"] = (out["리비전"] * 100).map(lambda x: f"{x:+.1f}%")
    out["컨센서스"] = out["컨센서스"].map(krw)
    for c in ("마지막 상향일", "마지막 하향일"):
        out[c] = out[c].dt.date
        out[c + " 경과일"] = (asof - df[c]).dt.days.astype("Int64")
    return out.rename(columns={"name": "종목", "industry_name": "업종"})

main = rv[(rv["FY"] == SORT_FY) & rv["리비전"].notna()].sort_values("리비전", ascending=False)
print(f"■ {SORT_FY[:4]}년 {METRIC} 1개월 리비전 상향 상위 (기준 {ASOF})")
display(table(main.head(15)))
print(f"■ 하향 상위")
display(table(main.sort_values("리비전").head(10)))

# %% [markdown]
# ## 5. 올해 vs 내년 리비전 비교
# 두 해 모두 오르면 "실적 눈높이가 전반적으로 올라가는 중", 올해만 오르면 이미 나온 분기 실적 반영일 가능성이 큽니다.

# %%
both = wide.dropna().merge(uni[["symbol", "name"]], left_index=True, right_on="symbol").set_index("name")[FY]
ax = (both * 100).plot.scatter(x=FY[0], y=FY[1], figsize=(6, 5), title="1개월 리비전(%) — 올해 vs 내년")
for n, r in (both * 100).iterrows():
    if abs(r[FY[0]]) > 5 or abs(r[FY[1]]) > 5:
        ax.annotate(n, (r[FY[0]], r[FY[1]]), fontsize=8)
ax.axhline(0, color="gray", lw=.5); ax.axvline(0, color="gray", lw=.5); ax.grid(alpha=.3)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 리비전 %는 **같은 증권사 집합의 평균이 어떻게 바뀌었나**입니다. 30일 사이 새 증권사가 들어오거나 빠지면 그 효과도 섞입니다(증권사 수 열 참고).
# - 증권사 추정치에는 단위·필드 입력 오류가 섞여 있어 중앙값 기준으로 걸렀습니다. 증권사가 2곳뿐이면 거를 수 없으니 `증권사` 열을 같이 보세요.
# - DeepSearch가 받는 증권사는 대형주도 4~7곳이라 시장 전체 컨센서스보다 표본이 작습니다. 증권사 2곳 미만 종목은 뺐습니다.
# - `⚠` 종목은 이익이 0 근처라 %가 크게 튈 수 있습니다. 절대 금액(컨센서스 열)을 같이 보세요.
# - 유니버스를 늘리면 종목당 1회씩 호출이 늘어납니다(100종목 ≈ 1분).
