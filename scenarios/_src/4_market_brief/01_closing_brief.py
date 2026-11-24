# %% [markdown]
# # 4-01 장마감 브리프 — 지수·종목동향·상위 종목·매크로를 한 장으로
#
# **질문 예시:** "어제 장 마감 시황 정리해줘", "11월 24일 코스피·코스닥 마감 브리프 만들어줘"
#
# CHECK 원본(`4_시황재현/01_장마감브리프`)은 KRX Brief를 **지수·지수선물·투자자 수급 + 금리·환율·유가**로 재현했습니다.
# DeepSearch에서는 아래 구성으로 바꿉니다.
#
# | 브리프 항목 | DeepSearch | 비고 |
# |---|---|---|
# | 지수(코스피·코스닥 계열 11종) | `GetMarketIndexes` | 그대로 |
# | 상승·하락·보합·상한가·하한가 종목 수 | `GetStockPrices` 전 종목 하루치 | 직접 집계 (상·하한가는 ±29.5% 근사) |
# | 시가총액·거래대금 상위 종목 | 같은 전 종목 스냅샷 | CHECK에 없던 추가 항목 |
# | 금리·환율·유가·해외지수 | FRED (`QueryFredSeriesData`) | 다우·나스닥·브렌트유도 됨 (CHECK에선 범위 밖) |
# | 오늘 시장 뉴스 | `DocumentSearch`, `DocumentAggregation` | CHECK에 없던 추가 항목 |
# | **지수선물, 투자자별 수급, 국고채** | **없음** | DeepSearch에 데이터가 없음 (`research/data_gaps`) |

# %%
ASOF = "2026-11-24"   # 브리프 날짜 (그날이 휴장이면 직전 거래일)

# %% [markdown]
# ## 1. 지수
# 11종 지수의 종가·등락·거래대금입니다. 지수 `change_rate`는 **퍼센트**, `value`(거래대금)는 **백만원** 단위입니다
# (코스피 거래대금 = 개별 종목 거래대금 합과 같은 규모인지 아래 3절에서 검산합니다).

# %%
d = pd.Timestamp(ASOF)
ix = index_prices((d - pd.Timedelta(days=10)).date(), d.date())
DAY = ix["date"].max()
print("브리프 기준 거래일:", DAY.date())
ORDER = ["KRX:KOSPI", "KRX:KOSPI200", "KRX:KOSPI100", "KRX:KOSPI50", "KRX:KOSPILC", "KRX:KOSPIMC", "KRX:KOSPISC",
         "KRX:KOSDAQ", "KRX:KOSDAQLC", "KRX:KOSDAQMC", "KRX:KOSDAQSC"]
t = ix[ix["date"] == DAY].set_index("symbol").loc[[s for s in ORDER if s in set(ix["symbol"])]]
idx_table = pd.DataFrame({
    "지수": t["entity_name"],
    "종가": t["close"].round(2),
    "전일 대비": t["change"].round(2),
    "등락률(%)": t["change_rate"].round(2),
    "거래대금": (t["value"] * 1e6).map(krw),
}).reset_index(drop=True)
idx_table

# %% [markdown]
# ## 2. 종목동향 — 상승·하락·보합·상한가·하한가
# 전 종목 하루치 시세를 한 번에 받아 시장별로 셉니다. ETF·ETN 등(`company_type_l1`=8)은 빼고, 우선주는 넣었습니다.
# 상한가·하한가는 가격제한폭(±30%)에 닿은 종목을 **등락률 ±29.5~30.5%**로 근사합니다. ±30%를 넘는 종목은 신규상장 첫날이거나
# 권리락·감자 등으로 기준가가 바뀐 날일 가능성이 커서 따로 셉니다(예: 2026-11-24 엠비디 −39.6%는 상장 첫날).

# %%
snap = all_stocks(DAY, common_only=False)
snap = snap[snap["company_type_l1"] != "8"]
snap = snap[snap["date"] == DAY]
traded = snap[snap["volume"] > 0]

def breadth(df):
    r = df["change_rate"]
    return pd.Series({"종목 수": len(df), "상승": (r > 0).sum(), "하락": (r < 0).sum(), "보합": (r == 0).sum(),
                      "상한가(근사)": ((r >= 0.295) & (r <= 0.305)).sum(), "하한가(근사)": ((r <= -0.295) & (r >= -0.305)).sum(),
                      "±30% 초과": (r.abs() > 0.305).sum()})

bt = pd.DataFrame({m: breadth(traded[traded["market"] == m]) for m in ["KOSPI", "KOSDAQ"]}).T
print("거래 없는 종목(정지 등) 제외:", len(snap) - len(traded), "종목")
bt

# %% [markdown]
# ## 3. 시가총액·거래대금
# 시장별 합계와, 지수 거래대금(백만원 단위)과의 검산입니다. 규모는 맞지만 **지수 거래대금이 종목 합보다 7~9% 큽니다**
# (2026-11-24 코스피 15.8조 vs 14.7조). 시간외 거래 포함 여부 같은 정의 차이로 보이나 확인하지 못했습니다.
# 시장 거래대금을 말할 때는 어느 쪽 숫자인지 밝히세요.

