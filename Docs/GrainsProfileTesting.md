# Grains dependency-migration test profiles

This is migration step 1 of `Docs/Design.md`: separate the harness before changing
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
Patches, Textures and Languages are copied unchanged. Assemblies, versioned 1.6
content and loadFolders are copied if present. Production Core is not activated
alongside the test copy. The test-mod assembly build is shared with the legacy
runner; the real profiles neither build nor load the MO/CCTO API fixtures.

Real profiles do not apply `E2E_Graphics.xml`, remove MO references, substitute
recipes, or manufacture missing provider Defs. At this migration stage, Vanilla
is expected to expose the existing unguarded MO references and placeholder art.
That failure must remain visible until runtime migration resolves it.

`build-e2e.bat <RimWorldRoot>` and the existing `run-e2e.bat` / `run-tests.bat`
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

The profile suite requires exactly its three named scenarios, 3/3 passes and
zero skips. Assertions check actual provider presence, fixture/production-Core
absence, resolved primary crop/recipe/simple-meal contracts, retained New Village
Def, and presence/absence of AMJ cold-tolerance extensions. Runtime log checking
fails on **any ERROR**, including provider errors. Both summary and log gates
run after a launched game even if the process or scenarios already failed.
Missing fresh output is a failure. The game watchdog is five minutes per profile;
the private-desktop matrix watchdog is forty minutes and terminates its own tree.

These are **migration smoke tests**, not the completed release matrix. Subsequent
implementation must add standalone wheat/flour/milling/food contracts, actual
New Village startup verification for each profile, six-grain environmental-choice
regression, and save compatibility cases. None is inferred from the three smoke
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
