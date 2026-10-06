#!/usr/bin/env python3
"""Validate that an AMJ Workshop cover preserves every locked common pixel."""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageChops

CANVAS = (960, 540)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cover", type=Path)
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--mask", type=Path, required=True)
    args = ap.parse_args()

    cover = Image.open(args.cover).convert("RGB")
    base = Image.open(args.base).convert("RGB")
    mask = Image.open(args.mask).convert("L")
    if cover.size != CANVAS:
        print(f"[FAIL] cover dimensions {cover.size}; expected {CANVAS}")
        return 1
    if base.size != CANVAS or mask.size != CANVAS:
        print("[FAIL] canonical base or mask has unexpected dimensions")
        return 1

    diff = ImageChops.difference(cover, base)
    locked_mask = mask.point(lambda p: 255 if p == 0 else 0)
    locked_diff = Image.composite(diff, Image.new("RGB", CANVAS), locked_mask)
    bbox = locked_diff.getbbox()
    if bbox:
        count = 0
        first = None
        for y in range(CANVAS[1]):
            for x in range(CANVAS[0]):
                if locked_diff.getpixel((x, y)) != (0, 0, 0):
                    count += 1
                    if first is None:
                        first = (x, y)
        print(f"[FAIL] {count} locked common pixels differ; first mismatch x={first[0]}, y={first[1]}")
        return 1

    print("[OK] Workshop cover preserves every locked common pixel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
