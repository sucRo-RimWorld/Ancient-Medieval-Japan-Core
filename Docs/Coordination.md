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

### AMJ-020 — More Mushrooms compatibility candidate recorded

**Requested by:** author (2026-10-04 JST)  
**Owner:** Content design / Compatibility  
**Status:** DONE (design recording only; adoption and compatibility remain unverified)

The author asked to record More Mushrooms (Workshop `3813323629`) as a possible substitute for AMJ-owned mushroom additions. Durable notes are now in `Docs/Design.md`: prior-mod audit, Hunting & Gathering scope/conclusion, and compatibility candidates.

If MO + More Mushrooms provides the required mushrooms and works correctly, prefer optional compatibility patches over duplicating plants, ingredients, or artwork. Candidate adjustments include historically appropriate cultivation, disabling hydroponics, wild gathering where appropriate, and MO food/category integration. CCTO temperature support and Environment distribution are proposed responsibilities only; no counterpart repository implementation or adoption is claimed. The existing normal-AMJ coexistence policy and conditional-dependency audit still apply. This adds no Core Alpha/Stage requirement.

**Next action:** when mushroom design resumes, audit current 1.6 source/packageId/DefNames and automate MO coexistence/load/harvest/ingredient checks before deciding adoption or patch ownership. No runtime PASS or supported-mod claim is established by this documentation change.

**Result / references:** `Docs/Design.md` → More Mushrooms prior-mod audit / Hunting & Gathering / 評価待ちの互換候補.


### AMJ-005 — Shared millet post-harvest graphics

**2026-10-04 author acceptance:** The latest in-game screenshot confirms the thicker-outline mature Awa and RawMillet sheaf render correctly. The author provisionally accepted this state ("一旦これでいいかな"). The requested texture-loading repair and outline refinement are complete; no further image edit or manual visual check is pending for this slice. This is human runtime/appearance confirmation, not a Pickle PASS.

**2026-10-04 runtime confirmation / outline refinement:** The author's screenshot confirmed the recovered sheaf renders correctly in game, resolving the question-mark defect. The author subsequently requested thicker outlines for mature Awa and RawMillet to match MO wheat. Local image-edit replacements now update the mature PNG and all three RawMillet stack slots; immature Awa, hull/edible textures, XML paths and gameplay data are unchanged. Both Stage A static validators PASS. No new Pickle runtime PASS is claimed. The later screenshot confirmed and provisionally accepted this outline weight.

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** DONE

Awa, Hie, and Kibi intentionally merge after harvest into the shared chain:
`AMJC_RawMillet` → `AMJC_MilletInHull` → `AMJC_Millet`.

These three ThingDefs now use AMJ-owned item graphics. Because they are shared by all three millet crops, their final art should be produced once as part of the shared millet chain rather than separately for each crop.

The same locked AMJ art rules apply, with item icons flatter than plant art and with fewer/shallow shadows than the accepted plant asset.

The already approved 2026-10-03 post-harvest artwork has now been isolated into production candidates for all three shared millet states. The in-game size/readability check passed, but the warm-gold pile used for `AMJC_RawMillet` was identified as semantically wrong: the harvested state is still stalks + seed heads and should read as a sheaf/bundle, not loose grain. Brown `AMJC_MilletInHull` and pale `AMJC_Millet` remain acceptable.

Each ThingDef now keeps its existing `Graphic_StackCount` behavior and points to an AMJ-owned texture directory. Three stack-count slots (`a/b/c`) are present for each state; this first integration uses the same approved pile silhouette in all three slots so the game check can focus on texture resolution, scale, and UI/map readability without introducing new unapproved art variation. Static validators now assert the exact paths plus all nine 256×256 PNGs.

**Naming decision:** harvested stalk+head grain states use the `～束` convention. `AMJC_RawMillet` is displayed as `雑穀束` / `millet sheaf`; `(生)` is not used for grain processing states. MO `DankPyon_RawWheat` receives the Japanese display override `小麦束` for the same reason. Internal DefNames are unchanged.

A dedicated millet-sheaf texture was then produced in the locked AMJ/MO style and accepted by the author on 2026-10-04 JST. It preserves the same warm yellow/olive palette family and simplified broad shapes as the accepted Awa art, but now correctly depicts harvested stalks + seed heads tied as a bundle.

The first quantized 256×256 export rendered as a red question mark for `AMJC_RawMillet` while the unchanged hull and edible-millet textures still rendered normally. To isolate the image asset itself without changing Def wiring, all three `Graphic_StackCount` slots have now been replaced with the same accepted 256×256 RGBA source export, leaving paths and stack behavior unchanged.

**2026-10-04 local diagnosis / Art request:** All three RawMillet PNGs before this repair were byte-identical and corrupt. Their IDAT chunk declares 44,080 bytes, but each entire file is only 14,485 bytes. Pillow fails to decode them; the IDAT boundary/CRC and zlib stream are invalid. Hull/edible millet and both Awa PNGs decode correctly. The sheaf export in `d848a75` also fails decoding; the older `53a6b05` asset decodes but depicts the rejected loose-grain artwork and must not be restored. XML directory paths, case, extension omission, `Graphic_StackCount`, and a/b/c naming agree with the working millet states; repository patches do not overwrite this wiring.

**2026-10-04 recovered asset:** The author supplied the intact accepted sheaf PNG (1254x1254 RGBA, transparent). All three RawMillet slots are now losslessly encoded RGBA PNGs after uniform full-canvas downsampling to the established 256x256 size. No redraw, crop, palette change, XML path change, or GraphicClass change. Exported pixels match the resized supplied source exactly in all three slots. Export SHA256: 905e72d9939ab6a46aab75b86733f2903c3b0614aebc6bfd433c6d772ef606c4.

**Validation:** Python Stage A and PowerShell Stage A validators PASS; git diff whitespace check PASS. E2E now stages repository Textures and checks Unity loading of all nine millet slots plus real stack materials at counts 1, 2, and stackLimit. The normal run-tests gate was attempted, but no scenarios ran: Quickstarts AbstractQuickstart failed type resolution during mod assembly loading. The isolated runtime log also reports SteamAPI.Init failure and fixture missing-graphic/translation errors. The stalled test process was terminated (runner exit -1). No Pickle/runtime ERROR-gate PASS is claimed.

**Next action:** none for the accepted art/texture repair. Automated runtime follow-up is tracked separately as TEST-003.

**Result / references:** shared processing implementation `1429ad30c2e1de6f931a2b25a730a3e65fb60228`; art-style baseline `2d4accb0c56bff6b81497a325877d5a5dc7d7710`; source artwork user-approved 2026-10-03.

### TEST-003 — Texture integration runtime follow-up

**Requested by:** Art/graphics / texture repair
**Owner:** Testing/tooling
**Status:** DONE

The PNG integrity regressions pass in both static validators. E2E now stages AMJ textures and checks Unity decoding plus stack-material selection. The 2026-10-04 16:16 JST rerun reaches all five current scenarios and the previous fixture/texture Vanilla ERROR entries are gone; only the first crop/grain scenario still fails with a bare NullReference. Inspection shows that scenario also performs the shared millet runtime texture test. That helper previously created a Thing and dereferenced `item.Graphic` only to reach `Graphic_StackCount`; the test now resolves `Graphic_StackCount` directly from `graphicData` and calls `SubGraphicForStackCount`, preserving the intended stack-selection assertion without the unrelated Thing/style path. Human in-game confirmation of the accepted art remains separate from automated test success.

