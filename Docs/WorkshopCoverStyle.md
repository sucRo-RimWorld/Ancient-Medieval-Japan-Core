# AMJ Workshop Cover Style

This document is the source of truth for the shared visual system used by **Ancient & Medieval Japan (AMJ)** Workshop cover images.

The current baseline is the author-approved Environment/Core cover system: a warm parchment field, an invariant left-side editorial title block, and a symbolic flat illustration occupying the right side.

## 1. Purpose

Every AMJ cover should be recognizable as part of the same series before the viewer reads the addon name.

The cover system therefore separates:

- a **shared typographic identity** on the left;
- a **feature-specific symbolic illustration** on the right.

Do not redraw the whole series as unrelated posters.

## 2. Canvas and overall composition

- Use a wide **16:9 Steam Workshop cover** composition.
- Keep the left side visually quieter and reserve it for typography.
- Use roughly **40% left / 60% right** as the default visual balance.
- The right-side illustration may overlap slightly toward center, but must not compromise text readability.
- Do not split the canvas with a hard divider, diagonal line, frame, or panel border.
- Use negative space rather than a visible separator.

## 3. Shared background

Use one warm, desaturated parchment-like background across the whole image.

Preferred qualities:
- pale warm cream / off-white;
- extremely subtle paper grain;
- no dark navy common panel;
- no map of Japan as a mandatory background element;
- no heavy vignette;
- no scenic sky gradient.

The background texture must stay quiet enough that the title remains readable at Workshop thumbnail size.

## 4. Shared typography block — invariant series element

The **left side is locked across the series**. Addon-specific cover work may change the right-side illustration and the addon name only. Do not redesign, reinterpret, or replace the common-left composition.

Use the same structure as the accepted Environment/Core references:

1. First line: **Ancient &**
2. Second line: **Medieval**
3. Third line: **Japan**
4. A thin horizontal divider / very small neutral floral mark may sit below the title as part of the shared series ornament.
5. The addon name sits below in a smaller, widely tracked serif label using the approved title-case presentation (for example `Core`, `Environment`, `Fermentation`).

Rules:
- use a restrained editorial serif for the three-line series title;
- keep `Ancient &` and `Medieval` in a dark muted green-charcoal / warm charcoal family;
- use **one muted reddish-brown accent for `Japan`**;
- keep the title large enough to dominate the left side at Workshop thumbnail size;
- preserve the same line breaks, hierarchy, approximate scale, and placement across all covers;
- the addon name must use consistent position and tracking across the series;
- pale beige abstract cloud / paper-cut shapes may be retained only as the **same subdued shared ornament** seen in the accepted series reference; do not invent addon-specific left-side decoration;
- no decorative plaque, glow, metallic effects, or calligraphic rewrite.

The common-left block is not a suggestion. If a generated image changes its wording, line breaks, hierarchy, accent placement, or overall composition, reject that generation even when the right-side illustration is good.
## 5. No stereotypical-Japan decoration

Do not use decorative elements merely to signal “Japan”.

Avoid:
- torii used as generic decoration;
- Mount Fuji used as a generic Japan symbol;
- cherry blossoms used as generic decoration;
- rising-sun motifs;
- family crests / mon used only for atmosphere;
- samurai silhouettes used only for atmosphere;
- decorative kanji or hanging signs;
- generic ukiyo-e ornaments;
- newly invented decorative cloud bands used only because they look Japanese.

Exception: the very small neutral flower/divider and pale beige abstract cloud/paper-cut shapes already used by the accepted Environment/Core common-left design may remain as fixed series ornaments. They are not addon-specific “Japan” symbols and should not be expanded or replaced.

Historical or cultural objects may appear only when they are actually part of the addon subject.

## 6. Right-side illustration language

The right side is **not a scenic landscape painting**.

Treat it as a symbolic editorial illustration or simplified natural-history plate.

Rules:
- no people on any AMJ Workshop cover;
- use 2–5 large motifs rather than a full environment filled with small objects;
- prioritize silhouette and recognition over realistic perspective;
- flatten depth aggressively;
- avoid cinematic lighting;
- avoid photorealism;
- avoid painterly detail;
- avoid small background clutter;
- do not build a complete village scene unless the addon itself requires village structure as the subject.

Each motif should read clearly at small size.

## 7. Color and shading

Use low saturation throughout.

### Per-element budget

For each object / motif:
- target **3 colors**:
  1. base color;
  2. darker plane;
  3. lighter plane;
- a very light gradient may be used inside one of those planes when it improves form;
- do not add many intermediate shades.

