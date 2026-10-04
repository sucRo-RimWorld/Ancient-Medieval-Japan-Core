#!/usr/bin/env python3
"""Regression check for the deterministic AMJ Workshop cover compositor."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/"Scripts"/"build_workshop_cover.py"
VALIDATE=ROOT/"Scripts"/"validate_workshop_cover.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # Synthetic canonical assets let the regression test run without private Library access.
        base=Image.new("RGB",(960,540),(241,232,215))
        ImageDraw.Draw(base).rectangle((20,20,300,350), fill=(30,45,40))
        base_path=td/"base.png"; base.save(base_path)
        mask=Image.new("L",(960,540),0)
        md=ImageDraw.Draw(mask)
        md.rectangle((330,0,959,539),fill=255)
        md.rectangle((66,378,310,426),fill=255)
        mask_path=td/"mask.png"; mask.save(mask_path)

        # Deliberately hostile full-canvas layer: the hard mask must protect the common area.
        hostile=Image.new("RGBA",(960,540),(255,0,255,255))
        hostile_path=td/"hostile.png"; hostile.save(hostile_path)
        out=td/"cover.png"
        subprocess.run([
            sys.executable,str(BUILD),"--base",str(base_path),"--mask",str(mask_path),
            "--right-layer",str(hostile_path),"--addon","Test","--output",str(out),"--mode","canvas"
        ],check=True)
        subprocess.run([
            sys.executable,str(VALIDATE),str(out),"--base",str(base_path),"--mask",str(mask_path)
        ],check=True)

        final=np.asarray(Image.open(out).convert("RGB"))
        b=np.asarray(base)
        m=np.asarray(mask)==0
        assert np.array_equal(final[m],b[m]), "locked pixels changed"
        assert np.any(final[:,400:,:] != b[:,400:,:]), "variable region did not change"
    print("[OK] Workshop cover template regression test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
