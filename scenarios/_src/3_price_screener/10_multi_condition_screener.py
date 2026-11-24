# %% [markdown]
# # 3-10 다조건 기업 스크리너 — 시장·밸류에이션·재무 범위 + 산업/사업 키워드
#
# **질문 예시:** "코스피에서 시총 1조 넘고 PBR 0.8 이하, 배당수익률 5% 넘는 종목 찾아줘",
# "영업이익률 15% 넘고 부채비율 100% 이하인 회사 중 '원자력' 사업 하는 곳은?"
#
# DeepSearch 자연어 쿼리는 `(조건) and (조건)` 형태로 여러 조건을 한 번에 걸 수 있습니다.
# 이 노트북은 **조건을 사전으로 적으면 쿼리를 만들어 실행**하고, 결과를 종목 정보·시세와 합쳐 표로 보여 줍니다.
#
# | 조건 | 쿼리 형태 | 입력 단위 |
# |---|---|---|
# | 시장 | `('코스피' 상장 기업)`, 둘 다면 `(('코스피' 상장 기업) or ('코스닥' 상장 기업))` | KOSPI / KOSDAQ / ALL |
# | 거래대금·시가총액 (기준일) | `(a <= 2026-11-24 시가총액 <= b)` | 억 원 |
# | PER·PBR (기준일) | `(a <= 2026-11-24 PER <= b)` | 배 |
# | 배당수익률 (기준일) | `(2026-11-24 배당수익률 >= 5)` | % (값 자체가 퍼센트) |
# | 매출액·영업이익·당기순이익·자산총계 (사업연도) | `(2025 매출액 >= …)` | 억 원 |
# | 영업이익률·당기순이익률 (사업연도) | `(2025 영업이익률 >= 0.15)` | % 입력 → 비율로 변환 |
# | 부채비율 | 쿼리로는 오류 → 부채총계·자본총계를 받아 직접 계산 | % |
# | 산업 키워드 | `('반도체' 산업 기업)` — 표준산업분류 이름 | 문자열 |
# | 사업 키워드 | `SearchCompanyBusinessSummary('원자력', count=50)` — 정기보고서 사업 요약 문장 | 문자열 |
#
# **확인한 제약 (2026-11-25):**
# - 재무 조건은 **연결 기준**입니다(삼성전자·한화·CJ를 `GetFinancialStatements` 연결 값과 대조해 일치). `연결`/`개별`을 쿼리에 넣으면 0건이 되어 별도 기준은 고를 수 없습니다.
# - `DPS/주가`로 배당수익률을 계산하는 옛 문법은 지금 종목명 검색으로 잘못 해석됩니다. `배당수익률`을 쓰세요.
# - 키워드 조건(산업·사업)을 수치 조건과 한 쿼리에 묶으면 `TypeError`가 나는 경우가 있어, **수치 조건과 키워드를 따로 조회해 교집합**합니다.
# - 사업 키워드 검색은 최대 50건(`count` 상한)까지만 봅니다. 흔한 단어는 결과가 잘립니다.

# %%
ASOF = "2026-11-24"   # 시장데이터(시총·PER 등) 기준일
FY = 2025             # 재무 조건의 사업연도

# %% [markdown]
# ## 1. 조건 → 쿼리 만들기
# 범위는 `(최소, 최대)`로 적고, 한쪽만 줄 때는 다른 쪽을 `None`으로 둡니다.

# %%
MARKET_DATA = {"거래대금": "억", "시가총액": "억", "PER": "배", "PBR": "배", "배당수익률": "%그대로"}
FINANCIAL = {"매출액": "억", "영업이익": "억", "당기순이익": "억", "자산총계": "억",
             "영업이익률": "%비율", "당기순이익률": "%비율"}
MARKET_CLAUSE = {"KOSPI": "('코스피' 상장 기업)", "KOSDAQ": "('코스닥' 상장 기업)",
                 "ALL": "(('코스피' 상장 기업) or ('코스닥' 상장 기업))"}


def _conv(v, unit):
    if v is None:
        return None
    if unit == "억":
        return int(v * 100_000_000)
    if unit == "%비율":
        return round(v / 100, 6)
    return v


