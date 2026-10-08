# AMJ Core Coordination

This file is the authoritative coordination surface for separate chats, agents, and workstreams working on **Ancient & Medieval Japan Core**.

Use it instead of asking the user to manually relay messages between workstreams.

## Working rule

At the start of AMJ Core work:

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

### DES-WATERWORKS-SPLIT-001 — Waterworks / Rice Cultivation responsibility split

**Requested by:** author (2026-10-07 JST)  
**Owner:** future Waterworks design / future Rice Cultivation design  
**Status:** DONE — ownership split confirmed; Waterworks design migrated to its standalone repository; Rice Cultivation remains a separate future workstream

Confirmed boundary:
- **Waterworks is a standalone water-management mod only.** It owns natural intake, gravity-fed open canals, culverts, distribution/control points, optional stone-lined upgrades, hot-spring intake/conveyance interfaces, and minimal external water-supply integration surfaces.
- **Rice Cultivation is a separate standalone mod.** It owns paddies, rice plants, rice-specific items and processing. It must not require Waterworks.
- Rice Cultivation without Waterworks will use a simpler paddy-establishment/water abstraction so that the rice mod remains independently playable. Exact rules are deliberately deferred to the Rice Cultivation workstream.
- Waterworks + Rice Cultivation may have official optional integration so paddies can consume Waterworks network state; Waterworks itself does not own paddy logic.
- For the already-discussed rice processing handoff, “same as grains” means the **same stage pattern, not the same ThingDefs**. Rice keeps its own item chain. The author also confirmed that rice produced via haza-kake remains a separate item from normal rice. Exact rice-processing details are not to be expanded in the Waterworks workstream.

**Durable source:** Waterworks is now owned by `sucRo-RimWorld/Ancient-Medieval-Japan-Waterworks`, with authoritative design in `Docs/Design.md`. Grains retains only the ownership / compatibility summary. Historical Waterworks design commits remain in this repository for traceability, but are no longer the active design source.

**Current Waterworks v1 baseline:** authoritative details live in `sucRo-RimWorld/Ancient-Medieval-Japan-Waterworks:Docs/Design.md`. Current minimal v1 is direct natural-water adjacency + dug open canal + binary wet/dry state + fill-in restoration. A separate intake building, gate, culvert, hot-spring classification and DBH adapter are no longer v1 requirements; they are post-core candidates only when a real use case justifies them.

**Next action:** no further Waterworks implementation work should be performed in Grains. Waterworks implementation continues in `sucRo-RimWorld/Ancient-Medieval-Japan-Waterworks`. Grains should only update this boundary when cross-mod ownership or compatibility changes. Rice Cultivation remains separate.

### DES-HOTSPRING-001 — standalone Hot Springs baseline and Waterworks boundary

**Requested by:** author (2026-10-07 JST)  
**Owner:** future Hot Springs / Waterworks design  
**Status:** DONE — baseline recorded; implementation/repository creation not started

Confirmed Hot Springs as a Core/Agriculture-independent AMJ Addon. Baseline: replace Steam Geyser-style natural generation with 2×2 natural hot-spring units, bias generation toward hills/mountains, permit adjacent units, and keep undeveloped springs out of autonomous bathing. **Undeveloped natural springs remain directly usable through the pawn right-click priority action 「湯治する」**; developed springs additionally participate in normal autonomous bathing/tōji. Ambulatory injured pawns may voluntarily use only enabled, reachable, allowed-area developed springs within a real-path travel threshold, while urgent treatment/downed/major bleeding states take priority. The same 「湯治する」 priority action is available on developed springs and may bypass the autonomous-distance threshold, while reachability, allowed-area/prohibition and medical-safety conditions still apply.

Tōji is modeled as temporary injury natural-healing improvement plus mood/recreation, not direct HP restoration or a general disease/immunity cure. Exact numbers remain balance-test work.

Dubs Bad Hygiene is a required official compatibility target but not currently a hard dependency: DBH-loaded profiles must integrate bathing with hygiene and are part of release testing. Existing hot-spring mods should coexist without AMJ replacing their buildings/jobs; Standalone Hot Spring-style source interoperability is an implementation-audit target, without automatic conversion or full behavior unification.

Remote hot-water extraction/conveyance is not owned by Hot Springs. **Waterworks owns only the general water-management layer**: source intake, conveyance, remote supply/artificial baths, river/shallow-water/open-channel/culvert/distribution infrastructure, and external integration surfaces. Paddy/rice cultivation has now been split into a separate standalone Rice Cultivation mod and is no longer owned by Waterworks or Core/Grains.

**Durable source:** `Docs/Design.md`, baseline commit `52683ed3c8b27302eb1cf107543cebb55eb2ce24`; natural-spring priority-use refinement `7e49dfaa33ac9b802e6bcdc083308fded9ef106e`.

**Next action:** when either Addon implementation begins, create/choose its owning repository, read its AGENTS/Coordination first, then move implementation-specific details into that repository's formal design without turning Core into a required dependency.

### COMPAT-CBF-001 — Custom Base Framework future settlement candidate

**Requested by:** author (2026-10-06 JST)  
**Owner:** Content design / future Factions and settlement generation  
**Status:** DONE (design recording only; adoption and compatibility remain unverified)

Recorded Custom Base Framework (Workshop `3813689040`) in `Docs/Design.md`: prior-mod audit, Factions conclusion, Japanese NPC settlement framework candidate, and pending compatibility candidates. The source-of-truth design keeps Factions at its existing later priority and schedules CBF reassessment when settlement design begins.

Potential division: CBF owns procedural assembly / editor / XML export; AMJ owns Japanese building pieces, settlement plans and content. No dependency, implementation, supported-mod claim, new Addon commitment, or runtime PASS is introduced.

**Next action:** when Factions / settlement design resumes, audit current API / package / permissions and MO / terrain / faction-generation coexistence, then prototype a small rural settlement using the existing automated runtime gates.

### AMJ-020 — More Mushrooms compatibility candidate recorded

**Requested by:** author (2026-10-04 JST)  
**Owner:** Content design / Compatibility  
**Status:** DONE (design recording only; adoption and compatibility remain unverified)

The author asked to record More Mushrooms (Workshop `3813323629`) as a possible substitute for AMJ-owned mushroom additions. Durable notes are now in `Docs/Design.md`: prior-mod audit, Hunting & Gathering scope/conclusion, and compatibility candidates.

If MO + More Mushrooms provides the required mushrooms and works correctly, prefer optional compatibility patches over duplicating plants, ingredients, or artwork. Candidate adjustments include historically appropriate cultivation, disabling hydroponics, wild gathering where appropriate, and MO food/category integration. CCTO temperature support and Environment distribution are proposed responsibilities only; no counterpart repository implementation or adoption is claimed. The existing normal-AMJ coexistence policy and conditional-dependency audit still apply. This adds no Core Alpha/Stage requirement.

**Next action:** when mushroom design resumes, audit current 1.6 source/packageId/DefNames and automate MO coexistence/load/harvest/ingredient checks before deciding adoption or patch ownership. No runtime PASS or supported-mod claim is established by this documentation change.

**Result / references:** `Docs/Design.md` → More Mushrooms prior-mod audit / Hunting & Gathering / 評価待ちの互換候補.

### AMJ-009 — Soba crop/item graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

The Soba data slice uses temporary Awa/millet graphics only. Under `Docs/Design.md §12.1.2`, Soba is a separate PlantDef and its three post-harvest ThingDefs are not shared with another crop, so the **immature plant, mature plant, sheaf, in-hull grain and edible grain all require Soba-specific production art before the public Alpha**. This does not block the already validated data slice, but it does block visual completion of the Soba vertical slice.

**Next action:** Art/graphics should produce Soba-specific plant and item assets following `Docs/ArtStyle.md`, then wire them without changing the validated gameplay data.

**Result / references:** data DefNames are `AMJC_Plant_Buckwheat_Soba`, `AMJC_RawBuckwheat`, `AMJC_BuckwheatInHull`, `AMJC_Buckwheat`; current temporary paths reuse Awa/millet assets.
**2026-10-05 boxed-resource icon lock:** The author approved a dedicated empty **Japanese masu** as the canonical boxed-resource master. AMJ keeps the familiar Vanilla/MO boxed-item silhouette language, but all compatible AMJ/Vanilla/MO retextures should use the same masu treatment. The container geometry, viewing angle, rim, joinery, palette, shading and placement are fixed; only the contents change. Generate/draw contents separately and composite them into the fixed master. If whole-icon generation drifts twice, stop regenerating and use deterministic local compositing. Durable procedure: `Docs/GoldenPaths/TextureAssetPipeline.md`; visual source of truth: `Docs/ArtStyle.md`.
Current master: **approved masu v2**. New-resource production: **v4 contact study BLOCKED pending visual validation**; see ART-TEMPLATE-019.

**2026-10-05 Soba in-hull integration:** `AMJC_BuckwheatInHull` now uses Soba-specific production art at `Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull`. The approved filled exemplar is reused for stack variants a/b/c for now. Remaining AMJ-009 art backlog is Soba immature/mature plant integration, sheaf integration, and edible buckwheat grain. Master `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`; manifest `Docs/References/AMJ_Masu_Template.json`; allowed/editable mask `Docs/References/AMJ_Masu_EditableMask.png`; required-fill guide `Docs/References/AMJ_Masu_RequiredFill.png`; approved representative `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`.

### AMJ-011 — Barley crop/item graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

The Barley data slice uses temporary MO wheat plant graphics and AMJ millet item graphics. Under `Docs/Design.md §12.1.2`, Barley is a separate PlantDef and its three post-harvest ThingDefs are not shared with another crop, so the **immature plant, mature plant, sheaf, in-hull grain and edible grain all require Barley-specific production art before the public Alpha**. This does not block the already validated data slice, but it does block visual completion of the Barley vertical slice.

**Next action:** Art/graphics should create Barley-specific plant and item assets following `Docs/ArtStyle.md`, then wire them without changing the validated gameplay data.

**Result / references:** data DefNames are `AMJC_Plant_Barley`, `AMJC_RawBarley`, `AMJC_BarleyInHull`, and `AMJC_Barley`; current temporary paths use MO wheat / AMJ millet assets.

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

### AMJ-018 — Public Alpha readiness gate

**Requested by:** Core/design / Testing/release  \
**Owner:** Testing/release / Art/graphics  \
**Status:** BLOCKED

The Stage A functional slice is now substantially complete: six dry-field crops and their primary processing are implemented, MO wheat is integrated, the New Village Scenario is implemented, and the current isolated automated gate has been confirmed at **7/7 Pickle PASS + zero runtime ERROR entries**.

