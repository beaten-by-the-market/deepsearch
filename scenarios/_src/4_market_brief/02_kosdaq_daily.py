# %% [markdown]
# # 4-02 코스닥 일일동향 — 지수·시총·종목동향·업종·상하위 종목
#
# **질문 예시:** "코스닥 어제 하루 어땠어?", "11월 24일 코스닥 상승/하락 종목수랑 업종동향 보여줘"
#
# CHECK 원본(`4_시황재현/02_코스닥일일동향`)은 거래소 **코스닥 일일동향 리포트**를 지수·시총·종목동향·업종·공매도·신용까지 재현했습니다.
# DeepSearch에서는 이렇게 바꿉니다.
#
# | 리포트 항목 | DeepSearch | 비고 |
# |---|---|---|
# | 코스닥·대중소형 지수 | `GetMarketIndexes` | 그대로 |
# | 시가총액·거래대금·종목동향 | `GetStockPrices` 전 종목 하루치 | 직접 집계 (상·하한가는 ±29.5% 근사) |
# | 업종동향 | 종목 업종코드(KSIC)로 **시총가중 등락률 직접 계산** | KRX 코스닥 업종지수가 없어 근사 |
# | 상승·하락·거래대금 상위 종목 | 같은 스냅샷 | CHECK 리포트보다 자세히 |
# | **투자자별 수급, 공매도, 신용잔고** | **없음** | DeepSearch에 데이터가 없음 (`research/data_gaps`) |

# %%
ASOF = "2026-11-24"   # 기준일 (휴장이면 직전 거래일)
# %%
# 업종 분류: GetStockSymbols 의 industry_id = "KRI:10" + KSIC(10차) 코드. 예) KRI:10C2612000 → C26(중분류)
KSIC_DIV = {
    "A01": "농업", "A03": "어업", "C10": "식료품", "C11": "음료", "C12": "담배", "C13": "섬유제품",
    "C14": "의복·모피", "C15": "가죽·가방·신발", "C16": "목재", "C17": "펄프·종이", "C18": "인쇄",
    "C19": "석유정제품", "C20": "화학제품", "C21": "의약품", "C22": "고무·플라스틱", "C23": "비금속광물",
    "C24": "1차금속", "C25": "금속가공", "C26": "전자부품·컴퓨터·통신장비", "C27": "의료·정밀·광학기기",
    "C28": "전기장비", "C29": "기타 기계·장비", "C30": "자동차·부품", "C31": "기타 운송장비(조선 등)",
    "C32": "가구", "C33": "기타 제품", "D35": "전기·가스", "E38": "폐기물·재생", "F41": "종합건설",
    "F42": "전문공사", "G45": "자동차 판매", "G46": "도매", "G47": "소매", "H49": "육상운송",
    "H50": "수상운송", "H51": "항공운송", "H52": "창고·운송서비스", "I55": "숙박", "J58": "출판·소프트웨어",
    "J59": "영상·오디오 제작", "J60": "방송", "J61": "통신", "J62": "IT서비스·SI", "J63": "정보서비스(포털 등)",
    "K64": "금융업", "K65": "보험", "K66": "금융서비스(증권 등)", "L68": "부동산", "M70": "연구개발(바이오 등)",
    "M71": "전문서비스", "M72": "엔지니어링", "M73": "기타 과학기술서비스", "N74": "시설관리",
    "N75": "사업지원서비스", "N76": "임대", "P85": "교육", "R90": "창작·예술", "R91": "스포츠·오락",
    "S95": "수리", "S96": "기타 개인서비스",
}
# 큰 업종 묶음 (KRX 섹터지수와 1:1은 아님 — 비교하기 쉬운 수준으로 직접 묶은 근사)
_GROUPS = {
    "반도체·전자": ["C26"], "2차전지·전기장비": ["C28"], "자동차": ["C30", "G45"], "조선·운송장비": ["C31"],
    "기계": ["C29"], "화학·정유": ["C19", "C20"], "제약·바이오": ["C21", "M70"], "의료·정밀기기": ["C27"],
    "철강·금속": ["C24", "C25"], "소재(비금속·종이·플라스틱)": ["C16", "C17", "C22", "C23"],
    "음식료·생활소비재": ["A01", "A03", "C10", "C11", "C12", "C13", "C14", "C15", "C18", "C32", "C33"],
    "건설": ["F41", "F42", "M72"], "유통·상사": ["G46", "G47"], "운송·물류": ["H49", "H50", "H51", "H52"],
    "소프트웨어·인터넷": ["J58", "J62", "J63"], "미디어·통신·엔터": ["J59", "J60", "J61", "R90", "R91"],
    "증권·금융": ["K64", "K66"], "보험": ["K65"], "유틸리티·환경": ["D35", "E38"],
    "기타 서비스": ["I55", "L68", "M71", "M73", "N74", "N75", "N76", "P85", "S95", "S96"],
}
DIV2GROUP = {d: g for g, ds_ in _GROUPS.items() for d in ds_}
FIN_HOLDING = ("금융", "신한지주")  # 이름에 들어 있으면 금융지주로 봄 (KB금융, 신한지주, 하나금융지주, 메리츠금융지주 …)


