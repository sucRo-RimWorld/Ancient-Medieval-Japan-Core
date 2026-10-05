# AMJ Core Agent Instructions

This repository is part of the **Ancient & Medieval Japan (AMJ)** project.

Before starting work in this repository:

1. Read this file.
2. Read the authoritative coordination log at `main:Docs/Coordination.md`.
3. Check for OPEN / IN PROGRESS items owned by the current workstream before starting new work.

## Cross-chat / cross-agent coordination

Do not use the user as a messenger between chats, agents, or workstreams.

When another AMJ workstream needs to be consulted, leave the request and relevant context in:

`main:Docs/Coordination.md`

When another repository is the actual owner of the requested work, record the request in that repository's authoritative `main:Docs/Coordination.md` rather than duplicating competing coordination records here.

## Source-of-truth rule

`Docs/Coordination.md` is only for handoff, status, blockers, and cross-workstream notes.

Durable decisions must also be reflected in the appropriate source of truth, such as:

- `Docs/Design.md`;
- C# code;
- XML/Defs/Patches;
- localization files;
- other repository-owned implementation/design documents.

Do not treat a coordination note as the final specification.

## Branch rule

The authoritative coordination log exists only on `main`.

Do not create branch-specific copies of `Docs/Coordination.md`.

If working on another branch, read and update `main:Docs/Coordination.md` separately when a coordination item changes.

## Consistency rule

When a design or implementation policy changes, do not edit only the immediately affected line.

Check the existing design, implementation, related systems, balance values, documentation, and tests for consistency before applying the change.

## Reporting GitHub changes

Only report that a GitHub file was updated when the change was actually committed to GitHub.

When reporting repository changes, include the actual commit SHA.

## PNG asset integrity gate

Every committed production PNG must pass `python Tests/validate_png_assets.py`. The validator checks every `Textures/**/*.png` for complete chunk boundaries, CRCs, a complete IDAT/zlib stream, valid scanlines, and a final IEND. It reports all broken PNGs found in one run rather than stopping after the first file.

The GitHub Actions `validate-png-assets` job is a prerequisite for Stage A validation. For binary writes made through automation or Git/GitHub APIs, treat the committed/checked-out bytes as authoritative: do not report the image write as successful until the repository-side PNG integrity gate passes. A valid PNG signature, dimensions, or successful viewer open is not sufficient.

## 自動テスト優先方針（AMJ共通）

AMJおよび関連Modでは、RimTest Redux・Pickleを積極的に用いた自動テストを優先し、人間による手動テストを最小限にする。

- ロジック・計算・設定検証などはRimTest Redux、ロード後のDef・実際のゲーム内挙動・統合回帰などはPickleを中心に、適した自動テストで確認する。
- 新機能・不具合修正では、再現可能な確認を可能な限り自動化し、リリース前の回帰確認も自動テストへ寄せる。既存のビルド・XML・静的検証は併用する。
- 手動テストは、画像の見た目、UIの読みやすさ、操作感・遊び心地など、人間の目視・操作が必要な項目に限定する。自動で確認済みの数値や挙動を毎回手動で再確認させない。
- 自動化が未整備の項目は、未検証範囲と自動化する対象を明示する。静的検証の成功を実行時テストの成功として扱わない。
- RimWorldを起動する自動テストでは、既存の実行時ERROR検出方針を必ず適用する。シナリオが全件成功しても対象Mod由来のERRORがあれば全体を失敗とする。

## 非対話ランタイムテスト方針（AMJ共通）

人間の目視判断を必要としない自動テストでは、RimWorldの可視ウィンドウをユーザーのデスクトップへ出さないことを標準とする。詳細な共通正本は Ancient-Medieval-Japan-Core `Docs/DevelopmentGoldenPathGuidelines.md` の **Non-interactive runtime-test rule**。

