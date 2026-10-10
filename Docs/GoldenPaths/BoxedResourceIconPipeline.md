# Boxed Resource Icon Pipeline — Golden Path

This file owns only the **masu boxed-resource family**. Shared visual style comes from `Docs/ArtStyle.md`; general source preservation, ImageGen permission, export, and PNG validation come from `Docs/GoldenPaths/TextureAssetPipeline.md`.

## Current production model

When ImageGen is used for new boxed resources, it creates only the **contents source layer**. Other privately screenable source-production methods may be used under the shared texture pipeline. The wooden masu is never generated.

Do not rely on ImageGen to solve the masu projection. The generated subject/style layer is passed through the deterministic `Scripts/Art/normalize_masu_contents.py` perspective normalizer before it is treated as a placement candidate.

Final placement, scale, masking, overlap, and contact with the masu are adjusted manually in an image editor.

The canonical empty masu is reused as the composition source. Because the visible contact/occlusion boundary changes with the contents and no stable protected region is currently approved for this manual path, this workflow does **not** claim the active fixed-template zero-difference guarantee. The archived v4 masks remain diagnostic only. Do not use their PASS/FAIL state as a production gate for manually composed icons.

Previous automatic contact/mask experiments remain research/diagnostic material only. They are not required reading for ordinary contents generation and are not the active production path.

## Canonical visual references

Before generating contents, open and compare against:

- empty masu master: `Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.png`;
- approved filled reference: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`;
- preserved high-resolution filled reference: `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png` (1254×1254; original identity/hash documented in `Art/Sources/README.md`);
- a subject-specific visual reference for the material being generated (rice for rice, soybeans for soybeans, etc.); for the accepted dehulled-buckwheat source, use `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png`.

Reference roles are deliberately separated:

- the **empty masu** defines the container geometry and the apparent projection/opening plane;
- the **approved buckwheat-in-hull image** defines approximate fill amount, mound footprint, composition density, and the target AMJ/MO simplification level;
- the **subject-specific reference** defines the material's own shape, aspect ratio, surface character, and characteristic color;
- relevant accepted AMJ/MO item art defines outline weight, palette restraint, and shading density.

Do **not** inherit buckwheat's triangular/angular grain shape, dark color, faceting, or material character when generating another subject. The buckwheat image is not a universal grain-shape template.

If any required reference cannot actually be retrieved and visually inspected, stop before ImageGen. Do not substitute memory, filename-only knowledge, or an unrelated material and do not claim a visual comparison that was not performed.

Do not regenerate or restyle the masu.

## Contents-source generation

Generate **contents only**, on transparency.

The raw generated source owns **material identity and AMJ/MO style**, not final container perspective. Prefer a neutral or near-top view that keeps the individual pieces readable enough for deterministic projection.

The source layer must:

- inherit the AMJ item/resource style from `Docs/ArtStyle.md`;
- use a **boxed-resource-specific line hierarchy**: within the contents layer, the outer silhouette remains stronger than internal grain/piece boundaries. The outer silhouette may retain the reference-like thickness needed to hold the pile together; it does **not** have to be mechanically thinner than the masu rim;
- keep the contents visually subordinate to the wooden masu primarily by using a **lighter RGB outline color** than the masu rim/outer contour, not by reducing opacity or automatically shaving the contour width;
- "lighter/paler outline" means a lighter **opaque color**, not reduced alpha. Keep substantive outline pixels opaque; transparency is for the background and anti-aliased edge pixels only;
- internal grain/piece boundaries are thinner and lighter than the contents outer silhouette and may be quite pale, but should likewise use opaque color rather than semi-transparent strokes;
- do not give every grain/piece an equally heavy dark outline; internal lines are subordinate separators and may be quite light as long as the material remains legible;
- use a limited palette and flat/simple shading;
- avoid glossy per-piece highlights, deep AO between every grain, photorealism, and painterly rendering;
- simplify the bulk into readable clustered pieces rather than rendering every particle, while preserving the subject's characteristic piece shape;
- keep piece size broadly consistent instead of introducing an artificial near/far scale gradient;
- form one compact continuous pile/footprint with information density comparable to the approved boxed-resource reference;
- contain no wooden box, rim, background, text, UI, or decorative ground shadow.

The raw generation target is a **source layer**, not a placement-ready icon. Do not ask ImageGen to solve the final rim occlusion, contact edge, or exact masu projection.

If the requested change is only a deterministic adjustment to an existing candidate — such as making the contents outline RGB lighter, thinning a contour, changing alpha cleanup, resizing, masking, or projection — do **not** regenerate the image with ImageGen. Edit the existing contents layer deterministically. In particular, never send the full masu composite back through ImageGen merely to change the contents outline: that would expose the fixed wooden masu to unwanted redrawing.

## Automated candidate preparation

Do not manually perform first-pass generation inspection. Run the family preparation entry point:

```bash
python Scripts/Art/prepare_boxed_resource_candidate.py \
  Work/Contents_Source.png \
  --output-dir Work/BoxedCandidate
