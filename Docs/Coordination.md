# AMJ Grains Coordination

This file is the authoritative coordination surface for separate chats, agents, and workstreams working on **Ancient & Medieval Japan Grains**.

Use it instead of asking the user to manually relay messages between workstreams.

## Working rule

At the start of AMJ Grains work:

1. Read `AGENTS.md`.
2. Read this file from `main`.
3. Check whether there are OPEN / IN PROGRESS items relevant to the current workstream.
4. Perform the work directly when possible.
5. Update this file when an item's status, owner, blocker, or result materially changes.
6. Put confirmed specifications and implementation decisions into the actual source-of-truth files as well.

This file is for coordination only. It is **not** the final design document.

## Source of truth

Current primary design source:

`Docs/Design.md`

Confirmed implementation details must also be reflected in the relevant C#/XML/Defs/Patches/localization files.

## Repository boundaries

AMJ-related standalone mods may have their own repositories and their own authoritative coordination logs.

When work belongs to another repository, create/update the handoff in that repository's:

`main:Docs/Coordination.md`

Do not use the user as the transport layer between repositories.

## Status vocabulary

- **OPEN** — needs work
- **IN PROGRESS** — currently being investigated or implemented
- **BLOCKED** — waiting on a specific prerequisite
- **DONE** — completed and reflected in the proper source of truth
- **ARCHIVED** — retained for history but no longer active

## Suggested workstream labels

Use whichever label best fits the task:

- **Core/design**
- **Agriculture/XML**
- **Food/cooking**
- **Buildings/furniture**
- **Research/progression**
- **Compatibility**
- **C#/framework**
- **Art/graphics**
- **Localization**
- **Testing/release**

## Current coordination items

### DES-IRONMAKING-001 — standalone ancient / medieval Ironmaking

**Requested by:** author (2026-10-07 JST)  
**Owner:** future Ironmaking design / compatibility  
**Status:** IN PROGRESS — confirmed concept and detailed draft recorded; implementation/repository/runtime not started

**Current durable source:** `sucRo-RimWorld/Ancient-Medieval-Japan-Project:Docs/Research/IronmakingDesign.md` (migrated under the pre-split staging rule; Project commit `f610761b8d9313f0114fdbdfb98898381946d54e`). Historical Grains design commits remain provenance only.

Author-confirmed scope: independent ironmaking from early iron working through primitive furnaces and box-furnace development to medieval tatara; Edo/early-modern completion is excluded. Grains/MO/Environment/Waterworks must not become mandatory suite dependencies. Previous MO-required Iron Resources primary-smelting ownership and deferred Ironworking policy are superseded; global ore-distribution changes remain a future separately evaluated candidate.

Detailed names, research costs, production quantities, Steel-as-Base-general-metal proxy, MO Coal reuse, extraction mechanism and equipment choices are **draft proposals**, not accepted balance/implementation. MO snapshot identifies charcoal-pile output as the same `DankPyon_Coal` used by mined coal, and IronIngot→Steel as an MO-owned chain. Historical sources distinguish medieval furnace development from later equipment and later “tamahagane” naming.

**Verification completed:** eight relevant attached-MO XML assertions match; candidate yield/fuel calculations match the table; design-link and superseded-owner checks pass. No production Defs, About metadata, DLL or PNG was changed. Old tatara / new 1.6 patch / Rice civilization actual source files were not available; no third-party copying permission or full runtime support is inferred. DBHforMedieval DLL was not decompiled. No RimWorld runtime/build/compatibility/save PASS claimed.

**Next smallest unit:** settle standalone sand-iron supply and usable general-metal endpoint, compare the initial furnace/Bill/fuel abstraction and review candidate balance. Then create/choose an owning Ironmaking repository, migrate this formal design and its handoff there, and implement/test only charcoal→small furnace→bloom→general metal before later furnaces. Keep research/balance proposals distinct from author-confirmed concept; no publishing/repository creation or background worker has been started.

### AMJ-011 — Barley post-harvest grain graphics

**Owner:** Art/graphics. **Status:** OPEN for grain items only. On main PR #20, dedicated immature/mature barley crop and densely bundled sheaf are implemented as AMJ-owned textures and XML paths. Barley in-hull and edible grain still use the shared millet item images, so those *two post-processing states* need dedicated final art before public release. Do not reopen crop/sheaf generation. Exact current crop/sheaf sources are documented in `Docs/References/GrainsCropSourceManifest.json`. Loaded-game visual appearance is a separate release gate.

### AMJ-017 — Grain-processing station graphics

**Requested by:** Alpha visual-completion audit  \
**Owner:** Art/graphics  \
**Status:** OPEN

The AMJ-specific `AMJC_GrainProcessingSpot` and `AMJC_GrainProcessingTable` are functionally validated but still use Medieval Overhaul StonecuttingSpot / Millstone graphics as development placeholders. Because these are AMJ-owned BuildingDefs normally visible during Stage A play, `Docs/Design.md §12.1.2` requires production graphics before the public Alpha.

