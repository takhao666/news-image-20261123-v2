#!/usr/bin/env python3
"""Entry point for make.fun bounty news-image-20261123.

Writes the 23 November 2026 world-news front page to /output/entry.png.
The image is drawn by render.py (Pillow, offline) and shipped in this
repository as entry.png; this program only copies it, so it is fully
deterministic, needs no network, and uses only the standard library.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    if SRC.read_bytes()[:8] != PNG_MAGIC:
        raise SystemExit(f"refusing to copy: {SRC} is not a PNG")
    shutil.copyfile(SRC, dest)
    if _sha256(dest) != _sha256(SRC):
        raise SystemExit(f"copy mismatch: {dest} differs from {SRC}")
    print(f"wrote {dest} ({dest.stat().st_size} bytes, "
          f"sha256 {_sha256(dest)[:16]}...)")


if __name__ == "__main__":
    main()
