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

The Soba data slice uses temporary existing AMJ graphics only. Dedicated art is needed for the Soba plant and, if visually useful, its post-harvest states. Do not block data validation on this item.

**Next action:** Art/graphics should pick this up after the currently active millet graphics work, following `Docs/ArtStyle.md`.

**Result / references:** data DefNames are `AMJC_Plant_Buckwheat_Soba`, `AMJC_RawBuckwheat`, `AMJC_BuckwheatInHull`, `AMJC_Buckwheat`.

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

The Barley data slice uses only temporary existing graphics. Dedicated Barley art can be produced independently after the currently active graphics work.

**Next action:** Art/graphics should create Barley plant/item assets following `Docs/ArtStyle.md`; data validation does not wait for this item.

**Result / references:** data DefNames are `AMJC_Plant_Barley`, `AMJC_RawBarley`, `AMJC_BarleyInHull`, and `AMJC_Barley`.

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
**Status:** IN PROGRESS

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

**Validation:** extend static validation, installed-MO source audit, and the existing five-scenario Pickle gate before marking DONE.

**Next action:** add regression coverage and run the normal automated gate.

**Result / references:** implementation commit follows.

### AMJ-013 — Wheat grain graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

`AMJC_Wheat` is a new processed grain state introduced by AMJ-012. The data slice temporarily reuses the accepted AMJ edible-millet stack texture and does not modify image assets.

**Next action:** Art/graphics may provide a dedicated wheat-grain texture after the currently active graphics work. Do not block wheat data validation on this item.

**Result / references:** target DefName is `AMJC_Wheat`; harvested `DankPyon_RawWheat` remains the MO wheat-sheaf asset/display override.

### AMJ-014 — Natural-soil ownership and Stage A fertility integration

**Requested by:** Agriculture/XML / Core design  \
**Owner:** Agriculture/XML / Testing/tooling  \
**Status:** IN PROGRESS

Core's older design still claimed ownership of low-fertility natural Terrain and Hilliness-linked generation, but Environment has already implemented and validated that responsibility as ENV-004.

Reconciled ownership:
- Environment owns naturally generated soil TerrainDefs/distribution and all Hilliness/world-generation changes;
- Core owns crop `fertilityMin` / `fertilitySensitivity`, processing and other crop balance;
- Environment Alpha uses one additional growable `AMJ_ThinSoil` at fertility 0.50, reusing Gravel 0.70 / Soil 1.00 / SoilRich 1.40 and intentionally not adding a 0.40 tier;
- Core does not duplicate `AMJ_ThinSoil` or add a natural-soil/worldgen GenStep;
- Soba's `fertilityMin=0.4` remains a crop property / compatibility floor, not a requirement for an Environment 0.40 terrain.

At the shared 0.50 integration point, Stage A intent is: Soba/Kibi/Awa/Hie/Barley sowable, MO Wheat not sowable; growth-factor ordering Soba 87.5% > Kibi 85% > Awa 80% > Hie 75% > Barley 70%.

**Validation:** add static and loaded-Def regression coverage for the 0.50 fertility integration point. Environment's own terrain placement/runtime validation remains owned by ENV-004 and is not duplicated here.

**Next action:** run the normal Core `run-tests.bat` after the fertility assertions are added. AMJ-014 becomes DONE after the existing five-scenario Pickle suite and zero-ERROR gate pass.

**Result / references:** Core design reconciliation commit follows; Environment source of truth is ENV-004 / `Docs/Design.md §10`.

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

The rendered 1.2× immature Awa was still visibly too small beside surrounding vegetation and the mature stage. It has therefore been enlarged by a further 120% from the known-good rendered asset, giving roughly 1.44× the original visible size while keeping the same 256×256 palette canvas and nearest-neighbor treatment. The new exact blob is `c3b9d1c98796c684fabadadc75de27e081907861`.

The final ~1.44× immature texture rendered correctly in game and its size/readability was accepted at normal zoom on 2026-10-04 JST. Mature and immature Awa plant graphics are therefore complete for this slice.

**Next action:** none for AMJ-004; move to AMJ-005 post-harvest graphics.

