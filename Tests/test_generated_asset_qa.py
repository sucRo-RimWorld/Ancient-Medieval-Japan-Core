import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

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
    def test_valid_transparent_candidate_passes_without_style_thresholds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.png"
            make_candidate(candidate, heavy_internal=True)
            policy = ROOT / "Docs/References/AMJ_BoxedResource_GenerationQA.json"
            result = module.validate(candidate, policy)
            self.assertTrue(result["passed"], result["failures"])
            # A stale subjective threshold may not silently become a blocker.
            legacy_policy = root / "legacy.json"
            legacy_policy.write_text(json.dumps({
                "allowed_formats": ["PNG"],
                "require_visible_content": True,
                "require_transparency": True,
                "metric_ranges": {"line_hierarchy_ratio": {"min": 1000000}}
            }), encoding="utf-8")
            self.assertTrue(module.validate(candidate, legacy_policy)["passed"])

    def test_empty_candidate_fails_visible_content_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty.png"
            Image.new("RGBA", (64, 64), (0, 0, 0, 0)).save(empty)
            policy = ROOT / "Docs/References/AMJ_GeneratedAsset_BaseQA.json"
            result = module.validate(empty, policy)
            self.assertFalse(result["passed"])
            self.assertIn("candidate has no visible content", result["failures"])

    def test_opaque_candidate_fails_isolated_asset_transparency_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            opaque = Path(tmp) / "opaque.png"
            Image.new("RGB", (64, 64), (235, 220, 180)).save(opaque)
            policy = ROOT / "Docs/References/AMJ_GeneratedAsset_BaseQA.json"
            result = module.validate(opaque, policy)
            self.assertFalse(result["passed"])
            self.assertIn("candidate has no transparent background", result["failures"])


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

    def test_prepare_then_review_end_to_end_without_api(self):
        awa = (
            ROOT
            / "Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png"
        )
        self.assertTrue(awa.is_file())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subject = root / "subject-wheat.png"
            candidate = root / "candidate.png"
            work = root / "work"
            mo_zip = root / "medieval-overhaul.zip"

            shutil.copyfile(awa, subject)
            shutil.copyfile(awa, candidate)
            with zipfile.ZipFile(mo_zip, "w") as archive:
                archive.write(
                    awa,
                    "FakeMO/Textures/Things/Plants/FullGrown/WheatPlant/"
                    "PlantWheat_Mature.png",
                )

            prepare_args = argparse.Namespace(
                family="plant-mature",
                subject="wheat",
                subject_reference=[subject],
                notes="mechanical end-to-end workflow test",
                mo_root=None,
                mo_zip=mo_zip,
                allow_no_mo_reference=False,
                policy=ROOT / "Docs/References/AMJ_Grains_ImageGenerator.json",
                output_dir=work,
            )
            self.assertEqual(generator._prepare(prepare_args), 0)

            manifest = json.loads(
                (work / "manifest.json").read_text(encoding="utf-8")
            )
            request = json.loads(
                (work / "generation-request.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], 2)
            self.assertEqual(manifest["status"], "prepared")
            self.assertFalse(manifest["generation"]["python_calls_image_api"])
            self.assertFalse(manifest["generation"]["api_key_required"])
            self.assertFalse(request["api_key_required"])
            self.assertFalse(request["automatic_retry"])
            self.assertEqual(request["image_count"], 1)
            self.assertEqual(len(manifest["references"]), 5)
            for item in manifest["references"]:
                bundled = work / item["bundle_path"]
                self.assertTrue(bundled.is_file())
                self.assertEqual(
                    generator._sha256(bundled.read_bytes()),
                    item["sha256"],
                )

            review_args = argparse.Namespace(
                work_dir=work,
                candidate=candidate,
            )
            self.assertEqual(generator._review(review_args), 0)

            reviewed = json.loads(
                (work / "manifest.json").read_text(encoding="utf-8")
            )
            qa = json.loads(
                (work / "qa-report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(reviewed["status"], "automatic-qa-passed")
            self.assertTrue(reviewed["automatic_qa_passed"])
            self.assertTrue(reviewed["semantic_visual_review_required"])
            self.assertFalse(reviewed["pre_display_screening_claimed"])
            self.assertTrue(qa["passed"])
            self.assertTrue((work / "candidate-source.png").is_file())
            self.assertTrue((work / "review-sheet.png").is_file())
            self.assertEqual(
                (work / "candidate-source.png").read_bytes(),
                candidate.read_bytes(),
            )

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