# %%
mk = snap.groupby("market").agg(시가총액=("market_cap", "sum"), 거래대금=("value", "sum")).loc[["KOSPI", "KOSDAQ"]]
idx_val = t.set_index("entity_name")["value"] * 1e6
mk["지수 거래대금"] = [idx_val.get("코스피"), idx_val.get("코스닥")]
mk.apply(lambda c: c.map(krw))

# %% [markdown]
# ## 4. 시가총액 상위 10 · 거래대금 상위 10

# %%
common = snap[snap["symbol"].str.endswith("0") & (snap["company_type_l1"] == "1")]

def show(df):
    return pd.DataFrame({"종목": df["name"], "시장": df["market"], "종가": df["close"].map("{:,.0f}".format),
                         "등락률(%)": (df["change_rate"] * 100).round(2), "시가총액": df["market_cap"].map(krw),
                         "거래대금": df["value"].map(krw)}).reset_index(drop=True)

print(PRICE_NOTICE)
print("\n[시가총액 상위 10]")
display(show(common.nlargest(10, "market_cap")))
print("[거래대금 상위 10]")
display(show(common.nlargest(10, "value")))

# %% [markdown]
# ## 5. 기타 — 금리·환율·유가·해외지수 (FRED)
# FRED 미국 시리즈는 공표가 1~3 영업일 늦습니다. 그래서 각 시리즈의 **기준일을 함께** 보여 줍니다.
# 등락은 바로 앞 관측치 대비입니다.

# %%
MACRO = {"DGS2": ("미국 2년 국채", "%"), "DGS10": ("미국 10년 국채", "%"), "DEXKOUS": ("원/달러", "원"),
         "DTWEXBGS": ("달러지수(광의)", ""), "DCOILWTICO": ("WTI", "$"), "DCOILBRENTEU": ("브렌트유", "$"),
         "DJIA": ("다우존스", ""), "NASDAQCOM": ("나스닥 종합", ""), "SP500": ("S&P 500", "")}
mac = fred(list(MACRO), (d - pd.Timedelta(days=20)).date(), d.date())
rows = []
for sid, (name, unit) in MACRO.items():
    s = mac[sid].dropna() if sid in mac else pd.Series(dtype=float)
    if len(s) < 2:
        rows.append({"항목": name, "시리즈": sid, "기준일": None, "값": None, "직전 대비": None})
        continue
    chg = s.iloc[-1] - s.iloc[-2]
    rows.append({"항목": name, "시리즈": sid, "기준일": s.index[-1].date(), "값": round(s.iloc[-1], 2),
                 "직전 대비": f"{chg:+.2f}" + ("%p" if unit == "%" else f" ({chg / s.iloc[-2] * 100:+.2f}%)")})
pd.DataFrame(rows)

# %% [markdown]
# ## 6. 오늘 시장 뉴스
# 기준일 경제 뉴스 중 증시 관련 제목과, 그 기사들에 종목 태그가 가장 많이 붙은 종목입니다.
# 종목 태그는 DeepSearch가 기사에서 자동 인식한 것이라 **오인식이 섞일 수 있습니다**
# (예: 2026-11-24에는 '엔비디아' 기사들이 코스닥 종목 '엠비디'로 태그되어 1위로 나왔습니다). 상위 종목은 제목으로 한 번 확인하세요.

# %%
total, news = doc_search("news", ["economy"], "title:(코스피 or 코스닥 or 증시)", DAY.date(), DAY.date(), count=100)
print(f"증시 제목 기사 {total:,}건 (최근 10건)")
display(news.sort_values("created_at", ascending=False).head(10)[["created_at", "publisher", "title"]])
agg = ds_df(f'DocumentAggregation(["news"],["economy"],"title:(코스피 or 코스닥 or 증시)","securities.name:10",'
            f'date_from={DAY.date()},date_to={DAY.date()})')
agg = agg.rename(columns={"key": "종목", "count": "기사 수"})[["종목", "기사 수"]]
print("증시 기사에 많이 나온 종목")
agg

# %% [markdown]
# ## 7. 한 줄 요약 (자동 문장)

# %%
k = t.set_index("entity_name")
kp, kq = bt.loc["KOSPI"], bt.loc["KOSDAQ"]
top = common.nlargest(1, "market_cap").iloc[0]
print(f"{DAY.date()} 코스피는 {k.loc['코스피','close']:,.2f}({k.loc['코스피','change_rate']:+.2f}%), "
      f"코스닥은 {k.loc['코스닥','close']:,.2f}({k.loc['코스닥','change_rate']:+.2f}%)로 마감했습니다. "
      f"코스피는 {kp['상승']:,}종목 상승·{kp['하락']:,}종목 하락, 코스닥은 {kq['상승']:,}종목 상승·{kq['하락']:,}종목 하락입니다. "
      f"시가총액 1위 종목({top['name']}) 등락률은 {top['change_rate'] * 100:+.2f}%입니다.")
print("※ 투자자별 수급(외국인·기관·개인)과 지수선물은 DeepSearch에 데이터가 없어 이 브리프에 넣지 못했습니다.")
