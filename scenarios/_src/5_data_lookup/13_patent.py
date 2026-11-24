# %% [markdown]
# # 5-13 특허 가져오기 — 키워드·회사별 특허와 상장사 출원인
#
# **질문 예시:** "작년 배터리 특허 출원한 상장사 순위 줘", "LG에너지솔루션 특허 월별 추이 보여줘"
#
# DeepSearch `["patent"]`에는 특허정보원(KIPRIS)의 국내 특허·실용신안이 들어 있습니다.
# 문서마다 `patent` 항목에 출원·등록 번호와 날짜, 등록 상태, IPC 분류, 청구항, **출원인(법인번호·사업자번호 포함)**, 발명자, 인용 특허가 있습니다.
# 출원인 이름은 공식명('주식회사 엘지에너지솔루션')이라, 상장사와 맞출 때는 **법인번호·사업자번호**를 씁니다.

# %%
ASOF = "2026-11-24"
KEYWORD = "배터리"
YEAR_FROM, YEAR_TO = "2025-01-01", "2025-12-31"   # 특허는 공개까지 시차가 있어 작년 기준이 안정적
COMPANY = "엘지에너지솔루션"                        # 특허의 회사 이름은 공식명

# %% [markdown]
# ## 1. 상장사 식별번호 지도
# 상장사(보통주)의 법인번호·사업자번호 → 종목코드. (식별번호는 보통주·우선주가 같아 보통주만 씁니다)

# %%
sym = ds_df("GetStockSymbols()")
L = sym[sym.company_type_l1.isin(["1", "2"]) & sym.symbol.str.endswith("0")].copy()
L["code"] = L.symbol.str.replace("KRX:", "", regex=False)
BY_CRID = dict(zip(L.company_rid.dropna().str.replace("-", ""), L.code))
BY_BRID = dict(zip(L.business_rid.dropna().str.replace("-", ""), L.code))
NAME = dict(zip(L.code, L.entity_name)); MKT = dict(zip(L.code, L.market))
print(f"상장사 {len(L):,}개 (법인번호 {len(BY_CRID):,} · 사업자번호 {len(BY_BRID):,})")

# %% [markdown]
# ## 2. 키워드 특허 받기 — '배터리', 2025년
# 문서 원본(`patent` 항목 포함)이 필요해 `ds()`로 직접 받습니다. 한 페이지 100건, 여기서는 5페이지(500건)까지.

# %%
def patent_docs(query, date_from, date_to, pages=5):
    docs, total = [], 0
    for p in range(1, pages + 1):
        c = ds(f'DocumentSearch(["patent"],[],{json.dumps(query, ensure_ascii=False)},count=100,page={p},'
               f'date_from={date_from},date_to={date_to})')["data"]["pods"][1]["content"]
        d = c.get("data") if isinstance(c.get("data"), dict) else c
        total = d.get("total_matches") or 0
        batch = d.get("docs") or []
        docs += batch
        if not batch or p * 100 >= total:   # 페이지가 100건보다 짧게 와도 뒤에 더 있을 수 있음
            break
    print(f"특허 '{query}' {date_from}~{date_to}: 전체 {total:,}건 중 {len(docs)}건")
    return docs

def flatten(docs):
    rows = []
    for x in docs:
        p = x.get("patent") or {}
        apps = p.get("applicants") or []
        codes = []
        for a in apps:
            c = BY_CRID.get(str(a.get("company_rid") or "").replace("-", "")) or \
                BY_BRID.get(str(a.get("business_rid") or "").replace("-", ""))
            if c:
                codes.append(c)
        ipc = p.get("ipc_codes") or []
        rows.append({
            "출원일": (p.get("application") or {}).get("date"),
            "출원번호": (p.get("application") or {}).get("uid"),
            "제목": x.get("title"),
            "출원인": ", ".join(a.get("name_ko", "") for a in apps),
            "상장사": ", ".join(NAME[c] for c in dict.fromkeys(codes)),
            "_codes": list(dict.fromkeys(codes)),
            "상태": p.get("registration_status"),
            "IPC": (ipc[0].get("subclass") or {}).get("code") if ipc else None,
            "url": x.get("content_url"),
        })
    return pd.DataFrame(rows)

raw = patent_docs(KEYWORD, YEAR_FROM, YEAR_TO)
pt = flatten(raw)
print(f"받은 {len(pt)}건 중 상장사 출원 {int((pt._codes.str.len() > 0).sum())}건")
pt[["출원일", "제목", "출원인", "상장사", "상태", "IPC"]].head(8)

# %% [markdown]
# ## 3. 상장사 출원인 순위와 등록 상태·IPC 분류

# %%
rank = pt.explode("_codes").dropna(subset=["_codes"]).groupby("_codes").size().sort_values(ascending=False)
rank = pd.DataFrame({"상장사": [NAME[c] for c in rank.index], "시장": [MKT[c] for c in rank.index], "특허 수": rank.values})
print("등록 상태:", pt.상태.value_counts().to_dict())
print("IPC 상위:", pt.IPC.value_counts().head(6).to_dict(), "(H01M = 전지)")
rank.head(12)

# %% [markdown]
# ## 4. 회사별 — 엘지에너지솔루션 특허 월별 추이
# 특허의 `securities.name`에는 공식명이 들어 있어 그대로 지정합니다. 건수 추이는 `DocumentTrends`로 받습니다.

# %%
tr = doc_trends("patent", [], f"securities.name:{COMPANY}", "2024-01-01", ASOF, interval="1M")
tr["월"] = tr.date.dt.strftime("%Y-%m")
ax = tr.plot.bar(x="월", y="count", figsize=(10, 3), legend=False, title=f"{COMPANY} 특허 문서 수(월별, 출원일 기준)")
ax.grid(alpha=.3, axis="y"); plt.show()
print("최근 6개월:", tr.tail(6)[["월", "count"]].values.tolist(), "← 공개 시차로 최근이 적게 보입니다")

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **공개 시차:** 특허는 출원 후 보통 18개월 뒤 공개되므로 최근 1년 출원은 일부만 보입니다. 추이는 2년 전까지가 믿을 만합니다.
# - **출원인 매칭:** 법인번호·사업자번호가 있는 출원인만 상장사로 맞출 수 있습니다. 대학·연구소·개인 출원은 빠집니다.
# - 날짜(`created_at`)는 출원일입니다. 등록 여부는 `patent.registration_status`로 봅니다.
