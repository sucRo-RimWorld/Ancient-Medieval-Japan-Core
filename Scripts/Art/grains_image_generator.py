#!/usr/bin/env python3
"""Generate one Grains art candidate from locked AMJ references, then QA it.

Development-only authoring entry point. It never writes directly to Textures/,
Art/Sources/, or Docs/References/ and never auto-retries a failed image.
Final semantic/visual acceptance remains a separate review gate.
"""
from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
import hashlib
import importlib.util
import io
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "Docs/References/AMJ_Grains_ImageGenerator.json"
API_URL = "https://api.openai.com/v1/images/edits"
PROTECTED_OUTPUT_ROOTS = (
    ROOT / "Textures",
    ROOT / "Art/Sources",
    ROOT / "Docs/References",
)


class GenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Reference:
    role: str
    source: str
    filename: str
    data: bytes
    sha256: str
    width: int
    height: int
    mode: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _image_meta(data: bytes, source: str) -> tuple[int, int, str, str]:
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            fmt = image.format or "UNKNOWN"
            if fmt not in {"PNG", "WEBP", "JPEG"}:
                raise GenerationError(f"unsupported reference format {fmt}: {source}")
            return image.width, image.height, image.mode, fmt
    except (OSError, ValueError) as exc:
        raise GenerationError(f"cannot decode reference image: {source}: {exc}") from exc


def _reference_from_bytes(role: str, source: str, filename: str, data: bytes) -> Reference:
    width, height, mode, _ = _image_meta(data, source)
    if len(data) > 50 * 1024 * 1024:
        raise GenerationError(f"reference exceeds 50 MB API limit: {source}")
    return Reference(role, source, filename, data, _sha256(data), width, height, mode)


def _reference_from_path(role: str, path: Path) -> Reference:
    path = path.resolve()
    if not path.is_file():
        raise GenerationError(f"required reference missing: {path}")
    return _reference_from_bytes(role, str(path), path.name, path.read_bytes())


def _find_one(root: Path, names: Iterable[str], role: str) -> Reference:
    wanted = {name.lower() for name in names}
    matches = sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.name.lower() in wanted
    )
    if not matches:
        raise GenerationError(
            f"MO reference not found for {role} under {root}: {sorted(wanted)}"
        )
    if len(matches) > 1:
        texture_matches = [
            path
            for path in matches
            if "textures" in {part.lower() for part in path.parts}
        ]
        if len(texture_matches) == 1:
            matches = texture_matches
        else:
            raise GenerationError(
                f"ambiguous MO reference for {role}; pass a cleaner --mo-root: "
                + ", ".join(str(path) for path in matches[:8])
            )
    return _reference_from_path(role, matches[0])


