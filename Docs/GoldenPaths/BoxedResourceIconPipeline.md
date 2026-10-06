# Boxed Resource Icon Pipeline — Golden Path

> **2026-10-06 occlusion-audit integration:** the first v3 implementation that physically split the canonical masu into complementary rear/front rasters is **superseded**. Visual inspection found damaged pixels at the split boundary. The separate MO audit also shows that upper/contact-region visibility depends on the contents. New-resource production is therefore blocked. The next model keeps the **full canonical master intact as the base/rear**, renders transparent **contents/contact** artwork above it without a cavity/pile clipping mask, then reasserts only conservative **hard-fixed foreground** wood from exact master pixels. The contact zone remains occludable. Activation requires contrasting-content-shape tests plus 256px/~64px visual review.

> Research addendum (2026-10-06): [the occlusion/fixed-region audit](../Research/BoxedResourceOcclusionAudit.md) assessed the preceding v2 snapshot. Its identity PASS proved exemplar reconstruction, not natural different-content production. The separate v3-layered change is preserved here; this research publication does not validate v3 or prove that restoring a fixed foreground permits natural contents-over-rim occlusion.

This document is the production contract for AMJ resource icons that share the Japanese masu while changing only the contents.

## Command semantics

For boxed-resource icons, 「作成」「制作」「続けて」 means deterministic local production from registered assets. It does not authorize ImageGen.

Only an explicit request containing 「生成」 permits ImageGen, and then only for the **contents** source. Never regenerate the masu or the final whole icon.

## Active architecture: three layers

The masu family uses this exact z-order:

1. **fixed rear masu** — back rim, rear/interior walls and floor;
2. **transparent contents** — the only resource-specific artwork;
3. **fixed front/side masu** — foreground rim and visible exterior/front walls.

This is mandatory. The foreground and rear are exact pixel selections from the canonical master; they are not redrawn or recolored.

### Why the old two-layer path is forbidden

Do not model the icon as “empty master + contents clipped/replaced through one cavity/pile/editable mask”.

That approach cannot represent the masu's perspective and occlusion correctly. It caused repeated failures at the upper-left/upper-right rim, boundary-color contamination, and complete-cavity replacement artifacts. Expanding or tuning a geometric mask does not fix the structural problem.

The historical editable mask and exact-variable/replace-RGBA identity assets remain useful as diagnostics/history, but they are **not** the production compositor for new resources.

## Contents layer contract

The contents layer is a normal transparent RGBA image on the final 256×256 canvas.

- Do **not** clip it to the historical editable mask.
- Do **not** clip it to a guessed diamond, pile polygon, or other simple cavity shape.
- It may extend underneath the foreground rim; the front layer will occlude it.
- It must not contain any masu wood pixels.
- It must not be resized after composition.
- For locally created art, prefer a high-resolution source and downsample the contents once before final composition.
- Item/resource art follows `Docs/ArtStyle.md`: few broad color planes, thick warm-brown outline, no texture noise, readable at about 64 px.

The required-fill guide is a **validation target only**. It measures whether a normal/full resource visually fills the box. It is not a clipping mask.

## Canonical fixed layers

The source of truth remains:

- master: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`
- manifest: `Docs/References/AMJ_Masu_Template.json`
- approved filled visual reference: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`
- persistent high-resolution reference: `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`

The manifest registers semantic foreground regions. Tooling derives rear/front layers directly from the hashed master.

An empty reconstruction must satisfy:

`alpha/replacement compose(rear, front) == canonical master`

with **0 decoded RGBA pixel differences**.

## Composition algorithm

For a new resource:

1. Verify the master/reference hashes.
2. Derive the fixed rear and fixed foreground from the manifest.
3. Create/draw the contents on a transparent 256×256 canvas.
4. Composite contents over the rear.
5. Restore/render the fixed foreground last.
6. Run the mechanical gates.
7. Inspect the result at 256 px and about 64 px.
8. Only then present it as a candidate.

The front layer is the occlusion model. Do not repair boundary problems by recoloring or blurring the contents edge after composition.

## Mechanical gates

A candidate is not presentable until all of these pass:

1. **Empty-master round trip:** rear + front = master, 0 RGBA differing pixels.
2. **Fixed foreground:** every registered front/side wood pixel in the final output equals the canonical master pixel exactly.
3. **Required-fill occupancy:** the final resource differs from the empty master across the registered required-fill target by at least the manifest threshold.
4. **Visible-envelope guard:** the final alpha must not leak outside the exact union of the canonical empty-master alpha and the registered representative-final alpha.
5. PNG integrity passes.
6. Canvas remains 256×256.

The visible-envelope guard is a fail-closed diagnostic based on authoritative rasters. It is not used to clip the contents.

## Visual gates

Mechanical validity does not make a good icon. Before showing a candidate:

- compare against the registered filled reference at 256 px and about 64 px;
- confirm the resource reads as being **inside** the masu, not pasted onto it;
- confirm the upper-left and upper-right contacts do not show stale source color or edge contamination;
- confirm the front rim/wood is unchanged;
- confirm the contents are not a single flat color when the accepted design requires visible per-piece variation;
- reject known jaggies, seams, halos, local blur patches, or resampling noise yourself.

Do not ask the author to accept a known deterministic defect.

## Reference integrity

Every comparison sheet must load the manifest's registered `representative_final` and verify its SHA-256.

Run:

`python Scripts/Art/boxed_resource_review.py Docs/References/AMJ_Masu_Template.json <candidate.png> --output <review.png>`

Do not substitute an ad-hoc local alias, regenerated image, or remembered reference.

## Candidate lifecycle

Invalid production branches are disposable. If a candidate used the wrong reference, wrong layer order, two-layer cavity replacement, simple content clipping, unintended whole-image generation, or contaminated pixels:

1. stop using it;
2. delete its descendants and review sheets;
3. do not use it as a reference;
4. record the invalidation in `Docs/Coordination.md`;
5. restart from authoritative assets.

## Current masu status

The physical/canonical master remains the visually approved **masu v2**. The compositor contract is **v3-layered**.

The v3-layered change does not redraw the master. It changes only how future contents are placed relative to it.

The former `replace_rgba` complete-cavity patch path is superseded for new resources. The old identity-variable asset remains historical diagnostic evidence that the old reference/master pair was internally consistent; it is not a reusable contents layer.

## Validation commands

Create a transparent contents scaffold:

`python Scripts/Art/fixed_template.py scaffold Docs/References/AMJ_Masu_Template.json --output <contents.png>`

Draw only the resource into that transparent contents image, then:

`python Scripts/Art/fixed_template.py compose Docs/References/AMJ_Masu_Template.json <contents.png> --output <final.png>`

`python Scripts/Art/fixed_template.py validate Docs/References/AMJ_Masu_Template.json <final.png>`

Then run:

`python Tests/test_masu_template.py`

`python Tests/validate_png_assets.py`
