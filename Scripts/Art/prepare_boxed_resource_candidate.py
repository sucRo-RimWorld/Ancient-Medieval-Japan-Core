#!/usr/bin/env python3
"""Prepare an AMJ boxed-resource ImageGen candidate for final visual review.

The script runs raw mechanical QA, applies deterministic masu-plane projection,
runs post-projection PNG/alpha integrity QA, and writes a compact review sheet. Semantic
visual QA (subject identity/style/forbidden objects) is still performed by the
agent before the sheet is shown to the author.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


qa = _load("generated_asset_qa", HERE / "generated_asset_qa.py")
normalizer = _load("normalize_masu_contents", HERE / "normalize_masu_contents.py")


def _fit(image: Image.Image, box: tuple[int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    canvas = Image.new("RGBA", box, (38, 38, 38, 255))
    thumb = ImageOps.contain(
        rgba, (box[0] - 24, box[1] - 48), Image.Resampling.LANCZOS
    )
    canvas.alpha_composite(
        thumb,
        ((box[0] - thumb.width) // 2, 30 + (box[1] - 48 - thumb.height) // 2),
    )
    return canvas


def _review_sheet(raw_path: Path, projected_path: Path, output: Path) -> None:
    with Image.open(raw_path) as raw_opened, Image.open(projected_path) as projected_opened:
        raw_opened.load()
        projected_opened.load()
        raw = raw_opened.convert("RGBA")
        projected = projected_opened.convert("RGBA")

    panel = (420, 420)
    canvas = Image.new("RGBA", (panel[0] * 3, panel[1]), (28, 28, 28, 255))
    draw = ImageDraw.Draw(canvas)

    raw_panel = _fit(raw, panel)
    projected_panel = _fit(projected, panel)
    small = projected.resize((64, 64), Image.Resampling.LANCZOS)
    small_panel = Image.new("RGBA", panel, (38, 38, 38, 255))
    enlarged = small.resize((256, 256), Image.Resampling.NEAREST)
    small_panel.alpha_composite(enlarged, ((panel[0] - 256) // 2, 90))

    canvas.alpha_composite(raw_panel, (0, 0))
    canvas.alpha_composite(projected_panel, (panel[0], 0))
    canvas.alpha_composite(small_panel, (panel[0] * 2, 0))
    draw.text((12, 10), "RAW CONTENTS", fill=(255, 255, 255, 255))
    draw.text(
        (panel[0] + 12, 10),
        "PROJECTED CONTENTS",
        fill=(255, 255, 255, 255),
    )
    draw.text(
        (panel[0] * 2 + 12, 10),
        "64 PX CHECK (8x)",
        fill=(255, 255, 255, 255),
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG")


def prepare(source: Path, output_dir: Path, policy: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_report_path = output_dir / "mechanical-qa-raw.json"
    projected_report_path = output_dir / "mechanical-qa-projected.json"
    projected_path = output_dir / "contents-projected.png"
    review_path = output_dir / "review-sheet.png"

    raw_result = qa.validate(source, policy)
    raw_report_path.write_text(
        json.dumps(raw_result, indent=2), encoding="utf-8"
    )
    if not raw_result["passed"]:
        raise ValueError(
            "raw candidate failed mechanical QA: "
            + "; ".join(raw_result["failures"])
        )

    normalizer.normalize(source, projected_path)

    # Verify the derivative is still a valid, non-empty transparent PNG.
    # Its canvas occupancy and antialiasing are subject-dependent.
    projected_result = qa.validate(projected_path, policy)
    projected_report_path.write_text(
        json.dumps(projected_result, indent=2), encoding="utf-8"
    )
    if not projected_result["passed"]:
        raise ValueError(
            "projected candidate failed structural QA: "
            + "; ".join(projected_result["failures"])
        )

    _review_sheet(source, projected_path, review_path)
    summary = {
        "passed": True,
        "raw_source": str(source),
        "projected": str(projected_path),
        "review_sheet": str(review_path),
        "raw_report": str(raw_report_path),
        "projected_report": str(projected_report_path),
        "next_gate": (
            "agent semantic visual QA, then author final visual approval"
        ),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--policy",
        type=Path,
        default=ROOT / "Docs/References/AMJ_BoxedResource_GenerationQA.json",
    )
    args = parser.parse_args()
    summary = prepare(args.source, args.output_dir, args.policy)
    print("PASS: boxed-resource candidate prepared")
    print(summary["review_sheet"])


if __name__ == "__main__":
    main()
