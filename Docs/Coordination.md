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

### DOC-PUBLICCOPY-COMMON-001 — AMJ public description wording rules

**Requested by:** author (2026-10-07 JST)  
**Owner:** Documentation/release  
**Status:** DONE

AMJ-common public-description rules were consolidated in `Docs/ModDescriptionGuidelines.md` and referenced from `AGENTS.md`. Japanese public copy should use established Japanese general terms, preserve English mainly for official names/identifiers, avoid internal engine terminology unless technically necessary, distinguish newly added content from reused/reconfigured systems, and prioritize player-visible changes over implementation or artwork provenance. README → Workshop → 2game → About.xml is the required decreasing-information hierarchy, and public-copy changes require cross-surface consistency checks.

The 2game common structure now uses `▼ 特徴`. The guideline is hosted in the Grains repository; the configured Mod display name remains Ancient & Medieval Japan Core.


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


### DOC-RULE-002 — README / Workshop summary relationship

**Requested by:** author (2026-10-06 JST)  
**Owner:** AMJ shared public-description policy  
**Status:** DONE — shared guideline updated

AMJ-wide public-description policy now treats each mod's README as the detailed public-content source of truth and the Steam Workshop description as a concise summary of that README. Workshop text may reorganize and compress for installation/selection readability, but it must not introduce substantive features, design rationale, compatibility claims, or other public facts that are absent from README.

The existing Japanese-first Workshop localization rule remains unchanged: README detailed content first → natural Japanese Workshop summary → author-approved Japanese Workshop text → English translation of that Japanese text.

**Durable source:** `Docs/ModDescriptionGuidelines.md`.

**Publication responsibility update (2026-10-06 JST):** actual Steam Workshop publication/update operations are author-manual. Agents prepare and synchronize the repository-side README, BBCode descriptions, localization and publication assets only, and must not treat Steam as updated until the author confirms it.

### LOC-RULE-001 — Japanese kanji / alias opening rule

**Requested by:** author (2026-10-06 JST)  
**Owner:** AMJ shared localization policy  
**Status:** DONE — shared rule published

AMJ-wide description policy now requires Japanese descriptions to begin with an established kanji form when one exists and to include recognized aliases / alternate names or common alternate written forms at the opening. Do not invent kanji, force uncommon ateji, or add weakly sourced names merely to satisfy the rule.

This extends, but does not replace, the existing Japanese-first workflow: draft/research Japanese, obtain author approval, then translate only the approved Japanese text into English.

**Durable source:** `Docs/HistoricalDescriptionGuidelines.md`, commit `fed314b19e3a61c88e0b93cec05d68ca6f966d67`. Core / Environment / CCTO AGENTS routing has been synchronized.

### COMPAT-CBF-001 — Custom Base Framework future settlement candidate

**Requested by:** author (2026-10-06 JST)  
**Owner:** Content design / future Factions and settlement generation  
**Status:** DONE (design recording only; adoption and compatibility remain unverified)

Recorded Custom Base Framework (Workshop `3813689040`) in `Docs/Design.md`: prior-mod audit, Factions conclusion, Japanese NPC settlement framework candidate, and pending compatibility candidates. The source-of-truth design keeps Factions at its existing later priority and schedules CBF reassessment when settlement design begins.

Potential division: CBF owns procedural assembly / editor / XML export; AMJ owns Japanese building pieces, settlement plans and content. No dependency, implementation, supported-mod claim, new Addon commitment, or runtime PASS is introduced.

**Next action:** when Factions / settlement design resumes, audit current API / package / permissions and MO / terrain / faction-generation coexistence, then prototype a small rural settlement using the existing automated runtime gates.


### ART-RULES-021 — image-rule consolidation and contents-first masu workflow
**Authoritative source-tree / Workshop exclusion update (2026-10-06 JST):** `Art/Sources/` is now the development-only source-of-truth tree for accepted masters and authoring files. The author-added empty masu PNG/XCF and dehulled-buckwheat source are retained there; the Workshop-cover SVG source has also been mirrored there without removing its reference copy. Workshop publication is fail-closed: `.workshopignore`, `_PublisherPlus.xml`, and the `git archive` staging path all exclude `Art/Sources/`. Production `Textures/` derivatives must not be relabeled as originals merely to fill the source tree; historical masters are migrated only from exact surviving source bytes. Source-archive commit `85416b6577db9188779cedf89bb1c9f853c999bd` was corrected by `6044f12f2d87a80634d5b6b80c28968a5a0e2f2f` to remove derivative copies; current Workshop exclusion/config commits: `8698bf45d7411c2997c284fa9e6f42cc390686d6`, `d48c7b2640dce065ee01842d737aae3e017698e4`, `ed1955dd248fd6311b187f228122e11d5f97a12d`, guard `5403cf64a6fdeadbe9410e098ce409e4152be12b`.

**Non-destructive source preservation correction (2026-10-06 JST):** Accepted high-resolution image masters are now explicitly immutable and stored under `Art/Sources/`; production `Textures/` PNGs are derivatives only. Resize/crop/recolor/export operations must write new files and leave the accepted source unchanged. If the exact source has not been uploaded/committed, agents must not claim it is preserved. Source commits: `ebeaca8b053fac98a7a822bf9324bb08c3667d41`, `a78495d4502d0795b6c5191ab3c5d61ef8a6a2e6`, guard `6aafbb35e656cf5603e8bc3af272271c3265da85`.


**Requested by:** author (2026-10-06 JST; rule cleanup after repeated generation/style failures)  
**Owner:** AMJ shared art policy / Core art  
**Status:** DONE — actual generation stress test completed; deterministic perspective guard green

Image rules were consolidated so routine work no longer accumulates failure-specific instructions in every entry document.

Current hierarchy:
- `Docs/ArtStyle.md` owns AMJ-wide visual language and precedence;
- asset-class style documents own only genuine class-specific visual differences;
- `Docs/GoldenPaths/TextureAssetPipeline.md` owns general generation/source/export/validation procedure;
- `Docs/GoldenPaths/FixedImageTemplates.md` applies only to intentionally reused visible components;
- family pipelines own geometry/compositing details.

Core AGENTS now routes to those sources instead of repeating boxed-resource/contact/fixed-template history. ArtStyle no longer contains masu masks, Workshop production steps, or fixed-template implementation. The fixed-template policy was reduced to generic pixel-reuse essentials.

The active boxed-resource workflow is now **contents-source generation + deterministic perspective normalization + manual composition**. ImageGen produces only the transparent material layer in AMJ style; it no longer owns the exact masu projection. `Scripts/Art/normalize_masu_contents.py` removes low-alpha generator residue and projects the material onto the shared diamond-like contents plane before manual placement/masking/occlusion against the canonical masu. The earlier v2/v3/v4 automatic contact-study remains diagnostic/research only and is no longer the ordinary production path.

Source-of-truth commits:
- AGENTS routing: `71f9f97728efefd74903fc736727804e3ae2d075`, obsolete-history removal `0fff08ee37dc972538589ad373b8d4e93c33f694`;
- shared ArtStyle separation: `3d649c7e67543d0753638a93c93ea91b02dc3a01`, `93bb24bf9869793163ae7b7eecad999331f8dea2`;
- general texture pipeline: `681d1c43692537b6967e2359505271888904ac21`, cleanup `a9bbffd6ec62e50223821d33ccdbb8530593d420`, ownership/heading normalization `f9e960c3368eb79b4e1b2e3d79c49e459289ae2a`;
- fixed-template simplification: `b1556b87832bd24f665de691fb4e8ad28e1d372b`;
- Workshop style/workflow separation: `d193c832a05d72d41110eb6798342191b2337e0e`, obsolete-style cleanup `15ec441bb8d228598b1a7b1ece772827ed71caeb`, inheritance clarification `89410d598c43318baad233ea1bc5d7dcde1e9e50`;
- boxed-resource contents-first workflow: `ce44ef823c1425def0c8fa5e4db80ec919e49e4b`, current-state cleanup `b0b9a230a5f095617fe774f65c01bf4769301335`;
- v4 manifest retained fail-closed as diagnostic-only metadata: `1252481382974a39e5a4928a1ffa5b52e1752e02`;
- reference-role / direct-perspective audit correction: `0f5005cde88c28c0724a7a962accd0097310253d`;
- deterministic contents normalizer: `8ec65c92199db30c764e2addc37ad7ce82556f58`, regression test `f66dbed535cf169576017f0e6bb347fbbfa8941d`, Stage A hook `1a2304af33cf66ed10736bfed7f4369150afc84a`;
- production-pipeline switch to deterministic projection: `d15ef5dc711288b6514958cd433bd96a4ac6fb39`, structural routing guard `3f8f9c17ebbea4141b34b278efc886cad592eb01`.

**Follow-up audit (2026-10-06 JST):** Removed the remaining boxed-resource history from shared ArtStyle, removed the brittle exact-keyword ImageGen gate, removed mandatory pre-generation approval loops, scoped Core-only sprite budgets away from Workshop presentation art, and made the current manual masu workflow explicitly outside the active fixed-template zero-difference guarantee until a stable protected region exists. Archived masu v4 automation is now manual-dispatch only and no longer blocks Stage A. Added `Tests/test_art_rule_structure.py`; Stage A also runs the Workshop fixed-template regression. Stage A at `1ff8be70debccbb9da395997eae5ae51e9a49609` passed all art-rule, Workshop-template, fixed-template, boxed-reference, PNG, Stage A, and Windows PowerShell gates.

