# %% [markdown]
# # 1-12 기업집단 대시보드 — 그룹별 시가총액과 수익률 (신규)
#
# **질문 예시:** "삼성·SK·현대차 그룹 시가총액이랑 올해 수익률 비교해줘", "삼성그룹 계열 상장사 중 뭐가 제일 많이 올랐어?"
#
# CHECK 데이터에는 기업집단(그룹) 분류가 없습니다. DeepSearch는 상장사마다 **기업집단 ID**를 붙여 두고 그룹 정보를 따로 제공합니다.
#
# | 단계 | DeepSearch |
# |---|---|
# | 상장사 → 그룹 | `GetStockSymbols()`의 `conglomerate_id` (전 종목 한 번) |
# | 그룹 이름·대기업집단 여부 | `FindConglomerateByID([...])` (한 번), `top30`=1 이 대기업집단 |
# | 그룹 계열사 전체(비상장 포함) | `GetConglomerateMembers(id)` |
# | 시가총액·수익률 | 날짜별 전 종목 시세(`GetStockPrices`) 4번 |

# %%
ASOF = "2026-11-24"
HORIZONS = {"1개월": pd.DateOffset(months=1), "3개월": pd.DateOffset(months=3), "연초 이후": None}
DETAIL_GROUP = "삼성"
print(PRICE_NOTICE)

# %% [markdown]
# ## 1. 상장사와 그룹 연결

# %%
sym = ds_df("GetStockSymbols()")
sym = sym[(sym["company_type_l1"] == "1") & sym["symbol"].str.endswith("0") & sym["market"].isin(["KOSPI", "KOSDAQ"])]
ids = sorted(sym["conglomerate_id"].dropna().unique())
grp = ds_df("FindConglomerateByID([" + ", ".join(f'"{i}"' for i in ids) + "])")
grp = grp[["conglomerate_id", "name_ko", "owner", "top30", "member_count", "main_company_name"]].rename(
    columns={"name_ko": "그룹", "owner": "동일인", "member_count": "계열사 수"})
big = grp[grp["top30"].astype(str) == "1"]
print(f"그룹 ID가 있는 상장사 {sym['conglomerate_id'].notna().sum()}곳 / 그룹 {len(grp)}개 중 대기업집단(top30=1) {len(big)}개")

# %% [markdown]
# ## 2. 날짜별 전 종목 시세
# 기준일, 1개월 전, 3개월 전, 작년 마지막 거래일 — 4번 호출합니다. 수익률은 **시작 시점 시가총액 가중**(그 사이 상장한 종목은 제외)입니다.

# %%
asof = pd.Timestamp(ASOF)
dates = {"기준": asof}
for k, off in HORIZONS.items():
    dates[k] = asof - off if off is not None else pd.Timestamp(f"{asof.year - 1}-12-31")
snaps = {}
for k, d in dates.items():
    a = all_stocks(d.date())
    snaps[k] = a[["symbol", "name", "close", "market_cap"]].set_index("symbol")
    print(f"{k:6} → 거래일 {a['date'].max().date()} ({len(a)}종목)")
now = snaps["기준"].join(sym.set_index("symbol")[["conglomerate_id"]], how="inner").reset_index()
now = now.merge(grp, on="conglomerate_id", how="left")

def group_return(members, start_key):
    s0 = snaps[start_key].reindex(members["symbol"]).dropna()
    if s0.empty:
        return float("nan")
    p1 = snaps["기준"].reindex(s0.index)["close"]
    w = s0["market_cap"]
    return (w * (p1 / s0["close"] - 1)).sum() / w.sum()

# %% [markdown]
# ## 3. 대기업집단 순위

# %%
total_cap = snaps["기준"]["market_cap"].sum()
rows = []
for cid, g in now[now["conglomerate_id"].isin(big["conglomerate_id"])].groupby("conglomerate_id"):
    r = {"그룹": g["그룹"].iloc[0], "동일인": g["동일인"].iloc[0], "상장사": len(g), "계열사 수": g["계열사 수"].iloc[0],
         "시가총액": g["market_cap"].sum(), "시장 비중": g["market_cap"].sum() / total_cap,
         "대표 상장사": g.sort_values("market_cap", ascending=False)["name"].head(3).str.cat(sep=", ")}
    for k in HORIZONS:
        r[k] = group_return(g, k)
    rows.append(r)
board = pd.DataFrame(rows).sort_values("시가총액", ascending=False).reset_index(drop=True)
show = board.copy()
show["시가총액"] = show["시가총액"].map(krw)
show["시장 비중"] = (show["시장 비중"] * 100).map("{:.1f}%".format)
for k in HORIZONS:
    show[k] = (show[k] * 100).map("{:+.1f}%".format)
print(f"코스피+코스닥 일반 보통주 시가총액 {krw(total_cap)} 기준")
show.head(20)

# %%
top = board.head(15).set_index("그룹")[list(HORIZONS)] * 100
ax = top.plot.barh(figsize=(8, 6), title="상위 15개 그룹 시가총액 가중 수익률(%)")
ax.invert_yaxis(); ax.axvline(0, color="gray", lw=.5); ax.grid(alpha=.3, axis="x")

# %% [markdown]
# ## 4. 한 그룹 자세히 보기
# 그룹 안에서 시가총액 비중과 종목별 수익률을 봅니다. 비상장 계열사까지 포함한 전체 명단은 `GetConglomerateMembers`로 받습니다.

# %%
cid = board.merge(grp, on="그룹").query("그룹 == @DETAIL_GROUP")["conglomerate_id"].iloc[0]
g = now[now["conglomerate_id"] == cid].copy()
g["그룹 내 비중"] = g["market_cap"] / g["market_cap"].sum()
for k in HORIZONS:
    s0 = snaps[k]["close"]
    g[k] = g["symbol"].map(lambda x: snaps["기준"]["close"].get(x) / s0.get(x) - 1 if x in s0.index else float("nan"))
out = g.sort_values("market_cap", ascending=False)[["name", "close", "market_cap", "그룹 내 비중"] + list(HORIZONS)].copy()
out["market_cap"] = out["market_cap"].map(krw)
out["그룹 내 비중"] = (out["그룹 내 비중"] * 100).map("{:.1f}%".format)
for k in HORIZONS:
    out[k] = (out[k] * 100).map(lambda v: "-" if pd.isna(v) else f"{v:+.1f}%")
members = ds_df(f'GetConglomerateMembers("{cid}")')
print(f"{DETAIL_GROUP} 그룹: 계열사 {len(members)}곳(사업연도 {members['fiscal_year'].max()}) 중 상장 {len(g)}곳")
out.rename(columns={"name": "종목", "close": "종가", "market_cap": "시가총액"})

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 그룹 수익률은 계열 상장사를 **시작 시점 시가총액으로 가중**한 값이라 대형 계열사(삼성전자, SK하이닉스 등)가 좌우합니다.
# - 그룹 소속은 **현재 기준**입니다. 기간 중 계열 편입·제외된 회사도 지금 소속으로 계산됩니다.
# - 우선주와 ETF는 뺐습니다. 리츠는 일반법인으로 분류돼 포함될 수 있습니다(예: 삼성FN리츠). 지주회사와 자회사가 함께 상장된 그룹은 시가총액이 이중으로 잡히는 면이 있습니다.
# - 대기업집단 표시(`top30`=1)는 DeepSearch 분류이고 공정위 지정 목록과 정확히 같지 않을 수 있습니다.
