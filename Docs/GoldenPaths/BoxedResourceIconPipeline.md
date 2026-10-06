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
- high-resolution reference when available: Library `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`.

Do not regenerate or restyle the masu.

## Contents-source generation

Generate **contents only**, on transparency.

The source layer must:

- inherit the AMJ item/resource style from `Docs/ArtStyle.md`;
- use a strong readable dark outline consistent with the relevant AMJ/MO item references;
- use a limited palette and flat/simple shading;
- avoid glossy per-piece highlights, deep AO between every grain, photorealism, and painterly rendering;
- use a small number of large simplified pieces rather than dozens of individually modeled particles;
- match the masu opening's oblique/isometric perspective rather than a top-down view;
- form a footprint and mound that can be placed naturally inside the opening;
- use smaller/more foreshortened forms toward the rear and larger forms toward the front only as much as needed to communicate the same perspective;
- contain no wooden box, rim, background, text, UI, or decorative ground shadow.

The generation target is a **source layer**, not a finished icon. Do not ask ImageGen to solve the final rim occlusion or final contact edge.

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
