# AMJ Workshop Cover Style

This document is the source of truth for the shared visual system used by **Ancient & Medieval Japan (AMJ)** Workshop cover images.

The current baseline is the author-approved 2026-10-05 Environment concept: a warm parchment field, strong left-side typography, and a symbolic flat illustration occupying the right side. It replaces the earlier dark-map / scenic-landscape cover direction.

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

## 4. Shared typography block

The left side is the series identity and should remain consistent between covers.

### Japanese title

Use:

**中世日本OH**

Rules:
- starts near the upper-left;
- large, bold, immediately readable at thumbnail size;
- one consistent size across the whole phrase;
- use either a strong Mincho or restrained heavy Gothic style;
- do not use brush-script calligraphy;
- no glow, sparkle, bevel, metallic shine, or decorative stroke effects.

### English series title

Use:

**Ancient & Medieval Japan**

Rules:
- place below the Japanese title;
- use a strong serif or similarly restrained historical editorial face;
- visually emphasize the initials **A / M / J** through weight, size, or one muted accent color;
- keep the rest of the title darker and quieter;
- the full phrase must still read naturally rather than looking like three disconnected initials.

### Addon name

Place the addon name below the series title in smaller type.

Examples:
- CORE
- ENVIRONMENT
- FERMENTATION
- SAKE
- COASTAL GATHERING
- REPAIR & REUSE
- JAPAN ONLY
- FACTIONS
- EVENTS
- BACKGROUNDS

Rules:
- no red brush-stroke badge;
- no decorative plaque;
- no Japanese decorative flower between rules;
- use simple tracking / spacing and restrained typography;
- addon name position should be consistent across the series.

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
- decorative cloud bands used only because they look Japanese.

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
| Core | cereal heads / rice or grain / beans / wooden tub or mortar / one small thatch fragment if needed |
| Environment | flat mountain bands / thin river / representative Japanese trees |
| Fermentation | soybeans / koji / fermentation jar / miso tub or vat |
| Sake | coarse grain / polished rice / sake jar / brewing vat / clear-vs-cloudy sake progression; no people |
| Coastal Gathering | shellfish / seaweed / shallow coast or tidal-flat shape / simple basket or drying element |
| Repair & Reuse | worn tool / repaired tool / reclaimed material pieces / simple bench or repair symbol |
| Japan Only | selective keep/remove contrast using familiar AMJ/MO object silhouettes; avoid flags or national symbols |
| Factions | village / temple-estate / local warrior or outlaw affiliation represented by buildings, banners, goods, or territory markers rather than people |
| Events | weathered notices, supply bundles, damaged field, road marker, abandoned goods, or other event consequences rather than characters |
| Backgrounds | tools, clothing bundles, work objects, travel pack, farming / craft / hunting objects representing life histories without portraits |

## 11. Required workflow

For every new AMJ Workshop cover:

1. **Do not generate immediately.**
2. First propose the composition and design in words.
3. State:
   - the 2–5 main motifs;
   - their approximate placement;
   - the intended silhouette hierarchy;
   - how the cover differs from adjacent AMJ addons;
   - any historically specific object that might need verification.
4. Wait for author approval or revision.
5. Generate only after the composition is accepted.
6. If the generated image becomes scenic, realistic, too saturated, too detailed, or stylistically inconsistent, return to the approved composition and regenerate with stronger simplification.
7. Once a cover is accepted, preserve that accepted image as the reference for that addon. Do not casually regenerate it.

## 12. Prompt baseline

Use this shared semantic baseline when generating a cover:

> Wide 16:9 Steam Workshop cover for the Ancient & Medieval Japan series. Warm pale parchment background with extremely subtle paper grain. Left side reserved for the shared typography: large bold Japanese title “中世日本OH”, beneath it “Ancient & Medieval Japan” with A, M, and J visually emphasized, and the addon name below in smaller restrained type. Right side is a symbolic, highly simplified flat editorial illustration, not a scenic landscape. No people. No stereotypical Japanese decorative symbols. Low-saturation limited palette. Each motif uses about three colors: base, darker plane, lighter plane, with only a very light gradient if useful. Large clean silhouettes, minimal detail, no photorealism, no cinematic lighting, no painterly texture, readable at small Workshop thumbnail size.

Then append only the addon-specific approved motif/composition instructions.

## 13. Reference layout

See:

`Docs/References/AMJ_WorkshopCover_Template.svg`

The SVG is a layout/style schematic, not a production cover and not a substitute for the author-approved generated reference image.
