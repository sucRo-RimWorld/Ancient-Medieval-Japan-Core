# AMJ Core Agent Instructions

This repository is part of the **Ancient & Medieval Japan (AMJ)** project.

Before starting work in this repository:

1. Read this file.
2. Read the authoritative coordination log at `main:Docs/Coordination.md`.
3. Check for OPEN / IN PROGRESS items owned by the current workstream before starting new work.

## Context reconstruction / source hierarchy

For every new chat or agent session working on AMJ or a related mod, rebuild context from repository sources instead of treating accumulated chat history as the primary source of truth:

1. Read this repository's `AGENTS.md` first.
2. Read the authoritative `main:Docs/Coordination.md`.
3. Read the relevant authoritative design, code, XML/Defs/Patches, localization, Golden Path, or other repository-owned source-of-truth files for the task.
4. Use prior chat history or memory only as supplementary context. If it conflicts with repository sources, the repository sources win.

Store information according to this hierarchy:

- Confirmed specifications, design decisions, accepted values, and implementation facts -> the appropriate formal repository source of truth.
- Cross-chat / cross-agent / cross-workstream handoff, current status, blockers, and requests -> `main:Docs/Coordination.md`.
- Permanent operating rules that should govern future work -> `AGENTS.md`.
- Do not leave a durable decision only in chat history or only in `Docs/Coordination.md`.

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

## Mod naming rule (AMJ common)

AMJ Core, Environment, CCTO and future related Mods must not use ASCII `:` or full-width `：` in Mod names. Use ` - ` when a separator is needed. Apply this to `About/About.xml` `<name>` and the corresponding Workshop title / formal README name; check it when creating, renaming or preparing a Mod for publication. YADA uses the display name for an upload staging directory, and an ASCII colon causes that step to fail on Windows. Display-name corrections must preserve `packageId` and existing Workshop IDs.

The shared source of truth is [Mod description guidelines — Mod名のコロン禁止](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Core/blob/main/Docs/ModDescriptionGuidelines.md). Colons in description prose, URLs and code syntax are outside this naming rule.

## Public mod descriptions

Public-description preparation and updates must also include the Japanese 2game summary in `Docs/2GameDescription-ja.txt` and its presentation policy in `Docs/2GamePresentation.md`. Follow the shared guideline's **2game向け説明（AMJ共通）** section and CCTO's six-section, plain-style template. Check README, Workshop English/Japanese, 2game Japanese and About.xml together; link named related mods and this mod's own GitHub repository. Record repository preparation separately from live-site publication.

Use the CCTO-based shared [mod description guidelines](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Core/blob/main/Docs/ModDescriptionGuidelines.md) when writing or updating public descriptions. Include save compatibility in every mod description, stating addition/removal conditions accurately for the mod's implementation. Keep README, Workshop English/Japanese BBCode, and About.xml consistent; refine the shared baseline as presentation improves.


## Retexture implementation rule (AMJ common)

When AMJ retextures Vanilla, Medieval Overhaul, or another prerequisite Mod asset, follow `Docs/RetextureImplementationGuidelines.md` in addition to the owning repository's art pipeline.

- AMJ-owned prerequisite graphics use AMJ-owned unique texPaths with explicit Def/Patch ownership by default; do not rely only on same-name texture shadowing/load order.
- Treat one retexture target as the complete loaded graphic-state family, not one mature/base PNG.
- Keep pure retexture patches visual-only; gameplay changes require their own owning design.
- Optional parent-Mod graphics must be guarded and must not copy/edit third-party distributed art in place.
- Audit known explicit-path competitors and validate the final loaded AMJ path where AMJ owns the target.

## Historical description audit (AMJ common)

Use `Docs/HistoricalDescriptionGuidelines.md` whenever AMJ adopts, patches, retextures, selects, or localizes Vanilla / Medieval Overhaul items, plants, animals, or comparable content.

