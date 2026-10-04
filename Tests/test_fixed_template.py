import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image

spec = importlib.util.spec_from_file_location('fixed_template', Path(__file__).resolve().parents[1] / 'Scripts/Art/fixed_template.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FixedTemplateTest(unittest.TestCase):
    def test_protection_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = Image.new('RGBA', (4, 4), (10, 20, 30, 128))
            master.save(root / 'master.png')
            mask = Image.new('L', (4, 4), 0)
            mask.putpixel((2, 2), 255)
            mask.save(root / 'mask.png')
            manifest = {'version': 1, 'size': [4, 4]}
            for key, filename in [('master', 'master.png'), ('editable_mask', 'mask.png')]:
                manifest[key] = {'path': filename, 'sha256': hashlib.sha256((root / filename).read_bytes()).hexdigest()}
            (root / 'template.json').write_text(json.dumps(manifest))
            Image.new('RGBA', (4, 4), (250, 0, 0, 255)).save(root / 'variable.png')
            module.compose(root / 'template.json', root / 'variable.png', root / 'out.png')
            with Image.open(root / 'out.png') as result:
                module.validate(master, mask, result)
                self.assertEqual(result.getpixel((0, 0)), (10, 20, 30, 128))
                self.assertEqual(result.getpixel((2, 2)), (250, 0, 0, 255))
                changed = result.copy()
            changed.putpixel((0, 0), (10, 20, 30, 127))
            with self.assertRaisesRegex(ValueError, 'protected'):
                module.validate(master, mask, changed)
            with self.assertRaisesRegex(ValueError, 'dimensions'):
                module.validate(master, mask, Image.new('RGBA', (8, 8)))
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                module.compose(root / 'template.json', root / 'variable.png', root / 'master.png')
            (root / 'master.png').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                module.load_template(root / 'template.json')

if __name__ == '__main__':
    unittest.main()