**Validation:** On 2026-10-04 JST, the author reported the latest `run-tests.bat` gate passing after the stack-graphic helper was rewritten to resolve `Graphic_StackCount` directly. Because the isolated gate now fails on any ERROR-level runtime entry, this confirms **5/5 Pickle PASS + zero runtime ERROR entries** for this follow-up. No image asset was changed by the fix.

**Next action:** none. Keep the runtime texture checks in the regular Stage A regression gate; do not expand or replace the accepted artwork as part of testing.

**Result / references:** runtime texture helper fix `2ce5ecc08ed3334c70020b0f9fcf57b7140e0288`; local 5/5 + zero-ERROR gate confirmed 2026-10-04 JST.

### TEST-002 — AMJC cold-tolerance data regression

**Requested by:** Agriculture/XML  \
**Owner:** Testing/tooling  \
**Status:** DONE

AMJC-owned crop temperature data must remain consistent across the authoritative design documents, PlantDefs, optional CCTO compatibility XML, and the final loaded Def state. This work is data-side only and does not overlap the separate art/graphics stream.

Implemented:
- GitHub/static validation checks the Awa Stage A row in `Docs/Design.md`, the Foxtail millet row in `Docs/Balance/Crops/ColdTolerance.md`, `Plants_StageA.xml`, and `CCTO_StageA.xml` for the current 8°C minimum-growth / -3°C fixed-death design;
- local PowerShell validation checks that the AMJC compatibility patch targets Awa, adds exactly one `CropColdToleranceOverhaul.ColdToleranceExtension`, uses -3°C, and does not enable dormancy;
- the isolated Pickle suite includes a fifth scenario that verifies the final loaded Awa Def contains exactly one CCTO extension with -3°C / no dormancy;
- E2E uses a developer-only CCTO XML-API fixture so AMJC tests its consumer-owned data without importing or retesting CCTO runtime behavior.

**Validation:** GitHub Stage A validation passed for commits `050f835f7ea9eeca753cda8ef96d3c85ee7f87b7` and `c0b2de1c9f07e97dda66cb07654fb56968188450`. On 2026-10-04 JST, the development-PC `run-tests.bat` gate was reported passing with the updated **5/5 Pickle suite**; because the runner only reports success after `Validate-RuntimeLog.ps1` also passes, the AMJ Core runtime ERROR gate was clean for that run.

**Next action:** none for TEST-002. Keep this regression coverage updated when Hie, Kibi, or additional AMJC crops are implemented.

**Result / references:** static-data test commit `050f835f7ea9eeca753cda8ef96d3c85ee7f87b7`; loaded-Def/Pickle test commit `c0b2de1c9f07e97dda66cb07654fb56968188450`; local 5/5 automated gate confirmed 2026-10-04 JST.

### AMJ-007 — Hie and Kibi cultivation data slice

**Requested by:** Agriculture/XML  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** DONE

Hie and Kibi are implemented from the already-approved Stage A balance and connected to the shared millet post-harvest chain. This item is data-side only; crop-specific graphics remain owned by the separate Art/graphics workstream.

- Hie `AMJC_Plant_BarnyardMillet_Hie`: growDays 6, yield 12, fertilityMin 0.5, sensitivity 0.5, growth 5–40°C, optimum 15–30°C, CCTO fixed death -2°C.
- Kibi `AMJC_Plant_ProsoMillet_Kibi`: growDays 5, yield 11, fertilityMin 0.5, sensitivity 0.3, growth 8–42°C, optimum 18–32°C, CCTO fixed death -3°C.
- Both harvest `AMJC_RawMillet` and therefore use the existing shared threshing/hulling path.
- Until dedicated graphics arrive, both temporarily reuse the accepted Awa mature/immature texture paths. No image asset is changed by this workstream.
- Static and Pickle regression coverage checks all three millet PlantDefs and all three AMJC-owned CCTO extension values.

**Validation:** GitHub Stage A validation passed on corrected commit `07d2b6faf8117c2cbf9b63c213bf21d6d478d0f1`. On 2026-10-04 JST, the development-PC `run-tests.bat` gate was reported passing with the existing **5/5 Pickle suite**. Because that runner only reports success after the repository-owned runtime ERROR scan also passes, the runtime ERROR gate was clean for this run.

**Next action:** none for the data slice. Dedicated Hie/Kibi graphics remain with Art/graphics and do not block the validated crop data.

**Result / references:** implementation `03273bfb999fc70f6e97b9deb23d5e4e74f220ba`; test-wiring correction `fa8ee2d140ce865b28072906e799b3856d9f09c8`; source-format fix and passing CI `07d2b6faf8117c2cbf9b63c213bf21d6d478d0f1`; local 5/5 automated gate confirmed 2026-10-04 JST.

### AMJ-008 — Soba cultivation and primary processing data slice

**Requested by:** Agriculture/XML  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** DONE

Implement the approved Stage A Soba role as the next data-side vertical slice.

- PlantDef: `AMJC_Plant_Buckwheat_Soba`, growDays 4, yield 8, fertilityMin 0.4, sensitivity 0.25, growth 5–35°C, optimum 12–25°C, sowMinSkill 1.
- Optional CCTO compatibility: fixed death -2°C.
- Processing path: `AMJC_RawBuckwheat` (120d) → threshing → `AMJC_BuckwheatInHull` (120d) + MO straw → hulling → `AMJC_Buckwheat` (60d).
- Conversion is 1:1 through both processing stages so the design baseline of 8 edible grain per harvest is preserved.
- Buckwheat flour is intentionally not added yet; the design requires a concrete flour-based use before creating that ThingDef.
- Existing grain-processing stations are reused. Initial work amounts match the established millet processing baseline.
- No image asset is created or modified in this workstream; temporary paths reuse existing AMJ millet/Awa assets.

**Validation:** GitHub Stage A static validation passed for implementation commit `4d5bad9a466507116c314584d3e7b20d0599c22d` and test-integration commit `c2a46a70430b7791a97a15690bc9de9b0e07788c`. Static coverage checks the Soba PlantDef, CCTO -2°C extension, 120d/120d/60d storage chain, all four processing recipes, 1:1 quantity conservation, localization, and existing MO prerequisites. On 2026-10-04 JST, the development-PC `run-tests.bat` gate was reported passing with the existing **5/5 Pickle suite**. Because the runner only reports success after the runtime ERROR scan passes, the runtime ERROR gate was clean for this run.

**Next action:** none for the Soba data slice. Dedicated Soba graphics remain separately tracked in AMJ-009 and do not block the validated data implementation.

**Result / references:** implementation `4d5bad9a466507116c314584d3e7b20d0599c22d`; automated-test integration `c2a46a70430b7791a97a15690bc9de9b0e07788c`; GitHub Actions run `37180980209` passed; local 5/5 automated gate confirmed 2026-10-04 JST.

### AMJ-009 — Soba crop/item graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

The Soba data slice uses temporary Awa/millet graphics only. Under `Docs/Design.md §12.1.2`, Soba is a separate PlantDef and its three post-harvest ThingDefs are not shared with another crop, so the **immature plant, mature plant, sheaf, in-hull grain and edible grain all require Soba-specific production art before the public Alpha**. This does not block the already validated data slice, but it does block visual completion of the Soba vertical slice.

**Next action:** Art/graphics should produce Soba-specific plant and item assets following `Docs/ArtStyle.md`, then wire them without changing the validated gameplay data.

