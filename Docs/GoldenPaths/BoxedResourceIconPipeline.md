# Boxed Resource Icon Pipeline — Golden Path

This file owns only the **masu boxed-resource family**. Shared visual style comes from `Docs/ArtStyle.md`; general source preservation, ImageGen permission, export, and PNG validation come from `Docs/GoldenPaths/TextureAssetPipeline.md`.

## Current production model

For new boxed resources, ImageGen is used only to create the **contents source layer**. The wooden masu is not generated.

Final placement, masking, overlap, and contact with the masu are adjusted manually in an image editor.

The canonical empty masu is reused as the composition source. Because the visible contact/occlusion boundary changes with the contents and no stable protected region is currently approved for this manual path, this workflow does **not** claim the active fixed-template zero-difference guarantee. The archived v4 masks remain diagnostic only. Do not use their PASS/FAIL state as a production gate for manually composed icons.

Previous automatic contact/mask experiments remain research/diagnostic material only. They are not required reading for ordinary contents generation and are not the active production path.

## Canonical visual references

Before generating contents, open and compare against:

- empty masu master: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`;
- approved filled reference: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`;
- high-resolution reference when available: Library `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`;
- a subject-specific visual reference for the material being generated (rice for rice, soybeans for soybeans, etc.).

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

The source layer must:

- inherit the AMJ item/resource style from `Docs/ArtStyle.md`;
- use a strong readable dark outline consistent with the relevant AMJ/MO item references;
- use a limited palette and flat/simple shading;
- avoid glossy per-piece highlights, deep AO between every grain, photorealism, and painterly rendering;
- simplify the bulk into readable clustered pieces rather than rendering every particle, while preserving the subject's characteristic piece shape;
- match the masu opening's oblique/isometric **projection and plane orientation** rather than using a top-down view;
- form a footprint and mound that can be placed naturally inside the opening;
- do **not** impose a generic "rear pieces smaller / front pieces larger" perspective gradient. The approved masu reads closer to a parallel/isometric projection, so piece size should remain broadly stable across depth unless the subject's own pose or overlap genuinely requires foreshortening;
- use overlap, visible top/side planes, and the shared opening-plane orientation to convey depth instead of artificial near/far scaling;
- contain no wooden box, rim, background, text, UI, or decorative ground shadow.

The generation target is a **source layer**, not a finished icon. Do not ask ImageGen to solve the final rim occlusion or final contact edge.

## Pre-presentation candidate gate

A generated contents layer must be reviewed **before it is shown as a usable candidate**. Reject it and regenerate from the same approved references when any of the following is true:

- the subject does not read as the requested material at game-like size;
- another reference material's geometry has leaked into it (for example, rice becoming triangular/faceted like buckwheat or stone);
- the apparent projection conflicts with the masu opening plane or collapses into a top-down pile;
- a systematic near/far scale gradient has been introduced without a subject-specific reason;
- outline strength is materially weaker than the applicable AMJ/MO item baseline;
- shading is glossy, heavily modeled, painterly, or uses deep AO on each individual piece;
- particle count/detail is high enough to become noisy at roughly 64 px;
- the generated layer contains any wood, container rim, box, background, UI, text, or decorative shadow;
- the layer is not usable as a transparent contents-only source.

When a candidate fails this gate, do not repair the failure by adding more ad-hoc permanent rules. First determine whether the failure comes from a missing/ambiguous reference role, a wrong subject description, or a capability limit. Only durable causes belong in this Golden Path.

## Manual composition

The author/compositor places and adjusts the contents against the canonical masu in an image editor.

Typical order:

1. canonical empty masu as the base;
2. generated/edited contents;
3. author-controlled front/upper container masking or overlay where needed.

Position, scale, perspective transform, local erasing/masking, and front-edge overlap are manual visual decisions. Do not encode a new universal cavity shape or one-size-fits-all automatic clipping mask merely to avoid this manual step.

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
