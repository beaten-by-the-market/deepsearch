# %% [markdown]
# # 2-05 공시 본문 — 원문에서 숫자·핵심 뽑아내기
#
# **질문 예시:** "오리온 실적 공시 본문에서 국가별 순매출 뽑아줘", "오늘 공매도 과열 지정 공시들 대상종목·ISIN 정리해줘", "오늘 나온 잠정실적 공시 매출·영업이익 표로 모아줘"
#
# DeepSearch 공시 검색은 **제목·시각·종목·원문 링크**까지만 줍니다(본문 필드 `content`에는 제목만 들어 있음).
# 그래서 이 노트북은 DeepSearch로 공시를 **찾고**, 링크가 가리키는 **KIND(거래소)·DART(금감원) 공개 뷰어 페이지**에서 본문을 직접 받아 표·숫자를 뽑습니다.
# API 키가 필요한 OpenDART는 쓰지 않습니다.
#
# | 링크 | 본문을 받는 경로 (2026-11-25 확인) |
# |---|---|
# | `kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=…` | 뷰어 페이지의 문서번호 → `method=searchContents&docNo=…` → 실제 본문 `.htm` |
# | `dart.fss.or.kr/dsaf001/main.do?rcpNo=…` | 페이지 안 `viewDoc("rcpNo","dcmNo",…)` 인자 → `report/viewer.do?…` 본문 HTML |
#
# CHECK 원본(`2_공시뉴스/05_공시본문`)의 두 예시(오리온 국가별 매출, 공매도 과열 공시 구조화)를 그대로 재현하고, 잠정실적 일괄 추출을 더했습니다.

# %%
ASOF = "2026-11-24"

# %% [markdown]
# ## 본문 받기 함수
# 웹 페이지를 읽는 방식이라 사이트 구조가 바뀌면 깨질 수 있습니다. 요청 사이에 0.3초씩 쉽니다.

# %%
import html as _html, io, re

UA = {"User-Agent": "Mozilla/5.0 (research notebook)"}

def _get(url, **kw):
    time.sleep(0.3)
    r = requests.get(url, headers=UA, timeout=30, **kw)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def kind_html(url):
    page = _get(url)
    doc_no = re.search(r"<option value='(\d+)\|", page).group(1)
    js = _get("https://kind.krx.co.kr/common/disclsviewer.do", params={"method": "searchContents", "docNo": doc_no})
    return _get(re.search(r"setPath\('[^']*','([^']+\.htm)'", js).group(1))

def dart_html(url):
    page = _get(url)
    a = re.search(r'viewDoc\("(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"([^"]*)"', page).groups()
    return _get("https://dart.fss.or.kr/report/viewer.do",
                params=dict(zip(["rcpNo", "dcmNo", "eleId", "offset", "length", "dtd"], a)))

def body(url):
    """공시 링크 → (본문 텍스트, 표 목록)."""
    h = kind_html(url) if "kind.krx.co.kr" in url else dart_html(url)
    try:
        tables = pd.read_html(io.StringIO(h))
    except ValueError:
        tables = []
    t = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    t = re.sub(r"<br\s*/?>|</p>|</tr>", "\n", t)
    t = _html.unescape(_html.unescape(re.sub(r"<[^>]+>", " ", t)))   # 본문에 &amp;nbsp; 처럼 두 번 인코딩된 곳이 있다
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip(), tables

# %% [markdown]
# ## 1. 오리온 실적 공시 → 국가별 순매출
# 오리온은 월별 잠정실적 공시의 "기타 투자판단 사항"에 국가별 매출을 **서술형 표**로 적습니다. 표가 아니라 글이라 정규식으로 뽑습니다.

# %%
total, docs = doc_search("company", ["disclosure"], "securities.name:오리온 and title:잠정", "2026-06-01", "2026-06-30", count=10)
doc = docs.sort_values("created_at").iloc[-1]
print(doc["created_at"], doc["title"], doc["url"])
text, tables = body(doc["url"])

def country_sales(text):
    out = {}
    for block in re.finditer(r"(\d{4}년 \d+월 (?:당월|누계))\s*한국\s*중국\s*베트남\s*러시아\s*합계(.*?)(?=\d{4}년 \d+월 (?:당월|누계)|$)", text, re.S):
        m = re.search(r"순매출\**\s*([-\d,\s]+)", block.group(2))
        nums = [int(x.replace(",", "")) for x in re.findall(r"-?[\d,]+", m.group(1))][:5]
        out[block.group(1)] = nums
    return pd.DataFrame(out, index=["한국", "중국", "베트남", "러시아", "합계"])

sales = country_sales(text)
print("단위: 억원 (순매출)")
sales

# %%
print("합계 검산:", (sales.iloc[:4].sum() == sales.loc["합계"]).to_dict())
fx = re.search(r"환율효과는 다음과 같습니다.*?:\s*(.*?)\s*-\s*\d{4}년", text, re.S)
print("본문의 환율효과:", fx.group(1) if fx else "-")

# %% [markdown]
# ## 2. 공매도 과열종목 지정 공시 → 대상종목·ISIN·지정일 표
# 거래소 공시는 정해진 서식(대상 종목·지정일·시장조치 내용)이라 표가 그대로 읽힙니다.
# DeepSearch 검색 결과에서 **종목 태그가 비어 있던 공시**(주로 우선주)도 본문으로 종목을 채울 수 있습니다.