### Whole-cover budget

- Keep the overall palette small and related.
- Prefer muted blue-gray, gray-green, olive, tan, ochre, brown, warm gray, and parchment cream.
- Use one restrained accent color at most for AMJ initials or a small functional emphasis.
- Avoid saturated green, bright cyan water, vivid red, and glossy gold.

## 8. Depth and perspective

Depth should come from **overlap and large flat layers**, not realistic rendering.

Good:
- two or three flat mountain silhouettes with atmospheric value changes;
- a thin river ribbon with minimal internal rendering;
- trees distinguished by silhouette;
- large containers or tools shown almost like diagram elements;
- simplified overlapping material groups.

Avoid:
- detailed valleys extending into the distance;
- realistic aerial perspective with many layers;
- photographic camera depth;
- dramatic foreground-to-background scale changes;
- detailed architecture drawn as a complete environment.

## 9. Environment reference

Environment is the current visual baseline for the right-side language.

Use:
- **2–3 completely flat mountain layers**;
- mountains shown only by silhouette and atmospheric value difference;
- **one thin, narrow river**, not a large broad river;
- **three representative tree forms** with clearly different silhouettes;
- no buildings;
- no people;
- no scenic “tourism poster” treatment.

The result should feel like a simplified geography / natural-history plate rather than a mountain landscape.

## 10. Addon motif guide

These are starting points, not immutable final compositions. Each cover must still go through the design-proposal step before generation.

| Addon | Preferred symbolic motifs |
|---|---|
| Core | cereal heads / grain / beans / grain bundle / masu of grain; avoid making flour-processing equipment the primary symbol |
| Environment | flat mountain bands / thin river / representative Japanese trees |
| Fermentation | soybeans / koji / fermentation jar / miso tub or vat |
| Sake | coarse grain / polished rice / sake jar / brewing vat / clear-vs-cloudy sake progression; no people |
| Coastal Gathering | shellfish / seaweed / shallow coast or tidal-flat shape / simple basket or drying element |
| Repair & Reuse | worn tool / repaired tool / reclaimed material pieces / simple bench or repair symbol |
| Japan Only | selective keep/remove contrast using familiar AMJ/MO object silhouettes; avoid flags or national symbols |
| Factions | village / temple-estate / local warrior or outlaw affiliation represented by buildings, banners, goods, or territory markers rather than people |
| Events | weathered notices, supply bundles, damaged field, road marker, abandoned goods, or other event consequences rather than characters |
| Backgrounds | tools, clothing bundles, work objects, travel pack, farming / craft / hunting objects representing life histories without portraits |

## 11. Production handoff

This document owns **Workshop-cover visual style only**. Retrieval of canonical rasters, author-approval stage, fixed pixels, generation scope, deterministic composition, and validation are owned by `Docs/GoldenPaths/WorkshopCoverPipeline.md`.

Before generating variable artwork, visually inspect the registered approved cover reference required by that pipeline. Do not reconstruct the shared cover format from this text alone.

## 12. Image-generation prompt baseline — variable artwork only

The image model is **not** responsible for the final cover format. It creates only the addon-specific right-side artwork that will later be composited onto the fixed common raster.

Use this semantic baseline:

> Addon-specific symbolic illustration for the Ancient & Medieval Japan Workshop-cover series. Transparent background. No title, no letters, no addon name, no parchment background, no divider, no flower mark, and no left-side decoration. Highly simplified flat editorial illustration rather than a scenic landscape. No people. No stereotypical Japanese decorative symbols unless they are genuinely part of the addon subject. Low-saturation limited palette. Each motif uses about three colors: base, darker plane, lighter plane, with only a very light gradient if useful. Large clean silhouettes, minimal detail, no photorealism, no cinematic lighting, no painterly clutter. Design the motif group for the right side of a 16:9 cover and keep the far-left area empty.

Append only the author-approved addon-specific motif/composition instructions. After generation, the artwork must be passed to `Scripts/build_workshop_cover.py`; never publish or approve the raw generated layer as the final cover.

## 13. Reference layout

See:

`Docs/References/AMJ_WorkshopCover_Template.svg`

Pixel-level registration is recorded in `Docs/References/AMJ_WorkshopCover_Template.json` and `Docs/References/AMJ_WorkshopCover_Manifest.md`. The SVG is only a human-readable schematic. The actual fixed format comes from the Library common-base PNG plus editable-mask PNG and the deterministic compositor documented in `Docs/GoldenPaths/WorkshopCoverPipeline.md`.
