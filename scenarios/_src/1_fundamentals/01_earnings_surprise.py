# %% [markdown]
# # 1-01 어닝 서프라이즈 — 실적이 증권사 예상과 얼마나 달랐나 (최근 8분기·여러 종목)
#
# **질문 예시:** "삼성전자 작년 실적 컨센 대비 어땠어?", "SK하이닉스·현대차·NAVER 최근 분기들 서프라이즈 비교해줘"
#
# CHECK 원본(`1_기업펀더멘털/01_어닝서프라이즈`)은 IFRS 실적과 날짜별 컨센서스 스냅샷을 비교했습니다.
# DeepSearch로도 같은 계산이 됩니다. 이 노트북은 **여러 종목 × 최근 8분기**의 서프라이즈 이력을 한 표로 만듭니다.
# 발표일 전후 주가 반응은 [1-03 실적발표 이벤트 스터디](03_earnings_event_study.ipynb)에서 봅니다.
#
# | 항목 | DeepSearch |
# |---|---|
# | 분기 실적(매출·영업이익·지배순이익·EPS) | `GetFinancialStatements` 분기·3개월 증분 — **여러 종목 한 번에** |
# | 발표일 | 거래소 공시 `연결재무제표기준영업(잠정)실적(공정공시)` (`DocumentSearch`, 공시) |
# | 발표 직전 컨센서스 | `SearchFirmFundamentalsForecasts` 증권사·작성일별 추정치 → 발표 전 90일 안의 증권사별 최신값 평균 |

# %%
ASOF = "2026-11-24"
STOCKS = {"KRX:005930": "삼성전자", "KRX:000660": "SK하이닉스", "KRX:005380": "현대차", "KRX:035420": "NAVER"}
N_Q = 8            # 최근 몇 분기
LOOKBACK = 90      # 발표 전 며칠 안의 추정치를 컨센서스로 볼지

# %% [markdown]
# ## 1. 분기 실적 (여러 종목 한 번에)
# 연결·IFRS, 3개월 증분(누적 아님) 기준입니다. 지배순이익은 `당기순이익지배기업지분`, EPS는 `기본주당순손익`입니다.

# %%
ACC = {"수익": "매출", "영업이익(손실)": "영업이익", "당기순이익지배기업지분": "지배순이익", "기본주당순손익": "EPS"}
start = (pd.Timestamp(ASOF) - pd.DateOffset(months=3 * N_Q + 6)).date()
fs = ds_df(f'GetFinancialStatements([{", ".join(STOCKS)}], report_type="IFRS", consolidated=True, is_annual=False, '
           f'is_accumulated=False, report_ids="Income", date_from={start}, date_to={ASOF})')
act = (fs[fs["name_ko"].isin(ACC)].pivot_table(index=["symbol", "date"], columns="name_ko", values="value", aggfunc="first")
       .rename(columns=ACC).reset_index())
quarters = sorted(act["date"].unique())[-N_Q:]
act = act[act["date"].isin(quarters)]
print("분기:", ", ".join(pd.Timestamp(q).strftime("%Y-%m") for q in quarters))
t = act.copy()
t["종목"] = t["symbol"].map(STOCKS); t["분기"] = t["date"].dt.strftime("%Y-%m")
for c in ("매출", "영업이익", "지배순이익"):
    t[c] = t[c].map(krw)
t.pivot_table(index="분기", columns="종목", values="영업이익", aggfunc="first")

# %% [markdown]
# ### (참고) 자연어 분기 질의와 비교
# `KRX:005930 시작-끝 분기 당기순이익 분기 기본주당순이익` 같은 자연어 질의도 분기 값을 줍니다.
# 하지만 **범위 첫 행이 4분기면 분기가 아니라 연간 값이 나옵니다**(아래 2024-12-31). 분기 실적은 `GetFinancialStatements`를 쓰세요.

# %%
q0, q1 = pd.Timestamp(quarters[0]) - pd.offsets.QuarterBegin(startingMonth=1), pd.Timestamp(quarters[-1])
nl = ds_df(f"KRX:005930 {q0.date()}-{q1.date()} 분기 당기순이익 분기 기본주당순이익")
nl.columns = ["date", "symbol", "entity_name", "자연어: 당기순이익", "자연어: EPS"]
fs_cmp = fs[(fs["symbol"] == "KRX:005930") & fs["name_ko"].isin(["총당기순이익", "기본주당순손익"])] \
    .pivot_table(index="date", columns="name_ko", values="value").rename(columns={"총당기순이익": "함수: 당기순이익", "기본주당순손익": "함수: EPS"})
