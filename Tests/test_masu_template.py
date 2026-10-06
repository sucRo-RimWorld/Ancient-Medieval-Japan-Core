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
    def test_new_resource_production_is_fail_closed_after_occlusion_audit(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(
            data["new_resource_production_status"],
            "blocked_pending_occlusion_validation",
        )
        self.assertEqual(
            data["v3_split_status"],
            "superseded_due_visible_split_damage",
        )
        self.assertEqual(
            data["next_layer_model"],
            "intact_master_base__contents_contact__hard_fixed_foreground",
        )
        self.assertIn("occludable", data["contact_region_policy"])

        master, mask = module.load_template(MANIFEST)
        self.assertEqual(master.size, (256, 256))

        # Existing approved identity evidence remains registered and hashed.
        legacy = data["legacy_identity_exemplar"]
        legacy_path = MANIFEST.parent / legacy["variable_layer_path"]
        expected_path = MANIFEST.parent / legacy["expected_final_path"]
        self.assertEqual(
            hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
            legacy["variable_layer_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(expected_path.read_bytes()).hexdigest(),
            legacy["expected_final_sha256"],
        )

        # The old generic three-layer path may remain as historical code, but it
        # cannot produce a new resource while the occlusion contract is blocked.
        contents = Image.new("RGBA", master.size, (0, 0, 0, 0))
        for y in range(70, 145):
            for x in range(55, 200):
                contents.putpixel((x, y), (180, 150, 105, 255))

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "contents.png"
            output = Path(tmp) / "final.png"
            contents.save(source)
            with self.assertRaisesRegex(ValueError, "production is blocked"):
                module.compose(MANIFEST, source, output)


if __name__ == "__main__":
    unittest.main()