The two buildings should remain visually related but clearly communicate the existing gameplay distinction:
- simple spot: improvised/manual, 1x1, slow;
- processing table: purpose-built, 1x1, normal speed;
- no gameplay/XML balance changes are part of the art task.

**Next action:** Art/graphics should create production textures for both grain-processing buildings after the crop-art backlog, then perform the normal in-game size/readability check.

**Result / references:** `Defs/ThingDefs_Buildings/Buildings_GrainProcessing.xml`; current temporary paths are `Things/Building/Production/StonecuttingSpot` and `Things/Building/Production/Millstone`.

### AMJ-013 — Wheat grain graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

`AMJC_Wheat` is a new processed grain state introduced by AMJ-012. The data slice temporarily reuses the accepted AMJ edible-millet stack texture. Because `AMJC_Wheat` is a distinct player-visible ThingDef rather than a deliberately shared post-harvest state, `Docs/Design.md §12.1.2` requires a dedicated production texture before the public Alpha. This does not block the already validated wheat data slice.

**Next action:** Art/graphics should provide a dedicated wheat-grain texture before the public Alpha and wire only the graphic path; do not change the validated wheat processing/balance.

**Result / references:** target DefName is `AMJC_Wheat`; harvested `DankPyon_RawWheat` remains the MO wheat-sheaf asset/display override.

### AMJ-019 — Millet hulled / edible grain production artwork

**Owner:** Grains Art/graphics. **Status:** IN PROGRESS — author-accepted in-hull image integrated; edible image and in-game review OPEN (2026-10-10 JST).

`AMJC_MilletInHull`（殻付き雑穀）は作者が提示したPNGを完成画像として承認。原画（1429×1100）を `Art/Sources/Things/Item/Resource/AMJC_Millet/MilletInHull/MilletInHull.png` に無加工で保存し、既存 `texPath` の `Graphic_StackCount` 用 `MilletInHull_a/b/c.png` を256×256、3枚同一データで置換した。元原画Git blob `4e90800baeeafaea974a4d9a96736f711ee255fc`、出力Git blob `18899fa7b663faecb77ac25e03140d297a73b6b3`。定量・レシピ・DefName・既存texPathは変更なし。PNG整合性・静的契約はCI結果で確定すること。実ゲームの見た目は未検証。

`AMJC_Millet`（殻なし・可食雑穀）は旧テクスチャのままで、作者採用済みの新画像がないため引き続きOPEN。アワ・ヒエ・キビの加工後状態は同一ThingDefを共有し、種別ごとの重複画像は不要。19種の栽培・束画像とは別計上する。正本: `Docs/Design.md §12.1.3`。

**Next:** 殻なし雑穀の採用・原画保存・3枚書き出し後、両方の通常ズームでの実ゲーム表示を確認。

### AMJ-018 — Current private-play and eventual public readiness

**Owner:** Testing/release + Art/graphics. **Status:** BLOCKED for release; source/UI/gameplay smoke checks remain. Author currently prefers private Workshop upload and normal play before public release.

PR #20 integrates immature/mature crops and bundled sheaves: 7/7/5. The 2026-10-10 source archive maps all 19 states into the owning original source tree, preserving old accepted masters. Stage A/Workshop CI for PR #20 PASS only for that head. This does **not** imply in-game rendering, runtime four-profile validation or public publication.

Remaining art: **AMJ-019 millet in-hull and edible (two shared post-harvest images)**; AMJ-011 dedicated hulled/edible barley items; AMJ-013 dedicated edible wheat grain; AMJ-017 AMJ processing spot/table; plus other unfinished processing/meal graphics identified by production audits. The 19 integrated crop/sheaf states do not include either AMJ-019 item. Soba's mature/immature/sheaf/boxed resources already have AMJ paths; do not incorrectly count them as missing. Next: verify 7 crop plants and 5 bundle graphics at normal zoom and the real MO/no-MO Def paths, then finish remaining item/station art and rerun applicable runtime gates. Old save migration is explicitly out of scope (Grains was never installed).

### ART-TEMPLATE-001 — Pixel-exact shared component policy

**Owner:** shared art/tooling
**Status:** DONE (policy/tooling); OPEN (per-family template registration at next derivative)

Author requested pixel-identical reused parts across AMJ image families. Canonical policy: `Docs/GoldenPaths/FixedImageTemplates.md`. AGENTS, ArtStyle, texture Golden Path and cover workflow now require a hashed lossless master, binary editable mask, deterministic compositing, and zero protected RGBA differences. `Scripts/Art/fixed_template.py` implements compositing/validation; its regression test is in CI. Visual-reference editing alone is no longer sufficient.

