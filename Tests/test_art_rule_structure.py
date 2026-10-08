#!/usr/bin/env python3
"""Regression checks for AMJ art-rule ownership and routing."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ArtRuleStructureTest(unittest.TestCase):
    def test_shared_documents_are_project_migration_pointers(self):
        for path in ['Docs/ArtStyle.md', 'Docs/DevelopmentGoldenPathGuidelines.md', 'Docs/HistoricalDescriptionGuidelines.md', 'Docs/ModDescriptionGuidelines.md', 'Docs/RetextureImplementationGuidelines.md', 'Docs/WorkshopCoverStyle.md', 'Docs/WorkshopPackaging.md', 'Docs/GoldenPaths/TextureAssetPipeline.md', 'Docs/GoldenPaths/FixedImageTemplates.md', 'Docs/GoldenPaths/WorkshopCoverPipeline.md', 'Docs/References/AMJ_WorkshopCover_Manifest.md']:
            text = read(path)
            self.assertIn("migration pointer only", text)
            self.assertIn("Ancient-Medieval-Japan-Project/blob/main/" + path, text)

    def test_agents_is_routing_layer(self):
        text = read("AGENTS.md")
        for required in (
            "Docs/ArtStyle.md",
            "Docs/GoldenPaths/TextureAssetPipeline.md",
            "Docs/GoldenPaths/FixedImageTemplates.md",
            "Docs/GoldenPaths/BoxedResourceIconPipeline.md",
            "Docs/WorkshopCoverStyle.md",
        ):
            self.assertIn(required, text)
        for forbidden in ("HardFixed", "ContactZone", "v4-contact-study", "blocked_pending_occlusion_validation"):
            self.assertNotIn(forbidden, text)

    def test_boxed_resource_pipeline_is_contents_first_manual_composition(self):
        text = read("Docs/GoldenPaths/BoxedResourceIconPipeline.md")
        self.assertIn("contents source layer", text)
        self.assertIn("adjusted manually in an image editor", text)
        self.assertIn("Docs/ArtStyle.md", text)
        self.assertIn("Docs/GoldenPaths/TextureAssetPipeline.md", text)
        self.assertIn("Scripts/Art/normalize_masu_contents.py", text)
        self.assertIn("deterministic normalizer", text)
        self.assertIn("Scripts/Art/prepare_boxed_resource_candidate.py", text)
        self.assertIn("AMJ_BoxedResource_GenerationQA.json", text)
        self.assertIn("single remaining human gate: final visual acceptance", text)
        self.assertIn("lighter **opaque color**, not reduced alpha", text)
        self.assertIn("never send the full masu composite back through ImageGen", text)
        self.assertIn("does **not** have to be mechanically thinner than the masu rim", text)
        self.assertIn("outline thickness by itself is not a failure", text)
        self.assertIn("Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.png", text)
        self.assertNotIn("HardFixed", text)
        self.assertNotIn("ContactZone", text)

    def test_authoritative_sources_are_excluded_from_workshop_archive(self):
        ignore = read(".workshopignore")
        attrs = read(".gitattributes")
        source_readme = read("Art/Sources/README.md")
        publisher_plus = read("_PublisherPlus.xml")
        staging = read("Scripts/Prepare-WorkshopContent.ps1")

        self.assertIn("\nArt\n", ignore)
        self.assertIn("/Art export-ignore", attrs)
        self.assertIn("/Art/** export-ignore", attrs)
        self.assertIn("/_PublisherPlus.xml export-ignore", attrs)
        self.assertIn("must **never** be included in Steam Workshop content", source_readme)
        self.assertIn("<exclude>Art</exclude>", publisher_plus)
        self.assertIn('Join-Path $outputFull "Art"', staging)

        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "workshop.zip"
            subprocess.run(
                ["git", "archive", "--format=zip", f"--output={archive}", "HEAD"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()
            self.assertFalse(
                any(name == "Art/" or name.startswith("Art/") for name in names),
                "Art leaked into git-archive Workshop staging",
            )

    def test_source_inventory_does_not_promote_texture_derivatives(self):
        source_readme = read("Art/Sources/README.md")
        self.assertIn("Do not copy a `Textures/` derivative", source_readme)
        self.assertTrue((ROOT / "Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.png").exists())
        self.assertTrue((ROOT / "Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.xcf").exists())
        self.assertTrue((ROOT / "Art/Sources/Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png").exists())
        self.assertFalse((ROOT / "Art/Sources/Workshop/AMJ_WorkshopCover_Template.svg").exists())

    def test_archived_masu_manifest_cannot_activate_production(self):
        data = json.loads(read("Docs/References/AMJ_Masu_Template.json"))
        self.assertEqual(data.get("operational_role"), "diagnostic_only")
        self.assertNotEqual(data.get("production_status"), "active")
        self.assertNotEqual(data.get("new_resource_production_status"), "active")
        self.assertEqual(
            data.get("active_production_pipeline"),
            "../GoldenPaths/BoxedResourceIconPipeline.md",
        )

    def test_archived_masu_workflow_is_manual_only(self):
        text = read(".github/workflows/masu-contact-study.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotRegex(text, r"(?m)^\s*push:\s*$")
        self.assertIn("Tests/test_masu_template.py", text)

    def test_stage_a_runs_current_art_guards_not_archived_masu_gate(self):
        text = read(".github/workflows/stage-a-validation.yml")
        self.assertIn("Tests/test_art_rule_structure.py", text)
        self.assertNotIn("Tests/test_workshop_cover_template.py", text)
        self.assertIn("Tests/test_generated_asset_qa.py", text)
        self.assertIn("Tests/test_prepare_boxed_resource_candidate.py", text)
        self.assertNotIn("Tests/test_masu_template.py", text)

    def test_legacy_masu_coordination_tasks_are_archived(self):
        text = read("Docs/Coordination.md")
        lines = text.splitlines()
        found = []
        for i, line in enumerate(lines):
            if not line.startswith("### ART-TEMPLATE-"):
                continue
            ident = line.split()[1]
            try:
                number = int(ident.rsplit("-", 1)[1])
            except (IndexError, ValueError):
                continue
            if not 4 <= number <= 18:
                continue
            found.append(ident)
            status = None
            for later in lines[i + 1:]:
                if later.startswith("### "):
                    break
                if later.startswith("**Status:** "):
                    status = later[len("**Status:** "):]
                    break
            self.assertIsNotNone(status, ident)
            self.assertTrue(
                status.startswith("ARCHIVED"),
                f"{ident} is not archived: {status}",
            )
        self.assertGreaterEqual(len(found), 15)



if __name__ == "__main__":
    unittest.main()

