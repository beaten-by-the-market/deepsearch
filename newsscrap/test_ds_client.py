"""
ds_client.py 스모크 테스트 — 핸드오프 부록 A 쿼리 재현.

검증 목표:
  1. `_windows`가 2년 범위를 ≤1년 청크 2개로 분할한다 (네트워크 불필요).
  2. `유한양행 배당`이 1년 윈도우(2023)에서 docs를 반환한다.
  3. **2년 윈도우(2023~2024)가 자동 분할되어 성공**한다(RequestEntityTooLarge 미발생).

⚠️ Windows 콘솔은 CP949라 한글이 깨지므로, 결과 본문은 UTF-8 파일
   (test_ds_client_output.txt)로 덤프해 확인한다. 콘솔에는 ASCII 요약만 출력.

실행:
    python newsscrap/test_ds_client.py
    (newsscrap/.env의 API_KEY 사용. 네트워크 필요.)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds_client

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "test_ds_client_output.txt")


def main():
    lines = []  # UTF-8 파일로 덤프할 상세 로그

    def log(msg):
        print(msg)              # 콘솔: ASCII 요약
        lines.append(str(msg))

    def dump(msg):
        lines.append(str(msg))  # 파일 전용(한글 포함)

    ok = True

    # ── 1. _windows 분할 (네트워크 불필요) ────────────────────────────────
    spans = ds_client._windows("20230101", "20241231")
    log(f"[1] _windows(2023~2024) -> {len(spans)} chunk(s)")
    dump(f"    spans={spans}")
    assert len(spans) == 2, f"2년은 2분할이어야 함, got {len(spans)}"
    assert spans[0] == ("20230101", "20231231")
    assert spans[1] == ("20240101", "20241231")
    log("    PASS: 2-year range split into 2 windows")

    # ── 2. 1년 윈도우: docs 반환 ──────────────────────────────────────────
    try:
        docs1, total1 = ds_client.document_search(
            "securities.name:유한양행 and 배당",
            date_from="20230101", date_to="20231231", count=3)
        log(f"[2] 1-year window: docs={len(docs1)} total={total1}")
        dump("    --- sample docs (1y) ---")
        for d in docs1[:3]:
            dump(f"    - {d.get('created_at','')} | {d.get('publisher','')} | {d.get('title','')}")
        if len(docs1) > 0 and total1 > 0:
            log("    PASS: 1-year window returned docs")
        else:
            log("    WARN: 1-year window returned 0 docs (데이터 변동 가능)")
    except Exception as e:
        ok = False
        log(f"    FAIL: 1-year window raised: {type(e).__name__}")
        dump(f"    error: {e}")

    # ── 3. 2년 윈도우: 자동 분할로 성공(예외 없이 docs 병합) ──────────────
    try:
        docs2, total2 = ds_client.document_search(
            "securities.name:유한양행 and 배당",
            date_from="20230101", date_to="20241231", count=3)
        log(f"[3] 2-year window (auto-split): docs={len(docs2)} total={total2}")
        dump("    --- sample docs (2y, merged & deduped) ---")
        for d in docs2[:5]:
            dump(f"    - {d.get('created_at','')} | {d.get('publisher','')} | {d.get('title','')}")
        # 핵심: RequestEntityTooLarge 없이 성공 + 1년치보다 많거나 같음
        if total2 >= total1:
            log("    PASS: 2-year auto-split succeeded (no RequestEntityTooLarge)")
        else:
            log("    WARN: 2-year total < 1-year total (데이터 변동 가능)")
    except Exception as e:
        ok = False
        log(f"    FAIL: 2-year window raised: {type(e).__name__}")
        dump(f"    error: {e}")

    # ── 결과를 UTF-8 파일로 덤프 (한글 확인용) ────────────────────────────
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"\n[output] UTF-8 dump -> {OUT_PATH}")
    log("RESULT: " + ("ALL PASS" if ok else "FAILURES PRESENT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
