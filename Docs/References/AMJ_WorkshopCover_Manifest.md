# AMJ Workshop Cover Raster Manifest

Persistent Library assets used by the deterministic Workshop-cover pipeline:

| Purpose | Library path | Dimensions | SHA-256 |
|---|---|---:|---|
| Approved visual reference | `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg` | 960×540 | `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658` |
| Fixed common base | `/AMJ/References/AMJ_WorkshopCover_CommonBase.png` | 960×540 | `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362` |
| Variable mask | `/AMJ/References/AMJ_WorkshopCover_VariableMask.png` | 960×540 | `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622` |

The approved visual-reference JPG is also preserved byte-for-byte at `Art/Sources/Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg` (recovered 2026-10-07 JST, SHA-256 as listed above). Prefer this verified repository copy when retrieving the approved reference. The common-base PNG and variable-mask PNG have not yet been archived under `Art/Sources`; retrieve those registered Library originals until their separate recovery is completed.

The registered images and their exact-byte archived copies are the pixel-level cross-chat source of truth. Do not regenerate these files from a prompt. If the author replaces the canonical format later, replace the Library assets and update this manifest and `Docs/WorkshopCoverStyle.md` together.
