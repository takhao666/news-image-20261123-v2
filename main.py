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
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _png_dimensions(path):
    """Parse the IHDR chunk and return (width, height)."""
    data = Path(path).read_bytes()
    if data[:8] != PNG_MAGIC:
        raise SystemExit(f"refusing to copy: {path} is not a PNG")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit(f"refusing to copy: {path} has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    if not SRC.is_file():
        raise SystemExit(f"missing source image: {SRC}")
    if SRC.stat().st_size == 0:
        raise SystemExit(f"empty source image: {SRC}")
    width, height = _png_dimensions(SRC)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"unexpected dimensions: {SRC} is {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    if not dest.is_file() or dest.stat().st_size == 0:
        raise SystemExit(f"copy failed: {dest} missing or empty")
    if _sha256(dest) != _sha256(SRC):
        raise SystemExit(f"copy mismatch: {dest} differs from {SRC}")
    print(f"wrote {dest} ({dest.stat().st_size} bytes, "
          f"{width}x{height}, sha256 {_sha256(dest)[:16]}...)")


if __name__ == "__main__":
    main()