No image was generated or replaced in ART-TEMPLATE-001 itself. The masu registration gap identified here is closed by ART-TEMPLATE-004 below. Covers are registered separately in ART-TEMPLATE-003. Do not claim unrelated asset families are pixel-locked unless they have their own master/mask/manifest registration. Species style references remain references rather than identical-species templates. Pending species proposals remain pending.

### TEST-005 — Core + Environment 自動ゲームプレイ評価

**Requested by:** author (2026-10-05 JST)  
**Owner:** Core gameplay balance / cross-mod testing  
**Status:** IN PROGRESS — test implementation added; combined RimWorld runtime PASS pending

「Core + EnvironmentだけでAMJ固有の遊びが成立するか」について、機械判定できる部分を手動プレイへ残さず自動化する。

実装済み:
- Pickle Stage Aへ `Stage A crops preserve distinct gameplay roles` を追加し、短期作・収量・寒冷適応・痩せ地適応・研究ゲートの役割差を関係式として回帰検証する。
- Stage Aサマリ契約を7シナリオから8シナリオへ更新した。
- 最新GitHub Stage A validationは commit `4c77664f6a1cb09e1d89349cda0717c2d4413e48` でGreen。
- Environment側に実マップ土壌 + Core作物の統合Quickstartを追加し、Thin Soilの播種差、地図加重の肥沃度成長倍率、気候勾配を自動評価する。

手動へ残すのは、見た目、UI自然さ、テンポ、煩雑さ、「差が存在する」ことを超えた面白さのみとする。

Durable design source: `Docs/Design.md` section **Core + Environment 自動ゲームプレイ評価方針**, commit `9eace339ba63e7e23d60d4a13c46727229d2be41`.

**Next action:** ローカルRimWorldでCore `run-e2e.bat` の新8/8ゲートと、Environment `run-runtime-tests.bat` のCore+Environment統合プロファイルを実行し、実行時PASS/ERRORゼロを確定する。合格後は数値条件の手動再確認を要求しない。

### TEST-RENDERED-PUBLISH — Isolated rendered runtime tooling (2026-10-05 JST)

**Owner:** Testing/tooling
**Status:** DONE (tooling publication); latest-main runtime regression pending

The earlier local snapshot passed Core 7/7, Environment six base Quickstarts
(58/57/54/52/3/3 assertions) and CCTO 70/70, with eight clean runtime logs
and combined exit 0. Game windows were enumerated on an independent non-visible
WinSta0 desktop while Direct3D rendering stayed enabled. The first hidden run
exposed worker-thread texture/map assertions; Core now posts those two steps
through PickleDriver and checks Unity main-thread execution. New Village Python
text reads explicitly use UTF-8. The saved launcher rerun passed after a separate
Haimatsu-review game released its DLL lock. No unrelated process was terminated.

Only this task's tooling/docs are published. Original working folders and other
local art/Def/review changes are preserved. These changes were transplanted onto
latest GitHub main, retaining its newer Core eight-scenario suite and Environment
Core-profile tests. Those newer runtime gates were not executed in the recorded
run and remain pending. No production art/Def/config change is included.

**Next action:** run the saved isolated desktop launcher against updated local
repositories to exercise the newer suites; human visual acceptance stays separate.

**Procedure:** Core Docs/IntegratedRuntimeTesting.md and
Scripts/IntegratedRuntimeDesktop/Run-AMJ-IsolatedDesktop.ps1.

### ART-SOURCE-ARCHIVE-023 — Original-source inventory

**Owner:** Art/graphics. **Status:** IN PROGRESS for the historical 2026-10-07 archive only. The previous **19 historical roles / 12 archived / 7 pending** are a *legacy-source recovery snapshot*, not the current crop-family count. Current 7 mature + 7 immature + 5 sheaf production states are mapped separately in `Docs/References/GrainsCropSourceManifest.json`. In this commit the 3 current existing mature source files are reused unchanged and 16 previously unarchived high-resolution crop/sheaf source inputs are added verbatim. Earlier accepted Awa/Hie/Kibi immature originals are preserved; their latest outlined versions have distinct source filenames. Image production and art approval are not release or game-rendering evidence.

**Next:** recover only genuine missing *historical* accepted masters when author-approved identity can be proven; never replace an original with a 256px derivative.

### ARCH-MODULAR-001 — Grains modularity and optional MO dependency

**Owner:** Grains agriculture/compatibility, Scenarios owner for starting scenarios. **Status:** IN PROGRESS for current-revision fresh-start real-game verification; mandatory MO dependency removal implemented. Old-save migration is out of scope.

Canonical design: `Docs/Design.md §2.8` (Base/MO ownership boundary), `Docs/GrainsDependencyAudit.md`, `Docs/GrainsProfileTesting.md`, `Docs/ScenarioExtraction.md` and production XML. Vanilla + Grains has independent wheat, grain processing and minimum flour-food paths; MO presence selects `Compatibility/MedievalOverhaul` and MO absence selects `BaseWithoutMO`. No duplicate default wheat/flour/millstone providers on MO profile. Legacy New Village definitions stay conditional when separate Scenarios is not present; separate Scenarios owns its own runtime and save handoff.