**Result / references:** Stage A cultivation `47ddb201ab167ac47c4af9da21d038b3096b3847`; shared millet processing completion `5fb1b15d3091d306bc59f8a5605e5496d4251afd`; mature Awa art `d515cb304531ae01debf1c6cd2ab859f9675fdf9`; texture-loading correction `b7813c846f5d3bb2c4ede99a53ca001336f77409`; final mature in-game visual comparison accepted on 2026-10-03; final immature texture commit `7f69d28a26af14ecd7311ac263bdf9dcd1ce3bb7`, accepted in game on 2026-10-04 JST.

### AMJ-003 — Shared millet threshing and hulling

**Requested by:** Agriculture/XML  \
**Owner:** Agriculture/XML  \
**Status:** DONE

Implemented and validated the shared post-harvest path used by Awa, Hie, and Kibi:
- `AMJC_MilletInHull` and edible `AMJC_Millet`;
- simple grain processing spot and full grain processing table;
- single and x10 threshing recipes;
- single and x10 hulling recipes;
- threshing outputs MO `DankPyon_Straw`; hulling preserves grain count 1:1;
- 120d raw millet → 120d millet in hull → 90d edible millet;
- raw/intermediate/final millet remain outside `DankPyon_Cereal`;
- Japanese localization for buildings, items, and recipes;
- raw millet market value corrected from the initial zero-value prototype to 1.1.

Automated validation now covers the repetitive numeric and Def-wiring checks:
- GitHub Actions runs the Stage A validator on pushes/PRs;
- local `run-tests.bat` validates repository XML against the installed MO 1.6 source, builds isolated developer-only test mods, launches RimWorld with Pickle/Quickstarts, requires a fresh clean 4/4 summary, and exits automatically;
- the validators correctly resolve RecipeDef inheritance for recipe users rather than requiring duplicate child XML.

The corrected GitHub Actions validator passes, and the development-PC local gate completed with all 4 Pickle scenarios passing. Numeric/Def-wiring smoke for this slice is therefore complete. Remaining manual checks are limited to final graphics/UI readability and processing-speed feel during normal play.

**Next action:** proceed to the next vertical slice; when the grain-processing graphics are finalized, perform only the visual/play-feel smoke rather than repeating numeric checks.

**Result / references:** implementation `1429ad30c2e1de6f931a2b25a730a3e65fb60228`; authoritative processing values `8fcc9df4851378a48bb31cef2d9852f999e38afd`; local automated runner `a2f28dc868f172e2d770ddf10239ef7ac36d899a`; inherited-recipe validator fixes `7684c45afe8b9844544320252e2e62e3ce043d57` and `a63fc75869597e3bd327340c625109a26e875c70`; batch argument fixes `708ea9e39b21765504002afe8d673b5434822ce4` and `f0961acc5c317577f4d5b3f64976ef405bc93cfb`; passing GitHub Actions run `37116278412`; local Pickle result 4/4 pass.

### AMJ-002 — Stage A Awa cultivation vertical slice

**Requested by:** Core/design  \
**Owner:** Agriculture/XML  \
**Status:** DONE

The first executable AMJ Core slice covers the Awa / foxtail millet cultivation-and-harvest path.

Implemented on `main`:
- initial `About/About.xml` with packageId `sucro.ancientmedievaljapan.core` and required Medieval Overhaul dependency;
- `AMJC_Plant_FoxtailMillet_Awa` with Stage A values;
- shared unthreshed harvest `AMJC_RawMillet`, inedible and 120-day storage, deliberately excluded from `DankPyon_Cereal`;
- optional CCTO extension for fixed cold death at -4 C;
- Japanese DefInjected labels/descriptions;
- temporary MO wheat/raw-wheat graphics pending the final-art step.

Runtime smoke was completed in game. The Awa Info Card showed growDays 6, fertilityMin 50%, fertility sensitivity 40%, growth range 8–42 C, harvest yield 13, and CCTO cold-death temperature -4 C. Harvest produced `雑穀(生) x13`; the item Info Card showed `AMJC_RawMillet`, AMJ Core as the source, and the expected rottable behavior. This validates the cultivation/harvest slice and confirms that the CCTO extension is loaded through the AMJ compatibility patch. CCTO's underlying fixed-threshold runtime semantics were already validated in the CCTO project and are not duplicated in AMJ.

**Next action:** implement the shared grain primary-processing slice (threshing + hulling) before adding Hie/Kibi, so the three millet PlantDefs can converge on the same complete post-harvest path.

