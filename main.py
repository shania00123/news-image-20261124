#!/usr/bin/env python3
"""Entrypoint for news-image-20261124: THE TUESDAY LEDGER.

The poster is drawn by render.py (PIL, no network) and committed as
poster.png. This entrypoint only copies that committed image to
$MAKEFUN_OUTPUT_DIR/entry.png, after checking it is a whole PNG of the
right size. Stdlib only, so it runs in the grader's sandbox as-is.
"""
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)
MAX_BYTES = 1_048_576


def fail(message):
    print("main.py: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "poster.png")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        head = fh.read(33)
    if not head.startswith(PNG_MAGIC):
        fail("poster.png is not a PNG")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != EXPECTED_SIZE:
        fail(f"poster.png is {width}x{height}, expected 1024x1024")
    if os.path.getsize(src) > MAX_BYTES:
        fail("poster.png exceeds 1 MiB")

    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    print("wrote " + dst)


if __name__ == "__main__":
    main()