**2026-10-10 author decision:** The old mandatory MO declaration is obsolete. Remove MO from Grains `About/About.xml` hard dependencies and retain optional `loadAfter` ordering; align README, Workshop/2game/metadata and static/profile regressions. Preserve current production `packageId=sucro.ancientmedievaljapan.core`, AMJC DefNames, MO-only wheat/flour/millstone/Straw interoperability, and CCTO optionality. This is a metadata/compatibility-contract change, **not** a claim that MO can safely be removed from a running historic Core/Grains save.

**Evidence boundaries / next work:** Four-profile 24/24 fresh native-job Pickle and ERROR 0 existed on earlier source; later climate/sow diagnostics and this dependency-metadata change have no new identical exact-head real-game matrix evidence. **2026-10-10 author clarification:** Grains has never been installed or used; no Grains saves need migration. Old-Core save load/re-save, mid-save add/remove and removing MO from hypothetical existing saves are removed from the release gate. The synthetic tools and historic notes remain archive-only, not active tasks. Graphics/normal UI, approved text, seasonal growth, fresh-start four-profile checks and publication decisions remain OPEN. No Steam upload or author-visible game test is claimed. Obsolete intermediate migration and PR step history is retained in Git history; formal current sources above supersede its prior MO-required instructions.

### ARCH-UPLAND-RICE-001 — Grains owns upland rice; paddy rice stays separate

**Requested by:** author (2026-10-08 JST)  
**Owner:** Grains design / Agriculture XML / Testing  
**Status:** IN PROGRESS — ownership re-audit complete; Production implementation and seven-crop runtime gates pending

Author-confirmed boundary: Grains owns dry-field cereals **including upland rice**, reusing Vanilla `Plant_Rice` / `RawRice` rather than creating a duplicate AMJ rice crop/item. Grains also owns grain post-harvest processing and milling. Future Rice Cultivation owns paddy/water management and water-rice cultivation; with Grains present, water rice must converge on the Grains rice/grain-processing path rather than duplicate milling or edible-rice Defs. Waterworks remains an optional water-supply layer for Rice Cultivation and is not part of the Grains loop.

Audit result: the current design still assigned water field, rice plant, paddy rice, edible rice and first-stage rice processing wholesale to Rice Cultivation, while runtime/test balance was fixed to six grains. Those statements are superseded by the updated Design boundary. CCTO already patches Vanilla `Plant_Rice`, so Grains should reuse that Def and must not add a duplicate cold-tolerance extension. Current six-grain environment and Pickle gates remain valid historical/current-implementation regressions but are insufficient for final release after this scope expansion.

**Next smallest unit:** implement the `Plant_Rice` upland-rice Patch without adding a new Plant/RawRice Def, settle its seven-crop balance against the existing six grains, remove Hydroponic sowability if runtime compatibility confirms the audited design, update Japanese-first labels/descriptions/art, extend static/Pickle environment + native harvest tests to seven crops, then run the real four-profile matrix before removing the Production MO dependency. Do not modify Rice Cultivation internals in this repository.


**ARCH-UPLAND-RICE-001 implementation slice (2026-10-08):** Vanilla `Plant_Rice` upland-rice patch and Japanese DefInjected label/description, Ground-only sow tag, 5-day/11-yield/0.7 minimum fertility/0.8 sensitivity, 10–42°C growth and 18–32°C optimal values. Existing `RawRice` is preserved, no new rice Def or CCTO extension. New static seven-crop matrix regression runs beside the historical six-crop fixture. Game-loaded seven-crop Pickle, sow/harvest, visuals, four profiles and save gates remain open. Do not claim standalone or remove MO dependency.


**ARCH-UPLAND-RICE-001 E2E follow-up (2026-10-08):** Four real-provider Pickle profiles retain six scenarios but now include `Plant_Rice` in seven-crop environment comparison and native harvest jobs. Loaded checks cover Vanilla `RawRice`, cooking eligibility, Ground-only sowTags, exact rice balance, and CCTO -1°C / extension cardinality. A temporary growing zone validates soil-sow eligibility; actual season-controlled sow remains pending. PowerShell expected scenarios changed with feature names. Rice XML additions now use conditional replace-or-add to avoid duplication with CCTO. Runtime C# compilation, four-profile ERROR 0, art and save checks remain pending.


**Grains complete-food E2E gate (2026-10-08):** Native `CookMealSimple` jobs are now exercised for `AMJC_Millet`, `AMJC_Buckwheat`, `AMJC_Barley`, `AMJC_Wheat`, `RawRice` with real harvested/threshed/hulled inputs in all four-profile features; five extra meal Bills confirm per-grain input consumed and Vanilla `MealSimple` output. Explicit Pickle scenario timeout 270s, internal watchdog 240s and isolated runner 420s are set, retaining six scenarios per profile and strict ERROR gate. Static harness-contract regression added; real game/C# run, images and save compatibility are not yet validated. Next: run the four profiles with installed game in noninteractive rendering-preserving mode; triage failures before creating production art. Do not remove MO dependency.


