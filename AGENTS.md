# AMJ Grains Agent Instructions

## Start here

1. Read this file and `main:Docs/Coordination.md`; locate the latest relevant owner/status/evidence, including later corrections. Historical entries are not current approval.
2. Read Project [AGENTS.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/AGENTS.md) and [Docs/SharedRules.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/SharedRules.md): apply its stop conditions, then open only the task-relevant canonical procedures.
3. Read the local specification and affected source/tests below. Shared rules are owned by Project; this file owns only local scope and routing. Missing access or conflicting authority blocks the dependent action, not unrelated safe work.

New features cannot enter implementation before the Project [existing-Mod audit gate](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md#implementation-entry-gate) covers VE and non-VE alternatives and records why independent implementation is needed. Existing approved behavior is not redesigned by this rule audit.

## Local task routes and stops

- `Docs/Design.md` owns grain/processing scope. `Docs/GrainsProfileTesting.md` owns the actual-provider runtime matrix; `Docs/GrainsDependencyAudit.md` owns dependency-removal conditions. Retain IDs and existing save/provider contracts.
- `Docs/Balance/Crops/ColdTolerance.md` owns custom crop values. CCTO remains optional and retains its own Vanilla/MO support data.
- Art: use the routing below, including the boxed-resource family procedure. Do not reactivate archived diagnostic template contracts as production policy.
- Packaging: `Tests/validate_workshop_payload.py`; release metadata: `Tests/validate_add_changenote.py`. Their success proves the named static contracts, not real-game or Steam completion.

## PNG asset integrity gate

Every committed production PNG must pass `python Tests/validate_png_assets.py`. The validator checks every `Textures/**/*.png` for complete chunk boundaries, CRCs, a complete IDAT/zlib stream, valid scanlines, and a final IEND. It reports all broken PNGs found in one run rather than stopping after the first file.

The GitHub Actions `validate-png-assets` job is a prerequisite for Stage A validation. For binary writes made through automation or Git/GitHub APIs, treat the committed/checked-out bytes as authoritative: do not report the image write as successful until the repository-side PNG integrity gate passes. A valid PNG signature, dimensions, or successful viewer open is not sufficient.

## CCTO framework and crop-data ownership

AMJC owns its custom crops' temperature values, design/balance tables (including archived candidate ranges), Def mappings, optional CCTO compatibility XML, and validation. Maintain these here, not in CCTO. Use `Docs/Balance/Crops/ColdTolerance.md` together with the cultivation design and implemented XML as the local source of truth. CCTO remains an optional framework; its own Vanilla/MO support data remains owned by CCTO.

## Art / image work

Keep this file as a routing layer; do not duplicate asset-family procedures here.

For AMJ art, resolve rules in this order:

1. Project `Docs/ArtStyle.md` — project-wide visual language and precedence.
2. The owning asset-class specification — adds subject-specific visual rules only.
3. Project `Docs/GoldenPaths/TextureAssetPipeline.md` — source preservation, generation permission, export, and validation.
4. Project `Docs/GoldenPaths/FixedImageTemplates.md` — only when visible parts are intentionally reused pixel-exactly.

Current asset-class specifications:
- grain/crop source generation: `Docs/GoldenPaths/GrainImageGeneration.md` (entry point: `Scripts/Art/grains_image_generator.py`);
- boxed resources / masu: `Docs/GoldenPaths/BoxedResourceIconPipeline.md`;
- Workshop covers: Project `Docs/WorkshopCoverStyle.md` + Project `Docs/GoldenPaths/WorkshopCoverPipeline.md`;
- prerequisite-Mod retextures: Project `Docs/RetextureImplementationGuidelines.md` plus the owning repository's art specification.

A family-specific document may narrow the shared style for its asset class, but it must not silently replace the AMJ-wide visual language. Any real exception belongs in the owning style specification, not in chat history or AGENTS.

For generation intent and ImageGen use, follow Project `Docs/GoldenPaths/TextureAssetPipeline.md`. Interpret the user's requested image action semantically; do not use an exact-keyword gate, and never regenerate accepted fixed/shared parts merely because new image work was requested.
