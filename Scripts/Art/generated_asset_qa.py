#!/usr/bin/env python3
"""Mechanical QA for generated AMJ image candidates.

This validator checks only measurable image properties. Subject identity,
historical fit, semantic composition, and final author approval remain visual
review responsibilities outside this script.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageChops, ImageFilter, ImageOps


def _pixels(image: Image.Image) -> list[Any]:
    getter = getattr(image, "get_flattened_data", None)
    if getter is not None:
        return list(getter())
    return list(image.getdata())


def _normalized_crop(image: Image.Image, size: int = 256, fill: float = 0.90) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    crop = rgba.crop(bbox)
    scale = (size * fill) / max(crop.size)
    resized = crop.resize(
        (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(
        resized,
        ((size - resized.width) // 2, (size - resized.height) // 2),
    )
    return canvas


def _fraction(values: Iterable[int], predicate) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(1 for value in values if predicate(value)) / len(values)


def _percentile(values: Iterable[int], q: float) -> int:
    ordered = sorted(values)
    if not ordered:
        return 0
    index = min(len(ordered) - 1, max(0, int(q * (len(ordered) - 1))))
    return ordered[index]


def analyze(path: Path) -> dict[str, Any]:
    with Image.open(path) as opened:
        opened.load()
        source_format = opened.format or "UNKNOWN"
        rgba = opened.convert("RGBA")

    total = rgba.width * rgba.height
    alpha = rgba.getchannel("A")
    alpha_hist = alpha.histogram()
    bbox = alpha.getbbox()

    metrics: dict[str, Any] = {
        "format": source_format,
        "width": rgba.width,
        "height": rgba.height,
        "transparent_fraction": alpha_hist[0] / total,
        "low_alpha_fraction_1_39": sum(alpha_hist[1:40]) / total,
        "opaque_fraction_180_255": sum(alpha_hist[180:]) / total,
        "visible_bbox": list(bbox) if bbox else [],
    }

    if bbox is None:
        metrics.update(
            {
                "coarse_color_bins_16_at_64": 0,
                "strong_edge_density_at_64": 0.0,
                "outer_dark_fraction_lt80": 0.0,
                "internal_dark_edge_fraction_lt140": 1.0,
                "internal_very_dark_edge_fraction_lt100": 1.0,
                "line_hierarchy_ratio": 0.0,
            }
        )
        return metrics

    normalized = _normalized_crop(rgba)
    preview = normalized.resize((64, 64), Image.Resampling.LANCZOS)
    preview_alpha = preview.getchannel("A")
    preview_rgb = preview.convert("RGB")

    coarse_bins = {
        (r // 16, g // 16, b // 16)
        for (r, g, b), a in zip(_pixels(preview_rgb), _pixels(preview_alpha))
        if a >= 128
    }
    metrics["coarse_color_bins_16_at_64"] = len(coarse_bins)

    preview_luma = ImageOps.grayscale(preview_rgb)
    preview_edges = preview_luma.filter(ImageFilter.FIND_EDGES)
    edge_values = [
        edge
        for edge, a in zip(_pixels(preview_edges), _pixels(preview_alpha))
        if a >= 128
    ]
    metrics["strong_edge_density_at_64"] = _fraction(edge_values, lambda x: x >= 70)

    alpha_256 = normalized.getchannel("A")
    mask = alpha_256.point(lambda x: 255 if x >= 180 else 0)
    eroded = mask.filter(ImageFilter.MinFilter(7))
    outer_band = ImageChops.subtract(mask, eroded)
    inner_mask = eroded.filter(ImageFilter.MinFilter(9))

    luma_256 = ImageOps.grayscale(normalized.convert("RGB"))
    edges_256 = luma_256.filter(ImageFilter.FIND_EDGES)

    alpha_values = _pixels(alpha_256)
    luma_values = _pixels(luma_256)
    outer_values = _pixels(outer_band)
    inner_values = _pixels(inner_mask)
    edge256_values = _pixels(edges_256)

    outer_luma = [
        luma
        for luma, a, flag in zip(luma_values, alpha_values, outer_values)
        if flag and a >= 220
    ]
    internal_pairs = [
        (edge, luma)
        for edge, luma, a, flag in zip(
            edge256_values, luma_values, alpha_values, inner_values
        )
        if flag and a >= 220
    ]
    edge_threshold = max(15, _percentile((edge for edge, _ in internal_pairs), 0.80))
    internal_edge_luma = [
        luma for edge, luma in internal_pairs if edge >= edge_threshold
    ]

    outer_dark = _fraction(outer_luma, lambda x: x < 80)
    internal_dark = _fraction(internal_edge_luma, lambda x: x < 140)
    internal_very_dark = _fraction(internal_edge_luma, lambda x: x < 100)

    metrics["outer_dark_fraction_lt80"] = outer_dark
    metrics["internal_dark_edge_fraction_lt140"] = internal_dark
    metrics["internal_very_dark_edge_fraction_lt100"] = internal_very_dark
    metrics["line_hierarchy_ratio"] = outer_dark / max(internal_dark, 1e-6)
    return metrics


def validate(path: Path, policy_path: Path) -> dict[str, Any]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    metrics = analyze(path)
    failures: list[str] = []

    allowed_formats = policy.get("allowed_formats")
    if allowed_formats and metrics["format"] not in allowed_formats:
        failures.append(
            f"format={metrics['format']} not in allowed formats {allowed_formats}"
        )

    if policy.get("require_visible_content", True) and not metrics["visible_bbox"]:
        failures.append("candidate has no visible content")

    # Color/edge/outline ratios are diagnostics, never pass/fail style gates.
    # Arbitrary global thresholds reject valid art and cannot verify aesthetics.
    if policy.get("require_transparency", False) and metrics["transparent_fraction"] == 0:
        failures.append("candidate has no transparent background")

    return {
        "passed": not failures,
        "failures": failures,
        "metrics": metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    result = validate(args.candidate, args.policy)
    payload = {
        **result,
        "candidate": str(args.candidate),
        "policy": str(args.policy),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if result["passed"]:
        print("PASS: generated candidate mechanical QA")
    else:
        print("FAIL: generated candidate mechanical QA")
        for failure in result["failures"]:
            print(f"- {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