**ARCH-MODULAR-001 MO1.6 provider archive preflight (2026-10-08):** The supplied `3219596926.zip` yielded 263 parseable XML files in loaded `1.6/Defs`, including the MO wheat/RawWheat/Flour/Millstone/1×+10× grinding Recipe and native Cooking `DankPyon_DoBillsMillstone` WorkGiver. Enhanced the Grains static provider validator to read packaged ZIPs as well as extracted folders and reject mismatched worker/recipe sources, with a synthetic ZIP negative regression. This is real MO **source** evidence but no RimWorld executable/Assembly-CSharp was available to launch four profiles or compile C#; renderer/ERROR/save gates remain OPEN.


**Grains runtime timeout preflight (2026-10-08):** Found Pickle global `-pickle-run-timeout=4` (240s) below the seven-crop/meal `@timeout:270` scenario budget. Parameterized the shared launcher global timeout with legacy default 4min; Grains alone now uses global 7min (420s) and outer 540s process watchdog. Static Windows tooling checks the four feature tags, global cap and process/matrix budgets. The private-desktop matrix still allows 40min, and per-job internal watchdog stays 240s. No game was launched; need real 4-profile Pickle, C# compile, runtime ERROR 0 before art.

### GRAINS-DESIGN-CODE-CONSISTENCY-20261008 — ownership, MO milling and crop docs

**Owner:** Grains source/documentation QA  
**Status:** Grains static design/code reconciliation implemented; real-game gates remain open (2026-10-08 JST)

Audited Grains Design, crop cold-tolerance source-of-truth, Scenarios extraction ledger, E2E contract and MO 1.6 upstream against Production XML. Reconciled old pre-upland Rice Cultivation ownership (including §8.1), obsolete six-crop/unfinished-flour wording, stale Scenarios compatibility paths, and mismatched MO grinding Hay claims. Grains' MO wheat conditional Patch removes upstream Hay from all three grinding recipes, so the loaded milling contract is flour-only, while the provider archive remains unchanged and legitimately contains Hay. New static/negative tests and loaded Pickle assertions guard that distinction. CCTO remains Vanilla rice death-temperature owner (-1°C), while Grains owns Plant_Rice's upland growth settings. No new gameplay Def, MO dependency removal or release claim. Pending: C# compile, all four real Pickle profiles, ERROR 0, season-dependent Sow, final art and old-save migration.


**日本語説明文・翻訳の監査（2026-10-08）:** `Docs/LocalizationHistoricalReview.md` に、Grains現行Def・日本語DefInjected・作業Recipeの状態と、史実に基づく日本語候補を登録。史実の説明案はまだ作者承認前であり本番XML・英語への新規反映を保留する。Baseで藁を生成しない脱穀説明、Baseで研究不要の大麦、未実装の麦茶/味噌、非MOで成立する小麦製粉の説明だけを機能契約へ合わせて直した。名称/DefName/packageId/Recipe/バランスは変えない。次は作者の日本語レビュー後にDefInjected/英文を対応させ、四プロファイルでローカライズ結果を検証する。


**Grains localization CI golden reconciliation (2026-10-08):** The first localization audit commit was blocked by the historical MO pre-split translation fixture: six shared threshing descriptions intentionally dropped untrue Base straw claims, while the immutable fixture retained old MO-mode straw wording. Fixed the validator to assert these six exact neutral strings and normalize only those in-memory for historical comparison; all other strings and legacy gameplay hashes retain strict verification. Added two negative tests; do not edit the historical fixture or make MO/base translation branches depend on each other. Follow-up CI must PASS before moving to new work.

### AMJGRAINS-LOC-APPROVAL-20261008 — accepted Japanese, paired English

**Owner:** Grains descriptions/localization. **Status:** JP approved and paired EN strings committed to source; static parity regression added; runtime text load/ERROR-0 not executed.

The author approved the existing 15 Japanese historical description/Recipe work-string candidates except two precise wording adjustments: use **AMJGrains** rather than Grains in player-facing prose, and replace the ambiguous wheat phrase `実は食材になるほか挽いて粉食に利用できる` with `小麦の穀粒は食事の材料に使え、石臼で挽けば小麦粉として粉食にも利用できる`. Apply the other approved Japanese text without extra historical claims. `Docs/LocalizationHistoricalReview.md` §2/§6 now records exact Japanese/English pairs. Source scopes: 5 shared grain-flour/food ThingDefs, 5 shared RecipeDefs, 4 non-MO wheat/millstone ThingDefs, one non-MO wheat milling Recipe. Japanese DefInjected describes all 15 and jobStrings for six Recipes; default English XML carries matching descriptions/jobStrings. Product labels, names/DefNames, gameplay XML, MO provider ownership and historical MO fixture unchanged. `Tests/test_grains_localization.py` checks exact docs–Japanese–English correspondence. Remaining: game-loaded language switching and four-provider Pickle/ERROR-0, extra plant prose review and images.

