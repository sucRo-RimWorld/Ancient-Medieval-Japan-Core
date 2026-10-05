# AMJ Art Style Guide

This document is the durable visual reference for **Ancient & Medieval Japan (AMJ)** assets.

The style was locked after comparing AMJ cereal/resource assets directly against Medieval Overhaul (MO) wheat and leather/hide textures. The author-approved Awa, Hie, and Kibi plant set from 2026-10-04 is the canonical cereal-plant baseline; the accepted millet-item/straw set remains the resource baseline. The rules and production assets below are the reproducible source of truth for future generation and manual art work.

## 1. Primary target

AMJ art should look at home beside **Medieval Overhaul**, not beside RimWorld Vanilla.

Reference characteristics observed in MO wheat and leather/hide:

- flat, graphic, vector-like shapes;
- silhouette first, detail second;
- few color regions;
- thick dark outline used to separate the object from the map/UI;
- hard-edged color planes rather than soft modeled lighting;
- little or no surface texture;
- no painterly noise;
- no photorealistic material rendering;
- enough simplification to remain readable at small in-game size.

The accepted Stage A cereal direction uses broad simplified leaves, a shared warm medium-dark brown outline, few large color planes, and crop identity carried primarily by the seed-head silhouette. Individual grains and fine botanical structure are suppressed unless essential to recognition.

The canonical cereal-plant textures are:

- `Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png`
- `Textures/Things/Plants/Immature/AMJC_Awa/AMJC_Awa_Immature.png`
- `Textures/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png`
- `Textures/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png`
- `Textures/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png`
- `Textures/Things/Plants/Immature/AMJC_Kibi/AMJC_Kibi_Immature.png`

These six transparent 256×256 production textures were accepted together on 2026-10-04. Awa uses dense upright foxtail heads, Hie uses compact branched/drooping heads, and Kibi uses a more open branched panicle. Mature and immature states retain the same crop silhouette language while changing the head maturity/color. Future cereal crops should match this trio's outline weight, color budget, leaf treatment, and information density.

Use this set together with the MO reference textures when calibrating future AMJ plant art.

## 2. Palette and shading budget

2026-10-04 cereal refinement: Awa, Hie, and Kibi now share the same warm medium-dark brown contour treatment and simplified information density. This supersedes earlier Awa/Hie production candidates and the short-lived per-material/color-trace outline experiment. The shared RawMillet sheaf remains in the same broad warm-outline family, but the crop-plant trio is the canonical reference for subsequent cereal plants.

Treat these as upper limits, not targets to fill.

### Plants

- 1 common warm brown / ochre-brown outline color;
- foliage: normally 2 flat colors (base + one secondary plane);
- flower/grain/fruit: normally 1–2 flat colors;
- total visible fill colors: ideally 3–4, maximum 5 when required for identification;
- no gradients;
- no soft airbrush shadows;
- no fine leaf veins;
- no many-step highlights.

### Items and resources

Items should be at least as flat as plants, and usually flatter.

- 1 common dark outline color;
- 1 base fill color;
- optionally 1 secondary shadow/highlight plane;
- use a third fill only when needed to identify the material;
- avoid per-piece specular highlights;
- avoid deep ambient-occlusion shadows between every grain;
- avoid giving every grain/seed its own light-dark modeling.

For piles of grain, use a **small number of large simplified pieces** to communicate "pile of grain". Do not render dozens of individually shaded particles.

For bundles such as straw, use a few broad strips/stems and a simple binding band. Do not render fiber texture.

The first canonical post-harvest millet item assets are now stored under:

- `Textures/Things/Item/Resource/AMJC_Millet/RawMillet/`
- `Textures/Things/Item/Resource/AMJC_Millet/MilletInHull/`
- `Textures/Things/Item/Resource/AMJC_Millet/Millet/`

They are isolated from the user-approved 2026-10-03 millet set rather than regenerated. The three states intentionally read as distinct material stages: warm-gold raw millet, brown hulled grain, and pale cleaned grain. They retain `Graphic_StackCount`; during this first integration pass the same approved pile silhouette is supplied to each stack-count slot so only rendering scale/readability changes are evaluated.

