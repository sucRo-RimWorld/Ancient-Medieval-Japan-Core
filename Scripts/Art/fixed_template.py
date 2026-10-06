"""Deterministic fixed-template compositing for AMJ art families."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw


def _read_spec(manifest_path):
    path = Path(manifest_path)
    spec = json.loads(path.read_text(encoding="utf-8"))
    if spec["version"] != 1:
        raise ValueError("Unsupported manifest version")
    status = spec.get("production_status", "active")
    if status != "active":
        raise ValueError(f"Template is not active for production: {status}")
    return path, spec


def _load_hashed_image(base, entry, mode=None):
    source = base / entry["path"]
    if hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
        raise ValueError(f"{source.name}: SHA-256 mismatch")
    with Image.open(source) as image:
        image.load()
        if mode and image.mode != mode:
            raise ValueError(f"{source.name}: expected image mode {mode}, got {image.mode}")
        return image.convert("RGBA") if mode != "L" else image.copy()


def load_template(manifest_path):
    path, spec = _read_spec(manifest_path)
    master = _load_hashed_image(path.parent, spec["master"])
    mask = _load_hashed_image(path.parent, spec["editable_mask"], "L")
    if master.size != tuple(spec["size"]) or mask.size != master.size:
        raise ValueError("Template/mask dimensions mismatch")
    values = set(mask.get_flattened_data())
    if not values <= {0, 255} or values != {0, 255}:
        raise ValueError("Mask must contain both protected 0 and editable 255 pixels only")
    return master, mask


def _required_guide(path, spec):
    entry = spec["required_fill"]
    required = _load_hashed_image(path.parent, entry, "L")
    if required.size != tuple(spec["size"]):
        raise ValueError("Required-fill guide dimensions mismatch")
    if not set(required.get_flattened_data()) <= {0, 255}:
        raise ValueError("Required-fill guide must be binary")
    return required


def build_three_layer_stack(manifest_path):
    # Historical v3 experiment only. Visual review found split-boundary damage.
    # Generic new-resource production is fail-closed before this model can be used.
    path, spec = _read_spec(manifest_path)
    if spec.get("layer_model") != "rear_contents_front":
        raise ValueError("Template does not use rear_contents_front layers")
    master, _ = load_template(path)

    front_mask = Image.new("L", master.size, 0)
    draw = ImageDraw.Draw(front_mask)
    regions = spec.get("front_occluder_regions")
    if not regions:
        raise ValueError("front_occluder_regions is missing")
    for polygon in regions:
        if len(polygon) < 3:
            raise ValueError("Invalid front occluder polygon")
        draw.polygon([tuple(point) for point in polygon], fill=255)

    transparent = Image.new("RGBA", master.size, (0, 0, 0, 0))
    front = Image.composite(master, transparent, front_mask)
    rear = Image.composite(transparent, master, front_mask)

    empty = Image.alpha_composite(rear, front)
    differing = sum(
        a != b for a, b in zip(empty.get_flattened_data(), master.get_flattened_data())
    )
    expected = int(spec.get("structural_gates", {}).get("empty_master_roundtrip_rgba_diff_pixels", 0))
    if differing != expected:
        raise ValueError(
            f"Rear/front split does not reconstruct master: {differing} != {expected}"
        )
    return master, rear, front, front_mask


def _registered_visual_envelope(path, spec, master):
    entry = spec["representative_final"]
    representative = _load_hashed_image(path.parent, entry)
    if representative.size != master.size:
        raise ValueError("Representative-final dimensions mismatch")
    threshold = int(spec.get("required_fill", {}).get("alpha_threshold", 1))
    ma = list(master.getchannel("A").get_flattened_data())
    ra = list(representative.getchannel("A").get_flattened_data())
    return [a >= threshold or b >= threshold for a, b in zip(ma, ra)]


def validate_three_layer_final(manifest_path, candidate):
    path, spec = _read_spec(manifest_path)
    master, rear, front, front_mask = build_three_layer_stack(path)
    candidate = candidate.convert("RGBA")
    if candidate.size != master.size:
        raise ValueError("Output dimensions mismatch; resizing is forbidden")

    # Foreground is a fixed z-order layer, so selected pixels must be exact.
    changed_front = sum(
        m == 255 and a != b
        for a, b, m in zip(
            candidate.get_flattened_data(),
            master.get_flattened_data(),
            front_mask.get_flattened_data(),
        )
    )
    expected_front = int(spec.get("structural_gates", {}).get("fixed_foreground_rgba_diff_pixels", 0))
    if changed_front != expected_front:
        raise ValueError(
            f"{changed_front} fixed foreground RGBA pixels changed"
        )

    # Contents may not create visible pixels outside the authoritative raster envelope.
    threshold = int(spec.get("required_fill", {}).get("alpha_threshold", 1))
    envelope = _registered_visual_envelope(path, spec, master)
    alpha = list(candidate.getchannel("A").get_flattened_data())
    leaks = sum(a >= threshold and not allowed for a, allowed in zip(alpha, envelope))
    if leaks:
        raise ValueError(f"{leaks} visible content pixels leak outside registered envelope")

    # Required fill is a validation target, never a clipping mask.
    required = _required_guide(path, spec)
    required_pixels = [i for i, v in enumerate(required.get_flattened_data()) if v == 255]
    cand_pixels = list(candidate.get_flattened_data())
    master_pixels = list(master.get_flattened_data())
    covered = sum(cand_pixels[i] != master_pixels[i] for i in required_pixels) / len(required_pixels)
    minimum = float(spec["required_fill"].get("min_alpha_coverage", 0.0))
    if covered < minimum:
        raise ValueError(
            f"Final resource under-fills required region: {covered:.3f} < {minimum:.3f}"
        )
    return candidate


def _validate_legacy(master, mask, candidate):
    if candidate.size != master.size:
        raise ValueError("Output dimensions mismatch; resizing is forbidden")
    candidate = candidate.convert("RGBA")
    changed = sum(
        a != b and m == 0
        for a, b, m in zip(
            master.get_flattened_data(),
            candidate.get_flattened_data(),
            mask.get_flattened_data(),
        )
    )
    if changed:
        raise ValueError(f"{changed} protected RGBA pixels changed")
    return candidate


def validate_variable_layer(manifest_path, layer, mask=None):
    path, spec = _read_spec(manifest_path)
    layer = layer.convert("RGBA")
    if layer.size != tuple(spec["size"]):
        raise ValueError("Variable layer must match template canvas")

    # Active masu: object-only transparent contents. Do not clip to editable mask.
    if spec.get("layer_model") == "rear_contents_front":
        return layer

    # Legacy fixed-mask families.
    master, registered_mask = load_template(path)
    if mask is None:
        mask = registered_mask
    alpha = layer.getchannel("A")
    threshold = int(spec.get("required_fill", {}).get("alpha_threshold", 1))
    if spec.get("enforce_variable_within_editable", True):
        outside = sum(
            a >= threshold and m == 0
            for a, m in zip(alpha.get_flattened_data(), mask.get_flattened_data())
        )
        if outside:
            raise ValueError(
                f"Variable layer has {outside} nontransparent pixels outside allowed fill region"
            )
    return layer


def scaffold(manifest, output):
    path, spec = _read_spec(manifest)
    master, mask = load_template(path)
    output = Path(output)
    if output.suffix.lower() != ".png":
        raise ValueError("Lossless PNG output required")

    if spec.get("layer_model") == "rear_contents_front":
        contents = Image.new("RGBA", master.size, (0, 0, 0, 0))
        output.parent.mkdir(parents=True, exist_ok=True)
        contents.save(output, format="PNG")
        print(f"PASS: transparent contents scaffold created; {output}")
        return

    transparent = Image.new("RGBA", master.size, (0, 0, 0, 0))
    patch = Image.composite(master, transparent, mask)
    output.parent.mkdir(parents=True, exist_ok=True)
    patch.save(output, format="PNG")
    print(f"PASS: legacy editable RGBA scaffold created; {output}")


def compose(manifest, variable, output):
    path, spec = _read_spec(manifest)
    master, mask = load_template(path)
    with Image.open(variable) as image:
        image.load()
        layer = image.convert("RGBA")
    validate_variable_layer(path, layer, mask)

    status = spec.get("new_resource_production_status", "active")
    if status != "active":
        raise ValueError(
            "New boxed-resource production is blocked until the occlusion contract is validated: "
            + status
        )

    if spec.get("layer_model") == "rear_contents_front":
        master, rear, front, front_mask = build_three_layer_stack(path)
        middle = Image.alpha_composite(rear, layer)
        # Foreground is restored as exact canonical pixels, not blended/clipped
        # through the contents mask.
        result = Image.composite(front, middle, front_mask)
        validate_three_layer_final(path, result)
    else:
        mode = spec.get("compose_mode", "alpha_over")
        if mode == "replace_rgba":
            result = Image.composite(layer, master, mask)
        elif mode == "alpha_over":
            merged = Image.alpha_composite(master, layer)
            result = Image.composite(merged, master, mask)
        else:
            raise ValueError(f"Unsupported compose_mode: {mode}")
        _validate_legacy(master, mask, result)

    output = Path(output)
    if output.suffix.lower() != ".png":
        raise ValueError("Lossless PNG output required")
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format="PNG")
    print(f"PASS: deterministic composition complete; {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["scaffold", "compose", "validate"])
    parser.add_argument("manifest")
    parser.add_argument("image", nargs="?")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.mode == "scaffold":
        if args.image:
            parser.error("scaffold does not take an image argument")
        if not args.output:
            parser.error("scaffold requires --output")
        scaffold(args.manifest, args.output)
        return

    if not args.image:
        parser.error(f"{args.mode} requires an image")

    if args.mode == "compose":
        if not args.output:
            parser.error("compose requires --output")
        compose(args.manifest, args.image, args.output)
        return

    path, spec = _read_spec(args.manifest)
    with Image.open(args.image) as image:
        image.load()
        if image.format != "PNG":
            raise ValueError("Final output must be lossless PNG")
        candidate = image.convert("RGBA")
    if spec.get("layer_model") == "rear_contents_front":
        validate_three_layer_final(path, candidate)
    else:
        master, mask = load_template(path)
        _validate_legacy(master, mask, candidate)
    print("PASS: validation complete")


if __name__ == "__main__":
    main()
