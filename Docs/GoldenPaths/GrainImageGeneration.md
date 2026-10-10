# Grains Image Generation — Golden Path

This procedure is the Grains-specific entry point for generating **new grain/crop source candidates**. Shared visual style remains owned by Project `Docs/ArtStyle.md`; general source preservation, generation permission, review boundaries, export, and PNG validation remain owned by Project `Docs/GoldenPaths/TextureAssetPipeline.md`. Boxed-resource geometry/composition remains owned by `Docs/GoldenPaths/BoxedResourceIconPipeline.md`.

## Purpose

Use `Scripts/Art/grains_image_generator.py` instead of ad-hoc chat prompts for Grains crop/resource generation.

The script deliberately does **not** call the OpenAI API and does not read `OPENAI_API_KEY`. It owns only the deterministic parts around generation:

1. resolve and hash the real AMJ / subject / Medieval Overhaul references;
2. build the exact Grains prompt and a local reference bundle;
3. hand that prepared request to ChatGPT's built-in image generation;
4. after one generated PNG exists, run mechanical QA, relative 64 px complexity comparison, family post-processing, and a review sheet.

This avoids separate API billing. The Python script itself cannot invoke ChatGPT's built-in image-generation tool; generation is the explicit middle step between `prepare` and `review`.

It does **not** promote a candidate to `Art/Sources/` or `Textures/`, and it never publishes anything.

## Supported families

- `plant-mature` — mature cereal/crop plant source.
- `plant-immature` — immature cereal/crop plant source.
- `loose-grain` — loose/cleaned/in-hull grain pile source.
- `sheaf` — harvested sheaf/bundle source.
- `boxed-contents` — transparent contents-only source for the existing masu pipeline. The wooden masu is never generated.

Family reference paths and prompt additions are registered in `Docs/References/AMJ_Grains_ImageGenerator.json`. Do not add incident-specific prompt fragments to `AGENTS.md` when the real issue belongs in the shared style, family policy, or validator.

## Stage 1 — prepare the generation request

Run from a checkout of `Ancient-Medieval-Japan-Grains`. Supply at least one actual subject-identity reference with `--subject-reference`. For plant families, supply an actual Medieval Overhaul source through `--mo-root` or `--mo-zip`; the script resolves the registered MO wheat reference and fails closed if it cannot identify one.

Example:

```powershell
python Scripts/Art/grains_image_generator.py prepare `
  --family plant-mature `
  --subject "wheat" `
  --subject-reference "C:\AMJ-refs\wheat-reference.png" `
  --mo-root "C:\RimWorld\Mods\Medieval Overhaul" `
  --notes "mature wheat with a compact upright ear; preserve the real ear silhouette" `
  --output-dir "Work\Art\WheatMature"
```

The work directory receives:

- `prompt.txt` — exact generation instruction;
- `references/` — exact-byte copies of every resolved reference used for the request;
- `manifest.json` — reference paths, dimensions and SHA-256 values plus workflow state;
- `generation-request.json` — the minimal handoff contract for ChatGPT image generation.

`prepare` makes **no network request** and cannot incur OpenAI API usage charges.

`--allow-no-mo-reference` exists only for an explicitly incomplete draft. It does not satisfy final visual acceptance and must not be treated as the production-equivalent path.

The script refuses work/candidate outputs below `Textures/`, `Art/Sources/`, or `Docs/References/` so an unreviewed generation cannot silently overwrite a production texture, accepted master, or registered reference.

## Stage 2 — generate exactly one image in ChatGPT

Use ChatGPT's built-in image generation with:

- the complete text from `prompt.txt`;
- **every** image under the prepared `references/` directory;
- one image only;
- transparent background.

Do not substitute a remembered prompt or filename-only reference. Do not auto-loop retries.

This stage is intentionally outside the Python script because invoking an image model from a standalone script would require an API credential and separate API billing.

### Visibility limitation

ChatGPT's in-chat image generation displays the result as part of generation. Therefore this API-free route cannot truthfully claim that a generated candidate was mechanically screened **before** the user could see it. The shared Project Texture Asset Pipeline's user-visible-generation rule applies: treat such an image as an immediately visible, not-yet-vetted draft until Stage 3 completes.

Do not claim that `prepare` or ChatGPT generation alone produced an approved Grains asset.

## Stage 3 — review the generated PNG

Run:

```powershell
python Scripts/Art/grains_image_generator.py review `
  --work-dir "Work\Art\WheatMature" `
  --candidate "C:\path\to\generated-wheat.png"
```

The review command:

1. verifies that every prepared reference still matches its recorded SHA-256;
2. stages the generated PNG byte-for-byte as `candidate-source.png`;
3. runs `Scripts/Art/generated_asset_qa.py` with the registered baseline policy;
4. compares candidate 64 px color complexity and edge density against the accepted AMJ style references;
5. writes `qa-report.json`;
6. writes `review-sheet.png` containing the candidate and the actual references;
7. for `boxed-contents`, calls `Scripts/Art/prepare_boxed_resource_candidate.py` after the common automatic gates pass.

If automatic QA fails, the command exits nonzero and does **not** retry generation. Change the production approach, prompt, or reference contract before another user-visible generation attempt.

Mechanical QA does not establish subject identity or aesthetic acceptance. After it passes, compare the candidate semantically against the actual references and reject it if silhouette, crop identity, MO/AMJ flatness, outline hierarchy, palette restraint, forbidden content, or family composition is wrong.

## Acceptance and promotion

Only after explicit author visual acceptance:

1. preserve the exact accepted high-resolution source under the mirrored `Art/Sources/` path;
2. export the 256×256 production derivative through the shared Texture Asset Pipeline;
3. wire the Def/path if needed;
4. run the repository PNG integrity and affected source/runtime gates.

A prepared request, generated draft, review sheet, or automatic-QA PASS alone is not production-art acceptance or release readiness.
