#!/usr/bin/env python3
"""Entry point for the 23 November 2026 front page.

Renders the newspaper image with render.build_front_page and writes it to
/output/entry.png (or to the path given as the first argument). No network,
no clock: the output is fully deterministic.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import build_front_page


def main(argv):
    out = argv[1] if len(argv) > 1 else "/output/entry.png"
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    build_front_page(out)
    with open(out, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(out)
    print(f"wrote {out}  {size} bytes  sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
