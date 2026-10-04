# AMJ Art Style Guide

This document is the durable visual reference for **Ancient & Medieval Japan (AMJ)** assets.

The style was locked after comparing generated Awa/millet assets directly against Medieval Overhaul (MO) wheat and leather/hide textures. The user-approved Awa + grain + straw set from 2026-10-03 is the canonical direction. Because the exact chat image is not a repository asset, the rules below are the reproducible source of truth for future generation and manual art work.

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

The approved Awa direction uses a small number of large foxtail heads, broad leaves, a muted olive-green body, warm yellow-gold grain heads, and one common dark outline. Individual millet grains are **not** drawn on the plant.

The canonical repository textures for this first accepted plant asset are:

- `Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png`
- `Textures/Things/Plants/Immature/AMJC_Awa/AMJC_Awa_Immature.png`

On 2026-10-04 the author replaced both production plant images with cutouts from the recovered immature/mature Awa sheet. The author approved removal of the surrounding semitransparent haze. ImageGen extraction preserves the requested two-green-head immature / three-gold-head mature composition and warm brown outline family, but is not a pixel-identical crop. Each separate transparent square output is downsampled to a 256×256 RGBA PNG without further palette changes. These replace the earlier 90%-mature / enlarged-immature exports; their map rendering and current outline weight were subsequently confirmed by the author. The existing Graphic_Random directory wiring is retained.

Use it together with the MO reference textures when calibrating future AMJ plant art.

## 2. Palette and shading budget

2026-10-04 author refinement: mature Awa and the shared RawMillet sheaf use stronger warm-brown contours calibrated against the installed MO mature wheat sprite. The local replacement thickens the contour with image editing, keeping the three-head composition, palette family and transparent 256×256 exports. Immature Awa and millet-in-hull are unchanged. This supersedes the previous thin-contour candidates. The author confirmed the in-game result by screenshot and provisionally accepted the current outline weight on 2026-10-04; no further art adjustment is requested for this slice.

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

### Awa / foxtail millet anchor

The approved mature Awa silhouette is the style anchor:

- approximately 3–4 large foxtail panicles;
- each panicle is a single simplified jagged/segmented mass, not a cluster of individually drawn grains;
- a small number of broad leaves;
- no leaf veins;
- no botanical micro-detail;
- warm gold heads + muted olive foliage + warm ochre-brown outline;
- flat fills with at most one secondary plane.

Future Hie, Kibi, rice, beans, vegetables, fibers, tools, buildings, and processed goods should match this **information density**, even when their shapes differ.

## 4. Line / outline treatment

- Use a warm brown to ochre-brown outline rather than pure black. MO wheat is the reference: the outline may be fairly thick, but a warmer/lighter line keeps it integrated with the fill colors.
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
