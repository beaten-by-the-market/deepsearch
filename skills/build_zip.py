"""
skills/deepsearch → dist/deepsearch.zip 빌드.

배포 zip은 손으로 만들지 말고 이 스크립트로 생성한다 (소스와 zip 불일치 방지).

실행:
    python skills/build_zip.py
"""

import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "skills", "deepsearch")
OUT_PATH = os.path.join(ROOT, "dist", "deepsearch.zip")

EXCLUDE_DIRS = {"__pycache__"}
EXCLUDE_EXTS = {".pyc"}


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    count = 0
    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(SKILL_DIR):
            dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
            for name in sorted(filenames):
                if os.path.splitext(name)[1] in EXCLUDE_EXTS:
                    continue
                path = os.path.join(dirpath, name)
                # zip 내부 경로는 deepsearch/... 형태 (압축 해제 시 스킬 폴더 그대로)
                arcname = os.path.relpath(path, os.path.dirname(SKILL_DIR)).replace(os.sep, "/")
                zf.write(path, arcname)
                count += 1
    print(f"{count} files -> {os.path.relpath(OUT_PATH, ROOT)}")


if __name__ == "__main__":
    main()
