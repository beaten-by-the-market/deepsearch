# %% [markdown]
# # 4-04 섹터 로테이션 — 업종별 수익률로 자금 흐름 읽기
#
# **질문 예시:** "오늘 어느 업종이 강했어?", "이번 주·이번 달 가장 강한 섹터랑 약한 섹터 정리해줘"
#
# CHECK 원본(`4_시황재현/04_섹터로테이션`)은 **KRX 섹터지수**(반도체·증권·은행 등 15개 안팎)를 등락률로 줄 세웠습니다.
# DeepSearch에는 섹터지수가 없습니다(지수는 코스피·코스닥 계열 11종뿐). 그래서 **업종지수를 직접 만듭니다.**
#
# 1. 전 종목 하루치 시세를 기준일·1주 전·1개월 전 세 번 받습니다(`GetStockPrices`, 호출 3회).
# 2. 종목 업종코드(KSIC 중분류)를 큰 업종 20여 개로 묶습니다. 지주회사는 따로, 금융지주는 증권·금융으로 둡니다.
# 3. 업종 수익률 = 기간 시작 시점 **시가총액 가중** 평균 수익률 (KRX 섹터지수와 같은 시총가중 방식이지만 구성 종목은 다릅니다).

# %%
ASOF = "2026-11-24"           # 기준일
MARKETS = ["KOSPI", "KOSDAQ"]  # 코스피만 보려면 ["KOSPI"]
MIN_N = 3                      # 종목이 이보다 적은 업종은 표에서 뺌
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
# ## 1. 비교 날짜 정하기
# 지수 일별 데이터로 거래일 달력을 만들어 1주(5거래일) 전, 1개월(약 21거래일) 전 날짜를 고릅니다.

# %%
d = pd.Timestamp(ASOF)
ix = index_prices((d - pd.Timedelta(days=50)).date(), d.date())
days = sorted(ix["date"].unique())
DAY, W1, M1, D1 = days[-1], days[-6], days[-22], days[-2]
print("기준일", DAY.date(), "| 1주 전", W1.date(), "| 1개월 전", M1.date())
kospi = ix[ix["symbol"] == "KRX:KOSPI"].set_index("date")["close"]
kosdaq = ix[ix["symbol"] == "KRX:KOSDAQ"].set_index("date")["close"]
bench = pd.DataFrame({"1일(%)": [kospi[DAY] / kospi[D1] - 1, kosdaq[DAY] / kosdaq[D1] - 1],
                      "1주(%)": [kospi[DAY] / kospi[W1] - 1, kosdaq[DAY] / kosdaq[W1] - 1],
                      "1개월(%)": [kospi[DAY] / kospi[M1] - 1, kosdaq[DAY] / kosdaq[M1] - 1]},
                     index=["코스피", "코스닥"]).mul(100).round(2)
bench

# %% [markdown]
# ## 2. 전 종목 수익률과 업종 묶기

# %%
cols = ["close", "change_rate", "market_cap", "volume"]
now = all_stocks(DAY, columns=cols)
now = add_sector(now[now["market"].isin(MARKETS) & (now["date"] == DAY)])
base = {}
for label, day in (("1주", W1), ("1개월", M1)):
    b = all_stocks(day, columns=["close", "market_cap"])
    base[label] = b[b["date"] == day].set_index("symbol")[["close", "market_cap"]]

df = now.set_index("symbol")
df["w_1일"] = df["market_cap"] / (1 + df["change_rate"])   # 전일 시총 근사
df["r_1일"] = df["change_rate"]
for label in base:
    df[f"r_{label}"] = df["close"] / base[label]["close"] - 1
    df[f"w_{label}"] = base[label]["market_cap"]
print("종목 수:", len(df), "| 1개월 전 시세가 없는 종목(그 뒤 상장 등):", df["r_1개월"].isna().sum())
print(PRICE_NOTICE)

# %% [markdown]
# ## 3. 업종 수익률 표 (큰 묶음)