**Result / references:** data DefNames are `AMJC_Plant_Buckwheat_Soba`, `AMJC_RawBuckwheat`, `AMJC_BuckwheatInHull`, `AMJC_Buckwheat`; current temporary paths reuse Awa/millet assets.
**2026-10-05 boxed-resource icon lock:** The author approved a dedicated empty **Japanese masu** as the canonical boxed-resource master. AMJ keeps the familiar Vanilla/MO boxed-item silhouette language, but all compatible AMJ/Vanilla/MO retextures should use the same masu treatment. The container geometry, viewing angle, rim, joinery, palette, shading and placement are fixed; only the contents change. Generate/draw contents separately and composite them into the fixed master. If whole-icon generation drifts twice, stop regenerating and use deterministic local compositing. Durable procedure: `Docs/GoldenPaths/TextureAssetPipeline.md`; visual source of truth: `Docs/ArtStyle.md`.
Canonical repository master: `Textures/Things/Item/Resource/AMJC_Shared/Masu/AMJC_Masu_Empty.png` (256×256 transparent PNG). New chats/agents should fetch this file from `main` and composite contents into it rather than regenerating the masu.


### AMJ-010 — Barley cultivation and primary processing data slice

**Requested by:** Agriculture/XML  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** DONE

Medieval Overhaul 1.6 was checked before implementation and does not define a Barley crop, so AMJC owns the Stage A Barley PlantDef and processing states rather than duplicating an MO Def.

- PlantDef: `AMJC_Plant_Barley`, growDays 10, yield 22, fertilityMin 0.5, sensitivity 0.6, growth 0–35°C, optimum 5–22°C, sowMinSkill 2.
- Cultivation requires MO `DankPyon_BasicAgriculture`.
- Optional CCTO compatibility: fixed death -8°C.
- Processing path: `AMJC_RawBarley` (120d) → threshing → `AMJC_BarleyInHull` (120d) + MO straw → hulling → `AMJC_Barley` (90d).
- Conversion is 1:1 through both stages, preserving the design baseline of 22 edible grain per harvest.
- Straw is produced at threshing, not at harvest; the MO wheat `Plant_SecondaryDrop` behavior is intentionally not reused.
- Barley flour is not added in Stage A because the current design only requires edible barley grain; later barley-specific uses can extend from `AMJC_Barley`.
- No image asset is created or modified here. The plant temporarily uses MO wheat texture paths; processing items temporarily reuse existing AMJ grain texture paths.

**Validation:** GitHub Stage A static validation passed for implementation commit `40d9914db9e1e0d9417f13a399465f61e1a3c2da` and test-integration commit `8c3da587185f8aeb868f12ca9a8d016e9364b2e9`. Coverage checks the Barley PlantDef, Basic Agriculture sow prerequisite, CCTO -8°C extension, 120d/120d/90d storage chain, four processing recipes, 22→22 quantity conservation, meal compatibility, and a local MO-source guard that fails if Medieval Overhaul later introduces a Barley-named Def. On 2026-10-04 JST, the author reported the latest development-PC `run-tests.bat` gate passing. Because the isolated gate now fails on any ERROR-level runtime entry, this confirms **5/5 Pickle PASS + zero runtime ERROR entries** with Barley included.

**Next action:** none for the Barley data slice. Dedicated Barley graphics remain independently tracked in AMJ-011.

**Result / references:** implementation `40d9914db9e1e0d9417f13a399465f61e1a3c2da`; automated-test integration `8c3da587185f8aeb868f12ca9a8d016e9364b2e9`; runtime harness/stack fix `2ce5ecc08ed3334c70020b0f9fcf57b7140e0288`; local 5/5 + zero-ERROR gate confirmed 2026-10-04 JST.

### AMJ-011 — Barley crop/item graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

The Barley data slice uses temporary MO wheat plant graphics and AMJ millet item graphics. Under `Docs/Design.md §12.1.2`, Barley is a separate PlantDef and its three post-harvest ThingDefs are not shared with another crop, so the **immature plant, mature plant, sheaf, in-hull grain and edible grain all require Barley-specific production art before the public Alpha**. This does not block the already validated data slice, but it does block visual completion of the Barley vertical slice.

**Next action:** Art/graphics should create Barley-specific plant and item assets following `Docs/ArtStyle.md`, then wire them without changing the validated gameplay data.

**Result / references:** data DefNames are `AMJC_Plant_Barley`, `AMJC_RawBarley`, `AMJC_BarleyInHull`, and `AMJC_Barley`; current temporary paths use MO wheat / AMJ millet assets.

### AMJ-016 — Hie and Kibi crop graphics

**Requested by:** Alpha visual-completion audit  \
**Owner:** Art/graphics  \
**Status:** DONE

Awa, Hie, and Kibi now have author-approved crop-specific mature and immature plant textures. The three crops retain the shared post-harvest millet chain; only their growing-plant graphics differ.

The accepted cereal baseline is now the six 256×256 transparent textures under:
- `Textures/Things/Plants/FullGrown/AMJC_Awa/` and `Textures/Things/Plants/Immature/AMJC_Awa/`;
- `Textures/Things/Plants/FullGrown/AMJC_Hie/` and `Textures/Things/Plants/Immature/AMJC_Hie/`;
- `Textures/Things/Plants/FullGrown/AMJC_Kibi/` and `Textures/Things/Plants/Immature/AMJC_Kibi/`.

Awa uses dense foxtail heads, Hie uses compact branched/drooping heads, and Kibi uses a more open branched panicle. All three use the common warm medium-dark brown outline, low information density, and simplified broad-leaf treatment recorded in `Docs/ArtStyle.md`. The final Hie immature candidate was accepted without further posture adjustment. These three crops are also the visual baseline for subsequent cereal art.

The PlantDefs point to their dedicated mature/immature paths. No crop balance or shared post-harvest Def was changed.

**Validation:** static validators cover the dedicated texture paths, PNG signatures, and 256×256 dimensions. No new Pickle/runtime PASS is claimed for this art replacement. Final normal-zoom comparison is intentionally deferred until the remaining Stage A crop art is complete, when the author will line up all crops in game for one combined visual check.

**Next action:** none for AMJ-016. Continue the Alpha art backlog with AMJ-009 (Soba).

**Result / references:** `Defs/ThingDefs_Plants/Plants_StageA.xml`; `Docs/ArtStyle.md`; accepted production textures above.

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

### TEST-004 — Isolated E2E runtime-log hygiene and source attribution

**Requested by:** Testing/tooling  \
**Owner:** Testing/tooling  \
**Status:** DONE

An uploaded Pickle report from 2026-10-04 showed 4/5 with a NullReference in the crop/Def scenario and also exposed seven ERROR-level entries generated by the lightweight E2E fixtures: missing fixture straw graphics and missing MO-only placeholder building textures. The report's scenario names also identify it as an older pre-Barley suite, so it is not valid evidence for AMJ-010.

Harness corrections:
- stage AMJC textures into the isolated target mod;
- give the MO straw fixture an explicit developer-only placeholder texture;
- apply an E2E-only patch replacing MO-only building and Barley placeholder graphics with staged AMJC textures;
- validate the actual line-oriented Player.log format in addition to structured RimLogging blocks;
- in the isolated profile, fail the automated gate on **any** ERROR-level runtime entry rather than only entries carrying an AMJC mod_id;
- emit `TestResults/Pickle/source-state.txt` containing the local Git HEAD and scenario names so uploaded reports can be tied to the exact local test source.

