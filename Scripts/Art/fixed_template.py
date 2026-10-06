"""Deterministic fixed-template compositing for AMJ art families."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

CONTACT_MODEL = 'intact_master_base__contents_contact__hard_fixed_foreground'


def _read_spec(manifest_path):
    path = Path(manifest_path)
    spec = json.loads(path.read_text(encoding='utf-8'))
    if spec['version'] != 1:
        raise ValueError('Unsupported manifest version')
    status = spec.get('production_status', 'active')
    if status != 'active' and not (spec.get('layer_model') == CONTACT_MODEL and status == 'blocked_pending_occlusion_validation'):
        raise ValueError(f'Template is not active for production: {status}')
    return path, spec


def _require_production(spec):
    for key in ('production_status', 'new_resource_production_status'):
        status = spec.get(key, 'active')
        if status != 'active':
            raise ValueError('New boxed-resource production is blocked until the occlusion contract is validated: ' + status)
    if spec.get('layer_model') == 'rear_contents_front':
        raise ValueError('Superseded rear/front split cannot be used for production')


def _load_hashed_image(base, entry, mode=None):
    source = base / entry['path']
    if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
        raise ValueError(f'{source.name}: SHA-256 mismatch')
    with Image.open(source) as image:
        image.load()
        if mode and image.mode != mode:
            raise ValueError(f'{source.name}: expected image mode {mode}, got {image.mode}')
        return image.convert('RGBA') if mode != 'L' else image.copy()


def _binary_mask(path, spec, entry, name, nonempty=True):
    mask = _load_hashed_image(path.parent, entry, 'L')
    if mask.size != tuple(spec['size']):
        raise ValueError(f'{name}: dimensions mismatch')
    values = set(mask.get_flattened_data())
    if not values <= {0, 255} or (nonempty and 255 not in values):
        raise ValueError(f'{name}: mask must be nonempty and binary')
    return mask


def load_template(manifest_path):
    path, spec = _read_spec(manifest_path)
    master = _load_hashed_image(path.parent, spec['master'])
    mask = _binary_mask(path, spec, spec['editable_mask'], 'Editable mask')
    if master.size != tuple(spec['size']):
        raise ValueError('Template/mask dimensions mismatch')
    if 0 not in set(mask.get_flattened_data()):
        raise ValueError('Mask must contain both protected 0 and editable 255 pixels only')
    return master, mask


def load_contact_contract(manifest_path):
    """Read registered study masks without enabling production."""
    path, spec = _read_spec(manifest_path)
    if spec.get('layer_model') != CONTACT_MODEL:
        raise ValueError('Template does not use intact-master contact composition')
    master, _ = load_template(path)
    representative = _load_hashed_image(path.parent, spec['representative_final'])
    if representative.size != master.size:
        raise ValueError('Representative-final dimensions mismatch')
    masks = {name: _binary_mask(path, spec, spec['region_contract'][name], name)
             for name in ('hard_fixed', 'contact_zone', 'extension_allowed')}
    required = _binary_mask(path, spec, spec['required_fill'], 'Required fill')
    for a, h, c, e, r in zip(master.getchannel('A').get_flattened_data(),
                           masks['hard_fixed'].get_flattened_data(),
                           masks['contact_zone'].get_flattened_data(),
                           masks['extension_allowed'].get_flattened_data(),
                           required.get_flattened_data()):
        if sum(v == 255 for v in (h, c, e)) > 1:
            raise ValueError('HardFixed/contact/extension masks overlap')
        if (a > 0) != (h == 255 or c == 255):
            raise ValueError('Every visible master pixel must be HardFixed or contact')
        if r == 255 and c != 255 and e != 255:
            raise ValueError('Required fill must be inside contact/extension')
    return master, masks, required


def _check_dimensions(master, candidate):
    if candidate.size != master.size:
        raise ValueError('Output dimensions mismatch; resizing is forbidden')
    return candidate.convert('RGBA')


def _validate_legacy(master, mask, candidate):
    candidate = _check_dimensions(master, candidate)
    changed = sum(a != b and m == 0 for a, b, m in zip(
        master.get_flattened_data(), candidate.get_flattened_data(), mask.get_flattened_data()))
    if changed:
        raise ValueError(f'{changed} protected RGBA pixels changed')
    return candidate


def validate(master, mask, candidate):
    """Backward-compatible validator for ordinary fixed-mask families."""
    return _validate_legacy(master, mask, candidate)


def _check_contact_canvas(master, masks, candidate, minimum):
    candidate = _check_dimensions(master, candidate)
    defined = total = forbidden = 0
    for a, b, h, c, e in zip(master.get_flattened_data(), candidate.get_flattened_data(),
                            masks['hard_fixed'].get_flattened_data(),
                            masks['contact_zone'].get_flattened_data(),
                            masks['extension_allowed'].get_flattened_data()):
        # Reject leaks; never crop a bad source into compliance. HardFixed alone
        # may be restored, including its antialiased RGBA, in the final step.
        forbidden += h == 0 and c == 0 and e == 0 and a != b
        if c == 255 and a[3] >= 8:
            total += 1
            defined += b[3] >= 8
    if forbidden:
        raise ValueError(f'{forbidden} forbidden RGBA pixels changed; source is not clipped')
    if not total or defined / total < minimum:
        raise ValueError('Incomplete contents/contact context canvas; transparent object-only input is invalid')
    return candidate


def validate_contact_final(manifest_path, candidate, require_fill=True):
    """Structural validation only; does not activate the registered study."""
    path, spec = _read_spec(manifest_path)
    master, masks, required = load_contact_contract(path)
    candidate = _check_contact_canvas(master, masks, candidate,
                                     float(spec.get('contact_patch_min_defined_coverage', 0.98)))
    changed = sum(h == 255 and a != b for a, b, h in zip(
        master.get_flattened_data(), candidate.get_flattened_data(), masks['hard_fixed'].get_flattened_data()))
    if changed:
        raise ValueError(f'{changed} HardFixed RGBA pixels changed')
    if require_fill:
        if spec['required_fill'].get('profile') != 'bulk_grain':
            raise ValueError('Unvalidated fill profile; register a family-specific occupancy rule')
        total = covered = 0
        threshold = int(spec['required_fill'].get('alpha_threshold', 8))
        for a, b, r in zip(master.get_flattened_data(), candidate.get_flattened_data(), required.get_flattened_data()):
            if r == 255:
                total += 1
                covered += a != b and b[3] >= threshold
        minimum = float(spec['required_fill']['min_changed_visible_coverage'])
        if not total or covered / total < minimum:
            raise ValueError(f'Final resource under-fills required region: {covered / total if total else 0:.3f} < {minimum:.3f}')
    return candidate


def validate_variable_layer(manifest_path, layer, mask=None):
    path, spec = _read_spec(manifest_path)
    if spec.get('layer_model') == CONTACT_MODEL:
        master, masks, _ = load_contact_contract(path)
        return _check_contact_canvas(master, masks, layer, float(spec.get('contact_patch_min_defined_coverage', 0.98)))
    if spec.get('layer_model') == 'rear_contents_front':
        raise ValueError('Superseded rear/front split cannot be used')
    layer = layer.convert('RGBA')
    if layer.size != tuple(spec['size']):
        raise ValueError('Variable layer must match template canvas')
    _, registered_mask = load_template(path)
    if mask is None:
        mask = registered_mask
    threshold = int(spec.get('required_fill', {}).get('alpha_threshold', 1))
    if spec.get('enforce_variable_within_editable', bool(spec.get('required_fill'))):
        outside = sum(a >= threshold and m == 0 for a, m in zip(
            layer.getchannel('A').get_flattened_data(), mask.get_flattened_data()))
        if outside:
            raise ValueError(f'Variable layer has {outside} nontransparent pixels outside allowed fill region')
    return layer


def _output_guard(path, spec, output, variable=None, study=False):
    output = Path(output)
    if output.suffix.lower() != '.png':
        raise ValueError('Lossless PNG output required')
    sources = {path.resolve()}
    # Protect all registered rasters, including reference/region masks, and input.
    def collect(value):
        if isinstance(value, dict):
            if 'path' in value:
                sources.add((path.parent / value['path']).resolve())
            for child in value.values():
                collect(child)
    collect(spec)
    legacy = spec.get('legacy_identity_exemplar', {})
    for key in ('variable_layer_path', 'expected_final_path'):
        if key in legacy:
            sources.add((path.parent / legacy[key]).resolve())
    if variable:
        sources.add(Path(variable).resolve())
    if output.resolve() in sources:
        raise ValueError('Output must not overwrite an input/template/reference')
    if study:
        # Study commands cannot write to game assets or persistent reference paths.
        repo = path.resolve().parent.parent.parent
        for folder in ('Textures', 'Docs/References'):
            if output.resolve().is_relative_to(repo / folder):
                raise ValueError('Study output must stay outside production/reference folders')
    return output


def scaffold(manifest, output, study=False):
    path, spec = _read_spec(manifest)
    if not study:
        _require_production(spec)
    elif spec.get('layer_model') != CONTACT_MODEL:
        raise ValueError('Study commands require a registered contact contract')
    master, mask = load_template(path)
    output = _output_guard(path, spec, output, study=study)
    if spec.get('layer_model') == CONTACT_MODEL:
        load_contact_contract(path)
        patch = master.copy()  # Intact wood/context, not an empty transparent layer.
    else:
        patch = Image.composite(master, Image.new('RGBA', master.size), mask)
    output.parent.mkdir(parents=True, exist_ok=True)
    patch.save(output, format='PNG')
    print(f'{"STUDY ONLY" if study else "PASS"}: context scaffold created; {output}')


def compose(manifest, variable, output, study=False):
    path, spec = _read_spec(manifest)
    if not study:
        _require_production(spec)
    elif spec.get('layer_model') != CONTACT_MODEL:
        raise ValueError('Study commands require a registered contact contract')
    output = _output_guard(path, spec, output, variable, study)
    master, mask = load_template(path)
    with Image.open(variable) as image:
        image.load()
        layer = image.convert('RGBA')
    validate_variable_layer(path, layer, mask)
    if spec.get('layer_model') == CONTACT_MODEL:
        _, masks, _ = load_contact_contract(path)
        # Input is already rendered with intact master context. Never alpha-over
        # a rendered patch a second time or carve complementary rear/front layers.
        result = Image.composite(master, layer, masks['hard_fixed'])
        validate_contact_final(path, result)
    else:
        mode = spec.get('compose_mode', 'alpha_over')
        if mode == 'replace_rgba':
            result = Image.composite(layer, master, mask)
        elif mode == 'alpha_over':
            result = Image.composite(Image.alpha_composite(master, layer), master, mask)
        else:
            raise ValueError(f'Unsupported compose_mode: {mode}')
        _validate_legacy(master, mask, result)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format='PNG')
    print(f'{"STUDY ONLY: structural gates passed, visual activation pending" if study else "PASS: deterministic composition complete"}; {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['scaffold', 'scaffold-study', 'compose', 'compose-study', 'validate'])
    parser.add_argument('manifest')
    parser.add_argument('image', nargs='?')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.mode in ('scaffold', 'scaffold-study'):
        if args.image or not args.output:
            parser.error('scaffold takes no image and requires --output')
        scaffold(args.manifest, args.output, study=args.mode.endswith('-study'))
        return
    if not args.image:
        parser.error(f'{args.mode} requires an image')
    if args.mode in ('compose', 'compose-study'):
        if not args.output:
            parser.error('compose requires --output')
        compose(args.manifest, args.image, args.output, study=args.mode.endswith('-study'))
        return
    path, spec = _read_spec(args.manifest)
    with Image.open(args.image) as image:
        image.load()
        if image.format != 'PNG':
            raise ValueError('Final output must be lossless PNG')
        candidate = image.convert('RGBA')
    if spec.get('layer_model') == CONTACT_MODEL:
        validate_contact_final(path, candidate)
    elif spec.get('layer_model') == 'rear_contents_front':
        raise ValueError('Superseded rear/front split cannot be validated for production')
    else:
        master, mask = load_template(path)
        _validate_legacy(master, mask, candidate)
    print('PASS: structural validation only; consult manifest production status before use')


if __name__ == '__main__':
    main()
