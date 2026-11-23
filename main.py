#!/usr/bin/env python3
"""Runner for THE MONDAY GLOBE, Monday 23 November 2026.

This is only the launcher. The page itself is drawn by render.py
(build_front_page), which uses PIL and nothing else: no network, no
clock, no randomness, so every run produces the same PNG bytes.

The destination defaults to /output/entry.png. A first positional
argument overrides it; otherwise the MAKEFUN_OUTPUT_DIR environment
variable, when set, supplies the folder instead.
"""

import os
import sys
from pathlib import Path

FALLBACK_DIR = Path("/output")
IMAGE_NAME = "entry.png"


def pick_destination(argv):
    """Decide where the finished page goes."""
    if len(argv) > 1:
        given = Path(argv[1])
        if given.is_dir():
            return given / IMAGE_NAME
        return given
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if folder:
        return Path(folder) / IMAGE_NAME
    return FALLBACK_DIR / IMAGE_NAME


def render_page(destination):
    """Ask render.py to draw the page and report the file size."""
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    import render

    destination.parent.mkdir(parents=True, exist_ok=True)
    render.build_front_page(str(destination))
    size = destination.stat().st_size
    print(f"front page done -> {destination} [{size} bytes]")
    return 0


def main(argv):
    try:
        target = pick_destination(argv)
    except (TypeError, ValueError) as problem:
        print(f"bad output path: {problem}", file=sys.stderr)
        return 2
    try:
        return render_page(target)
    except OSError as problem:
        print(f"could not write the page: {problem}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
