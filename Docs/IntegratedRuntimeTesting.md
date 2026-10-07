# Core + Environment rendered, isolated-desktop runtime gate

For the four real-provider Grains migration profiles, use
[`GrainsProfileTesting.md`](GrainsProfileTesting.md) and `run-grains-tests.bat`.
The existing Core entry point below retains the historical fixture suite.

## Known-good Windows procedure

Run from the Core repository in a normal user session with Steam running:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File Scripts/IntegratedRuntimeDesktop/Run-AMJ-IsolatedDesktop.ps1
```

The companion `run-amj-gates.cmd` targets the development installation at
`D:\SteamLibrary\steamapps\common\RimWorld`. Adjust its two repository directories
for a different installation. It calls Core `run-e2e.bat`, then Environment
`run-runtime-tests.bat`, serially, and propagates failure. The latter includes
build/static validation, six base Quickstarts, the optional installed CCTO
compatibility run, and the installed MO tree-reference static audit.

The launcher creates a unique WinSta0 desktop with CreateDesktop and assigns
STARTUPINFO.lpDesktop to the child runner. It never switches the user's input
desktop. This is Windows desktop isolation, not an X11 virtual framebuffer or
an independent virtual monitor. No Xvfb, Wine, display driver or VM is installed.
RimWorld retains normal Direct3D rendering; neither `-nographics` nor headless
mode is used. Enumerated window process IDs prove the game windows reside on
the isolated desktop. The existing isolated SaveData/log paths, assertion
requirements and ERROR gates are preserved.

API references:
- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopw
- https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow

The launcher waits without changing the active desktop, retains the desktop
handle until the child runner exits, closes handles in `finally`, and kills
its own process tree on outer failure/timeout. The batch output is saved beside
the launcher as ignored `automated-gates.log`; canonical per-test reports remain
under each repository's TestResults. Do not run concurrent gates using those
same report directories.

## Failure prevention

Before rebuilding Environment, finish or close any authorized interactive
Environment review instance. The 2026-10-05 saved-launcher rerun initially
stopped at CS0016 because the Haimatsu snow-review game held the output DLL.
After that instance exited, the saved launcher passed both full gates again.
Do not classify a DLL file lock as a source compilation defect or terminate
an unrelated review instance without authorization.

1. Windows PowerShell must discover its own modules. The runner sets PSModulePath
   only for itself and descendants to the Windows PowerShell system module root.
   Inheriting the Codex PowerShell 7 module search order caused Get-FileHash to
   disappear in the original child scripts. Do not globally change PSModulePath.
2. A restricted/low-integrity game process can fail SteamAPI.Init and then fail
   to discover Workshop helpers. Use normal user execution, with the same user
   session as Steam. Missing AbstractQuickstart in that case is not proof of an
   AMJ source/API defect. Keep runtime errors fatal.
3. Pickle scenario continuations can arrive on a worker thread. AMJ texture and
   live map assertions are Task-returning steps posted through PickleDriver.Post.
   RuntimeThread asserts UnityData.IsInMainThread before accessing Unity/Verse,
   and propagates assertion failures through the returned Task. Existing actual
   texture, stack-material and five-villager assertions remain the regression.
4. Empty desktop window enumeration at process exit is normal. Read the child
   exit code rather than treating that enumeration as a test failure.
5. Python reads of repository text explicitly use UTF-8, including New Village
   Japanese design text, so the static gate does not depend on Windows CP932.

## Verified result, 2026-10-05 JST

Core: 7/7 Pickle scenarios, no skipped scenarios, zero isolated runtime ERRORs.
Environment base assertions: WarmTemperate 58/58, CoolTemperate 57/57,
Subalpine 54/54, Alpine 52/52, River 3/3, Coast 3/3. CCTO: 70/70.
All Environment reports have preLaunchErrors=0, complete live capture and no
truncation; the repository runtime ERROR validators passed. Overall child exit 0.
PowerShell syntax, Environment build/static, exact PNG copy and MO 8-tree /
15-reference static audit passed. Core Python and installed-source PowerShell
static validation passed as well.

The first private-desktop Core run reproduced the worker-thread failures; the
corrected run passed the unchanged assertions. Production Defs, art and normal
saves/configuration were not changed by this test work. Environment was tested
with the pre-existing local uncommitted plant-review changes; this is not a
claim about pristine GitHub main. Full MO runtime and a combined Core+Environment
in-game profile are not added by these two existing entry points. Visual-review
ledger acceptance is separate. Changes from this task remain local/uncommitted.

## Publication scope

The verified 7-scenario and Environment counts above belong to the earlier local
working tree. These tooling fixes were subsequently transplanted onto GitHub
main while preserving its newer 8-scenario suite and all other changes. The
newer Environment Core-profile gameplay-contract gate was not part of the
recorded runtime run. No new-main runtime PASS is inferred from that history.
