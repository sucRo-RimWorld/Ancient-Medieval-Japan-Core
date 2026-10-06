# Texture Asset Pipeline — Golden Path

This document owns the general AMJ texture production path. Visual style is owned by `Docs/ArtStyle.md`; family-specific geometry/compositing belongs in the owning family Golden Path.

## 1. Generation intent and fixed-part protection

Interpret the user's image intent semantically rather than by requiring a specific Japanese keyword. A request to create, generate, render, redraw, or materially restyle a new visual source may use ImageGen when the active asset-class pipeline allows it. A request that only needs deterministic reuse, resizing, cropping, masking, palette adjustment, or compositing should use the accepted source and local tooling instead of regenerating it.

Shared/fixed parts are never regenerated. When an asset family has registered fixed components, generate or edit only the variable component and composite it through the owning template/pipeline. Do not treat a request to continue work as permission to replace accepted masters or fixed regions.

This document records the general reusable production path for AMJ texture work.

## 2. Preserve accepted sources

Once the author accepts an image, treat it as a master source.

- Do not recreate an accepted asset from memory or from text alone.
- Reuse, crop, recolor, resize, mask, or composite the accepted source before considering fresh generation.
- If only one component changes, keep all other accepted components fixed.
- A newly generated image is not automatically a replacement for an accepted master.

### Do not edit from production-resolution derivatives

When an accepted source exists at higher resolution than the in-game output, perform material/palette cleanup on the highest authoritative source available and resize only once at export. The 256px production PNG is not a reusable editing source for recoloring/shading transformations. Repeated recolor → blur/median → requantize cycles on a downsampled raster create irreversible noise/banding or broad blurred patches.

For fixed-template contents, build semantic variable layers at high resolution, then downsample the completed variable layer once and composite it into the fixed production-resolution master.

## 3. New-image generation

Use image generation when the requested result needs genuinely new visual content, a new silhouette/structure, or material stylistic redrawing that is not a deterministic source transform. Do not use it for simple resize/crop/mask/export operations or for recreating an accepted fixed/shared component.

1. Generate one isolated asset.
2. Compare it to the relevant accepted AMJ/MO reference at game-like size.
3. Keep the information density at or below the reference.
4. Ask for author acceptance before treating the output as a master.
5. After acceptance, preserve that exact source for later derivatives.

## 4. Automated candidate QA before author review

Generated candidates are not sent directly to the author for first-pass debugging. The production default is:

**ImageGen/source creation → mechanical QA → deterministic family processing → agent semantic visual QA → author final visual review.**

Mechanical QA uses `Scripts/Art/generated_asset_qa.py`. Use the owning family policy when one exists; otherwise use the conservative baseline `Docs/References/AMJ_GeneratedAsset_BaseQA.json`. Measurable checks may include PNG/alpha structure, low-alpha residue, transparency, game-size color complexity, edge density, and family-specific line hierarchy.

The mechanical validator does **not** claim to understand subject identity or aesthetics. After it passes, the agent must automatically compare the candidate against the actual viewed references and reject it internally when the requested subject, silhouette, style, forbidden-content rules, or family composition are wrong. A failed candidate is not presented as a normal review candidate.

For repeated generation, make at most three automatic attempts from the same approved reference set. If all attempts fail, stop and report the recurring failure class/capability limit rather than asking the author to inspect a stream of known-bad images.

The author should normally see only a candidate that has passed all automatic gates, together with the applicable game-size/reference comparison. **The author's remaining role is final visual acceptance**, not routine detection of mechanical/style failures that the pipeline can identify itself.

Family pipelines may add stronger deterministic transforms, metrics, review-sheet generation, or fixed-pixel validation. They must preserve this ordering.

## 5. Asset-family handoff

This document owns the **general texture production path**, not family geometry or compositing contracts.

Use the owning family document for additional requirements:
- boxed resources / masu: `Docs/GoldenPaths/BoxedResourceIconPipeline.md`;
- Workshop covers: `Docs/WorkshopCoverStyle.md` + `Docs/GoldenPaths/WorkshopCoverPipeline.md`;
- fixed reused components: `Docs/GoldenPaths/FixedImageTemplates.md`;
- Environment tree/plant retextures: Environment `Docs/ArtDirection.md` + its texture pipeline.

Do not copy family-specific masks, occlusion regions, historical failure notes, or layout contracts into this general pipeline.

## 6. PNG integrity

Viewer-open success, a PNG signature, or correct IHDR dimensions are not sufficient.

All production PNGs must pass `Tests/validate_png_assets.py`, which checks complete chunk boundaries, CRCs, compressed image data, scanlines, and IEND. GitHub Actions runs the same dedicated PNG gate before Stage A validation.

For automated Git/GitHub binary writes, validate the bytes that are actually committed/checked out. Prefer an exact previously validated blob when recovering accepted art from history.

## 7. Fixed reused components

When an image intentionally reuses a visible component pixel-exactly, follow `Docs/GoldenPaths/FixedImageTemplates.md`. Otherwise do not impose fixed-template machinery on a merely stylistically similar asset.
