# %% [markdown]
# # 5-08 종목정보 불러오기 — 상장사 목록·식별자·기업 개요·52주 주가
#
# **질문 예시:** "상장사 전체 목록이랑 업종·결산월 뽑아줘", "내 관심종목 기업 개요랑 52주 고저 보여줘"
#
# 뉴스·공시를 상장사 기준으로 거르거나 종목별로 묶으려면 먼저 **상장사 목록**이 있어야 합니다.
# `GetStockSymbols()` 한 번이면 4,400여 종목의 시장·업종·식별자(NICE 코드, 사업자번호, 법인번호)·결산월·기업집단이 옵니다.
# 종목별로 `GetEntitySummary`를 반복해 부를 필요가 없습니다.

# %%
ASOF = "2026-11-24"
# 관심종목: 종목명이나 6자리 코드 아무거나. Colab에서는 아래 UPLOAD=True 로 엑셀/CSV를 올려도 됩니다.
WATCHLIST = ["삼성전자", "000660", "에코프로비엠", "현대차", "NAVER", "한국전력"]
UPLOAD = False

# %% [markdown]
# ## 1. 전 종목 기본정보
# `company_type_l1`: 1 일반법인, 2 공기업(한국전력·기업은행 등), 8 ETF·ETN 등. 우선주는 종목코드 끝자리가 0이 아닙니다.

# %%
sym = ds_df("GetStockSymbols()")
sym["code"] = sym.symbol.str.replace("KRX:", "", regex=False)
sym["종류"] = sym.company_type_l1.map({"1": "일반법인", "2": "공기업", "8": "ETF·ETN 등"}).fillna("기타")
sym["우선주"] = ~sym.code.str.endswith("0")
print(f"전체 {len(sym):,}종목 (기준일 {sym.date.max().date()})")
print(pd.crosstab(sym.market, sym.종류, margins=True, margins_name="합계").to_string())
print("\n제공 컬럼:", ", ".join(sym.columns))

# %% [markdown]
# 일반법인·공기업 보통주만 남기면 "상장사"가 됩니다. 결산월과 기업집단 소속도 같이 볼 수 있습니다.

# %%
listed = sym[sym.company_type_l1.isin(["1", "2"]) & ~sym.우선주 & sym.market.isin(["KOSPI", "KOSDAQ", "KONEX"])].copy()
print(f"상장사(보통주) {len(listed):,}개:", listed.market.value_counts().to_dict())
print("결산월:", listed.fiscal_year_end.value_counts().head(5).to_dict())
print("기업집단 소속:", int(listed.conglomerate_id.notna().sum()), "개사")
listed[["code", "entity_name", "market", "industry_name", "symbol_nice", "business_rid", "company_rid",
        "fiscal_year_end", "date_listed"]].head(8)

# %% [markdown]
# ## 2. 종목 찾기 — 이름 일부나 코드로

# %%
def find_stock(text, only_listed=True):
    base = listed if only_listed else sym
    t = str(text).strip()
    hit = base[(base.code == t) | base.entity_name.str.contains(t, regex=False, na=False)]
    return hit[["code", "entity_name", "market", "industry_name"]]

find_stock("하이닉스")

# %%
find_stock("반도체", only_listed=True).head(3)   # 이름에 '반도체'가 든 종목 (업종 검색이 아님)

# %% [markdown]
# ## 3. 관심종목 목록 만들기
# 이름이든 코드든 섞어 넣으면 코드로 바꿉니다. Colab에서 `UPLOAD = True`로 두면 파일 업로드 창이 뜹니다
# (첫 열이나 `종목코드`·`종목명` 열을 읽습니다). 서식 파일은 아래 셀이 만들어 줍니다.

# %%
def to_codes(items):
    out, miss = [], []
    for it in items:
        it = str(it).strip().zfill(6) if str(it).strip().isdigit() else str(it).strip()
        hit = listed[(listed.code == it) | (listed.entity_name == it)]
        (out.append(hit.code.iloc[0]) if len(hit) else miss.append(it))
    if miss:
        print("찾지 못함:", miss)
    return out

if IN_COLAB and UPLOAD:
    from google.colab import files
    up = files.upload()
    name = next(iter(up))
    w = pd.read_excel(name, dtype=str) if name.endswith(("xlsx", "xls")) else pd.read_csv(name, dtype=str)
    col = next((c for c in w.columns if c in ("종목코드", "종목명")), w.columns[0])
    WATCHLIST = w[col].dropna().tolist()

codes = to_codes(WATCHLIST)
watch = listed.set_index("code").loc[codes, ["entity_name", "market", "industry_name"]]
watch

# %%
# 관심종목 서식 파일 (Colab이면 바로 내려받기)
pd.DataFrame({"종목코드": ["005930", "000660"], "종목명": ["삼성전자", "SK하이닉스"]}).to_csv(
    "watchlist_template.csv", index=False, encoding="utf-8-sig")
if IN_COLAB:
    from google.colab import files
    files.download("watchlist_template.csv")
print("watchlist_template.csv 저장")

# %% [markdown]
# ## 4. 기업 개요 — 여러 종목을 한 번에
# `GetCompanySummary`는 종목 목록을 한 번에 받습니다(대표자, 주요 사업, 설립일, 종업원 수, 주소 등).

# %%
summ = ds_df(f"GetCompanySummary([{', '.join('KRX:' + c for c in codes)}])")
keep = [c for c in ["entity_name", "ceo_ko", "business_area_ko", "date_founded", "date_listed", "employee_count",
                    "address_road_name_ko", "website"] if c in summ.columns]
print("GetCompanySummary 컬럼 수:", summ.shape[1])
summ[keep]

# %% [markdown]
# ## 5. 52주 일별 주가와 고저
# 관심종목을 한 번에 받습니다. 가격은 수정주가입니다.

# %%
d0 = (pd.Timestamp(ASOF) - pd.DateOffset(years=1)).date()
px = stock_prices(["KRX:" + c for c in codes], d0, ASOF, columns=["close", "high", "low", "volume", "market_cap"])
print(PRICE_NOTICE)
g = px.groupby("symbol")
t = pd.DataFrame({
    "종목": g.entity_name.last(),
    "현재가": g.close.last(),
    "52주 최고": g.high.max(),
    "52주 최저": g.low.min(),
    "시가총액": g.market_cap.last().map(krw),
})
t["최고가 대비(%)"] = (t.현재가 / t["52주 최고"] * 100 - 100).round(1)
t["최저가 대비(%)"] = (t.현재가 / t["52주 최저"] * 100 - 100).round(1)
t["1년 수익률(%)"] = (g.close.last() / g.close.first() * 100 - 100).round(1)
t.sort_values("1년 수익률(%)", ascending=False)

# %%
w = px.pivot_table(index="date", columns="entity_name", values="close")
ax = (w / w.iloc[0] * 100).plot(figsize=(9, 4), title="관심종목 52주 주가 (시작=100)")
ax.grid(alpha=.3); ax.set_xlabel(""); plt.show()

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 목록은 **현재 상장 종목 기준**입니다. 과거 시점의 상장사 목록(상장폐지 종목 포함)은 이 함수로 만들 수 없습니다.
# - `industry_name`은 통계청 표준산업분류(KSIC)입니다. 거래소 업종·WICS와 다릅니다.
# - 식별번호(NICE·사업자·법인)는 보통주와 우선주가 같습니다. 문서의 회사와 맞출 때는 보통주 목록을 쓰세요(→ 2-13).
