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

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** IN PROGRESS

Awa, Hie, and Kibi intentionally merge after harvest into the shared chain:
`AMJC_RawMillet` → `AMJC_MilletInHull` → `AMJC_Millet`.

These three ThingDefs still use temporary MO item graphics. Because they are shared by all three millet crops, their final art should be produced once as part of the shared millet chain rather than separately for each crop.

The same locked AMJ art rules apply, with item icons flatter than plant art and with fewer/shallow shadows than the accepted plant asset.

The already approved 2026-10-03 post-harvest artwork has now been isolated into production candidates for all three shared millet states. The in-game size/readability check passed, but the warm-gold pile used for `AMJC_RawMillet` was identified as semantically wrong: the harvested state is still stalks + seed heads and should read as a sheaf/bundle, not loose grain. Brown `AMJC_MilletInHull` and pale `AMJC_Millet` remain acceptable.

Each ThingDef now keeps its existing `Graphic_StackCount` behavior and points to an AMJ-owned texture directory. Three stack-count slots (`a/b/c`) are present for each state; this first integration uses the same approved pile silhouette in all three slots so the game check can focus on texture resolution, scale, and UI/map readability without introducing new unapproved art variation. Static validators now assert the exact paths plus all nine 256×256 PNGs.

**Naming decision:** harvested stalk+head grain states use the `～束` convention. `AMJC_RawMillet` is displayed as `雑穀束` / `millet sheaf`; `(生)` is not used for grain processing states. MO `DankPyon_RawWheat` receives the Japanese display override `小麦束` for the same reason. Internal DefNames are unchanged.

A dedicated millet-sheaf texture was then produced in the locked AMJ/MO style and accepted by the author on 2026-10-04 JST. It preserves the same warm yellow/olive palette family and simplified broad shapes as the accepted Awa art, but now correctly depicts harvested stalks + seed heads tied as a bundle.

The first quantized 256×256 export rendered as a red question mark for `AMJC_RawMillet` while the unchanged hull and edible-millet textures still rendered normally. To isolate the image asset itself without changing Def wiring, all three `Graphic_StackCount` slots have now been replaced with the same accepted 256×256 RGBA source export, leaving paths and stack behavior unchanged.

**Next action:** pull latest `main`, restart RimWorld, and verify only whether `雑穀束` now renders instead of a question mark. If it renders, judge size/readability; if it still does not, inspect the runtime missing-texture/Unity import error rather than making another blind image-format change.

**Result / references:** shared processing implementation `1429ad30c2e1de6f931a2b25a730a3e65fb60228`; art-style baseline `2d4accb0c56bff6b81497a325877d5a5dc7d7710`; source artwork user-approved 2026-10-03.

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
**Status:** IN PROGRESS

Hie and Kibi are implemented from the already-approved Stage A balance and connected to the shared millet post-harvest chain. This item is data-side only; crop-specific graphics remain owned by the separate Art/graphics workstream.

- Hie `AMJC_Plant_BarnyardMillet_Hie`: growDays 6, yield 12, fertilityMin 0.5, sensitivity 0.5, growth 5–40°C, optimum 15–30°C, CCTO fixed death -2°C.
- Kibi `AMJC_Plant_ProsoMillet_Kibi`: growDays 5, yield 11, fertilityMin 0.5, sensitivity 0.3, growth 8–42°C, optimum 18–32°C, CCTO fixed death -3°C.
- Both harvest `AMJC_RawMillet` and therefore use the existing shared threshing/hulling path.
- Until dedicated graphics arrive, both temporarily reuse the accepted Awa mature/immature texture paths. No image asset is changed by this workstream.
- Static and Pickle regression coverage now checks all three millet PlantDefs and all three AMJC-owned CCTO extension values.

**Validation:** GitHub static CI must pass on the corrected implementation. RimWorld/Pickle runtime PASS is not claimed until the development-PC `run-tests.bat` gate is rerun.

**Next action:** run `run-tests.bat`; if the existing five-scenario suite passes with a clean runtime ERROR gate, mark the data slice DONE. Art remains independent.

**Result / references:** implementation `03273bfb999fc70f6e97b9deb23d5e4e74f220ba`; test-wiring correction `fa8ee2d140ce865b28072906e799b3856d9f09c8`.

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