- Pickle / RimTest Redux / Quickstarts / 統合回帰 / runtime ERROR gate / map・気候・土壌サンプリング等は、原則として非対話・非表示で実行する。
- 描画・Texture Atlas・`Graphic.Draw`・BadTex等を検証する場合は、描画そのものを無効化しない。仮想／オフスクリーン／非表示の表示先など、プラットフォームに適した隔離実行で実描画経路を維持する。
- 描画経路がテスト対象なら `-nographics` 等で迂回しない。
- 可視実行は、最終的なテクスチャ見た目、通常ズーム視認性、UI、操作感、遊び心地など、人間の判断が必要な確認だけに限定する。
- 通常の自動ランナーと、visual / interactive / debug用途の可視ランナーを分離する。
- 既存ランナーが可視ウィンドウを出す場合は移行対象とし、次回の重要変更時または定期回帰ゲート化前に非対話実行経路を追加する。挙動忠実度を保てない場合のみ、理由を文書化した例外を認める。

## Automated runtime-error gate

For any automated test that launches RimWorld, a passing scenario/test count is not sufficient by itself.

The test harness must capture an isolated runtime log and fail the overall test run if the repository-owned mod emits any ERROR-level entry. Do this even when all Pickle/RimTest scenarios otherwise pass. Warnings remain non-fatal unless a repository-specific test explicitly promotes them.

Any new RimWorld runtime-test harness added to this repository must include this mod-origin ERROR gate from the start. Static-only validation does not fabricate a runtime-log result; add the gate when runtime automation is introduced.

## Public mod descriptions

Use the CCTO-based shared [mod description guidelines](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Core/blob/main/Docs/ModDescriptionGuidelines.md) when writing or updating public descriptions. Include save compatibility in every mod description, stating addition/removal conditions accurately for the mod's implementation. Keep README, Workshop English/Japanese BBCode, and About.xml consistent; refine the shared baseline as presentation improves.


## Historical description audit (AMJ common)

Use `Docs/HistoricalDescriptionGuidelines.md` whenever AMJ adopts, patches, retextures, selects, or localizes Vanilla / Medieval Overhaul items, plants, animals, or comparable content.

Audit inherited Vanilla/MO prose for historical fit with ancient/medieval Japan and rewrite unsuitable text. AMJ-authored descriptions should include supported historical facts and, where supportable, a meaningful difference from modern Japan, modern use, or modern distribution. Do not invent a medieval counterpart for historically unsuitable content; record it for a separate keep/replace/remove design decision.

Historical description text is Japanese-first: research and draft Japanese, obtain author approval, then translate only the approved Japanese text into English. Keep source/rationale notes in durable design/localization documentation rather than only in Coordination.

## CCTO framework and crop-data ownership

AMJC owns its custom crops' temperature values, design/balance tables (including archived candidate ranges), Def mappings, optional CCTO compatibility XML, and validation. Maintain these here, not in CCTO. Use `Docs/Balance/Crops/ColdTolerance.md` together with the cultivation design and implemented XML as the local source of truth. CCTO remains an optional framework; its own Vanilla/MO support data remains owned by CCTO.

## Golden Path closeout rule

Follow the AMJ shared Golden Path policy in Ancient-Medieval-Japan-Core `Docs/DevelopmentGoldenPathGuidelines.md`.

For production texture work, also follow `Docs/GoldenPaths/TextureAssetPipeline.md`. Boxed-resource icons must additionally follow `Docs/GoldenPaths/BoxedResourceIconPipeline.md`. A shared container template is not production-ready merely because its protected pixels are stable: the registered filled visual reference, frame occupancy, content-fill profile, and representative final composite must also pass. If the family manifest is marked blocked/inactive, do not generate or compose a production derivative from it.

Before presenting any art candidate as ready for approval or registration, perform a self-QC pass and automatically fix objective defects that do not change the approved design: jagged/rough edges caused by resizing, halos, clipping, seams, stray pixels, wrong canvas occupancy, accidental leftovers from another layer, or visibly inconsistent common-part geometry. Do not ask the author to accept a defect you already know how to fix. Ask only when the correction would change the approved design or requires a genuine aesthetic tradeoff.