**Actual generation stress test (2026-10-06 JST):** The approved buckwheat reference and a subject-specific Japanese short-grain-rice reference were actually viewed, then rice contents were generated rather than only auditing prompt text. Direct ImageGen attempts still produced a frontal mound / excessive per-grain modeling and did not reliably reproduce the masu opening plane. This confirmed that stronger wording alone was insufficient. A neutral material-only rice source was then passed through the new deterministic normalizer; the resulting transparent layer adopted the shared diamond-like contents plane without regenerating the masu. This is a pipeline/capability test only: no rice production icon, final masu composite, or author visual approval is claimed. Stage A run #281 for `3f8f9c17ebbea4141b34b278efc886cad592eb01` completed successfully, including the new normalizer regression.

**Line-hierarchy refinement (2026-10-06 JST):** Author selected the best of the rice-generation trials partly because it alone used a strong outer contour around the entire pile while keeping grain-to-grain boundaries thinner and lighter. This is now a durable Core clustered-resource rule in `Docs/ArtStyle.md` and an explicit boxed-resource generation/rejection criterion. Equal-weight dark outlines around every grain are rejected because they fragment the pile and increase game-scale noise. Source commits: `e450bc309d8c25b5bea5bd88b583f909241c601a`, `57dcb408b2b559ece4ac94a7bd92a5f12b24fdee`, regression guard `368e62f04b3759b0c0644e2a2900771403c86df6`.

**Opaque-outline clarification (2026-10-06 JST):** For boxed-resource contents, "lighter outline" now explicitly means a lighter **opaque RGB color**, not lower alpha. The contents outer contour must remain weaker/thinner than the wooden masu rim while staying stronger than internal piece boundaries; internal separators may be pale but likewise use opaque color. Deterministic requests such as outline lightening/thinning must edit the existing contents layer rather than send the full masu composite through ImageGen, so the fixed wooden masu cannot be redrawn. Source commits: `8ea306d04a58d66b23550a4ea7a209db259467b6`, regression guard `9c5938c45c0985addec1f251ad4fb37f239bea1b`.

**Automated generation QA (2026-10-06 JST):** First-pass generated-image checking is now automated before author review. Common production order is ImageGen/source creation → mechanical QA → deterministic family processing → agent semantic visual QA → author final visual acceptance. Reusable mechanical validator: `Scripts/Art/generated_asset_qa.py`; common baseline policy: `Docs/References/AMJ_GeneratedAsset_BaseQA.json`. Boxed resources add `Docs/References/AMJ_BoxedResource_GenerationQA.json` and `Scripts/Art/prepare_boxed_resource_candidate.py`, which runs mechanical QA, deterministic projection, post-projection structural checks, and review-sheet generation. The author-selected rice trial is stored persistently at Library `/AMJ/References/AMJ_BoxedResource_LineHierarchy_Rice_Test.png` (SHA-256 `8e808c75763e8bcd63e9826a4224044dafb4f5d8c786b28ee325641b3e229e81`) only as line-hierarchy/information-density calibration, not as an approved rice production icon. Calibration replay: the selected trial passes the registered boxed policy; the other three retained generation trials are rejected automatically (two for overly dark/heavy internal lines and one for excessive game-size color complexity). Rejected attempts are no longer ordinary author-review candidates; after up to three automatic attempts, persistent failure is reported as a capability/blocker instead. Source commits: validator `c045b3d91f7a68c8dd6f0f6f4aa4600183ea4647`, boxed policy `6b13f9633fc993523a957d048350d247e41afa25`, boxed preparation `120d2f4d9e9b49dc02d343a63fa3d4121a9c59c9`, tests `076ec04b300de4d55941e1d660c22d7345f7e74d` / `a35c356cbcb5b79e055e71364e3f74d19c63b42f`, baseline policy `1057eeee26dd9779feef87686008d91b9063aaf6`, shared workflow `be01463b25e70f34a137a532471fe6bc5baa665a`, boxed workflow `50418b09ae76980a6b1eebe3868b0a403cf81026`, routing guard `90dfa5b745a9e6328bbf118a2c2e7cf6596a753e`, Stage A hook `8ad840b81c8dfca35d18605d6b2c186e1e2922e7`.


### ART-TEMPLATE-019 — MO comparison corrections implemented as contact study

**Requested by:** author (2026-10-06 JST; 「修正して」 after MO icon comparison)
**Owner:** Art/tooling / boxed-resource icons
**Status:** ARCHIVED — retained as diagnostic/research; superseded for production by ART-RULES-021

Historical result: the **v4-contact-study** superseded earlier automatic v2/v3 experiments at the time. It is now retained only as diagnostic/research material; the active production workflow is ART-RULES-021 / `Docs/GoldenPaths/BoxedResourceIconPipeline.md`. Master and approved in-hull Soba raster bytes remain unchanged.

The registered study contract now uses conservative lower HardFixed wood, occludable ContactZone including upper front/side walls, independent ExtensionAllowed, and bulk-grain RequiredFill. The rendered source keeps the full intact master as context, and includes contents plus contact edits. The compositor restores only HardFixed exactly, rejects Forbidden RGBA changes (including transparent RGB/low-alpha) rather than clipping, and does not split rear/front or constrain extension to Soba's silhouette. Old v3 compositor entry points are removed. Both production status fields are blocked.

Explicit scaffold-study/compose-study commands provide the reviewable research path without writing into Textures or Docs/References, or overwriting registered sources. AGENTS, ArtStyle, all related Golden Paths, the manifest, scripts and tests are aligned. Durable source: `Docs/GoldenPaths/BoxedResourceIconPipeline.md`; original research remains separately recorded.

Validation: 14 Python regression tests pass, including same-mask synthetic shapes, over-front-wall overlap preservation, exact lower-wood RGBA restoration, leak/hash/binary/disjoint guards, historical Soba 0-diff identity and fail-closed production. All 24 production PNGs pass integrity; Stage A/New Village static validation passes. Synthetic shapes are structural evidence only; no new visual approval or RimWorld runtime PASS is claimed.

**Next action:** none for ordinary production. Revisit the v4 study only if automatic occlusion/compositing research is intentionally resumed.


### ART-RESEARCH-017 — Boxed-resource occlusion audit recorded

**Requested by:** author (2026-10-06 JST; investigation only, then push findings)  
**Owner:** Art/tooling / boxed-resource research  
**Status:** DONE — research documentation; research publication only

Durable source: `Docs/Research/BoxedResourceOcclusionAudit.md`. Eleven MO 1.6.2.2 boxed-produce PNGs from the author-provided package were inspected and compared at original resolution. Shared RGBA pixels concentrate in the lower portion; upper/contact-region differences depend on the contents. The source art's AI/manual/compositing method is unknown.

The existing Soba zero-difference identity result remains valid as an exemplar-preservation regression. It does not prove natural different-content production. Earlier ART-TEMPLATE-013/014/016 statements treating the exemplar's exact difference shape or identity PASS as sufficient for future materials must be read with this limitation.

Hard-fixed / occludable / extension regions plus a required-fill guide, and joint contact-region artwork, are recorded as research candidates; this publication does not implement them. No images, master/mask bytes, manifest activation, scripts, tests, or generation permissions change. No new identity/runtime PASS or completed production fix is claimed. Related art entry documents link to the audit. Before publication, separate commit `c8e7f2ff1248a2ec677a9b511f03d217ff53712e` changed main to v3-layered. That work is preserved; this audit assessed the preceding v2 snapshot and does not claim to validate v3 or its rim-overlap behavior.

**Next action:** if pipeline redesign is requested, validate contrasting content shapes under one registered region contract before implementing/activating revised production tooling. This task closes on research publication only.

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
Current master: **approved masu v2**. New-resource production: **v4 contact study BLOCKED pending visual validation**; see ART-TEMPLATE-019.

**2026-10-05 Soba in-hull integration:** `AMJC_BuckwheatInHull` now uses Soba-specific production art at `Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull`. The approved filled exemplar is reused for stack variants a/b/c for now. Remaining AMJ-009 art backlog is Soba immature/mature plant integration, sheaf integration, and edible buckwheat grain. Master `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`; manifest `Docs/References/AMJ_Masu_Template.json`; allowed/editable mask `Docs/References/AMJ_Masu_EditableMask.png`; required-fill guide `Docs/References/AMJ_Masu_RequiredFill.png`; approved representative `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`.


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


### DESIGN-016 — Japan Only責務の修正

**Requested by:** author (2026-10-05 JST)  
**Owner:** former Japan Only / cross-mod design  
**Status:** ARCHIVED — superseded 2026-10-07 by DESIGN-MOJ-001

2026-10-05時点ではJapan OnlyをMO由来西洋要素の除去・非表示化だけに限定していたが、作者の2026-10-07方針変更により撤回。履歴として残し、現行仕様には使用しない。

Superseded durable design: `Docs/Design.md`, old commit `973c14a2d4555b1e3e880fb91ac342b061f4e8e6`.  
Current replacement: DESIGN-MOJ-001 / design commit `ea656dcbeef821295acbedbf6a81621197219938`.


### DESIGN-MOJ-001 — AMJ - Medieval Overhaul Japanization

**Requested by:** author (2026-10-07 JST)  
**Owner:** future AMJ - Medieval Overhaul Japanization repository / cross-mod design  
**Status:** IN PROGRESS — architecture baseline recorded; MO research/retexture inventory started; dedicated repository and implementation not started

The former Japan Only concept is replaced by the formal mod name **`AMJ - Medieval Overhaul Japanization`**.

Confirmed architecture:
- hard dependency: Medieval Overhaul;
- role: **MO Patch + MO Retexture**;
- reorganize MO's research flow across the mod to fit ancient-to-medieval Japanese technological history rather than merely hiding western content;
- retain and reuse MO's useful material/processing stages wherever they still make sense in Japan;
- patch names/descriptions, prerequisites, TechLevel, recipes/materials and unlock paths where needed;
- retexture MO-owned weapons, armor, buildings and equipment when the same gameplay role can represent a Japanese counterpart without creating duplicate Defs;
- centralize MO-owned AMJ retextures in Japanization; AMJ-owned Def art remains with each owning mod;
- the mod is **not** a new Core. Grains, Rice Cultivation, Waterworks, Hot Springs, Ironmaking and other AMJ mods remain independently playable and do not require Japanization;
- World Tech Level is the strong recommendation for world-wide medieval/tech filtering; Japanization does not reimplement that general filter and does not hard-depend on WTL;
- Japanization does not absorb climate/environment, factions/events/backgrounds, independent fermentation/brewing/preservation loops, or Ironmaking's Japanese iron-production loop.

