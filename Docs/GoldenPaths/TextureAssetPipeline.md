## Wording and ImageGen permission

For AMJ production art, distinguish **作成/制作** from **生成**.

- 「作成」「制作」「続けて」: use the established pipeline only — reuse accepted sources, local transforms, deterministic compositing, masks, and validation. Do not invoke ImageGen merely because the task is an image task.
- 「生成」: ImageGen may be used only where this pipeline explicitly allows new source artwork.
- Shared/fixed parts are never regenerated. If generation is allowed, generate only the variable component and then composite it through the registered template.
- If no valid local/deterministic route exists and generation was not explicitly requested, fail closed and report the missing source instead of substituting generation.

# Texture Asset Pipeline — Golden Path

> Boxed-resource audit (2026-10-06): see [occlusion and fixed-region findings](../Research/BoxedResourceOcclusionAudit.md). Identity reconstruction validates the registered Soba exemplar, not natural new-content production. The audit itself did not change production. Its correction is now implemented as the v4 contact study below; master/exemplar art is unchanged and new-resource production remains blocked.

This document records the reusable production path for AMJ texture work after the successful boxed-resource / masu iteration.

## 1. Preserve accepted sources

Once the author accepts an image, treat it as a master source.

- Do not recreate an accepted asset from memory or from text alone.
- Reuse, crop, recolor, resize, mask, or composite the accepted source before considering fresh generation.
- If only one component changes, keep all other accepted components fixed.
- A newly generated image is not automatically a replacement for an accepted master.

### Do not edit from production-resolution derivatives

When an accepted source exists at higher resolution than the in-game output, perform material/palette cleanup on the highest authoritative source available and resize only once at export. The 256px production PNG is not a reusable editing source for recoloring/shading transformations. Repeated recolor → blur/median → requantize cycles on a downsampled raster create irreversible noise/banding or broad blurred patches.

For fixed-template contents, build semantic variable layers at high resolution, then downsample the completed variable layer once and composite it into the fixed production-resolution master.

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

The registered **masu v2 empty master** is the canonical container master. It is a technical derivation of the author-approved filled exemplar and high-resolution empty source; known resampling artifacts were cleaned before registration.

The family also requires an accepted **filled exemplar**. For the current masu family the visual reference is `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png` (SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`). The accepted v2 master matches the exemplar's `[17, 28, 239, 235]` frame occupancy.

Detailed activation, fill-profile, layering, and acceptance rules are in `Docs/GoldenPaths/BoxedResourceIconPipeline.md`.

Canonical master file: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png` (256×256 RGBA). This file is the authoritative pixel source for the masu itself; future boxed-resource icons must reuse these pixels rather than regenerate the container.

Registered fixed-template manifest: `Docs/References/AMJ_Masu_Template.json`. New chats must retrieve the master, registered HardFixed/ContactZone/ExtensionAllowed masks and RequiredFill guide from main. The historical editable mask remains an identity diagnostic; it is not the current content permission shape.

### Container reuse and contact

The approved master establishes the container angle, geometry, scale, wood palette and placement. Only conservative lower HardFixed wood is immutable in the final RGBA. Upper rim, interior and upper front/side walls form an occludable contact band: contents, contact outline and subtle contact shading are edited together. Unoccluded wood retains master pixels. Independent ExtensionAllowed permits different protruding shapes; Soba's alpha envelope is not the family limit.

### Production sequence

The current **v4-contact-study** contract is implemented for validation, with production blocked. Follow `BoxedResourceIconPipeline.md` for exact commands and masks.

1. Use `scaffold-study` to copy the full intact master into a diagnostic context canvas outside production/reference folders.
2. Draw contents and contact within ContactZone/ExtensionAllowed. Do not use a transparent object-only layer or cavity/pile clipping.
3. Use `compose-study`; it rejects forbidden changes and restores only HardFixed directly from the master. It does not split or re-alpha-blend the rendered master/context.
4. Run structural checks, the registered-reference comparison at 256px/~64px, and PNG integrity. Correct technical defects before presentation.
5. Validate low grains, large pieces and strong over-rim overlap with the same unchanged region contract. Synthetic fixtures are structural evidence only.
6. Record visual acceptance and suitable fill profiles before activating production. The current bulk-grain fill rule is not universal.
7. Only after activation may production `scaffold` / `compose` produce resources; use the same master/contract for stack variants.

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
