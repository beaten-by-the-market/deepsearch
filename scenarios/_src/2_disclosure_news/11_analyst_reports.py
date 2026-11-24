# %% [markdown]
# # 2-11 증권사 리포트 흐름 — 누가 언제 무슨 리포트를 냈고, 목표주가는 어디쯤인가
#
# **질문 예시:** "삼성전자 최근 반년 증권사 리포트 정리해줘", "증권사 목표주가 평균이랑 지금 주가 차이는?", "최신 리포트 첫 장 요약해줘", "요즘 리포트가 가장 많이 나오는 종목은?"
#
# CHECK API에는 증권사 리포트·목표주가·투자의견이 없습니다(CHECK `1_기업펀더멘털` README: "목표주가·투자의견은 제공되지 않습니다").
# DeepSearch는 **리포트 원문 PDF**와 **증권사별 목표주가·투자의견**을 함께 줘서, 새로 만든 시나리오입니다.
#
# | 단계 | DeepSearch 함수 |
# |---|---|
# | 리포트 목록(증권사·제목·PDF) | `DocumentSearch(["research"],["company"], "securities.symbol:005930")` |
# | 목표주가·투자의견 | `SearchTargetPrices(KRX:005930, …)` |
# | 주가 | `GetStockPrices` |
# | 리포트가 많이 나온 종목 | `DocumentAggregation(["research"],["company"], "*", "securities.symbol:30")` |
# | PDF 본문 | 리포트 링크(`ddi-cdn.deepsearch.com/…pdf`)를 받아 PyMuPDF로 텍스트 추출 |
#
# **종목 지정은 `securities.symbol:6자리코드`로 하세요.** 리서치 문서의 종목 이름은 `에스케이하이닉스`·`현대자동차`처럼 공식명이 섞여 있어
# `securities.name:SK하이닉스`로는 일부만 잡힙니다(2026-08~11 SK하이닉스: 이름 2건 vs 코드 19건).

# %%
ASOF = "2026-11-24"
START = "2026-05-25"     # 리포트 검색은 1년 이내
CODE = "005930"          # 삼성전자

# %%
import re, sys, subprocess
try:
    import fitz  # PyMuPDF
except ImportError:      # Colab 에는 기본으로 없다
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "pymupdf"], check=True)
    import fitz

# %% [markdown]
# ## 1. 리포트 목록

# %%
total, rep = doc_search("research", ["company"], f"securities.symbol:{CODE}", START, ASOF, count=100, pages=2)
rep = rep.sort_values("created_at", ascending=False).drop_duplicates(["publisher", "title"])
name = universe().set_index("symbol").loc[f"KRX:{CODE}", "name"]
print(f"{name} 기업 리포트 {total}건 (중복 제외 {len(rep)}건), {START} ~ {ASOF}")
rep[["created_at", "publisher", "title"]].head(12)

# %% [markdown]
# 증권사별·월별 건수. 증권사 이름은 원문 그대로라 `미래에셋대우`(현 미래에셋증권), `신한금융투자`(현 신한투자증권)처럼 옛 이름이 섞여 있습니다.

# %%
rep["월"] = rep["created_at"].dt.strftime("%Y-%m")
pd.crosstab(rep["publisher"], rep["월"], margins=True, margins_name="합계").sort_values("합계", ascending=False)

# %% [markdown]
# ## 2. 목표주가·투자의견 vs 주가
# `SearchTargetPrices`의 `opinion_code`: 1~2 매도 쪽, 3 중립, 4~5 매수 쪽. **컨센서스**는 날짜마다 증권사별 가장 최근 목표가(최근 90일 이내)의 평균으로 계산합니다.

# %%
tp = ds_df(f"SearchTargetPrices(KRX:{CODE}, date_from={START}, date_to={ASOF})")
tp = tp[tp["target_price"] > 0].sort_values("date")
OPINION = {1: "매도", 2: "비중축소", 3: "중립", 4: "매수", 5: "강력매수"}
tp["의견"] = tp["opinion_code"].map(OPINION)
px = stock_prices(f"KRX:{CODE}", START, ASOF, columns=["close"]).set_index("date")["close"]
print(PRICE_NOTICE)
print(f"목표주가 {len(tp)}건, 증권사 {tp['name_ko'].nunique()}곳 | 투자의견 분포: {tp['의견'].value_counts().to_dict()}")

tp["직전 대비(%)"] = (tp["target_price"] / tp.groupby("name_ko")["target_price"].shift() - 1) * 100
latest = tp.groupby("name_ko").tail(1).sort_values("date", ascending=False)
latest[["date", "name_ko", "의견", "target_price", "직전 대비(%)", "current_price"]].rename(
    columns={"name_ko": "증권사", "target_price": "목표주가", "current_price": "발표 당시 주가"}).round(1)

