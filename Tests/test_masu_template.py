import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Docs/References/AMJ_Masu_Template.json"

spec = importlib.util.spec_from_file_location(
    "fixed_template", ROOT / "Scripts/Art/fixed_template.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MasuTemplateTest(unittest.TestCase):
    def test_layered_masu_reconstructs_master_and_occludes_contents(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["template_revision"], "v3-layered")
        self.assertEqual(data["master_revision"], "v2")
        self.assertEqual(data["layer_model"], "rear_contents_front")
        self.assertEqual(data["content_clipping"], "none")

        master, rear, front, front_mask = module.build_three_layer_stack(MANIFEST)
        self.assertEqual(master.size, (256, 256))

        empty = Image.alpha_composite(rear, front)
        differing = sum(
            a != b
            for a, b in zip(
                empty.get_flattened_data(), master.get_flattened_data()
            )
        )
        self.assertEqual(differing, 0)

        # Three-layer scaffold is transparent object-only contents.
        with tempfile.TemporaryDirectory() as tmp:
            scaffold_path = Path(tmp) / "contents.png"
            module.scaffold(MANIFEST, scaffold_path)
            with Image.open(scaffold_path) as image:
                contents = image.convert("RGBA")
            self.assertIsNone(contents.getchannel("A").getbbox())

        # Synthetic contents intentionally cross the front rim.  They are not
        # pre-clipped; the fixed foreground must occlude them exactly.
        contents = Image.new("RGBA", master.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(contents)
        draw.polygon(
            [(128, 52), (214, 104), (128, 170), (42, 104)],
            fill=(190, 165, 120, 255),
        )

        with tempfile.TemporaryDirectory() as tmp:
            contents_path = Path(tmp) / "contents.png"
            output_path = Path(tmp) / "final.png"
            contents.save(contents_path)
            module.compose(MANIFEST, contents_path, output_path)
            with Image.open(output_path) as image:
                result = image.convert("RGBA")

        front_diffs = sum(
            m == 255 and a != b
            for a, b, m in zip(
                result.get_flattened_data(),
                master.get_flattened_data(),
                front_mask.get_flattened_data(),
            )
        )
        self.assertEqual(front_diffs, 0)
        self.assertNotEqual(result.getpixel((128, 110)), master.getpixel((128, 110)))

        # Blank contents must not pass the required-fill gate.
        blank = Image.new("RGBA", master.size, (0, 0, 0, 0))
        middle = Image.alpha_composite(rear, blank)
        blank_final = Image.composite(front, middle, front_mask)
        with self.assertRaisesRegex(ValueError, "under-fills"):
            module.validate_three_layer_final(MANIFEST, blank_final)

        # Historical editable mask remains registered but is not the compositor.
        editable_path = MANIFEST.parent / data["editable_mask"]["path"]
        self.assertEqual(
            hashlib.sha256(editable_path.read_bytes()).hexdigest(),
            data["editable_mask"]["sha256"],
        )
        self.assertIn("not used to clip", data["editable_mask_role"])


if __name__ == "__main__":
    unittest.main()
