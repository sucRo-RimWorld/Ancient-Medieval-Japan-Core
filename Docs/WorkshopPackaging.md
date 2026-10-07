# Workshop packaging — AMJ shared Golden Path

## Subscriber-only contract

Core, Environment, CCTO and future related Mods ship only what a subscribed
player needs: runtime About metadata/preview/Workshop identity, Defs, Patches,
Languages, production Textures/Sounds/Assemblies, loadFolders.xml where used,
and required license/attribution notices. README and all design/development
information remain on GitHub. License/attribution obligations take priority over
size reduction; add any required third-party notices to the validator contract.

Exclude everything else through root `.rimignore`: Art (all sources/templates),
Docs, Source, Scripts, Tests/fixtures, TestResults, development Quickstarts,
VCS/editor metadata, build/launch tools, local overrides, backups/debug symbols,
and archives. Exclusion preserves repository originals; never delete accepted
sources to reduce an upload. Adding a new item includes classifying it and
updating the exclusion list before publication. Unknown surviving file types or
roots fail the automatic audit until explicitly reviewed.

## YADA syntax and policy ownership

`.rimignore` is the exclusion authority. YADA's actual
[Scanner.cs](https://github.com/zed-0xff/RW-YADA/blob/master/Source/Scanner.cs)
reads nonblank noncomment lines and applies inherited filename/directory-name
patterns at each level, case-insensitively for literal names. This is not Git
ignore syntax: no slash-prefixed paths, `!` exceptions or Git-style `**` rules.
Use `Art` for the complete tree and `_LocalTest.xml` for the nested local patch.
A filename pattern such as `*.pdb` applies at every level. Never exclude `*.dll`:
compiled Environment/CCTO production assemblies are necessary for players.

Core's `.gitattributes`, `.workshopignore`, and `_PublisherPlus.xml` are adapters
of this policy, not separate exceptions. The git-archive path uses generated
export-ignore entries; `.workshopignore` is descriptive and is not assumed to be
honored by the vanilla uploader. Other builders must copy only the same runtime
and legal categories and must audit their final payload. License/attribution
files must not be excluded merely because they are text.

## Repeatable validation and publication

1. Read main AGENTS and Coordination; preserve unrelated local changes. Select
   the intended release source using the owning release/provenance procedure.
2. Run `python Tests/validate_workshop_payload.py`. It models the supported YADA
   basename rules against every tracked file, fails on unnecessary survivors or
   removed runtime/legal files, and runs nested-fixture/path-syntax regressions.
   `--inventory paths.json` permits a remote Git tree audit without fabricating a
   game/build environment. CI runs the same gate on main and PRs, canceling older
   superseded checks. Passing proves filtering only.
3. Build required production DLLs with the owning build/release procedure.
   Core currently uses XML and textures; Environment requires
   `AncientMedievalJapanEnvironment.dll`, CCTO `CropColdToleranceOverhaul.dll`.
   Those compiled outputs may be local/untracked and must not be lost by a
   Git-only archive. Never substitute a test assembly for the production DLL.
4. Stage through the existing publisher or builder, then run
   `python Tests/validate_workshop_payload.py --payload ABSOLUTE_STAGE_PATH`
   (add `--expected-assembly AncientMedievalJapanEnvironment.dll` or
   `--expected-assembly CropColdToleranceOverhaul.dll` for compiled Mods).
   This mode audits every actual file without applying a filter again and fails
   if development material is already present. Keep provenance/manifests/test
   reports outside the subscriber payload. Environment's release loadFolders
   must load only the production root; development runners belong in observers.
5. Use the owning texture/loaded-Def/runtime gates for missing assets and behavior.
   Repository inventory PASS does not establish package completeness, runtime
   PASS, upload success or that the installed Workshop version has changed.
6. Publish only the verified payload to the existing Workshop ID. Re-download
   and audit the subscribed package plus the owning runtime checks. Steam
   publication remains author-manual unless explicitly authorized otherwise.

## Current adapters

- Core: YADA root filter; PublisherPlus adapter; `prepare-workshop.bat` using
  `.gitattributes` and clean-worktree `git archive` (XML-only current payload).
- Environment: YADA root filter; `Scripts/Build-ReleaseCandidate.py` selects only
  runtime/legal files and makes production-root-only loadFolders. The separate
  immutable/provenance release repair in Coordination retains its own owner;
  any replacement builder must apply this subscriber-only contract.
- CCTO: YADA root filter; retain the locally built `Assemblies/` DLL and LICENSE.

Future versioned runtime directories, new asset types or legally required notices
must be explicitly registered in the validator and documented here before release.

## Conditional Grains runtime content

`loadFolders.xml` and `Compatibility/MedievalOverhaul/{Defs,Patches,Languages}` are subscriber runtime content. Keep the complete tree in YADA/export archives; the game loader decides whether MO is active. `Tests/Fixtures/MO_PreSplit_Contracts.json` and XML projection/test scripts remain development-only and excluded.
