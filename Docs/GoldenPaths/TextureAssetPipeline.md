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

Canonical repository asset: `Textures/Things/Item/Resource/AMJC_Shared/Masu/AMJC_Masu_Empty.png`. This 256×256 transparent PNG is the cross-chat/cross-agent master. Fetch it from `main` before producing any boxed-resource derivative; do not regenerate the container from prose.

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
   `python Tests/validate_png_assets.py`
10. Commit only after the PNG integrity gate passes.

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
