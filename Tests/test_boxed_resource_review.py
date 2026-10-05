import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/Art/boxed_resource_review.py"
MANIFEST = ROOT / "Docs/References/AMJ_Masu_Template.json"

spec = importlib.util.spec_from_file_location("boxed_review", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BoxedResourceReviewTest(unittest.TestCase):
    def test_registered_reference_is_hash_verified(self):
        data, ref_path, reference = module.load_registered_reference(MANIFEST)
        self.assertEqual(reference.size, tuple(data["size"]))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.png"
            output = root / "review.png"
            reference.save(candidate)
            module.render_review(MANIFEST, candidate, output)
            self.assertTrue(output.is_file())

            bad_manifest = root / "bad.json"
            bad = json.loads(MANIFEST.read_text(encoding="utf-8"))
            bad["representative_final"]["path"] = str(ref_path)
            bad["representative_final"]["sha256"] = "0" * 64
            bad_manifest.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                module.load_registered_reference(bad_manifest)


if __name__ == "__main__":
    unittest.main()
