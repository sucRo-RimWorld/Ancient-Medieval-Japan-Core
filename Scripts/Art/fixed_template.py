"""Compose variable art without changing a template's protected RGBA pixels."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def load_template(manifest_path):
    path = Path(manifest_path)
    spec = json.loads(path.read_text(encoding='utf-8'))
    if spec['version'] != 1:
        raise ValueError('Unsupported manifest version')
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


def compose(manifest, variable, output):
    master, mask = load_template(manifest)
    with Image.open(variable) as image:
        image.load()
        layer = image.convert('RGBA')
    if layer.size != master.size:
        raise ValueError('Variable layer must already match the template canvas')
    # Composite only inside the approved editable region, then restore all fixed pixels.
    merged = Image.alpha_composite(master, layer)
    result = Image.composite(merged, master, mask)
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
    parser.add_argument('mode', choices=['compose', 'validate'])
    parser.add_argument('manifest')
    parser.add_argument('image', help='Variable layer for compose; final PNG for validate')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.mode == 'compose':
        if not args.output:
            parser.error('compose requires --output')
        compose(args.manifest, args.image, args.output)
    else:
        master, mask = load_template(args.manifest)
        with Image.open(args.image) as image:
            image.load()
            if image.format != 'PNG':
                raise ValueError('Final output must be lossless PNG')
            validate(master, mask, image)
        print('PASS: protected RGBA pixel differences = 0')

if __name__ == '__main__':
    main()