### AMJGRAINS-SIX-CROP-APPROVAL-20261008 — approved and localized crop descriptions

**Owner:** Grains localization/historical presentation. **Status:** Six Japanese crop texts approved; JP/EN production strings added with static parity checks. Runtime/UI verification pending.

The author approved all six §7 historical crop explanations (Awa/Hie/Kibi/Soba/Barley/upland Vanilla `Plant_Rice`) without further wording changes on 2026-10-08. Replaced their five shared JP PlantDefInjected descriptions and the JP upland Rice description with exactly the approved text; translated the corresponding five shared English PlantDef descriptions and the `Patches/UplandRice.xml` English description. Canonical approved Japanese text is `Docs/LocalizationHistoricalReview.md §7`, aligned English in §8. Existing §2/§6 fifteen-approved food/milling/manual-wheat texts unchanged. Static `Tests/test_grains_localization.py` now enforces strict Japanese and English copy parity, named source XML and the conditional upland rice patch, while retaining historical/agronomic checks. `label`, DefName, packageId, gameplay, CCTO/MO integration and old fixtures preserved. Remaining: four real-game profiles, actual UI language switching, zero mod-owned runtime ERRORs, images and save migration.

### AMJGRAINS-CROP-FIXTURE-RECONCILE-20261008

**Owner:** Grains compatibility and localization tests. **State:** Follow-up to author-approved crop descriptions; CI recheck needed.

After approved crop descriptions reached main in commit `81dc10ce0d9b83f8ae0945ea63a5f2926df7deb7`, Stage A reported that five shared AMJC crop descriptions differed from immutable pre-split MO hash contracts. This was expected because the old hashes include English description text. Preserve `Tests/Fixtures/MO_PreSplit_Contracts.json`. The source validator now checks five live English descriptions against exact approved `Docs/LocalizationHistoricalReview.md` section 8 entries, restores only those five historic description strings in a deepcopy for existing hash comparison, and keeps all other contract checks intact. Test fixtures include the canonical approved document and reject unexpected edits to either the PlantDef text or its approved English source. `Plant_Rice` remains covered by the separate localization/Patch test. This is not game-runtime verification.

### GRAINS-SEVEN-CROP-BALANCE-AUDIT-20261008

**Owner:** Grains cultivation/food-chain balance. **Status:** Static full chain audit added, no gameplay retune; CI validation pending. Runtime and player-time balance remain open.

The authoritative `Docs/Balance/Crops/SevenGrainFoodChainAudit.md` now compares 7 crop choices, 10-unit thresh/hull outputs, 1:1 retention, normalized workAmount, 60/90-day flour storage, 0.5 nutrition flour input to 0.9 food, +2 Mood, and the original MO 1.6 source grinding work costs. The 27-cell seven-crop projection has all seven tied-or-unique maxima but `Plant_Rice` is only tied in six and uniquely best in zero; earlier unqualified niche phrasing is corrected in the GrainsEnvironment design source. MO wheat bulk flour costs 800 nominal work versus 300 Base; no MO-global grinding work changes have been imposed. A new `Tests/test_grains_balance_chain.py` and Stage A workflow step guard source XML/recipe/food and exact current max-count signature. `validate_grains_chain.py --mo-root` additionally verifies 300/100/800 workAmount on 1.6 source; synthetic ZIP fixture gains a negative work drift case. All tests here are static. Verify Stage A/Workshop CI and then four-profile actual Pickle, C# compile, ERROR 0, season sow, grain storage behavior, artwork, old saves before release.

### GRAINS-RICE-POSTHARVEST-IMPLEMENTATION-20261008

**Owner:** Grains production / E2E / localization. **Status:** Source implementation; full Python CI, C# compile, four-profile Pickle/ERROR-0, save migration and rendering pending.

Implemented Vanilla `Plant_Rice → AMJC_RiceSheaf → AMJC_RiceInHull → RawRice` with the shared processing benches and both individual/bulk Bills; initial work values 15/120 and 10/80, 1:1 conservation, intermediates 120-day/non-edible. Existing `RawRice` remains untouched. MO-only threshing generates `DankPyon_Straw`, Base cannot reference it. Approved Japanese copy is carried into new JP DefInjected and paired English defaults; rice crop description is narrowly aligned. Four-provider Pickle source covers native harvest, real bulk thresh, real bulk hull, Vanilla simple meal and CCTO coexistence without altering profile scenario count. Existing AMJ millet art is temporary; dedicated rice art waits for runtime validation. The historical pre-split MO fixture is not modified. Canonical design/balance: `Docs/Balance/Crops/RicePostHarvestProcessing.md`, `Docs/Balance/Crops/SevenGrainFoodChainAudit.md`. Do not remove About MO dependency or claim game validation/release until runtime gates pass.


