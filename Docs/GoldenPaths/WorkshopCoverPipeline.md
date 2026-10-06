# AMJ Workshop Cover Golden Path

This is the deterministic production path for Ancient & Medieval Japan Workshop covers. It exists so a different chat, agent, or context can produce the same series format without asking an image model to redraw the common portion.

## Canonical persistent visual assets

The following author-approved/canonical images are stored in the user's persistent Library and must be retrieved from there in a new chat:

- `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`
  - author-approved visual reference
  - 960×540
  - file SHA-256: `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658`
- `/AMJ/References/AMJ_WorkshopCover_CommonBase.png`
  - fixed common raster used for composition
  - 960×540
  - file SHA-256: `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362`
- `/AMJ/References/AMJ_WorkshopCover_VariableMask.png`
  - hard mask defining what is allowed to change
  - 960×540
  - file SHA-256: `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622`

`Docs/WorkshopCoverStyle.md` remains the semantic/style source of truth. These raster files are the pixel-level source of truth for format reproduction.

## What is fixed

The common raster owns the parchment field, top/bottom neutral ornaments, `Ancient & / Medieval / Japan` title block, divider and flower mark. These pixels are not regenerated.

The mask allows only:

- the addon-name slot (`x=66..310`, `y=378..426`); and
- the addon illustration area from `x=330` to the right edge.

Everything outside those variable regions is forcibly restored from the canonical base during composition. A generated image cannot overwrite the common-left region even if it accidentally contains text, symbols, or a different background there.

## Required workflow

1. Read `AGENTS.md`, `main:Docs/Coordination.md`, `Docs/WorkshopCoverStyle.md`, and this file.
2. Retrieve and visually inspect `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`. If it cannot be viewed, stop; do not generate a cover from memory/text alone.
3. Retrieve/materialize `AMJ_WorkshopCover_CommonBase.png` and `AMJ_WorkshopCover_VariableMask.png` from the Library. Verify their hashes if there is any doubt about identity.
4. Resolve the addon-specific right-side composition from the current user request and any already-approved addon specification. Reuse an existing approved composition when one exists. Do not insert a mandatory extra approval round unless the user explicitly asks for proposal/review-first work.
5. Generate **only the addon-specific illustration**, preferably as a transparent-background PNG. Do not ask ImageGen to draw the AMJ title, parchment background, divider, ornaments, or addon label.
6. Compose the final cover with `Scripts/build_workshop_cover.py`. The compositor adds the addon label and forcibly restores every locked common pixel.
7. Run `Scripts/validate_workshop_cover.py` on the composed PNG. A failure means the output is not an AMJ-format cover.
8. Visually compare the composed image with the approved Core reference for balance and with the approved proposal for the right-side subject.
9. Only after deterministic validation and visual inspection pass may the image be shown as a candidate for author approval.
10. Once the author approves it, preserve the accepted cover and do not casually regenerate it.

## Example

After materializing the Library template files to local paths:

```bash
python Scripts/build_workshop_cover.py \
  --base Work/AMJ_WorkshopCover_CommonBase.png \
  --mask Work/AMJ_WorkshopCover_VariableMask.png \
  --right-layer Work/Fermentation_Right.png \
  --addon Fermentation \
  --output Work/AMJ_Fermentation_Cover.png

python Scripts/validate_workshop_cover.py \
  Work/AMJ_Fermentation_Cover.png \
  --base Work/AMJ_WorkshopCover_CommonBase.png \
  --mask Work/AMJ_WorkshopCover_VariableMask.png
```

Use `--mode canvas` when the generated transparent layer is already designed on a 16:9 full canvas. The final hard mask still clips all generated changes out of the locked common region.

## Guarantee boundary

This pipeline gives a real deterministic guarantee for the **format**, not for the generated illustration:

- locked common pixels are copied from one canonical raster and can be validated pixel-for-pixel;
- the addon label occupies one fixed slot and is rendered by the compositor rather than ImageGen;
- the right-side illustration remains creative/generated content and therefore is not pixel-deterministic.

Thus separate chats/contexts can reproduce the same AMJ cover format as long as they retrieve the same Library base/mask and use the compositor. Direct whole-cover image generation is no longer the production path.

## Regression check

Run:

```bash
python Tests/test_workshop_cover_template.py
```

The test deliberately composites an opaque magenta full-canvas layer. It must still preserve every locked pixel from a synthetic common base. This catches accidental removal or reversal of the hard-mask guarantee.
