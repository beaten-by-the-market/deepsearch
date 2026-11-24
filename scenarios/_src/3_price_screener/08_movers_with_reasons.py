# %% [markdown]
# # 3-08 오늘 급등락 종목과 이유 — 공시 + 뉴스 제목·긍부정
#
# **질문 예시:** "오늘 많이 오른/내린 종목 뭐야? 왜 그런지도 알려줘", "오늘 거래대금 상위 종목은 무슨 뉴스 때문이야?"
#
# 그날 **등락률 상위·하위, 거래대금 상위** 종목을 뽑고, 각 종목에
# ① 전날 장 마감 후부터 당일까지의 **공시**, ② 같은 시간대의 **뉴스 제목과 긍부정**을 붙여 "왜"를 설명합니다.
#
# **왜 DeepSearch로 하나 (CHECK `3_시세스크리너/01` 확장):** CHECK 뉴스에는 종목 태그가 없어 원본은 공시만 붙였습니다.
# 공시가 없는 급등(테마·풍문)은 설명하지 못했습니다. DeepSearch 뉴스에는 종목 태그(`securities`)와
# 긍부정 값이 있어 **공시가 없는 종목도 뉴스로 원인**을 확인할 수 있습니다.
# 또 CHECK 순위 데이터는 최신 거래일만 됐지만, 여기서는 `ASOF`를 바꾸면 **과거 날짜**도 됩니다.

# %%
ASOF = "2026-11-24"   # 기준일(거래일)
TOP = 8               # 그룹별 종목 수
MIN_VALUE = 1e9       # 거래대금 하한(10억) — 거래가 거의 없는 종목의 등락률 제외

# %% [markdown]
# ## 1. 그날 전 종목 시세와 순위
# 신규상장 첫날 종목은 등락률 기준이 달라(공모가 대비) 제외합니다.

# %%
def stocks(day):
    """일반법인(1)·공기업(2) 보통주 전 종목 하루치. 헬퍼의 all_stocks(common_only=True)는 공기업 8종목
    (한국전력·기업은행·강원랜드 등, company_type_l1='2')을 빼므로 여기서 직접 거릅니다."""
    s = all_stocks(day, common_only=False)
    return s[s["company_type_l1"].isin(["1", "2"]) & s["symbol"].str.endswith("0")].reset_index(drop=True)

snap = stocks(ASOF)
day = snap["date"].max().date()
snap = snap[(snap["date"].dt.date == day) & (snap["volume"] > 0)].copy()
listed = pd.to_datetime(snap["date_listed"].astype(str).str[:10], errors="coerce")
snap = snap[~(listed.dt.date >= day)]   # 상장일이 기준일 이후·당일인 종목 제외 (상장일 모르면 유지)
snap["거래대금(억)"] = snap["value"] / 1e8
print("거래일", day, "/ 종목 수", len(snap))

liquid = snap[snap["value"] >= MIN_VALUE]
groups = {
    "상승 상위": liquid.sort_values("change_pct", ascending=False).head(TOP),
    "하락 상위": liquid.sort_values("change_pct").head(TOP),
    "거래대금 상위": snap.sort_values("value", ascending=False).head(TOP),
}
up, down = (snap["change_pct"] > 0).sum(), (snap["change_pct"] < 0).sum()
print(f"상승 {up} / 하락 {down} / 상한가(≥29.5%) {(snap['change_pct'] >= 29.5).sum()} / 하한가 {(snap['change_pct'] <= -29.5).sum()}")
print(PRICE_NOTICE)

# %% [markdown]
# ## 2. 공시 — 대상 종목을 묶어 한 번에
# 전날 15:30 이후 공시는 당일 주가에 반영되므로 함께 봅니다.

# %%
prev_day = sorted(index_prices(day - timedelta(days=10), day)["date"].dt.date.unique())[-2]
since = pd.Timestamp(prev_day) + pd.Timedelta(hours=15, minutes=30)
until = pd.Timestamp(day) + pd.Timedelta(hours=23, minutes=59)

targets = pd.concat(groups.values()).drop_duplicates("symbol")
codes = [s.split(":")[-1] for s in targets["symbol"]]
_, disc = doc_search("company", ["disclosure"], "securities.symbol:(" + " or ".join(codes) + ")",
                     prev_day, day, count=100, pages=3)
if not disc.empty:
    disc = disc[(disc["created_at"] >= since) & (disc["created_at"] <= until)]