cmp_ = nl.set_index("date")[["자연어: 당기순이익", "자연어: EPS"]].join(fs_cmp)
cmp_["일치"] = (cmp_["자연어: 당기순이익"] - cmp_["함수: 당기순이익"]).abs() < 1e9
cmp_.assign(**{c: cmp_[c].map(krw) for c in ("자연어: 당기순이익", "함수: 당기순이익")})

# %% [markdown]
# ## 2. 발표일 찾기
# 거래소 공시 가운데 **`연결재무제표기준영업(잠정)실적`**만 씁니다. 현대차는 월별 판매 실적도 `영업(잠정)실적`이라는 제목으로 내기 때문입니다.
# `[기재정정]`은 빼고, 분기 말 다음 날부터 100일 안의 **첫 공시**를 그 분기의 발표로 봅니다(삼성전자는 분기 첫 주 잠정 발표가 여기에 해당).
# 공시 검색은 한 번에 1년까지라 두 번에 나눠 찾습니다.

# %%
codes = " or ".join(s.split(":")[1] for s in STOCKS)
ann = []
a = pd.Timestamp(quarters[0])
while a < pd.Timestamp(ASOF):
    b = min(a + pd.DateOffset(days=364), pd.Timestamp(ASOF))
    _, d = doc_search("company", ["disclosure"], f"securities.symbol:({codes}) and title:잠정", a.date(), b.date(), count=100)
    ann.append(d)
    a = b + pd.Timedelta(days=1)
ann = pd.concat(ann, ignore_index=True)
ann = ann[ann["title"].str.contains("연결재무제표기준영업\\(잠정\\)실적") & ~ann["title"].str.contains("정정")]
ann["symbol"] = "KRX:" + ann["symbols"].str.split(",").str[0].str.strip()

def announce(sym, q_end):
    d = ann[(ann["symbol"] == sym) & (ann["created_at"] > q_end) & (ann["created_at"] <= q_end + pd.Timedelta(days=100))]
    return d["created_at"].min() if len(d) else pd.NaT

act["발표"] = [announce(s, q) for s, q in zip(act["symbol"], act["date"])]
act.assign(종목=act["symbol"].map(STOCKS), 분기=act["date"].dt.strftime("%Y-%m")) \
   .pivot_table(index="분기", columns="종목", values="발표", aggfunc="first")

# %% [markdown]
# ## 3. 발표 직전 컨센서스와 서프라이즈
# 분기 추정치는 결산월 코드 F(3월)·X(6월)·Y(9월)·Z(12월)로 들어 있고, `forecast_date`가 대상 분기(YYYYMM)입니다.
# - 발표 시각 **이전** `LOOKBACK`일 안에 낸 추정치만 쓰고, 증권사마다 가장 최근 것 하나만 남깁니다.
# - 입력 오류(다른 항목 값을 넣은 경우 등)를 걸러내려고 **중앙값의 1/3~3배를 벗어난 추정치는 뺍니다.**
# - 순이익 추정치(`csd_net_income`)는 지배순이익과 비교합니다. **분기 EPS 추정치(`csd_eps`)는 비어 있어** EPS 서프라이즈는 계산하지 않습니다.

# %%
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)   # 분기 EPS 열이 통째로 비어 생기는 pandas 경고
fcs = []
for sym in STOCKS:                                   # 종목당 1회 (목록으로 넣으면 첫 종목만 옴)
    f = ds_df(f"SearchFirmFundamentalsForecasts({sym}, last_only=False, date_from={start}, date_to={ASOF})")
    if not f.empty:
        fcs.append(f.assign(symbol=sym))
fc = pd.concat(fcs, ignore_index=True)
fc = fc[fc["accounting_type"].isin(["F", "X", "Y", "Z"])]
print("분기 추정치 중 EPS가 채워진 행:", int(fc["csd_eps"].notna().sum()), "/", len(fc))

FIELDS = {"매출": "csd_revenue", "영업이익": "csd_operating_income", "지배순이익": "csd_net_income"}