## 3. Shape language

- Prefer large readable masses over botanical or material accuracy.
- Preserve the distinctive silhouette of the real object, then remove nonessential interior detail.
- Curves and corners should be deliberate and graphic rather than naturalistic.
- Interior divisions should be few and large.
- At 64 px display size, the asset should remain identifiable without relying on interior texture.

### Stage A cereal anchors

The accepted Awa / Hie / Kibi trio is the cereal style anchor:

- **Awa:** approximately three dense, upright foxtail panicles; each reads as one large compact mass rather than separate branches or grains.
- **Hie:** a small number of compact branched panicles that visibly droop when mature; immature heads may be somewhat more upright but keep the same simplified massing.
- **Kibi:** an open, airy branched panicle with clear gaps between major branches; do not turn it into either Awa's dense baton or Hie's heavier compact droop.
- all three use a small number of broad leaves, no leaf veins, no botanical micro-detail, and flat fills with at most one secondary plane;
- all three use the same warm medium-dark brown outline and approximately the same information density.

Future cereals should match this **information density** even when their silhouettes differ. Other plants, fibers, tools, buildings, and processed goods should follow the same silhouette-first principle without mechanically copying cereal anatomy. Botanical differences should be expressed primarily through silhouette, not through a higher count of individual grains, branches, veins, or interior marks.

## 4. Line / outline treatment

- **Stage A crop plants use one shared outline color.** The accepted 2026-10-04 Awa/Hie comparison establishes a warm, medium-dark brown contour that reads clearly dark without appearing near-black. Do not vary the outline hue by crop, seed head, or foliage; silhouette and fill colors carry the botanical distinction. This supersedes the earlier per-material/color-trace outline experiment.
- Outline width must stay visually strong after downscaling.
- The outer contour is more important than internal linework.
- Internal outlines should be minimized; prefer adjacent color planes where possible.
- Do not add sketch lines, ink hatching, or thin decorative strokes.

## 5. Canvas and export

Unless a specific Def requires otherwise:

- 256×256 px working/export target for individual Thing/Plant textures;
- transparent background;
- no UI frame;
- no labels or text;
- no cast shadow outside the object;
- object centered with sufficient transparent margin for RimWorld scaling;
- evaluate at 256 px and again at roughly 64 px before acceptance.

Larger working files are allowed, but the final result must survive reduction without becoming visually denser than MO.

## 6. Generation prompt baseline

When generating an AMJ asset, begin from this semantic prompt rather than generic "RimWorld style":

> Single isolated game texture for Ancient & Medieval Japan, visually matched to Medieval Overhaul. Flat vector-like 2D graphic, very limited palette, thick dark warm-brown outline, large simple silhouette, hard-edged color planes, minimal shading, no gradient, no texture noise, no photorealism, no painterly rendering, no fine detail, transparent background, readable at 64 px, 256×256 composition.

Then add only the subject-specific shape and colors.

For plants add:

> Simplify botanical structure aggressively. Use only a few broad leaves/stems and large symbolic flower/seed-head shapes. Do not draw individual seeds, leaf veins, hairs, or realistic surface detail.

For item/resource icons add:

> Even flatter than the plant art. Use one base fill and at most one secondary plane per material. No per-piece highlights or deep contact shadows.

### Canonical boxed-resource icon: Japanese masu master

For loose harvested produce, beans, grains, hulled grain, and similar resources, AMJ uses the **Vanilla / Medieval Overhaul boxed-resource silhouette language** but replaces the generic crate surface treatment with a simplified Japanese **masu**.

The author-approved **empty square masu** is the canonical container master. The container is a reusable production component, not something to redraw for every resource.

The author-approved **filled buckwheat-in-hull image** is also a required composition reference for this family. Pixel-stable container reuse is necessary but not sufficient: the container scale on the canvas and the apparent amount/height of contents must match the accepted visual family.

