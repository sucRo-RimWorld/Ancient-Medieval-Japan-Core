# Grains dependency-migration test profiles

**Latest seasonal-test evidence (2026-10-08 JST):** `automated-gates(8).log` confirms the post-sky-fix **vanilla 6/6, runtime ERROR 0**. The other three profiles on that corrected test source remain OPEN. Earlier `automated-gates(4).log` established four-profile fresh smoke **24/24, ERROR 0**, before seasonal-test changes; it does not certify the latest matrix. Legacy saved-game compatibility, natural seasonal weather, visual approval and release-readiness remain separate gates. Production MO dependency remains unchanged; see the dated evidence sections below.

This covers migration steps 1 through 3 of `Docs/Design.md`: separate the harness before changing
production dependency metadata or runtime ownership. The production `About.xml`
still requires MO. A successful tooling test is not a successful Grains release.

## Windows entry point

From the development checkout, with Steam running and the test helpers installed:

```bat
run-grains-tests.bat "D:\SteamLibrary\steamapps\common\RimWorld"
run-grains-tests.bat "D:\SteamLibrary\steamapps\common\RimWorld" vanilla
```

The default runs all four profiles sequentially and records every result even if
an earlier profile fails. Optional second argument: `vanilla`, `vanilla-ccto`,
`mo`, `mo-ccto`, or `all`. The normal entry point uses the existing Windows
private-desktop launcher without switching the input desktop. Unity rendering
stays enabled; do not replace it with `-nographics`.

| Profile | MO provider | CCTO provider | API fixtures |
|---|---|---|---|
| vanilla | absent | absent | absent |
| vanilla-ccto | absent | installed CCTO | absent |
| mo | installed MO | absent | absent |
| mo-ccto | installed MO | installed CCTO | absent |

All profiles use installed Harmony, RimLogging, Pickle and Quickstarts, a staged
AMJ target, and the separate AMJ test mod. Only declared hard dependencies are
added recursively; active loadAfter/forceLoadAfter constraints are then ordered.
For example, current MO additionally requires VEF and Processor Framework.
Installed optional mods and DLC are not enabled just because they are installed
or enabled in the player's normal configuration. Missing dependencies, ambiguous
duplicate package installations and dependency/load-order cycles fail setup.

## Staging boundary

`build-e2e.bat <RimWorldRoot> <profile>` uses
`Scripts/Stage-GrainsTestProfile.ps1` for the four real-provider profiles.
The disposable `AncientMedievalJapanCore.E2ETarget` has the existing test packageId,
no hard MO dependency, and profile-specific provider load order. Its Defs,
Patches, Textures, Languages, Compatibility and BaseWithoutMO are copied unchanged. Assemblies, versioned 1.6
content and loadFolders are copied if present. Production Core is not activated
alongside the test copy. The test-mod assembly build is shared with the legacy
runner; the real profiles neither build nor load the MO/CCTO API fixtures.

Real profiles do not apply `E2E_Graphics.xml`, remove MO references, substitute
recipes, or manufacture missing provider Defs. Base MO Def references were isolated in step 2. Vanilla
now has initial wheat/flour/milling/food XML, with pending runtime/art/prose verification.
Those gaps must remain visible until runtime migration resolves them.

`build-e2e.bat <RimWorldRoot>` and the existing `run-e2e.bat` / `run-tests.bat`
rewrite only the staged loader MO condition to the fixture packageId and
retain the historical MO+CCTO lightweight-fixture suite and eight assertions.
That suite remains useful for narrow XML contracts; its PASS does not prove
real MO/CCTO integration or Vanilla independence. Do not run the legacy and
Grains runners concurrently: both rebuild the same staged test-mod directories.
Generated test mods must remain disabled during ordinary play. `clean-e2e.bat`
removes the generated target, test mod and both fixtures when no test is running.

## Evidence and failure gates

Each profile gets fresh isolated SaveData and Pickle output under
`TestResults/Grains/<profile>/`. `matrix.json` records launch state, exit code,
setup diagnostics and report paths. The report includes:

- `Player.log` and Pickle `summary.json`;
- the profile manifest and resolved installed package/root list;
- source HEAD, existing source fingerprints, and SHA-256 hashes of the staged
  runtime target, compiled test assemblies/features and non-Vanilla providers.

The profile suite requires exactly its six grain-only named scenarios, 6/6 passes and
zero skips. Assertions check actual provider presence, fixture/production-Core
absence, resolved primary crop/recipe/simple-meal contracts, loaded wheat/flour/milling/food contracts, and presence/absence of AMJ cold-tolerance extensions. Runtime log checking
fails on **any ERROR**, including provider errors. Both summary and log gates
run after a launched game even if the process or scenarios already failed.
Missing fresh output is a failure. The Grains game-process watchdog is nine minutes per profile;
Pickle has a separate **seven-minute run-wide limit**, exceeding the production scenario's
270-second allowance. The private-desktop matrix watchdog remains forty minutes and
terminates its own tree. The legacy fixture suite retains its four-minute Pickle default.

These are **migration smoke tests**, not the completed release matrix. Subsequent
implementation must prove actual harvest/Bill cooking behavior, six-grain environmental-choice
regression, and save compatibility cases. None is inferred from loaded-contract smoke
scenarios or from the old fixture suite.

