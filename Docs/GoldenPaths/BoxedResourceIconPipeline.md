# Boxed Resource Icon Pipeline — Golden Path

This document is the production contract for AMJ resource icons that share a box/masu/container while changing only the contents.

## Command semantics for this family

For boxed-resource icons, 「作成」「制作」「続けて」 always means **template-based local creation**, not whole-image generation and not automatic ImageGen use. Use the registered reference/master/masks and deterministic tooling.

Only an explicit author request containing 「生成」 permits ImageGen, and then only for the **contents layer**. The masu, registered reference, and final whole icon must not be generated.

If a new contents layer cannot be derived locally and no generation was requested, stop as BLOCKED rather than invoking ImageGen.

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

## Agent self-QC before review or registration

The agent owns objective cleanup. Before showing a candidate as ready, and again before registering a master, inspect the 256 px image and a game-like ~64 px reduction. Automatically correct any known fixable defect that does not alter the accepted visual direction, including jaggies from upscaling, resampling artifacts, halos, clipped edges, layer seams, leftover pixels from the exemplar, incorrect frame occupancy, or an obviously under-filled/over-filled container.

Do **not** defer a known technical defect to the author with "acceptable?" or "妥協範囲?" when it can be corrected deterministically. Only request author judgment for a real design choice or tradeoff. A candidate with a known fixable defect is not registration-ready.

## Identity-exemplar validation before new resources

Before using a boxed-resource family for a *different* material/resource, validate the pipeline against its approved filled exemplar.

For the current masu family, the expected output is the registered **buckwheat-in-hull** exemplar itself. The validation run must:

1. use the registered empty masu/master and the intended reusable content/occlusion layer structure;
2. recompose the approved buckwheat-in-hull icon without changing its color/material;
3. preserve all protected/common pixels exactly;
4. require **0 RGBA pixel differences** against the registered representative final for the identity exemplar;
5. fail closed if the result needs manual recolor, blur, local patching, or another ad-hoc correction to match the reference.

A diagnostic exact-delta round trip may prove that the reference/master pair is internally consistent, but it does not by itself prove that the reusable production layer structure is correct. The production layer structure must pass the same zero-difference exemplar reconstruction before any other resource is attempted.

### Current identity result: PASS

The current masu v2 family now passes the intended identity validation through the **actual reusable production compositor**, not a diagnostic delta shortcut.

