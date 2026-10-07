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

## Inventory / recovery queue

The complete Core source-recovery inventory is [Inventory.md](Inventory.md): 19 image roles, 11 already archived and 8 pending source verification/recovery, with 2 supplemental references counted separately. Original-file counts may differ where several assets share one source sheet. A candidate's presence does not establish final-source identity; three named immature-millet candidates were measured at 256×256 and must not be promoted to pre-resize masters. G04 now has a separately verified high-resolution original.

## Current authoritative sources

- `Shared/Containers/AMJ_Masu_Empty_Master.png`
- `Shared/Containers/AMJ_Masu_Empty_Master.xcf`
- `Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png`
- `Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png`
- `Workshop/AMJ_WorkshopCover_Template.svg`
- `Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg`
- `Workshop/AMJ_WorkshopCover_CommonBase.png`
- `Workshop/AMJ_WorkshopCover_VariableMask.png`
- `Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`
- `Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png`
- `Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png`
- `Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png`

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

### Soba immature plant — 2026-10-07 JST

- Archived file: `Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png`.
- Original: `黒背景の芽吹く植物アイコン(1).png`, Library identity `libfile_3f5c688ff0088191b57c3583709cbf94`.
- Original dimensions: 1448×1086 RGBA; 545,958 bytes. Preserved without resizing, recoloring, or re-encoding.
- SHA-256: `194e4b67ea25ab77d73a07f973bbbf7bfaba4ededbda9eb1366c08bc7a2e75b4`.
- Production counterpart: `Textures/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png` (256×256).
- Provenance: the accepted-source recovery recorded in `AMJ-009-ART-SOBA-PLANT` and the production integration commit `c7d5d2c229119aac717de80718ff7c2bdb92a00d`. Visual comparison confirms the same three shoots/bud clusters, leaves, stem junctions, colors and silhouette. The unsuffixed `黒背景の芽吹く植物アイコン.png` has additional shoots and a different composition and was excluded.
- The historical palette/export recipe has not been reconstructed; visual and recorded provenance establish the recovered candidate, without claiming an exact pixel-identical direct resize. This recovery preserves the original bytes only and does not change production files.

### Buckwheat in hull — 2026-10-07 JST

- Archived file: `Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png`.
- Original: `AMJ_BoxedResource_BuckwheatInHull_Ideal.png`, Library identity `libfile_5a34c43373188191a48e3796290482af`; registered at `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`.
- Original dimensions: 1254×1254 RGBA; 869,790 bytes. Preserved without resizing, recoloring, or re-encoding.
- SHA-256: `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`, matching `Docs/References/AMJ_Masu_Template.json` → `visual_reference` and the retained accepted-reference records.
- Production counterparts: `Textures/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull_{a,b,c}.png` (256×256). All three are byte-identical to the registered normalized representative `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png` (SHA-256 `0f81aa92460154d2b1ae50de14d7360be5e44ff46f8c81bdd113b6e19143d752`).
- Provenance: approved filled exemplar in the boxed-resource pipeline and the 2026-10-05 Soba in-hull integration recorded under `AMJ-009`. The source was visually checked, and full-canvas Pillow RGBA LANCZOS resize to 256×256 reproduces all production pixels exactly (0 different RGBA pixels).
- This recovery archives only the accepted original. Production textures and the historical diagnostic template/masks are unchanged.

### Approved Core Workshop cover reference — 2026-10-07 JST

- Archived file: `Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg`.
- Original: `AMJ_WorkshopCover_Core_Approved_Reference.jpg`, Library identity `libfile_f0ec7d3c94f88191ab304f0fbdb13946`; registered at `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`.
- Original dimensions: 960×540 RGB JPEG; 92,308 bytes. Preserved without resizing or re-encoding.
- SHA-256: `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658`, matching `Docs/References/AMJ_WorkshopCover_Manifest.md` and `Docs/GoldenPaths/WorkshopCoverPipeline.md`.
- Provenance: the author-approved visual reference registered by the deterministic Workshop-cover pipeline. Visually inspected and fully decoded; exact registered source bytes were copied.
- This file is the accepted visual reference, distinct from the SVG schematic, fixed common base and variable mask. The common base and variable mask are now archived separately. This archive action does not create or replace `About/preview.png` or publish a Workshop cover.

### Workshop cover common raster — 2026-10-07 JST

- Archived file: `Workshop/AMJ_WorkshopCover_CommonBase.png`.
- Original: `AMJ_WorkshopCover_CommonBase.png`, Library identity `libfile_1730eee945f8819198690f7cb988c96c`; registered at `/AMJ/References/AMJ_WorkshopCover_CommonBase.png`.
- Original dimensions: 960×540 RGB PNG; 149,866 bytes. Preserved without resizing, color conversion, or re-encoding.
- SHA-256: `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362`, matching `Docs/References/AMJ_WorkshopCover_Manifest.md` and `Docs/GoldenPaths/WorkshopCoverPipeline.md`.
- Provenance: the registered fixed common raster for the deterministic cover compositor. Visually inspected the parchment field, title and common ornaments; original bytes are preserved.
- Source PNG validation checked chunk boundaries/CRCs, the complete IDAT/zlib stream, RGB scanlines/filters, IEND and full image decoding. The production-only PNG gate permits indexed/RGBA encoding; this immutable RGB source is validated separately without changing its encoding.
- The variable mask is now archived separately. This action does not create a cover, replace `About/preview.png`, or publish to Workshop.