def _range(label, lo, hi):
    if lo is not None and hi is not None:
        return f"({lo} <= {label} <= {hi})"
    if lo is not None:
        return f"({label} >= {lo})"
    return f"({label} <= {hi})"


def build_query(cond):
    """조건 사전 → 수치 조건 쿼리 문자열. 키워드·부채비율은 run_screen 에서 따로 처리."""
    parts = [MARKET_CLAUSE[cond.get("market", "ALL")]]
    for key, unit in MARKET_DATA.items():
        if key in cond:
            lo, hi = (_conv(x, unit) for x in cond[key])
            parts.append(_range(f"{ASOF} {key}", lo, hi))
    for key, unit in FINANCIAL.items():
        if key in cond:
            lo, hi = (_conv(x, unit) for x in cond[key])
            parts.append(_range(f"{cond.get('fy', FY)} {key}", lo, hi))
    return " and ".join(parts)


build_query({"market": "KOSPI", "시가총액": (10000, None), "PBR": (0.1, 0.8), "배당수익률": (5, None)})

# %% [markdown]
# ## 2. 실행 함수
# 1) 수치 조건 쿼리 → 2) 산업·사업 키워드 쿼리(따로) → 3) 부채비율(부채총계·자본총계로 계산) → 교집합 →
# 4) 일반법인·공기업 보통주만 남기고(ETF·우선주 제외) 기준일 시세를 붙입니다.

# %%
def value_cols(df):
    return [c for c in df.columns if c not in ("date", "symbol", "entity_name", "RowID") and not c.startswith("상장 기업")]


def run_screen(cond, show_query=True):
    steps = []
    q = build_query(cond)
    if show_query:
        print("수치 조건 쿼리:", q)
    base = ds_df(q)
    steps.append(("수치 조건", len(base)))
    if base.empty:
        print("→ 수치 조건에 맞는 종목이 없습니다(또는 조건 문법 오류).")
        return pd.DataFrame()
    keep = base[["symbol"] + value_cols(base)].drop_duplicates("symbol")

    if cond.get("industry_kw"):
        q2 = f"{MARKET_CLAUSE[cond.get('market', 'ALL')]} and ('{cond['industry_kw']}' 산업 기업)"
        ind = ds_df(q2)
        steps.append((f"산업 키워드 '{cond['industry_kw']}'", len(ind)))
        keep = keep[keep.symbol.isin(ind.symbol)]

    if cond.get("business_kw"):
        q3 = f"{MARKET_CLAUSE[cond.get('market', 'ALL')]} and SearchCompanyBusinessSummary('{cond['business_kw']}', count=50)"
        biz = ds_df(q3)
        steps.append((f"사업 키워드 '{cond['business_kw']}'", len(biz)))
        if len(biz) >= 50:
            print("  ⚠ 사업 키워드 결과가 상한(50)에 닿았습니다. 일부 회사가 빠졌을 수 있습니다.")
        keep = keep.merge(biz[["symbol", "summary_title"]].rename(columns={"summary_title": "사업 요약"}),
                          on="symbol", how="inner")

    if "부채비율" in cond:
        lo, hi = cond["부채비율"]
        fy = cond.get("fy", FY)
        debt = ds_df(f"{MARKET_CLAUSE[cond.get('market', 'ALL')]} and ({fy} 부채총계 >= 0) and ({fy} 자본총계 > 0)")
        debt["부채비율(%)"] = debt[f"부채총계 {fy}"] / debt[f"자본총계 {fy}"] * 100
        ok = debt[(debt["부채비율(%)"] >= (lo if lo is not None else -1e18)) &
                  (debt["부채비율(%)"] <= (hi if hi is not None else 1e18))]
        steps.append(("부채비율 (자본잠식 제외)", len(ok)))
        keep = keep.merge(ok[["symbol", "부채비율(%)"]], on="symbol", how="inner")

    snap = all_stocks(ASOF)[["symbol", "name", "market", "industry_name", "close", "market_cap", "value"]]
    out = keep.merge(snap, on="symbol", how="inner")   # 일반법인·공기업 보통주만 남는다
    steps.append(("교집합 → 보통주(ETF·우선주 제외)", len(out)))
    print(" → ".join(f"{a} {b}개" for a, b in steps))
    out = out.rename(columns={"name": "종목", "market": "시장", "industry_name": "업종", "close": "종가"})
    out["시가총액"] = out.pop("market_cap").map(krw)
    out["거래대금(당일)"] = out.pop("value").map(krw)
    out = out.drop(columns=[f"시가총액 {ASOF}", f"거래대금 {ASOF}"], errors="ignore")  # 시세 열과 중복
    for c in list(out.columns):           # 원 단위 금액 열은 읽기 쉽게
        if any(k in c for k in ("매출액", "영업이익 ", "당기순이익 ", "자산총계")):
            out[c] = out[c].map(krw)
        elif "이익률" in c:
            out[c] = (out[c] * 100).round(1).astype(str) + "%"
        elif any(k in c for k in ("PER", "PBR", "배당수익률", "부채비율")):
            out[c] = out[c].astype(float).round(2)
    front = ["종목", "시장", "업종", "종가", "시가총액"]
    return out[front + [c for c in out.columns if c not in front + ["symbol"]]].reset_index(drop=True)