DBH for Medieval compatibility is a formal target, optional rather than a hard dependency. Attached 2026-10-07 Def audit confirmed that DBH for Medieval adds, among other things, manual pump, simple bathtub/toilet, washing kit, boiler pot, filter device, irrigation canal/sluice and its own medieval hygiene/irrigation research. Its MO patches already replace Vanilla Steel / industrial components with MO `DankPyon_IronIngot` / `DankPyon_ComponentBasic`, connect wind pumps to MO windmill research, add MO coal as fuel and add DBH water values to MO foods/drinks.

Japanization compatibility responsibility:
- align DBH for Medieval research placement, labels/descriptions, material costs and visuals with the Japanese historical progression;
- reuse DBH for Medieval's C# behavior rather than reimplementing pumps, hot-water storage, baths or plumbing;
- DBH for Medieval's `ES_IrrigationCanal` / `ES_SluiceGate` use the DBH PipeNet / Sprinkler path and are not the same system as Waterworks' gravity-fed natural-water canals. Keep both roles distinct; any bridge belongs at the Waterworks boundary/Adapter rather than suppressing one as a duplicate;
- respect Hot Springs/Waterworks ownership of AMJ-specific bathing, hot-spring and water-management loops.

**Durable source:** `Docs/Design.md`, architecture commit `ea656dcbeef821295acbedbf6a81621197219938`; DBH/Waterworks coexistence correction `9fa28b37fe1e55aae3a1d5862b7e1246a8653f6e`.

**2026-10-07 initial MO 1.6.2.2 research inventory:** author-provided MO archive contains 51 MO-owned `ResearchProjectDef` entries. MO also patches 16 Vanilla research projects into/repositions them in the Medieval research tab: Devilstrand, PsychoidBrewing, Smithing, CarpetMaking, PassiveCooler, ComplexFurniture, TreeSowing, Cocoa/Fruit tree sowing, Pemmican/Food preservation, Brewing, Stonecutting, RecurveBow/Archery, Greatbow, ComplexClothing/Tailoring, PlateArmor and LongBlades.

First-pass redesign hotspots, not yet final mappings:
- `Alchemy -> Steel -> Mithril` is a western/fantasy progression and must be disentangled; Ironmaking owns Japanese iron-production content while Japanization owns the MO-side research connection.
- MO military progression contains crossbow/arbalest/ballista/trebuchet/repeating ballista plus Basic/Military/Noble weapon tiers; these require historical classification rather than simple translation.
- `TextileSpinning` currently unlocks a western-style spinning wheel and therefore requires a Japan-specific historical audit before reuse/retexture.
- armor progression `ProtectiveClothing -> ChainArmor -> PlateArmor`, cooking branches, windmill/watermill, royal/rustic architecture and carrier-bird/exploration branches all require explicit keep/reinterpret/retexture/hide decisions.
- Gunpowder should be assessed as a late-medieval/Sengoku branch rather than remaining downstream of generic Alchemy.

**2026-10-07 first-pass 67-node classification complete:** a dedicated research source now covers all 51 MO-owned research nodes plus all 16 Vanilla nodes that MO moves/reworks. It uses maintain / reposition / reinterpret+retexture / hide / further-audit classifications and records historical anchors plus item-level follow-up requirements. No production XML, Def, texture, About metadata or dependency was changed by this research pass.

Cross-document reconciliation completed:
- MO-to-Japan retexture ownership is now explicitly centralized in Japanization in `Docs/RetextureImplementationGuidelines.md`; AMJ-owned Def art remains with the owning feature Mod.
- `Docs/IronmakingDesign.md` now distinguishes MO-alone behavior from Japanization-loaded behavior: Ironmaking does not rewrite MO research, while Japanization may reorganize MO metal research and connect it to Ironmaking conditionally.
- `Docs/Design.md` links the 67-node research audit as the detailed source for MO research classification.

**Result / commits:**
- research audit: `Docs/Research/MedievalOverhaulJapanizationResearchAudit.md`, commit `eb25895778dfe1284a6192bdd729183b3e4b5ce8`
- Design link: `9083cef4180c514bdf9449d69a56f4dbf0f0d6dc`
- retexture ownership reconciliation: `710c573a8b35bb0f0665e5ec51a4120a7ecc2de8`
- Ironmaking boundary reconciliation: `5128ed760a701cba20cf9017b7e3e04284a56369`

**2026-10-07 Def-level follow-up completed for military/loadouts and domestic production:**
- military mapping now traces the actual MO equipment families behind crossbow/siege, protection/chain/plate/adorned armor, bows, polearms, maces, blades, gunpowder, Smithing and tailoring;
- full dependency traversal shows `ProtectiveClothing` gates 17 MO Defs, `ChainArmor` 23, and Vanilla `PlateArmor` 23 MO Defs including multi-prerequisite adorned items. Japanization therefore curates retained Defs rather than inventing one Japanese equivalent for every Western variant;
- MO crossbow research currently couples handheld crossbows with fixed Scorpio/Ballista turrets. The audit separates portable `弩` from installed `弩` candidates and keeps Trebuchet/Repeater outside the baseline historical path;
- PawnKind audit confirms MO directly requires Western gear through `apparelRequired` and selects Western weapon/apparel tags. Japanization must patch MO PawnKind/Faction loadouts together with Def visibility/retexture; hiding player recipes alone is insufficient;
- faction boundary is now durable: Japanization owns MO-owned FactionDef/PawnKind presentation/loadout consistency, while AMJ Factions owns new Japanese historical faction/social gameplay;
- domestic/production audit confirms MO research nodes are cross-domain bundles: `Presser` mixes apple/cheese/paper, `Pemmican` mixes drying racks/rations, `Oven` mixes bread with Western pies/cakes, `RusticFurniture` reaches 131 MO Defs and `Stonecutting` reaches 68. Japanization must redistribute/curate actual unlock outputs rather than translate research labels wholesale;
- Oven is now a late-Sengoku/Nanban optional candidate rather than core Japanese flour-food infrastructure; Grains must not depend on it. Drying racks, pot cooking, millstone and watermill remain strong reuse candidates; Western recipe bundles remain item-level curation targets.

**Result / commits:**
- military Def mapping: `Docs/Research/MedievalOverhaulJapanizationMilitaryMapping.md`, commit `e081364ae4924c1b04a823343ed0f3a8f39a8366`
- military-audit cross-link: `89a75fe5d40a3e5124c014a8b59e2c5e33ef3c66`
- faction/loadout audit: `Docs/Research/MedievalOverhaulJapanizationFactionLoadoutAudit.md`, commit `e85670db253638b41d12954121f1534b2feabadd`
- military -> faction cross-link: `3d86824b3ada798c0d5dffd794704e86a9e871ad`
- Design faction/loadout ownership boundary: `283b7aaadfea3bacec2683e438302f41733354e6`
- domestic/production audit: `Docs/Research/MedievalOverhaulJapanizationDomesticProductionAudit.md`, commit `282db3d3d75f9e928033ad309b102815c931b597`
- research-audit domestic cross-link: `48bd4e2ecf0cc51fee8c1d5751fb0e79a6a2b291`

**2026-10-07 cooking/effect + architecture/furniture follow-up:** exact cooking XML was re-audited and the domestic-production research source now records recipe counts, ingredient/output families and MO food Hediff behavior. Key result: Japanization must curate effects as well as names. Representative retained-upstream effects range from +5/+10/+20% WorkSpeed on grill tiers and +5/+10/+20% ImmunityGain on soup tiers up to +20% WorkSpeed +40% Immunity plus multiple capacity offsets on some lavish/fantasy meals. These values are not automatically retained when recipes are Japanized.

Architecture/furniture direct-output curation is also recorded:
- RusticFurniture direct gates include cooking/baking tools, doors/gates, oil lighting, hearth, market stall, water barrel, game tables, lectern, oven, stew pot, apiary, mending bench, smoker and ice-related equipment;
- Stonecutting directly gates Tudor/castle walls, reinforced trench, ice cellar, large oven and kiln;
- RoyalRusticFurniture directly gates Western royal closet/bookshelf/armchair/throne/tables/dresser/Tudor bed/chest;
- ComplexFurniture directly gates reinforced log gate plus colored rustic beds.
The current rule is to retain/retexture only honest functional mappings, not create a one-to-one “Japanese skin” for every Western furniture form. Go/floor-level furnishing/tatami history provides stronger Japanese references than Western card tables/thrones/chairs.

**Durable source:** `Docs/Research/MedievalOverhaulJapanizationDomesticProductionAudit.md`, commit `4db54ad06cf0777a332c3ce5975327a41e572bcc`.

**2026-10-07 Processor Framework / lighting follow-up:** MO processor wiring is now traced. The generic presser embeds cheese (cow/goat/sheep) + apple processes, while paper uses a separate paper-press building/process. Drying racks use weather-sensitive 2.5-day PF drying at 0.8 base efficiency; smoker uses a 1-day fueled hot process with loaded efficiency 0.10 and therefore needs nutrition/spoilage balance review rather than being treated as equivalent to drying. The manual millstone is a normal Bill worktable, not PF. The MO watermill embeds two PF processes: cereal -> flour (0.25 day, efficiency 1.0, bonus Hay) and raw wood -> WoodLog (0.25 day, efficiency 2.0), so a historically valid water wheel does not imply both upstream process roles must stay. Windmill processor convenience does not override the baseline decision to hide the power windmill.

