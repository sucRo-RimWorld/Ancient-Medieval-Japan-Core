#!/usr/bin/env python3
"""Validate that an AMJ Workshop cover preserves every locked common pixel."""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from PIL import Image

CANVAS = (960, 540)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cover", type=Path)
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--mask", type=Path, required=True)
    args=ap.parse_args()

    cover=Image.open(args.cover).convert("RGB")
    base=Image.open(args.base).convert("RGB")
    mask=Image.open(args.mask).convert("L")
    if cover.size != CANVAS:
        print(f"[FAIL] cover dimensions {cover.size}; expected {CANVAS}")
        return 1
    if base.size != CANVAS or mask.size != CANVAS:
        print("[FAIL] canonical base or mask has unexpected dimensions")
        return 1

    ca=np.asarray(cover)
    ba=np.asarray(base)
    locked=np.asarray(mask)==0
    diff=np.any(ca != ba, axis=2) & locked
    count=int(diff.sum())
    if count:
        ys,xs=np.where(diff)
        print(f"[FAIL] {count} locked common pixels differ; first mismatch x={int(xs[0])}, y={int(ys[0])}")
        return 1
    print("[OK] Workshop cover preserves every locked common pixel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