# %%
total, ov = doc_search("company", ["disclosure"], 'title:"공매도 과열종목 지정"', ASOF, ASOF, count=100)
ov = ov.sort_values("created_at")
print(f"{ASOF} 공매도 과열종목 지정 공시 {total}건, 그중 DeepSearch 종목 태그 없음 {(ov['symbols'] == '').sum()}건")

rows = []
for _, d in ov.iterrows():
    try:
        _, tbs = body(d["url"])
        kv = dict(zip(tbs[0][0], tbs[0][1]))
    except Exception as e:
        rows.append({"공시시각": d["created_at"], "DeepSearch 종목": d["stocks"], "대상 종목": f"(실패: {e})"})
        continue
    target = str(kv.get("대상 종목", ""))
    m = re.match(r"(.+?)\((KR\w{10})\)", target)
    rows.append({"공시시각": d["created_at"].strftime("%H:%M"), "시장": d["publisher"],
                 "DeepSearch 종목": d["stocks"] or "(태그 없음)",
                 "대상 종목": m.group(1) if m else target, "ISIN": m.group(2) if m else "",
                 "지정일(공매도 금지일)": kv.get("지정일", ""),
                 "금지 기간": re.search(r"지정일 (\S+ 간)", str(kv.get("시장조치 내용", ""))).group(1)
                 if re.search(r"지정일 (\S+ 간)", str(kv.get("시장조치 내용", ""))) else ""})
parsed = pd.DataFrame(rows)
parsed

# %% [markdown]
# 지정일은 공시 다음 거래일입니다. 공시가 20시께 나오고 **다음 날 하루** 공매도가 금지된다는 점이 본문으로 확인됩니다(`2-03` 트리거일 정의의 근거).

# %% [markdown]
# ## 3. 같은 날 잠정실적 공시 → 매출·영업이익 한 표
# `영업(잠정)실적(공정공시)`는 대부분 같은 서식(매출액·영업이익·순이익 × 당해실적/누계실적, 당기·전기·전년동기)이라 한꺼번에 뽑을 수 있습니다.
# 회사가 별도 표를 덧붙이거나 서식이 다르면 `파싱 실패`로 남깁니다.

# %%
EARN_DAY = "2026-11-13"     # 3분기 실적 시즌 마지막 주
total, er = doc_search("company", ["disclosure"], "title:영업(잠정)실적", EARN_DAY, EARN_DAY, count=100)
er = er[~er["title"].str.contains("정정") & (er["stocks"] != "")].drop_duplicates("stocks").head(20)
print(f"{EARN_DAY} 잠정실적 공시 {total}건 중 {len(er)}건 본문 추출")

def earnings_table(tables):
    for t in tables:
        if t.shape[1] < 8:
            continue
        cells = [str(x) for x in t.values.ravel() if "단위" in str(x)]       # 예: "단위 : 백만원, %"
        u = cells[0] if cells else ""
        unit = "백만원" if "백만원" in u else ("억원" if "억원" in u else ("원" if "원" in u else None))
        if unit is None:
            continue
        g = t[(t[1].astype(str) == "당해실적") & t[0].isin(["매출액", "영업이익", "당기순이익"])]
        if len(g):
            g = g.drop_duplicates(0).set_index(0)
            return unit, g
    return None, None

def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None

out = []
for _, d in er.iterrows():
    try:
        _, tbs = body(d["url"])
        unit, g = earnings_table(tbs)
    except Exception as e:
        unit, g = None, None
    row = {"종목": d["stocks"].split(", ")[0], "제목": d["title"][:20], "단위": unit or "파싱 실패"}
    if g is not None:
        scale = {"억원": 1, "백만원": 0.01, "원": 1e-8}[unit]
        for k in ("매출액", "영업이익"):
            if k in g.index:
                cur, yoy_base = num(g.loc[k, 2]), num(g.loc[k, 6])
                row[f"{k}(억원)"] = round(cur * scale, 1) if cur is not None else None
                row[f"{k} 전년동기(억원)"] = round(yoy_base * scale, 1) if yoy_base is not None else None
                row[f"{k} YoY(%)"] = num(g.loc[k, 7])
    out.append(row)
earn = pd.DataFrame(out)
print("성공", (earn["단위"] != "파싱 실패").sum(), "/", len(earn))
earn

# %% [markdown]
# ## 결과 읽는 법과 한계
# - **정형 공시(거래소 시장조치, 잠정실적 표준 서식)는 거의 그대로 구조화**됩니다. 서술형 본문(오리온 국가별 매출)은 회사마다 문장 형식이 달라 회사별 정규식이 필요합니다.
# - 본문의 숫자는 **잠정치**입니다. 확정치는 정기보고서나 `GetFinancialStatements`로 교차 확인하세요.
# - KIND·DART 웹 페이지 구조에 기댄 방법입니다. 사이트가 바뀌면 `kind_html`/`dart_html`의 정규식을 고쳐야 합니다. 대량 수집은 하지 말고 필요한 공시만 받으세요.
# - DeepSearch에서 공시 본문 자체는 받을 수 없습니다(`DocumentSearch`의 `content`는 제목만, `read_document.py`도 DART 프레임 구조 때문에 본문이 거의 안 나옴).
