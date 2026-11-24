# %% [markdown]
# # 1-05 사업 프로파일 — 이 회사는 뭘 팔고, 누구와 경쟁하나
#
# **질문 예시:** "에코프로비엠 뭐 만들어서 파는 회사야? 매출 구성 보여줘", "삼성전자 사업 프로파일 정리해줘"
#
# CHECK 원본(`1_기업펀더멘털/05_사업프로파일`)은 회사 소개·매출 구성·**시장 점유율**을 보여줬습니다.
# DeepSearch로는 다음과 같이 만듭니다.
#
# | 항목 | DeepSearch |
# |---|---|
# | 기본 정보 | `GetCompanySummary` (설립일·대표·업종·직원 수) |
# | 사업 요약·현황 | `GetCompanyBusinessSummary` (사업보고서 요약 문장) |
# | 매출 구성과 추이 | `GetCompanyProductsSales` (사업보고서 제품별 매출, 연간·분기 누적) |
# | 관련 테마 | `GetEntityTags` (DeepSearch 주제 태그) |
# | 같은 업종 상장사 | `GetStockSymbols`의 업종(`industry_name`) + 전 종목 시세 |
# | 시장 점유율 | **구조화 데이터 없음** → 제목에 "점유율"이 들어간 증권사 리포트·뉴스를 찾아 보여줌 |

# %%
ASOF = "2026-11-24"
STOCK = "KRX:247540"   # 에코프로비엠 (삼성전자는 KRX:005930)

# %% [markdown]
# ## 1. 기본 정보와 사업 요약

# %%
s = ds_df(f"GetCompanySummary({STOCK})").iloc[0]
NAME = s["entity_name"]
info = {
    "회사": s["name_ko"], "대표": s["ceo_ko"], "설립일": s["date_founded"] or s["date_established"],
    "주요 사업": s["business_area_ko"], "직원 수": f'{s["employee_no"]:,}명 ({s["date_employees"]} 기준)',
    "홈페이지": s["website"],
}
for k, v in info.items():
    print(f"{k:6}: {v}")

b = ds_df(f"GetCompanyBusinessSummary({STOCK})").iloc[0]
print(f"\n■ {b['summary_title']}")
for c in ("summary_content_1", "summary_content_2", "summary_content_3"):
    print(" ", b[c])
print(f"\n■ {b['status_title']}")
for c in ("status_content_1", "status_content_2", "status_content_3"):
    print(" ", b[c])
print(f"\n(요약 기준일 {str(b['updated_at'])[:10]})")

# %% [markdown]
# ## 2. 매출 구성 (가장 최근 연간)
# 사업보고서의 "제품별 매출"입니다. 단위는 백만원이라 억원으로 바꿉니다. `계`는 합계, 음수는 부문 간 내부거래 제거입니다.

# %%
ps = ds_df(f"GetCompanyProductsSales({STOCK}, date_from=2020-01-01, date_to={ASOF})")
ps["sales_억"] = ps["total_sales"] / 100           # 백만원 → 억원
annual = ps[ps["accounting_type"] == "1"]           # 1=연간, 4=1분기, 2=반기 누적, 5=3분기 누적
last = annual["date"].max()
mix = annual[(annual["date"] == last) & (annual["product_code"] != "99")][["product_name", "sales_억"]].copy()
total = annual[(annual["date"] == last) & (annual["product_code"] == "99")]["sales_억"].iloc[0]
mix["비중(%)"] = (mix["sales_억"] / total * 100).round(1)
print(f"{NAME} {last.year}년 매출 {total:,.0f}억원")
mix.rename(columns={"product_name": "제품(사업보고서 표기)", "sales_억": "매출(억원)"}).round(0)

# %% [markdown]
# ## 3. 매출 구성 추이 (연간)

# %%
# 제품명 표기와 코드가 해마다 조금씩 바뀌므로, 괄호 안 설명과 "및 …"을 떼어 낸 이름으로 묶습니다.
import re
def base_name(n):
    n = re.sub(r"\(.*?\)|\(.*$", "", str(n)).strip()
    return n.split(" 및 ")[0].strip() or str(n)
