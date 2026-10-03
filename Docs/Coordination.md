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

### AMJ-004 — Awa final plant graphic

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

Because AMJ currently has only one mature Awa texture, the PlantDef now uses the simpler and deterministic path `Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature` with `Graphic_Single`. Static CI/local validators now assert both this exact graphic wiring and that the PNG exists, so a path/class mismatch is caught before another in-game smoke. The immature graphic intentionally remains the MO wheat placeholder.

**Next action:** pull the latest `main`, restart RimWorld fully, and perform one visual-only check of mature Awa at ordinary in-game zoom. If the texture renders and its silhouette/scale is acceptable beside MO crops, mark AMJ-004 DONE; do not repeat numeric processing tests.

**Result / references:** Stage A cultivation `47ddb201ab167ac47c4af9da21d038b3096b3847`; shared millet processing completion `5fb1b15d3091d306bc59f8a5605e5496d4251afd`.

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
