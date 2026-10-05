import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Docs/References/AMJ_Masu_Template.json"

spec = importlib.util.spec_from_file_location(
    "fixed_template", ROOT / "Scripts/Art/fixed_template.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MasuTemplateTest(unittest.TestCase):
    def test_v1_is_blocked_until_visual_contract_is_rebuilt(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["production_status"], "blocked_visual_mismatch")
        self.assertEqual(data["visual_reference"]["normalized_alpha_bbox"], [17, 28, 239, 235])
        self.assertEqual(data["master_alpha_bbox"], [34, 42, 232, 213])
        self.assertIn("required-fill", " ".join(data["activation_requirements"]))

        with self.assertRaisesRegex(ValueError, "not active for production"):
            module.load_template(MANIFEST)

        master, mask = module.load_template(MANIFEST, allow_inactive=True)
        self.assertEqual(master.size, (256, 256))
        self.assertEqual(mask.size, master.size)
        self.assertEqual(master.getchannel("A").getbbox(), tuple(data["master_alpha_bbox"]))

        # v1 still protects the intended structural pixels, but must not be used
        # for production derivatives until v2 passes the visual composition gate.
        self.assertEqual(mask.getpixel((128, 120)), 255)
        self.assertEqual(mask.getpixel((128, 47)), 0)
        self.assertEqual(mask.getpixel((45, 115)), 0)
        self.assertEqual(mask.getpixel((128, 190)), 0)


if __name__ == "__main__":
    unittest.main()
