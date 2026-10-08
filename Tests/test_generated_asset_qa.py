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



GENERATOR_SCRIPT = ROOT / "Scripts/Art/grains_image_generator.py"
generator_spec = importlib.util.spec_from_file_location(
    "grains_image_generator",
    GENERATOR_SCRIPT,
)
generator = importlib.util.module_from_spec(generator_spec)
sys.modules["grains_image_generator"] = generator
generator_spec.loader.exec_module(generator)


class GrainsImageGeneratorTest(unittest.TestCase):
    @staticmethod
    def _png_bytes():
        import io

        out = io.BytesIO()
        Image.new("RGBA", (32, 32), (0, 0, 0, 0)).save(out, format="PNG")
        return out.getvalue()

    def test_prompt_locks_single_asset_and_reference_roles(self):
        ref = generator._reference_from_bytes(
            "accepted AMJ style reference",
            "fake.png",
            "fake.png",
            self._png_bytes(),
        )
        prompt = generator._build_prompt(
            "wheat",
            "plant-mature",
            {"prompt_rules": ["No gradients."]},
            [ref],
            "upright mature head",
        )
        self.assertIn("exactly ONE NEW isolated source image", prompt)
        self.assertIn("accepted AMJ style reference", prompt)
        self.assertIn("No gradients.", prompt)
        self.assertIn("upright mature head", prompt)
        self.assertIn("transparent background", prompt.lower())

    def test_generator_rejects_authoritative_output_tree(self):
        old_roots = generator.PROTECTED_OUTPUT_ROOTS
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            protected = root / "Textures"
            protected.mkdir()
            generator.PROTECTED_OUTPUT_ROOTS = (protected,)
            try:
                with self.assertRaisesRegex(generator.GenerationError, "protected"):
                    generator._assert_safe_output(protected / "bad")
                generator._assert_safe_output(root / "Work" / "ok")
            finally:
                generator.PROTECTED_OUTPUT_ROOTS = old_roots

    def test_prepare_bundle_preserves_reference_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref = generator._reference_from_bytes(
                "subject identity reference",
                "subject.png",
                "subject.png",
                self._png_bytes(),
            )
            bundled = generator._write_reference_bundle(root, [ref])
            self.assertEqual(len(bundled), 1)
            copied = root / bundled[0]["bundle_path"]
            self.assertEqual(copied.read_bytes(), ref.data)
            self.assertEqual(bundled[0]["sha256"], ref.sha256)

    def test_generator_policy_is_api_free_and_has_no_retry_batch(self):
        policy_path = ROOT / "Docs/References/AMJ_Grains_ImageGenerator.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        self.assertEqual(policy["schema_version"], 1)
        self.assertEqual(
            policy["generation_workflow"]["provider"],
            "ChatGPT built-in image generation",
        )
        self.assertFalse(policy["generation_workflow"]["python_calls_image_api"])
        self.assertFalse(policy["generation_workflow"]["api_key_required"])
        self.assertFalse(policy["generation_workflow"]["automatic_retry"])
        self.assertIn("plant-mature", policy["families"])
        self.assertIn("boxed-contents", policy["families"])
        for family in policy["families"].values():
            self.assertNotIn("retries", family)
            self.assertNotIn("batch", family)
            for relative in family.get("accepted_references", []):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_generator_source_contains_no_paid_api_path(self):
        source = GENERATOR_SCRIPT.read_text(encoding="utf-8")
        forbidden = (
            "OPENAI_API_KEY",
            "api.openai.com",
            "urllib.request",
            "/v1/images",
            "b64_json",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)
        self.assertIn("ChatGPT built-in image generation", source)
        self.assertIn('"prepare"', source)
        self.assertIn('"review"', source)


if __name__ == "__main__":
    unittest.main()
