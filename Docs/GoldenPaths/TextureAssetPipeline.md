# Texture Asset Pipeline — Golden Path

This document records the reusable production path for AMJ texture work after the successful boxed-resource / masu iteration.

## 1. Preserve accepted sources

Once the author accepts an image, treat it as a master source.

- Do not recreate an accepted asset from memory or from text alone.
- Reuse, crop, recolor, resize, mask, or composite the accepted source before considering fresh generation.
- If only one component changes, keep all other accepted components fixed.
- A newly generated image is not automatically a replacement for an accepted master.

## 2. New-image generation

Use image generation only when a genuinely new silhouette or subject-specific drawing is required.

1. Generate one isolated asset.
2. Compare it to the relevant accepted AMJ/MO reference at game-like size.
3. Keep the information density at or below the reference.
4. Ask for author acceptance before treating the output as a master.
5. After acceptance, preserve that exact source for later derivatives.

If the same failure mode appears in two consecutive generation attempts, stop repeating the prompt and switch to local editing/compositing.

## 3. Boxed resource icons — canonical masu workflow

### Visual target

AMJ keeps the familiar Vanilla / Medieval Overhaul boxed-resource silhouette language so raw resources remain immediately readable, but the shared container is a simplified Japanese **masu**.

The author-approved **empty square masu** is the canonical container master.

The family also requires an accepted **filled exemplar**. For the current masu family the visual reference is `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png` (SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`). The current v1 empty master is blocked because its canvas occupancy is smaller than the accepted exemplar. Do not use v1 for new boxed-resource production.

Detailed activation, fill-profile, layering, and acceptance rules are in `Docs/GoldenPaths/BoxedResourceIconPipeline.md`.

Canonical master file: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png` (256×256 RGBA). This file is the authoritative pixel source for the masu itself; future boxed-resource icons must reuse these pixels rather than regenerate the container.

Registered fixed-template manifest: `Docs/References/AMJ_Masu_Template.json`; editable mask: `Docs/References/AMJ_Masu_EditableMask.png`. New chats/agents must fetch the manifest, master, and mask from `main`, then use `Scripts/Art/fixed_template.py`; do not regenerate the container from prose.

### Immutable parts

The following are fixed across every icon in this family:

- masu silhouette;
- approved three-quarter angle/perspective;
- scale and placement;
- rim width and board thickness;
- corner joinery;
- outline;
- wood colors and shading planes;
- transparent margins.

Only the contents change.

### Production sequence

1. Start from the accepted empty-masu master.
2. Create the new contents separately. Generation may be used for the contents, but it must not define a new container.
3. Fit the contents to the master interior.
4. Composite them into the master. Prefer fixed rear/interior and front-rim layers so the contents are naturally occluded by the front wall.
5. For stack-count variants, reuse the same master and alter only the quantity/arrangement of contents.
6. Compare against the empty master. Any drift in container silhouette, angle, rim, joinery, palette, shading, or placement is a rejection.
7. Use deterministic local compositing from the first derivative; whole-icon generation cannot certify fixed pixels.
8. Export to the repository's production texture requirements.
9. Run:
   `python Scripts/Art/fixed_template.py validate Docs/References/AMJ_Masu_Template.json <final.png>`
   `python Tests/test_masu_template.py`
   `python Tests/validate_png_assets.py`
10. Commit only after both protected-pixel and PNG-integrity gates pass.

### Vanilla / Medieval Overhaul retextures

When AMJ retextures a compatible Vanilla or Medieval Overhaul boxed raw-resource icon:

- retain the familiar boxed-item reading/silhouette class;
- replace the generic crate treatment with the canonical AMJ masu;
- do not independently redesign the container per resource.

A genuinely different container family requires a separately approved master.

## 4. PNG integrity

Viewer-open success, a PNG signature, or correct IHDR dimensions are not sufficient.

All production PNGs must pass `Tests/validate_png_assets.py`, which checks complete chunk boundaries, CRCs, compressed image data, scanlines, and IEND. GitHub Actions runs the same dedicated PNG gate before Stage A validation.

For automated Git/GitHub binary writes, validate the bytes that are actually committed/checked out. Prefer an exact previously validated blob when recovering accepted art from history.

## Pixel-exact shared image components

Follow `Docs/GoldenPaths/FixedImageTemplates.md` for every reused component. Registered masters and binary editable masks are mandatory before producing derivatives. Generate variable material only, composite deterministically, and require zero decoded RGBA differences in protected pixels. Reference-image editing and visual similarity are insufficient. Existing style references do not imply identical silhouettes for different species.