- registered compose mode: `replace_rgba`
- identity variable layer: `Docs/References/AMJ_BuckwheatInHull_IdentityVariable.png`
- expected final: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`
- result: **0 RGBA pixel differences**
- protected/common pixels: **0 RGBA differences from the empty master**

Why replacement is required: the approved variable RGBA already contains its own antialiasing/occlusion against the cavity. Alpha-compositing it over the empty master a second time changes those pixels. The reusable contract therefore replaces RGBA only inside the editable mask while leaving every protected pixel from the master untouched.

This passes the validation target requested by the author: the approved **buckwheat-in-hull** exemplar can be reconstructed exactly through the standard registered template path. New resources may now use this same structural contract, but must provide their own clean variable RGBA layer.

## Registration gate

A template remains blocked/inactive until all of these are true:

1. The outer container/frame occupancy on the final canvas matches the accepted filled exemplar.
2. Key rim corners, angle, silhouette, transparent margins, and overall scale are aligned to the accepted exemplar.
3. The required-fill and allowed-fill guides are registered.
4. A representative contents layer is composed through the deterministic tool.
5. The representative final icon is compared to the accepted exemplar at 256 px and at game-like small size (about 64 px).
6. The representative composite is already author-approved or is compared against an author-approved exemplar. Technical cleanup that preserves that approved design is performed proactively before registration; a new approval is needed only for a substantive visual change.
7. Protected RGBA differences are exactly zero and PNG integrity checks pass.

An empty master by itself cannot activate a family.

## Identity round-trip gate

Before changing material/color/contents, prove that the template decomposition itself is correct.

1. Load the registered empty master and registered filled exemplar.
2. Compute an **exact variable-pixel mask** from pixels whose RGBA differs between those two authoritative images.
3. Extract the exemplar's pixels only at that exact mask.
4. Recompose those pixels onto the empty master.
5. Require the recomposed image to be pixel-identical to the exemplar: **0 differing pixels**.
6. Only after this passes may a new material variant be derived.

Do not use the broad editable mask or a hand-drawn/interior polygon as the production content mask for this identity test. Those masks are permission/coverage guides, not a proof of correct layer decomposition. If exact round-trip fails, stop and repair the template decomposition instead of tuning color.

## High-resolution contents-source rule

When the family later creates a genuinely new resource, use the highest authoritative source available and downsample once at export. However, the **current validation phase does not recolor or redesign Soba**: it must first reproduce the registered buckwheat-in-hull exemplar exactly through the reusable template/layer structure.


## Variable-patch scaffold contract

For a `replace_rgba` family, the variable input is a **complete rendered patch of the editable cavity**, not a transparent object-only contents layer. Starting from transparency would erase the empty-master cavity/rim-adjacent pixels selected by the editable mask and recreates the exact failure mode seen during the Soba validation loop.

Every genuinely new resource must therefore start with:

`python Scripts/Art/fixed_template.py scaffold <manifest> --output <variable-patch.png>`

The scaffold copies the registered empty-master RGBA exactly inside the editable mask and is transparent outside it. Draw or composite the new resource **onto this scaffold** without changing its canvas size. Do not clear unchanged cavity pixels to transparency.

For `replace_rgba`, required-fill occupancy is measured by **RGBA differences from the registered empty master inside the required-fill guide**, not by alpha coverage. The scaffold by itself must fail the required-fill gate; a transparent object-only layer must fail the editable-patch completeness gate.

The finished variable patch is then passed to `compose`. This ensures that unchanged cavity pixels remain identical to the registered master while actual resource pixels replace only the permitted region.

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

## Candidate lifecycle and contamination disposal

Candidate assets are disposable working material, not reference material.

If any step reveals that a candidate chain used the wrong registered reference, wrong common-part pixels, a broken/obsolete mask, an unintended whole-image regeneration, contaminated color/edge data, or another invalid production path, then **the entire derivative chain from that point is invalid**.

Required response:

1. Stop using every descendant candidate immediately.
2. Delete persistent Library copies of those candidates/reviews/previews.
3. Delete local working copies and generated comparison sheets derived from them.
4. Remove durable documentation that presents discarded candidates as reusable assets.
5. Keep the authoritative master/reference/manifest only.
6. Record the invalidation in `Docs/Coordination.md`.
7. Restart from the last verified authoritative source; do not "repair" a contaminated candidate unless the repair is a deterministic reconstruction from authoritative sources with no contaminated pixels retained.

Do not retain invalid candidates merely because they might be useful for visual comparison. If a diagnostic example must be preserved, it must be clearly segregated as non-source diagnostic material with an unambiguous `INVALID_`/failure label and must never be accepted by production tooling as a reference.

## Reference-integrity rule

Every comparison sheet and palette judgment must use the exact manifest-registered `representative_final`. Do not use an ad-hoc local alias, a prior candidate, a regenerated image, or a visually similar copy as the "reference".

Run:

`python Scripts/Art/boxed_resource_review.py Docs/References/AMJ_Masu_Template.json <candidate.png> --output <review.png>`

The script verifies the registered reference SHA-256 before rendering the 256px and ~64px comparison. Hash mismatch or missing reference is a hard failure. A reference presented to the author without this verification is invalid.

## Visual-reference rule

For every derivative, inspect the actual accepted filled exemplar before creating the contents. Text instructions and the empty master alone are insufficient. If the reference cannot be retrieved or its SHA-256 does not match the registered value, stop rather than approximating from memory.

A mechanically valid result that visibly diverges from the accepted filled exemplar is rejected. CI success never overrides a failed visual-composition check.

## Current masu status

Accepted filled reference:
- Library source: `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`
- source SHA-256: `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`
- normalized repository exemplar: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`
- normalized alpha envelope: `[17, 28, 239, 235]`

**Masu v2 is ACTIVE.** The previous upscaled v2 candidate was not registered because self-QC found visible resampling roughness. The active v2 master was rebuilt from high-resolution sources: the author-approved filled exemplar supplies the protected exterior/rim pixels, while only the editable cavity is replaced with the clean empty interior. This removes the scaling artifacts while keeping the approved outer appearance exact.

Registered v2:
- master: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`
- allowed/editable fill mask: `Docs/References/AMJ_Masu_EditableMask.png`
- required-fill guide: `Docs/References/AMJ_Masu_RequiredFill.png`
- manifest: `Docs/References/AMJ_Masu_Template.json`
- representative final: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`

The representative final has zero RGBA differences from the master outside the editable mask. The required-fill guide is a strict subset of the allowed/editable mask, and the compositor rejects variable layers that do not span/cover the registered required-fill region.

## Validation commands

After v2 is active, boxed-resource derivatives must pass the family manifest through:

`python Scripts/Art/fixed_template.py scaffold <manifest> --output <variable-patch.png>`

Edit the scaffold to add the resource, then:

`python Scripts/Art/fixed_template.py compose <manifest> <variable-patch.png> --output <final.png>`

`python Scripts/Art/fixed_template.py validate <manifest> <final.png>`

Then run the family regression test and:

`python Tests/validate_png_assets.py`
