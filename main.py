#!/usr/bin/env python3
"""Harness entry point for this news-image submission.

The front page is pre-rendered by generate.py (run it first to rebuild
entry.png). This file only copies those exact bytes to the directory the
harness names, so the image the judges see is the one that was reviewed.
Standard library only — the grading environment has no PIL.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not outdir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    src = os.path.join(HERE, "entry.png")
    if not os.path.exists(src):
        print("entry.png missing: run python3 generate.py first",
              file=sys.stderr)
        return 1
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
