# AMJ Core development tools

AMJ Core uses two layers of automated Stage A validation.


## 自動テスト優先方針（AMJ共通）

AMJおよび関連Modでは、RimTest Redux・Pickleを積極的に用いた自動テストを優先し、人間による手動テストを最小限にする。

- ロジック・計算・設定検証などはRimTest Redux、ロード後のDef・実際のゲーム内挙動・統合回帰などはPickleを中心に、適した自動テストで確認する。
- 新機能・不具合修正では、再現可能な確認を可能な限り自動化し、リリース前の回帰確認も自動テストへ寄せる。既存のビルド・XML・静的検証は併用する。
- 手動テストは、画像の見た目、UIの読みやすさ、操作感・遊び心地など、人間の目視・操作が必要な項目に限定する。自動で確認済みの数値や挙動を毎回手動で再確認させない。
- 自動化が未整備の項目は、未検証範囲と自動化する対象を明示する。静的検証の成功を実行時テストの成功として扱わない。
- RimWorldを起動する自動テストでは、既存の実行時ERROR検出方針を必ず適用する。シナリオが全件成功しても対象Mod由来のERRORがあれば全体を失敗とする。

## 対話型開発補助ツール（AMJ共通）

人間の目視・操作が必要な確認を短時間で準備するため、次のツールを開発専用として利用してよい。これらは自動テストの代替ではなく、出荷Modの依存関係にも含めない。

- **DevKit — Better Dev Mode Menu** (Workshop `3814373104`): Def / defName 検索、Thing・植物・建築物・Pawn等の配置、Debug Action検索、Favorites / Recent等を使い、目視確認・デバッグ用の盤面準備を高速化する。
- **Rim Control** (Workshop `3774299554`): ゲーム中の数値・visual・placement等を一時変更し、バランス値や表示設定の候補を素早く比較するためのプロトタイピング用途に使う。

運用ルール:

- DevKitでスポーン・配置できたこと自体を、実装またはテスト成功の証拠として扱わない。
- Rim Controlで変更した値は試作値にすぎない。採用する場合は、必ず所有リポジトリのXML / C# / Def / 正式設計書へ反映して正本化する。
- 正本へ反映した後、Rim Controlの上書きを無効化し、必要な静的検証・RimTest Redux・Pickle・通常のruntime gateで再検証する。
- 自動テスト、リリースゲート、正式な通常プロファイル確認では DevKit / Rim Control を無効化する。例外は、そのツール自身との互換性を明示的に調べるテストだけとする。
- 可視実行を行う場合も、用途は最終テクスチャ、通常ズーム視認性、UI、操作感、遊び心地など、人間判断が必要な項目に限定する。

## GitHub validation

`.github/workflows/stage-a-validation.yml` runs `Tests/validate_stage_a.py` on pushes to `main` and pull requests.

This checks repository-owned XML values and wiring, including the six Stage A field crops, shared grain storage/processing, optional CCTO data, PNG integrity, and New Village start conditions. `Tests/validate_new_village.py` is called by the same CI entry point; no separate workflow is required.

PowerShell scripts containing non-ASCII characters must be saved as UTF-8 **with BOM**, because the local runner uses Windows PowerShell 5.1, which otherwise reads script source using the Windows ANSI code page. ASCII-only scripts may omit the BOM. The Python validator checks this rule for every `.ps1`, and a Windows CI job parses all scripts with Windows PowerShell 5.1 before runtime testing on the development PC.

## Local full gate

From the repository root:

`run-tests.bat "D:\SteamLibrary\steamapps\common\RimWorld"`

The gate:

1. verifies the installed Medieval Overhaul 1.6 source exists;
2. runs `Scripts/Validate-StageA.ps1` against repository XML and the installed MO source;
3. generates four development-only test mods under `RimWorld\Mods`;
4. compiles the Pickle and Quickstarts test assemblies;
5. creates an isolated RimWorld save-data profile without changing the normal mod list;
6. launches RimWorld automatically and redirects runtime output to an isolated `TestResults\Pickle\Player.log`;
7. runs the seven `stage-a.feature` scenarios, including the production New Village start through `@quickstart:AmjNewVillageQuickstart`;
8. requires a fresh clean 7/7 Pickle summary;
9. scans the isolated runtime log and fails the full gate if AMJ Core / its staged E2E target emitted any ERROR-level entry;
10. lets Pickle exit RimWorld automatically.

Required local Workshop helpers are Pickle (3791648678) and Quickstarts (3793646067), plus their normal Harmony/RimLogging requirements.

A clean Pickle scenario count is not sufficient if the target mod logged an ERROR. Runtime ERROR inspection is part of the authoritative local gate.

Generated test mods:

- `AncientMedievalJapanCore.E2ETarget`
- `AncientMedievalJapanCore.E2E`
- `AncientMedievalJapanCore.MOFixture`
- `AncientMedievalJapanCore.CCTOFixture`

Remove them with:

`clean-e2e.bat "D:\SteamLibrary\steamapps\common\RimWorld"`

## Automated coverage

The current local integration suite checks loaded RimWorld Defs for:

- all Stage A crop growth/fertility/temperature, sowing requirements and harvest targets, including the MO wheat patch;
- loaded AMJC-owned optional CCTO crop data;
- millet, buckwheat, barley and wheat storage tiers;
- no accidental `DankPyon_Cereal` registration;
- simple processing spot speed 0.5;
- grain processing table speed 1.0 and Basic Agriculture requirement;
- the Stage A threshing/hulling bills on both stations;
- single and x10 threshing/hulling inputs, products and work amounts;
- `13 raw millet -> 13 millet in hull + 13 Straw -> 13 edible millet`;
- final edible grains accepted by the Vanilla simple-meal ingredient filter;
- loaded New Village Scenario/Faction/PawnKind: five out of eight, Standing arrival, three explicit starting research projects, empty faction research/techprint tags, initial items/stuff and early processing access;
- the production New Village Scenario actually generating a home map with five villagers, the correct player faction, only the three intended projects finished, required supplies present, iron knives/wooden club, and no initial field-crop research barrier.

Manual checks should be reserved for appearance, Japanese UI readability, building footprint/interaction-cell usability, and whether processing speed feels appropriate during real play.


## New Village source and runtime validation

The normal local gate also calls `Scripts/Validate-NewVillage.ps1` with the installed game and MO roots. It checks source Def references, native Scenario part classes, inherited base definitions, initial item quantities/materials, and the design table. Direct callers that omit `RimWorldRoot` receive an explicit warning that the installed Core reference audit was skipped.

The runtime suite uses lightweight MO XML and a CCTO XML-API fixture, with DLCs and AMJ Backgrounds absent. This covers the production AMJC Scenario against RimWorld's real start pipeline, not all MO Harmony/gameplay behavior. No custom pawn/item/research override is applied by `AmjNewVillageQuickstart`. Loaded supply definitions are checked exactly; the live map must contain at least the promised amounts because independent map generation can add other items.

The New Village C# build and seven-scenario runtime gate remain pending on the development PC. Python static validation and source XML inspection are not a runtime PASS. Keep AMJ-015 IN PROGRESS until the clean 7/7 summary and isolated ERROR scan are confirmed. Manual work remains limited to start feel and UI/appearance.

## Isolated rendered desktop launcher

See [IntegratedRuntimeTesting.md](IntegratedRuntimeTesting.md) and
`Scripts/IntegratedRuntimeDesktop/Run-AMJ-IsolatedDesktop.ps1`. Historical
local verification passed 7/7 plus zero ERRORs before the current eight-scenario
extension. Two texture/live-map test entry points now dispatch through
PickleDriver.Post and enforce Unity main-thread execution. This publication
preserves the newer suite; it does not claim a fresh eight-scenario runtime PASS.