**Result / references:** implementation commit `47ddb201ab167ac47c4af9da21d038b3096b3847`; identifier/source-of-truth update `c909843999ec5d9e2e850404a709a354d56610a4`.

### AMJ-001 — Stage A crop balance baseline recovery

**Requested by:** Core/design  \
**Owner:** Agriculture/XML  \
**Status:** DONE

Recovered the previously confirmed Stage A balance values for the six first-Alpha field crops (Awa, Hie, Kibi, barley, MO wheat, buckwheat) from repository history and reconciled them with the current MO-required / standalone-CCTO architecture.

The restored authoritative design now includes:
- growDays;
- final edible-grain yield baselines;
- fertilityMin / fertilitySensitivity;
- growth-temperature design values;
- sowMinSkill and research unlocks;
- grain processing/storage tiers;
- CCTO-compatible fixed cold-death temperatures, using CCTO only when installed rather than duplicating its C# framework in Core.

Historical design references used for recovery include `9b6807b48cf43da50a70caf1a99a5989391473ca` (growDays), `768665413e70ad7451b6b2255c67eb349ea32099` (yield/fertility/temperature), `33430521c97e22e2a52fe1ca661deeb6faf5c025` (skill/storage), and `36f271de4d82162fb002922bbb295ae5f68f31ae` (later grain-processing/storage structure). At recovery time the AMJC values were sourced from CCTO `Docs/ImplementationTable.md`. Ownership was subsequently corrected in AMJ-006: the current source is AMJC `Docs/Balance/Crops/ColdTolerance.md`, aligned with the cultivation design and AMJC compatibility XML. Do not use CCTO as the AMJC plant-data source.

**Result / references:** `Docs/Design.md` commit `f8190ecdaf5ca2d2313e54496b928f8eb66b5685`.

### TEST-001 — AMJ-wide runtime ERROR gate

**Requested by:** project-wide automated-test policy  
**Owner:** testing/tooling  
**Status:** DONE

AMJ automated tests that launch RimWorld must treat repository-owned ERROR-level runtime log entries as test failures even when the scenario count itself passes.

AMJ Core E2E now:
- redirects RimWorld/Unity runtime output to isolated `TestResults\Pickle\Player.log`;
- validates the normal 4/4 Pickle summary;
- then scans the isolated log for ERROR entries attributed to AMJ Core / the staged E2E target;
- fails the overall gate when such an ERROR exists.

Implementation: `9bb1038691147f0ea1046aa206332374217ec3f9`, `dbccb4f92053c14869a11bcf4079b3954a0e41a3`, `c6eed6b1f862e2def624db8998a2884f7c38318e`, `0ed52c49a1bb4cf5542a0f97b99d62964dae0538`.
Project-rule commits: `7e8e3229bf3d05e3a747a3a94b4e6d160b69ece7`, `990d329456126ceb1291a5c2d76a04c327d0d03e`.


### DOC-001 — Shared public-description format and save compatibility

**Requested by:** author / public-description policy (2026-10-04 JST)  
**Owner:** Documentation/release  
**Status:** DONE (repository documentation)

All AMJ-related mod descriptions must include save compatibility. CCTO is the evolving format baseline. Durable shared policy: [Docs/ModDescriptionGuidelines.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Core/blob/main/Docs/ModDescriptionGuidelines.md). Addition/removal safety must reflect each mod's actual implementation; custom content and world-generation mods do not inherit CCTO's safe-removal claim.

About.xml now states the development build's save-compatibility limits; AGENTS.md points to the shared policy for future README/Workshop preparation.

**Next action:** Use the shared CCTO-based format when preparing the public description; verify save addition/removal before making stronger claims.


### DOC-002 — Workshop descriptions omit detailed versions and test results

**Requested by:** author (2026-10-04 JST)  
**Owner:** Documentation/release  
**Status:** DONE (repository documentation)

The shared public-description policy now omits detailed mod version numbers, Version sections, and test counts/results from Workshop descriptions. Keep the supported RimWorld version and Alpha/Beta stage, features, dependencies, supported content, and save compatibility. Detailed release numbers and validation evidence belong in README/development/release records; changes belong in Workshop changelogs and GitHub releases.

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