```

It automatically:

1. runs `Scripts/Art/generated_asset_qa.py` with `Docs/References/AMJ_BoxedResource_GenerationQA.json` to verify that the source is a decodable PNG with visible content and transparency;
2. calls `Scripts/Art/normalize_masu_contents.py` to create the transparent placement guide;
3. checks that the derived PNG is still decodable, visible and transparent;
4. writes diagnostic JSON reports and a comparison sheet of raw contents, projected contents and a 64 px view.

**Color-bin counts, edge density, dark outline ratios, arbitrary canvas-fill percentages, and low-alpha percentages do not reject candidates.** They cannot establish art quality and can reject legitimate subject-specific shapes, antialiased edges or author-accepted art. The previous numeric rice line-hierarchy calibration is no longer a validation standard. Judge line hierarchy, material identity, simplification, placement and perspective from the actual accepted references, at game size. Structural QA does not constitute visual acceptance.

The perspective normalizer:

- zeros low-alpha pixels including hidden RGB so generated dark glow/background residue cannot turn into a resampling halo;
- crops to the actual visible contents;
- deterministically projects that crop onto the shared diamond-like masu contents plane;
- keeps the output background transparent;
- never adds, redraws, or edits the wooden masu.

The default projection is a **contents-plane normalization guide**, not a cavity clipping mask and not a claim that final contact/occlusion is automatic. Final scale/placement and rim overlap remain manual. Do not tune the projection separately for each material merely to make a bad generation look acceptable; change the registered default only after cross-material visual review.

## Pre-presentation candidate gate

After automated mechanical preparation passes, the agent performs the remaining **automatic semantic visual QA** against the actually viewed references. The author is not the first-pass checker.

Reject internally when any of the following is true:

- the subject does not read as the requested material at game-like size;
- another reference material's geometry has leaked into it (for example, rice becoming triangular/faceted like buckwheat or stone);
- the normalized footprint still cannot be placed naturally on the masu opening plane;
- a systematic near/far scale gradient has been baked into the source without a subject-specific reason;
- the contents outer silhouette is not clearly stronger than the internal piece boundaries;
- the contents outline visually competes with or overpowers the wooden masu rim after composition; **outline thickness by itself is not a failure** when the lighter RGB color keeps the contents subordinate;
- substantive contents outline pixels are made faint through reduced alpha instead of a lighter opaque RGB color;
- internal grain/piece boundaries are as thick/dark as the contents outer silhouette, making the pile read as many disconnected outlined objects rather than one mass;
- shading is glossy, heavily modeled, painterly, or uses deep AO on each individual piece;
- particle count/detail is high enough to become noisy at roughly 64 px;
- the generated layer contains any wood, container rim, box, background, UI, text, or decorative shadow;
- the source or normalized output is not usable as a transparent contents-only layer.

Failure/retry behavior and the boundary for immediately visible image generation follow Project `Docs/GoldenPaths/TextureAssetPipeline.md`; this family defines no separate attempt quota. Before adding a boxed-resource-specific rule, determine whether the failure is caused by the reference role, subject description, deterministic projection, or a capability limit.

For privately screenable sources, mechanical QA, deterministic projection, agent semantic QA and the review sheet must pass before the **single remaining human gate: final visual acceptance**.

## Manual composition

The author/compositor places and adjusts the contents against the canonical masu in an image editor.

Typical order:

1. canonical empty masu as the base;
2. projected contents from `prepare_boxed_resource_candidate.py`;
3. author-controlled front/upper container masking or overlay where needed.

Position, scale, local erasing/masking, and front-edge overlap are manual visual decisions. A small manual perspective correction is allowed when required by the actual content/contact, but the routine base projection should come from the deterministic normalizer rather than asking ImageGen to rediscover it. Do not encode a new universal cavity clipping mask merely to avoid the final manual contact step.

If a reusable front/upper overlay becomes author-approved and is registered as a fixed component later, it may be added to the fixed-template system. Until then, do not invent or reconstruct such a raster from memory.

## Visual acceptance

Before a final boxed icon is treated as accepted:

- compare it with the approved filled reference at 256 px and about 64 px;
- confirm the contents and masu share the same apparent perspective;
- confirm the front/side rim overlap reads naturally;
- reject top-down contents, pasted-on/flat appearance, cut-off outlines, halos, excessive particle detail, or style drift from AMJ/MO;
- preserve the canonical masu appearance except for deliberate manual occlusion/contact handling.

After the final composite is accepted, use the general texture pipeline and PNG integrity gate for repository integration.

## Research material

`Docs/Research/BoxedResourceOcclusionAudit.md`, the v4 study manifest/region masks, and related study commands are retained as historical/diagnostic evidence. They may be used when investigating automation again, but they do not add production rules to the current manual-composition workflow.