# %%
def sector_table(df, key):
    out = {}
    for name, g in df.groupby(key):
        row = {"종목 수": len(g), "시가총액": g["market_cap"].sum()}
        for p in ("1일", "1주", "1개월"):
            x = g[[f"r_{p}", f"w_{p}"]].dropna()
            row[f"{p}(%)"] = (x[f"r_{p}"] * x[f"w_{p}"]).sum() / x[f"w_{p}"].sum() * 100 if len(x) else None
        row["대표 종목"] = ", ".join(g.nlargest(3, "market_cap")["name"])
        out[name] = row
    t = pd.DataFrame(out).T
    t = t[t["종목 수"] >= MIN_N]
    for c in ("1일(%)", "1주(%)", "1개월(%)"):
        t[c] = t[c].astype(float).round(2)
    t["시가총액"] = t["시가총액"].map(krw)
    return t

sec = sector_table(df, "sector").sort_values("1개월(%)", ascending=False)
sec["1개월 순위"] = range(1, len(sec) + 1)
sec["1주 순위"] = sec["1주(%)"].rank(ascending=False).astype(int)
sec["순위 변화(1주−1개월)"] = sec["1개월 순위"] - sec["1주 순위"]   # +면 최근 1주에 순위가 올라옴
sec

# %%
ax = sec[["1일(%)", "1주(%)", "1개월(%)"]].iloc[::-1].plot.barh(figsize=(9, 8), title=f"업종별 시총가중 수익률 (기준 {DAY.date()})")
ax.axvline(0, color="gray", lw=.8); ax.grid(axis="x", alpha=.3)

# %% [markdown]
# ## 4. 무엇이 업종을 움직였나 — 1개월 최강·최약 업종의 기여 종목
# 기여도 = 종목 비중(1개월 전 시총 기준) × 종목 수익률. 대형주 한두 개가 업종 수익률을 좌우하는지 확인합니다.

# %%
def contributors(sector, n=5):
    g = df[(df["sector"] == sector)].dropna(subset=["r_1개월"])
    w = g["w_1개월"] / g["w_1개월"].sum()
    c = (w * g["r_1개월"] * 100).rename("기여(%p)")
    out = pd.DataFrame({"종목": g["name"], "비중(%)": (w * 100).round(1), "1개월(%)": (g["r_1개월"] * 100).round(1),
                        "기여(%p)": c.round(2)})
    return out.reindex(c.abs().sort_values(ascending=False).index).head(n).reset_index(drop=True)

for s in (sec.index[0], sec.index[-1]):
    print(f"[{s}] 1개월 {sec.loc[s, '1개월(%)']:+.2f}%")
    display(contributors(s))

# %% [markdown]
# ## 5. 세부 업종(KSIC 중분류) 상위·하위
# 큰 묶음 안에서 어느 세부 업종이 강했는지 봅니다(종목 5개 이상만).

# %%
div = sector_table(df, "div_name")
div = div[div["종목 수"] >= 5].sort_values("1주(%)", ascending=False)
print("[최근 1주 강한 세부 업종 7]"); display(div.head(7))
print("[최근 1주 약한 세부 업종 7]"); display(div.tail(7))

# %% [markdown]
# ## 6. 읽는 법과 한계
# - **위험선호 vs 방어:** 반도체·2차전지·기계·증권이 앞서면 위험선호(risk-on), 음식료·통신·유틸리티가 앞서면 방어(risk-off)로 읽습니다.
# - **순위 변화가 큰 업종**은 자금이 새로 들어오거나 빠지는 곳입니다(최근 1주 순위가 1개월 순위보다 높으면 +).
# - **KRX 섹터지수와 숫자가 다릅니다.** 업종 분류(KSIC 기준, 예: 삼성물산은 '도매'), 구성 종목(전 종목), 가중 방식(유동주식 아닌 전체 시총)이 다릅니다.
# - 업종 분류는 현재 기준 하나뿐이고, 현재 상장 종목만 들어갑니다(기간 중 상장폐지 종목 제외).
# - 투자자별 수급과 결합("외국인이 들어온 업종")은 DeepSearch에 수급 데이터가 없어 할 수 없습니다.