print(PRICE_NOTICE)

# %% [markdown]
# ## 3. 예시 ① 저PBR·고배당 대형주 (코스피)
# 시총 1조 원 이상, PBR 0.1~0.8배, 배당수익률 5% 이상, 흑자(PER > 0).

# %%
r1 = run_screen({"market": "KOSPI", "시가총액": (10000, None), "PBR": (0.1, 0.8),
                 "배당수익률": (5, None), "PER": (0.01, None)})
r1.sort_values(f"배당수익률 {ASOF}", ascending=False).reset_index(drop=True).head(20)

# %% [markdown]
# ## 4. 예시 ② 고마진·저부채 실적주 (코스피+코스닥)
# 당일 거래대금 10억 원 이상, 2025년 매출 1,000억 원 이상·영업이익률 15% 이상·순이익 흑자, 부채비율 100% 이하.

# %%
r2 = run_screen({"market": "ALL", "거래대금": (10, None), "매출액": (1000, None),
                 "영업이익률": (15, None), "당기순이익": (0.01, None), "부채비율": (None, 100)})
print(len(r2), "종목 (영업이익률 높은 순 20개)")
r2.assign(_m=r2[f"영업이익률 {FY}"].str.rstrip("%").astype(float)).sort_values("_m", ascending=False).drop(columns="_m").reset_index(drop=True).head(20)

# %% [markdown]
# ## 5. 예시 ③ 사업 키워드 '원자력' + 흑자 + PBR 1.5배 이하
# 사업 키워드는 회사가 정기보고서에 쓴 **사업 요약 문장**에서 찾습니다. 통계청 업종이 달라도(밸브·정비·건설 등)
# 원전 관련 사업을 적은 회사가 잡힙니다.

# %%
r3 = run_screen({"market": "ALL", "PBR": (None, 1.5), "영업이익": (0.01, None), "business_kw": "원자력"})
r3

# %% [markdown]
# ## 6. 예시 ④ 산업 키워드 '반도체' + PER 0~20배 + 시총 3,000억 이상
# 산업 키워드는 **표준산업분류 이름**에 그 단어가 들어간 회사입니다(예: "다이오드, 트랜지스터 및 유사 반도체소자 제조업").
# 삼성전자처럼 업종명이 다른 회사("통신 및 방송 장비 제조업")는 빠지므로, 넓게 찾으려면 사업 키워드를 쓰세요.

# %%
r4 = run_screen({"market": "ALL", "PER": (0.01, 20), "시가총액": (3000, None), "industry_kw": "반도체"})
r4.sort_values(f"PER {ASOF}").reset_index(drop=True).head(20)

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **PER 조건은 음수(적자)도 포함합니다.** `PER <= 10`만 걸면 적자 기업이 섞이니 최소값(0.01)을 함께 주세요.
# - **재무는 연결 기준, 사업연도 단위**입니다. 분기 실적 조건은 이 쿼리로 걸 수 없습니다.
# - **결과는 현재 상장 종목 기준**이고 시세·거래대금은 KRX 기준입니다(NXT 미포함).
# - 사업 키워드는 최대 50건만 보고, 요약 문장에 단어가 있느냐로 판단하므로 매출 비중은 따로 확인해야 합니다(→ 1-05 사업 프로파일).
