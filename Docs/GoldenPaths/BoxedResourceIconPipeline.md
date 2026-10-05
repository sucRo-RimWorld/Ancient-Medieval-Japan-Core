# Boxed Resource Icon Pipeline — Golden Path

This document is the production contract for AMJ resource icons that share a box/masu/container while changing only the contents.

## Why fixed pixels are not enough

A deterministic template can preserve every container pixel and still produce a bad icon. The shared part may be registered at the wrong scale on the canvas, or the contents may be too small, too low, too sparse, or layered unnaturally. Therefore boxed-resource production has two independent gates:

1. **structural identity** — shared container pixels remain exact;
2. **composition identity** — the final icon matches an accepted filled exemplar in frame occupancy, fill amount, apparent height, and occlusion.

Passing only the structural gate is not sufficient.

## Required family assets

Before a boxed-resource family is production-active, register all of the following:

- an author-approved **filled exemplar** at known source resolution, stored persistently and identified by SHA-256;
- an empty lossless master at final production resolution;
- a protected/editable mask for structural pixel locking;
- a **required-fill guide** for the area a normal full stack must substantially occupy;
- an **allowed-fill guide** defining where contents may extend without damaging the container silhouette;
- a manifest containing paths, hashes, canvas size, frame/alpha bounding box, fill-guide semantics, layer order, and production status.

The empty master should be derived from, or explicitly aligned against, the accepted filled exemplar. Do not independently generate an empty container and then declare it canonical because it looks similar.

## Registration gate

A template remains blocked/inactive until all of these are true:

1. The outer container/frame occupancy on the final canvas matches the accepted filled exemplar.
2. Key rim corners, angle, silhouette, transparent margins, and overall scale are aligned to the accepted exemplar.
3. The required-fill and allowed-fill guides are registered.
4. A representative contents layer is composed through the deterministic tool.
5. The representative final icon is compared to the accepted exemplar at 256 px and at game-like small size (about 64 px).
6. The author accepts the representative composite.
7. Protected RGBA differences are exactly zero and PNG integrity checks pass.

An empty master by itself cannot activate a family.

## Contents contract

For the normal/full boxed-resource presentation:

- contents must visually fill the interior instead of reading as a small pile placed on the floor;
- the pile footprint should approach the inner rim on all four sides in the same manner as the accepted exemplar;
- apparent pile height and central mound must remain in the accepted family range;
- visible empty floor must not increase substantially relative to the accepted exemplar;
- individual resource shapes may change, but their overall mass/occupancy must remain comparable;
- stack-count variants may intentionally use less content, but each variant needs an explicit occupancy target rather than arbitrary scaling.

Do not shrink the entire contents group merely to make it fit. Redraw/rearrange contents inside the registered guides.

## Layer order

Use deterministic compositing:

1. fixed rear/interior master;
2. variable contents layer;
3. fixed front/side rim or other foreground container layer where required;
4. restore all protected master RGBA pixels exactly.

Never resize, rotate, recolor, blur, quantize, or regenerate the shared container after registration. Do not resize the completed icon after composition; work on the final canvas from the start.

## Visual-reference rule

For every derivative, inspect the actual accepted filled exemplar before creating the contents. Text instructions and the empty master alone are insufficient. If the reference cannot be retrieved or its SHA-256 does not match the registered value, stop rather than approximating from memory.

A mechanically valid result that visibly diverges from the accepted filled exemplar is rejected. CI success never overrides a failed visual-composition check.

## Current masu status

Accepted filled reference:
- Library: `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`
- SHA-256: `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`
- source: 1254×1254 PNG
- normalized 256×256 alpha envelope: `[17, 28, 239, 235]`

Current v1 empty master:
- `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`
- alpha envelope: `[34, 42, 232, 213]`

The v1 master is therefore visibly underscaled and is **BLOCKED for production derivatives**. Its manifest remains in the repository so tooling fails closed and records why it cannot be used.

Masu v2 activation requires a corrected empty master aligned to the accepted filled reference plus required/allowed fill guides and an author-approved representative filled composite.

## Validation commands

After v2 is active, boxed-resource derivatives must pass the family manifest through:

`python Scripts/Art/fixed_template.py compose <manifest> <contents-layer.png> --output <final.png>`

`python Scripts/Art/fixed_template.py validate <manifest> <final.png>`

Then run the family regression test and:

`python Tests/validate_png_assets.py`
