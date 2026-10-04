import importlib.util
from pathlib import Path
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Docs/References/AMJ_Masu_Template.json"

spec = importlib.util.spec_from_file_location(
    "fixed_template", ROOT / "Scripts/Art/fixed_template.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MasuTemplateTest(unittest.TestCase):
    def test_registered_masu_template_is_fail_closed(self):
        master, mask = module.load_template(MANIFEST)
        self.assertEqual(master.size, (256, 256))
        self.assertEqual(mask.size, master.size)

        # Interior is editable; rim/exterior/common pixels remain protected.
        self.assertEqual(mask.getpixel((128, 120)), 255)
        self.assertEqual(mask.getpixel((128, 47)), 0)
        self.assertEqual(mask.getpixel((45, 115)), 0)
        self.assertEqual(mask.getpixel((128, 190)), 0)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            variable = root / "variable.png"
            output = root / "output.png"
            Image.new("RGBA", master.size, (255, 0, 255, 255)).save(variable)

            module.compose(MANIFEST, variable, output)
            with Image.open(output) as result:
                result.load()
                module.validate(master, mask, result)
                result = result.convert("RGBA")
                for m, expected, actual in zip(
                    mask.get_flattened_data(),
                    master.get_flattened_data(),
                    result.get_flattened_data(),
                ):
                    if m == 0:
                        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