def _find_one_in_zip(zip_path: Path, names: Iterable[str], role: str) -> Reference:
    wanted = {name.lower() for name in names}
    try:
        archive = zipfile.ZipFile(zip_path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise GenerationError(f"cannot open MO ZIP {zip_path}: {exc}") from exc
    with archive:
        matches = sorted(
            name
            for name in archive.namelist()
            if Path(name).name.lower() in wanted
            and "/textures/" in f"/{name.lower()}"
        )
        if not matches:
            raise GenerationError(
                f"MO reference not found for {role} in {zip_path}: {sorted(wanted)}"
            )
        if len(matches) > 1:
            raise GenerationError(
                f"ambiguous MO reference for {role} in ZIP: "
                + ", ".join(matches[:8])
            )
        member = matches[0]
        return _reference_from_bytes(
            role,
            f"{zip_path}!{member}",
            Path(member).name,
            archive.read(member),
        )


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GenerationError(f"cannot load generator policy {path}: {exc}") from exc
    if policy.get("schema_version") != 1 or not isinstance(policy.get("families"), dict):
        raise GenerationError(f"unsupported generator policy schema: {path}")
    return policy


def _assert_safe_output(path: Path) -> None:
    resolved = path.resolve()
    for root in PROTECTED_OUTPUT_ROOTS:
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        raise GenerationError(
            f"candidate output may not write into protected source/production tree: {resolved}"
        )


def _load_family_references(
    family_name: str,
    family: dict[str, Any],
    subject_refs: list[Path],
    mo_root: Path | None,
    mo_zip: Path | None,
    allow_no_mo: bool,
) -> list[Reference]:
    references: list[Reference] = []
    for rel in family.get("accepted_references", []):
        references.append(
            _reference_from_path("accepted AMJ style reference", ROOT / rel)
        )

    for subject_ref in subject_refs:
        references.append(
            _reference_from_path("subject identity reference", subject_ref)
        )

    if family.get("require_subject_reference", True) and not subject_refs:
        raise GenerationError(
            f"{family_name} requires at least one --subject-reference"
        )

    mo_names = family.get("mo_reference_filenames", [])
    if mo_names:
        if mo_root and mo_zip:
            raise GenerationError("use only one of --mo-root or --mo-zip")
        if mo_root:
            references.append(
                _find_one(
                    mo_root,
                    mo_names,
                    "Medieval Overhaul style reference",
                )
            )
        elif mo_zip:
            references.append(
                _find_one_in_zip(
                    mo_zip,
                    mo_names,
                    "Medieval Overhaul style reference",
                )
            )
        elif family.get("require_mo_reference", False) and not allow_no_mo:
            raise GenerationError(
                f"{family_name} requires an actual MO reference; pass "
                "--mo-root/--mo-zip or explicitly use --allow-no-mo-reference "
                "for a knowingly incomplete draft"
            )

    if len(references) > 16:
        raise GenerationError(f"too many API input images ({len(references)} > 16)")
    return references


def _build_prompt(
    subject: str,
    family_name: str,
    family: dict[str, Any],
    references: list[Reference],
    notes: str,
) -> str:
    reference_lines = [
        f"{index}. {ref.role}: {ref.filename} (use for {ref.role}; reference only)"
        for index, ref in enumerate(references, 1)
    ]
    rules = family.get("prompt_rules", [])
    prompt = f"""Create exactly ONE NEW isolated source image for Ancient & Medieval Japan (AMJ) Grains.

TARGET
- Subject: {subject}
- Asset family: {family_name}
- Intended use: high-resolution source candidate that will later be exported deterministically to a RimWorld texture.

INPUT IMAGE ROLES
{chr(10).join(reference_lines)}

Use every input only for its stated role. Do not collage, trace, copy exact pixels, or reproduce an existing reference as the result. The result must depict the requested subject, not one of the style references.

AMJ / MEDIEVAL OVERHAUL VISUAL CONTRACT
- Flat vector-like 2D game art; silhouette first, detail second.
- Restrained palette and information density; hard-edged color planes.
- Thick warm medium-dark brown outer outline; internal linework is subordinate.
- No gradients, no soft airbrush modeling, no photorealism, no painterly noise.
- No text, UI, frame, scenery, background, decorative cast shadow, watermark, or unrelated objects.
- Transparent background. Center the subject with generous transparent margin.
- Must remain clear around 64 px; do not add detail that exists only to impress at full resolution.

FAMILY-SPECIFIC RULES
{chr(10).join("- " + str(rule) for rule in rules)}
"""
    if notes.strip():
        prompt += f"\nSUBJECT-SPECIFIC NOTES\n- {notes.strip()}\n"
    prompt += "\nGenerate only the single isolated asset."
    return prompt


def _multipart(
    fields: dict[str, str],
    references: list[Reference],
) -> tuple[bytes, str]:
    boundary = "----AMJGrains" + secrets.token_hex(16)
    out = bytearray()

    def add_line(value: bytes = b"") -> None:
        out.extend(value + b"\r\n")

    for name, value in fields.items():
        add_line(f"--{boundary}".encode())
        add_line(f'Content-Disposition: form-data; name="{name}"'.encode())
        add_line()
        add_line(value.encode("utf-8"))

    for ref in references:
        add_line(f"--{boundary}".encode())
        safe_name = ref.filename.replace('"', "_")
        add_line(
            f'Content-Disposition: form-data; name="image[]"; '
            f'filename="{safe_name}"'.encode()
        )
        mime = mimetypes.guess_type(ref.filename)[0] or "application/octet-stream"
        add_line(f"Content-Type: {mime}".encode())
        add_line()
        out.extend(ref.data)
        out.extend(b"\r\n")

    add_line(f"--{boundary}--".encode())
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def _call_openai(
    api_key: str,
    *,
    model: str,
    prompt: str,
    references: list[Reference],
    size: str,
    quality: str,
) -> tuple[bytes, dict[str, Any]]:
    fields = {
        "model": model,
        "prompt": prompt,
        "n": "1",
        "size": size,
        "quality": quality,
        "background": "transparent",
        "output_format": "png",
    }
    body, content_type = _multipart(fields, references)
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
            "Accept": "application/json",
            "User-Agent": "AMJ-Grains-Image-Generator/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:4000]
        raise GenerationError(
            f"OpenAI image API HTTP {exc.code}: {detail}"
        ) from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise GenerationError(f"OpenAI image API request failed: {exc}") from exc

    try:
        encoded = payload["data"][0]["b64_json"]
        image_bytes = base64.b64decode(encoded, validate=True)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise GenerationError(
            "OpenAI image API response contained no decodable image"
        ) from exc
    return image_bytes, payload.get("usage") or {}


def _load_generated_qa():
    path = ROOT / "Scripts/Art/generated_asset_qa.py"
    spec = importlib.util.spec_from_file_location("amj_generated_asset_qa", path)
    if spec is None or spec.loader is None:
        raise GenerationError(f"cannot load QA module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _complexity_report(
    candidate: Path,
    references: list[Reference],
    output_dir: Path,
) -> dict[str, Any]:
    qa = _load_generated_qa()
    candidate_metrics = qa.analyze(candidate)
    refs: list[dict[str, Any]] = []

    for index, ref in enumerate(references):
        temp = output_dir / f".reference-{index}.png"
        try:
            with Image.open(io.BytesIO(ref.data)) as image:
                image.load()
                image.convert("RGBA").save(temp, format="PNG")
            metrics = qa.analyze(temp)
        finally:
            temp.unlink(missing_ok=True)
        refs.append(
            {
                "role": ref.role,
                "source": ref.source,
                "metrics": metrics,
            }
        )

    style_metrics = [
        ref["metrics"]
        for ref in refs
        if "style reference" in ref["role"]
    ]
    failures: list[str] = []
    if style_metrics:
        max_colors = max(
            metrics["coarse_color_bins_16_at_64"]
            for metrics in style_metrics
        )
        max_edges = max(
            metrics["strong_edge_density_at_64"]
            for metrics in style_metrics
        )
        allowed_colors = max_colors + max(6, round(max_colors * 0.35))
        allowed_edges = min(1.0, max_edges * 1.35 + 0.02)

        if candidate_metrics["coarse_color_bins_16_at_64"] > allowed_colors:
            failures.append(
                "game-size color complexity exceeds accepted style references: "
                f"{candidate_metrics['coarse_color_bins_16_at_64']} > "
                f"{allowed_colors}"
            )
        if candidate_metrics["strong_edge_density_at_64"] > allowed_edges:
            failures.append(
                "game-size edge density exceeds accepted style references: "
                f"{candidate_metrics['strong_edge_density_at_64']:.4f} > "
                f"{allowed_edges:.4f}"
            )

    return {
        "passed": not failures,
        "failures": failures,
        "candidate": candidate_metrics,
        "references": refs,
    }


def _review_sheet(
    candidate: Path,
    references: list[Reference],
    output: Path,
) -> None:
    tile = 256
    label_h = 34
    entries: list[tuple[str, Image.Image]] = []

    with Image.open(candidate) as image:
        image.load()
        entries.append(("CANDIDATE", image.convert("RGBA").copy()))
    for ref in references:
        with Image.open(io.BytesIO(ref.data)) as image:
            image.load()
            entries.append((ref.role[:26], image.convert("RGBA").copy()))

    cols = min(4, len(entries))
    rows = (len(entries) + cols - 1) // cols
    canvas = Image.new(
        "RGBA",
        (cols * tile, rows * (tile + label_h)),
        (245, 245, 245, 255),
    )
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    checker = Image.new("RGBA", (tile, tile), (230, 230, 230, 255))
    cdraw = ImageDraw.Draw(checker)
    step = 16
    for y in range(0, tile, step):
        for x in range(0, tile, step):
            if ((x // step) + (y // step)) % 2:
                cdraw.rectangle(
                    (x, y, x + step - 1, y + step - 1),
                    fill=(205, 205, 205, 255),
                )

    for index, (label, image) in enumerate(entries):
        x = (index % cols) * tile
        y = (index // cols) * (tile + label_h)
        preview = image.copy()
        preview.thumbnail((tile - 20, tile - 20), Image.Resampling.LANCZOS)
        cell = checker.copy()
        cell.alpha_composite(
            preview,
            ((tile - preview.width) // 2, (tile - preview.height) // 2),
        )
        canvas.alpha_composite(cell, (x, y))
        draw.text(
            (x + 6, y + tile + 4),
            label,
            fill=(20, 20, 20, 255),
            font=font,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, format="PNG")


def _write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def run(args: argparse.Namespace) -> int:
    policy_path = args.policy.resolve()
    policy = _load_policy(policy_path)
    try:
        family = policy["families"][args.family]
    except KeyError as exc:
        raise GenerationError(
            f"unknown family {args.family!r}; "
            f"choose from {sorted(policy['families'])}"
        ) from exc

    output_dir = args.output_dir.resolve()
    _assert_safe_output(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    references = _load_family_references(
        args.family,
        family,
        args.subject_reference,
        args.mo_root,
        args.mo_zip,
        args.allow_no_mo_reference,
    )
    prompt = _build_prompt(
        args.subject,
        args.family,
        family,
        references,
        args.notes or "",
    )
    (output_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "policy": str(policy_path),
        "family": args.family,
        "subject": args.subject,
        "model": args.model,
        "size": args.size,
        "quality": args.quality,
        "references": [
            {
                "role": ref.role,
                "source": ref.source,
                "filename": ref.filename,
                "sha256": ref.sha256,
                "width": ref.width,
                "height": ref.height,
                "mode": ref.mode,
            }
            for ref in references
        ],
        "prompt_sha256": _sha256(prompt.encode("utf-8")),
        "generated": False,
        "automatic_retry": False,
    }
    _write_manifest(output_dir / "manifest.json", manifest)

    if args.dry_run:
        print(
            "PASS: generation plan prepared without API call: "
            f"{output_dir}"
        )
        return 0

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise GenerationError(
            "OPENAI_API_KEY is required unless --dry-run is used"
        )

    image_bytes, usage = _call_openai(
        key,
        model=args.model,
        prompt=prompt,
        references=references,
        size=args.size,
        quality=args.quality,
    )
    candidate = output_dir / "candidate-source.png"
    candidate.write_bytes(image_bytes)
    width, height, mode, fmt = _image_meta(image_bytes, str(candidate))
    if fmt != "PNG":
        raise GenerationError(f"API output was not PNG: {fmt}")

    qa = _load_generated_qa()
    base_qa_path = ROOT / policy["base_qa_policy"]
    base_result = qa.validate(candidate, base_qa_path)
    complexity = _complexity_report(candidate, references, output_dir)
    _write_manifest(
        output_dir / "qa-report.json",
        {
            "base": base_result,
            "relative_complexity": complexity,
        },
    )

    manifest.update(
        {
            "generated": True,
            "candidate": {
                "path": str(candidate),
                "sha256": _sha256(image_bytes),
                "width": width,
                "height": height,
                "mode": mode,
            },
            "usage": usage,
            "mechanical_qa_passed": bool(
                base_result["passed"] and complexity["passed"]
            ),
        }
    )
    _write_manifest(output_dir / "manifest.json", manifest)

    if not base_result["passed"] or not complexity["passed"]:
        print(
            "FAIL: generated candidate rejected by automatic "
            "mechanical/style-complexity QA"
        )
        for failure in base_result["failures"] + complexity["failures"]:
            print(f"- {failure}")
        print(
            "Internal candidate retained for diagnosis only: "
            f"{candidate}"
        )
        return 2

    if family.get("postprocess") == "boxed-resource":
        preparer = ROOT / "Scripts/Art/prepare_boxed_resource_candidate.py"
        boxed_dir = output_dir / "boxed-prepared"
        subprocess.run(
            [
                sys.executable,
                str(preparer),
                str(candidate),
                "--output-dir",
                str(boxed_dir),
            ],
            cwd=ROOT,
            check=True,
        )
        manifest["boxed_prepared"] = str(boxed_dir)
        _write_manifest(output_dir / "manifest.json", manifest)

    review = output_dir / "review-sheet.png"
    _review_sheet(candidate, references, review)
    print(
        "PASS: one candidate passed automatic gates; "
        f"visual review still required: {review}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--family",
        required=True,
        help="Policy family key, e.g. plant-mature or loose-grain",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="Requested crop/material name",
    )
    parser.add_argument(
        "--subject-reference",
        type=Path,
        action="append",
        default=[],
        help="Actual subject identity image; repeatable",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Botanical/material silhouette notes that must be preserved",
    )
    parser.add_argument(
        "--mo-root",
        type=Path,
        help="Extracted Medieval Overhaul root used to resolve the real reference",
    )
    parser.add_argument(
        "--mo-zip",
        type=Path,
        help="Medieval Overhaul ZIP used to resolve the real reference",
    )
    parser.add_argument(
        "--allow-no-mo-reference",
        action="store_true",
        help="Explicit incomplete-draft override; never implies final acceptance",
    )
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Development-only output directory, normally Work/Art/...",
    )
    parser.add_argument(
        "--model",
        default="gpt-image-2.5-sunburst-2026-09-08",
    )
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high", "xhigh", "max", "auto"],
        default="high",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve references and write prompt/manifest without calling the API",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return run(args)
    except (GenerationError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
