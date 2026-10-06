"""Build deterministic v4-contact-study artifacts from existing AMJ resource art.

This is a study-only renderer. It never writes into Textures or Docs/References,
never changes the registered masks, and never enables production.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

import boxed_resource_review
import fixed_template

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "Docs/References/AMJ_Masu_Template.json"
OUT = ROOT / "build/masu-contact-study"

MILLET_ROOT = ROOT / "Textures/Things/Item/Resource/AMJC_Millet"
BUCKWHEAT_ROOT = ROOT / "Textures/Things/Item/Resource/AMJC_Buckwheat"


def crop_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("source asset is fully transparent")
    return rgba.crop(bbox)


def transformed(path: Path, width: int, angle: float = 0.0) -> Image.Image:
    with Image.open(path) as image:
        source = crop_alpha(image)
    height = max(1, round(source.height * width / source.width))
    source = source.resize((width, height), Image.Resampling.LANCZOS)
    if angle:
        source = source.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    return source


def place(canvas: Image.Image, object_image: Image.Image, center: tuple[int, int]) -> None:
    x = round(center[0] - object_image.width / 2)
    y = round(center[1] - object_image.height / 2)
    # Keep the full object rectangle inside the registered independent extension
    # rectangle. We deliberately do not crop a leaking object into compliance.
    if x < 8 or y < 8 or x + object_image.width > 248 or y + object_image.height > 196:
        raise ValueError(
            f"study placement exceeds ExtensionAllowed rectangle: "
            f"{(x, y, x + object_image.width, y + object_image.height)}"
        )
    canvas.alpha_composite(object_image, (x, y))


def contact_shadow(canvas: Image.Image, box: tuple[int, int, int, int]) -> None:
    # A small, content-local contact shadow is part of the rendered context.
    # The coordinates stay inside the visible/contact region; this is not a mask.
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse(box, fill=(44, 25, 16, 54))
    canvas.alpha_composite(overlay)


def diagnostic_restore(master: Image.Image, hard_fixed: Image.Image, context: Image.Image) -> Image.Image:
    # Exact same final operation as fixed_template.compose for the contact model.
    return Image.composite(master, context, hard_fixed)


def metrics(master: Image.Image, candidate: Image.Image, masks: dict[str, Image.Image], required: Image.Image) -> dict:
    hard_diff = forbidden_diff = total_fill = changed_fill = 0
    for a, b, h, c, e, r in zip(
        master.get_flattened_data(),
        candidate.get_flattened_data(),
        masks["hard_fixed"].get_flattened_data(),
        masks["contact_zone"].get_flattened_data(),
        masks["extension_allowed"].get_flattened_data(),
        required.get_flattened_data(),
    ):
        if h == 255 and a != b:
            hard_diff += 1
        if h == 0 and c == 0 and e == 0 and a != b:
            forbidden_diff += 1
        if r == 255:
            total_fill += 1
            if a != b and b[3] >= 8:
                changed_fill += 1
    return {
        "hard_fixed_rgba_diff_pixels": hard_diff,
        "forbidden_rgba_diff_pixels": forbidden_diff,
        "required_fill_changed_visible_coverage": (
            changed_fill / total_fill if total_fill else 0.0
        ),
    }


def region_guide(master: Image.Image, masks: dict[str, Image.Image], required: Image.Image) -> Image.Image:
    guide = master.copy()
    tint = Image.new("RGBA", master.size, (0, 0, 0, 0))
    px = tint.load()
    for y in range(master.height):
        for x in range(master.width):
            if masks["hard_fixed"].getpixel((x, y)) == 255:
                px[x, y] = (225, 72, 72, 95)
            elif masks["contact_zone"].getpixel((x, y)) == 255:
                px[x, y] = (72, 140, 225, 88)
            elif masks["extension_allowed"].getpixel((x, y)) == 255:
                px[x, y] = (72, 205, 115, 58)
            if required.getpixel((x, y)) == 255:
                # RequiredFill is a validation guide, not a clipping boundary.
                old = px[x, y]
                px[x, y] = (230, 200, 70, max(old[3], 90))
    guide.alpha_composite(tint)
    return guide


def build_cases(master: Image.Image, representative: Image.Image) -> dict[str, Image.Image]:
    cases: dict[str, Image.Image] = {}

    # 1) Low granular baseline: exact registered real image, proving that the
    # v4 compositor preserves the already-approved contact treatment.
    cases["01_low_grain_registered"] = representative.copy()

    # 2) Large pieces: existing AMJ in-hull millet art, layered as real artwork
    # on the intact master context. No cavity/pile/exemplar mask is used.
    large = master.copy()
    contact_shadow(large, (48, 104, 210, 158))
    hull = MILLET_ROOT / "MilletInHull/MilletInHull_a.png"
    place(large, transformed(hull, 132, -4), (116, 104))
    place(large, transformed(hull, 112, 12), (150, 107))
    place(large, transformed(hull, 94, -16), (107, 120))
    cases["02_large_pieces"] = large

    # 3) Strong over-rim stress: a filled base plus an existing AMJ millet
    # sheaf crossing the upper/front contact area. The lower HardFixed wood is
    # restored only after this context has been drawn.
    overlap = master.copy()
    contact_shadow(overlap, (45, 108, 213, 160))
    grain = MILLET_ROOT / "Millet/Millet_a.png"
    place(overlap, transformed(grain, 168, 0), (128, 110))
    sheaf = MILLET_ROOT / "RawMillet/RawMillet_a.png"
    place(overlap, transformed(sheaf, 105, -18), (132, 105))
    cases["03_strong_over_rim"] = overlap

    return cases


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    master, masks, required = fixed_template.load_contact_contract(MANIFEST)
    spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    representative_path = MANIFEST.parent / spec["representative_final"]["path"]
    with Image.open(representative_path) as image:
        representative = image.convert("RGBA")

    region_guide(master, masks, required).save(OUT / "00_region_guide.png")

    results = {
        "template_revision": spec["template_revision"],
        "production_status": spec["production_status"],
        "note": "study only; structural status does not activate production",
        "cases": {},
    }

    for name, context in build_cases(master, representative).items():
        case_dir = OUT / name
        case_dir.mkdir(parents=True, exist_ok=True)
        context_path = case_dir / "context.png"
        final_path = case_dir / "final.png"
        review_path = case_dir / "review.png"
        context.save(context_path, format="PNG")

        record = {"status": "not_run"}
        try:
            fixed_template.compose(MANIFEST, context_path, final_path, study=True)
            with Image.open(final_path) as image:
                final = image.convert("RGBA")
            record.update(metrics(master, final, masks, required))
            record["status"] = "STRUCTURAL_PASS"
            boxed_resource_review.render_review(MANIFEST, final_path, review_path)
        except Exception as exc:
            # Preserve a clearly-labeled diagnostic rendering so a visual failure
            # can be inspected without weakening the official validator.
            diagnostic = diagnostic_restore(master, masks["hard_fixed"], context)
            diagnostic_path = case_dir / "final_UNVALIDATED.png"
            diagnostic.save(diagnostic_path, format="PNG")
            record.update(metrics(master, diagnostic, masks, required))
            record["status"] = "STRUCTURAL_FAIL"
            record["error"] = f"{type(exc).__name__}: {exc}"
            boxed_resource_review.render_review(MANIFEST, diagnostic_path, review_path)

        results["cases"][name] = record

    (OUT / "metrics.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for name, record in results["cases"].items():
        print(name, record)
    print("STUDY ONLY: artifacts written under", OUT)


if __name__ == "__main__":
    main()