**Validation:** GitHub Stage A validation passed for harness cleanup `005442b2b12719cb77d4643479716f93866d444d`, explicit null-diagnostic hardening `b0ae057cc4beeea01b47c0060f4c1e3ffce2ab97`, and the Windows source-state syntax fix `962fb1cc7f741b8c6c4ee229724824b828a9f59a`. The uploaded 4/5 report is intentionally not counted as Barley validation because it contains the older "Loaded AMJ millet CCTO..." scenario name and therefore predates the current Barley suite. The 16:16 JST rerun now shows the current "Loaded AMJ crop CCTO..." scenario name and confirms the previous fixture/texture Vanilla ERROR entries are gone. It still fails 1/5 in the first crop/grain scenario with a bare NullReference from the local step assembly. Diagnostic hardening is therefore extended with explicit logical checkpoints and SHA-256 source fingerprints; the next report must show 5/5 and no ERROR-level entries other than none.

**Validation:** After the final stack-graphic test fix, the author reported the latest `run-tests.bat` gate passing on 2026-10-04 JST. The isolated runtime gate is configured to fail on **any** ERROR-level entry, so this result confirms the current five-scenario suite passed 5/5 with zero runtime ERROR entries. The earlier fixture graphics errors and bare NullReference are therefore resolved. Source attribution remains part of the harness through `source-state.txt` / SHA-256 fingerprints for future reports.

**Next action:** none. Keep the zero-ERROR isolated gate and source attribution as permanent regression infrastructure.

**Result / references:** harness cleanup `005442b2b12719cb77d4643479716f93866d444d`; explicit failure diagnostics `b0ae057cc4beeea01b47c0060f4c1e3ffce2ab97`; source-state additions `87ef581842d0a5d215aea80601a588c2c2614979`; stack-graphic runtime fix `2ce5ecc08ed3334c70020b0f9fcf57b7140e0288`; local 5/5 + zero-ERROR gate confirmed 2026-10-04 JST.

### AMJ-012 — MO wheat Stage A integration

**Requested by:** Agriculture/XML  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** DONE

Audit and integrate Medieval Overhaul 1.6 wheat without creating a duplicate wheat PlantDef.

The installed MO 1.6 source confirms:
- `DankPyon_Plant_Wheat`: growDays 12, harvestYield 28, fertilitySensitivity 0.9, Basic Agriculture prerequisite, no active fertilityMin;
- the plant uses `MedievalOverhaul.Plant_SecondaryDrop` to yield Hay at harvest;
- `DankPyon_RawWheat` is a 120-day `DankPyon_Cereal` item and therefore goes directly into MO flour/ale recipes;
- all three MO flour recipes also yield Hay;
- `DankPyon_Flour` stores for 90 days.

AMJ integration:
- keep MO's PlantDef, growth/yield/sensitivity/research and harvested `DankPyon_RawWheat`;
- set wheat fertilityMin to 0.7;
- treat `DankPyon_RawWheat` as the unthreshed wheat sheaf and remove it from `DankPyon_Cereal`;
- remove the MO harvest-time secondary Hay drop;
- add `AMJC_Wheat` as the 90-day edible grain and the only AMJ wheat state connected to `DankPyon_Cereal`;
- add 1x / 10x wheat threshing at the AMJ grain-processing stations, producing 1:1 grain + `DankPyon_Straw`;
- remove Hay from MO flour recipes because straw was already separated at threshing;
- change MO flour storage from 90 to the AMJ flour baseline of 60 days;
- leave MO/CCTO wheat temperature values owned by CCTO rather than duplicating them in AMJC compatibility XML.

**2026-10-04 local validator finding:** the first development-PC run stopped before RimWorld launch with `[FAIL] Wheat patch must remove Hay exactly once from DankPyon_CraftFlour_Manual.` The AMJ wheat Patch itself already contained exactly one Hay-removal operation for each of the three MO flour recipes, and the Python static validator had correctly verified those operations. The failure was in `Validate-StageA.ps1`: it read the XML-adapter property as `$_.xpath.InnerText`, which evaluates incorrectly for this PowerShell XML access path and made the count appear as zero. The validator now obtains the child with `SelectSingleNode("xpath")` and compares its trimmed `InnerText`. No wheat gameplay/XML value changed.

**2026-10-04 installed-MO audit finding:** after the Hay-XPath validator fix, the local gate next stopped with `Expected exactly one active MO ThingDef 'DankPyon_Flour', found 2.` This was another audit false positive rather than duplicate loaded ThingDefs. Medieval Overhaul uses the same `DankPyon_Flour` defName for both a `ThingDef` and a `ThingCategoryDef` in separate XML files. The original `Get-MoDef` helper counted files containing the raw `<defName>DankPyon_Flour</defName>` text before filtering by XML node type, so it counted both files. The helper now parses candidate XML and counts only `/Defs/$TypeName[defName='$DefName']` nodes. No AMJ or MO gameplay value changed.

**Validation:** implementation and all repository-side regression coverage are in place. Python static validation checks the canonical wheat row, AMJ wheat Patch structure, `AMJC_Wheat`, wheat threshing recipes and 28→28 quantity preservation. Local PowerShell validation audits the installed MO 1.6 source assumptions before running. The isolated Pickle fixture reproduces MO's pre-patch wheat state and the existing five-scenario suite checks the final loaded crop, threshing, flour storage, milling filter/Hay behavior, quantity preservation and meal compatibility. GitHub Actions is green for the validator fixes, including `a2679a7064bca50d05758b8385f89c635bb62479` and `ca026ad13bf153b8125927c63e829e345da80563`. On 2026-10-04 JST, the author reported the latest development-PC `run-tests.bat` gate passing. Because that runner completes only after the five-scenario Pickle suite and isolated zero-ERROR runtime gate both pass, this confirms **5/5 Pickle PASS + zero runtime ERROR entries** with the MO wheat integration active.

**Next action:** none for the wheat data slice. Dedicated wheat-grain graphics remain separately tracked in AMJ-013.

**Result / references:** validator XPath fix `a2679a7064bca50d05758b8385f89c635bb62479`; MO node-type audit fix `ca026ad13bf153b8125927c63e829e345da80563`; implementation `91141565150bdf696bac1b5915257122bcd0958e`; Python/static coverage `f0e0cc04ed9ecca58f440a40650527a51ea4cb17`; installed-MO source audit `a97d9e84fad476a13632f2c81fc160d0007aa3e2`; E2E fixture `d772e9ceb6cd1f30953ab85a3a95f11977b4f898`; loaded-Def/Pickle coverage `bc8aea41e460986209893ead9881812d6b7fe0c0`; source fingerprints `2a55d4b72efbeb9fea9b7f3165c1c20a27025f3d`; local 5/5 + zero-ERROR gate confirmed 2026-10-04 JST.

### AMJ-013 — Wheat grain graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

`AMJC_Wheat` is a new processed grain state introduced by AMJ-012. The data slice temporarily reuses the accepted AMJ edible-millet stack texture. Because `AMJC_Wheat` is a distinct player-visible ThingDef rather than a deliberately shared post-harvest state, `Docs/Design.md §12.1.2` requires a dedicated production texture before the public Alpha. This does not block the already validated wheat data slice.

**Next action:** Art/graphics should provide a dedicated wheat-grain texture before the public Alpha and wire only the graphic path; do not change the validated wheat processing/balance.

**Result / references:** target DefName is `AMJC_Wheat`; harvested `DankPyon_RawWheat` remains the MO wheat-sheaf asset/display override.

