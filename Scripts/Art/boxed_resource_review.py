"""Render a boxed-resource comparison using only the manifest-registered reference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_registered_reference(manifest_path: Path):
    spec = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = spec["representative_final"]
    ref = (manifest_path.parent / entry["path"]).resolve()
    if not ref.is_file():
        raise FileNotFoundError(f"registered reference missing: {ref}")
    actual = sha256(ref)
    if actual != entry["sha256"]:
        raise ValueError(f"registered reference SHA-256 mismatch: {actual} != {entry['sha256']}")
    with Image.open(ref) as image:
        image.load()
        reference = image.convert("RGBA")
    if reference.size != tuple(spec["size"]):
        raise ValueError("registered reference size does not match template size")
    return spec, ref, reference


def render_review(manifest_path: Path, candidate_path: Path, output_path: Path):
    spec, ref_path, reference = load_registered_reference(manifest_path)
    with Image.open(candidate_path) as image:
        image.load()
        candidate = image.convert("RGBA")
    if candidate.size != tuple(spec["size"]):
        raise ValueError("candidate must already match the registered template canvas")

    width, height = spec["size"]
    small = 64
    footer = 92
    canvas = Image.new("RGBA", (width * 2, height + footer), (28, 28, 28, 255))
    canvas.alpha_composite(reference, (0, 0))
    canvas.alpha_composite(candidate, (width, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text((8, height + 6), "REGISTERED REFERENCE", fill=(255, 255, 255, 255))
    draw.text((width + 8, height + 6), "CANDIDATE", fill=(255, 255, 255, 255))
    canvas.alpha_composite(reference.resize((small, small), Image.Resampling.LANCZOS), ((width-small)//2, height+26))
    canvas.alpha_composite(candidate.resize((small, small), Image.Resampling.LANCZOS), (width+(width-small)//2, height+26))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG")
    print(f"PASS: registered reference verified: {ref_path}")
    print(f"PASS: registered reference SHA-256: {sha256(ref_path)}")
    print(f"PASS: review written: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render_review(args.manifest, args.candidate, args.output)


if __name__ == "__main__":
    main()