## Tooling regression

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File Tests/test_grains_profiles.ps1
```

This launches no game. It stages all four profiles in a temporary directory,
verifies exact runtime byte preservation and production/player-config immutability,
tests provider isolation and ordering, rejects wrong-suite summaries, and checks
missing/forbidden dependencies and cycles. GitHub's Windows PowerShell 5.1 job
also parses the scripts and runs this regression. It does not compile the game
test assemblies or claim runtime success.

## Conditional runtime folders and static contracts

Production `loadFolders.xml` loads `/`, activates
`Compatibility/MedievalOverhaul` only for `DankPyon.Medieval.Overhaul`, and activates
`BaseWithoutMO` only when that provider is absent.
Real-profile staging preserves the loader and conditional files byte for byte.
Only the legacy fixture stage changes its disposable loader conditions via
`Prepare-FixtureLoadFolders.ps1`; production XML never names a fixture.
Workshop archives must include the loader and all conditional runtime files.

`Tests/validate_grains_base.py` verifies zero MO identifiers in Base Defs/localization
and compares all 38 pre-split explicit AMJC contracts to their MO projection.
The golden fixture records source commit and hashes. `amj_profile_xml.py` and
`AmjProfileXml.ps1` project only AMJ-owned Defs and the Base-difference Add/Replace
patches. They do not simulate external MO wheat patches, XML inheritance, loaded
Def references, localization resolution or texture loading. Existing wheat-patch
checks remain separate; actual game tests are required for those boundaries.

## Approved Scenario ownership boundary (2026-10-07)

New Village, its starting player Faction/PawnKind, research and supplies will move
to an independent starting-scenario mod. That mod must work with Vanilla alone;
Grains and MO integrations are optional and owned by the scenario mod. Neither
mod makes the other a hard dependency. The owner is Ancient-Medieval-Japan-Scenarios / sucro.ancientmedievaljapan.scenarios. Production legacy copies are guarded; actual save-migration verification remains pending.

Current Grains real-provider suites have six grain-only scenarios. Their dedicated Scenario-presence requirement and two village checks are removed. Canonical start checks/Quickstart live in Scenarios (four profiles, three scenarios each); Grains retains LegacyVillageSteps and AmjLegacyVillageQuickstart in the old eight-case fixture for its compatibility copy. Preserve all 38 historical contracts, including legacy start contracts, rather than dropping the golden snapshot.

The scenario owner must test Vanilla alone, Grains, MO and Grains+MO starts, plus
old Core New Village saves and exactly one provider of every migrated Def when
old/new packages coexist. Grains standalone must pass without the scenario mod.
Apply the existing non-interactive rendering and runtime ERROR gates. None of
these extraction/migration tests is claimed as already passing.

## Step 3 chain validation and outstanding release gates

`python Tests/validate_stage_a.py` includes Base/MO chain validation.
`python Tests/test_grains_chain.py` rejects nutrition multiplication, extra milling
products, bread-like storage, cooking research gates, broken MO flour routing and
duplicate fallback defs. Shared new AMJ contracts are allowed explicitly; the
original 38-contract hashes are still compared unchanged.

The sixth Pickle scenario checks loaded fallback/provider isolation, wheat
harvest/thresh definitions, flour nutrition and recipe users, the standard mill
research gate, CCTO wheat extension, and food input/output/storage/Mood. This is
loaded-contract coverage, not completed growing/harvesting/milling/cooking Bills.
C# compilation and real-profile execution remain pending in an installed game.

MO integration removes the standard millstone's research prerequisites so the
minimum Grains flour loop is research-free. This external patch must be audited
against actual MO source and the final loaded Def; it is excluded from the
AMJ-only static projection. New descriptions are blank pending Japanese author
review before English translation. All new graphics are documented development
references (existing AMJ or Vanilla); no final image was generated. Environmental
choice, save migration, provider/parent inheritance and graphics require runtime
verification before changing production About.xml or claiming standalone release.

Repeat the actual-provider XML audit with `python Tests/validate_grains_chain.py --mo-root <MO-root>` against the installed or supplied MO 1.6 sources. This checks source targets/nutrition, not the resolved runtime Patch result.


## Environmental and production-job regressions (2026-10-07)

`Tests/validate_grains_environment.py` and `Tests/Fixtures/Grains_Environment.json`
fix 27 representative cells per Base/MO profile: fertility 0.5/1.0/1.4,
temperature 10/20/30°C, and 5/10/20 **effective growing days**. See the owning
balance specification in `Docs/Balance/Crops/GrainsEnvironment.md` for assumptions
and source provenance. This is an analytical finite-season model, not actual
weather, resting or frost survival. Regression mutations cover fertility exclusion,
season length, high-temperature suitability and one-grain dominance.

The seventh Pickle scenario uses loaded crops and the actual
`PlantUtility.GrowthRateFactorFor_Fertility` / `_Temperature` utilities over the
same cells. Every grain must win at least one cell; no grain may win >=2/3 of viable
cells, counting ties as wins. It does not advance a growing plant through a season.

The sixth grain-only scenario requests `AmjStageAQuickstart`, independently of New Village.
`GrainsSimulationSteps.cs` creates mature plants for all six grains (an extra Soba
plant supplies its x10 processing chain), one capable Plants/Crafting/Cooking-20
worker, processing table, profile-owned mill and a fuelled Campfire. Existing
Quickstart pawns are temporarily despawned; only this disposable map is prepared.
The test never creates harvested ingredients or recipe products. Native designated
harvest jobs create the sheaves. Eleven native `DoBill` jobs then thresh/hull,
mill and cook millet, buckwheat and wheat into all three minimum foods. The MO
wheat milling step uses `DankPyon_CraftFlourBulk` on the actual MO millstone.

Bills come from the loaded recipes, ingredient selection comes from loaded
`WorkGiver_DoBill` workers, and ingredients/products are counted across map stacks
and the test worker's carried stack. Each Bill must finish one iteration, consume
the expected ten ingredient units and produce exactly its declared output counts.
Harvest and milling/cooking must add no Straw/Hay; MO threshing's declared Straw
is allowed. The test checks available table recipes and rejects jobs that end
without their outputs. It does not call product-generation helpers itself.

To avoid reliance on normal game speed or Pickle pause state, the test pauses the
fresh map and posts batches of at most 64 `TickManager.DoSingleTick()` calls to the
Unity main thread, yielding between batches. Each job is limited to 20,000 ticks;
the production scope has a 150-second wall limit within the existing 300-second
profile process timeout. Cleanup ends the worker's job, removes setup objects,
restores terrain, parked pawns and the prior speed. Rendering, private desktop,
provider isolation, source hashes, strict summary and ERROR gate remain required.

**Verification boundary:** source/tooling/static checks can run here. This workspace
has no installed game/assemblies: the new C# has not been compiled or run against
RimWorld. Only an actual six-scenario 6/6, zero-skips, runtime ERROR 0 run of each
real profile establishes that these job tests work. Mature-plant setup does not
prove sowing, calendar growth, cold death, mood ingestion or save migration.


Production-job source review also found missing work routing for AMJ's two
processing benches and Base manual mill. Shared `AMJC_DoGrainProcessing` and
Base-only `AMJC_DoGrainsMilling` now connect those benches to native
`WorkGiver_DoBill` under Crafting. MO mill routing remains MO-owned. Static
positive/negative contracts cover giver class and fixed targets; actual jobs are
still uncompiled/unrun here. The step source preserves asynchronous cleanup while
remaining compatible with the repository's Framework C# 5 compiler syntax.


## Starting-scenario extraction and legacy compatibility

`Docs/ScenarioExtraction.md` is the owning extraction/migration procedure.
`python Tests/test_scenario_extraction.py` builds two disposable test packages
and checks six XML ownership configurations plus guard/order/duplicate regressions.
It preserves all current explicit contracts whenever Grains is present; standalone
Scenario supplies use draft RawRice 300 instead of unavailable AMJC grain refs.
Production scenario Defs/localization and MO starting differences now reside in conditional LegacyStartingScenarios; six grain-only real-profile suites now omit canonical village checks; the legacy fixture remains eight. The generator
requires fresh output and distinct `.extractiontest` IDs, records source/payload
hashes and does not install, publish or rewrite saves. An unchanged current Core
cannot coexist with a new provider; the regression explicitly rejects that mix.

Physical XML relocation is implemented. CI also checks the actual separate Scenarios repository at reviewed commit cbd5e313f9cb0871f7227e447d3faa7497fd962e through Tests/validate_scenario_pair.py (six configurations). This proves explicit XML contracts, not game loader behavior or successful old-save migration. Canonical NewVillage steps/Quickstart/start features are now Scenarios-owned; generic Stage A/environment/Bill tests remain in Grains. Exact suite names/counts/source attribution are updated together. Both real
four-profile suites and save-migration runs must retain rendering/private desktop
and ERROR gates before reporting a release-ready separation.

Scenarios build, provider-alias staging, four-profile runner, private-desktop entry point and actual-start assertions are source/tooling only: see the owner Docs/RuntimeTesting.md. They have not compiled or run here; old-save migration automation remains next.

## Upland rice scope extension (2026-10-08 audit)

Grains owns Vanilla `Plant_Rice` as **upland rice (陸稲)** through the committed Production `Patches/UplandRice.xml`, retaining `RawRice` without a duplicate item Def. XML and seven-crop analytical regression exist; loaded-Def, sow/harvest and real-game success remain unverified.

The real-provider suite retains **six named scenarios per profile**, but its C# Pickle source and static analysis now cover **seven crops**. No four-profile game execution has occurred. These tests must pass at runtime before standalone release:

- the loaded `Plant_Rice` is the Grains upland-rice definition/patch in both Vanilla and MO profiles;
- upland rice is sowable on normal ground with the implemented `Ground`-only sow tag and without `Hydroponic`;
- a native harvest produces `AMJC_RiceSheaf`; real threshing/hulling Bills yield Vanilla `RawRice`, which remains accepted by ordinary meals;
- CCTO profiles retain CCTO's existing `Plant_Rice` minimum-growth / cold-death behavior without a duplicate Grains cold-tolerance extension;
- the analytical and loaded-Def environment regressions are extended from six crops to seven and still reject a single crop dominating the representative cells;
- the real-profile matrix exercises at least one native upland-rice sow/harvest path and retains the strict runtime ERROR gate.

Future Rice Cultivation integration is not part of the Grains standalone matrix. That owner must test its water-rice crop converging on `RawRice` or the then-current Grains rice-processing path when Grains is present, without duplicating the Grains milling/food chain.


### Seven-crop Pickle regression (2026-10-08)

The four real-provider profiles retain **six named scenarios each**, now covering **seven crops** including Vanilla `Plant_Rice` in the environmental-niche and native designated-harvest checks. Loaded runtime assertions verify the upland rice growth/fertility/temperature balance, Ground-only sow tags, `RawRice` meal compatibility, and exactly one CCTO extension with a -1°C threshold only when CCTO is present. A temporary normal-soil growing zone checks engine sow eligibility with `PlantUtility.CanSowOnGrower` and `CanNowPlantAt`, and the native harvest job produces actual `AMJC_RiceSheaf`. New real rice thresh/hull Bills must yield `RawRice`; the preexisting 11 processing/cooking Bills are retained. The PowerShell expected-name registry matches the new feature files.

The upland rice XML now uses conditional replace-or-add for all six PlantProperties fields that may already be present (including CCTO's minimum growth temperature). The static test validates match and nomatch values and guards against duplicate operations. The historical six-crop analytical fixture is not rewritten.

**Still unverified:** C# compilation, actual four-profile Pickle 6/6 and ERROR 0, a calendar-controlled native Sow job, graphical rendering, old-save compatibility, and the standalone MO-dependency release gate.


### Real simple-meal Bill extension (2026-10-08)

The quickstart production scenario includes **five real Vanilla `CookMealSimple` Bills** after native harvest and the eleven preexisting grain Bills, plus two new bulk rice processing Bills. Inputs must come from additional native thresh/hull Bills using the already-harvested millet, buckwheat, barley and wheat sheaves; two additional real Soba harvests provide enough sheaves for the second bulk route. Vanilla `RawRice` is obtained via two native bulk rice thresh/hull Bills from the newly harvested `AMJC_RiceSheaf`. The five edible ingredient Defs are `AMJC_Millet` (shared by Awa/Hie/Kibi), `AMJC_Buckwheat`, `AMJC_Barley`, `AMJC_Wheat`, and `RawRice`. Each meal Bill locks its ingredient filter to one raw grain and verifies its actual consumed stack count, recipe completion and additional `MealSimple` output. No harvested or cooked ingredient is manufactured by the fixture.

A new static regression in `Tests/test_grains_chain.py` protects the E2E harness wiring and the identical four-profile feature tags. The long `@quickstart:AmjStageAQuickstart` scenario uses Pickle `@timeout:270`; the production helper's wall-clock watchdog is 240 seconds, the isolated Pickle run-wide limit is 420 seconds, and the game-process watchdog is 540 seconds. The profile suite still expects exactly six scenarios for each of four profiles, with strict scenario/ERROR-0 gating. **This is source/test harness implementation only, not a claim of successful game execution or C# compilation.** Dedicated production art, true native sow job, four-profile runtime, graphical checks, migration and release gating remain open.


## MO 1.6 source/provider preflight (2026-10-08)

The provided packaged MO archive `3219596926.zip` was checked as source evidence. All 263 XML files under the loaded `1.6/Defs` root parsed. It contains `DankPyon_Plant_Wheat` (12-day grow period, yield 28, `DankPyon_RawWheat`), `DankPyon_Flour` (nutrition 0.05), the researched `DankPyon_Millstone`, both 1× and 10× flour recipes, and `DankPyon_DoBillsMillstone` (`WorkGiver_DoBill` on Cooking, fixed to the MO millstone). This **does not prove loaded Defs, C# compilation or runtime job success**.

The existing `Tests/validate_grains_chain.py --mo-root` source validator now accepts an extracted Medieval Overhaul installation **or** a Workshop ZIP directly. In ZIP mode it reads only version 1.6 XML and checks the native MO WorkGiver, both flour recipes and wheat provider. The static regression creates a synthetic versioned ZIP and confirms that an incompatible MO WorkGiver fails before the game is run. Example: `python Tests/validate_grains_chain.py --mo-root 3219596926.zip`. Game-run four-profile Pickle, strict runtime ERROR 0, actual native sow, art and migration gates remain pending.


### Pickle run-wide timeout audit (2026-10-08)

Pickle's `-pickle-run-timeout` is measured in **minutes** and applies to the entire feature run, whereas `@timeout:270` allows one long production scenario 270 **seconds**. The former shared 4-minute (240-second) global cap could terminate this scenario prematurely. The shared launcher now accepts `-PickleRunTimeoutMinutes` (default `4` for legacy tests); Grains' four-profile runner uses `7` minutes with a separate `540`-second process watchdog. The Windows static tooling verifies `scenario < Pickle run < process` and the 40-minute four-profile watchdog boundary. This is runner verification, not proof of game runtime or C# compilation.


### MO millstone Hay byproduct regression (2026-10-08)

The **unpatched MO 1.6 provider source** declares `Hay` alongside `DankPyon_Flour` in its three milling Recipes (manual, regular and bulk). Grains' MO-conditional `MedievalOverhaul_StageA_Wheat.xml` **removes `products/Hay` from all three Recipes**, so the expected loaded Grains+MO grinding output is flour only, not Hay. The native-Bill helper compares all *loaded* Recipe product counts, rejecting undeclared Hay/Straw; the loaded-MO Pickle contract additionally asserts all three Recipes are flour-only. The upstream-MO archive validator intentionally checks the provider's original Hay before AMJ patches apply, while the Grains static validator enforces the three removal operations. Neither static check substitutes for a real RimWorld test.


### Upland rice translation and loaded Straw test hardening (2026-10-08)

`Tests/test_grains_localization.py` now enforces the six §10 author-approved Japanese/English item/recipe labels and descriptions and the four bilingual jobStrings against actual Production DefInjected/Def XML. Negative mutations of the source, localization and approved document must fail. The four-profile loaded-Def Pickle step checks the **exact** MO rice-thresh products and quantities (`AMJC_RiceInHull` plus `DankPyon_Straw`) and requires the Base thresh and both hull Recipes to have only the specified main output. Static verification is not equivalent to C# compilation, game loading or ERROR-0 success.


### Uploaded four-profile runtime failure remediation (2026-10-08; real rerun pending)

The `automated-gates(2).log` recorded Vanilla and MO Pickle failures, including missing mood description, missing `SimpleMeal` texture, a `Single()` exception and a test-only empty 15×15 search; two CCTO profiles stopped before launch on duplicate installed providers. Fixes preserve the approved 2.5-day meal rot time and standard meal Forbiddable/Ingredients/FoodPoisonable comps while avoiding a second inherited rottable; reference Vanilla `Things/Item/Meal/Simple` as `Graphic_Single`; add English/Japanese mood text; and prepare the isolated map's 15×15 central area deterministically instead of requiring untouched land to be empty. The CCTO duplicate resolver selects one local Mods copy in its **test-only provider manifest** rather than erroring when both local and Workshop CCTO are installed; duplicates of unrelated required providers remain errors. The manifest explicitly records the selected root; installed files and player configuration are untouched. Actual provider identity in game, four-profile 6/6, ERROR 0, loaded rottable comps and textures must still be verified by the real rerun.


### Real-game four-profile Pickle 6/6; temporary meal-graphic correction (2026-10-08)

The author-provided `automated-gates(3).log` confirms the exact six expected Pickle scenarios passed without skips in **all four profiles** (vanilla / vanilla-ccto / mo / mo-ccto); C# build, CCTO local-first selection and real work-Bill behavior no longer report scenario failures. However the **ERROR-0 gate still fails in all four profiles**, solely on three flour-meal graphics: `AMJC_Houtou`, `AMJC_Sobagaki` and `AMJC_MilletDumplings` use `Things/Item/Meal/Simple` with `Graphic_Single`, a path which the installed game reports cannot resolve, plus follow-on `MatFrom with null sourceTex`. Previous `Things/Item/Meal/SimpleMeal` was also missing. Do not infer texture availability from old Vanilla Def XML or the Python source projection.

As a **temporary, unapproved visual placeholder only**, these three food Defs now reuse the Grains-owned, already shipped Millet/Buckwheat three-variant PNG sets and matching `Graphic_StackCount` class. Houtou/dumplings use Millet and sobagaki uses Buckwheat. This intentionally is not a claim that the food art depicts prepared dishes; replace with proper approved individual food artwork during the post-runtime art phase. The chain validator and negative tests confirm actual `Textures/` PNG presence for all three `_a/_b/_c` variants, matching Def paths and class, so regressions to unprovided Vanilla art should be caught in CI. No PNG bytes, numbers, Recipes, thoughts, names, package IDs, load order, MO dependency, or historical copy changed. **Re-run real four-profile 6/6 and runtime ERROR 0** before marking the release gate passed. Visual approval and old-save migration remain separate.


### 四構成の実機スモーク確定結果（2026-10-08 JST）

作者アップロードの `automated-gates(4).log` により、以下の**実ゲーム**実行結果を確認した。GitHub CI上の仮想summaryではなく、各構成でQuickstarts、Pickle C# assembly、実ゲームの起動が行われたテスト結果である。

| Profile | Pickle | 隔離ログERROR | 判定 |
| --- | ---: | ---: | --- |
| `vanilla` | 6/6 | 0 | PASS |
| `vanilla-ccto` | 6/6 | 0 | PASS |
| `mo` | 6/6 | 0 | PASS |
| `mo-ccto` | 6/6 | 0 | PASS |

実行スクリプトは六つの期待シナリオ名と失敗/skip 0を検証し、ERRORレベルのログがないことも確認した。全構成でテスト対象Def/Patch/Textureのバイト同一ステージが成功した。CCTOがローカル・Workshopに重複していても、テスト用manifestにローカル側を選択して正常に実行した。粉食3品をAMJ同梱穀物の仮画像へ切り替えた `6d0c791bca3424a8e97c73fb48f906beded01ed7` の後、以前の `Texture2D` / `MatFrom` のERRORは再発していない。C#コンパイルは成功、`CS1684` は非致命警告のみ。

**この範囲のゲートはDONE：** 4構成のロード済み契約と、E2Eに組み込んだ作物収穫・加工/製粉/料理の実Bill、6シナリオ×4、隔離ランタイムERROR 0。**リリース前の残件：** 旧Core／既存セーブの読み込み・途中導入/削除、季節別のネイティブ播種/経時低温検証、日本語/英語の実UI表示、完成料理/作物/設備の専用画像と通常ズームの目視、プレイ時間・バランス、依存MOの本番解除判定。既存節に残る「実機未実施」の文言は当時の作業記録であり、最新の合否は本節を正本とする。


### 旧Coreの穀物セーブ保存契約：読取専用・実機移行未実施（2026-10-08）

Grains固有の存続確認は新規の `Scripts/grains_save_contract.py` が担当する。独立Scenariosの `Scripts/scenario_save_contract.py` は開始Scenario/Faction/PawnKindの所有者切替を担当し、Grains側で重複実装しない。Grainsの検査器はRimWorld 1.6の UTF-8 XML形式の **production-ID** `.rws` に限定し、旧Core `sucro.ancientmedievaljapan.core` とMOが保存元/更新先の双方にある場合にだけ適用する。名前の改変や保存データの修復は一切実行しない。

旧Core環境で作成した実際の旧セーブを**コピー**して、検証に使用する。元セーブは読み取り専用。作物・加工品・設備などの `AMJC_` Things と、`Plant_Rice` / `RawRice` の保存ID・Def名・数量、AMJC Recipeの保存Bill、ゲームtick、GameVersion、Mod ID集合を更新前と更新後の再保存されたXMLで比較する。必須Grains項目とVanilla米を含まないセーブは、この検証用fixtureの入力として拒否する。Id・数量・Bill等が変化した場合も不合格。時刻停止状態でのエンジンload→re-saveを比較前提とし、作物の自然成長や生産による数量変化を許容しない。

ローカル使用例（入力のSHAは作業時の実際の40文字のcommitを指定。旧版ソースとセーブの来歴は別途記録する）。

```powershell
python Scripts/grains_save_contract.py prepare --save "D:\\AMJ-TestFixtures\\old-core-grains.rws" --output "D:\\AMJ-TestResults\\grains-migration" --legacy-commit <OLD_FULL_SHA> --updated-commit <NEW_FULL_SHA>
python Scripts/grains_save_contract.py compare --before "D:\\AMJ-TestResults\\grains-migration\\baseline.rws" --after "D:\\AMJ-TestResults\\grains-migration\\same-provider-upgrade\\resaved.rws"
```

`prepare` は新しい隔離フォルダ内に元XMLのSHA256、元セーブとバイト同一な `baseline.rws`、プロバイダ/実機検証要件を `plan.json` へ保存する。既存フォルダを上書きしない。`compare` が通っても `runtimeVerified=false` と明示する。**これは実ゲーム起動器ではなく、実機で旧セーブを更新版Grainsへロード・再保存する処理は未実装**。XML要素が一致しても未解決Def、ロード後の参照、ログERRORやUIは証明されない。Scenarios追加/削除やMO解除はこの契約の外側であり、Scenarios専用ゲートまたは別のリリーステストが必要。

`Tests/test_grains_save_contract.py` はsynthetic保存XMLで数量の欠落、`RawRice` の再解釈、加工Bill差分、tick変更、Mod構成欠落、別名テストMod、破損XML、既存結果への上書きを負例として検出する。GitHub CIではこのfixtureテストのみ実行し、実旧セーブをリポジトリへアップロードしない。現在の4×6 Pickle/ERROR-0 PASSは変わらず、**旧セーブ移行の実機ゲートは依然OPEN**。


### 暦移動＋制御温度による実播種・低温成長の追加検査（2026-10-08）

既存の4構成×6シナリオの名称・件数と本番XMLを維持したまま、実Bill/収穫/調理が完了した最後に、`GrainsSimulationSteps.ProductionScope.NativeSeasonalSowAndGrowth` を追加した。Quickstartの隔離された土壌セルを使い、テスト専用の暦と屋外温度を設定して、以下の**ゲーム実装の経路**を検証する：

1. **適温25℃：** 栽培区画で陸稲を選択し、実際の `WorkGiver_GrowerSow.JobOnCell` が `JobDefOf.Sow` を提供することを確認。ジョブを動かして `Plant_Rice` の実播種を完了。
2. **暦を1 quadrum（15日）進めて5℃：** 新たな区画で陸稲の播種ジョブが出ないこと、既に播かれた陸稲の成長率が0になり、実際の `DoSingleTick` 2,200tickで成長が停止することを確認。
3. **同じ5℃：** 区画を大麦に切替え、実際の播種ジョブで `AMJC_Plant_Barley` を播き、2,200tickで成長が進むことを確認。
4. **25℃へ戻す：** 稲の成長が2,200tickで再開することを確認。区画・テスト植物・積雪深・暦tick・温度Overrideを成功/失敗時ともに復元する。

**このテストの限界：** `BiomeDef.constantOutdoorTemperature` をテスト中だけ25/5℃に設定するため、RimWorldの native sow/growth/long-tick 経路は通るが、地形・実際の季節曲線・降雪・天候変化を通じた自然発生の温度変化を検証するものではない。また固定枯死温度の**実際の枯死処理**は今回の条件（5℃）では試験していない。CCTOなし/あり、MOなし/ありの4構成での実機結果は追加変更後**未実行**。旧 `automated-gates(4).log` の6/6・ERROR 0は変更前の版の合格実績であり、新しい播種テストの実行結果として再使用しない。

今回追加したのはテストソースと回帰検証のみ。必要なゲーム本体・Pickle・QuickstartsがないCIではC#ビルドと実ゲーム動作は判断できない。 `Tests/test_grains_chain.py` は Job/生育tick/保存復元の接続が失われないことを静的に確認する。新しい実機確認でも元の `run-grains-tests.bat` を使い、4構成の6/6とERROR 0を必須にする。


### automated-gates(5).log の実機結果と再現修正（2026-10-08 JST）

2026-10-08の作者提供ログにより、新しい暦＋5/25℃実播種/成長検証で `vanilla`, `vanilla-ccto`, `mo-ccto` は各Pickle **6/6・ERROR 0**、`mo` のみ **5/6・ERRORあり**だった。失敗したシナリオ名は `Grains mo real harvest and flour food Bills complete` で、末尾に追加された温度復帰検証の `Native TickLong must resume rice growth after warming.` で失敗した。4構成すべてC#ビルド成功、CS1684は非致命の警告のみ。**この実行を4構成完全合格とは扱わない。**

RimWorld 1.6参照実装の `Plant.Resting` は現地日内割合が `<0.25` または `>0.8` の場合にtrueとなり、`Plant.GrowthPerTick` は `Resting` 時に**温度にかかわらず0**となる。旧テストは最初の昼固定後、実ジョブ時間と15日暦ジャンプ・2,200tickを重ねながら、復温直前には日内時刻を昼へ戻していなかった。MO単独での成長停止が日没/休息によるものだった可能性が高いが、ログには最後の時刻・光量がないため断定しない。

修正では、**最後の復温直前だけローカル時刻を次の正午へ進める**（`GenLocalDate.HourOfDay` と `GenDate.TicksPerHour` を使用）。テスト用の元tickは終了時に復元する。 `map.skyManager.SkyManagerUpdate()` で実スカイライトを刷新し、日内休息外・実際の光量・成長率・生育段階と25℃の生育季節を確認してから、以前と同じ`DoSingleTick` 2,200tickによる成長増加を検査する。失敗時は光量/温度係数/日内割合/成長段階/初期・最終成長量を出力し、原因を判別できるようにした。夜間休息を無視するPlantパッチ、架空の太陽光追加、成長量の強制設定、期待値緩和は行っていない。

対象はE2Eソースと静的回帰のみ。**この修正後の実機4構成＋ERROR 0は未実行**であり、旧(4)・(5)ログから合格を流用しない。本番穀物XMLや栽培数値・CCTO・MO互換挙動は不変。未完の旧セーブ、自然気候の経時検証、実際のCCTO凍害枯死、専用画像の検証は引き続き独立のゲート。


### automated-gates(6).log：MO単独再検証PASS（2026-10-08 JST）

作者提供の修正後 `mo` 単独プロファイル実行ログで、**C#ビルド成功、Pickle 6/6、隔離実行時ERROR 0** を確認した。`automated-gates(5).log` で失敗した `Native TickLong must resume rice growth after warming.` の再発はこの実行で認められなかった。修正対象は `b127e162d91403281a01c7903ac6ed64752657c2` の、最終復温フェーズでローカル正午・天空光・成長率を確認するテストである。データ保持のため隔離SaveDataを作成し、通常 `ModsConfig.xml` は変更なし。CS1684（`Span`/`ReadOnlySpan`）は引き続き非致命のコンパイラ警告。

| 証拠ログ | 構成 | 新しい暦・播種・経時成長を含むPickle | 隔離ERROR | 判定 |
|---|---|---:|---:|---|
| `automated-gates(5).log` | vanilla | 6/6 | 0 | PASS（復温修正前） |
| `automated-gates(5).log` | vanilla-ccto | 6/6 | 0 | PASS（復温修正前） |
| `automated-gates(6).log` | mo | 6/6 | 0 | PASS（復温修正後） |
| `automated-gates(5).log` | mo-ccto | 6/6 | 0 | PASS（復温修正前） |

新しい季節別播種・制御温度下の成長処理について、**各プロバイダ構成の実機合格実績は揃った**。ただしこの表の3構成は修正前、MO単独だけが修正後のコードで実行されているため、**同一コミットの修正版を4構成で一括実行したことにはならない**。最終の4構成再実行を残す。旧セーブ移行・日本語/英語の実UI・自然季節気象・CCTO閾値を跨ぐ生死・画像/プレイバランス・本番MO依存解除の各リリースゲートは別途OPEN。今回の結果は既存の制御温度テストの実機確認であり、自然季節曲線・霜の影響の実証ではない。


### automated-gates(7).log — 4構成最終回帰のNREとテスト専用照明同期修正（2026-10-08）

`automated-gates(7).log` は同一修正版4構成一括テストで、**`vanilla`、`vanilla-ccto`、`mo` はいずれも6/6不達・ERRORあり**、`mo-ccto` のみ6/6・ERROR 0。3構成の失敗シナリオはすべて `real harvest and flour food Bills complete`、表示例外は `Object reference not set to an instance of an object` で、スタックトレースなし。コンパイル全件成功、CS1684は非致命。**この回帰はFAILED**。以前の(6)のMO 6/6/ERROR0をこの同一コミット4構成のPASSへ流用しない。

`b127e16` で追加した `map.skyManager.SkyManagerUpdate()` のテスト途中・強制的な呼び出しが今回の共通原因候補。RimWorld 1.6の実装では当該メソッドは天候と画面・シェーダー・陰影まで処理し、CCTO/MO非依存の単純な日照値更新APIではない。ログから発生行は確定できないため、この因果関係は**仮説**として扱う。テストの修正では直接の `SkyManagerUpdate()` 呼び出しを廃止し、ローカル正午時点のゲーム本来の `GenCelestial.CurCelestialSunGlow(map)` 値を検証して `map.skyManager.ForceSetCurSkyGlow(solarGlow)` で**隔離Quickstartのキャッシュ照度だけ**を合わせる。元の照度も保存・復元する。稲の`TickLong`成長判定、休息時間外と温度/光量係数の条件、および2,200tickの実ゲーム進行は維持。例外には工程名と元の例外を内包させ、スタックが得られなくても原因の絞り込みが可能なようにする。

**テスト本体の新しい実機実行は未完了**。3構成のNREが完全に解消されたことや、自然季節・降雪・CCTO固定枯死を検証したとは主張しない。ゲーム本番XML/Def、依存関係、レシピ、温度値、画像を変更していない。続く実機ではまず`vanilla`単独を診断し、6/6・ERROR 0なら残る構成を確認する（未失敗条件の機械的な繰り返しは避ける）。


### automated-gates(8).log — 照明同期修正後のVanilla合格（2026-10-08 JST）

作者提供ログ `automated-gates(8).log`（原本SHA256: `967ec9afcac0915103f3213d33ac1af91b53312fa884021dd85dbeb1886dad06`）では、`vanilla` 単独のC#ビルド、Pickle **6/6**、隔離実行時 **ERROR 0** を確認した。通常のModsConfigは変更されず、CS1684は非致命警告だった。(7)のNullReferenceExceptionはこの実行では再発していない。ログ本文にコミット番号やsource-stateの内容は含まれないため、厳密なコミット/全ソースhashの対応付けまでは主張しない。

残る `vanilla-ccto` / `mo` / `mo-ccto` の照明修正後版は未確認。以前の(5)〜(7)の別版合格を転用しない。今回の合格は制御温度と暦移動を伴うネイティブ播種/成長であり、自然気象、CCTO枯死、旧セーブ、画像、公開可否の合格を意味しない。

### 4構成のソース同一性を保つ実行手順

`Scripts/GrainsSourceState.ps1` はAbout・本番Defs/Patches・BaseWithoutMO・MO互換・旧シナリオ・全翻訳・全Textures・E2Eソース/全4feature・Scripts、およびloader/build/通常ランナーのバイトと相対パスをSHA256へまとめる。絶対パス、時刻、git HEAD、設計書、TestResults、Pythonキャッシュは計算に含めない。同じバイトを別ディレクトリへ移しただけなら同じ値になる。ファイル追加/削除/改名も対象で、稲パッチや翻訳/画像を旧固定リストから漏らさない。

通常の `run-grains-tests.bat` は引き続き非表示デスクトップ・実描画経路で実行する。ランナーは開始時の全体hashをコンソール、`TestResults/Grains/matrix-source-state.txt`、各 `Pickle/source-state.txt` と `matrix.json` の `SourceHash` に記録する。各構成のbuild前と結果確定前に同じhashを要求し、途中の編集やsource-stateの不一致は終了コード2にする。構成別の6シナリオと実行時ERROR 0も従来どおり必要で、ソース同一性だけでは合格にしない。

最終4構成ゲートは、変更を終えた一つのソースで引数なし（または `all`）を実行して確認する。単独構成を診断した場合はその構成だけの証拠として扱う。旧ログ(8)のVanillaはゲーム処理修正後の診断合格として保持し、この新しいランナーの実機合格へ読み替えない。

`Tests/test_grains_profiles.ps1` はWindows PowerShell 5.1のsyntheticテストで移設/時刻/報告書に対する同値性、稲/翻訳/PNG/C#/feature/runner/Aboutの変更、追加・削除・改名、4構成共通の記録hashを検証する。このテストは実ゲーム合格を代替しない。


**CI verified (2026-10-08 JST):** commit `a055c5b0e4f76ce7d69b57c89ed08850d2e52e30` passed [Stage A run 37761723079](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Grains/actions/runs/37761723079), including Windows PowerShell 5.1 parsing and the expanded synthetic four-profile/source-drift tests, plus [Workshop payload run 37761722979](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Grains/actions/runs/37761722979). Source-identity tooling validation is DONE. This is not an installed-game execution of the new runner; corrected real-provider matrix remains OPEN.
