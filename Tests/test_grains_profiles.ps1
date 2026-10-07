$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
. (Join-Path $repo 'Scripts/GrainsTestProfiles.ps1')
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
    $game = Join-Path $temp 'RimWorld'
    $mods = Join-Path $game 'Mods'
    New-Item -ItemType Directory -Force -Path $mods | Out-Null
    $originalAbout = (Get-FileHash -LiteralPath (Join-Path $repo 'About/About.xml')).Hash
    $sourceConfig = Join-Path $temp 'UserConfig'
    New-Item -ItemType Directory -Force -Path $sourceConfig | Out-Null
    '<ModsConfigData><version>1.6.4633</version><activeMods><li>unrelated.player.mod</li></activeMods><knownExpansions><li>ludeon.rimworld.royalty</li></knownExpansions></ModsConfigData>' |
        Set-Content -LiteralPath (Join-Path $sourceConfig 'ModsConfig.xml')
    '<PrefsData><devMode>False</devMode></PrefsData>' | Set-Content -LiteralPath (Join-Path $sourceConfig 'Prefs.xml')
    $sourceHash = (Get-FileHash -LiteralPath (Join-Path $sourceConfig 'ModsConfig.xml')).Hash
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
    foreach ($profile in @('vanilla','vanilla-ccto','mo','mo-ccto')) {
        $spec = Get-GrainsTestProfile $profile
        & (Join-Path $repo 'Scripts/Stage-GrainsTestProfile.ps1') -RepositoryRoot $repo -ModsRoot $mods -Profile $profile
        $target = Join-Path $mods 'AncientMedievalJapanCore.E2ETarget'
        Assert (-not (Test-Path (Join-Path $target 'Patches/E2E_Graphics.xml'))) 'Graphics substitutions leaked into real profile.'
        foreach ($folder in @('Defs','Patches','Textures','Languages','Compatibility','BaseWithoutMO')) {
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
        @{total=6;passed=6;failed=0;skipped=0;scenarios=@($spec.Scenarios | ForEach-Object { @{name=$_} })} |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
        & (Join-Path $repo 'Scripts/Validate-GrainsPickleSummary.ps1') -SummaryPath $summaryPath -Profile $profile
        $statePath = Join-Path $temp 'source-state.txt'
        & (Join-Path $repo 'Scripts/Write-TestSourceState.ps1') -RepositoryRoot $repo -OutputPath $statePath -Profile $profile
        $state = Get-Content -LiteralPath $statePath
        Assert ($state -contains "profile=$profile") 'Source attribution has the wrong profile.'
        Assert (@($state | Where-Object { $_ -like 'feature=*' }).Count -eq 6) 'Source attribution lists the legacy suite.'
        @{total=6;passed=6;failed=0;skipped=0;scenarios=@(@{name='wrong suite'})} |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
        MustFail { & (Join-Path $repo 'Scripts/Validate-GrainsPickleSummary.ps1') -SummaryPath $summaryPath -Profile $profile } 'Unrelated summary was accepted.'
    }
    & (Join-Path $repo 'Scripts/Prepare-FixtureLoadFolders.ps1') -TargetRoot $target
    [xml]$fixtureLoader = Get-Content -LiteralPath (Join-Path $target 'loadFolders.xml') -Raw
    Assert ($fixtureLoader.loadFolders.'v1.6'.li[1].IfModActive -eq 'sucro.ancientmedievaljapan.core.mofixture') 'Legacy fixture condition was not isolated.'
    Assert ($fixtureLoader.loadFolders.'v1.6'.li[2].IfModNotActive -eq 'sucro.ancientmedievaljapan.core.mofixture') 'Legacy fixture failed to exclude fallback content.'
    [xml]$productionLoader = Get-Content -LiteralPath (Join-Path $repo 'loadFolders.xml') -Raw
    Assert ($productionLoader.loadFolders.'v1.6'.li[1].IfModActive -eq 'DankPyon.Medieval.Overhaul') 'Fixture condition leaked into production.'
    . (Join-Path $repo 'Scripts/AmjProfileXml.ps1')
    foreach ($xmlProfile in @('vanilla','mo')) {
        $projection = Get-AmjProfileXml $repo $xmlProfile
        $table = $projection.SelectSingleNode("/Defs/ThingDef[defName='AMJC_GrainProcessingTable']")
        $metal = if ($xmlProfile -eq 'mo') { 'DankPyon_IronIngot' } else { 'Steel' }
        Assert ($table.costList.SelectSingleNode($metal).InnerText -eq '30') 'Projected processing table material differs.'
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
    MustFail { Get-GrainsTestProfile 'invalid' } 'Invalid profile was accepted.'
    Write-Host '[OK] Four-profile staging/config/summary/negative regressions PASS (no RimWorld runtime claim).'
} finally { Remove-Item -LiteralPath $temp -Recurse -Force }