# %%
def consensus(day, window=90):
    w = tp[(tp["date"] <= day) & (tp["date"] > day - pd.Timedelta(days=window))]
    return w.groupby("name_ko").tail(1)["target_price"].mean() if len(w) else None

cons = pd.Series({d: consensus(d) for d in px.index})
last_day = px.index[-1]
for w in (90, 30):
    c = consensus(last_day, w)
    print(f"{last_day.date()} 종가 {px.iloc[-1]:,.0f}원 | 최근 {w}일 목표주가 컨센서스 "
          + (f"{c:,.0f}원 | 괴리(상승여력) {(c / px.iloc[-1] - 1) * 100:+.1f}%" if c else "없음"))
print("※ 주가가 급락한 뒤엔 예전 목표가가 남아 있어 90일 컨센서스의 괴리가 크게 나옵니다. 최근 30일 값과 같이 보세요.")

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(px.index, px.values, color="k", label="종가(수정주가)")
ax.plot(cons.index, cons.values, color="#c0504d", label="목표주가 컨센서스(90일)")
ax.scatter(tp["date"], tp["target_price"], s=14, color="#c0504d", alpha=.4, label="개별 목표주가")
for d in rep["created_at"].dt.normalize().unique():
    ax.axvline(d, color="#4f81bd", alpha=.08)
ax.set_title(f"{name} 주가와 증권사 목표주가 (파란 세로줄: 리포트 발간일)"); ax.legend(fontsize=8); ax.grid(alpha=.3)

# %% [markdown]
# ## 3. 최신 리포트 PDF 첫 장 읽기
# 리포트 링크는 공개 CDN의 PDF입니다. 첫 페이지 텍스트에서 투자의견·목표주가 줄을 찾아 보여줍니다.

# %%
pdf_doc = rep[rep["url"].str.endswith(".pdf", na=False)].iloc[0]
print(pdf_doc["created_at"].date(), pdf_doc["publisher"], "|", pdf_doc["title"])
pdf = fitz.open(stream=requests.get(pdf_doc["url"], timeout=60).content, filetype="pdf")
first = pdf[0].get_text()
print(f"총 {pdf.page_count}쪽, 첫 장 {len(first):,}자\n")
for line in first.splitlines():
    if re.search(r"목표주가|투자의견|Target|BUY|매수|Rating", line, re.I):
        print("  ▶", line.strip()[:100])
print("\n--- 첫 장 앞부분 ---\n" + re.sub(r"\n{2,}", "\n", first)[:900])

# %% [markdown]
# ## 4. 요즘 리포트가 가장 많이 나온 종목
# 최근 4주 기업 리포트를 종목 코드로 집계합니다. 리포트가 몰리는 종목은 실적 발표·이벤트로 시장의 관심이 큰 종목입니다.

# %%
agg = ds_df(f'DocumentAggregation(["research"],["company"],"*","securities.symbol:30",'
            f'date_from={(pd.Timestamp(ASOF) - pd.Timedelta(days=28)).date()},date_to={ASOF})')
agg = agg[agg["key"].astype(str).str.len() == 6]          # 종목 태그가 없는 리포트("" 키)는 뺀다
agg["symbol"] = "KRX:" + agg["key"].astype(str)
top = agg.merge(universe()[["symbol", "name", "market"]], on="symbol", how="left")
snap = all_stocks(ASOF, common_only=False)[["symbol", "change_pct", "market_cap"]]
top = top.merge(snap, on="symbol", how="left")
top["시가총액"] = top["market_cap"].map(krw)
top[["name", "market", "count", "시가총액", "change_pct"]].rename(
    columns={"name": "종목", "count": "리포트 수(4주)", "change_pct": f"{ASOF} 등락률(%)"}).head(15).round(2)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - DeepSearch 리서치는 **약 15개 증권사**(삼성·신한·한국투자·미래에셋·iM·SK·LS·유진·대신·메리츠·한화·IBK·유안타·상상인·한국IR협의회) 리포트입니다. KB·NH·키움 등은 없어 **전체 컨센서스보다 표본이 작습니다.**
# - 목표주가 컨센서스는 이 노트북이 직접 계산한 값(증권사별 최근 90일 최신값 평균)이라 다른 정보업체 컨센서스와 다를 수 있습니다.
# - 같은 리포트가 두 번 들어온 경우가 있어 증권사·제목으로 중복을 지웠습니다.
# - PDF 첫 장은 증권사마다 배치가 달라 투자의견·목표주가 줄을 못 찾을 수도 있습니다. 숫자는 `SearchTargetPrices` 값을 기준으로 보세요.
# - `SearchAnalystReports` 함수는 이 구독에서 오류(500) 또는 0행이라 쓰지 않습니다.
