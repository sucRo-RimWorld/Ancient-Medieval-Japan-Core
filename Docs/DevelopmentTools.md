# AMJ Core development tools

AMJ Core uses two layers of automated Stage A validation.

## GitHub validation

`.github/workflows/stage-a-validation.yml` runs `Tests/validate_stage_a.py` on pushes to `main` and pull requests.

This checks repository-owned XML values and wiring, including the Awa crop values, millet storage stages, processing-station values, the four threshing/hulling recipes, and the 13-unit conservation path.

## Local full gate

From the repository root:

`run-tests.bat "D:\SteamLibrary\steamapps\common\RimWorld"`

The gate:

1. verifies the installed Medieval Overhaul 1.6 source exists;
2. runs `Scripts/Validate-StageA.ps1` against repository XML and the installed MO source;
3. generates three development-only test mods under `RimWorld\Mods`;
4. compiles the Pickle and Quickstarts test assemblies;
5. creates an isolated RimWorld save-data profile without changing the normal mod list;
6. launches RimWorld automatically;
7. runs the four `stage-a.feature` scenarios;
8. requires a fresh clean 4/4 Pickle summary;
9. lets Pickle exit RimWorld automatically.

Required local Workshop helpers are Pickle (3791648678) and Quickstarts (3793646067), plus their normal Harmony/RimLogging requirements.

Generated test mods:

- `AncientMedievalJapanCore.E2ETarget`
- `AncientMedievalJapanCore.E2E`
- `AncientMedievalJapanCore.MOFixture`

Remove them with:

`clean-e2e.bat "D:\SteamLibrary\steamapps\common\RimWorld"`

## Automated coverage

The current local integration suite checks loaded RimWorld Defs for:

- Awa growDays, fertility, temperature, sow skill, harvest target and yield;
- raw millet / millet-in-hull / edible millet storage tiers;
- no accidental `DankPyon_Cereal` registration;
- simple processing spot speed 0.5;
- grain processing table speed 1.0 and Basic Agriculture requirement;
- the same four Stage A bills on both stations;
- single and x10 threshing/hulling inputs, products and work amounts;
- `13 raw millet -> 13 millet in hull + 13 Straw -> 13 edible millet`;
- final edible millet acceptance by the Vanilla simple-meal ingredient filter.

Manual checks should be reserved for appearance, Japanese UI readability, building footprint/interaction-cell usability, and whether processing speed feels appropriate during real play.