A 2026-10-04 audit also resolved the planned Food Drying step for the current scope. Food Drying remains priority-A optional compatibility, but Stage A grains are already dry-storage staples and the current Food Drying 1.6 outputs are crop-specific dried foods with rehydration paths. No compatibility Patch is added merely to convert AMJ grains into a different crop's dried item. `Docs/Design.md` now requires food-by-food semantic compatibility and defers actual Patch additions until suitable fresh AMJ foods such as wild greens, mushrooms, fruit or root vegetables exist.

The public Alpha is therefore blocked primarily by **production-art completion**, not by missing Stage A gameplay:
- AMJ-009: Soba plant + three post-harvest item states;
- AMJ-011: Barley plant + three post-harvest item states;
- AMJ-013: dedicated wheat-grain texture;
- AMJ-017: simple grain-processing spot + grain-processing table graphics.

After those assets are wired and visually checked, run the normal static/CI + isolated runtime gate again, then do only the minimum manual release checks that automation cannot cover: normal-zoom appearance/readability, Japanese public text, and starting feel.

**Next action:** complete the remaining production-art backlog in the order AMJ-009 → AMJ-011 → AMJ-013 → AMJ-017, rerunning automated regression after each wiring change where practical.

**Result / references:** current runtime baseline: local 7/7 + zero ERROR confirmed 2026-10-04 JST; Food Drying scope clarification `3e66838f5cf6cd2851aa11c11a7d723603057572`; Alpha-art backlog tracking `5c64ac39cc517ead52cacca88a3f9f661420ca49`.

### DOC-008 — AMJ-wide historical description audit policy

**Requested by:** author (2026-10-04 JST)  
**Owner:** Documentation/localization / content design  
**Status:** DONE (policy documentation; content audits remain per-feature work)

AMJ now treats inherited Vanilla and Medieval Overhaul descriptions as historical-presentation content that must be audited rather than automatically retained. When AMJ adopts, patches, retextures, selects, or localizes existing items, plants, animals, or comparable content, descriptions are checked from the perspective of ancient/medieval Japan and rewritten when they are anachronistic, culturally mismatched, misleading, overly modern, or otherwise unsuitable.

AMJ-authored descriptions should include supported historical facts and, where supportable, a meaningful difference from modern Japan, modern use, modern distribution, or modern production. Historically unsuitable content must not be made to look authentic through invented prose; if wording cannot solve the mismatch, the content is flagged for a separate keep/replace/remove design decision.

Authoring remains Japanese-first: research/draft Japanese, obtain author approval, then translate only the approved Japanese text into English. Durable research/source rationale is retained outside Coordination.

**Result / references:** shared guideline `Docs/HistoricalDescriptionGuidelines.md` commit `ca17b37eb3cca5266d1f62a2d73f527a503d76e5`; Core AGENTS link `3a501077be572b651dcc4d646cf84fd1730b976e`; Environment application `0e1b74173eca79dde09dffa2287fc5f72a583c27`, `3b8b7c753b79951b315c2ffe31822416a31595c8`; CCTO scope/reference `5b60adbc676f35f98e6c7c9801f22846e5ebf097`.

### DESIGN-015 — AMJ容器（甕）監査

**Requested by:** author (2026-10-05 JST)  
**Owner:** Common systems / Fermentation-Preservation design  
**Status:** DONE — design audit complete; implementation remains per-feature work

既存容器Mod・現行MO 1.6ソース・古代～中世日本の甕/陶器/桶樽史を再監査した結果、初期案の「同じ1個の甕を通常貯蔵 / 封蔵 / 発酵へ状態切替して使い回す共通システム」は採用しない方向に更新した。

確定した設計方針:
- Storage用甕と発酵甕は別ThingDef/設備でよく、同一物体のモード切替を要求しない。
- 保存用の封甕が必要ならSalt Preservation等の所有設備として別途追加し、Coreへ万能容器ロジックを置かない。
- 発酵甕はProcessor Frameworkを利用する専用Processorを優先し、Storageとの統合C#・内部コンテナ・専用Job/UIは初期実装しない。
- 粘土はMO `DankPyon_Clay` を正本とする。現行MO 1.6ではDigging Spotで20 clay / 600 work、MarketValue 1.2であり、粘土希少性を理由に甕の使い回しを強制しない。
- 大型甕のコストは原料希少性より成形・焼成・燃料・運搬側にあるため、必要ならWork量・窯/研究前提・焼成工程で表現する。
- 時代考証上、中世備前/常滑風大甕を新石器段階へそのまま出さない。早期Storageは土器系、後期は焼締大甕・埋甕・結桶/結樽等を機能側で表現する。
- Adaptive Primitive / Neolithic系のpot Storage、MOのbarrel/chest/sack等を優先再利用し、日本固有の差がない汎用Storageを重複実装しない。

歴史監査では、古代大型甕の貯蔵専用器としての利用、中世12世紀以降の甕・壺の広範な生活流通、16世紀酒屋等の埋甕遺構による酒造・液体貯蔵、鎌倉末～室町期の結桶・結樽普及を確認した。したがって「甕は貯蔵にも発酵にも使われた」は正しいが、「同じゲーム内甕を必ず転用する」は歴史的必然ではない。

Durable design source: `Docs/Design.md` section **AMJ容器（甕）— 既存Mod・時代考証監査後の方針**, commit `fa92e9f8de07f309eaa59c02b1fde63a27178ae0`.

**Next action:** 実装時は機能ごとに判断する。CoreのStorage甕は既存Storageとの差が残る場合だけ追加し、Fermentation側は専用Processor甕を設計する。共通甕状態機械の技術プロトタイプは不要。

### DOC-010 — Workshop cover common-left drift prevention

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art direction / Workshop covers  
**Status:** DONE (documentation guard; image-generation model output still requires visual inspection)

Root cause of the cross-chat cover inconsistency was not only generation variance. The repository guidance itself had drifted from the actually accepted Environment/Core visual system: `Docs/WorkshopCoverStyle.md` and the SVG schematic still described the superseded `中世日本OH` + A/M/J-initial-emphasis left block, while the accepted covers use a three-line `Ancient &` / `Medieval` / `Japan` editorial block with `Japan` in muted reddish-brown. Because a separate chat does not reliably carry the previous chat's visual context, this stale/contradictory source allowed the left side to be reconstructed incorrectly.

Prevention now in place:
- the common-left block is explicitly invariant across the series;
- addon-specific instructions may modify the right-side illustration and addon name only;
- the old Japanese heading, A/M/J emphasis, dark panel, Japan map, and red brush badge are explicitly forbidden;
- the pre-generation workflow requires a left-side preflight before image generation;
- generated results must be checked left-side first and rejected if wording, line breaks, hierarchy, or accent placement drift;
- cross-chat work must read the repository source and schematic rather than rely on remembered chat context;
- `Docs/References/AMJ_WorkshopCover_Template.svg` now matches the accepted left layout.

**Result / references:** Workshop style lock `a9e360155bb7d4daa4d1cc2b8c2bcd55d6d694d8`; reference schematic `4a35862af845e2b1971d1a489ad6f3f2ec6030fc`; ArtStyle binding `7526366b415e166fc15434038b9395b0a56b4ac6`.

**Next action:** for every future cover, proposal → author approval → preflight → generation → left-side-first inspection. Do not accept a right-side-successful image if the shared left block drifted.

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

### TEST-POLICY-003 — Non-interactive runtime tests

**Requested by:** author (2026-10-05 JST)  
**Owner:** Testing/tooling  
**Status:** DONE — project-wide policy recorded; existing visible runners remain migration work

AMJ共通方針として、人間の目視を必要としない自動テストはユーザーのデスクトップへ可視RimWorldウィンドウを出さず、非対話実行を標準とする。

- Pickle / RimTest Redux / Quickstarts / integration / runtime ERROR gate等は非表示・非対話が既定。
- 描画経路を検証する場合はrenderingを無効化せず、virtual/off-screen/hidden display相当で実描画経路を維持する。
- 可視実行はvisual/UI/操作感/遊び心地等の人間判断に限定。
- default automated runnerとvisual/debug runnerを分離する。
- 既存の可視runnerは移行対象であり、この記録は非表示化完了を意味しない。

Shared durable source: `Docs/DevelopmentGoldenPathGuidelines.md`, commit `a81c0389fb1834a098a462291b3f4814abcffef3`. Repository instruction: `AGENTS.md`, commit `2ac00e423a814708d70113e10b1edbeebfd7c353`.

**Next action:** desktop Work/local Windows toolingでCore runtime harnessを非対話実行へ移行し、8-scenario E2Eが可視ウィンドウなしで同一ERROR gateを保って通ることを確認する。

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

### AMJ-009-ART-SOBA-PLANT — Dedicated Soba plant textures

**Requested by:** author (2026-10-05 JST)  
**Owner:** AMJ Core art  
**Status:** IMPLEMENTED; first CI exposed immature-path edit bug, fix pushed

Recovered the previously approved Soba mature and immature source art from the persistent Library rather than regenerating it. Both were deterministically normalized to 256×256 transparent PNGs and wired into the Soba PlantDef:

- mature: `Textures/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`
- immature: `Textures/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png`

The former temporary Awa paths are removed from `AMJC_Plant_Buckwheat_Soba`. Stage A validation now asserts both dedicated Soba texture paths, PNG signatures, and 256×256 dimensions.

The previously approved Soba sheaf source has not been wired in this commit because the persistent Library contains several adjacent sheaf iterations and the exact author-approved one cannot be proven from the retained metadata alone. Do not guess between those variants; resolve the authoritative sheaf source separately before replacing the current RawMillet placeholder. No new ImageGen was used.