Audit inherited Vanilla/MO prose for historical fit with ancient/medieval Japan and rewrite unsuitable text. AMJ-authored descriptions should include supported historical facts and, where supportable, a meaningful difference from modern Japan, modern use, or modern distribution. Do not invent a medieval counterpart for historically unsuitable content; record it for a separate keep/replace/remove design decision.

Historical description text is Japanese-first: research and draft Japanese, obtain author approval, then translate only the approved Japanese text into English. For Japanese descriptions, follow `Docs/HistoricalDescriptionGuidelines.md` name-form rules: begin with an established kanji form when one exists, and include recognized aliases / alternate names or common alternate written forms at the opening. Do not invent kanji or weakly sourced names. Keep source/rationale notes in durable design/localization documentation rather than only in Coordination.

## CCTO framework and crop-data ownership

AMJC owns its custom crops' temperature values, design/balance tables (including archived candidate ranges), Def mappings, optional CCTO compatibility XML, and validation. Maintain these here, not in CCTO. Use `Docs/Balance/Crops/ColdTolerance.md` together with the cultivation design and implemented XML as the local source of truth. CCTO remains an optional framework; its own Vanilla/MO support data remains owned by CCTO.

## Workshop distribution rule (AMJ common)

AMJ Core, Environment, CCTO and future related Mods must exclude **all files unnecessary for a Workshop subscriber** through the repository-root `.rimignore`. This includes Art masters/templates, design and development documentation (including README), source, tests/fixtures/reports, scripts/build tools, VCS/editor metadata, local overrides and debug/backup/archive files. Preserve runtime assets, About metadata, loadFolders.xml where used, and legally required licenses/attribution.

- `.rimignore` is the authoritative exclusion list. YADA uses inherited basename/wildcard rules, not Git-ignore path or negation syntax; exclude `_LocalTest.xml`, not `Patches/_LocalTest.xml`.
- Adding a file/folder includes deciding whether subscribers need it and updating exclusions when they do not. Preserve development/source material in Git; exclusion is not deletion.
- Every alternative publisher/archive/staging builder must produce the same subscriber-only payload. Keep adapters synchronized with `.rimignore`; do not maintain independent policy exceptions.
- Run `python Tests/validate_workshop_payload.py` before publication. Validate the final staging/installed package too; runtime-required DLLs and assets must actually be present. Repository filtering PASS alone is not build/runtime/Steam publication PASS.
- Shared procedure and payload contract: [Core Docs/WorkshopPackaging.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Core/blob/main/Docs/WorkshopPackaging.md).

## Art / image work

Keep this file as a routing layer; do not duplicate asset-family procedures here.

For AMJ art, resolve rules in this order:

1. `Docs/ArtStyle.md` — project-wide visual language and precedence.
2. The owning asset-class specification — adds subject-specific visual rules only.
3. `Docs/GoldenPaths/TextureAssetPipeline.md` — source preservation, generation permission, export, and validation.
4. `Docs/GoldenPaths/FixedImageTemplates.md` — only when visible parts are intentionally reused pixel-exactly.

Current asset-class specifications:
- boxed resources / masu: `Docs/GoldenPaths/BoxedResourceIconPipeline.md`;
- Workshop covers: `Docs/WorkshopCoverStyle.md` + `Docs/GoldenPaths/WorkshopCoverPipeline.md`;
- prerequisite-Mod retextures: `Docs/RetextureImplementationGuidelines.md` plus the owning repository's art specification.

A family-specific document may narrow the shared style for its asset class, but it must not silently replace the AMJ-wide visual language. Any real exception belongs in the owning style specification, not in chat history or AGENTS.

For generation intent and ImageGen use, follow `Docs/GoldenPaths/TextureAssetPipeline.md`. Interpret the user's requested image action semantically; do not use an exact-keyword gate, and never regenerate accepted fixed/shared parts merely because new image work was requested.

## Golden Path closeout rule

Follow `Docs/DevelopmentGoldenPathGuidelines.md`. Reusable procedures belong in the owning Golden Path or source-of-truth document; `Docs/Coordination.md` remains status/handoff only.