### AMJ-014 — Natural-soil ownership and Stage A fertility integration

**Requested by:** Agriculture/XML / Core design  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** DONE

Core's older design still claimed ownership of low-fertility natural Terrain and Hilliness-linked generation, but Environment has already implemented and validated that responsibility as ENV-004.

Reconciled ownership:
- Environment owns naturally generated soil TerrainDefs/distribution and all Hilliness/world-generation changes;
- Core owns crop `fertilityMin` / `fertilitySensitivity`, processing and other crop balance;
- Environment Alpha uses one additional growable `AMJ_ThinSoil` at fertility 0.50, reusing Gravel 0.70 / Soil 1.00 / SoilRich 1.40 and intentionally not adding a 0.40 tier;
- Core does not duplicate `AMJ_ThinSoil` or add a natural-soil/worldgen GenStep;
- Soba's `fertilityMin=0.4` remains a crop property / compatibility floor, not a requirement for an Environment 0.40 terrain.

At the shared 0.50 integration point, Stage A intent is: Soba/Kibi/Awa/Hie/Barley sowable, MO Wheat not sowable; growth-factor ordering Soba 87.5% > Kibi 85% > Awa 80% > Hie 75% > Barley 70%.

**Validation:** Core design ownership is reconciled and automated coverage is added. Python/static, PowerShell and loaded-Def Pickle tests lock fertility 0.50 as the cross-repository integration point: Soba/Kibi/Awa/Hie/Barley are sowable, MO Wheat is not, and the growth-factor order is Soba 87.5% > Kibi 85% > Awa 80% > Hie 75% > Barley 70%. GitHub Actions passed for design reconciliation `c841b66547f51af79743a72d3db20d38b7345816` and regression coverage `201bbe90aa92a0d2d55ac9d1d16c92bdf6f28c11`. On 2026-10-04 JST, the author reported the latest development-PC `run-tests.bat` gate passing; therefore the same loaded-Def assertions passed in the **5/5 Pickle suite with zero runtime ERROR entries**. Environment's terrain placement/runtime validation remains owned by ENV-004 and is not duplicated here.

**Next action:** none. Keep fertility 0.50 as the permanent Core↔Environment contract test point unless the Environment soil design is intentionally revised.

**Result / references:** Core design reconciliation `c841b66547f51af79743a72d3db20d38b7345816`; Core fertility regression coverage `201bbe90aa92a0d2d55ac9d1d16c92bdf6f28c11`; Environment coordination alignment `7a1d59288eca9b42c2dfd4573295d981177c9a7d`; Environment source of truth remains ENV-004 / `Docs/Design.md §10`; local 5/5 + zero-ERROR Core gate confirmed 2026-10-04 JST.

### AMJ-019 — Post-Stage-A roadmap: fiber before oil

**Requested by:** author / Core design  \
**Owner:** Core/design  \
**Status:** DONE

After Stage A, prioritize **beans → fiber → root crops → paddy rice**. Hemp and ramie move ahead of oilseed work, including their shared bast-fiber category and connection to MO spinning/paper infrastructure.

Oil extraction is no longer part of the Core progression roadmap. Perilla and other oil crops are not rejected permanently, but their Core inclusion is now **on hold**; do not add them merely to create an oil chain. If perilla later has a distinct seed-food role it may return as a Core crop, while pressing/oil production belongs with the feature that actually consumes the oil (food/preservation/fermentation/materials etc.).

**Next action:** after the Stage A public-Alpha art gate, treat Azuki/Soybean as the bean stage, then design the hemp/ramie fiber stage before root crops or paddy work. Do not start an oil-processing stage unless a concrete downstream gameplay use justifies it.

**Result / references:** oil/fiber priority update `b6466d9c9d0af32869271fe2c8e9373ec428ef8d`; formal Core Stage roadmap `29ad9ac7c82d8c1d240a933f7bec7f41f3474687`; future-candidate section aligned to Stage B〜E in `08d7779dd5107008c58f22b44e9c432d3bf5dd37`.
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
### AMJ-015 — Core standard Scenario: 新しい村

**Requested by:** Core/design / Testing/tooling  
**Owner:** Core/design / XML / Testing/tooling  
**Status:** DONE

**Implementation progress (2026-10-04 JST):** The author selected five starting pawns from eight candidates and a minimal life-foundation research set. The concrete Alpha contract is now in `Docs/Design.md`: `AMJC_NewVillage`, dedicated Medieval player faction `AMJC_PlayerVillage`, ordinary Human pawn kind `AMJC_Villager`, Standing arrival, exactly `DankPyon_Lumber` / `DankPyon_RusticFurniture` / `DankPyon_BasicCooking` completed through Scenario parts, and explicitly empty faction research/techprint tags. Backgrounds is not required. Vanilla/MO Scenario/Faction/PawnKind definitions are not patched.

The first supply balance is 60 MO rations, 200 edible millet, 100 millet sheaf, herbal medicine 20, processed wood 200, raw wood 200, iron 30, cloth 80, silver 150, two short bows, two iron knives and one wooden club. No animals, scattered extras, buildings or components. Individual skill/trait/age selection remains normal. Research and supply details are implementation choices for the selected minimal-start direction; adjust after start-feel review if needed.

Implemented XML, Japanese Scenario/Faction/PawnKind text, bilingual keyed start dialog, public descriptions/save limitations, and two Pickle regressions. The existing five-scenario suite becomes seven. The second new regression selects the actual production Scenario via `@quickstart:AmjNewVillageQuickstart`, with no initial-condition overrides, and checks map/pawn/faction/research/item/stuff state plus early processing access. Its MO references use the existing lightweight XML-fixture architecture; it is not a full MO Harmony integration test. Both build branches include `NewVillageSteps.cs`, all MO fixture Def XML is staged, the summary requires 7/7, and the isolated fail-on-any-ERROR gate remains mandatory.

**Pre-runtime validation:** Python Stage A + New Village static validation PASS; supplied MO 1.6 and versioned RimWorld Core Def XML reference audit PASS; repository/localization XML parses; diff whitespace check PASS. Native Scenario/PawnKind structure and the `defaultFactionDef` field were checked against 1.6-format Defs and game-code structure (the former `defaultFactionType` is a load alias).

**2026-10-04 runtime report / fixture repair:** `report(4).zip` from source `6475a470885e4b67d6c03a2f37796753fa2ef5ae` confirms C# compilation/start execution and 7/7 Pickle PASS, but the overall gate correctly fails on one Vanilla ERROR: `Collection cannot init: No textures found at path Things/Item/Resource/WoodLogs`. The new raw-wood fixture introduced this unavailable collection path; it now uses the existing staged `E2E/Placeholder` with `Graphic_Single`, like other MO fixture items. Static regression checks all explicit MO fixture graphics against that staged single-texture contract. Production Scenario/supplies/graphics are unchanged. The author also observed a brief missing-image cross; no report screenshot exists, so its identity is unconfirmed. A clean runtime ERROR-gate rerun is still required; retain IN PROGRESS.

**2026-10-04 local parser failure:** The first author run stopped before validation/game launch with mojibake and cascading parser errors at `Validate-NewVillage.ps1:99`. The new script contained Japanese literals in UTF-8 without BOM; Windows PowerShell 5.1 interpreted those bytes through the ANSI code page. It is now saved with a UTF-8 BOM. Other repository PowerShell scripts were audited and are ASCII-only. Stage A CI now rejects non-ASCII `.ps1` files without a BOM and includes a Windows PowerShell 5.1 parser job for all scripts. Source-encoding policy is documented in `Docs/DevelopmentTools.md`. The full local seven-scenario runtime gate remains pending; this fix does not establish a runtime PASS.