### Workshop cover variable mask — 2026-10-07 JST

- Archived file: `Workshop/AMJ_WorkshopCover_VariableMask.png`.
- Original: `AMJ_WorkshopCover_VariableMask.png`, Library identity `libfile_f831c30d1cac819192ed282dbf430698`; registered at `/AMJ/References/AMJ_WorkshopCover_VariableMask.png`.
- Original dimensions: 960×540, 8-bit grayscale (L) PNG; 1,216 bytes. Preserved without resizing, color conversion, or re-encoding.
- SHA-256: `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622`, matching the Workshop-cover manifest, template JSON and Golden Path.
- Provenance: the registered deterministic compositor mask, with 0 meaning protected and 255 meaning editable. All pixels match the registered right-side region `x >= 330` and addon-label rectangle `[66,378,310,426]` (inclusive pixel bounds), with no other editable pixels.
- Source PNG validation checked chunk boundaries/CRCs, the complete IDAT/zlib stream, grayscale scanlines/filters, IEND and full decoding. The production-only PNG gate permits indexed/RGBA encoding; this immutable grayscale source is validated separately without conversion.
- All four registered Workshop source roles (SVG, approved reference, common base and variable mask) are now archived. This action does not create or replace a cover or publish to Workshop.

### Hie mature plant — 2026-10-07 JST

- Archived file: `Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png`.
- Original: `ヒエの穂が揺れる可愛い植物アイコン.png`, Library identity `libfile_81f9f17fbb988191916144a698e3bfa5`.
- Original dimensions: 1254×1254 RGBA; 909,425 bytes. Preserved without resizing, recoloring, or re-encoding.
- SHA-256: `58bc4a98f4557d5df112f97c2094d7cbb5681ea8f46c36246064b10da3c573db`.
- Production counterpart: `Textures/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png` (256×256 indexed PNG; SHA-256 `b1348a888a4eb05e5b30a051b112530947cdf5699d663046bfdae39be43becd1`).
- Provenance: `AMJ-016` author-approved cereal graphics and integration `ddb7a593cd552fc7a37909838b870cbd8fc28436`; the current mature production blob is still the approved integration blob. Visual comparison confirms the same three golden drooping panicles, broad leaves, stems, junctions and silhouette.
- The initially listed `直立したヒエの植物アイコン.png` (`libfile_b626dec6725c8191bc318e25fa265b58`, green-grained version) differs in maturity and panicle structure and was excluded from G03. It was subsequently verified and archived separately for G04 below.
- Historical positioning/palette-export steps have not been reconstructed; a direct full-canvas resize is not pixel-identical to the indexed production PNG. Identity is established from visual correspondence and the accepted integration record, without claiming an exact export reproduction.
- This recovery preserves only the exact original bytes; production textures are unchanged.

### Hie immature plant — 2026-10-07 JST

- Archived file: `Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png`.
- Original: `直立したヒエの植物アイコン.png`, Library identity `libfile_b626dec6725c8191bc318e25fa265b58`.
- Original dimensions: 1254×1254 RGBA; 656,097 bytes. Preserved without resizing, recoloring, or re-encoding.
- SHA-256: `1d1d8bd67d1bd2c28cbb3e783dab043d07f5e6877eab053a7df869b8ad703538`.
- Production counterpart: `Textures/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png` (256×256 indexed PNG; SHA-256 `8faaa28ae522b5fd1727e1f522042539e3e74ace6131bcd4760fcbfe42ede144`).
- Provenance: `AMJ-016` and approval integration `ddb7a593cd552fc7a37909838b870cbd8fc28436` record acceptance of the final Hie immature candidate without further posture adjustment. Repair `0262092fa06c4578450af15c5b936fdd80156113` restored the valid PNG from finalization `02c4a193fe0514eba57d5aab69edf8a69145c645`; current production retains their identical blob `ff214627c143f900c1b1c932dbfe249ff373e345`.
- Visual comparison confirms the same three green-grained branched panicles, broad leaves, stems, junctions and silhouette. This original is distinct from the golden mature source and from the named 256×256 derivative.
- Historical palette/export steps have not been reconstructed; direct full-canvas resizing does not reproduce the indexed production pixels exactly. This recovery establishes source identity from visual correspondence and retained approval/repair records, without claiming exact export reproduction.
- Only the exact original bytes are archived; production textures are unchanged.

## Workshop distribution

The repository-root `Art/` tree is development-only material and must **never** be included in Steam Workshop content.

- `.rimignore` excludes the root `Art` directory for YADA Workshop uploads.
- `.workshopignore` records the same whole-`Art/` exclusion for uploaders that support that file.
- `_PublisherPlus.xml` excludes `Art` when publishing through RimWorld's PublisherPlus workflow.
- The fail-closed publication path is `Scripts/Prepare-WorkshopContent.ps1` / `prepare-workshop.bat`, which creates a clean `git archive` staging tree and verifies that the entire `Art/` tree is absent before manual Steam publication.
- Do not publish the repository working directory through any path that bypasses these exclusions.
