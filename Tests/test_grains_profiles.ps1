$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
. (Join-Path $repo 'Scripts/GrainsTestProfiles.ps1')
. (Join-Path $repo 'Scripts/GrainsSourceState.ps1')
function Assert([bool]$Condition, [string]$Message) { if (-not $Condition) { throw $Message } }
function MustFail([scriptblock]$Action, [string]$Message) {
    $failed = $false
    try { & $Action } catch { $failed = $true }
    Assert $failed $Message
}
function Metadata([string]$Id, [string[]]$Deps = @(), [string[]]$After = @()) {
    [xml]$xml = '<ModMetaData><name>Test</name><packageId/><modDependencies/><loadAfter/></ModMetaData>'
    $xml.ModMetaData.packageId = $Id
    foreach ($id in $Deps) {
        $li = $xml.CreateElement('li'); $packageNode = $xml.CreateElement('packageId'); $packageNode.InnerText = $id
        [void]$li.AppendChild($packageNode); [void]$xml.SelectSingleNode('/ModMetaData/modDependencies').AppendChild($li)
    }
    foreach ($id in $After) {
        $li = $xml.CreateElement('li'); $li.InnerText = $id; [void]$xml.SelectSingleNode('/ModMetaData/loadAfter').AppendChild($li)
    }
    return $xml
}
$temp = Join-Path ([IO.Path]::GetTempPath()) ('AMJ-Grains-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $temp | Out-Null
try {
    # Match the real Steam folder structure; keep the fake Workshop copy
    # inside this test's disposable directory, not a shared temp parent.
    $game = Join-Path $temp 'steamapps/common/RimWorld'
    $mods = Join-Path $game 'Mods'
    $workshop = Join-Path $temp 'steamapps/workshop/content/294100'
    New-Item -ItemType Directory -Force -Path $mods | Out-Null
    New-Item -ItemType Directory -Force -Path $workshop | Out-Null
    $originalAbout = (Get-FileHash -LiteralPath (Join-Path $repo 'About/About.xml')).Hash
    $sourceConfig = Join-Path $temp 'UserConfig'
    New-Item -ItemType Directory -Force -Path $sourceConfig | Out-Null
    '<ModsConfigData><version>1.6.4633</version><activeMods><li>unrelated.player.mod</li></activeMods><knownExpansions><li>ludeon.rimworld.royalty</li></knownExpansions></ModsConfigData>' |
        Set-Content -LiteralPath (Join-Path $sourceConfig 'ModsConfig.xml')
    '<PrefsData><devMode>False</devMode></PrefsData>' | Set-Content -LiteralPath (Join-Path $sourceConfig 'Prefs.xml')
    $sourceHash = (Get-FileHash -LiteralPath (Join-Path $sourceConfig 'ModsConfig.xml')).Hash
    $expectedState = Get-GrainsSourceState $repo
    $baseIds = @('brrainz.harmony','ludeon.rimworld','rimworks.rimlogging','rimworks.pickle','rimworks.quickstarts')
    foreach ($id in $baseIds + @('oskarpotocki.vanillafactionsexpanded.core','syrchalis.processor.framework',
        'dankpyon.medieval.overhaul','sucro.cropcoldtoleranceoverhaul','unrelated.player.mod')) {
        $aboutDir = Join-Path $mods "$id/About"
        New-Item -ItemType Directory -Force -Path $aboutDir | Out-Null
        $deps = @()
        if ($id -eq 'dankpyon.medieval.overhaul') { $deps = @('brrainz.harmony','oskarpotocki.vanillafactionsexpanded.core','syrchalis.processor.framework') }
        if ($id -eq 'sucro.cropcoldtoleranceoverhaul') { $deps = @('brrainz.harmony') }
        (Metadata $id $deps).Save((Join-Path $aboutDir 'About.xml'))
    }
    # Simulate the user's simultaneous CCTO local + Workshop installs
    # without modifying their actual installation or normal mod list.
    $duplicateCcto = Join-Path $workshop '3812412548/About'
    New-Item -ItemType Directory -Force -Path $duplicateCcto | Out-Null
    Copy-Item -LiteralPath (Join-Path $mods 'sucro.cropcoldtoleranceoverhaul/About/About.xml') -Destination (Join-Path $duplicateCcto 'About.xml')
    foreach ($profile in @('vanilla','vanilla-ccto','mo','mo-ccto')) {
        $spec = Get-GrainsTestProfile $profile
        & (Join-Path $repo 'Scripts/Stage-GrainsTestProfile.ps1') -RepositoryRoot $repo -ModsRoot $mods -Profile $profile
        $target = Join-Path $mods 'AncientMedievalJapanCore.E2ETarget'
        Assert (-not (Test-Path (Join-Path $target 'Patches/E2E_Graphics.xml'))) 'Graphics substitutions leaked into real profile.'
        foreach ($folder in @('Defs','Patches','Textures','Languages','Compatibility','BaseWithoutMO','LegacyStartingScenarios')) {
            foreach ($file in Get-ChildItem -LiteralPath (Join-Path $repo $folder) -File -Recurse) {
                $relative = $file.FullName.Substring($repo.Length + 1)
                Assert ((Get-FileHash -LiteralPath $file.FullName).Hash -eq (Get-FileHash -LiteralPath (Join-Path $target $relative)).Hash) "Runtime bytes changed: $relative"
            }
        }
        Assert ((Get-FileHash -LiteralPath (Join-Path $repo 'loadFolders.xml')).Hash -eq (Get-FileHash -LiteralPath (Join-Path $target 'loadFolders.xml')).Hash) 'Production loader changed in real profile.'
        [xml]$about = Get-Content -LiteralPath (Join-Path $target 'About/About.xml') -Raw
        Assert ($null -eq $about.ModMetaData.modDependencies) 'Staged target still requires MO.'
        $featureDir = Join-Path $mods 'AncientMedievalJapanCore.E2E/Pickle/Features'
        Assert (@(Get-ChildItem -LiteralPath $featureDir -Filter *.feature).Count -eq 1) 'Stale feature remained.'
        Assert (Test-Path (Join-Path $featureDir $spec.Feature)) 'Wrong profile feature staged.'
        $output = Join-Path $temp $profile
        & (Join-Path $repo 'Scripts/Prepare-TestSaveData.ps1') -OutputRoot $output -Profile $profile -RimWorldRoot $game -SourceModsConfigPath (Join-Path $sourceConfig 'ModsConfig.xml')
        Assert ($LASTEXITCODE -eq 0) 'Config generation failed.'
        # In Windows PowerShell 5.1, piping ConvertFrom-Json directly into
        # @() can retain the entire JSON array as one object. Deserialize first
        # and enumerate its individual PackageId/Root records deliberately.
        $manifestText = Get-Content -LiteralPath (Join-Path $output 'providers.json') -Raw -Encoding UTF8
        $resolved = ConvertFrom-Json -InputObject $manifestText
        $cctoRecords = @($resolved | Where-Object { $_.PackageId -eq 'sucro.cropcoldtoleranceoverhaul' })
        Assert ($cctoRecords.Count -eq [int]$spec.UseCCTO) 'Unexpected CCTO manifest presence.'
        if ($spec.UseCCTO) {
            $providerPath = $cctoRecords[0].Root
            Assert ($providerPath -is [string]) 'CCTO manifest must contain one path string, not a wrapped JSON array.'
            $chosen = [IO.Path]::GetFullPath($providerPath)
            $expected = [IO.Path]::GetFullPath((Join-Path $mods 'sucro.cropcoldtoleranceoverhaul'))
            Assert ($chosen -eq $expected) 'CCTO duplicate resolution did not select the local installed copy.'
        }
        [xml]$config = Get-Content -LiteralPath (Join-Path $output 'Config/ModsConfig.xml') -Raw
        $active = @($config.ModsConfigData.activeMods.li)
        Assert (($active -contains 'dankpyon.medieval.overhaul') -eq $spec.UseMO) 'MO presence mismatch.'
        Assert (($active -contains 'sucro.cropcoldtoleranceoverhaul') -eq $spec.UseCCTO) 'CCTO presence mismatch.'
        Assert (@($active | Where-Object { $_ -like '*fixture' -or $_ -like 'ludeon.rimworld.*' -or $_ -eq 'unrelated.player.mod' }).Count -eq 0) 'Unexpected mods became active.'
        Assert ([array]::IndexOf($active,'sucro.ancientmedievaljapan.core.e2etarget') -lt [array]::IndexOf($active,'sucro.ancientmedievaljapan.core.e2e')) 'Target must load before steps.'
        foreach ($id in $spec.Providers) {
            Assert ([array]::IndexOf($active,$id) -lt [array]::IndexOf($active,'sucro.ancientmedievaljapan.core.e2etarget')) 'Real provider must load before target.'
        }
        $summaryPath = Join-Path $temp 'summary.json'
        @{total=$spec.Scenarios.Count;passed=$spec.Scenarios.Count;failed=0;skipped=0;scenarios=@($spec.Scenarios | ForEach-Object { @{name=$_} })} |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
        & (Join-Path $repo 'Scripts/Validate-GrainsPickleSummary.ps1') -SummaryPath $summaryPath -Profile $profile
        @{total=8;passed=8;failed=0;skipped=0;scenarios=@($spec.Scenarios | ForEach-Object { @{name=$_} }) + @(@{name='removed village definition'},@{name='removed village start'})} |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
        MustFail { & (Join-Path $repo 'Scripts/Validate-GrainsPickleSummary.ps1') -SummaryPath $summaryPath -Profile $profile } 'Old eight-scenario combined-owner summary was accepted.'
        $statePath = Join-Path $temp 'source-state.txt'
        & (Join-Path $repo 'Scripts/Write-TestSourceState.ps1') -RepositoryRoot $repo -OutputPath $statePath -Profile $profile
        $state = Get-Content -LiteralPath $statePath
        Assert ($state -contains "profile=$profile") 'Source attribution has the wrong profile.'
        Assert ($state -contains "sourceSnapshotHash=$($expectedState.Hash)") 'Profile source fingerprint differs.'
        foreach ($relative in @('Patches/UplandRice.xml',
            'Languages/Japanese/DefInjected/ThingDef/AMJC_RiceProcessing.xml',
            'Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png',
            'Tests/E2E/Profiles/grains-mo-ccto.feature')) {
            Assert (@($state | Where-Object { $_.StartsWith("sha256[$relative]=") }).Count -eq 1) "Missing or duplicate source witness: $relative"
        }
        Assert (@($state | Where-Object { $_ -like 'feature=*' }).Count -eq $spec.Scenarios.Count) 'Source attribution lists the legacy suite.'
        @{total=$spec.Scenarios.Count;passed=$spec.Scenarios.Count;failed=0;skipped=0;scenarios=@(@{name='wrong suite'})} |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
        MustFail { & (Join-Path $repo 'Scripts/Validate-GrainsPickleSummary.ps1') -SummaryPath $summaryPath -Profile $profile } 'Unrelated summary was accepted.'
    }
    # An unrelated duplicate required provider must remain an error.
    $ambiguousMO = Join-Path $workshop '9999999999/About'
    New-Item -ItemType Directory -Force -Path $ambiguousMO | Out-Null
    Copy-Item -LiteralPath (Join-Path $mods 'dankpyon.medieval.overhaul/About/About.xml') -Destination (Join-Path $ambiguousMO 'About.xml')
    MustFail {
        & (Join-Path $repo 'Scripts/Prepare-TestSaveData.ps1') -OutputRoot (Join-Path $temp 'ambiguous-MO') -Profile 'mo' -RimWorldRoot $game -SourceModsConfigPath (Join-Path $sourceConfig 'ModsConfig.xml')
    } 'An unrelated duplicate MO provider was silently selected.'
    Remove-Item -LiteralPath (Split-Path -Parent $ambiguousMO) -Recurse -Force
    & (Join-Path $repo 'Scripts/Prepare-FixtureLoadFolders.ps1') -TargetRoot $target
    [xml]$fixtureLoader = Get-Content -LiteralPath (Join-Path $target 'loadFolders.xml') -Raw
    Assert ($fixtureLoader.loadFolders.'v1.6'.li[1].IfModActive -eq 'sucro.ancientmedievaljapan.core.mofixture') 'Legacy fixture condition was not isolated.'
    Assert ($fixtureLoader.loadFolders.'v1.6'.li[2].IfModNotActive -eq 'sucro.ancientmedievaljapan.core.mofixture') 'Legacy fixture failed to exclude fallback content.'
    Assert ($fixtureLoader.loadFolders.'v1.6'.li[4].IfModActive -eq 'sucro.ancientmedievaljapan.core.mofixture') 'Legacy scenario MO patch condition was not isolated.'
    foreach ($index in @(3,4)) {
        Assert ($fixtureLoader.loadFolders.'v1.6'.li[$index].IfModNotActive -eq 'sucro.ancientmedievaljapan.scenarios') 'Independent scenario exclusion guard was lost.'
    }
    [xml]$productionLoader = Get-Content -LiteralPath (Join-Path $repo 'loadFolders.xml') -Raw
    Assert ($productionLoader.loadFolders.'v1.6'.li[1].IfModActive -eq 'DankPyon.Medieval.Overhaul') 'Fixture condition leaked into production.'
    . (Join-Path $repo 'Scripts/AmjProfileXml.ps1')
    foreach ($xmlProfile in @('vanilla','mo')) {
        $projection = Get-AmjProfileXml $repo $xmlProfile
        $table = $projection.SelectSingleNode("/Defs/ThingDef[defName='AMJC_GrainProcessingTable']")
        $steel = $table.SelectSingleNode('costList/Steel')
        Assert ($null -ne $steel -and $steel.InnerText -eq '30' -and
            $table.SelectNodes('costList/*').Count -eq 1) 'AMJG processing table must keep Steel 30 in both profiles.'
        Assert ($null -eq $table.SelectSingleNode('researchPrerequisites')) 'AMJG processing table must stay research-free.'
        $barley = $projection.SelectSingleNode("/Defs/ThingDef[defName='AMJC_Plant_Barley']")
        Assert ($null -ne $barley -and $null -eq $barley.SelectSingleNode('plant/sowResearchPrerequisites')) 'AMJG barley must stay research-free.'
        $research = $projection.SelectNodes("/Defs/ScenarioDef[defName='AMJC_NewVillage']/scenario/parts/li[@Class='ScenPart_StartingResearch']")
        $expected = if ($xmlProfile -eq 'mo') { 3 } else { 0 }
        Assert ($research.Count -eq $expected) 'Projected scenario research differs.'
    }
    Assert ((Get-FileHash -LiteralPath (Join-Path $repo 'About/About.xml')).Hash -eq $originalAbout) 'Production metadata changed.'
    Assert ((Get-FileHash -LiteralPath (Join-Path $sourceConfig 'ModsConfig.xml')).Hash -eq $sourceHash) 'Player config changed.'
    $installed = @{}
    foreach ($id in $baseIds + @('sucro.ancientmedievaljapan.core.e2etarget','sucro.ancientmedievaljapan.core.e2e')) {
        $installed[$id] = [pscustomobject]@{ Xml = (Metadata $id) }
    }
    MustFail { Get-GrainsActiveMods (Get-GrainsTestProfile 'mo') $installed } 'Missing MO was accepted.'
    $installed['rimworks.pickle'].Xml = Metadata 'rimworks.pickle' @('dankpyon.medieval.overhaul')
    MustFail { Get-GrainsActiveMods (Get-GrainsTestProfile 'vanilla') $installed } 'Vanilla accepted transitive MO dependency.'
    $installed['rimworks.pickle'].Xml = Metadata 'rimworks.pickle' @('rimworks.quickstarts')
    $installed['rimworks.quickstarts'].Xml = Metadata 'rimworks.quickstarts' @('rimworks.pickle')
    MustFail { Get-GrainsActiveMods (Get-GrainsTestProfile 'vanilla') $installed } 'Dependency cycle was accepted.'
    $installed['rimworks.pickle'].Xml = Metadata 'rimworks.pickle' @() @('rimworks.quickstarts')
    $installed['rimworks.quickstarts'].Xml = Metadata 'rimworks.quickstarts' @() @('rimworks.pickle')
    MustFail { Get-GrainsActiveMods (Get-GrainsTestProfile 'vanilla') $installed } 'Active load-order cycle was accepted.'
    # Pickle run-wide timeouts are in minutes, scenario timeouts in seconds.
    $launcherSource = Get-Content -LiteralPath (Join-Path $repo 'Scripts/Run-RimWorldWithTimeout.ps1') -Raw
    $runnerSource = Get-Content -LiteralPath (Join-Path $repo 'Scripts/Run-GrainsProfiles.ps1') -Raw
    Assert ($launcherSource.Contains('[int]$PickleRunTimeoutMinutes = 4')) 'Legacy Pickle timeout default changed.'
    Assert ($launcherSource.Contains("'-pickle-run-timeout={0}'")) 'Pickle run-wide option missing.'
    $runMatch = [regex]::Match($runnerSource, '-TimeoutSeconds\s+(\d+)\s+-PickleRunTimeoutMinutes\s+(\d+)')
    Assert $runMatch.Success 'Grains runner must set both timeout budgets.'
    $processSeconds = [int]$runMatch.Groups[1].Value
    $runSeconds = [int]$runMatch.Groups[2].Value * 60
    Assert ($processSeconds -gt $runSeconds) 'Process watchdog can preempt the Pickle run cap.'
    Assert ($processSeconds * 4 -lt 40 * 60) 'Four-profile maximum exceeds the desktop watchdog.'
    foreach ($profile in @('vanilla','vanilla-ccto','mo','mo-ccto')) {
        $feature = Get-Content -LiteralPath (Join-Path $repo "Tests/E2E/Profiles/grains-$profile.feature") -Raw
        $scenarioTimeout = [regex]::Match($feature, '@timeout:(\d+)')
        Assert $scenarioTimeout.Success "Production scenario timeout is missing: $profile"
        Assert ($runSeconds -gt [int]$scenarioTimeout.Groups[1].Value) "Pickle run cap is shorter than the production scenario: $profile"
    }

    MustFail { Get-GrainsTestProfile 'invalid' } 'Invalid profile was accepted.'
    # Same bytes at a different installation path must produce the same hash.
    # Reports/docs/mtime must not affect it; additions, deletions, renames and
    # edits of actual runtime/localization/graphics/harness bytes must affect it.
    $snapshot = Join-Path $temp 'source-snapshot'
    New-Item -ItemType Directory -Force -Path $snapshot | Out-Null
    foreach ($folder in @('About','Defs','Patches','BaseWithoutMO','Compatibility',
        'LegacyStartingScenarios','Languages','Textures','Scripts')) {
        Copy-Item -LiteralPath (Join-Path $repo $folder) -Destination $snapshot -Recurse
    }
    New-Item -ItemType Directory -Force -Path (Join-Path $snapshot 'Tests') | Out-Null
    Copy-Item -LiteralPath (Join-Path $repo 'Tests/E2E') -Destination (Join-Path $snapshot 'Tests') -Recurse
    foreach ($path in @('loadFolders.xml','build-e2e.bat','run-grains-tests.bat')) {
        Copy-Item -LiteralPath (Join-Path $repo $path) -Destination $snapshot
    }
    Assert ((Get-GrainsSourceState $snapshot).Hash -eq $expectedState.Hash) 'Machine path contaminated source fingerprint.'
    New-Item -ItemType Directory -Force -Path (Join-Path $snapshot 'TestResults') | Out-Null
    'unrelated report' | Set-Content -LiteralPath (Join-Path $snapshot 'TestResults/matrix.json')
    'unrelated documentation' | Set-Content -LiteralPath (Join-Path $snapshot 'README.md')
    Assert-GrainsSourceState $snapshot $expectedState.Hash
    foreach ($relative in @('Patches/UplandRice.xml',
        'Languages/Japanese/DefInjected/ThingDef/AMJC_RiceProcessing.xml',
        'Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png',
        'Tests/E2E/GrainsSimulationSteps.cs', 'Tests/E2E/Profiles/grains-mo-ccto.feature',
        'Scripts/Run-GrainsProfiles.ps1', 'About/About.xml')) {
        $path = Join-Path $snapshot $relative
        $original = [IO.File]::ReadAllBytes($path)
        [IO.File]::WriteAllBytes($path, [byte[]](@($original) + @(0)))
        MustFail { Assert-GrainsSourceState $snapshot $expectedState.Hash } "Changed source was accepted: $relative"
        [IO.File]::WriteAllBytes($path, $original)
        (Get-Item -LiteralPath $path).LastWriteTimeUtc = [DateTime]::UtcNow
        Assert-GrainsSourceState $snapshot $expectedState.Hash
    }
    $added = Join-Path $snapshot 'Textures/new-runtime-asset.png'
    [IO.File]::WriteAllBytes($added, [byte[]]@(1,2,3))
    MustFail { Assert-GrainsSourceState $snapshot $expectedState.Hash } 'Added runtime file was accepted.'
    $beforeRename = (Get-GrainsSourceState $snapshot).Hash
    Move-Item -LiteralPath $added -Destination (Join-Path $snapshot 'Textures/renamed-runtime-asset.png')
    Assert ((Get-GrainsSourceState $snapshot).Hash -ne $beforeRename) 'Changed path was accepted.'
    Remove-Item -LiteralPath (Join-Path $snapshot 'Textures/renamed-runtime-asset.png')
    Assert-GrainsSourceState $snapshot $expectedState.Hash
    $ricePatch = Join-Path $snapshot 'Patches/UplandRice.xml'
    Remove-Item -LiteralPath $ricePatch
    MustFail { Assert-GrainsSourceState $snapshot $expectedState.Hash } 'Deleted runtime file was accepted.'
    Assert ($runnerSource.Contains('Assert-GrainsSourceState $repo $sourceState.Hash')) 'Matrix does not reject source drift.'
    Assert ($runnerSource.Contains('SourceHash = $sourceState.Hash')) 'Matrix omits its source evidence.'
    Write-Host '[OK] Four-profile staging/config/summary/negative regressions PASS (no RimWorld runtime claim).'
} finally { Remove-Item -LiteralPath $temp -Recurse -Force }
