#!/usr/bin/env python3
"""Prepare and review one Grains image candidate without calling a paid image API.

This repository tool owns the deterministic parts around image generation:
reference resolution, prompt construction, reference bundling, mechanical QA,
and review-sheet generation.

The actual image-generation step is deliberately external to this Python
process. In ChatGPT work, use the built-in image-generation tool between the
"prepare" and "review" commands. No API credential is read and no network
request is made by this script.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "Docs/References/AMJ_Grains_ImageGenerator.json"
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
                raise GenerationError(f"unsupported image format {fmt}: {source}")
            return image.width, image.height, image.mode, fmt
    except (OSError, ValueError) as exc:
        raise GenerationError(f"cannot decode image: {source}: {exc}") from exc


def _reference_from_bytes(role: str, source: str, filename: str, data: bytes) -> Reference:
    width, height, mode, _ = _image_meta(data, source)
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
            f"unreviewed image workflow may not write into protected source/"
            f"production tree: {resolved}"
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


def _role_slug(role: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", role.lower()).strip("-")
    return value or "reference"


def _write_reference_bundle(
    output_dir: Path,
    references: list[Reference],
) -> list[dict[str, Any]]:
    reference_dir = output_dir / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)
    bundled: list[dict[str, Any]] = []

    for index, ref in enumerate(references, 1):
        suffix = Path(ref.filename).suffix.lower() or ".png"
        filename = f"{index:02d}-{_role_slug(ref.role)}{suffix}"
        path = reference_dir / filename
        path.write_bytes(ref.data)
        if _sha256(path.read_bytes()) != ref.sha256:
            raise GenerationError(f"reference bundle write changed bytes: {path}")
        bundled.append(
            {
                "role": ref.role,
                "source": ref.source,
                "source_filename": ref.filename,
                "bundle_path": str(path.relative_to(output_dir)),
                "sha256": ref.sha256,
                "width": ref.width,
                "height": ref.height,
                "mode": ref.mode,
            }
        )
    return bundled


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _prepare(args: argparse.Namespace) -> int:
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
    bundled = _write_reference_bundle(output_dir, references)

    policy_bytes = policy_path.read_bytes()
    manifest: dict[str, Any] = {
        "schema_version": 2,
        "workflow": "chatgpt-imagegen-prepare-review",
        "status": "prepared",
        "family": args.family,
        "subject": args.subject,
        "policy": {
            "path": str(policy_path),
            "sha256": _sha256(policy_bytes),
        },
        "prompt": {
            "path": "prompt.txt",
            "sha256": _sha256(prompt.encode("utf-8")),
        },
        "references": bundled,
        "generation": {
            "provider": "ChatGPT built-in image generation",
            "python_calls_image_api": False,
            "api_key_required": False,
            "image_count": 1,
            "transparent_background": True,
            "candidate_expected": "candidate-source.png",
            "automatic_retry": False,
            "note": (
                "Run image generation outside this Python process using prompt.txt "
                "and every bundled reference. Then run the review subcommand on the "
                "resulting PNG."
            ),
        },
    }
    _write_json(output_dir / "manifest.json", manifest)
    _write_json(
        output_dir / "generation-request.json",
        {
            "provider": manifest["generation"]["provider"],
            "prompt_file": "prompt.txt",
            "reference_files": [item["bundle_path"] for item in bundled],
            "image_count": 1,
            "transparent_background": True,
            "candidate_expected": "candidate-source.png",
            "api_key_required": False,
            "automatic_retry": False,
        },
    )

    print(f"PASS: Grains image-generation request prepared: {output_dir}")
    print("NEXT: generate exactly one image in ChatGPT using prompt.txt and all references.")
    print("THEN: run this script's review subcommand on the generated PNG.")
    return 0


def _load_generated_qa():
    path = ROOT / "Scripts/Art/generated_asset_qa.py"
    spec = importlib.util.spec_from_file_location("amj_generated_asset_qa", path)
    if spec is None or spec.loader is None:
        raise GenerationError(f"cannot load QA module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _references_from_manifest(
    work_dir: Path,
    manifest: dict[str, Any],
) -> list[Reference]:
    references: list[Reference] = []
    for item in manifest.get("references", []):
        path = work_dir / item["bundle_path"]
        if not path.is_file():
            raise GenerationError(f"bundled reference missing: {path}")
        data = path.read_bytes()
        actual = _sha256(data)
        if actual != item["sha256"]:
            raise GenerationError(
                f"bundled reference SHA-256 mismatch: {path}: "
                f"{actual} != {item['sha256']}"
            )
        references.append(
            _reference_from_bytes(
                item["role"],
                item.get("source", str(path)),
                item.get("source_filename", path.name),
                data,
            )
        )
    if not references:
        raise GenerationError("manifest contains no bundled references")
    return references


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


def _review(args: argparse.Namespace) -> int:
    work_dir = args.work_dir.resolve()
    _assert_safe_output(work_dir)
    manifest_path = work_dir / "manifest.json"
    if not manifest_path.is_file():
        raise GenerationError(f"prepared manifest missing: {manifest_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GenerationError(f"cannot read prepared manifest: {exc}") from exc
    if manifest.get("schema_version") != 2:
        raise GenerationError("review requires a schema_version 2 prepared manifest")

    references = _references_from_manifest(work_dir, manifest)
    candidate_input = args.candidate.resolve()
    if not candidate_input.is_file():
        raise GenerationError(f"candidate missing: {candidate_input}")
    _assert_safe_output(candidate_input)

    candidate_bytes = candidate_input.read_bytes()
    width, height, mode, fmt = _image_meta(candidate_bytes, str(candidate_input))
    if fmt != "PNG":
        raise GenerationError(f"candidate must be PNG, got {fmt}")

    candidate = work_dir / "candidate-source.png"
    candidate.write_bytes(candidate_bytes)
    if _sha256(candidate.read_bytes()) != _sha256(candidate_bytes):
        raise GenerationError("candidate staging changed bytes")

    policy_info = manifest.get("policy", {})
    policy_path = Path(policy_info.get("path", DEFAULT_POLICY))
    if not policy_path.is_file():
        policy_path = DEFAULT_POLICY
    policy_bytes = policy_path.read_bytes()
    if policy_info.get("sha256") and _sha256(policy_bytes) != policy_info["sha256"]:
        raise GenerationError(
            "generator policy changed since prepare; prepare a fresh request before review"
        )
    policy = _load_policy(policy_path)
    family_name = manifest["family"]
    try:
        family = policy["families"][family_name]
    except KeyError as exc:
        raise GenerationError(f"prepared family no longer exists: {family_name}") from exc

    qa = _load_generated_qa()
    base_qa_path = ROOT / policy["base_qa_policy"]
    base_result = qa.validate(candidate, base_qa_path)
    passed = bool(base_result["passed"])

    report = {
        "base": base_result,
        "passed": passed,
        "semantic_visual_review_required": True,
        "pre_display_screening_claimed": False,
    }
    _write_json(work_dir / "qa-report.json", report)

    manifest["candidate"] = {
        "input_path": str(candidate_input),
        "staged_path": "candidate-source.png",
        "sha256": _sha256(candidate_bytes),
        "width": width,
        "height": height,
        "mode": mode,
    }
    manifest["status"] = "automatic-qa-passed" if passed else "automatic-qa-failed"
    manifest["automatic_qa_passed"] = passed
    manifest["semantic_visual_review_required"] = True
    manifest["pre_display_screening_claimed"] = False

    if passed and family.get("postprocess") == "boxed-resource":
        preparer = ROOT / "Scripts/Art/prepare_boxed_resource_candidate.py"
        boxed_dir = work_dir / "boxed-prepared"
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
        manifest["boxed_prepared"] = str(boxed_dir.relative_to(work_dir))

    _write_json(manifest_path, manifest)
    _review_sheet(candidate, references, work_dir / "review-sheet.png")

    if not passed:
        print("FAIL: candidate rejected by structural image QA")
        for failure in base_result["failures"]:
            print(f"- {failure}")
        print("No automatic retry is performed.")
        return 2

    print(
        "PASS: candidate passed structural image checks; "
        "semantic/visual comparison and author acceptance remain required"
    )
    return 0


def _add_common_prepare_args(parser: argparse.ArgumentParser) -> None:
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
        help="Development-only work directory, normally Work/Art/...",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare",
        help="Resolve references and create an API-free ChatGPT generation request",
    )
    _add_common_prepare_args(prepare)

    review = subparsers.add_parser(
        "review",
        help="Run deterministic QA on one image produced after prepare",
    )
    review.add_argument(
        "--work-dir",
        type=Path,
        required=True,
        help="Directory previously created by the prepare command",
    )
    review.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Generated PNG to stage and review",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "prepare":
            return _prepare(args)
        if args.command == "review":
            return _review(args)
        raise GenerationError(f"unsupported command: {args.command}")
    except (GenerationError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