**AMJ-009 Soba plant CI follow-up (2026-10-05 JST):** The first integration CI run (#205) correctly failed Stage A because the Soba immature path was still the Awa placeholder. The write script had scoped the XML block by the first literal `</ThingDef>`, which accidentally matched the nested `descriptionHyperlinks/ThingDef` element before the plant section. The correction now scopes the replacement directly from the Soba defName through its immatureGraphicPath; no image bytes changed.

### AMJ-009-ART-SOBA-SHEAF — Dedicated Soba sheaf texture

**Requested by:** author / continuation of AMJ-009 art integration (2026-10-05 JST)  
**Owner:** AMJ Core art  
**Status:** IMPLEMENTED; CI pending

Recovered the last Soba-sheaf iteration from the persistent Library sequence before the workstream moved on to boxed-resource art. It matches the accepted Soba-sheaf design: a compact tied bundle with tan/yellow/reddish stalks, large dark triangular buckwheat fruits, three broad leaves and a few pale flowers. No ImageGen was used in this integration step.

The source was deterministically normalized to a 256×256 transparent production PNG and wired as `Graphic_StackCount` under:

- `Textures/Things/Item/Resource/AMJC_Buckwheat/RawBuckwheat/RawBuckwheat_a.png`
- `.../RawBuckwheat_b.png`
- `.../RawBuckwheat_c.png`

All three stack slots intentionally reuse the same approved silhouette for now, matching the current buckwheat-in-hull handling. `AMJC_RawBuckwheat` no longer reuses the millet sheaf path. Stage A validation now locks the dedicated texPath plus all three 256×256 PNG slots.

The edible `AMJC_Buckwheat` grain remains on its temporary millet-grain path; this commit does not create or infer that separate asset.

### POLICY-WORKSHOP-PAYLOAD-001 — Subscriber-only distribution (2026-10-07 JST)

**Requested by:** author
**Owner:** AMJ shared release / packaging
**Status:** DONE — repository policy/exclusions; actual Steam update remains separate

Core, Environment and CCTO now route subscriber-only Workshop packaging through
AGENTS and Core Docs/WorkshopPackaging.md. Root .rimignore excludes Art, Docs,
README, source, scripts/build tools, tests/fixtures/reports, VCS/editor metadata,
local overrides, archives and debug leftovers. Runtime assets, About identity,
loadFolders where used and required license/attribution remain. Development
originals stay in Git. YADA upstream Scanner.cs confirms inherited basename
rules; ineffective Patches/_LocalTest.xml is corrected to _LocalTest.xml.
Do not replace project filters with YADA's generic starter template.

Validation PASS: three tracked-file inventories; nested fixture/path-syntax,
accidental-runtime-exclusion and actual-payload leakage regressions; Core
archive/YADA equality and publisher adapter drift checks; corrected whole-Art
source-exclusion regression; Environment builder fixture retains production DLL
and root-only loader, and excludes README/Docs/Art/tests. Python/XML/workflow
syntax checks PASS. These prove packaging/static behavior, not new real-game
runtime or Steam publication success. Workshop filter CI is added with main-only
push and canceled superseded runs. Core's standard preparation gates source and
staged output; Environment's candidate builder gates the actual subscriber files.

**Next action:** apply current filters to the actual upload root before the next\nauthor-manual Workshop update; separately audit the downloaded package.\n

### ART-SOURCE-ARCHIVE-023 — Recover pre-resize accepted image masters (2026-10-07 JST)

**Requested by:** author  
**Owner:** Core art / source-archive recovery  
**Status:** IN PROGRESS — handoff restored after the previous workstream stopped without an explicit remaining-work record

#### Done

- The authoritative development-only source archive exists under `Art/Sources/`; `Art/Sources/README.md` defines the immutable-master rule, mirrored-path convention, and the prohibition on promoting a production-resolution derivative to source status.
- The following Core sources are already repository-preserved:
  - `Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.png`
  - `Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.xcf`
  - `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png`
  - `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png`
  - `Art/Sources/Workshop/AMJ_WorkshopCover_Template.svg`
  - `Art/Sources/Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg`
  - `Art/Sources/Workshop/AMJ_WorkshopCover_CommonBase.png`
  - `Art/Sources/Workshop/AMJ_WorkshopCover_VariableMask.png`
  - `Art/Sources/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`
  - `Art/Sources/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png`
  - `Art/Sources/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png`
  - `Art/Sources/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png`
  - `Art/Sources/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png`
- Workshop packaging rules already exclude the whole root `Art/` tree, so these development masters are not subscriber payload.
- Environment's separate accepted-tree source archive is owned by the Environment repository and is not part of this Core recovery item.

#### Remaining

- The Core archive is not complete. Audit all previously accepted Core image assets for an exact pre-resize / authoring source that still survives outside `Art/Sources/`.
- Priority audit families include the currently shipped Soba/Buckwheat and Millet assets, including:
  - `Textures/Things/Item/Resource/AMJC_Buckwheat/RawBuckwheat/`
  - `Textures/Things/Item/Resource/AMJC_Millet/RawMillet/`
  - `Textures/Things/Item/Resource/AMJC_Millet/MilletInHull/`
  - `Textures/Things/Item/Resource/AMJC_Millet/Millet/`
- This list is an audit queue, not a claim that an original survives for every asset. Exact source identity/provenance must be established before migration.
- Do **not** copy a 256x256 `Textures/` file into `Art/Sources/` merely to fill a gap, and do **not** regenerate a missing historical master and label it as the original.
- Where only a production derivative survives, record that limitation explicitly rather than inventing a source.

#### Next action

1. Read the completed `Art/Sources/Inventory.md` before the next single-image recovery; use its pending-source rows and do not count production derivatives as masters.
2. Verify candidate identity using available provenance, dimensions, hashes, retained approval records, and/or deterministic derivation evidence.
3. Commit each proven exact pre-resize/editor source under the mirrored `Art/Sources/` path without altering its bytes.
4. Update `Art/Sources/README.md` so its inventory matches what is actually preserved.
5. For accepted assets whose exact source cannot be recovered, leave an explicit missing-source record; do not block unrelated work by silently keeping the task open without a handoff.

This item remains open until the Core accepted-image inventory has been audited and every recoverable exact original has either been archived or explicitly recorded as unavailable.

**Handoff request (2026-10-07 JST):** This recovery is now a priority handoff to the next dedicated Core art/source-recovery chat or agent. Before starting any new Core image-production work, that workstream should read this item, recover ChatGPT/Library-only accepted pre-resize sources while they are still available, archive every proven source under `Art/Sources/`, and record unrecoverable gaps explicitly. Do not ask the author to relay this handoff manually.



**Single-asset closeout (2026-10-07 JST):** Recovered and archived only the accepted Soba mature original at `Art/Sources/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png` (1247×1261 RGBA, 779,854 bytes; SHA-256 `4899ea7fa6aed00d87b78819b26148b74ff5404c6e28ab050b5ad4042c08d97c`). The source bytes are unchanged, and `Art/Sources/README.md` records the original identity, production counterpart, provenance and the limit that the historical palette/export recipe was not reconstructed. The preceding different composition was checked and excluded. No production texture was changed. Source PNG integrity, all production PNGs, Workshop exclusion and exact copy checks PASS. This turn stops after this one image as requested; there is no background recovery worker. Overall ART-SOURCE-ARCHIVE-023 remains OPEN/IN PROGRESS for the other sources. **Next smallest unit:** recover and verify the accepted Soba immature original, then archive that one image and record its result before proceeding to item-art families.


**Whole-Core inventory closeout (2026-10-07 JST):** Completed the requested inventory before further image migration. `Art/Sources/Inventory.md` is the durable item-by-item ledger; README links it. 26 production PNGs form 14 distinct image groups (6 identical a/b/c triples); 2 production-source groups are archived, 12 pending. The current empty masu plus 4 registered Workshop roles add 5 image roles, of which 2 are archived and 3 pending. Total: **19 roles / 4 archived / 15 pending verification or recovery**, not a claim of 15 proven recoverable original files. Millet hull/edible candidate art shares one 1448×1086 sheet, so one recovered file may satisfy two rows. Three named immature-millet candidates were measured at 256×256 and remain insufficient as pre-resize originals. Two supplemental roles (masu foreground and rice line-hierarchy calibration) are separate from the total. Grain rework status does not erase the historical-source preservation task. No new image was moved or generated in this inventory turn. Inventory row/count consistency and byte-identical a/b/c grouping checks PASS; source archive remains Workshop-excluded. **Next action:** continue with one verified G08 Soba-immature source, archive its exact bytes, then update Inventory/README and this main-only log before the next image. No background worker is active.


**Single-asset closeout — G08 (2026-10-07 JST):** Recovered and archived only the accepted Soba immature original at `Art/Sources/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png` (1448×1086 RGBA, 545,958 bytes; SHA-256 `194e4b67ea25ab77d73a07f973bbbf7bfaba4ededbda9eb1366c08bc7a2e75b4`). Exact source identity: `黒背景の芽吹く植物アイコン(1).png`, Library `libfile_3f5c688ff0088191b57c3583709cbf94`. The AMJ-009-ART-SOBA-PLANT recovery record and integration `c7d5d2c229119aac717de80718ff7c2bdb92a00d` provide provenance; visual comparison confirms the production's three shoots/bud clusters, leaves and stem junctions. The unsuffixed extra-shoot composition was excluded. The historical palette/export recipe was not reconstructed, so this does not claim exact pixel-identical derivation. Source bytes and original dimensions are preserved; production textures are unchanged. Exact-copy comparison, source PNG integrity, all 26 production PNGs and Workshop exclusion checks PASS. README and Inventory now record **19 roles / 5 archived / 14 pending** (game 14/3/11, common/Workshop 5/2/3). This turn stops after this one image as requested; no background recovery worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** G13 BuckwheatInHull — obtain its registered 1254×1254 source, verify the manifest SHA-256 and accepted identity, then archive only that image and report.


**Single-asset closeout — G13 (2026-10-07 JST):** Archived only the accepted BuckwheatInHull original at `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png` (1254×1254 RGBA, 869,790 bytes; SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`). Recovered exact registered Library source `libfile_5a34c43373188191a48e3796290482af`; its SHA/dimensions match the visual_reference record in `Docs/References/AMJ_Masu_Template.json`. Visually inspected the source against production. Full-canvas RGBA LANCZOS resize to 256×256 produces 0 different RGBA pixels versus all a/b/c production slots; each production slot also matches the registered normalized representative SHA. Original bytes/dimensions were preserved, without production edits or regeneration. Exact-copy comparison, source PNG integrity, all 26 production PNGs and Workshop exclusion checks PASS. README/Inventory record **19 roles / 6 archived / 13 pending** (game 14/4/10, common/Workshop 5/2/3); the boxed-resource Golden Path now points to the preserved high-resolution filled reference. This turn stops after this one image; no background recovery worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** W02 approved Core Workshop cover reference — recover the registered JPG, verify its manifest identity/hash and 960×540 dimensions, then archive only that file and report before further moves.


**Single-asset closeout — W02 (2026-10-07 JST):** Archived only the author-approved Core Workshop cover reference at `Art/Sources/Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg` (960×540 RGB JPEG, 92,308 bytes; SHA-256 `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658`). Recovered registered original `libfile_f0ec7d3c94f88191ab304f0fbdb13946`; its SHA/dimensions match the Workshop-cover manifest and Golden Path. Visually inspected and fully decoded the JPG; exact-copy/hash checks PASS. No re-encoding, production texture/preview change, generation or Workshop publication. All 26 production PNGs and Workshop exclusion checks PASS. README/Inventory now record **19 roles / 7 archived / 12 pending** (game 14/4/10, common/Workshop 5/3/2); the cover manifest and Golden Path identify the archived reference while keeping the common base/mask pending. This turn stops after this one image; no background recovery worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** W03 fixed Workshop common base — recover the registered 960×540 PNG, verify manifest SHA-256 `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362`, then archive only that image and report.


**Single-asset closeout — W03 (2026-10-07 JST):** Archived only the fixed Workshop cover common raster at `Art/Sources/Workshop/AMJ_WorkshopCover_CommonBase.png` (960×540 RGB PNG, 149,866 bytes; SHA-256 `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362`). Recovered exact registered original `libfile_1730eee945f8819198690f7cb988c96c`; SHA/dimensions match the cover manifest/Golden Path. Visually inspected common title/background/ornaments; exact-copy/hash checks, PNG chunk/CRC boundaries, complete IDAT/zlib stream, RGB scanlines/filters, IEND and full decoding PASS. The production-only PNG validator rejects RGB encoding by policy, so the immutable RGB source was structurally validated separately without conversion; all 26 production PNGs pass the unchanged production gate. Workshop exclusion PASS. No production texture/preview edits, generation or publication. README/Inventory record **19 roles / 8 archived / 11 pending** (game 14/4/10, common/Workshop 5/4/1). Manifest and cover Golden Path now identify the preserved common base; the variable mask remains pending. Corrected the mask inventory's inherited 'same as above' shorthand so it explicitly remains unmaterialized/unarchived. This turn stops after this one image; no background worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** W04 Workshop variable mask — obtain registered 960×540 PNG, verify SHA-256 `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622`, then archive only that file and report.


**Single-asset closeout — W04 (2026-10-07 JST):** Archived only the Workshop cover variable mask at `Art/Sources/Workshop/AMJ_WorkshopCover_VariableMask.png` (960×540, 8-bit grayscale/L PNG, 1,216 bytes; SHA-256 `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622`). Recovered exact registered original `libfile_f831c30d1cac819192ed282dbf430698`; SHA/dimensions match manifest/template JSON/Golden Path. Visually inspected the mask; all pixels match registered editable regions (right-side x>=330 plus inclusive addon-label rectangle [66,378,310,426]), with 0 protected and 255 editable. Exact-copy/hash, PNG chunks/CRCs, complete IDAT/zlib stream, grayscale scanlines/filters/IEND and full decode checks PASS. This grayscale source is validated separately from the unchanged production-only indexed/RGBA gate; all 26 production PNGs PASS. Workshop exclusion PASS. No production/preview changes, generation or publication. README/Inventory record **19 roles / 9 archived / 10 pending** (game 14/4/10, common/Workshop 5/5/0); all four Workshop roles are now preserved, including the SVG. Manifest, cover Golden Path and style reference identify the archived common base/mask. This turn stops after this one image; no background worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS for game-art sources. **Next smallest unit:** G03 Hie mature plant — retrieve its candidate, verify the accepted version against current production and approval records, then archive only the proven original and report; do not promote a 256px derivative or regenerate missing art.


**Single-asset closeout — G03 (2026-10-07 JST):** Archived only the accepted Hie mature original at `Art/Sources/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png` (1254×1254 RGBA, 909,425 bytes; SHA-256 `58bc4a98f4557d5df112f97c2094d7cbb5681ea8f46c36246064b10da3c573db`). Recovered `ヒエの穂が揺れる可愛い植物アイコン.png`, Library `libfile_81f9f17fbb988191916144a698e3bfa5`. `AMJ-016` and integration `ddb7a593cd552fc7a37909838b870cbd8fc28436` record author approval; current mature production retains that integration's blob. Visual comparison confirms three golden drooping panicles, broad leaves, stems and junctions. The initially inventoried green-grained `直立したヒエの植物アイコン.png` (`libfile_b626dec6725c8191bc318e25fa265b58`) is 1254×1254 but differs from mature production and was excluded from G03; its G04 identity remains unverified. Historical placement/palette export was not reconstructed, and no exact direct-resize match is claimed. Original bytes/dimensions unchanged; no production edit or generation. Exact-copy/hash, source PNG integrity, all 26 production PNGs and Workshop exclusion checks PASS. README/Inventory record **19 roles / 10 archived / 9 pending** (game 14/5/9, common/Workshop 5/5/0). This turn stops after this one image; no background recovery worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** G04 Hie immature plant — compare the measured high-resolution green-grained candidate with the accepted immature production and approval records, then archive only a proven source; do not promote the known 256px derivative.

**Single-asset closeout — G04 (2026-10-07 JST):** Archived only the accepted Hie immature original at `Art/Sources/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png` (1254×1254 RGBA, 656,097 bytes; SHA-256 `1d1d8bd67d1bd2c28cbb3e783dab043d07f5e6877eab053a7df869b8ad703538`). Exact source: `直立したヒエの植物アイコン.png`, Library `libfile_b626dec6725c8191bc318e25fa265b58`. Visual comparison confirms the accepted three green-grained branched panicles, broad leaves, stems and junctions. AMJ-016 / approval integration `ddb7a593cd552fc7a37909838b870cbd8fc28436` record acceptance without further posture adjustment; PNG repair `0262092fa06c4578450af15c5b936fdd80156113` restored the finalization `02c4a193fe0514eba57d5aab69edf8a69145c645` blob, which current production retains. Historical palette/export steps were not reconstructed; no exact direct-resize reproduction is claimed. The named 256px derivative was not promoted to master status. Original bytes/dimensions unchanged; no production edit or generation. Exact-copy/hash, source PNG integrity, all 26 production PNGs and Workshop exclusion checks PASS. README/Inventory record **19 roles / 11 archived / 8 pending** (game 14/6/8, common/Workshop 5/5/0). This turn stops after this one image; no background worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** G05 Kibi mature plant — retrieve its high-resolution candidate, verify the accepted version against production and approval/repair records, then archive only a proven exact source and report.

**Single-asset closeout — G05 (2026-10-07 JST):** Archived only the accepted Kibi mature original at `Art/Sources/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png` (1254×1254 RGBA, 940,212 bytes; SHA-256 `53af394e4bcef8b9f45fe97237a05c9c7606fef71bdacc3e743fc64644d831e2`). Exact source: `黄金のキビ穂アイコン.png`, Library `libfile_cd4a791d96048191bde27c7f903d5dd9`. Visual comparison confirms the accepted open branched golden panicles, broad leaves, stems and junctions. AMJ-016 / approval integration `ddb7a593cd552fc7a37909838b870cbd8fc28436` record acceptance; PNG repair `0262092fa06c4578450af15c5b936fdd80156113` restored finalization `02c4a193fe0514eba57d5aab69edf8a69145c645`, and current production retains that valid blob. Historical positioning/palette export was not reconstructed; no exact direct-resize reproduction is claimed. Original bytes/dimensions unchanged; no production edit or generation. Exact-copy/hash, source PNG integrity, all 26 production PNGs and Workshop exclusion checks PASS. README/Inventory record **19 roles / 12 archived / 7 pending** (game 14/7/7, common/Workshop 5/5/0). The Done list now also includes G04, whose preceding closeout was already recorded. This turn stops after this one image; no background worker is active. Overall ART-SOURCE-ARCHIVE-023 remains IN PROGRESS. **Next smallest unit:** G06 Kibi immature plant — recover and verify its pre-resize source against the accepted production and approval/repair records; do not promote the known 256px derivative.

### ARCH-MODULAR-001 — Minimal dependencies / optional AMJ integration (2026-10-07 JST)

**Requested by:** author  
**Owner:** AMJ architecture / dependency design  
**Status:** IN PROGRESS — steps 1–3, work routing, environmental/job regression source and independent-Scenario extraction prototype implemented; static/Windows CI PASS; production Scenario transfer, C#/game/save/art/descriptions pending

The author accepted a shift from a central Core dependency tree toward **independent AMJ mods with official optional integration**. The 2026-10-07 Core/MO implementation audit is now complete and its durable conclusions are recorded in `Docs/Design.md` at commit `aa0481c8c8eba2486f1b5db7a7a28240e8314922`.

Audit result:
- Removing Medieval Overhaul as a hard dependency is **technically realistic**, but current Core cannot load MO-free yet because Stage A / New Village still contain unconditional MO Def/material/research/category/texture references.
- No production `1.6/`, production C# source, or production DLL exists in Core main; runtime implementation is XML/Patches. E2E test C# is separate.
- No production AMJC Def currently inherits an MO ParentDef. CCTO is already correctly guarded with `PatchOperationFindMod`; MO compatibility is not.
- The largest current Base couplings are `DankPyon_Straw` outputs, `DankPyon_BasicAgriculture`, `DankPyon_IronIngot`, `DankPyon_RawWood`, `DankPyon_Cereal`, MO wheat/RawWheat, MO-only New Village research/supplies, `DankPyon_Peasant`, and temporary MO texture paths.
- `Patches/MedievalOverhaul_StageA_Wheat.xml` and the MO RawWheat localization override are class A: they exist specifically to extend MO and should remain as **conditional MO compatibility**, not as Base dependencies.
- Base crop/processing functionality is class B and can be self-contained. Straw is class C: Agriculture does not need to own a duplicate straw resource merely to remove MO; Base threshing can omit straw and MO compatibility can add `DankPyon_Straw`.
- If Stage A still exposes wheat in the Vanilla profile, Vanilla has no suitable wheat PlantDef to inherit as the Stage A wheat, so AMJ needs a non-MO fallback wheat Plant/harvest chain while preserving existing `AMJC_Wheat`. MO-loaded profiles must not expose a duplicate AMJ wheat crop.
- Flour/milling is **not required merely to prove the minimum Vanilla agriculture loop** (`grow -> harvest -> primary process -> Vanilla meal`). If the Vanilla profile formally retains wheat's flour-food role, add an AMJ-owned flour/recipe then; a separate dedicated mill building is not mandatory because the existing AMJ grain-processing equipment can host a minimal milling recipe.
- Paper/Paper Press, Salt, MO Drying Rack and Processor Framework are not current Stage A production dependencies and must not become Agriculture hard dependencies. Paper/salt/drying belong to their owning feature/Addons or conditional MO integration. Future PF users must declare PF directly rather than relying on MO to pull it transitively.
- Waterworks remains Core-independent and owns **water-management infrastructure only**. Rice Cultivation is a separate standalone mod that owns paddies/rice/its primary processing and may integrate with Waterworks optionally. Agriculture/Grains owns dry-field grains and generic primary processing; cross-use remains optional compatibility.
- Keep `sucro.ancientmedievaljapan.core`, the current public Core name, `AMJC_` prefix, and existing AMJC DefNames. Architecturally, however, Core is now treated as an **Agriculture-equivalent independent content mod, not the common required foundation of the AMJ suite**.
- Existing MO+Core saves should retain current AMJC identifiers and MO-profile behavior through compatibility. Removing MO from an already-running save is a separate migration case and is not considered safe until dedicated runtime tests prove it.

Required migration order (step 1 harness implemented; production runtime migration not started):
1. Split the test harness first so a test-only Vanilla target can load Base XML without changing production About.xml.
2. Remove unconditional MO refs from Base XML and supply Vanilla/AMJ research/material/scenario paths.
3. Replace MO placeholder art used by Barley and grain-processing buildings with AMJ-owned production art.
4. Add the non-MO wheat fallback if wheat remains part of the Vanilla Stage A promise; keep MO wheat as the MO-profile source.
5. Guard/isolate all MO wheat/flour/category/straw/scenario/localization compatibility.
6. Pass the permanent four-profile matrix: Vanilla+Core, Vanilla+Core+CCTO, MO+Core, MO+Core+CCTO, with runtime ERROR 0.
7. Only after that change About.xml/load order and synchronize README/Workshop/public descriptions.

Future Fermentation/Brewing dependency tests should cover their Vanilla standalone loop plus Agriculture integration when Agriculture adds ingredients. Add MO cases only for declared MO compatibility; do not multiply by CCTO unless those mods directly touch crop-temperature definitions.

**No dependency metadata or runtime Def was changed by this audit.** About.xml still requires MO, as requested.

**2026-10-07 Grains re-scope reconciliation:** The ongoing Core-scope discussion has now been merged into this dependency workstream rather than treated as a separate design thread. The current direction in `Docs/Design.md` is to evaluate shrinking the future Core/Agriculture concept into a **Grains-focused independent mod**, while Waterworks owns paddy/rice cultivation. Relevant durable design commits include `957bdd5908c0e6995ea3f0f7837b987f613464e9`, `b92feac69babd925427d78e43599bdde29e82db8`, `cc9ad4f2b3b8b6045d6b81ed4b553b9b25a4b16b`, `b2a3dc8a4159eba5985970bf9b5c9c7e34c7023d`, `6f42c92796c8a5b1bd347d8d543ef3f5b9c87cf1`, and `582c3b1ee53bf58b4ff96c7647d33c23a7626e67`.

This changes several assumptions that must be reconciled **before** runtime migration starts:
- The standalone target is no longer merely “enough dry-field agriculture to reach a Vanilla meal.” If the mod becomes Grains, **wheat, wheat flour, and a minimal milling path are part of the standalone identity**, because wheat's defining role is flour-food rather than just another raw plant ingredient.
- Grains flour foods are intended to be research-free, low-equipment daily foods; milling must conserve total nutrition, and flour-food value comes from the extra processing/meal quality rather than free food multiplication.
- Grains' retention criterion is environmental crop choice: representative map conditions must make different grains preferable through soil fertility, temperature, growing-season length, yield and processing value. A permanent regression should verify that one grain does not collapse into the best choice across nearly all profiles.
- The former Stage E paddy/rice loop is now assigned to a separate **Rice Cultivation** mod, not Waterworks and not Core/Grains. Waterworks is water-management only. Do not use the older combined Waterworks+paddy ownership model when planning dependency removal.
- Beans, fiber and root crops are no longer safe assumptions for the future Core scope while the Grains re-scope is being evaluated. Do not perform new dependency work for those future stages until ownership is settled.
- Two earlier audit conclusions now require explicit resolution rather than silent implementation: **(a)** whether Vanilla/Grains threshing omits straw or Grains owns a non-MO straw path, and **(b)** whether MO-loaded profiles keep MO wheat as the visible crop or Grains keeps one AMJ-owned wheat source across profiles. Preserve existing save/DefName compatibility while deciding these.
- Consequently, migration step 4 is broadened from “fallback wheat if needed” to **design and test the standalone wheat + flour + milling chain**, and step 5 must then isolate or map MO wheat/flour/category/straw compatibility around that chain.

Until that reconciliation is complete, do **not** start changing `About.xml`, production dependency metadata, or runtime Def ownership merely from the older Agriculture assumptions.

**2026-10-07 Grains ownership resolution complete:** The requested Base-vs-MO ownership reconciliation is now durable in Docs/Design.md, latest design commit eb8a62dceb4c9e06557b06da9db26c262fbcbcb2. The final boundary is:
- Base/Grains owns dry-field grains, a non-MO wheat fallback, AMJC_Wheat as the shared post-thresh wheat grain, fallback wheat flour, buckwheat/millet flour, Base milling recipes, a minimal manual millstone, and research-free minimum flour foods.
- MO-loaded profiles use MO wheat/RawWheat as the visible crop/sheaf provider, converge after threshing to AMJC_Wheat, then use DankPyon_Flour as the sole standard wheat flour and DankPyon_Millstone as the standard mill. Do not expose duplicate AMJ wheat/flour/millstone in the same profile.
- Grains does not own an AMJ Straw ThingDef. Base threshing abstracts stalk residue; MO compatibility adds DankPyon_Straw only at threshing. Harvest-time and milling-time Hay/Straw remain removed in the MO integration.
- Base must contain zero unconditional MO research/material/category/scenario refs. New Village remains in the current package only as save-compatible auxiliary content during migration; its Base definition must become Vanilla/Grains-only and MO differences must move to conditional compatibility.
- Environmental grain choice is a release invariant for both Base and MO profiles; representative fertility/temperature/growing-season cases must not collapse to one grain being best almost everywhere.
- Beans, fiber/spinning/paper and root/general vegetable stages are removed from the Grains roadmap. Their historical design notes remain future AMJ candidates, but Grains ownership is explicitly invalidated.
- The current Stage A crop/Scenario tables that still show MO identifiers are marked as the current MO-required implementation snapshot until runtime migration updates code/tests and those tables together.

No runtime Def, About.xml, dependency metadata, or production texture was changed in this ownership-resolution turn.

**2026-10-07 test-harness split:** Step 1 implementation merged through PR #1. Implementation commit `a289fdbbaa07b6c94f0960fc1b1a9f959beb8589`; main merge `88124c347fee85017df8a56b9b53f602eeefa229`. Formal procedure: `Docs/GrainsProfileTesting.md`; `Docs/Design.md` records the implemented tooling boundary.
- Added `run-grains-tests.bat` with four real-provider profiles: vanilla, vanilla-ccto, mo, mo-ccto. Default execution stays on a private Windows desktop with rendering enabled.
- The disposable target copies runtime Def/Patch/texture/language bytes unchanged, changes only test metadata, and does not load production Core, MO/CCTO API fixtures or E2E graphics substitutions. Installed hard dependencies are resolved explicitly; missing/duplicate/forbidden providers and cycles fail preparation.
- Retained the old eight-scenario fixture suite. New three-scenario profile suites are migration smoke contracts, not full Grains release validation.
- Fresh per-profile SaveData/results, source/provider/payload fingerprints, timeout, named-summary checks and an any-ERROR gate are in place. All requested profiles run sequentially even when an earlier one fails.
- Verified locally: PowerShell 7.4.6 parsing; four-profile byte-preserving staging/config/summary/source-attribution/negative tests; existing Stage A/New Village, art-rule/PNG and Workshop payload gates.
- GitHub PR CI PASS: Stage A validation run `37554462337`, including Windows PowerShell 5.1 parsing and the new profile tooling regression; Workshop payload filtering run `37554462325`.
- **Not run:** C# test-assembly compilation against RimWorld and real game execution, because this cloud workspace has no RimWorld installation. No 4-profile runtime PASS is claimed. Vanilla is still expected to expose current unguarded MO references/art. Production About/Defs/Patches/Textures/Languages remain unchanged.
- Full wheat/flour/milling/food, per-profile New Village actual starts, environmental six-grain choice and save migration regressions remain to be added during implementation.

**Next action:** begin migration step 2: remove Base MO research/material/category/Straw/Scenario references and move the MO differences into conditional compatibility in the order specified in Docs/Design.md. Use the new four-profile harness during migration; build/game verification belongs to an environment with the installed RimWorld/real providers/helpers. About.xml remains last. No background worker or runtime test is currently active.


**2026-10-07 Base/MO separation step 2:** PR #2 merged. Implementation `8ed4b04990740ee80ea69c2994479496bf808b21`; main merge `41a10b62a1a0b8feae3771857e64a76a27ecbf20`. Durable implementation/design: runtime XML, `Docs/Design.md`, `Docs/GrainsProfileTesting.md` and `Docs/WorkshopPackaging.md`.
- Base Defs/localization contain zero unconditional MO identifiers. Base barley/table are research-free, table uses Steel 30, simple spot uses Woody, and Base threshing omits Straw. Base New Village has no starting research, Neolithic clothing, WoodLog 400/Steel 30, steel knives and Pemmican 1080 (54 nutrition proxy).
- Production `loadFolders.xml` conditionally activates `Compatibility/MedievalOverhaul`. MO-specific wheat recipes, original external wheat patch and RawWheat/recipe translations are isolated there. All 38 pre-split explicit AMJC contracts and original moved patch/override bytes and recipe translation values are verified preserved for MO. This proves explicit XML contracts, not resolved game behavior.
- All four real-provider suites now have five scenarios including New Village loaded settings and actual Quickstart supplies/research. Real-profile loader/runtime bytes remain unchanged in staging; only legacy fixture staging rewrites its disposable loader condition. The legacy eight-scenario suite remains separate.
- Local PASS: Stage A, Base/MO New Village, actual supplied MO 1.6 XML references (Python and PowerShell), Base-boundary negative regressions, PowerShell parsing/projection and four-profile tooling, art-rule routing, 26 production PNGs, Workshop filtering plus actual Git archive parity.
- GitHub PR CI PASS: Stage A run `37558256570` (including Windows PowerShell 5.1 parsing/tooling and new boundary regressions); Workshop payload run `37558256561`. Remote implementation tree exactly matches the locally validated Git tree.
- **Not run:** RimWorld C# test assembly compilation or real game profiles; no installed game/assemblies in this cloud workspace. Runtime ERROR 0 and successful starts are not claimed.
- Production About.xml/packageId/name/dependency metadata and texture bytes remain unchanged. Three MO placeholder graphics remain intentionally unresolved; Base wheat/flour/milling/food is not yet present, so this is not standalone-ready.

**Next action:** migration step 3 from the final Grains ownership section: add conditional non-MO fallback wheat/sheaf, AMJC_Wheat thresh convergence, fallback wheat flour plus buckwheat/millet flour, manual millstone, nutrition-conserving milling and research-free minimum flour foods. MO profiles must continue exposing only MO wheat/RawWheat, DankPyon_Flour and DankPyon_Millstone. Extend tests without weakening the preserved old MO contracts. Then replace the three MO placeholder graphics through the authorized art workflow, add environmental/save regressions, and run the real four-profile matrix in an installed-game environment. About.xml stays last. No background worker or game test is active.


**2026-10-07 author-approved Scenario extraction:** Final ownership changed: New Village Scenario, starting Faction/PawnKind, starting research and supplies belong to an independent starting-scenario mod, not Grains. Durable specification: `Docs/Design.md` — 開始シナリオの独立Mod化; test handoff: `Docs/GrainsProfileTesting.md`. Vanilla standalone is required for the scenario mod; Grains/MO are optional integrations owned there, with no hard dependency in either direction.

**Implementation state:** ownership/design only; no Def, package metadata or test feature was physically moved in this turn. Existing Base/MO Scenario differences and 38-contract preservation remain transitional. The new mod name/packageId/repository, Vanilla-only supply quantities and save-migration mechanism are not yet decided.

**Extraction handoff / pending gate:** audit the Scenario/Faction/PawnKind, translations/dialogue, compatibility patches and Quickstart/tests; preserve AMJC DefNames and ensure exactly one provider when old/new packages coexist. Prove old New Village save loading and package replacement before claiming safe removal. Transfer the scenario contracts/start tests to the new owner alongside removing Grains' dedicated-Scenario requirement; retain all grain contracts. Scenario matrix: Vanilla, Grains, MO, Grains+MO, plus old saves/coexistence and runtime ERROR 0. No physical-extraction/runtime PASS is claimed.

**Next action for this workstream:** continue Grains step 3 wheat/flour/milling/food without adding new village-start functionality to Grains. Perform physical Scenario extraction only after the migration design and verification path above are concrete. The present package retention is temporary, not a reversal of the approved separation. No background worker is active.


**2026-10-07 Grains step 3 initial XML/tooling implementation:** PR #3 merged. Main merge `d09a3de74271a17ce969795b19ac22c5ea506dbf`; implementation `c5938544cc3f58fd45a1d25c8e97b3f053aef403`, corrected head `c22fd90af7f8c8089cf34fe57da97c2e107036e4`. Durable source: `Docs/Design.md` step 3, runtime Defs/loadFolders/Patches, `Docs/GrainsProfileTesting.md`, and `Docs/Balance/Crops/ColdTolerance.md`.
- MO absence activates `BaseWithoutMO` through IfModNotActive (confirmed in supplied MO LoadFolders.xml): fallback AMJC_Plant_Wheat / AMJC_RawWheat / AMJC_WheatFlour / AMJC_ManualMillstone and wheat milling. Existing thresh recipe names converge to AMJC_Wheat. MO presence retains MO crop/sheaf/flour/mill only. Shared AMJC_BuckwheatFlour / AMJC_MilletFlour and three foods are new.
- Wheat keeps 12 days, 28 yield, fertilityMin 0.7 and sensitivity 0.9; Base has no sowing research and conditional CCTO -6°C death. Milling 10 grains ->10 flour at 0.05 nutrition/unit preserves total nutrition. Flour is non-food raw and stores 60 days. Stone initial cost BlocksGranite 30 + WoodLog 20; material acquisition still follows Vanilla.
- Houtou/Sobagaki/MilletDumplings: each 0.5 nutrition of its designated flour -> one 0.9-nutrition meal, 2.5 days storage, +2 Mood for 0.5 day, research-free Campfire/ElectricStove/FueledStove recipes. MO-only flour input substitution for Houtou; buckwheat/millet recipes use MO millstone. MO millstone research prerequisites removed conditionally for the minimum flour loop.
- All old 38 explicit AMJC MO contracts and original patch/localization snapshots remain unchanged; 11 new shared Defs are allowed explicitly, not by dropping the old gate. All four real-provider suites now have six named scenarios with loaded flour-chain contracts. Legacy fixture suite remains eight; only its disposable positive/negative loader conditions use the fixture packageId. Both conditional trees are preserved in real staging and Workshop archives.
- Local PASS: Base/MO chain and Stage A/New Village static contracts, 7 chain tests (6 negative cases) +4 Base-boundary tests (3 negative cases), supplied MO 1.6 flour/mill/source target audit, PowerShell parsing/projection and four-profile staging/config/summary attribution, 26 production PNGs and actual Git archive/payload parity (70 subscriber files).
- Initial PR CI stopped before tests on Pillow download ReadTimeout; the dependency remains pinned and pip socket timeout increased from 15 to 60 seconds. Corrected PR CI PASS: Stage A run `37560815435` (Windows PowerShell 5.1, full art/PNG checks, 7 chain tests, 4 boundary tests and Stage A/chain static validation), Workshop payload run `37560815496`. Corrected remote tree matches the validated local tree.
- **Not run:** C# test assembly compilation, real game loads, actual growing/harvesting/milling/cooking Bills, rendering, six-grain environmental dominance or old-save migration; no installed RimWorld in this cloud workspace. Added Pickle assertions are loaded-contract coverage, not proof of completed production jobs.
- New historical descriptions are explicitly blank pending Japanese-first author review then English translation. New graphics are existing AMJ/Vanilla development references; no image was generated and no production PNG changed. Existing 3 MO-dependent placeholders remain. About/packageId/dependency metadata and transitional New Village runtime configuration remain unchanged. Scenario extraction remains approved but physically pending.

**Next smallest implementation unit:** add representative fertility/temperature/season crop-choice regression and reproducible actual harvest/milling/cooking Bill tests, then compile/run the four real-provider profiles in an installed-game environment with rendering and ERROR gate retained. Complete Japanese descriptions/translation and approved asset work before release; preserve the independent scenario ownership/migration handoff. Do not remove About.xml MO dependency until runtime/art/save release gates pass. No background worker/game test is active.


**2026-10-07 Grains environment / production-job regression source and work routing:** PR #4 merged. Main merge `10ba58bea3bcb6dbfa05143e4f0ae35dd73d49b2`; initial implementation `2eeef630742bf6e93753d3ac5cff94edcedc4dda`, final head `be03af75de85bc83c67578a23a0ed13ef2f2feee`. Durable sources: `Docs/Balance/Crops/GrainsEnvironment.md`, `Docs/GrainsProfileTesting.md`, `Docs/Design.md`, runtime WorkGiverDefs and E2E/tooling.
- Added 27 fertility (0.5/1.0/1.4), temperature (10/20/30°C), effective-growth-season (5/10/20 days) cells per Base/MO. 23 viable cells; all six grains have a maximum-yield niche. Wins including ties: Awa 1, Hie 2, Kibi 8, Soba 4, Barley 4, Wheat 6. No grain wins >=2/3 of viable cells. Snapshot and four test methods (including four mutation subcases) cover the analytical boundary. This excludes calendar light/resting/weather, sow/harvest labor, frost death and Straw value; the full environmental release gate is still pending.
- Added loaded PlantUtility environment assertions and six-grain real-harvest plus eleven native thresh/hull/mill/cook Bill steps, using generic Stage A Quickstart rather than New Village. Mature plants/worker/benches/fuel are setup; harvested inputs/products are never created by test code. Assertions cover harvest yield bounds, exact ingredient consumption/product counts, one Bill iteration and Straw/Hay boundaries. Main-thread 64-tick batches, per-job/whole-suite bounds and cleanup are documented. These are new C# sources, not proven runtime results.
- Source review caught missing native work routing: shared AMJC_DoGrainProcessing now connects Spot/Table, Base-only AMJC_DoGrainsMilling connects the manual mill, both under Crafting. MO's existing mill worker remains the owner there. New WorkGiver Japanese functional labels added. Nine chain regression methods now include bad/missing routing mutations. All 38 original MO explicit contracts remain preserved; shared new-Def allowlist extends explicitly for the new WorkGiver.
- All four real-provider features now require eight named scenarios, 8/8 with zero skips. Build inputs/source fingerprints include the new step source and work routing XML. Tooling rejects old six-scenario reports; provider isolation, byte-preserving staging, private desktop/rendering and any-ERROR gate remain intact. Legacy fixture feature remains eight and its historical assertions remain separate.
- Local PASS: 4 environment +9 chain +4 Base tests, Stage A/actual supplied MO source audit, PowerShell four-profile config/staging/summary/provenance negatives, art routing/26 PNGs and final actual Git archive subscriber payload (74 runtime files; 129 development files excluded). Remote final tree exactly matches validated local tree `b65edacdf1c7840e083b6e10472262fd2321cdd5`.
- Final-head GitHub CI PASS: Stage A `37562510088` (includes Windows PowerShell 5.1 and new environment/routing tests), Workshop payload `37562510092`. These workflows do not compile C# or launch RimWorld.
- **Not run:** C# test-assembly compilation and all four actual game profiles, runtime ERROR 0, growing/sowing/calendar climate survival, mood ingestion, final graphics or old-save migration. No game/managed assemblies are installed here. Existing three MO-dependent graphic placeholders remain. No About/packageId/name/texture changes; no images generated. Scenario ownership remains independent and physical extraction pending.

**Next smallest unit:** compile the real-provider test assemblies against installed RimWorld and run the isolated eight-scenario profiles, fixing API/setup/job failures from actual evidence. Base graphic placeholder resolution is a known prerequisite for a clean Base runtime log; use the authorized art workflow. Keep full environmental cold/Straw/save gates open. If continuing in this game-free cloud workspace, advance the independent-Scenario extraction inventory/migration design or Japanese-first description drafts without claiming runtime success or prematurely removing About's MO dependency. No background worker/game test is active.


**2026-10-07 independent starting-scenario extraction prototype:** PR #5 merged. Main merge `567d2abd20ed5bf4fa49df2b1026c3945849ff0a`; implementation `b46b8a3fa05824a4c91d2449e4ec624fbe576361`. Formal source: `Docs/ScenarioExtraction.md`, linked from Design/GrainsProfileTesting; machine-readable inventory: `Tests/Fixtures/ScenarioExtraction/manifest.json`.
- Inventoried three preserved Defs (AMJC_NewVillage / AMJC_PlayerVillage / AMJC_Villager), five localization/dialogue files, two scenario-owned MO patch operations and the runtime test handoff. Grain-related MO operations remain Grains-owned; generic Stage A/environment/Bill tests are not part of the scenario transfer.
- Added standard-library `Scripts/prepare_scenario_extraction.py`. It generates a disposable Grains + independent StartingScenarios pair, requiring fresh repository-external output and distinct .extractiontest IDs. No permanent package identity/repository is assigned; it does not install, publish, rewrite saves or touch production runtime sources. Source and generated payload SHA-256 records are included.
- Prototype Grains relocates legacy scenario Defs/languages and MO start differences under conditional LegacyStartingScenarios. They load only when the independent provider is absent; the MO legacy patch additionally requires active MO. The new provider owns the same DefNames/types when enabled, with Vanilla base and optional MO then Grains differences. Loader positive/negative conditions and patch order are explicit, not implicit mod-order guesses.
- Six configurations pass explicit XML ownership/reference projection: legacy Grains with/without MO, independent Scenario with/without MO, and both packages with/without MO. Every current explicit Def contract and ordering is preserved in all four configurations with Grains. Standalone stocks use **draft-only RawRice 300** as the substitute for Millet 200 + RawMillet 100; this is not a formal balance acceptance or a claim of equivalent labor/nutrition/storage.
- Eight regression methods include duplicate providers with unchanged old Core, lost legacy/MO guards, reversed optional-patch order, unconditional grain refs, unsafe IDs/overwrite, input hashes/localization-byte preservation and generated-payload hashes. Unchanged current Core + new provider is explicitly rejected; production migration must update Core/Grains to the guarded version first. The normal runtime suites remain unchanged at eight each.
- Local PASS: extraction 8 methods, Base 4/chain 9/environment 4, Stage A and art-routing/26 production PNGs, Workshop filtering and actual Git archive parity. PR CI PASS: Stage A `37604039492` (including Windows PowerShell 5.1 and new extraction regressions), Workshop payload `37604039468`. The seven-file implementation tree exactly matched validated local source `9fa81d4135d5909139bc0e7cce14eb27d5d26633`. Other main art-source archive changes were retained during integration; the merged tree was checked separately before this handoff.
- **Not run / not completed:** physical production Def/test ownership transfer, permanent mod metadata/repository, full inherited references/graphics/engine loader, actual starts and old-save read/save/removal. No installed game/assemblies exist here. Current production About/Defs/Patches/loadFolders/Languages/Textures remain unchanged by this work. Existing Grains/MO save content cannot be replaced by the standalone Scenario alone merely because the faction/pawn-kind names are preserved.

**Next smallest unit:** settle the independent module identity/storage, apply the reviewed guarded extraction to production and transfer only NewVillage test ownership. Update all hard-coded profile loader/staging/source hashes/counts, Workshop runtime-prefix validation and archive adapters together. Then compile/run the four independent-scenario start profiles and old-save/add/remove cases on an installed game, retaining private desktop, actual rendering and ERROR 0. Do not claim safe Core/MO removal, delete legacy compatibility Defs or remove production About's MO dependency ahead of their runtime/art/save gates. No game or background worker is active.


**2026-10-07 independent Scenarios repository registration and Core repository rename:** Author created `sucRo-RimWorld/Ancient-Medieval-Japan-Scenarios` and renamed Core repository to `sucRo-RimWorld/Ancient-Medieval-Japan-Grains` (same repository ID 1397406397). Scenario source commit `13372c3794217446ae449140c8e4dd6db77d09ae`; tree `5713051604c17ffb05d251efab911f53a4b53154` exactly matches locally validated source.
- Selected identity: Ancient & Medieval Japan - Scenarios / `sucro.ancientmedievaljapan.scenarios`; separate Git repository, not an embedded module. Formal ownership/identity reflected in Design and ScenarioExtraction. Current Grains packageId `sucro.ancientmedievaljapan.core` and AMJC DefNames stay intact. Repository rename is not a production Mod metadata/dependency migration.
- Scenarios owns candidate 3Def/5localization files and optional MO then Grains start patches. Vanilla-only RawRice 300 remains draft-only. Four local test methods cover four XML configurations, guard-loss/order negatives and identity/dialogue. Workshop .rimignore and Git archive adapter parity pass: 13 runtime/license files. Runtime/start/save migration and runtime-test ownership transfer remain unverified/pending.
- Grains production loader/Defs remain unchanged. Current Grains + candidate Scenarios still duplicates DefNames; do not enable that pair until guarded LegacyStartingScenarios migration is merged. Next owner task: update Grains physical extraction/staging/validators and move only scenario runtime tests into Scenarios, then run real four-profile start and old-save/add/remove tests with rendering and ERROR gate. Grains About MO dependency stays behind existing release gates. No game/background worker active.


**2026-10-07 guarded production Scenario extraction (XML/static unit):** Grains PR #6 merged at `3b92e3816d78f8ee9596c87a76e937f276d3344c`; implementation `c5567a5d8c08be59d96cb5db07bc518ca8c9f332`. Scenarios migration notice updated at `f6c0b5a423c660b377407b52341ecb3082388c46`. Formal sources: Design/ScenarioExtraction/GrainsProfileTesting, loadFolders, LegacyStartingScenarios and manifest.
- Moved 3Def and 5language files byte-for-byte into production LegacyStartingScenarios, loaded only when Scenarios is absent. Split 2 MO starting operations from grain patches; legacy MO root requires MO present AND Scenarios absent. New starts remain Scenarios-owned; legacy copies preserve fallback/provider contracts. No packageId/DefName/About dependency/texture changes.
- Updated Python/PowerShell projections, Base boundary, real/fixture staging, build-e2e, source fingerprints and Workshop runtime-prefix validation. Fixture rewrites both MO-positive roots and preserves Scenario absence guards. All 38 historical MO explicit contracts remain intact. Workshop filter/actual archive parity PASS: 75 subscriber files, legacy runtime files retained.
- Local PASS: extraction 8, Base 4, chain 9, environment 4 methods; actual separate production pair six configurations; PowerShell profile/fixture negatives; Stage A; art routing; 26 PNGs. GitHub CI PASS: Stage A `37614452046` (including Windows PowerShell 5.1 and actual independent owner checkout) and Workshop `37614451954`. Implementation remote tree exactly matched local `28d43217114215deb9089b8a705a91c8ab3167e1`. Concurrent Waterworks/Ironmaking design changes retained; merged tree separately revalidated. CI pins reviewed Scenarios cbd5e313f9cb0871f7227e447d3faa7497fd962e; later Scenarios changes affect migration notices, not Def/Patch/loader bytes.
- **Not completed:** runtime-test/Quickstart ownership transfer, C# compilation, game loader/inheritance/full refs, real starts, old-save/add/remove/re-save and runtime ERROR 0. No installed game/assemblies here. RawRice 300 remains draft-only. XML/static success does not establish safe save changes, Core/MO removal or release readiness. Prior current-Grains duplicate warning is superseded for the guarded commit; older versions still duplicate. About MO dependency remains gated.

**Next smallest unit:** transfer NewVillage runtime steps/Quickstart/start features to Scenarios; retain generic Stage A/environment/native Bill tests and explicit legacy-save regression in Grains. Add four independent start profiles plus old-save/add/remove coverage with accurate source/summary attribution, then compile/run on installed RimWorld with offscreen/private rendering and ERROR gate. No game/background worker active.

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

### AMJGRAINS-SIX-CROP-HISTORICAL-REVIEW-20261008

**Owner:** Grains localization/historical presentation. **Status:** Six new Japanese draft descriptions researched and archived; author approval pending; no runtime text changes.

Following approval and shipping of 15 grain flour/food/manual-wheat descriptions in `eff3dd9c8e301d99d8d83b267f7bd15432897326`, audited the remaining shared Awa/Hie/Kibi/Soba/Barley plants and Vanilla `Plant_Rice` upland localization against committed PlantDefs/Patch and public archaeological/government evidence. `Docs/LocalizationHistoricalReview.md §7` owns six **unapproved Japanese-only** descriptions (recognized kanji first; AMJGrains name; gaming roles vs historic/ecological claims separated; near-modern rice decline limited to documented record). `Tests/test_grains_localization.py` confirms six candidate keys, live-language isolation, and key source agronomic contrasts. Do not translate or publish the six drafts before author approval. No DefName, packageId, label, CCTO ownership, harvested Def, balance, textures, or MO provider changed. Next after approval: JP DefInjected + aligned English, source/translation checks; real Pickle/UI/saves still outstanding.

### AMJGRAINS-SIX-CROP-APPROVAL-20261008 — approved and localized crop descriptions

**Owner:** Grains localization/historical presentation. **Status:** Six Japanese crop texts approved; JP/EN production strings added with static parity checks. Runtime/UI verification pending.

The author approved all six §7 historical crop explanations (Awa/Hie/Kibi/Soba/Barley/upland Vanilla `Plant_Rice`) without further wording changes on 2026-10-08. Replaced their five shared JP PlantDefInjected descriptions and the JP upland Rice description with exactly the approved text; translated the corresponding five shared English PlantDef descriptions and the `Patches/UplandRice.xml` English description. Canonical approved Japanese text is `Docs/LocalizationHistoricalReview.md §7`, aligned English in §8. Existing §2/§6 fifteen-approved food/milling/manual-wheat texts unchanged. Static `Tests/test_grains_localization.py` now enforces strict Japanese and English copy parity, named source XML and the conditional upland rice patch, while retaining historical/agronomic checks. `label`, DefName, packageId, gameplay, CCTO/MO integration and old fixtures preserved. Remaining: four real-game profiles, actual UI language switching, zero mod-owned runtime ERRORs, images and save migration.

### AMJGRAINS-CROP-FIXTURE-RECONCILE-20261008

**Owner:** Grains compatibility and localization tests. **State:** Follow-up to author-approved crop descriptions; CI recheck needed.

After approved crop descriptions reached main in commit `81dc10ce0d9b83f8ae0945ea63a5f2926df7deb7`, Stage A reported that five shared AMJC crop descriptions differed from immutable pre-split MO hash contracts. This was expected because the old hashes include English description text. Preserve `Tests/Fixtures/MO_PreSplit_Contracts.json`. The source validator now checks five live English descriptions against exact approved `Docs/LocalizationHistoricalReview.md` section 8 entries, restores only those five historic description strings in a deepcopy for existing hash comparison, and keeps all other contract checks intact. Test fixtures include the canonical approved document and reject unexpected edits to either the PlantDef text or its approved English source. `Plant_Rice` remains covered by the separate localization/Patch test. This is not game-runtime verification.

### GRAINS-SEVEN-CROP-BALANCE-AUDIT-20261008

**Owner:** Grains cultivation/food-chain balance. **Status:** Static full chain audit added, no gameplay retune; CI validation pending. Runtime and player-time balance remain open.

The authoritative `Docs/Balance/Crops/SevenGrainFoodChainAudit.md` now compares 7 crop choices, 10-unit thresh/hull outputs, 1:1 retention, normalized workAmount, 60/90-day flour storage, 0.5 nutrition flour input to 0.9 food, +2 Mood, and the original MO 1.6 source grinding work costs. The 27-cell seven-crop projection has all seven tied-or-unique maxima but `Plant_Rice` is only tied in six and uniquely best in zero; earlier unqualified niche phrasing is corrected in the GrainsEnvironment design source. MO wheat bulk flour costs 800 nominal work versus 300 Base; no MO-global grinding work changes have been imposed. A new `Tests/test_grains_balance_chain.py` and Stage A workflow step guard source XML/recipe/food and exact current max-count signature. `validate_grains_chain.py --mo-root` additionally verifies 300/100/800 workAmount on 1.6 source; synthetic ZIP fixture gains a negative work drift case. All tests here are static. Verify Stage A/Workshop CI and then four-profile actual Pickle, C# compile, ERROR 0, season sow, grain storage behavior, artwork, old saves before release.

### GRAINS-RICE-POSTHARVEST-CORRECTION-20261008 — mandatory rice processing design

**Owner:** Grains harvest/processing. **Status:** Design corrected; production XML, localized new items/recipes, Pickle and real-game tests NOT implemented.

The author questioned why upland Vanilla `Plant_Rice` yields edible `RawRice` without any thresh/hull, and indicated the processing should be required. Investigation confirmed that direct `RawRice` harvest is only an expedient Vanilla compatibility shortcut and contradicts Grains' earlier rice processing conception. Canonical replacement design: `Plant_Rice → AMJC_RiceSheaf → [thresh] AMJC_RiceInHull → [hull] RawRice`. Retain Vanilla `Plant_Rice`, `RawRice` and all third-party Vanilla rice references, but change the plant's harvest target and provide two common grain processing bills (single and 10-bulk). Proposed baseline work amounts 15/120 and 10/80 are **not final accepted balance values**. Keep MO Straw conditional; decide optional drying with future Rice Cultivation owner (Project until split). Accepted Japanese historical crop texts must not be silently rewritten; new item/recipe display copy is JP-first and requires author review before EN/production publication. The own-spec record is `Docs/Balance/Crops/RicePostHarvestProcessing.md`; `Docs/Design.md`, seven-crop balance audit and the environmental fixture commentary now distinguish the *current unprocessed XML* from this intended design. Next run strict static/XML regressions and actual native-Bill+four-profile Pickle after implementation; old RawRice inventories must remain edible. No user relay needed for other workstreams.

### GRAINS-RICE-POSTHARVEST-IMPLEMENTATION-20261008

**Owner:** Grains production / E2E / localization. **Status:** Source implementation; full Python CI, C# compile, four-profile Pickle/ERROR-0, save migration and rendering pending.

Implemented Vanilla `Plant_Rice → AMJC_RiceSheaf → AMJC_RiceInHull → RawRice` with the shared processing benches and both individual/bulk Bills; initial work values 15/120 and 10/80, 1:1 conservation, intermediates 120-day/non-edible. Existing `RawRice` remains untouched. MO-only threshing generates `DankPyon_Straw`, Base cannot reference it. Approved Japanese copy is carried into new JP DefInjected and paired English defaults; rice crop description is narrowly aligned. Four-provider Pickle source covers native harvest, real bulk thresh, real bulk hull, Vanilla simple meal and CCTO coexistence without altering profile scenario count. Existing AMJ millet art is temporary; dedicated rice art waits for runtime validation. The historical pre-split MO fixture is not modified. Canonical design/balance: `Docs/Balance/Crops/RicePostHarvestProcessing.md`, `Docs/Balance/Crops/SevenGrainFoodChainAudit.md`. Do not remove About MO dependency or claim game validation/release until runtime gates pass.


**GRAINS-RICE-POSTHARVEST-QA-20261008:** Additional protection for the shipped rice processing source: §10 exact Japanese/English localization parity for two ThingDefs and four RecipeDefs (including four bilingual jobStrings), plus negative drift tests; Pickle loaded contracts now require the precise MO Straw Def and 1×/10× counts rather than accepting any second coproduct. Historical 38 MO contracts remain immutable. Full CI and four-profile C#/Pickle still separate; no gameplay balance/art/dependency changes.


**GRAINS-AUTOMATED-GATES-FIX-20261008:** Prepared targeted remediation for uploaded `automated-gates(2).log` errors: mood ThoughtStage empty description, invalid meal texture/stack graphic class, inherited double rottable (retain four standard meal comps and 2.5-day expiry), and overly strict empty 15×15 fixture search. CCTO-only duplicate local/Workshop installation is resolved by choosing a local copy in the test manifest, without modifying either installed copy or player ModsConfig; any other duplicate remains an error. Deterministic/negative Python and synthetic four-profile PowerShell tests expanded. This is a source correction, **not** a claim that the real 4×6 Pickle/ERROR-zero gate has passed.


**CI follow-up on automated-gates fixes (2026-10-08):** GitHub Actions run 37733027245 confirmed two failing negative tests were not guarded because the refreshed chain validator omitted the meal-comp and graphic assertions; restored those assertions and fixed the now-changed 2.5-day XPath in an existing negative test. Windows synthetic duplicate CCTO provider passed source resolution, but its manifest assertion hit PowerShell cast/member precedence (`[string]$cctoRecords[0].Root`); parenthesized the `Root` access before conversion. Confirmed by job logs before this targeted correction; the original loaded-game four-profile gate is still pending.

### GRAINS-REAL-PROVIDER-SMOKE-PASS-20261008

**Owner:** Grains testing/release. **Status:** DONE only for fresh four-profile actual-game smoke/ERROR-zero; migration and release gates OPEN (2026-10-08 JST).

The author's `automated-gates(4).log` confirms exactly **6/6 Pickle scenarios per profile, 24/24 total, runtime ERROR 0 in vanilla / vanilla-ccto / mo / mo-ccto**, with byte-preserving stage, native production job scenarios and C# compilation (nonfatal CS1684 warnings). CCTO local provider selection worked, and the meal Texture2D/MatFrom errors from (3) are absent after the temporary packed graphic change. The authoritative acceptance boundaries are now recorded in `Docs/GrainsProfileTesting.md`; rice progression evidence in `Docs/Balance/Crops/RicePostHarvestProcessing.md`; and the overall milestone in `Docs/Design.md`. Do not request another identical smoke solely to re-establish this gate. **Still OPEN:** real legacy save migration/add-remove testing, calendar-controlled sow/cold growth, Japanese/English UI checks, finished art/normal zoom, play-balance and standalone MO-dependency release decision. The phrase “fresh migration smoke” does not constitute proof that an old user's save was migrated. No gameplay source, textures or dependency metadata changed by this documentation closeout.

### GRAINS-OLD-SAVE-CONSERVATION-CONTRACT-20261008

**Owner:** Grains save migration testing. **Status:** Read-only save XML fixture preparation and negative tests implemented; *actual legacy engine load/re-save pending*. The separate Scenarios repository continues owning New Village's scenario/faction/pawnkind migration inspector and runtime adapter. Grains owns preservation of saved `AMJC_` crop/food/equipment things, Vanilla `Plant_Rice` / `RawRice`, and persisted AMJC processing/cooking Bills across **same packageId** old-Core -> current Grains, with MO retained. `Scripts/grains_save_contract.py` preserves original .rws bytes, records claimed SHA/version/source IDs in a new evidence directory and compares paused-save snapshots with strict IDs/quantities/bills/ticks/mod sets. Reject missing required grain/rice witnesses and test-package aliases. No source save mutation, provider removal, Def renaming or gameplay source changes. `Tests/test_grains_save_contract.py` uses synthetic XML, added as a separate Stage A CI step. This is **not** a real save engine adapter, successful actual migrated save, nor confirmation of release readiness; further work requires a genuine old .rws from an older production Core and an installed-game production-ID isolated load/re-save + every-ERROR 0 gate. The 4×6 fresh smoke gate remains DONE.

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

### RULE-AUDIT-20261008 — operating-rule consolidation

**Owner:** Project common rules; this repository retains its local specification and gates.
**Status:** SOURCE RESTRUCTURED; validation/publication evidence is recorded in Project `Docs/RuleAudit.md` and actual commit/CI results, not inferred here.

AGENTS now routes through Project `Docs/SharedRules.md` stop conditions and task procedures. New development requires VE and non-VE source/evidence comparison plus a justified implementation decision. Static/runtime/specification/distribution/publication remain separate states. Historical records below/above retain their original scope; this entry does not reopen paused work, change gameplay/dependencies/art/versions, or supersede owner runtime/release blockers. Main-only Coordination means one authoritative integrated log, not deleting branch snapshots. No Steam/2game update is claimed.

### ART-GRAINS-GENERATOR-20261009 — Grains-specific grain/crop image generation entry point

**Requested by:** author (2026-10-09 JST)  
**Owner:** Art/tooling / Grains  
**Status:** CORRECTED SOURCE IMPLEMENTATION — paid API path removed; no image accepted by this work

The initial implementation called the OpenAI image API and therefore would have created separate API usage/cost outside the ChatGPT subscription. The author rejected that design. It is superseded.

Current source keeps `Scripts/Art/grains_image_generator.py` as a deterministic **prepare/review** entry point only. `prepare` resolves and hashes the registered accepted AMJ references, caller-supplied subject identity and applicable real Medieval Overhaul reference, then writes `prompt.txt`, an exact-byte reference bundle, `manifest.json`, and `generation-request.json`. The actual image is generated once with ChatGPT's built-in image generation outside the Python process. `review` then stages that PNG byte-for-byte, runs existing generated-asset QA plus relative 64 px complexity comparison, creates the review sheet, and hands boxed contents to the existing boxed-resource preparer. The script contains no `OPENAI_API_KEY`, OpenAI API endpoint, image-API request, or automatic retry/batch loop.

Because in-chat image generation displays its result immediately, this no-extra-API-cost route cannot claim private pre-display screening. The generated image remains an immediately visible, not-yet-vetted draft until `review` and semantic comparison complete, per the shared Project texture pipeline. Candidate/work output remains blocked from `Textures/`, `Art/Sources/`, and `Docs/References/`. No gameplay XML, Def paths, production PNGs, dependency metadata, Workshop payload, or publication state changed.
