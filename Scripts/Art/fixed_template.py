"""Compose variable art without changing a template's protected RGBA pixels."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def load_template(manifest_path, allow_inactive=False):
    path = Path(manifest_path)
    spec = json.loads(path.read_text(encoding='utf-8'))
    if spec['version'] != 1:
        raise ValueError('Unsupported manifest version')
    status = spec.get('production_status', 'active')
    if status != 'active' and not allow_inactive:
        raise ValueError(f'Template is not active for production: {status}')
    images = []
    for key in ('master', 'editable_mask'):
        entry = spec[key]
        source = path.parent / entry['path']
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'{key}: SHA-256 mismatch')
        with Image.open(source) as image:
            image.load()
            if key == 'editable_mask' and image.mode != 'L':
                raise ValueError('Mask must be an 8-bit grayscale PNG')
            images.append(image.convert('RGBA') if key == 'master' else image.copy())
    master, mask = images
    if master.size != tuple(spec['size']) or mask.size != master.size:
        raise ValueError('Template/mask dimensions mismatch')
    values = set(mask.get_flattened_data())
    if not values <= {0, 255} or values != {0, 255}:
        raise ValueError('Mask must contain both protected 0 and editable 255 pixels only')
    return master, mask


def validate(master, mask, candidate):
    if candidate.size != master.size:
        raise ValueError('Output dimensions mismatch; resizing is forbidden')
    candidate = candidate.convert('RGBA')
    changed = sum(a != b and m == 0 for a, b, m in
                  zip(master.get_flattened_data(), candidate.get_flattened_data(), mask.get_flattened_data()))
    if changed:
        raise ValueError(f'{changed} protected RGBA pixels changed')
    return candidate



def validate_variable_layer(manifest_path, layer, mask=None):
    path = Path(manifest_path)
    spec = json.loads(path.read_text(encoding='utf-8'))
    master, registered_mask = load_template(path)
    if mask is None:
        mask = registered_mask
    layer = layer.convert('RGBA')
    if layer.size != tuple(spec['size']):
        raise ValueError('Variable layer must match template canvas')
    alpha = layer.getchannel('A')
    master_alpha = master.getchannel('A')
    threshold = int(spec.get('required_fill', {}).get('alpha_threshold', 1))
    req = spec.get('required_fill')
    mode = spec.get('compose_mode', 'alpha_over')

    if spec.get('enforce_variable_within_editable', bool(req)):
        outside = sum(
            a >= threshold and m == 0
            for a, m in zip(alpha.get_flattened_data(), mask.get_flattened_data())
        )
        if outside:
            raise ValueError(f'Variable layer has {outside} nontransparent pixels outside allowed fill region')

    # replace_rgba patches are complete rendered cavity states, not transparent
    # object-only overlays.  Every normally opaque master pixel inside the
    # editable region must therefore remain defined in the patch.
    if mode == 'replace_rgba':
        holes = sum(
            m == 255 and ma >= threshold and la < threshold
            for la, ma, m in zip(
                alpha.get_flattened_data(),
                master_alpha.get_flattened_data(),
                mask.get_flattened_data(),
            )
        )
        if holes:
            raise ValueError(f'Variable patch has {holes} transparent holes inside editable region')

    if req:
        req_path = path.parent / req['path']
        if hashlib.sha256(req_path.read_bytes()).hexdigest() != req['sha256']:
            raise ValueError('required_fill: SHA-256 mismatch')
        with Image.open(req_path) as image:
            image.load()
            if image.mode != 'L':
                raise ValueError('Required-fill guide must be an 8-bit grayscale PNG')
            required = image.copy()
        if required.size != layer.size or not set(required.get_flattened_data()) <= {0, 255}:
            raise ValueError('Invalid required-fill guide')
        required_pixels = [i for i, v in enumerate(required.get_flattened_data()) if v == 255]
        if not required_pixels:
            raise ValueError('Required-fill guide is empty')

        minimum = float(req.get('min_alpha_coverage', 0.0))
        if mode == 'replace_rgba':
            # A complete patch includes the empty cavity/background too, so
            # alpha coverage would always look full.  Measure actual resource
            # occupancy by RGBA change from the registered empty master.
            layer_pixels = list(layer.get_flattened_data())
            master_pixels = list(master.get_flattened_data())
            changed = [a != b for a, b in zip(layer_pixels, master_pixels)]
            covered = sum(changed[i] for i in required_pixels) / len(required_pixels)
            changed_mask = Image.new('L', layer.size, 0)
            changed_mask.putdata([255 if c else 0 for c in changed])
            bbox = changed_mask.getbbox()
        else:
            alpha_values = list(alpha.get_flattened_data())
            covered = sum(alpha_values[i] >= threshold for i in required_pixels) / len(required_pixels)
            bbox = alpha.point(lambda v: 255 if v >= threshold else 0).getbbox()

        if covered < minimum:
            raise ValueError(f'Variable layer under-fills required region: {covered:.3f} < {minimum:.3f}')
        req_bbox = required.getbbox()
        if bbox is None or bbox[0] > req_bbox[0] or bbox[1] > req_bbox[1] or bbox[2] < req_bbox[2] or bbox[3] < req_bbox[3]:
            raise ValueError('Variable layer does not span required fill bbox')
    return layer


def scaffold(manifest, output):
    master, mask = load_template(manifest)
    transparent = Image.new('RGBA', master.size, (0, 0, 0, 0))
    patch = Image.composite(master, transparent, mask)

    output = Path(output)
    if output.suffix.lower() != '.png':
        raise ValueError('Lossless PNG output required')
    output.parent.mkdir(parents=True, exist_ok=True)
    patch.save(output, format='PNG')

    # Scaffold is intentionally NOT a valid finished variable patch yet:
    # until resource art is added it must fail the required-fill occupancy gate.
    print(f'PASS: editable RGBA scaffold created from registered master; {output}')


def compose(manifest, variable, output):
    master, mask = load_template(manifest)
    with Image.open(variable) as image:
        image.load()
        layer = image.convert('RGBA')
    if layer.size != master.size:
        raise ValueError('Variable layer must already match the template canvas')
    validate_variable_layer(manifest, layer, mask)
    # Compose according to the registered family contract.
    # replace_rgba is required when the variable layer already contains the exact
    # antialiased/occluded RGBA for the editable cavity; alpha-over would blend
    # those pixels with the empty master a second time and cannot reconstruct the
    # approved exemplar exactly.
    spec = json.loads(Path(manifest).read_text(encoding='utf-8'))
    mode = spec.get('compose_mode', 'alpha_over')
    if mode == 'replace_rgba':
        result = Image.composite(layer, master, mask)
    elif mode == 'alpha_over':
        merged = Image.alpha_composite(master, layer)
        result = Image.composite(merged, master, mask)
    else:
        raise ValueError(f'Unsupported compose_mode: {mode}')
    validate(master, mask, result)
    output = Path(output)
    if output.suffix.lower() != '.png':
        raise ValueError('Lossless PNG output required')
    source_paths = [Path(manifest).resolve(), Path(variable).resolve()]
    spec = json.loads(Path(manifest).read_text(encoding='utf-8'))
    source_paths += [(Path(manifest).parent / spec[k]['path']).resolve()
                     for k in ('master', 'editable_mask')]
    if output.resolve() in source_paths:
        raise ValueError('Output must not overwrite an input/template')
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format='PNG')
    with Image.open(output) as image:
        image.load()
        validate(master, mask, image)
    print(f'PASS: protected RGBA pixel differences = 0; {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['scaffold', 'compose', 'validate'])
    parser.add_argument('manifest')
    parser.add_argument('image', nargs='?', help='Variable patch for compose; final PNG for validate')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.mode == 'scaffold':
        if args.image:
            parser.error('scaffold does not take an image argument')
        if not args.output:
            parser.error('scaffold requires --output')
        scaffold(args.manifest, args.output)
    elif args.mode == 'compose':
        if not args.image:
            parser.error('compose requires a variable patch image')
        if not args.output:
            parser.error('compose requires --output')
        compose(args.manifest, args.image, args.output)
    else:
        if not args.image:
            parser.error('validate requires a final PNG')
        master, mask = load_template(args.manifest)
        with Image.open(args.image) as image:
            image.load()
            if image.format != 'PNG':
                raise ValueError('Final output must be lossless PNG')
            validate(master, mask, image)
        print('PASS: protected RGBA pixel differences = 0')

if __name__ == '__main__':
    main()