def add_sector(df):
    """industry_id·industry_name → 중분류(div, div_name)와 큰 묶음(sector). 지주회사는 따로 떼고, 금융지주는 증권·금융으로."""
    df = df.copy()
    df["div"] = df["industry_id"].str[6:9]
    df["div_name"] = df["div"].map(KSIC_DIV).fillna(df["div"])
    df["sector"] = df["div"].map(DIV2GROUP).fillna("기타 서비스")
    hold = df["industry_name"].eq("지주회사")
    fin = df["name"].str.contains("|".join(FIN_HOLDING))
    df.loc[hold & ~fin, ["sector", "div_name"]] = ["지주회사", "지주회사"]
    df.loc[hold & fin, ["sector", "div_name"]] = ["증권·금융", "금융지주"]
    return df

# %% [markdown]
# ## 1. 코스닥 지수
# 지수 `change_rate`는 퍼센트, `value`는 백만원 단위입니다. 아래 그래프는 최근 약 1개월 추이입니다.

# %%
d = pd.Timestamp(ASOF)
ix = index_prices((d - pd.Timedelta(days=45)).date(), d.date())
DAY = ix["date"].max()
print("기준 거래일:", DAY.date())
kq = ix[ix["symbol"].str.startswith("KRX:KOSDAQ")]
t = kq[kq["date"] == DAY].set_index("symbol").loc[["KRX:KOSDAQ", "KRX:KOSDAQLC", "KRX:KOSDAQMC", "KRX:KOSDAQSC"]]
display(pd.DataFrame({"지수": t["entity_name"], "종가": t["close"].round(2), "전일 대비": t["change"].round(2),
                      "등락률(%)": t["change_rate"].round(2), "거래대금": (t["value"] * 1e6).map(krw)}).reset_index(drop=True))
ax = kq[kq["symbol"] == "KRX:KOSDAQ"].set_index("date")["close"].plot(figsize=(8, 3), title="코스닥 지수 최근 1개월")
ax.grid(alpha=.3)

# %% [markdown]
# ## 2. 시가총액·거래·종목동향
# 코스닥 전 종목(우선주 포함, ETF 제외) 하루치 시세를 한 번에 받아 집계합니다. 거래가 없던 종목(거래정지 등)은 종목동향에서 뺍니다.

# %%
snap = all_stocks(DAY, common_only=False)
snap = snap[(snap["market"] == "KOSDAQ") & (snap["company_type_l1"] != "8") & (snap["date"] == DAY)]
traded = snap[snap["volume"] > 0]
r = traded["change_rate"]
summary = pd.Series({
    "시가총액": krw(snap["market_cap"].sum()),
    "거래대금(종목 합)": krw(snap["value"].sum()),
    "거래대금(지수)": krw(t.loc["KRX:KOSDAQ", "value"] * 1e6),
    "거래량(종목 합)": f"{snap['volume'].sum() / 1e6:,.1f}백만 주",
    "상장 종목": len(snap), "거래 종목": len(traded),
    "상승": int((r > 0).sum()), "하락": int((r < 0).sum()), "보합": int((r == 0).sum()),
    "상한가(근사, +29.5% 이상)": int(((r >= 0.295) & (r <= 0.305)).sum()),
    "하한가(근사, −29.5% 이하)": int(((r <= -0.295) & (r >= -0.305)).sum()),
    "±30% 초과(기준가 조정 의심)": int((r.abs() > 0.305).sum()),
})
display(summary.to_frame("값"))
odd = traded[traded["change_rate"].abs() > 0.305]
if len(odd):
    print("가격제한폭(±30%)을 넘은 종목 — 신규상장 첫날이거나 권리락·감자·병합 등으로 기준가가 바뀐 날일 가능성이 큽니다.")
    display(odd[["name", "close", "change_rate", "value", "date_listed"]].assign(
        change_rate=lambda x: (x.change_rate * 100).round(2), date_listed=lambda x: x.date_listed.astype(str).str[:10]))

