#!/usr/bin/env python3
"""Deterministically compose an AMJ Workshop cover.

Image generation supplies only the addon-specific right-side artwork. The shared AMJ
series area comes from the canonical raster template and is forcibly restored after
composition so a generated layer cannot alter locked pixels.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CANVAS = (960, 540)
RIGHT_BOX = (330, 10, 950, 532)
LABEL_BOX = (66, 378, 310, 426)
LABEL_FILL = (83, 85, 76, 255)
DEFAULT_TRACKING = 9


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
        Path(r"C:\\Windows\\Fonts\\times.ttf"),
        Path(r"C:\\Windows\\Fonts\\georgia.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def tracked_metrics(draw: ImageDraw.ImageDraw, text: str, font, tracking: int) -> tuple[float, int]:
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + max(0, len(text) - 1) * tracking
    bbox = font.getbbox("Ag")
    return total, bbox[3] - bbox[1]


def draw_addon_name(image: Image.Image, text: str) -> None:
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = LABEL_BOX
    chosen = None
    for size in range(38, 17, -1):
        tracking = max(3, round(DEFAULT_TRACKING * size / 38))
        font = find_font(size)
        total, height = tracked_metrics(draw, text, font, tracking)
        if total <= (x1 - x0 - 6) and height <= (y1 - y0 - 4):
            chosen = (font, tracking, total)
            break
    if chosen is None:
        font = find_font(18)
        tracking = 3
        total, _ = tracked_metrics(draw, text, font, tracking)
    else:
        font, tracking, total = chosen

    bbox = font.getbbox("Ag")
    glyph_h = bbox[3] - bbox[1]
    x = x0 + ((x1 - x0) - total) / 2
    y = y0 + ((y1 - y0) - glyph_h) / 2 - bbox[1]
    for ch in text:
        draw.text((x, y), ch, font=font, fill=LABEL_FILL)
        x += draw.textlength(ch, font=font) + tracking


def place_right_layer(layer: Image.Image, mode: str) -> Image.Image:
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    if mode == "canvas":
        if layer.size != CANVAS:
            layer = layer.resize(CANVAS, Image.Resampling.LANCZOS)
        out.alpha_composite(layer, (0, 0))
        return out

    x0, y0, x1, y1 = RIGHT_BOX
    max_w, max_h = x1 - x0, y1 - y0
    lw, lh = layer.size
    if lw <= 0 or lh <= 0:
        raise ValueError("right layer has invalid dimensions")
    scale = min(max_w / lw, max_h / lh)
    new_size = (max(1, round(lw * scale)), max(1, round(lh * scale)))
    resized = layer.resize(new_size, Image.Resampling.LANCZOS)
    px = x0 + (max_w - new_size[0]) // 2
    py = y0 + (max_h - new_size[1]) // 2
    out.alpha_composite(resized, (px, py))
    return out


def build(base_path: Path, mask_path: Path, right_path: Path, addon: str, output: Path, mode: str) -> None:
    base = load_rgba(base_path)
    mask = Image.open(mask_path).convert("L")
    if base.size != CANVAS or mask.size != CANVAS:
        raise ValueError(f"canonical base/mask must be {CANVAS}, got {base.size}/{mask.size}")

    right = load_rgba(right_path)
    composed = base.copy()
    composed.alpha_composite(place_right_layer(right, mode))
    draw_addon_name(composed, addon)

    # Hard guarantee: all black-mask pixels come back from the canonical base.
    final = Image.composite(composed, base, mask)
    output.parent.mkdir(parents=True, exist_ok=True)
    final.convert("RGB").save(output, format="PNG", optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True, help="materialized canonical common base from the AMJ Library")
    ap.add_argument("--mask", type=Path, required=True, help="materialized canonical variable mask from the AMJ Library")
    ap.add_argument("--right-layer", type=Path, required=True, help="addon-specific PNG; transparent background strongly preferred")
    ap.add_argument("--addon", required=True, help="display label, e.g. Fermentation")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--mode", choices=("fit", "canvas"), default="fit", help="fit artwork into right box or treat it as a full 960x540 canvas")
    args = ap.parse_args()
    build(args.base, args.mask, args.right_layer, args.addon, args.output, args.mode)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