Lighting audit confirms MO already has torch/oil-lamp families independently of candle research. Japanization can use oil/torch lighting as the baseline and keep candles later/optional; Western candelabra/lamp forms require item-level mapping rather than wholesale translation.

**Durable source:** `Docs/Research/MedievalOverhaulJapanizationDomesticProductionAudit.md`, processor/lighting commit `ce535726744ed4c5326f71e049cbed06d1665710`.

**Next action:** inspect smoker input/output nutrition/spoilage/value, audit the watermill lumber process against woodworking chronology and resource balance, finish object-level lighting/furniture/architecture mapping, then compare weapon stats/material costs. High-priority unresolved areas remain Carrier Birds, Heavy Crossbow, Tar, Smoker and Carpet Making. Create/choose the dedicated Japanization repository before production XML/assets are written.

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

No image was generated or replaced in ART-TEMPLATE-001 itself. The masu registration gap identified here is closed by ART-TEMPLATE-004 below. Covers are registered separately in ART-TEMPLATE-003. Do not claim unrelated asset families are pixel-locked unless they have their own master/mask/manifest registration. Species style references remain references rather than identical-species templates. Pending species proposals remain pending.

### ART-TEMPLATE-002 — Automatically register future shared image families

**Status:** DONE (policy)

Future art work must identify reused components and automatically register each new family/master, document fixed/editable regions and production/validation commands, and integrate zero protected RGBA difference checks before subsequent derivatives. Canonical extension: `Docs/GoldenPaths/FixedImageTemplates.md`; mandatory entry: AGENTS. No images changed. Existing shared policy references in Environment inherit this extension.

### ART-TEMPLATE-003 — Workshop cover v1 deterministic template registered

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art direction / Workshop covers / shared art tooling  
**Status:** DONE

The accepted Core cover has now been converted into a cross-chat deterministic cover format. This supersedes DOC-011's earlier suggestion that reference-image editing is sufficient for final production.

Persistent Library rasters:
- visual reference: `/AMJ/References/AMJ_WorkshopCover_Core_Approved_Reference.jpg`
  - SHA-256 `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658`
- fixed common base: `/AMJ/References/AMJ_WorkshopCover_CommonBase.png`
  - SHA-256 `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362`
- variable mask: `/AMJ/References/AMJ_WorkshopCover_VariableMask.png`
  - SHA-256 `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622`

The mask allows only the addon-name slot and the right-side illustration area (`x >= 330`). All other final pixels are forcibly restored from the common base.

Durable repository registration / tooling:
- `Docs/References/AMJ_WorkshopCover_Template.json`
- `Docs/References/AMJ_WorkshopCover_Manifest.md`
- `Docs/GoldenPaths/WorkshopCoverPipeline.md`
- `Scripts/build_workshop_cover.py`
- `Scripts/validate_workshop_cover.py`
- `Tests/test_workshop_cover_template.py`

The three Library rasters were re-listed, materialized into a fresh container directory, and SHA-256 checked against the manifest; all three matched exactly. The compositor was then run against the materialized base/mask and passed the protected-pixel validator. The regression test also passed with a deliberately hostile opaque full-canvas layer, demonstrating that generated content cannot overwrite locked pixels.

**Production rule:** ImageGen creates only the addon-specific right-side transparent artwork. The final cover must be composed and validated by the deterministic tooling. Direct whole-cover generation and reference-image editing are not valid final-production paths.

**Next action:** apply this v1 pipeline to every subsequent AMJ Workshop cover. If any canonical Library raster is unavailable or hash-mismatched, stop production rather than reconstructing it.



### ART-TEMPLATE-004 — Masu v1 deterministic template registered

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

A consistency audit found that two different files were simultaneously documented as the canonical masu master. The later duplicate path is retained as the sole v1 source of truth because it is the 256×256 master explicitly stored for cross-chat reuse; the older `Textures/Things/Item/Resource/AMJC_Shared/Masu/AMJC_Masu_Empty.png` copy is removed to eliminate ambiguous masters.

Registered v1:
- master: `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`
  - SHA-256 `d10d44008698a692c9ad2369deb548f2af13f93d0621f7454cd84697e2a92d7b`
- editable mask: `Docs/References/AMJ_Masu_EditableMask.png`
  - SHA-256 `e1ef4ef8144e7029d908c91397e2491f17a232fef6a5f6c7a6258c81414d7af5`
- manifest: `Docs/References/AMJ_Masu_Template.json`

The editable region is limited to the masu interior cavity. Rim, exterior faces, outline, joinery, wood shading, placement and transparent margins remain protected. `Tests/test_masu_template.py` loads the real manifest and verifies deterministic composition with zero protected RGBA differences; CI runs it before Stage A validation.

**Next action:** all boxed-resource derivatives, beginning with Soba, must create only the contents layer and compose/validate it through the registered v1 template.


### ART-TEMPLATE-005 — Boxed-resource composition contract and masu v1 block

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

Direct comparison of the accepted buckwheat-in-hull icon with the first deterministic masu derivative exposed a gap in the fixed-part rule. Protected RGBA pixels were stable, but the result was still visually wrong: the container/contents composition occupied too little of the canvas and the contents read as a small pile placed in an oversized empty box.

Accepted visual reference is now persistent at `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`, SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`. Source size is 1254×1254. When normalized to 256×256, its non-transparent envelope is approximately `[17, 28, 239, 235]`; current v1 empty master is `[34, 42, 232, 213]`. Therefore the existing v1 template is not a valid production master despite passing protected-pixel checks.

The durable rule is `Docs/GoldenPaths/BoxedResourceIconPipeline.md`: boxed-resource families require both a fixed structural master and an accepted filled exemplar; frame occupancy and content fill/height are part of the contract; an empty master cannot become active until a representative filled composite is accepted. The current v1 manifest is marked blocked so automation fails closed.

**Next action:** build and author-approve masu v2 from the accepted filled exemplar, register required/allowed content-fill guides, then produce the Soba in-hull derivative. Do not continue from v1.


### ART-TEMPLATE-006 — Masu v2 visual candidate

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The blocked v1 master was not reused unchanged. A v2 candidate was derived by aligning the empty masu to the accepted filled buckwheat reference's 256×256 frame occupancy, then composing the accepted filling profile into a broader contents envelope rather than clipping contents to the old interior-only diamond.

The superseded v2 review candidates were discarded after the cleaned v2 master became active. They are not retained as reusable references. Only the registered master/masks and the approved exemplar remain authoritative.

The initial v2 review candidate matched the accepted exemplar's overall alpha envelope `[17, 28, 239, 235]` and restored the fuller mound/occupancy, but self-QC found visible roughness from upscaling the 256px empty master. That known defect was corrected proactively rather than being registered. The active v2 master now keeps the accepted exemplar's protected exterior/rim pixels exactly and rebuilds only the editable cavity from the high-resolution empty source. Registered assets are `Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`, `Docs/References/AMJ_Masu_EditableMask.png`, `Docs/References/AMJ_Masu_RequiredFill.png`, `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`, and `Docs/References/AMJ_Masu_Template.json`.


### ART-TEMPLATE-007 — Proactive art self-QC before registration

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

A review exposed that the agent had identified visible roughness in a candidate yet was still prepared to wait for author acceptance before correcting it. This is now forbidden. Before presenting a candidate as registration-ready, the agent must inspect the full-size and game-size views and automatically repair objective defects that preserve the already approved design: resize jaggies, resampling roughness, halos, clipping, seams, stray/leftover layer pixels, incorrect frame occupancy, and other deterministic cleanup issues.

The author should only be asked about genuine design/aesthetic tradeoffs. Known fixable defects must not be delegated back as a "妥協できるか" decision.

Applied immediately to masu v2: the upscaled 256px candidate was discarded as master material; v2 was rebuilt from high-resolution sources and the author-approved filled exemplar, then registered with allowed/required fill guides and a normalized representative regression asset.


### ART-TEMPLATE-008 — Masu v2 author visual confirmation

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The author reviewed the v2 comparison, including the 256px and game-like small-size views, and confirmed that it looks acceptable ("問題なさそう"). This closes the remaining visual-approval gate for the active masu v2 family. Continue subsequent boxed-resource icons from the registered v2 master/fill guides; do not regenerate the masu.


### ART-TEMPLATE-009 — Registered-reference comparison enforcement

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

Audit confirmed that the user's uploaded approved exemplar is exactly the registered Library visual reference: SHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`. The repository's normalized representative remains `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`, SHA-256 `0f81aa92460154d2b1ae50de14d7360be5e44ff46f8c81bdd113b6e19143d752`.

The failure was procedural: a manual comparison path mixed locally named intermediate images and, in a later attempt, whole-image generation was used instead of the registered reference/template path. This allowed an incorrect image/color to be presented as the comparison basis even though the registered reference itself was correct.

Permanent fix: `Scripts/Art/boxed_resource_review.py` now builds comparisons only from the manifest's `representative_final` after SHA-256 verification. `Tests/test_boxed_resource_review.py` regression-tests the fail-closed hash check, and CI runs it. Ad-hoc local aliases or regenerated images must never be presented as the registered reference.


### ART-TEMPLATE-010 — Discard contaminated boxed-resource intermediates

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

All stale/contaminated boxed-resource candidate images created during the broken reference/compositing path were discarded from the persistent Library, including the old Soba in-hull candidate set and the pre-cleanup masu v2 candidate/review images. The local working copies of dehulled-Soba candidates, color-fix candidates, comparison sheets, generated whole-icon retries, mask previews, and superseded v2 candidate assets were also deleted.

