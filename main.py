#!/usr/bin/env python3
"""news-image-20261124 v2 — entrypoint.

Copies the poster this repository ships (poster.png, drawn by render.py)
to the output directory as entry.png. Standard library only, no network,
no randomness: two runs write identical bytes.

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
It is never a relative folder: the grader reads /output/entry.png.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER = os.path.join(HERE, "poster.png")
MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    with open(POSTER, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print("poster.png is %d bytes, over the 1 MiB limit" % len(data),
              file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("poster.png is not a PNG", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print("poster.png is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    with open(target, "rb") as fh:
        if fh.read() != data:
            print("read-back mismatch on %s" % target, file=sys.stderr)
            return 1
    print("wrote %s (%d bytes)" % (target, len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