**GRAINS-RICE-POSTHARVEST-QA-20261008:** Additional protection for the shipped rice processing source: §10 exact Japanese/English localization parity for two ThingDefs and four RecipeDefs (including four bilingual jobStrings), plus negative drift tests; Pickle loaded contracts now require the precise MO Straw Def and 1×/10× counts rather than accepting any second coproduct. Historical 38 MO contracts remain immutable. Full CI and four-profile C#/Pickle still separate; no gameplay balance/art/dependency changes.


**GRAINS-AUTOMATED-GATES-FIX-20261008:** Prepared targeted remediation for uploaded `automated-gates(2).log` errors: mood ThoughtStage empty description, invalid meal texture/stack graphic class, inherited double rottable (retain four standard meal comps and 2.5-day expiry), and overly strict empty 15×15 fixture search. CCTO-only duplicate local/Workshop installation is resolved by choosing a local copy in the test manifest, without modifying either installed copy or player ModsConfig; any other duplicate remains an error. Deterministic/negative Python and synthetic four-profile PowerShell tests expanded. This is a source correction, **not** a claim that the real 4×6 Pickle/ERROR-zero gate has passed.


**CI follow-up on automated-gates fixes (2026-10-08):** GitHub Actions run 37733027245 confirmed two failing negative tests were not guarded because the refreshed chain validator omitted the meal-comp and graphic assertions; restored those assertions and fixed the now-changed 2.5-day XPath in an existing negative test. Windows synthetic duplicate CCTO provider passed source resolution, but its manifest assertion hit PowerShell cast/member precedence (`[string]$cctoRecords[0].Root`); parenthesized the `Root` access before conversion. Confirmed by job logs before this targeted correction; the original loaded-game four-profile gate is still pending.

### GRAINS-NATIVE-SEASONAL-SOW-20261008

**Owner:** Grains native sow/temperature E2E. **Status:** Test code + deterministic static regression proposed/integrated; compiled and run against the installed game only on next author-side real-provider E2E. Existing 4×6/ERROR-0 evidence remains valid solely for earlier commit, not for the modified E2E. No production Def/Recipe/crop temperature change.

Extends the last real production scenario without changing four profiles' six-scenario manifest: uses a real grow-zone and `WorkGiver_GrowerSow.JobOnCell` -> `JobDefOf.Sow` with a capable pawn; confirms real `Plant_Rice` sow at 25 C, +one-quadrum calendar movement with controlled 5 C blocks new rice sow and stops its long-tick growth, while barley can sow/grow at 5 C, and rice resumes growth on rewarming. SingleTick is advanced in short batches, with strict timeout and try/catch preserved; fixture date, biome temperature, plants, snow depth and zone are restored. Controlled `BiomeDef.constantOutdoorTemperature` is **not** natural climate simulation and does not prove actual frost death or extreme seasonal survival. See `Docs/GrainsProfileTesting.md` and `Docs/Balance/Crops/ColdTolerance.md`. Rerun the 4 real-provider profiles and ERROR 0 after compilation; do not claim this new coverage passed until logs prove it.

### ADD-CHANGENOTE-20261008 — Workshop release metadata

**Owner:** Ancient-Medieval-Japan-Grains release/packaging
**Status:** SOURCE IMPLEMENTED — CI verification required; no Steam publication claimed

Following Project `Docs/WorkshopChangenotes.md`, added `About/Manifest.xml`, `About/Changelog.txt`, and matching `About.xml` `modVersion=0.1.0-dev`. A deterministic validator now runs in the existing Workshop payload CI. `Tests/validate_workshop_payload.py` requires both files in the subscriber archive/stage in addition to its existing YADA rules. This adds **author-side** Add Changenote support only; package ID, gameplay implementation, current live-site content, and prior test/release status are unchanged. `0.1.0-dev` is the source metadata version, not a claim of a newly performed upload.

### GRAINS-SKY-FIX-VANILLA-PASS-AND-SOURCE-IDENTITY-20261008

**Owner:** Grains automated runtime testing. **Status:** post-fix Vanilla diagnosis DONE; other three corrected runtime profiles OPEN. Source-identity guard implemented; Windows CI validation DONE (see evidence below).

Read the actual `automated-gates(8).log`: vanilla C# build succeeded, six named Pickle scenarios passed, isolated ERROR 0, player ModsConfig unchanged. Only nonfatal CS1684 warnings. Raw log SHA256 is `967ec9afcac0915103f3213d33ac1af91b53312fa884021dd85dbeb1886dad06`. No commit/source-state fingerprint appears in this console excerpt, so do not fabricate an exact source revision. Previous NRE did not recur in this run; this is not a four-profile or full release PASS.