No contaminated dehulled-Soba candidate was committed to the repository. The only authoritative filled Soba reference remains:
- Library: `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`
- SHA-256: `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6`
- normalized repository copy: `Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`

Future work must restart the dehulled-Soba image from the registered reference/template path; discarded candidates must not be recovered or reused.


### ART-TEMPLATE-011 — Contaminated candidate auto-disposal rule

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

Durable rule added: when an image-processing path is discovered to be contaminated, all descendants from that point are invalidated immediately and removed from both persistent Library and local working storage. Invalid candidates are not retained merely for possible comparison because they can later be mistaken for authoritative sources.

The authoritative master/reference/manifest are kept; work restarts from the last verified authoritative source. If a failure image must be kept for diagnostics, it must be isolated and unmistakably marked as invalid/non-source so production tooling and review scripts cannot use it as a reference.

Formal rules: `AGENTS.md`, `Docs/GoldenPaths/BoxedResourceIconPipeline.md`, and `Docs/GoldenPaths/FixedImageTemplates.md`.


### ART-TEMPLATE-012 — 作成/生成の実行意味を分離

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

Author clarified that 「画像作成」 must not be interpreted as permission to invoke ImageGen. Durable rule now distinguishes command semantics:

- 「作成」「制作」「続けて」 = continue the registered production pipeline using authoritative assets, local editing, deterministic compositing, and validation.
- 「生成」 = explicit permission to use ImageGen only where the active Golden Path allows it.
- Fixed-template families may generate only variable material; shared parts and whole final images remain non-generative.
- If a valid local path is unavailable and generation was not explicitly requested, stop as BLOCKED rather than silently switching to ImageGen.

Formal rules are recorded in `AGENTS.md`, `Docs/GoldenPaths/TextureAssetPipeline.md`, `Docs/GoldenPaths/BoxedResourceIconPipeline.md`, and `Docs/GoldenPaths/FixedImageTemplates.md`.

### DESIGN-017 — AMJ各Modのリテクスチャ所有方針

**Requested by:** author (2026-10-05 JST)  
**Owner:** Cross-mod art / architecture ownership  
**Status:** DONE — durable design updated

AMJにおけるリテクスチャの意味と所有を再精査し、各Modが自分の責務範囲の前提Mod資産まで画風統一を担当する方針に確定した。

- Vanilla / MO等の既存Defも、AMJ追加資産と並べた際の統一感が不足する場合は担当Modが独自テクスチャへ差し替える。
- 同一Def / 同一前提資産を複数AMJ Modが競合上書きしない。1資産1所有Modを原則とする。
- 所有先は主要な機能・景観責務で決め、ロード順では決めない。
- 専用Retexture Modへの集約は標準方針にしない。自然な1所有Modを決められない横断案件等が生じた場合だけ再検討する。
- Japan Onlyはリテクスチャを担当しない。
- Coreの旧記述「MO小麦等のテクスチャを維持する」は撤回し、DefName/参照は維持しつつ必要なテクスチャはCoreが差し替えられるよう修正した。

Durable design source: `Docs/Design.md §8.5.1 AMJ共通リテクスチャ方針`, commit `633dbc04e1f89e423b77f970603362d6dc2421e7`.

**Next action:** 各機能のアート作業では、対象資産のAMJ内ownerを先に確認してから前提資産をリテクスチャする。

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


### ART-TEMPLATE-013 — Boxed-resource validation target corrected

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The author clarified that the current work was never intended to produce a dehulled-Soba asset. The purpose of the exercise is to validate the boxed-resource pipeline itself by asking whether the approved **buckwheat-in-hull** exemplar can be reconstructed correctly from the registered masu/template workflow.

All dehulled-Soba recolor branches are therefore out of scope and invalid as validation evidence. They must not be used to judge the pipeline.

The validation target is now:

1. start from the registered empty masu/master and authoritative approved buckwheat-in-hull reference;
2. derive/register the reusable variable-content layer and foreground occlusion structure needed by the template;
3. deterministically recompose the **same buckwheat-in-hull icon**;
4. require zero protected-pixel drift and, for the identity exemplar test, zero final RGBA difference from the registered approved reference;
5. only after this identity reconstruction passes may the same template be used for a different resource.

The test is about reproducing the approved in-hull reference faithfully, not changing its material or color.
### ART-TEMPLATE-014 — Exact variable-mask identity gate

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

Repeated Soba failures showed that color work was continuing before the layer decomposition itself had been proven. The broad editable/interior masks allowed visually plausible but structurally wrong composites, including broken rim occlusion and simple layer-over effects.

The process is reset to a structural identity gate. Using the registered 256px empty master (SHA-256 `a48875944834130676a32f8545e3b9eaae077dec773b7107643f1e65bf3f3fd3`) and registered filled exemplar (SHA-256 `0f81aa92460154d2b1ae50de14d7360be5e44ff46f8c81bdd113b6e19143d752`), an exact RGBA-difference mask was derived. Extracting only those exemplar pixels and recomposing them onto the empty master reproduces the exemplar with **0 differing pixels**. Exact variable bbox: `[35, 44, 223, 169]`.

This exact variable mask, not the broad editable mask or guessed pile polygon, is the structural basis for future boxed-resource material variants. The prior dehulled-Soba color candidates are invalid and were deleted. Color/material work must not resume until the high-resolution variable source is mapped to this exact 256px identity mask without altering fixed rim pixels.

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


### ART-TEMPLATE-015 — Validation intent correction

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The author corrected the workstream intent: the current image exercise is a **pipeline validation using the approved buckwheat-in-hull image as both source reference and expected output**. It is not a request to design a dehulled-buckwheat icon.

All local dehulled-Soba candidates and associated recolor experiments are discarded. Future validation output must show whether the registered pipeline reproduces the approved in-hull exemplar itself. A different resource/material must not be introduced until this identity validation passes through the intended reusable layer structure.

### WORK-001 — Retexture implementation precedent audit

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art compatibility / architecture  
**Status:** DONE — prior-art audit and shared implementation rule recorded

The earlier handoff incorrectly bundled already-completed runtime-test work into this item. The author clarified that the runtime testing is finished; this item is therefore closed on the remaining retexture audit only.

Audited representative approaches:
- Vanilla Textures Expanded;
- Vanilla Textures Expanded - Variations;
- ReGrowth 2 current 1.6 source;
- Medieval Overhaul current distributed 1.6.2.2 payload;
- Clean Textures;
- representative Van's Retextures;
- Misc. Training Medieval Retexture;
- Primitive Storage Retexture / Adaptive Primitive Storage;
- [CF] Better Looking Plants;
- Plants and Mushrooms Retexture.

Durable result:
- AMJ-owned prerequisite assets use **AMJ-owned unique texPaths + explicit Def/XML patching** by default.
- same-name texture shadowing/load-order-only replacement is not the canonical AMJ mechanism;
- retexture ownership is per complete loaded graphic-state family, not per one mature/base PNG;
- optional parent mods are guarded; static retextures do not require C#;
- known Mods that explicitly patch the same Def field (not merely the same original texture file) require narrow load-order/compatibility handling and final-loaded-path regression;
- pure retexture patches remain visual-only.

Shared source of truth: `Docs/RetextureImplementationGuidelines.md`, introduced at commit `e61a6379886d0f8a5ada8edb75a94943572f23ea`; linked from Core Design at `65b0dd95236c801c27c0c52aa4170b5996a32e03`.

**Next action:** when the first Core-owned prerequisite retexture is integrated, add its target/state manifest and regression coverage required by the shared guideline. No runtime-test rerun is part of this audit item.


### ART-TEMPLATE-016 — Buckwheat-in-hull production identity PASS