# %% [markdown]
# ## 3. 업종동향 (근사)
# KRX 코스닥 업종지수 대신, 종목의 표준산업분류(KSIC) 중분류별로 **시가총액 가중 평균 등락률**을 계산합니다.
# 종목 5개 미만인 업종은 한두 종목이 좌우하므로 뺐습니다. 큰 묶음(섹터) 기준도 함께 봅니다.

# %%
k = add_sector(snap[snap["symbol"].str.endswith("0") & (snap["company_type_l1"] == "1")])
k = k[k["volume"] > 0]
prev_cap = k["market_cap"] / (1 + k["change_rate"])       # 전일 시총(가중치) 근사

def wavg(g):
    w = prev_cap.loc[g.index]
    return pd.Series({"종목 수": len(g), "등락률(%)": round((g["change_rate"] * w).sum() / w.sum() * 100, 2),
                      "시가총액": krw(g["market_cap"].sum()),
                      "대표 종목": ", ".join(g.nlargest(3, "market_cap")["name"])})

div = pd.DataFrame({n: wavg(g) for n, g in k.groupby("div_name")}).T
div = div[div["종목 수"] >= 5].sort_values("등락률(%)", ascending=False)
print("[강한 업종 5]"); display(div.head(5))
print("[약한 업종 5]"); display(div.tail(5))

# %%
sec = pd.DataFrame({n: wavg(g) for n, g in k.groupby("sector")}).T.sort_values("등락률(%)", ascending=False)
sec

# %% [markdown]
# ## 4. 상승률·하락률·거래대금 상위 종목
# 상승·하락률 상위는 시가총액 300억 원 이상 보통주만 봅니다(초소형주 쏠림 방지). 등락률이 ±30%를 넘으면 위 2절처럼 기준가 조정일일 수 있습니다.

# %%
c = k[k["market_cap"] >= 3e10]

def won(v):
    return krw(v) if abs(v) >= 1e8 else f"{v / 1e4:,.0f}만"

def show(df):
    return pd.DataFrame({"종목": df["name"], "업종": df["div_name"], "종가": df["close"].map("{:,.0f}".format),
                         "등락률(%)": (df["change_rate"] * 100).round(2), "거래대금": df["value"].map(won),
                         "시가총액": df["market_cap"].map(krw)}).reset_index(drop=True)
print(PRICE_NOTICE)
print("\n[상승률 상위 10]"); display(show(c.nlargest(10, "change_rate")))
print("[하락률 상위 10]"); display(show(c.nsmallest(10, "change_rate")))
print("[거래대금 상위 10]"); display(show(k.nlargest(10, "value")))

# %% [markdown]
# ## 5. 한 줄 요약
# 투자자별 수급·공매도·신용잔고는 DeepSearch에 데이터가 없어 넣지 못했습니다(`research/data_gaps`).

# %%
print(f"{DAY.date()} 코스닥은 {t.loc['KRX:KOSDAQ','close']:,.2f}({t.loc['KRX:KOSDAQ','change_rate']:+.2f}%)로 마감했습니다. "
      f"상승 {summary['상승']:,}·하락 {summary['하락']:,}·보합 {summary['보합']:,}종목, 상한가(근사) {summary['상한가(근사, +29.5% 이상)']}·하한가(근사) {summary['하한가(근사, −29.5% 이하)']}종목. "
      f"가장 강한 업종은 {div.index[0]}({div.iloc[0]['등락률(%)']:+.2f}%), 가장 약한 업종은 {div.index[-1]}({div.iloc[-1]['등락률(%)']:+.2f}%)입니다.")
