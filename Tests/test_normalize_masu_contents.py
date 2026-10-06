import importlib.util
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/Art/normalize_masu_contents.py"

spec = importlib.util.spec_from_file_location("normalize_masu_contents", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NormalizeMasuContentsTest(unittest.TestCase):
    def test_projects_visible_contents_and_cleans_low_alpha_background(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.png"
            output = root / "output.png"

            image = Image.new("RGBA", (100, 80), (255, 0, 0, 3))
            draw = ImageDraw.Draw(image)
            draw.rectangle((20, 10, 80, 70), fill=(220, 210, 190, 255))
            image.save(source)

            module.normalize(
                source,
                output,
                canvas=256,
                alpha_cutoff=40,
            )

            with Image.open(output) as result:
                result.load()
                result = result.convert("RGBA")
                self.assertEqual(result.size, (256, 256))
                self.assertEqual(result.getpixel((0, 0))[3], 0)

                bbox = result.getchannel("A").getbbox()
                self.assertIsNotNone(bbox)
                self.assertGreater(bbox[0], 0)
                self.assertGreater(bbox[1], 0)
                self.assertLess(bbox[2], 256)
                self.assertLess(bbox[3], 256)

    def test_rejects_empty_source_after_alpha_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "empty.png"
            output = root / "output.png"
            Image.new("RGBA", (32, 32), (0, 0, 0, 0)).save(source)

            with self.assertRaisesRegex(ValueError, "no visible alpha"):
                module.normalize(source, output)


if __name__ == "__main__":
    unittest.main()