**2026-10-04 first seven-scenario runtime failure:** The first post-parser-fix local run reached RimWorld but the fail-on-any-ERROR gate stopped on `Collection cannot init: No textures found at path Things/Item/Resource/WoodLogs`; the author also saw a missing-texture marker during startup. This came from the developer-only `DankPyon_RawWood` MO fixture, which referenced MO's production texture path even though the isolated fixture only stages `E2E/Placeholder`. The fixture now uses that staged placeholder with `Graphic_Single`; production Scenario/Defs and real MO integration are unchanged.

**2026-10-04 final runtime validation:** After pulling the fixture correction, the author reported the normal `run-tests.bat` gate passing. The gate requires all seven Pickle scenarios and then runs `Validate-RuntimeLog.ps1 -FailOnAnyError`, so this confirms **7/7 Pickle PASS + zero ERROR-level entries in the isolated runtime log** for the New Village integration. The Scenario implementation and its automated runtime coverage are therefore complete.

**Handoff (2026-10-04 JST):** Stage A dry-field agriculture data work is effectively complete for the six Alpha crops. Awa/Hie/Kibi/Soba/Barley and MO Wheat are implemented with primary processing, CCTO integration where owned by AMJC, fertility-role coverage, and the current five-scenario automated gate. AMJ-012 (MO wheat integration) and the Core↔Environment fertility contract were locally confirmed with 5/5 Pickle PASS + zero runtime ERROR. Remaining crop-specific graphics stay in the separate Art/graphics stream and do not block data-side work.

The initial public Alpha remains scoped to **dry-field / millet agriculture**. Paddy-rice work belongs to later Stage E design and should not be started as the next data slice.

The next non-art Alpha requirement identified in `Docs/Design.md` is the **Core standard Scenario**. The current design only defines the concept:
- at least one Core Scenario;
- ordinary people leave their former community and establish a small new village;
- not a warlord / daimyo / privileged-class start;
- must work without AMJ Backgrounds;
- may integrate with AMJ Backgrounds later;
- working title: **「新しい村」**;
- starting pawn count, starting materials and research state are still intentionally undecided.

Pre-timeout investigation:
- Medieval Overhaul ScenarioDefs provide usable XML structure examples such as `DankPyon_TavernOwnerStart`, `DankPyon_MercenaryStart` and `DankPyon_LoneWolfStart`.
- MO examples use `ScenPart_ConfigPage_ConfigureStartingPawns`, `ScenPart_PlayerPawnsArriveMethod`, `ScenPart_StartingThing_Defined`, optional starting animals/scatter parts, and a start dialog.
- Do **not** copy MO start balance blindly: the sampled MO starts include large amounts of silver/iron/components and specialized faction/start assumptions that are not automatically appropriate for AMJ's ordinary-village premise.
- Investigation timed out while checking the correct RimWorld/MO 1.6 player-faction choice and appropriate starting-material baseline; no ScenarioDef implementation was committed.

**Next action:** none for implementation/runtime validation. Any later manual check is limited to Japanese start UI readability and start feel/balance, and should be treated as tuning rather than a blocker. Rice remains Stage E, not the next data task.

**Result / references:** authoritative start contract: `Docs/Design.md` → Core標準Scenario. Implementation: `Defs/Scenarios/Scenarios_NewVillage.xml`, `Defs/FactionDefs/Factions_PlayerVillage.xml`, `Defs/PawnKindDefs/PawnKinds_Villager.xml`. Static checks: `Tests/validate_new_village.py`, `Scripts/Validate-NewVillage.ps1`. Runtime start coverage: `Tests/E2E/NewVillageSteps.cs`, `AmjNewVillageQuickstart`, `stage-a.feature`. Fixture texture correction: `83f25a4d91c8a39b327e5c4b7ba5f9dbf043af34`. Local **7/7 Pickle PASS + zero runtime ERROR entries** confirmed 2026-10-04 JST; the pre-implementation handoff below is retained as history.

Add new items using the following form.

### AMJ-XXX — Short title

**Requested by:** <workstream/chat/repository>  
**Owner:** <workstream>  
**Status:** OPEN

Context, constraints, and exact question/request.

**Next action:** concrete next step.

**Result / references:** add commit SHA, PR, design section, or other durable reference when available.

## Completed handoffs

### AMJ-004 — Awa plant graphics

**2026-10-04 author-requested replacement:** The author supplied a recovered sheet containing immature (left) and mature (right) Awa and approved removal of surrounding semitransparent haze. ImageGen extracted the two plants onto transparent backgrounds; the resulting assets were downsampled to 256x256 RGBA and replaced the existing immature/mature PNGs. These are image-edit outputs, not byte/pixel-identical crops of the supplied sheet. Existing Graphic_Random directory paths and plant XML remain unchanged. Hie, Kibi and temporary Soba graphics also reference these Awa paths, so they receive the replacement as well. Python and PowerShell Stage A validation PASS. The author subsequently confirmed the in-game plant rendering by screenshot and provisionally accepted the current mature outline. Automated runtime coverage is tracked separately as TEST-003.

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** DONE

The Awa cultivation/balance slice and shared grain-processing path are validated. Per the vertical-slice workflow, replace the temporary MO wheat mature-plant graphic before moving on to the next crop.

Art target:
- **AMJ visual style is now locked**; the durable reproduction rules are in `Docs/ArtStyle.md` and the palette/flatness swatch is `Docs/References/AMJ_ArtStyle_Palette.svg`;
- the approved direction is the user-accepted Awa + millet-item set from 2026-10-03, produced after direct comparison with MO wheat and leather/hide;
- future art must use MO, not RimWorld Vanilla, as the flatness/information-density baseline;
- full-grown Awa / foxtail millet only for this step;
- transparent background, clear small-size silhouette, RimWorld 3/4 top-down readability;
- simplified vector-like shapes with restrained shading, matching the general information density and outline weight of Medieval Overhaul plant art without copying its wheat silhouette;
- visibly distinct foxtail seed heads: narrow cylindrical/bristled panicles rather than wheat ears;
- warm yellow-gold mature panicles with muted green leaves/stems;
- one production texture first; immature art remains the existing temporary MO wheat placeholder until the mature graphic passes an in-game appearance check.

The accepted mature Awa art has now been exported as a 256×256 transparent PNG and stored at `Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png`. The first map test showed a missing-texture marker. Moving the file into an MO-like `Graphic_Random` directory layout was not sufficient: the Info card could still resolve an image while mature plants on the map rendered as red question marks.

A second in-game test showed mature plants still rendering as red question marks, and switching the PlantDef to `Graphic_Single` also made the immature stage disappear. Re-checking the actual MO 1.6 source confirmed that wheat uses `Graphic_Random` with a directory path (`Things/Plants/FullGrown/WheatPlant`) and a separate `immatureGraphicPath`. The earlier switch to `Graphic_Single` was therefore reverted.

The actual image bytes were also audited. The PNG blob previously committed to GitHub did not match the approved local export, so the repository texture has been replaced with a freshly encoded 256×256 palette PNG generated from the approved flat Awa asset. CI/local validation now checks the PNG signature and 256×256 IHDR dimensions in addition to the MO-style `Graphic_Random` wiring. The immature stage remains the MO wheat placeholder by design.