def consensus(sym, q_end, cut):
    f = fc[(fc["symbol"] == sym) & (fc["forecast_date"] == q_end.strftime("%Y%m")) &
           (fc["date"] < cut.normalize()) & (fc["date"] >= cut.normalize() - pd.Timedelta(days=LOOKBACK))]
    out = {}
    for name, col in FIELDS.items():
        g = f.dropna(subset=[col]).sort_values("date").groupby("inst_code").tail(1)[col]
        if len(g):
            med = g.median()
            g = g[(g > med / 3) & (g < med * 3)] if med > 0 else g
        out[name] = g.mean() if len(g) else None
        out[name + " 증권사 수"] = len(g)
    return out

rows = []
for _, r in act.iterrows():
    cut = r["발표"] if pd.notna(r["발표"]) else r["date"] + pd.Timedelta(days=45)
    c = consensus(r["symbol"], r["date"], cut)
    row = {"종목": STOCKS[r["symbol"]], "분기": r["date"].strftime("%Y-%m"),
           "발표": r["발표"].date() if pd.notna(r["발표"]) else "(공시 없음: 분기말+45일 기준)"}
    for name in FIELDS:
        cons, real = c[name], r[name]
        row[name + " 실제"] = real
        row[name + " 컨센서스"] = cons
        row[name + " 서프라이즈(%)"] = (real / cons - 1) * 100 if cons and real is not None and cons > 0 else None
        row[name + " n"] = c[name + " 증권사 수"]
    rows.append(row)
sur = pd.DataFrame(rows)

show = sur[["종목", "분기", "발표"]].copy()
for name in FIELDS:
    show[name] = [f"{krw(a)} vs {krw(b)} ({s:+.1f}%, {n}곳)" if pd.notna(s) else f"{krw(a)} (컨센서스 없음)"
                  for a, b, s, n in zip(sur[name + " 실제"], sur[name + " 컨센서스"], sur[name + " 서프라이즈(%)"], sur[name + " n"])]
show[show["종목"] == "삼성전자"].reset_index(drop=True)

# %% [markdown]
# ## 4. 종목 비교 — 영업이익 서프라이즈 이력

# %%
op = sur.pivot_table(index="분기", columns="종목", values="영업이익 서프라이즈(%)")[list(STOCKS.values())]
op.round(1)

# %%
stat = pd.DataFrame({
    "평균 서프라이즈(%)": op.mean(),
    "상회 분기 수": (op > 0).sum(),
    "계산된 분기 수": op.notna().sum(),
    "평균 증권사 수": sur.groupby("종목")["영업이익 n"].mean().reindex(op.columns),
}).round(1)
stat["상회 비율"] = (stat["상회 분기 수"] / stat["계산된 분기 수"]).map("{:.0%}".format)
stat

# %%
ax = op.plot(kind="bar", figsize=(10, 4), title="분기별 영업이익 서프라이즈 (실제 ÷ 발표 직전 컨센서스 - 1, %)")
ax.axhline(0, color="gray", lw=.8); ax.set_ylabel("%"); ax.grid(axis="y", alpha=.3)

# %% [markdown]
# ### 다른 종목 표 (매출·영업이익·순이익)

# %%
for nm in list(STOCKS.values())[1:]:
    print(nm)
    display(show[show["종목"] == nm].drop(columns="종목").reset_index(drop=True))

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **서프라이즈 = 실제 ÷ 발표 직전 컨센서스 − 1.** +면 예상보다 잘 나왔다는 뜻입니다. 같은 종목이 계속 상회하면 증권사가 보수적으로 추정하는 경향이 있는 것입니다.
# - 실제 값은 **확정 분기 재무제표** 기준입니다. 잠정 발표 수치와 조금 다를 수 있습니다.
# - 컨센서스는 DeepSearch가 받는 증권사(분기 추정은 대개 3~9곳) 기준이라 시장 전체 컨센서스보다 얇습니다. 증권사 수(`n`)를 같이 보세요.
# - **분기 EPS 컨센서스가 없어** EPS 서프라이즈는 계산하지 않습니다. 순이익 추정치는 일부 증권사만 냅니다.
# - 발표 공시를 못 찾은 분기는 분기 말 + 45일을 기준 시점으로 씁니다(표에 표시). 재무제표가 아직 안 들어온 최신 분기는 표에서 빠집니다.
# - **지배순이익은 분기 값이 튀는 경우가 있습니다**(예: SK하이닉스 2026-06 93.8조 → 2026-09 39.5조, 영업이익보다 큰 분기). 순이익 서프라이즈는 증권사 1~2곳 표본인 경우가 많으니 영업이익을 주로 보세요.
