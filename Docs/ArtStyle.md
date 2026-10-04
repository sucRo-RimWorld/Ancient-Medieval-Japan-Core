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

### Canonical produce crate / masu-style container

For loose harvested produce, beans, grains, hulled grain, and similar resources that use the Medieval Overhaul / Vanilla shallow wooden-box presentation, **the container itself must not be regenerated per asset**.

- The accepted `AMJC_BuckwheatInHull` shallow wooden box is the canonical container master.
- Future AMJ container icons must reuse the **exact same box pixels** after the production texture is normalized to 256×256.
- Box geometry, perspective, outline, rim thickness, wood colors, shading planes, and placement are fixed.
- Only the contents above/inside the box may change.
- Generate or draw the contents separately on transparency, then composite them into the canonical box with deterministic local image processing.
- Do not ask the image generator to redraw the box for each resource; this rule exists specifically to prevent visual drift.
- When a different container class is genuinely required, define a new canonical master for that class rather than mutating this one.

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

Before committing any PNG asset to GitHub, run `python Tests/validate_stage_a.py` and do not commit until it passes. The validator checks every `Textures/**/*.png` for complete chunk boundaries, CRCs, a complete compressed image stream, supported 8-bit indexed/RGBA encoding, and valid scanlines. A file opening in an image viewer, having a PNG signature, or reporting 256×256 in IHDR is not sufficient evidence of a valid production asset.

When binary textures are written through automation or Git/GitHub APIs, validate the bytes that will actually be committed. If a binary replacement is recovered from repository history, prefer an exact previously validated blob over re-encoding or regenerating accepted art.

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