**Requested by:** author (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The corrected validation target is now complete. The approved buckwheat-in-hull exemplar is reconstructed through the actual registered reusable template path with **0 differing RGBA pixels**.

Implementation:
- `Docs/References/AMJ_BuckwheatInHull_IdentityVariable.png` stores the approved variable RGBA inside the editable mask and is transparent outside it.
- `Docs/References/AMJ_Masu_Template.json` registers `compose_mode: replace_rgba`.
- `Scripts/Art/fixed_template.py` supports that mode by replacing RGBA only inside the registered editable mask instead of alpha-blending it over the empty master.
- `Tests/test_masu_template.py` invokes the real compositor and requires 0 final RGBA differences versus `AMJ_BuckwheatInHull_Ideal_256.png`, while also requiring 0 protected/common-pixel differences versus the empty master.

This is the first valid proof that the boxed-resource production path itself can reproduce the approved in-hull Soba reference. It is not a dehulled-Soba result and does not change the approved icon.


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


### ART-TEMPLATE-016 — replace_rgba scaffold and occupancy hardening

**Requested by:** author / follow-up to boxed-resource identity validation (2026-10-05 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The zero-diff identity gate exposed a second reusable-contract issue before any new resource was attempted: under `replace_rgba`, the input cannot be a transparent object-only contents layer. It must be a complete rendered editable-cavity patch. Otherwise transparent pixels selected by the editable mask erase the empty-master cavity and reproduce the earlier broken-rim/layer-paste failure.

`fixed_template.py` now provides a `scaffold` mode that copies the registered master RGBA inside the editable mask and leaves everything outside transparent. New resource art must be added to this scaffold. Validation rejects broadly incomplete/transparent patches via the manifest-defined editable-region coverage gate.

Required-fill validation is also corrected for `replace_rgba`: alpha coverage is no longer meaningful because the scaffold itself is opaque. Occupancy is now measured by RGBA differences from the registered empty master within the required-fill guide. An untouched scaffold therefore fails closed, while the registered buckwheat-in-hull identity patch remains required to pass.


**ART-TEMPLATE-016 CI correction (2026-10-05 JST):** The first scaffold-hardening CI run (#207) failed the masu regression because an exact zero-hole rule was too strict for the already approved identity exemplar: its antialiased rear-edge region legitimately contains a small number of low-alpha pixels inside the historical editable mask. The contract is therefore expressed as a measurable coverage threshold instead of a per-pixel opacity prohibition. `replace_patch_min_defined_coverage` is registered at 0.98; the approved exemplar remains above that threshold, while a transparent object-only input fails closed. Required-fill occupancy remains difference-from-master based.


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

### DEV-TOOLS-001 — DevKit / Rim Control を開発専用補助ツールとして採用

**Requested by:** author (2026-10-06 JST)  
**Owner:** Testing/tooling  
**Status:** DONE (policy documentation)

AMJ共通の対話型開発補助ツールとして、DevKit — Better Dev Mode Menu (Workshop `3814373104`) と Rim Control (Workshop `3774299554`) を採用した。

DevKitはDef検索・スポーン・Debug Action等を用いた目視確認の準備短縮、Rim Controlはゲーム中の数値・visual・placement等の一時変更によるプロトタイピングに使用する。どちらも自動テストの代替や出荷依存にはしない。

Rim Controlで得た採用値はXML / C# / Def / 正式設計書へ正本化し、上書きを無効にしてから静的検証・RimTest Redux・Pickle・runtime gateで再検証する。正式テスト、自動テスト、リリースゲート、通常プロファイルの正式確認では両ツールを無効化する。

**Result / references:** durable rule in `Docs/DevelopmentTools.md`. Documentation-only change; no new runtime PASS is claimed.



### ART-TEMPLATE-017 — Masu three-layer compositor (superseded split)

**Requested by:** author (2026-10-06 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The author identified the structural error behind the repeated Soba boundary loop: a complex masu cannot be modeled as “master + contents clipped by one simple interior/pile mask”. The active production model is therefore changed to an explicit z-order stack:

1. fixed **rear masu** (back rim / inner walls / floor);
2. transparent **contents** layer;
3. fixed **front/side masu** foreground occluder.

The foreground/rear split selects exact pixels from the canonical masu master; it does not redraw the wood. Contents are no longer clipped by the historical editable mask or a guessed diamond/pile polygon. The foreground layer performs the perspective/occlusion naturally.

The deterministic split currently uses semantic front wood regions registered in the manifest. Local proof: rear + front reconstruct the canonical empty master with **0 differing RGBA pixels**. The old `replace_rgba` complete-cavity patch and exact-variable identity path are superseded for new resource production and retained only as historical diagnostics.

The new gate requires exact empty-master reconstruction, exact fixed foreground pixels, required-fill occupancy, and no visible content outside the authoritative master/reference envelope before a candidate can be presented.


### ART-TEMPLATE-018 — Occlusion audit integrated; unsafe compositor blocked

**Requested by:** author (2026-10-06 JST)  
**Owner:** Art/tooling / boxed-resource icons  
**Status:** ARCHIVED — task superseded by ART-RULES-021; artifacts remain valid only where current source-of-truth documents still reference them.

The separate research push `5690fbf8daa1eb73d0b9d263ca37ad1c0e08c024` has been read and integrated. The author also confirmed that the first v3 three-layer split visibly damaged the masu image. Therefore the fact that rear+front numerically reconstructed the empty master is not accepted as sufficient evidence.

Integrated conclusions:
- the Soba identity round trip proves preservation of that exemplar only;
- the upper/contact region is content-dependent and must be occludable;
- do not use a guessed cavity/pile polygon to clip contents;
- do not destructively carve the canonical master into complementary rear/front rasters;
- the revised target model is: **full canonical masu master as base/rear → transparent contents/contact → conservative hard-fixed foreground copied exactly from the master**;
- only hard-fixed foreground is reasserted after contents; contact-zone wood is not blindly restored;
- activation requires the same contract to work for contrasting content shapes and to pass 256px/~64px visual review.

`Docs/References/AMJ_Masu_Template.json` now records `new_resource_production_status = blocked_pending_occlusion_validation`. `Scripts/Art/fixed_template.py` refuses generic new-resource composition while blocked, and `Tests/test_masu_template.py` locks that fail-closed state. Existing approved in-hull Soba art and its historical identity evidence remain unchanged.

No new edible-Soba candidate is accepted by this change.

**CI follow-up:** the first fail-closed integration exposed two regressions inherited from the earlier v3 tooling rewrite rather than from the occlusion policy itself: the generic fixed-template validator had lost its historical no-required-fill default behavior, and the public `validate()` / output-overwrite guard had been dropped. These were restored in `cdf64ce4e93dd292ac5f8575448efd9c425ace55`, `345b3ce7756f8fa7221afa203ff1c145f8359324`, and `d1172f4f362f7b3d6c6985d251248bf276f5de43`. GitHub Actions Stage A validation run #225 completed successfully. The unsafe v3 new-resource compositor remains blocked; the CI success validates the fail-closed/tooling state, not a new image-production contract.


### ART-OPS-022 — Binary PNG publication timeout prevention

**Requested by:** author (2026-10-06 JST)  
**Owner:** AMJ shared art / repository operations  
**Status:** DONE — durable publication rule added

A RawBuckwheat correction attempt entered an unnecessarily expensive transport path after the image candidate itself had already been validated: the workflow explored palette quantization and emitted a complete base64 PNG payload as intermediate output before the GitHub write. The low-level Git data path itself is sometimes necessary because the available high-level GitHub file update action is UTF-8-text-only; the avoidable failure was mixing image transformation and verbose payload transport into that publication step.

The shared texture Golden Path now separates asset production from publication. Publishing PNGs may not quantize/re-encode/resize them merely to reduce API payload size, must not echo full binary/base64 payloads, and must use the shortest exact-byte path available. With connector-only binary writes, all target PNG paths are committed in one blob/tree/commit/ref transaction, reusing one blob SHA for identical stack-count slots. Repository-side PNG validation remains the completion gate.

**Durable source:** `Docs/GoldenPaths/TextureAssetPipeline.md`, commit `85934b3c65b50c426ce8edabcc541387bd990af1`.

### POLICY-MOD-NAME-001 — Mod名のコロン禁止（2026-10-06 JST）

**Requested by:** author  
**Owner:** AMJ shared release / documentation  
**Status:** DONE

AMJ Core・Environment・CCTOおよび今後の関連Modの名称では、半角 `:`・全角 `：` を禁止し、必要な区切りには ` - ` を使用する。About.xmlのname、Workshopタイトル、README等の正式名称に適用する。表示名の修正ではpackageId・既存Workshop IDを維持する。

YADAがMod表示名を一時ディレクトリ名に使用し、Windowsで半角コロンによりアップロード前処理が停止した件の再発防止。共通正本はCore `Docs/ModDescriptionGuidelines.md`（commit `695bff2a32a57cdf817b13b255587e749399b417`）。このリポジトリのAGENTSにも規則を反映済み（commit `44910d3a9081a2f733a09c8a10a34b1a6d6a3b57`）。

確認時点でCore・Environment・CCTOのAbout.xmlのnameはいずれもコロンなし。今回の変更は文書・運用規則のみで、ゲーム実行時テストやSteam公開の成功を示すものではない。

### DOC-RULE-003 — 2game presentation shared across AMJ

**Requested by:** author (2026-10-06 JST)

**Owner:** AMJ shared public-description policy

**Status:** DONE — shared guideline and Core / Environment / CCTO AGENTS routing synchronized

The six-section 2game template previously existed only in CCTO's Docs/2GamePresentation.md and Docs/2GameDescription-ja.txt. Current shared guidelines did not explicitly include it. Docs/ModDescriptionGuidelines.md now makes 2game source preparation and consistency checks mandatory for AMJ public-description work, with plain Japanese, short bullets, ▼ headings, related-mod direct links and an owning GitHub link. README remains the detailed public source; site publication remains a separate state. AMJE now has its own source and presentation policy. CCTO retains its existing template and now links the shared policy and its own GitHub repository.

Validation: documentation-only diffs, heading/link/format checks and diff whitespace checks. Reusable update checks live in the shared guideline and AMJE presentation policy. No live-site update or runtime PASS is claimed.

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


### DESIGN-CULTURE-001 — Vanilla premodern culture / Thought audit

**Requested by:** author (2026-10-07 JST)  
**Owner:** `sucRo-RimWorld/Ancient-Medieval-Japan-Project` until a dedicated Mod repository exists  
**Status:** ARCHIVED HERE — migrated to Project

The candidate was initially discovered while auditing Japanization, but the author established the project-wide rule that **ideas must live in the Project repository before they are split into standalone Mods**.

Current boundary:
- Japanization still does not own general Vanilla Thought/Trait/Need/social-culture changes;
- Grains no longer stores the evolving Premodern Culture design or audit;
- Grains keeps only the compatibility/ownership boundary pointer in `Docs/Design.md`;
- detailed idea, roadmap status and research now live in `Ancient-Medieval-Japan-Project`.

Migration:
- Project idea/roadmap staging rule: Project `AGENTS.md`
- Project candidate record: `Docs/Ideas.md`, `Docs/Roadmap.md`
- Project detailed audit: `Docs/Research/VanillaPremodernCultureThoughtAudit.md`
- Grains boundary cleanup: `Docs/Design.md` commit `ce2e300048a8922d3145bba7fb7ace0b0ece2a0d`
- Grains duplicate research file removed: commit `1e40b22cdd7fed4f638ee09cbcae5cddd5578c20`

**Next action:** continue this idea only from the Project repository until the author decides it warrants a dedicated Mod repository.


### META-PRESPLIT-MIGRATION-001 — move unowned designs to Project

**Requested by:** author (2026-10-07 JST)  
**Owner:** Grains/design boundary  
**Status:** DONE — detailed unowned designs removed from Grains authority

Under the AMJ Project pre-split staging rule, detailed designs/research for future standalone modules with no owner repository were migrated to `sucRo-RimWorld/Ancient-Medieval-Japan-Project` at Project commit `f610761b8d9313f0114fdbdfb98898381946d54e`.

Migrated areas include Hot Springs; Fermentation/Brewing/Sake/Preservation; containers/pottery; Hunting & Gathering/Coastal Gathering; Backgrounds/Clothing/Factions/Events; Medieval Overhaul Japanization and its detailed audits; Repair/Reuse; deferred plants/processing; architecture/religion boundaries; and Ironmaking.

Grains now keeps only concise ownership/compatibility pointers for these areas. Historical commits remain provenance, not current design authority. Environment/Waterworks/CCTO candidates were not moved because their implementation owner is already clear.


**2026-10-07 scenario runtime-test ownership handoff completed (source/tooling unit):** Grains PR #7 merged at `69ed44e5fdb3e349bf6dfb429d80f25d7374bb0f`, implementation `4a13086fe98f1d65fa66bf61366ff59ba0a82c93`. Scenarios PR #1 merged at `3ee114a56e778ace979903e208890ab662179027`, final implementation `46dfc4f09ee3285cc04d87ea097aa9e35bf15805`; owner handoff `d418d81369dda033ef6cd1bfa43110f4b0062190`.
- Scenarios owns canonical NewVillage steps/Quickstart and four provider profiles, three cases each, plus build/staging/config/fingerprints/fresh-summary/ERROR/private-desktop execution tooling. Grains normal profiles now require six grain-only cases; the eight-case fixture retains two explicitly legacy village cases (LegacyVillageSteps/AmjLegacyVillageQuickstart). Fixture start checks are not legacy-save migration evidence. Formal sources: Docs/GrainsProfileTesting.md, Docs/ScenarioExtraction.md and Scenarios Docs/RuntimeTesting.md. Manifest separates legacy test handoff from current owner sources.
- CI PASS: Grains Stage A `37640099282`, Workshop `37640099260`; Scenarios static/Windows PowerShell 5.1 `37640057729`. Local profile tooling, extraction eight methods, paired six XML configurations, unchanged 38-contract snapshot, PNG 26 and Workshop 75-file archive parity passed. Scenarios archive remains 13 files. Synthetic summaries/ERROR negatives verify tooling only. No production runtime content, metadata or dependency change in this unit.
- **Not completed:** C# compilation, real RimWorld starts/loader/rendering, legacy-save read/re-save or provider add/remove/overwrite tests. No installed game/assemblies here; no game process active. RawRice 300 remains draft. Existing saves and Core/MO removal are not certified; fallback Defs and About MO dependency remain gated.
**Next owner:** continue actual start/save automation from Scenarios main Coordination and Docs/RuntimeTesting.md. Compile/run its four profiles on installed RimWorld through the private-desktop entry, then implement and execute old-save/add/remove/re-save fixtures with rendering, accurate source/save evidence and every-ERROR failure. Grains retains grain runtime and legacy compatibility responsibility.


**2026-10-07 Grains residual MO dependency audit:** Author requested returning to Grains after the passing Scenarios static/CI work. Grains PR #8 merged at `274c955dfcd9bd44531d2cfa0ceac48676fc1ccc`; implementation `b0c8e54c64c1ed7e36920b95ae34bef4219b959b`. Formal current source: `Docs/GrainsDependencyAudit.md`, linked from Design. Scenarios main priority record: `ee2f2737244e2ffa09b620588cef2f0f72124055`.
- Confirmed in author-supplied MO 1.6.2.2 archive: three unconditional Grains Defs still reference four MO-provided texture paths (Barley mature/immature, GrainProcessingSpot, GrainProcessingTable). Grains does not supply those paths. These generic paths escape identifier checks; full Vanilla texture inventory/runtime provider resolution is not proven.
- Base validator output now explicitly covers MO identifier/class references only and names excluded texture/inheritance/runtime scope. Current Design ownership table now reflects physical Scenario extraction with guarded legacy fallback. No Production runtime XML, packageId, MO About dependency, texture or historical prose changes.
- Local PASS: Base 4, chain 9, environment 4, extraction 8 methods; Stage A and 26 PNGs. PR CI PASS: Stage A `37646630725` (including Windows tooling), Workshop `37646630503`. API tree exactly matched local tested `8e85e236361da7be3fb2c789f0091c6fa4a4a574`.
- Next Grains unit: resolve the three Defs' graphics dependency with Grains-owned paths/assets and all displayed states, then execute four real profiles and legacy-save gates. Additional Scenarios engine save adapter work is paused by author priority, not approved as complete. C# compilation/game/rendering/save migration remain unverified here; About MO dependency stays gated. No game/background worker active.


### COMPAT-MOJ-OWNERSHIP-001 — Japanization compatibility ownership

**Owner:** Grains compatibility / Project Japanization architecture  
**Status:** DONE — no Grains implementation change required

Project-level Japanization architecture now explicitly preserves Grains' existing compatibility contract:

- Grains continues to own the minimum optional MO compatibility required for the supported `MO + Grains` profile (MO wheat/flour/Millstone/Straw/category connections where applicable).
- `AMJ - Medieval Overhaul Japanization` does **not** absorb that compatibility and must not become required for Grains + MO.
- Japanization owns only additional adaptation caused by its own MO-wide historical research/Def/retexture reconstruction.
- If both layers touch the same upstream MO area, do not duplicate the same semantic patch; Japanization must preserve/adapt the Grains contract rather than fork it.

**Durable source:** `sucRo-RimWorld/Ancient-Medieval-Japan-Project:Docs/Research/MedievalOverhaulJapanizationIntegrationMatrix.md`, commit `5483cc42744ed2652bf7599272c00225668d9963`.

**Next action:** none in Grains until a concrete Japanization implementation conflicts with an existing Grains MO compatibility path.


**2026-10-08 standalone graphics provider separation:** Grains PR #9 merged at `8fd5266eee22556baa73ef4cf87886c92956a684`; implementation `52808edc98211dfbf12f48a81deaf1ea18f00d37`. Current formal source: `Docs/GrainsDependencyAudit.md` implementation addendum and Design step 5.
- Shared Base barley mature/immature now uses the existing AMJ Awa PNG families. Both processing benches use the existing Vanilla TableStonecutter development reference; their original size/direction/shader fields stay unchanged. Four Replace operations inside the MO-active compatibility root restore all historical MO paths. All 38 MO explicit contracts, including graphics, remain intact.
- Added Base known-MO-path rejection and existing AMJ family checks; regressions reject an immature MO path returning to Base and a missing conditional graphics restore. Local PASS: Base 6, chain 9, environment 4, extraction 8; actual independent Scenarios pair six configurations; Stage A, PNG 26, Workshop 75-file filter, PowerShell four-profile byte-preserving staging/summary/negative checks. No fabricated game run: the PowerShell summary tests are synthetic tooling checks.
- GitHub PR CI PASS: Stage A `37648858058` (including Windows tooling and independent owner checkout), Workshop `37648858225`. API and merge tree match local tested `a191335bf04bf48382ac5dc8aaba133666f8a094`. Incoming Japanization ownership handoff retained.
- This closes known MO texture-path exposure in the Base projection, not finished art or full provider resolution. Barley borrows Awa; both benches share a temporary stonecutter image and real rotation/mask/footprint appearance is unverified. No PNG generation/change or package/Def/metadata rename. About MO dependency remains gated.
- Next: prepare/review dedicated Grains art for these three Defs and run real four-profile graphics/Bill/ERROR checks plus save gates on an installed game. C# compilation, game/rendering/old-save tests remain pending; no game/background worker active.


**2026-10-08 author correction — AMJ graphics priority with MO:** PR #10 merged at `11fa3bfdb24b21b3219d3232a380ecee95887156`; implementation `365cf16c0f48b7fd505ec588c53fcc15ed585d60`. Supersedes PR #9's policy of restoring historical MO images. Formal current rule: Design step 5 and GrainsDependencyAudit current-policy section.
- Removed the four MO graphics restore operations. AMJ-owned barley mature/immature and the two processing benches now keep the same AMJ-selected shared graphics with or without MO. Existing AMJ Awa/Vanilla stonecutter references remain temporary; no new/generated PNG or approved master change.
- Historical fixture unchanged. Validator first requires the four current AMJ paths in both projections, then normalizes exactly those fields in a comparison copy for historical hashes. All remaining fields of the 38 contracts stay checked. Added negative regression for gameplay mutation of a visually changed bench; MO-image override is rejected instead of requiring restoration.
- Local PASS: Base 7, chain 9, environment 4, extraction 8, actual paired repositories six XML configurations, Stage A, PNG 26, Workshop 75-file payload and PowerShell four-profile tooling. PR CI PASS: Stage A `37651940611`, Workshop `37651940498`. API and merge tree equal local tested `6a5ad1bd4e740fc499b0537958dac088bb1d391f`.
- Next: dedicated production art and real four-profile rendering/Bill/ERROR/save gates. MO materials/research/Straw/provider compatibility retained; packageId and DefNames unchanged; About MO dependency stays gated. Runtime/C# compilation/real save migration not executed here; no game/background worker active.

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

### DOC-SHARED-RULES-OWNER-001 — Shared rule migration to Project (2026-10-08 JST)

**Owner:** Project common rules / repository routing
**Status:** DONE — current AGENTS and shared-rule references route to Project

Canonical shared rules and Workshop template/tooling now live in Project `Docs/SharedRules.md` and its linked sources. Grains old Markdown paths are migration pointers only. Existing historical coordination entries retain their original commit/path provenance; resolve future work through the new Project index. Mod-specific implementation, tests and accepted content art remain with this repository. No runtime behavior, new preview generation or Steam publication is part of this migration.


**Grains MO grinding E2E false-positive fix (2026-10-08):** Identified a deterministic mischeck in `GrainsSimulationSteps.ProductionScope.Bill`: MO's real `DankPyon_CraftFlourBulk` produces 10 `Hay` as a declared coproduct, yet the helper asserted that Hay could never increase. The native-Bill test now validates each declared product (including MO Hay) by exact recipe quantities; only undeclared Hay and Straw must remain unchanged. Added `Tests/test_grains_chain.py` guard plus formal GrainsProfileTesting source notes. Still pending C# compilation, real four-profile Pickle+runtime ERROR 0, native sow, art and migration gates. This change is test-harness correction only.


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


### GRAINS-MEAL-TEXPATH-RUNTIME-20261008

**Owner:** Grains E2E/runtime texture gate. **Status:** Four actual-provider Pickle profiles 6/6 each (24 passed) observed in uploaded `automated-gates(3).log` (2026-10-08), but ERROR-0 FAILED in all four. No runtime scenario failures remain. Each profile emitted the same unresolved Texture2D for `AMJC_Houtou`, `AMJC_Sobagaki`, `AMJC_MilletDumplings` at `Things/Item/Meal/Simple` plus consequential `MatFrom with null sourceTex`; the older `.../SimpleMeal` path also failed in the previous uploaded log. Existing Vanilla texture path assumptions are not sufficient proof of actual availability. Corrected production Defs to temporarily point at bundled Grains-owned 3-variant grain PNG sets (Houtou/dumplings Millet, Sobagaki Buckwheat), `Graphic_StackCount` to match. Added CI source-path file-existence assertions and negative path/class/missing-sprite regressions. No art generation or claim of finished dishes; images still pending approval. Require another real 4x6 + runtime ERROR 0 pass before closing release gate; old saves/rendering/standalone dependency remain open.


### GRAINS-REAL-PROVIDER-SMOKE-PASS-20261008

**Owner:** Grains testing/release. **Status:** DONE only for fresh four-profile actual-game smoke/ERROR-zero; migration and release gates OPEN (2026-10-08 JST).

The author's `automated-gates(4).log` confirms exactly **6/6 Pickle scenarios per profile, 24/24 total, runtime ERROR 0 in vanilla / vanilla-ccto / mo / mo-ccto**, with byte-preserving stage, native production job scenarios and C# compilation (nonfatal CS1684 warnings). CCTO local provider selection worked, and the meal Texture2D/MatFrom errors from (3) are absent after the temporary packed graphic change. The authoritative acceptance boundaries are now recorded in `Docs/GrainsProfileTesting.md`; rice progression evidence in `Docs/Balance/Crops/RicePostHarvestProcessing.md`; and the overall milestone in `Docs/Design.md`. Do not request another identical smoke solely to re-establish this gate. **Still OPEN:** real legacy save migration/add-remove testing, calendar-controlled sow/cold growth, Japanese/English UI checks, finished art/normal zoom, play-balance and standalone MO-dependency release decision. The phrase “fresh migration smoke” does not constitute proof that an old user's save was migrated. No gameplay source, textures or dependency metadata changed by this documentation closeout.


### GRAINS-OLD-SAVE-CONSERVATION-CONTRACT-20261008

**Owner:** Grains save migration testing. **Status:** Read-only save XML fixture preparation and negative tests implemented; *actual legacy engine load/re-save pending*. The separate Scenarios repository continues owning New Village's scenario/faction/pawnkind migration inspector and runtime adapter. Grains owns preservation of saved `AMJC_` crop/food/equipment things, Vanilla `Plant_Rice` / `RawRice`, and persisted AMJC processing/cooking Bills across **same packageId** old-Core -> current Grains, with MO retained. `Scripts/grains_save_contract.py` preserves original .rws bytes, records claimed SHA/version/source IDs in a new evidence directory and compares paused-save snapshots with strict IDs/quantities/bills/ticks/mod sets. Reject missing required grain/rice witnesses and test-package aliases. No source save mutation, provider removal, Def renaming or gameplay source changes. `Tests/test_grains_save_contract.py` uses synthetic XML, added as a separate Stage A CI step. This is **not** a real save engine adapter, successful actual migrated save, nor confirmation of release readiness; further work requires a genuine old .rws from an older production Core and an installed-game production-ID isolated load/re-save + every-ERROR 0 gate. The 4×6 fresh smoke gate remains DONE.


### GRAINS-NATIVE-SEASONAL-SOW-20261008

**Owner:** Grains native sow/temperature E2E. **Status:** Test code + deterministic static regression proposed/integrated; compiled and run against the installed game only on next author-side real-provider E2E. Existing 4×6/ERROR-0 evidence remains valid solely for earlier commit, not for the modified E2E. No production Def/Recipe/crop temperature change.

Extends the last real production scenario without changing four profiles' six-scenario manifest: uses a real grow-zone and `WorkGiver_GrowerSow.JobOnCell` -> `JobDefOf.Sow` with a capable pawn; confirms real `Plant_Rice` sow at 25 C, +one-quadrum calendar movement with controlled 5 C blocks new rice sow and stops its long-tick growth, while barley can sow/grow at 5 C, and rice resumes growth on rewarming. SingleTick is advanced in short batches, with strict timeout and try/catch preserved; fixture date, biome temperature, plants, snow depth and zone are restored. Controlled `BiomeDef.constantOutdoorTemperature` is **not** natural climate simulation and does not prove actual frost death or extreme seasonal survival. See `Docs/GrainsProfileTesting.md` and `Docs/Balance/Crops/ColdTolerance.md`. Rerun the 4 real-provider profiles and ERROR 0 after compilation; do not claim this new coverage passed until logs prove it.


### GRAINS-MO-SEASONAL-NOON-20261008

**Owner:** Grains Pickle/environment testing. **Status:** Targeted E2E fixture correction applied for author `automated-gates(5).log`; new runtime rerun PENDING. Real runtime: vanilla 6/6 + ERROR0; vanilla-ccto 6/6 + ERROR0; mo **5/6 FAIL, Pickle error** `Native TickLong must resume rice growth after warming.`; mo-ccto 6/6 + ERROR0. Previous 4×6 smoke gate was completed on the earlier build only, not new seasonal test.

Root cause hypothesis with confirmed engine behavior: Plant.Resting forbids growth when local DayPercent <0.25 or >0.8; the test used noon only on initial sow, but advanced the calendar +15 days and executed real jobs / multiple 2200-tick windows before warm recovery, so a dusk/resting phase can invalidate warm TickLong growth despite temperature 25 C. The uploaded summary does not include diagnostic dayPercent/glow, so don't assert definitive causation. Fix in `Tests/E2E/GrainsSimulationSteps.cs`: reschedule **recovery** at local noon and refresh `SkyManagerUpdate`, assert nonzero actual light/growth rate and non-resting day before using native TickLong to verify growth, add rich diagnostics. Strengthen `Tests/test_grains_chain.py`; authoritative rationale and limits in `Docs/GrainsProfileTesting.md` and `Docs/Balance/Crops/ColdTolerance.md`. No production values/XML or dependency metadata changed. CI static PASS is not real-game approval; need next real 4-profile 6/6 and ERROR 0 on revised source.


### GRAINS-MO-NOON-RETEST-PASS-20261008

**Owner:** Grains Pickle/runtime compatibility. **Status:** MO-only targeted rerun DONE, full same-revision four-profile matrix still OPEN. Uploaded `automated-gates(6).log`: revised native seasonal sow/5 C cold/25 C rewarming fixture with real MO provider built successfully and passed all 6 Pickle scenarios, runtime ERROR 0, unchanged player's ModsConfig; only non-fatal CS1684 warnings. Previous `automated-gates(5).log` vanilla, vanilla-ccto, mo-ccto each passed 6/6 and ERROR 0 on the pre-noon-fix test, while original mo failed 5/6. Revised mo test fix is commit `b127e162d91403281a01c7903ac6ed64752657c2`. Distinguish per-provider acceptance evidence across two source revisions from an all-four same-revision gate: **all-four latest-build rerun not yet evidenced**. Record this in canonical `Docs/GrainsProfileTesting.md` and `Docs/Balance/Crops/ColdTolerance.md`. Do not alter balance XML, bypass native ticks, repeat targeted mo-only again without cause, or claim real natural seasonal/frost-death/legacy-save release gates passed. After a full all-four 6/6 ERROR-0 pass, proceed with separate release gates (actual old save, UI bilingual load, art, MO-dependency metadata review).


### GRAINS-SEASONAL-SKY-NRE-20261008

**Owner:** Grains test runtime compatibility. **Status:** (7) regression FAILED; focused sky-synchronization fixture correction prepared, post-fix actual game validation still OPEN. `automated-gates(7).log` final same-revision matrix: vanilla FAIL + ERROR, vanilla-ccto FAIL + ERROR, mo FAIL + ERROR, all at real production job/seasonal scenario with bare `Object reference not set to an instance of an object`; mo-ccto PASS 6/6 ERROR 0. Nonfatal CS1684 build warnings only. A direct `map.skyManager.SkyManagerUpdate()` call added in prior E2E test is a plausible common NRE cause, *not proven* without a stack trace: engine implementation also updates weather, shadows, shader and camera. Replace its manual invocation in controlled recovery with native `GenCelestial.CurCelestialSunGlow(map)` reading and isolated map `ForceSetCurSkyGlow`, saved/restored sky cache; keep real Sow JobDriver, daytime/temperature checks and DoSingleTick growth. Add phase-aware failure diagnostics, update source contract test, record in `Docs/GrainsProfileTesting.md` and `Docs/Balance/Crops/ColdTolerance.md`. No production gameplay/config changes. Next: run isolated `vanilla` first on actual game to check resolution, then other profiles and ERROR-0; do not claim 4/4 before results.

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
