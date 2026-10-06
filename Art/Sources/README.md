# AMJ Authoritative Art Sources

This directory stores accepted source artwork and authoring files that must survive independently of production-resolution exports.

## Rules

- Once the author accepts an image, preserve the exact accepted source here as an **immutable master** before creating or replacing production derivatives.
- Never overwrite a source merely to make a 256×256 game texture.
- Derive production PNGs from a copy/export and write them under `Textures/`.
- Preserve the source file's original pixel dimensions, alpha, and authoring structure unless the author explicitly approves a new master.
- Keep editable authoring files such as GIMP `.xcf` files beside the corresponding rendered master when they are part of the accepted source.
- Mirror the `Textures/` relative asset path beneath `Art/Sources/` where practical so source and derivative are easy to pair.
- If an already-approved master survives elsewhere (for example a persistent reference store), migrate the **exact accepted bytes** here when that asset is next touched. Do not substitute a production-resolution derivative or regenerated approximation for a missing source.
- A source is not considered repository-preserved until the exact file is actually committed here.

## Current authoritative sources

- `Shared/Containers/AMJ_Masu_Empty_Master.png`
- `Shared/Containers/AMJ_Masu_Empty_Master.xcf`
- `Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png`
- `Workshop/AMJ_WorkshopCover_Template.svg`
- `Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`

Do not copy a `Textures/` derivative into this tree merely to make the inventory look complete. Historical accepted assets whose exact higher-resolution/source bytes still survive elsewhere should be migrated here only from those exact bytes. If only the production derivative remains, keep that limitation explicit rather than relabeling the derivative as an original source.

Additional accepted sources should be added to the corresponding mirrored path as they are finalized or recovered.

## Recovered historical sources

### Soba mature plant — 2026-10-07 JST

- Archived file: `Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`.
- Original: `そばの実と花をつけた植物アイコン.png`, Library identity `libfile_a3c815e98f708191aee6d27f9b740a9b`.
- Original dimensions: 1247×1261 RGBA; 779,854 bytes. Preserved without resizing, recoloring, or re-encoding.
- SHA-256: `4899ea7fa6aed00d87b78819b26148b74ff5404c6e28ab050b5ad4042c08d97c`.
- Production counterpart: `Textures/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png` (256×256).
- Provenance: the accepted-source recovery recorded in `AMJ-009-ART-SOBA-PLANT` and the dedicated production integration commit `c7d5d2c229119aac717de80718ff7c2bdb92a00d`. Visual comparison confirms the same stem, triangular fruit clusters, leaves, flowers, and silhouette; the preceding `そばの実と花の植物アイコン.png` is a different rejected/earlier composition and was not archived.
- The production counterpart is palette-encoded and is not a byte/pixel-identical direct resize of this original; the historical full export recipe has not been reconstructed. This recovery preserves the original only and does not change production files.

## Workshop distribution

The repository-root `Art/` tree is development-only material and must **never** be included in Steam Workshop content.

- `.rimignore` excludes the root `Art` directory for YADA Workshop uploads.
- `.workshopignore` records the same whole-`Art/` exclusion for uploaders that support that file.
- `_PublisherPlus.xml` excludes `Art` when publishing through RimWorld's PublisherPlus workflow.
- The fail-closed publication path is `Scripts/Prepare-WorkshopContent.ps1` / `prepare-workshop.bat`, which creates a clean `git archive` staging tree and verifies that the entire `Art/` tree is absent before manual Steam publication.
- Do not publish the repository working directory through any path that bypasses these exclusions.
