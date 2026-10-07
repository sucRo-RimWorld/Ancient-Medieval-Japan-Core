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

The profile suite requires exactly its six named scenarios, 6/6 passes and
zero skips. Assertions check actual provider presence, fixture/production-Core
absence, resolved primary crop/recipe/simple-meal contracts, New Village loaded settings and actual Quickstart supplies/research
for the active profile, loaded wheat/flour/milling/food contracts, and presence/absence of AMJ cold-tolerance extensions. Runtime log checking
fails on **any ERROR**, including provider errors. Both summary and log gates
run after a launched game even if the process or scenarios already failed.
Missing fresh output is a failure. The game watchdog is five minutes per profile;
the private-desktop matrix watchdog is forty minutes and terminates its own tree.

These are **migration smoke tests**, not the completed release matrix. Subsequent
implementation must prove actual harvest/Bill cooking behavior, six-grain environmental-choice
regression, and save compatibility cases. None is inferred from the six smoke
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
mod makes the other a hard dependency. The final name/package/repository and
save-migration mechanism remain undecided; physical extraction has not occurred.

The current six-scenario profile suites and eight-scenario fixture suite retain
New Village only as transitional contracts. During extraction, move the startup
checks and the Scenario/Faction/PawnKind golden contracts to the new owner; remove
the dedicated-Scenario presence requirement from Grains in that same change.
Keep grain contracts rather than discarding the old snapshot wholesale.

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