print(f"공시 {len(disc)}건 ({since:%m-%d %H:%M} ~ {day})")

def disc_titles(code, n=3):
    if disc.empty:
        return ""
    t = disc[disc["symbols"].str.contains(code, na=False)].sort_values("created_at")["title"].drop_duplicates()
    return " / ".join(t.tolist()[-n:])

# %% [markdown]
# ## 3. 뉴스 — 종목별 제목 상위와 긍부정 비율
# 종목별로 한 번씩 검색합니다(대상 24개 안팎 → 24회 호출, 태그 검색이 0건이면 제목 검색 1회 추가).
# 긍부정은 받은 기사(최대 30건, 사진 기사 제외)의 건수입니다.
# 종목명이 일반 단어와 같은 경우(예: 'DB', 'NEW') 관련 없는 기사가 섞일 수 있어, **제목에 종목명이 들어간 기사**를 우선 보여줍니다.

# %%
def news_for(name, code):
    total, df = doc_search("news", [], f"securities.symbol:{code}", prev_day, day, count=30)
    if df.empty:   # 종목 태그가 빠진 기사도 있어, 0건이면 제목 검색으로 한 번 더
        total, df = doc_search("news", [], f'title:"{name}"', prev_day, day, count=30)
    if df.empty:
        return 0, "", ""
    df = df[(df["created_at"] >= since) & (df["created_at"] <= until) & ~df["title"].str.startswith("[포토]")]
    if df.empty:
        return 0, "", ""
    pol = df["polarity"].value_counts()
    mood = f"긍{pol.get('긍정', 0)}·부{pol.get('부정', 0)}·중{pol.get('중립', 0)}"
    in_title = df[df["title"].str.contains(name, regex=False)]
    pick = (in_title if len(in_title) else df).sort_values("created_at", ascending=False)
    return len(df), mood, " / ".join(pick["title"].str[:45].drop_duplicates().head(2))

news = {}
for sym, name in zip(targets["symbol"], targets["name"]):
    news[sym] = news_for(name, sym.split(":")[-1])

# %% [markdown]
# ## 4. 그룹별 결과

# %%
def table(g):
    t = g[["symbol", "name", "market", "change_pct", "거래대금(억)"]].copy()
    t["공시"] = [disc_titles(s.split(":")[-1]) for s in t["symbol"]]
    t["뉴스수"] = [news[s][0] for s in t["symbol"]]
    t["긍부정"] = [news[s][1] for s in t["symbol"]]
    t["대표 뉴스"] = [news[s][2] for s in t["symbol"]]
    t["원인 근거"] = [("공시+뉴스" if a and n else "공시" if a else "뉴스" if n else "없음")
                   for a, n in zip(t["공시"], t["뉴스수"])]
    return t.set_index("name").drop(columns="symbol").round(1)

table(groups["상승 상위"])

# %%
table(groups["하락 상위"])

# %%
table(groups["거래대금 상위"])

# %% [markdown]
# ## 5. 원인 근거 요약
# 공시만으로 설명되는 종목, 뉴스로만 설명되는 종목(= CHECK 원본에서는 '이유 없음'으로 남았을 종목)을 셉니다.

# %%
summary = pd.concat({k: table(g)["원인 근거"].value_counts() for k, g in groups.items()}, axis=1).fillna(0).astype(int)
summary

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **공시가 없고 뉴스만 있는 급등**은 테마·풍문·업황 기사로 움직인 경우가 많습니다. 대표 뉴스 제목으로 재료를 확인하세요.
# - **긍부정은 기사 단위 모델 값**입니다(`polarity`, 없으면 `customized_ml`의 값). 주가 방향과 반대인 경우도 흔합니다.
# - 뉴스 종목 태그는 동명 종목 오탐이 있습니다. 제목에 종목명이 들어간 기사를 우선 보여주지만, 뉴스 수에는 오탐이 섞일 수 있습니다.
# - **뉴스가 0건인 급등주도 있습니다.** 상한가·대규모 거래에도 DeepSearch에 수집된 기사가 없거나 종목 태그가 빠진 경우입니다
#   (2026-11-24 로보티즈 +19.5%·거래대금 2,090억인데 태그 기사 0건). 이때는 증권사 리포트·커뮤니티 등 다른 출처가 필요합니다.
# - 등락률·거래대금은 KRX 기준(NXT 미포함), 가격은 수정주가입니다.
