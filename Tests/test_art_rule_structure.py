#!/usr/bin/env python3
"""Regression checks for AMJ art-rule ownership and routing."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ArtRuleStructureTest(unittest.TestCase):
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

    def test_shared_art_style_has_no_family_implementation_contract(self):
        text = read("Docs/ArtStyle.md")
        self.assertIn("AMJ-wide invariants", text)
        self.assertIn("Asset-class style specification", text)
        for forbidden in (
            "HardFixed",
            "ContactZone",
            "ExtensionAllowed",
            "v4-contact-study",
            "blocked_pending_occlusion_validation",
            "AMJ_Masu_Template",
            "AMJ_WorkshopCover_CommonBase",
        ):
            self.assertNotIn(forbidden, text)

    def test_general_texture_pipeline_is_generic_and_intent_based(self):
        text = read("Docs/GoldenPaths/TextureAssetPipeline.md")
        self.assertEqual(text.count("# Texture Asset Pipeline — Golden Path"), 1)
        self.assertIn("Interpret the user's image intent semantically", text)
        self.assertIn("Shared/fixed parts are never regenerated", text)
        for forbidden in (
            "v4-contact-study",
            "blocked_pending_occlusion_validation",
            "HardFixed",
            "ContactZone",
            "「生成」: ImageGen may be used only",
        ):
            self.assertNotIn(forbidden, text)

    def test_boxed_resource_pipeline_is_contents_first_manual_composition(self):
        text = read("Docs/GoldenPaths/BoxedResourceIconPipeline.md")
        self.assertIn("contents source layer", text)
        self.assertIn("adjusted manually in an image editor", text)
        self.assertIn("Docs/ArtStyle.md", text)
        self.assertIn("Docs/GoldenPaths/TextureAssetPipeline.md", text)
        self.assertNotIn("HardFixed", text)
        self.assertNotIn("ContactZone", text)

    def test_workshop_pipeline_has_no_mandatory_preapproval_loop(self):
        text = read("Docs/GoldenPaths/WorkshopCoverPipeline.md")
        self.assertIn("Do not insert a mandatory extra approval round", text)
        self.assertNotIn("obtain author approval", text)

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
        self.assertIn("Tests/test_workshop_cover_template.py", text)
        self.assertNotIn("Tests/test_masu_template.py", text)

    def test_legacy_masu_coordination_tasks_are_archived(self):
        text = read("Docs/Coordination.md")
        for number in range(4, 19):
            ident = f"ART-TEMPLATE-{number:03d}"
            match = re.search(
                rf"(?ms)^### {re.escape(ident)}\b.*?^\*\*Status:\*\* ([^\n]+)",
                text,
            )
            self.assertIsNotNone(match, ident)
            self.assertTrue(
                match.group(1).startswith("ARCHIVED"),
                f"{ident} is not archived: {match.group(1)}",
            )


if __name__ == "__main__":
    unittest.main()
