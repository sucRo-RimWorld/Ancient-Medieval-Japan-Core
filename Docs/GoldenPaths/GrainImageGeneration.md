# Grains Image Generation — Golden Path

This procedure is the Grains-specific entry point for generating **new grain/crop source candidates**. Shared visual style remains owned by Project `Docs/ArtStyle.md`; general source preservation, generation permission, automatic-vs-human review boundaries, export, and PNG validation remain owned by Project `Docs/GoldenPaths/TextureAssetPipeline.md`. Boxed-resource geometry/composition remains owned by `Docs/GoldenPaths/BoxedResourceIconPipeline.md`.

## Purpose

Use `Scripts/Art/grains_image_generator.py` instead of ad-hoc chat prompts for Grains crop/resource generation. The script makes the required reference set, prompt contract, one-image generation, candidate QA, and review material reproducible.

It does **not** replace final semantic/visual judgment. It does not promote a candidate to `Art/Sources/` or `Textures/`, and it never publishes anything.

## Supported families

- `plant-mature` — mature cereal/crop plant source.
- `plant-immature` — immature cereal/crop plant source.
- `loose-grain` — loose/cleaned/in-hull grain pile source.
- `sheaf` — harvested sheaf/bundle source.
- `boxed-contents` — transparent contents-only source for the existing masu pipeline. The wooden masu is never generated.

Family reference paths and prompt additions are registered in `Docs/References/AMJ_Grains_ImageGenerator.json`. Do not add incident-specific prompt fragments to `AGENTS.md` or this document when the real issue belongs in the shared style, family policy, or validator.

## Preconditions

Before a real generation call:

1. run from a checkout of `Ancient-Medieval-Japan-Grains`;
2. supply at least one actual subject-identity reference with `--subject-reference`;
3. for plant families, supply an actual Medieval Overhaul source through `--mo-root` or `--mo-zip`; the script resolves the registered MO wheat reference and fails closed if it cannot identify one;
4. set `OPENAI_API_KEY` for API-backed generation;
5. write only to a development directory such as `Work/Art/...`.

`--allow-no-mo-reference` exists only for an explicitly incomplete draft. It does not satisfy final visual acceptance and must not be treated as an equivalent production path.

The script refuses candidate outputs below `Textures/`, `Art/Sources/`, or `Docs/References/` so an unreviewed generation cannot silently overwrite a production texture, accepted master, or registered reference.

## Dry-run first

Resolve all references and inspect the exact prompt/manifest without making an API call:

```powershell
python Scripts/Art/grains_image_generator.py `
  --family plant-mature `
  --subject "wheat" `
  --subject-reference "C:\AMJ-refs\wheat-reference.png" `
  --mo-root "C:\RimWorld\Mods\Medieval Overhaul" `
  --notes "mature wheat with a compact upright ear; preserve the real ear silhouette" `
  --output-dir "Work\Art\WheatMature" `
  --dry-run
```

The output directory receives `prompt.txt` and `manifest.json`, including the resolved reference paths, dimensions, and SHA-256 values. A dry-run proves reference/prompt resolution only; it is not image or art validation.

## Generate one candidate

Remove `--dry-run` from the same command. The default model is the pinned `gpt-image-2.5-sunburst-2026-09-08` snapshot; `--model` is an explicit override. Generation is always `n=1`, transparent PNG, and has **no automatic retry loop**.

A successful standard-family run produces:

- `candidate-source.png` — the raw high-resolution generated source candidate;
- `prompt.txt` — exact prompt sent;
- `manifest.json` — model, source-reference identities/hashes, candidate hash/dimensions, and API usage returned by the endpoint;
- `qa-report.json` — baseline generated-asset QA plus relative 64px color/edge-density comparison against the accepted style references;
- `review-sheet.png` — candidate beside the actual references for the remaining semantic/visual review.

If mechanical or relative-complexity QA fails, the command exits nonzero after one generation and does not retry. The rejected file stays in the development directory for diagnosis only. Change the production approach or prompt/reference contract before another run; do not blind-loop until something passes.

## Boxed contents

Use `boxed-contents` only for the **contents layer**. After the common automatic gates pass, the script calls `Scripts/Art/prepare_boxed_resource_candidate.py` and writes its projected/boxed preparation under `boxed-prepared/`.

The active boxed-resource Golden Path still owns perspective normalization, manual placement/contact/occlusion, and final author acceptance. This script never asks ImageGen to redraw the wooden masu.

## Acceptance and promotion

After automatic QA passes, compare the candidate against the actual references at full size and roughly 64px. Reject it if subject identity, silhouette, MO/AMJ flatness, outline hierarchy, palette restraint, or family composition is wrong even when the numeric report is green.

Only after explicit author visual acceptance:

1. preserve the exact accepted high-resolution source under the mirrored `Art/Sources/` path;
2. export the 256×256 production derivative through the shared Texture Asset Pipeline;
3. wire the Def/path if needed;
4. run the repository PNG integrity and affected source/runtime gates.

A generated source, review sheet, or QA PASS alone is not production-art acceptance or release readiness.
