import hashlib
import importlib.util
import json
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
    def test_v2_identity_exemplar_round_trips_at_zero_rgba_diff(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["template_revision"], "v2")
        self.assertEqual(data["production_status"], "active")
        self.assertEqual(data["compose_mode"], "replace_rgba")

        master, allowed = module.load_template(MANIFEST)
        self.assertEqual(master.size, (256, 256))
        self.assertEqual(master.getchannel("A").getbbox(), tuple(data["master_alpha_bbox"]))
        self.assertEqual(allowed.getbbox(), tuple(data["editable_bbox"]))

        req_path = MANIFEST.parent / data["required_fill"]["path"]
        rep_path = MANIFEST.parent / data["representative_final"]["path"]
        var_path = MANIFEST.parent / data["identity_exemplar"]["variable_layer_path"]

        self.assertEqual(hashlib.sha256(req_path.read_bytes()).hexdigest(), data["required_fill"]["sha256"])
        self.assertEqual(hashlib.sha256(rep_path.read_bytes()).hexdigest(), data["representative_final"]["sha256"])
        self.assertEqual(hashlib.sha256(var_path.read_bytes()).hexdigest(), data["identity_exemplar"]["variable_layer_sha256"])

        with Image.open(req_path) as image:
            required = image.convert("L")
        self.assertEqual(required.getbbox(), tuple(data["required_fill_bbox"]))
        for a, r in zip(allowed.get_flattened_data(), required.get_flattened_data()):
            if r == 255:
                self.assertEqual(a, 255)

        with Image.open(rep_path) as image:
            representative = image.convert("RGBA")
        with Image.open(var_path) as image:
            variable = image.convert("RGBA")

        module.validate_variable_layer(MANIFEST, variable, allowed)

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "identity.png"
            module.compose(MANIFEST, var_path, output)
            with Image.open(output) as image:
                recomposed = image.convert("RGBA")

        differing_pixels = sum(
            a != b
            for a, b in zip(
                recomposed.get_flattened_data(),
                representative.get_flattened_data(),
            )
        )
        self.assertEqual(differing_pixels, data["identity_exemplar"]["required_rgba_diff_pixels"])

        # Protected/common pixels remain exact copies of the empty master.
        protected_diffs = sum(
            m == 0 and a != b
            for a, b, m in zip(
                master.get_flattened_data(),
                recomposed.get_flattened_data(),
                allowed.get_flattened_data(),
            )
        )
        self.assertEqual(protected_diffs, 0)

        tiny = Image.new("RGBA", master.size, (0, 0, 0, 0))
        for y in range(100, 130):
            for x in range(105, 150):
                tiny.putpixel((x, y), (100, 60, 40, 255))
        with self.assertRaisesRegex(ValueError, "required"):
            module.validate_variable_layer(MANIFEST, tiny, allowed)


if __name__ == "__main__":
    unittest.main()