annual = annual.assign(item=annual["product_name"].map(base_name))
tr = annual[annual["product_code"] != "99"].pivot_table(index="date", columns="item", values="sales_억", aggfunc="sum")
tr.index = tr.index.year
share = tr.div(tr.clip(lower=0).sum(axis=1), axis=0) * 100
print("연도별 매출(억원)")
display(tr.round(0))
ax = share.clip(lower=0).plot(kind="bar", stacked=True, figsize=(8, 4), title=f"{NAME} 매출 구성 비중(%) — 내부거래 제거 제외")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8); _ = ax.set_xlabel("")

# %% [markdown]
# ## 4. 관련 테마 태그
# DeepSearch가 기업에 붙인 주제 태그 가운데 **해당(score=1)** 인 것만 고릅니다.

# %%
tags = ds_df(f"GetEntityTags({STOCK})")
hit = tags[tags["data"].apply(lambda d: isinstance(d, dict) and d.get("score") == 1)].copy()
hit["category"] = hit["category"].apply(lambda c: " ".join(c) if isinstance(c, list) else str(c))
for cat, g in hit.groupby("category"):
    print(cat, ":", ", ".join(g["name"]))

# %% [markdown]
# ## 5. 같은 업종 상장사 (경쟁사 후보)
# 업종 분류(통계청 표준산업분류 세세분류, `industry_name`)가 같은 상장사를 시가총액 순으로 봅니다.

# %%
snap = all_stocks(ASOF)
me = snap[snap["symbol"] == STOCK].iloc[0]
peers = snap[snap["industry_id"] == me["industry_id"]].sort_values("market_cap", ascending=False)
print(f"업종: {me['industry_name']} — 상장사 {len(peers)}곳 (기준 {snap['date'].max().date()})")
out = peers[["name", "market", "close", "change_pct", "market_cap"]].head(10).copy()
out["시가총액"] = out["market_cap"].map(krw)
out.drop(columns="market_cap").round(2)

# %% [markdown]
# ## 6. 점유율 언급 찾기 (대안)
# 점유율 수치는 DeepSearch에 구조화돼 있지 않습니다. 대신 **최근 1년 증권사 리포트·뉴스 가운데 이 회사가 태그되고 본문에 "점유율"이 나오는 문서**를 찾습니다.
# 제목에 "점유율 NN%"가 있으면 수치도 뽑아 둡니다. 리포트 PDF 본문은 스킬의 `read_document.py`로 읽을 수 있습니다.

# %%
import re
start = (pd.Timestamp(ASOF) - pd.DateOffset(years=1) + pd.Timedelta(days=1)).date()
for cat, label in (("research", "증권사 리포트"), ("news", "뉴스")):
    n, d = doc_search(cat, [], f"securities.name:{NAME} and 점유율", start, ASOF, count=50)
    d["점유율 수치"] = d["title"].str.findall(r"점유율[^0-9]{0,6}(\d+(?:\.\d+)?%)").str.join(", ")
    print(f"■ {label} {n}건 — 최근 5건")
    for _, r in d.head(5).iterrows():
        print(f"  {r['created_at']:%Y-%m-%d} [{r['publisher']}] {r['title']}")
    hits = d[d["점유율 수치"] != ""]
    if len(hits):
        print(f"  제목에 점유율 수치가 있는 문서 {len(hits)}건:")
        for _, r in hits.head(5).iterrows():
            print(f"    {r['created_at']:%Y-%m-%d} {r['점유율 수치']} — {r['title']}")
    print()

# %% [markdown]
# ## 결과 읽는 법과 한계
# - 매출 구성의 제품명은 사업보고서 표기를 20자 안팎에서 자른 것입니다(예: `DRAM,NAND Flash,모바일AP 등(제`).
# - 최신 연간이 없으면 분기 누적(`accounting_type` 4·2·5)을 쓰면 됩니다. 분기 누적은 1월부터 그 분기까지의 합계입니다.
# - **시장 점유율 수치는 없습니다.** 리포트·뉴스 검색은 근거 문서를 찾는 용도이고, 수치는 본문에서 확인해야 합니다. 제목에 나온 점유율은 회사 전체가 아니라 특정 시장(예: 중동 스마트폰) 기준인 경우가 많습니다.
# - 같은 업종 상장사는 표준산업분류가 같은 회사라 실제 경쟁사와 다를 수 있습니다(예: 지주사·다각화 기업).
