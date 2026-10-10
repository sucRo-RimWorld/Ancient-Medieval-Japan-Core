import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/Art/prepare_boxed_resource_candidate.py"

spec = importlib.util.spec_from_file_location("prepare_boxed_resource_candidate", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules["prepare_boxed_resource_candidate"] = module
spec.loader.exec_module(module)


def make_candidate(path: Path) -> None:
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (40, 70, 216, 190),
        radius=35,
        fill=(235, 220, 180, 255),
        outline=(30, 25, 20, 255),
        width=12,
    )
    for x in (90, 130, 170):
        draw.line((x, 85, x - 10, 175), fill=(190, 170, 135, 255), width=2)
    image.save(path)


class PrepareBoxedResourceCandidateTest(unittest.TestCase):
    def test_prepare_writes_projected_candidate_reports_and_review_sheet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.png"
            out = root / "out"
            policy = root / "policy.json"
            make_candidate(source)
            policy.write_text(
                json.dumps(
                    {
                        "allowed_formats": ["PNG"],
                        "require_visible_content": True,
                        "require_transparency": True
                    }
                ),
                encoding="utf-8",
            )

            summary = module.prepare(source, out, policy)

            self.assertTrue(summary["passed"])
            self.assertTrue((out / "contents-projected.png").is_file())
            self.assertTrue((out / "mechanical-qa-raw.json").is_file())
            self.assertTrue((out / "mechanical-qa-projected.json").is_file())
            self.assertTrue((out / "review-sheet.png").is_file())
            self.assertTrue((out / "summary.json").is_file())

            with Image.open(out / "contents-projected.png") as projected:
                projected.load()
                self.assertEqual(projected.mode, "RGBA")
                self.assertGreater(
                    projected.getchannel("A").histogram()[0],
                    0,
                )


if __name__ == "__main__":
    unittest.main()