Persistent accepted visual reference: `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png` (1254×1254 PNG, SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`). At 256×256 normalization its non-transparent visual envelope is approximately `[17, 28, 239, 235]`. The current v1 empty master envelope is `[34, 42, 232, 213]`, so v1 is visibly underscaled relative to the accepted icon and is **blocked for production derivatives**.

Do not reactivate the masu family until a v2 empty master is aligned to the accepted filled reference, a content fill guide is registered, and one representative filled composite is visually accepted at both 256 px and game-like small size. See `Docs/GoldenPaths/BoxedResourceIconPipeline.md`.

Canonical master file: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png` (256×256 RGBA). This file is the authoritative pixel source for the masu itself; future boxed-resource icons must reuse these pixels rather than regenerate the container.

Deterministic template registration: `Docs/References/AMJ_Masu_Template.json` with editable mask `Docs/References/AMJ_Masu_EditableMask.png`. The editable region is the masu interior only; rim, exterior faces, outline, joinery, wood shading, placement, and transparent margins are protected and must have zero RGBA pixel differences.

Fixed container properties:
- square masu silhouette and the approved three-quarter viewing angle;
- container scale and placement on the 256×256 canvas;
- rim width and board thickness;
- dark warm-brown outer contour;
- corner joinery;
- wood palette and shading planes;
- transparent margin around the container.

Only the **contents** may vary between resources. The final production icon must preserve the master container geometry and appearance; do not accept a generated variant just because it is "similar".

Production rule:
1. Start from the accepted empty-masu master.
2. Generate/draw only the resource contents, using the master as the visual and geometric reference.
3. Composite the contents into the master so that the container itself remains unchanged. Where useful, keep the rear/interior and front-rim portions as separate fixed layers so the contents sit naturally inside the masu.
4. For stack-count variants, keep the same master and change only content amount/arrangement.
5. If image generation alters the masu silhouette, perspective, rim, joinery, wood colors, or placement, reject that output rather than treating the changed container as a new base.
6. Whole-icon regeneration is not a production path for shared parts. Use deterministic local compositing from the first derivative and require zero protected RGBA pixel differences under `Docs/GoldenPaths/FixedImageTemplates.md`.
7. Normalize the finished production texture to the repository format and run `python Tests/validate_png_assets.py` before committing.

When AMJ retextures compatible Vanilla / Medieval Overhaul boxed raw-resource icons, preserve their familiar **boxed-item reading at game scale**, but use this same canonical masu treatment for series consistency.

This masu workflow is the default for boxed resource icons. A genuinely different container class requires an explicitly approved new master; do not mutate the masu master ad hoc.

## 7. Required iteration procedure

Prefer **reuse and local image processing before new image generation**. Image generation is comparatively slow and may time out, while most AMJ follow-up work after a style/silhouette is accepted can be completed more reliably by transforming the accepted source asset.

Use this priority order:

1. Reuse an already accepted AMJ asset when the subject or visual family is the same.
2. For size, crop, transparent-margin, palette, outline-color, simple recolor, stack-slot, or export-format changes, modify the accepted image locally without regenerating the artwork.
3. For related assets that can be derived from an approved source without inventing a new silhouette, use local editing/compositing first.
4. Use image generation only when a genuinely new silhouette, object structure, or subject-specific drawing is required.
5. Once a generated source is accepted, preserve that accepted source and make later revisions from it rather than repeatedly regenerating near-identical variants.

For genuinely new AMJ art, use this loop:

1. Generate **one isolated asset**, not an infographic or multi-asset presentation.
2. Compare it directly with the relevant MO reference at similar display size.
3. Ask:
   - Does AMJ have more color steps?
   - More shading?
   - More interior lines?
   - More small pieces?
   - More realistic texture?
4. If yes, simplify the AMJ asset.
5. Repeat until its information density is at or below MO.
6. Only then perform the in-game appearance check.
7. Once the style for that asset class is accepted, reuse the same palette/outline/detail budget for related assets.

Do not treat a generated comparison sheet as the final game texture. The final texture must be a clean isolated asset.

Before committing any PNG asset to GitHub, run `python Tests/validate_png_assets.py` and do not commit until it passes. The dedicated validator checks every `Textures/**/*.png` for complete chunk boundaries, CRCs, a complete compressed image stream, supported 8-bit indexed/RGBA encoding, and valid scanlines, and reports all broken PNGs in one run. GitHub Actions runs the same integrity gate before Stage A validation. A file opening in an image viewer, having a PNG signature, or reporting 256×256 in IHDR is not sufficient evidence of a valid production asset.

When binary textures are written through automation or Git/GitHub APIs, validate the bytes that will actually be committed. If a binary replacement is recovered from repository history, prefer an exact previously validated blob over re-encoding or regenerating accepted art.


### Workshop cover generation workflow

The Workshop-cover visual system is maintained separately from in-game Thing/Plant texture rules.

**Source of truth:** `Docs/WorkshopCoverStyle.md`  
**Layout schematic:** `Docs/References/AMJ_WorkshopCover_Template.svg`

The 2026-10-05 author-approved Environment-style direction supersedes the earlier dark-left-panel / Japan-map / scenic-landscape cover template.

High-level rules:
- first propose the composition and design in words, then generate only after author approval;
- use a warm pale parchment field rather than a dark common-left panel;
- treat the left side as an **invariant shared series block**: three lines reading `Ancient &` / `Medieval` / `Japan`, with `Japan` alone in muted reddish-brown, followed by the addon name in the fixed tracked position;
- do not reintroduce the superseded `中世日本OH` heading, A/M/J-initial emphasis, dark panel, Japan map, or red brush badge;
- addon-specific generation instructions may change the right-side motifs and addon name only, not the common-left composition;
- make the right side a symbolic, highly simplified flat editorial illustration rather than a scenic landscape;
- no people on any AMJ Workshop cover;
- use low saturation and a limited palette;
- target about three colors per motif (base / dark / light), with only a very light gradient where useful;
- do not use stereotypical Japan decoration merely for atmosphere;
- preserve strong readability at small Steam Workshop thumbnail size;
- before generation, retrieve and visually inspect the approved Core cover reference from Library `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`; do not generate from text rules or SVG alone;
- do **not** ask ImageGen to create the complete Workshop cover. Generate only the addon-specific right-side artwork, preferably with transparency;
- retrieve the canonical Library common base and variable mask, then compose with `Scripts/build_workshop_cover.py` following `Docs/GoldenPaths/WorkshopCoverPipeline.md`;
- run `Scripts/validate_workshop_cover.py`; any protected-pixel difference is a hard failure.

Do not use the older fixed dark-left common image or red brush-stroke addon badge for new covers.

## 8. Rejection criteria

Reject and regenerate when any of the following is true:

- it looks closer to RimWorld Vanilla than MO;
- it uses realistic/painterly shading;
- it appears three-dimensional because of many light-dark steps;
- individual grains/seeds/fibers are over-rendered;
- the object relies on texture rather than silhouette;
- color count is noticeably higher than the comparable MO asset;
- the outline is thinner or less graphic than the MO reference;
- item icons have stronger shadows than the approved AMJ millet set;
- it looks impressive at full resolution but becomes noisy at in-game size.

## 9. MO reference assets

When available locally, compare against these MO assets before accepting new AMJ art:

- mature wheat plant (`PlantWheat_Mature` / MO wheat full-grown texture);
- `Leather_a`;
- `Leather_b`;
- `HideMedium_a`.

Use them as references for **flatness, palette size, outline strength, shading amount, and information density**, not as shapes to copy.

## 10. Palette swatch reference

See `Docs/References/AMJ_ArtStyle_Palette.svg`.

The swatches are not mandatory exact colors. They document the approved relationship:

- very dark warm-brown outline;
- muted olive foliage;
- one lighter olive plane;
- warm yellow-gold grain;
- optional darker gold/brown secondary plane;
- pale cream for cleaned grain.

The consistent relationship and low number of planes matter more than exact RGB values.

## Pixel-exact shared image components

Follow `Docs/GoldenPaths/FixedImageTemplates.md` for every reused component. Registered masters and binary editable masks are mandatory before producing derivatives. Generate variable material only, composite deterministically, and require zero decoded RGBA differences in protected pixels. Reference-image editing and visual similarity are insufficient. Existing style references do not imply identical silhouettes for different species.
