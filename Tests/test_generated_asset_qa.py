import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/Art/generated_asset_qa.py"

spec = importlib.util.spec_from_file_location("generated_asset_qa", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules["generated_asset_qa"] = module
spec.loader.exec_module(module)


def make_candidate(path: Path, *, heavy_internal: bool) -> None:
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (40, 70, 216, 190),
        radius=35,
        fill=(235, 220, 180, 255),
        outline=(30, 25, 20, 255),
        width=12,
    )
    color = (40, 35, 30, 255) if heavy_internal else (190, 170, 135, 255)
    width = 6 if heavy_internal else 2
    for x in (90, 130, 170):
        draw.line((x, 85, x - 10, 175), fill=color, width=width)
    image.save(path)


class GeneratedAssetQaTest(unittest.TestCase):
    def test_line_hierarchy_metrics_distinguish_heavy_internal_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.png"
            bad = root / "bad.png"
            make_candidate(good, heavy_internal=False)
            make_candidate(bad, heavy_internal=True)

            good_metrics = module.analyze(good)
            bad_metrics = module.analyze(bad)

            self.assertLess(
                good_metrics["internal_dark_edge_fraction_lt140"],
                bad_metrics["internal_dark_edge_fraction_lt140"],
            )
            self.assertGreater(
                good_metrics["line_hierarchy_ratio"],
                bad_metrics["line_hierarchy_ratio"],
            )
            self.assertLess(
                good_metrics["coarse_color_bins_16_at_64"],
                bad_metrics["coarse_color_bins_16_at_64"],
            )

    def test_policy_can_accept_light_internal_lines_and_reject_heavy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.png"
            bad = root / "bad.png"
            policy = root / "policy.json"
            make_candidate(good, heavy_internal=False)
            make_candidate(bad, heavy_internal=True)
            policy.write_text(
                json.dumps(
                    {
                        "allowed_formats": ["PNG"],
                        "require_visible_content": True,
                        "metric_ranges": {
                            "transparent_fraction": {"min": 0.25},
                            "internal_dark_edge_fraction_lt140": {"max": 0.30},
                            "line_hierarchy_ratio": {"min": 3.5},
                            "coarse_color_bins_16_at_64": {"max": 30}
                        }
                    }
                ),
                encoding="utf-8",
            )

            self.assertTrue(module.validate(good, policy)["passed"])
            rejected = module.validate(bad, policy)
            self.assertFalse(rejected["passed"])
            self.assertGreaterEqual(len(rejected["failures"]), 1)

    def test_empty_candidate_fails_visible_content_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty.png"
            policy = root / "policy.json"
            Image.new("RGBA", (64, 64), (0, 0, 0, 0)).save(empty)
            policy.write_text(
                json.dumps(
                    {
                        "allowed_formats": ["PNG"],
                        "require_visible_content": True,
                        "metric_ranges": {}
                    }
                ),
                encoding="utf-8",
            )
            result = module.validate(empty, policy)
            self.assertFalse(result["passed"])
            self.assertIn("candidate has no visible content", result["failures"])


if __name__ == "__main__":
    unittest.main()