For boxed-resource visual comparisons, never substitute a locally remembered/generated "reference" image. Use `Scripts/Art/boxed_resource_review.py`, which loads the manifest's `representative_final`, verifies its SHA-256, and builds the 256px/~64px comparison from that exact registered file. If the hash or file is unavailable, stop instead of approximating.

Before any new boxed-resource material variant is produced, pass an identity round-trip gate: derive the exact variable-pixel mask from the registered empty master versus the registered filled exemplar, extract only those pixels, recompose them onto the master, and require **zero differing pixels** versus the exemplar. Do not proceed to recoloring/material changes until this structural identity test passes. A broad editable mask or approximate geometric interior mask is not sufficient.

If an art-processing path is found to be contaminated (wrong reference, wrong shared part, broken mask/composite path, unintended whole-image regeneration, or any other condition that makes downstream derivatives untrustworthy), invalidate and discard all derivatives from that path immediately. Do not retain them "for comparison" where they can be selected later by mistake. Keep only authoritative registered masters/references and explicitly clean diagnostic artifacts that cannot be mistaken for production sources. Persistent Library copies and local working copies must both be removed; Coordination must record the invalidation.

After a non-trivial task succeeds, especially after debugging or failed attempts, do not move on with only the working implementation. Record the successful reusable procedure in the owning repository, automate deterministic/repetitive steps, and add regression guards for failure modes discovered during the work. For recurring work, completion includes the reusable documented/automated path, not only the one successful result.

`Docs/Coordination.md` remains status/handoff only; the procedure itself must live in durable repository documentation/scripts.

## AMJ image wording / generation permission

In AMJ art work, Japanese wording is operationally significant:

- 「作成」「制作」「続けて」 means **execute the established production pipeline** using authoritative masters, local editing, deterministic compositing, and validation. It does **not** grant permission to invoke ImageGen.
- 「生成」 explicitly permits image generation when the active Golden Path allows it.
- For fixed-template families, even an explicit 「生成」 applies only to the variable material. Never regenerate the registered shared part or whole final image.
- If deterministic/local creation cannot proceed without new generated source material and the author did not ask for 「生成」, stop and report the specific missing source/blocked step instead of silently invoking ImageGen.

## Pixel-exact shared image components

Follow `Docs/GoldenPaths/FixedImageTemplates.md` for every reused component. Registered masters and binary editable masks are mandatory before producing derivatives. Generate variable material only, composite deterministically, and require zero decoded RGBA differences in protected pixels. Reference-image editing and visual similarity are insufficient. Existing style references do not imply identical silhouettes for different species.

### Workshop cover fixed-template rule

For AMJ Workshop covers, also follow `Docs/GoldenPaths/WorkshopCoverPipeline.md` and `Docs/WorkshopCoverStyle.md`.

Before any cover generation:
- retrieve and visually inspect Library `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`;
- retrieve the canonical `AMJ_WorkshopCover_CommonBase.png` and `AMJ_WorkshopCover_VariableMask.png` from the same Library folder;
- generate only addon-specific right-side artwork, not a complete cover;
- compose with `Scripts/build_workshop_cover.py` and validate with `Scripts/validate_workshop_cover.py`;
- if the required Library rasters are unavailable, do not reconstruct them from memory, prompts, or SVG; treat cover production as blocked.

## Future shared-image families

For every new image family with reused parts, automatically apply `Docs/GoldenPaths/FixedImageTemplates.md` without waiting for a separate author request. Before the next derivative, register the approved master/mask/hashed manifest, extend the family-owned specification and generation entry, and implement/run zero protected RGBA pixel-difference validation. Include recurring registered derivatives in automated integration/CI checks. This registration/documentation/validation is part of task completion, not an optional follow-up.