The first mature-art comparison beside MO wheat was acceptable, but a final refinement was requested before locking it: preserve the accepted mature silhouette, reduce its on-canvas size to roughly 90%, and shift the outline from near-black toward the warmer yellow-brown/ochre family seen in MO wheat. That revised mature texture is now wired in.

A dedicated immature Awa texture has also been added. It uses the same warm outline/palette family. The PlantDef now points `immatureGraphicPath` to `Things/Plants/Immature/AMJC_Awa`; the MO wheat placeholder is removed.

The first in-game comparison showed the immature Awa silhouette was noticeably too small relative to both mature Awa and MO wheat. The accepted immature image was enlarged to approximately 120% of its previous visible size while preserving its existing shape, palette, and outline treatment; the 256×256 texture canvas remains unchanged.

That 1.2× replacement then rendered as a red question mark in game even though the path and Def wiring were unchanged from the previously working immature texture. The initial diagnosis that indexed PNG encoding itself was the cause was not supported: the previously working immature asset was also an indexed-color PNG.

The replacement was rebuilt directly from the exact previously working blob `533818ce40a03f98d473821ddc2113b47531da88`: only the visible sprite was enlarged to 120% with nearest-neighbor scaling on the same 256×256 palette canvas, preserving the original palette/transparency structure. The resulting exact blob `d9a0c7425bf327c25016ef86157b8f0eabfeac54` rendered correctly in game, resolving the red-question-mark regression.

The rendered 1.2× immature Awa was still visibly too small beside surrounding vegetation and the mature stage. It has therefore…2229 tokens truncated… save compatibility. Detailed release numbers and validation evidence belong in README/development/release records; changes belong in Workshop changelogs and GitHub releases.

Durable source updated: Docs/ModDescriptionGuidelines.md. All related repositories already refer to this shared guide through AGENTS.md.

**Next action:** Use this policy for all future AMJ-related Workshop descriptions.


### DOC-003 — README and Workshop have distinct information depth

**Requested by:** author (2026-10-04 JST)  
**Owner:** Documentation/release  
**Status:** DONE (repository documentation)

README is the detailed public source of truth and may retain rationale, full values/specifications, development and validation detail. Workshop descriptions are not shortened copies of README: they should deliberately select only information needed to understand and evaluate the mod, including its purpose, key design/feature points, major supported scope, dependencies, and save compatibility, with README used for detailed reference.

CCTO is the current reference implementation of this policy: its Workshop English/Japanese copy was substantially shortened while strengthening the realism-focused balance and reusable framework positioning.

**Result / references:** shared guideline commit `3886774ee678859a2ed181df37e0fb63ed897ea7`; CCTO description commit `e6db12b27b1837161c7983c9f0db1a167dae70bd`.


### TEST-POLICY-002 — RimTest Redux / Pickle automation-first policy

**Requested by:** author (2026-10-04 JST)  
**Owner:** Testing/tooling  
**Status:** DONE (policy documentation)

The shared project policy now prioritizes RimTest Redux / Pickle automated testing and minimizes human manual tests. Durable instructions are in `AGENTS.md` and `Docs/DevelopmentTools.md`. Reproducible logic, loaded Defs, runtime behavior and release regressions should be automated; manual testing is reserved for appearance, readability and play/interaction feel. Build/static checks remain complementary, and runtime suites retain the mandatory mod-origin ERROR gate.

This documentation update does not claim new runtime coverage or a new test PASS. Existing implementation/test history remains unchanged.

**Next action:** apply this policy to subsequent feature, fix and release work; record unautomated coverage explicitly and move reproducible checks into the automated gate.

**Result / references:** AGENTS policy commit `db8b697cb4e633e5e52a128d0c980744e93018d2`; development workflow commit `c0a9603a02613f41a67a70bf2411fb18c600d33a`.


### DOC-004 — Workshop copy is authored Japanese-first

**Requested by:** author (2026-10-04 JST)  
**Owner:** Documentation/release  
**Status:** DONE (repository documentation)

For AMJ-related mods, Workshop descriptions are now written in natural Japanese first and then translated into English. README/design documents remain the factual source of truth, but the finalized Japanese Workshop text is the wording/content source for the English Workshop copy. English must not independently add or remove substantive claims.

CCTO has been updated as the reference implementation of this workflow. Its planned Vanilla Plants Expanded compatibility is also clearly separated from current support: the initial target is the 20-plant basic set rather than the full 100+ plant catalog.

**Result / references:** shared guideline commit `181bd898c18f047001b9801ad13521c3d1f6fafd`; CCTO Japanese-first restructuring `12e6d4df09d14cf90ab689d9f1bbb800beb6ebf2`; CCTO VPE follow-up `d15adeec49c6edcac23f84acf2141457043b4305`.



### AMJ-006 — Own AMJC cold-tolerance data locally

**Requested by:** author (2026-10-04 JST)

**Owner:** Balance/XML / Agriculture/XML

**Status:** DONE

AMJC owns the temperature values, design/balance tables, archived candidate ranges, Def mappings, and optional CCTO compatibility XML for AMJC-owned crops. CCTO is used as the reusable framework; it retains its own Vanilla/MO data.

Transferred the 13 confirmed fixed-value rows and 13 archived candidate-range rows from CCTO design/mapping documents to `Docs/Balance/Crops/ColdTolerance.md` without changing values. `Docs/Design.md`, README, and AGENTS now use this local source. The historical AMJ-001 recovery note explicitly points to the replacement source rather than directing future work back to CCTO.

The existing Awa native growth minimum and AMJC-side extension already follow this ownership pattern. Remaining crop rows are design values, not newly implemented Defs. Do not add patches for absent Defs or copy the CCTO framework into AMJC.

**Validation:** table preservation and Awa data alignment checked; runtime XML/C# and tests unchanged. No new RimWorld runtime test result is claimed for this documentation/data-source move.

**Next action:** use AMJC's local cold-tolerance source for each future crop slice; generic framework changes are coordinated in CCTO.

**Result / references:** `Docs/Balance/Crops/ColdTolerance.md`; CCTO source snapshot `c2c18a98a59d9018f48822c99fffc09d053e54d6`; CCTO counterpart BAL-003.

### AMJ-014 — Japanese recipe naming synchronization

**Requested by:** author (2026-10-04 JST)
**Owner:** Localization
**Status:** DONE

Audited AMJC's 68 direct label/description/jobString fields against Japanese DefInjected entries: no missing fields. Updated only AMJC_ThreshMillet.description and AMJC_ThreshMilletBulk.description from the obsolete 雑穀(生) name to the accepted 雑穀束 name recorded in AMJ-005. Quantities, recipes, DefNames, English text, and gameplay data are unchanged.

**Validation:** PowerShell Stage A static validator PASS; localization XML parses; git diff whitespace check PASS. No game UI/runtime validation claimed.

### DOC-008 — AMJ-wide historical description audit policy

**Requested by:** author (2026-10-04 JST)  
**Owner:** Documentation/localization / content design  
**Status:** DONE (policy documentation; content audits remain per-feature work)

AMJ now treats inherited Vanilla and Medieval Overhaul descriptions as historical-presentation content that must be audited rather than automatically retained. When AMJ adopts, patches, retextures, selects, or localizes existing items, plants, animals, or comparable content, descriptions are checked from the perspective of ancient/medieval Japan and rewritten when they are anachronistic, culturally mismatched, misleading, overly modern, or otherwise unsuitable.

