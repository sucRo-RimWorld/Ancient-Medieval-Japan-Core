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

### AMJ-004 — Awa plant graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** IN PROGRESS

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

The replacement has therefore been rebuilt directly from the exact previously working blob `533818ce40a03f98d473821ddc2113b47531da88`: only the visible sprite was enlarged to 120% with nearest-neighbor scaling on the same 256×256 palette canvas, preserving the original palette/transparency structure. The resulting exact blob is `d9a0c7425bf327c25016ef86157b8f0eabfeac54`. The incorrect RGBA-only validator requirement has been removed.

**Next action:** pull latest `main`, restart RimWorld, and verify that this exact 1.2× derivative renders. If a red question mark still appears, stop changing image bytes and capture the missing-texture/runtime log entry so the resolver/path failure can be diagnosed directly.

**Result / references:** Stage A cultivation `47ddb201ab167ac47c4af9da21d038b3096b3847`; shared millet processing completion `5fb1b15d3091d306bc59f8a5605e5496d4251afd`; mature Awa art `d515cb304531ae01debf1c6cd2ab859f9675fdf9`; texture-loading correction `b7813c846f5d3bb2c4ede99a53ca001336f77409`; final in-game visual comparison accepted on 2026-10-03.

### AMJ-005 — Shared millet post-harvest graphics

**Requested by:** Agriculture/XML  \
**Owner:** Art/graphics  \
**Status:** OPEN

Awa, Hie, and Kibi intentionally merge after harvest into the shared chain:
`AMJC_RawMillet` → `AMJC_MilletInHull` → `AMJC_Millet`.

These three ThingDefs still use temporary MO item graphics. Because they are shared by all three millet crops, their final art should be produced once as part of the shared millet chain rather than separately for each crop.

The same locked AMJ art rules apply, with item icons flatter than plant art and with fewer/shallow shadows than the accepted plant asset.

**Next action:** after AMJ-004's revised mature/immature pair passes the in-game check, use the already approved 2026-10-03 post-harvest artwork as the source for raw millet, millet in hull, and edible millet. Do not regenerate those three unless the in-game check exposes a concrete problem.

**Result / references:** shared processing implementation `1429ad30c2e1de6f931a2b25a730a3e65fb60228`; art-style baseline `2d4accb0c56bff6b81497a325877d5a5dc7d7710`.

Add new items using the following form.

### AMJ-XXX — Short title

**Requested by:** <workstream/chat/repository>  
**Owner:** <workstream>  
**Status:** OPEN

Context, constraints, and exact question/request.

**Next action:** concrete next step.

**Result / references:** add commit SHA, PR, design section, or other durable reference when available.

## Completed handoffs

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

Historical design references used for recovery include `9b6807b48cf43da50a70caf1a99a5989391473ca` (growDays), `768665413e70ad7451b6b2255c67eb349ea32099` (yield/fertility/temperature), `33430521c97e22e2a52fe1ca661deeb6faf5c025` (skill/storage), and `36f271de4d82162fb002922bbb295ae5f68f31ae` (later grain-processing/storage structure). Current CCTO AMJ values are sourced from CCTO `Docs/ImplementationTable.md`.

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
