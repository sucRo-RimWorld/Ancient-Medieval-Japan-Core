# AMJ Art Style Guide

This document is the durable visual reference for **Ancient & Medieval Japan (AMJ)** assets.

The style was locked after comparing AMJ cereal/resource assets directly against Medieval Overhaul (MO) wheat and leather/hide textures. The author-approved Awa, Hie, and Kibi plant set from 2026-10-04 is the canonical cereal-plant baseline; the accepted millet-item/straw set remains the resource baseline. The rules and production assets below are the reproducible source of truth for future generation and manual art work.

## Rule ownership and precedence

This file owns the **AMJ-wide visual language**. Keep operational procedures out of this document.

Apply image rules in this order:

1. **Shared AMJ visual language (this file):** simplified silhouette-first forms, restrained palette/detail, no photorealism or painterly noise, and readability at game scale.
2. **Asset-class style specification:** adds class-specific visual rules and may explicitly define a controlled deviation from non-invariant details such as shading treatment. For example, Environment tree sprites may use restrained internal gradient variation while Core crop/item textures use the flatter budgets below.
3. **Production Golden Path:** controls source reuse, generation/compositing, export, and validation. It must not redefine the visual style.
4. **Fixed-template rules:** apply only when visible parts are intentionally reused pixel-exactly.

The AMJ-wide invariants are silhouette-first simplification, restrained palette/information density, non-photorealistic/non-painterly rendering, and readability at game scale. Asset classes may vary outline treatment, shading budget, canvas, or composition only when their owning style specification says so explicitly. Do not accumulate one-off prompt exceptions or AGENTS notes.

## 1. In-game asset primary target

AMJ in-game sprites/textures should look at home beside **Medieval Overhaul**, not beside RimWorld Vanilla. Presentation classes such as Workshop covers inherit the shared invariants above but use their own class-specific composition, palette, and edge-treatment rules.

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

## 2. Core crop/item palette and shading budget

These numeric budgets are the current **Core crop and Thing/resource baseline**. Other AMJ asset classes inherit the project-wide invariants from section 1, but may define a controlled class-specific shading budget in their owning style specification.

Treat these as upper limits, not targets to fill.

### Core crop plants

- 1 common warm brown / ochre-brown outline color;
- foliage: normally 2 flat colors (base + one secondary plane);
- flower/grain/fruit: normally 1–2 flat colors;
- total visible fill colors: ideally 3–4, maximum 5 when required for identification;
- no gradients;
- no soft airbrush shadows;
- no fine leaf veins;
- no many-step highlights.

### Core items and resources

Items should be at least as flat as the Core crop art, and usually flatter.

- 1 common dark outline color;
- 1 base fill color;
- optionally 1 secondary shadow/highlight plane;
- use a third fill only when needed to identify the material;
- avoid per-piece specular highlights;
- avoid deep ambient-occlusion shadows between every grain;
- avoid giving every grain/seed its own light-dark modeling.

For piles of grain, use a **small number of large simplified pieces** to communicate "pile of grain". Do not render dozens of individually shaded particles.

For bundles such as straw, use a few broad strips/stems and a simple binding band. Do not render fiber texture.

Canonical post-harvest millet item references are stored under:
- `Textures/Things/Item/Resource/AMJC_Millet/RawMillet/`;
- `Textures/Things/Item/Resource/AMJC_Millet/MilletInHull/`;
- `Textures/Things/Item/Resource/AMJC_Millet/Millet/`.

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
- For clustered Core items/resources such as piles of grain, use a clear **line hierarchy**: the silhouette around the entire pile is the thickest/darkest contour, while boundaries between individual pieces are thinner and lighter.
- Internal piece boundaries are subordinate structure, not equal-strength outlines. They may be visibly pale when that preserves the pile as one readable mass.
- Internal outlines should be minimized; prefer adjacent color planes where possible.
- Reject clustered-item art where every grain/piece is enclosed by the same heavy dark line as the outer silhouette, because it fragments the pile and raises visual noise at game scale.
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

For **Core Thing/Plant textures**, begin from this semantic baseline rather than generic "RimWorld style":

> Single isolated game texture for Ancient & Medieval Japan, visually matched to Medieval Overhaul. Flat vector-like 2D graphic, very limited palette, thick dark warm-brown outline, large simple silhouette, hard-edged color planes, minimal shading, no texture noise, no photorealism, no painterly rendering, no fine detail, transparent background, readable at 64 px, 256×256 composition.

For Core crop plants, keep the existing no-gradient/few-plane budget from section 2. For Core items/resources, make the result at least as flat as the plant art: one base fill and at most one secondary plane per material, no per-piece glossy highlights, and no deep contact shadow on every grain.

Do not reuse this exact budget for a different asset class when its owning style specification defines a controlled exception. The project-wide invariants in section 1 still apply.

Family-specific geometry, perspective, fixed regions, and compositing are **not** style rules and do not belong here:
- boxed resources / masu: `Docs/GoldenPaths/BoxedResourceIconPipeline.md`;
- Workshop covers: `Docs/WorkshopCoverStyle.md` and `Docs/GoldenPaths/WorkshopCoverPipeline.md`;
- Environment tree/plant retextures: Environment `Docs/ArtDirection.md`.

## 7. Required iteration procedure

1. Read this shared style plus the owning asset-class specification.
2. Open the actual accepted AMJ/MO reference images relevant to that class; do not substitute memory or a text-only description.
3. Prefer an accepted source/local edit when no new silhouette or structure is needed. Use new generation only when the active production pipeline permits it.
4. For a new candidate, compare it directly against the relevant reference at full size and at roughly game-size display.
5. Reject the candidate before presentation if it is more realistic, more shaded, more detailed, more saturated, or less clearly outlined than the applicable baseline.
6. Once accepted, preserve that exact source and use the owning production Golden Path for integration and validation.

This section is the visual review loop only. Source preservation, ImageGen permission, fixed-template compositing, PNG integrity, and family-specific masks belong in the owning Golden Path documents.

## 8. Core Thing/Plant rejection criteria

For Core Thing/Plant assets, reject and regenerate when any of the following is true. Other asset classes use their owning style specification plus the shared invariants above:

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

## 10. Core crop/item palette swatch reference

See `Docs/References/AMJ_ArtStyle_Palette.svg`.

The swatches are not mandatory exact colors. They document the approved relationship:

- very dark warm-brown outline;
- muted olive foliage;
- one lighter olive plane;
- warm yellow-gold grain;
- optional darker gold/brown secondary plane;
- pale cream for cleaned grain.

The consistent relationship and low number of planes matter more than exact RGB values.

## 11. Fixed reused components

Pixel-exact reuse is a production concern, not a visual-style rule. When an asset intentionally reuses a visible component, follow `Docs/GoldenPaths/FixedImageTemplates.md` and the owning family pipeline.
