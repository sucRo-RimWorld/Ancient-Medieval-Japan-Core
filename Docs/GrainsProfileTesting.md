# Grains dependency-migration test profiles

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
Missing fresh output is a failure. The game watchdog is five minutes per profile;
the private-desktop matrix watchdog is forty minutes and terminates its own tree.

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