Added profile-independent production/harness SHA256 coverage and before/after source-drift checks to the normal runner, full byte attribution to source-state, source hash to console/matrix, and synthetic positive/negative Windows regressions. Canonical procedure/evidence is in `Docs/GrainsProfileTesting.md`; temperature evidence also in `Docs/Balance/Crops/ColdTolerance.md`. No C# steps, production XML, crop values, art or dependency metadata changed. Remaining immediate game action: all four profiles from unchanged corrected source, 6/6 each and ERROR 0. Natural climate/frost, actual old saves, final bilingual UI/art and release decisions remain separate. This environment has no installed RimWorld or Windows PowerShell; do not claim local game/Windows tests.


**CI verified (2026-10-08 JST):** commit `a055c5b0e4f76ce7d69b57c89ed08850d2e52e30` passed [Stage A run 37761723079](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Grains/actions/runs/37761723079), including Windows PowerShell 5.1 parsing and the expanded synthetic four-profile/source-drift tests, plus [Workshop payload run 37761722979](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Grains/actions/runs/37761722979). Source-identity tooling validation is DONE. This is not an installed-game execution of the new runner; corrected real-provider matrix remains OPEN.

### GRAINS-SEASONAL-NRE-DIAGNOSTICS-20261008

Uploaded automated-gates(9).log reports source SHA256 fd08db39254d0272c369a781d03f43911b23f6829ec1eea3b6fe501ca20a7563. Vanilla passed 6/6 with ERROR 0; vanilla-ccto, mo and mo-ccto failed the seasonal warm-recovery setup with NullReferenceException. The excerpt does not provide individual pass counts for failed profiles or final matrix/source-drift completion. The earlier sky-update hypothesis has not resolved the failure and is not a proven cause.

Diagnostic-only E2E change: report Exception.ToString() in the outer message so Pickle's message-only output includes the underlying stack, and label individual calendar/celestial/cache/temperature/growth operations. Explicitly check rice survival and sky-manager availability without skipping or relaxing any native sow/growth assertion. Production XML, crop values, recipes, textures and dependencies unchanged. Root cause and actual-game fix remain OPEN; next installed-game execution is a focused failed-profile diagnosis, not another speculative full matrix.

### ART-GRAINS-GENERATOR-20261009 — Grains-specific grain/crop image generation entry point

**Requested by:** author (2026-10-09 JST)  
**Owner:** Art/tooling / Grains  
**Status:** CORRECTED SOURCE IMPLEMENTATION — paid API path removed; no image accepted by this work

The initial implementation called the OpenAI image API and therefore would have created separate API usage/cost outside the ChatGPT subscription. The author rejected that design. It is superseded.

Current source keeps `Scripts/Art/grains_image_generator.py` as a deterministic **prepare/review** entry point only. `prepare` resolves and hashes the registered accepted AMJ references, caller-supplied subject identity and applicable real Medieval Overhaul reference, then writes `prompt.txt`, an exact-byte reference bundle, `manifest.json`, and `generation-request.json`. The actual image is generated once with ChatGPT's built-in image generation outside the Python process. `review` then stages that PNG byte-for-byte, runs existing generated-asset QA plus relative 64 px complexity comparison, creates the review sheet, and hands boxed contents to the existing boxed-resource preparer. The script contains no `OPENAI_API_KEY`, OpenAI API endpoint, image-API request, or automatic retry/batch loop.

Because in-chat image generation displays its result immediately, this no-extra-API-cost route cannot claim private pre-display screening. The generated image remains an immediately visible, not-yet-vetted draft until `review` and semantic comparison complete, per the shared Project texture pipeline. Candidate/work output remains blocked from `Textures/`, `Art/Sources/`, and `Docs/References/`. No gameplay XML, Def paths, production PNGs, dependency metadata, Workshop payload, or publication state changed.


### GRAINS-GENERATED-ART-20261010 — crops and sheaves

**Owner:** Grains art. **Status:** SOURCE INTEGRATED / STATIC VERIFIED; fresh-game rendering OPEN.

PR #20 (`cd52a3d9e15467d2f6ebc1bdaac63cda84f98cbd`) wired seven immature and seven mature crop paths, five bundle families, Vanilla upland rice and MO wheat conditional graphical override. Latest immature outline is #4D4E3C with upright millet. The 2026-10-10 source archive preserves or maps all 19 source states via the hash-locked manifest (16 new sources, 3 preexisting originals). The author's crop image checks are acknowledged; no re-generation or repeat approval request. Static PNG / Stage A / Workshop tests are distinct from loaded-game visual acceptance.

**Next:** fresh-start screen/render inspection across actual Vanilla and MO providers, address only concrete sprite/UI failures; independently complete postharvest **millet in-hull and edible grain** (AMJ-019), barley/wheat item images and processing station art. No Steam release or real-game PASS claimed.