AMJ-authored descriptions should include supported historical facts and, where supportable, a meaningful difference from modern Japan, modern use, modern distribution, or modern production. Historically unsuitable content must not be made to look authentic through invented prose; if wording cannot solve the mismatch, the content is flagged for a separate keep/replace/remove design decision.

Authoring remains Japanese-first: research/draft Japanese, obtain author approval, then translate only the approved Japanese text into English. Durable research/source rationale is retained outside Coordination.

**Result / references:** shared guideline `Docs/HistoricalDescriptionGuidelines.md` commit `ca17b37eb3cca5266d1f62a2d73f527a503d76e5`; Core AGENTS link `3a501077be572b651dcc4d646cf84fd1730b976e`; Environment application `0e1b74173eca79dde09dffa2287fc5f72a583c27`, `3b8b7c753b79951b315c2ffe31822416a31595c8`; CCTO scope/reference `5b60adbc676f35f98e6c7c9801f22846e5ebf097`.

### POLICY — Golden Path closeout after verified success

**Requested by:** author / AMJ project operations  
**Owner:** shared AMJ development policy  
**Status:** DONE

AMJ now has a project-wide completion rule for non-trivial/repeatable work: once an implementation reaches a verified successful state, the workstream must capture the successful sequence as a Golden Path before moving on. Deterministic/repetitive steps should be automated, discovered failure modes should receive regression guards when practical, and the reusable procedure must live in durable repository documentation/scripts rather than only in chat or Coordination.

Canonical shared policy: `Docs/DevelopmentGoldenPathGuidelines.md` in Core, commit `c54cefd71093edae61035b13793bee372edaa52a`. Core agent instructions reference the rule in `0cbcb28c382740db6dadb80b35bbc8bdcb5e7c6e`.

Environment and CCTO agent instructions have also been bound to the shared rule. Repository-specific Golden Paths remain owned by each repository.

### TEST-004 — Stage A CI loop from corrupted plant PNGs

**Requested by:** author (2026-10-05 JST)  
**Owner:** Testing/tooling / Art integration  
**Status:** DONE

Stage A validation runs #120–#128 repeatedly failed even when later commits only changed documentation. The failures were not caused by those documentation edits: the Python Stage A validator scans every production PNG on each run, and the Stage A millet art sequence had left invalid binary assets in `main`. The latest failure (#128) stopped at `Textures/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png` with a truncated PNG chunk. Audit of the six Awa/Hie/Kibi mature/immature production textures found current Awa mature and Hie mature structurally valid, while Kibi mature plus all three immature textures required replacement.

The repair restored only the four broken PNG blobs from the earlier same-workstream revision where those exact files had valid PNG structure/CRC, leaving the valid current Awa mature and Hie mature assets untouched. XML, crop balance, Def wiring, localization and gameplay data were not changed.

**Validation:** repair commit `0262092fa06c4578450af15c5b936fdd80156113`; GitHub Actions Stage A validation run #129 completed successfully, including both `validate-stage-a` and `validate-windows-powershell`.

**Golden Path follow-up:** PNG integrity now has a dedicated `Tests/validate_png_assets.py` gate. It scans every production texture for chunk boundaries, CRCs, complete IDAT/zlib data, valid scanlines and IEND, and reports all broken PNGs in one run. `Tests/test_validate_png_assets.py` regression-tests both truncated-IDAT and bad-CRC failures. `Docs/ArtStyle.md` and `AGENTS.md` require this gate for PNG work.

**Next action:** none. GitHub Actions runs `validate-png-assets` before `validate-stage-a`; binary texture writes must not be treated as successful until the repository-side gate passes.

**Result / references:** repair `0262092fa06c4578450af15c5b936fdd80156113`; dedicated PNG gate `c0823137002c37cc6e5f9ae69f0ea819c98e7e2a`; successful workflow run #131 (`37216862456`) with `validate-png-assets`, `validate-stage-a`, and `validate-windows-powershell` all Green.

### DESIGN-015 — AMJ共通容器（甕）の別途検討

**Requested by:** author (2026-10-05 JST)  
**Owner:** Common systems / Fermentation-Preservation design  
**Status:** OPEN — design investigation only; implementation not approved

AMJで、前近代日本の汎用「甕」を1つの共通容器として持ち、用途に応じて **貯蔵 / 保存 / 発酵** に使い分ける案を別途検討する。現時点では実装確定ではない。

優先して確認する点:
- 既存の土器・甕・Storage・Processor系Modに、同一容器を3用途で使い分けられる実装があるか再監査する
- 3機能を同時発揮させず、通常貯蔵 / 封をした保存 / 発酵仕込み中の占有、という排他的な状態切替がゲームとして有効か検討する
- RimWorld標準StorageとProcessor系の差を踏まえ、内部収納・Job/UI・腐敗処理・Framework接続の技術プロトタイプを行う
- Core所有とした場合でも、Core非必須を基本とするFermentation / Salt Preservation等との依存関係を壊さない構成を決める
- 既存Modで十分な場合は重複実装しない

Durable design source: `Docs/Design.md` section **AMJ共通容器（甕）— 別途検討する設計候補**, commit `b042e3f7e0e8d768a658fd9ae345c020cb11daca`.

**Next action:** 容器システムを扱う別作業系統で、既存Mod監査 → 最小プロトタイプ → 所有/依存設計の順に検討し、採否が決まった時点で正式仕様へ更新する。

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

### DOC-011 — Workshop generation requires actual approved-image inspection

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art direction / Workshop covers  
**Status:** DONE (workflow guard)

The previous guard still allowed a new chat to rely on text rules + SVG. That was insufficient for the author's requirement that generation first inspect an existing accepted cover and hold the common portion fixed.

The generation gate now requires:
- retrieve and visually inspect the actual approved Core cover reference before every generation;
- persistent cross-chat reference location: Library `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`;
- if the visual reference cannot be accessed, generation is blocked;
- use the approved image as the visual source of truth for shared background, title hierarchy, ornament, spacing and left/right geometry;
- prefer reference-image edit mode so the common area is preserved and only the addon name + right-side illustration change;
- compare the result side-by-side with the approved reference and reject any common-part drift.

Durable rule commits: `81a1fe37df58dea63f7591d802fad9a3ca45cc42` (`Docs/WorkshopCoverStyle.md`), `07ba16b0f74f1f995f4794d8ec980250dbe092c2` (`Docs/ArtStyle.md`).

**Next action:** every future cover must pass visual-reference retrieval → proposal → approval → preflight → reference-based generation/edit → side-by-side inspection.


### ART-TEMPLATE-001 — Pixel-exact shared component policy

**Owner:** shared art/tooling
**Status:** DONE (policy/tooling); OPEN (per-family template registration at next derivative)

Author requested pixel-identical reused parts across AMJ image families. Canonical policy: `Docs/GoldenPaths/FixedImageTemplates.md`. AGENTS, ArtStyle, texture Golden Path and cover workflow now require a hashed lossless master, binary editable mask, deterministic compositing, and zero protected RGBA differences. `Scripts/Art/fixed_template.py` implements compositing/validation; its regression test is in CI. Visual-reference editing alone is no longer sufficient.

No image was generated or replaced. Existing masu has its accepted master but needs a registered interior mask/manifest before the next derivative. Covers need a clean shared master/approved editable mask from the accepted visual reference before the next cover. Do not claim all existing assets are already pixel-locked. Species style references remain references rather than identical-species templates. Pending species proposals remain pending.
