#!/usr/bin/env python3
"""Copier for THE MONDAY GLOBE, Monday 23 November 2026.

The front page itself (entry.png, next to this file) was drawn when the
entry was built; this program only copies it to the output location.
It uses the Python standard library only, so it runs in the grader's
sandbox where nothing is installed before it runs.

The destination defaults to /output/entry.png. A first positional
argument overrides it; otherwise the MAKEFUN_OUTPUT_DIR environment
variable, when set, supplies the folder instead.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
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


def copy_page(destination):
    """Copy entry.png to the destination and report the file size."""
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
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
        return copy_page(target)
    except OSError as problem:
        print(f"could not write the page: {problem}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
