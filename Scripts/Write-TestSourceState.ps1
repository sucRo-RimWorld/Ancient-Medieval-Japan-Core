param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [ValidateSet('fixture','vanilla','vanilla-ccto','mo','mo-ccto')]
    [string]$Profile = 'fixture'
)

$ErrorActionPreference = "Stop"
$RepositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("sourceRoot=$RepositoryRoot")
$lines.Add("profile=$Profile")
$lines.Add("generatedAt=$([DateTimeOffset]::Now.ToString('o'))")

$gitHead = $null
try {
    $gitOutput = & git -C $RepositoryRoot rev-parse HEAD 2>$null
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace([string]$gitOutput)) {
        $gitHead = ([string]$gitOutput).Trim()
    }
}
catch {
    $gitHead = $null
}
if ([string]::IsNullOrWhiteSpace($gitHead)) {
    $gitHead = "unavailable"
}
$lines.Add("gitHead=$gitHead")

$trackedFiles = @(
    "Tests\E2E\StageASteps.cs",
    "Tests\E2E\TestMod\Pickle\Features\stage-a.feature",
    "Defs\ThingDefs_Plants\Plants_StageA.xml",
    "Defs\ThingDefs_Items\Items_StageA_Grains.xml",
    "Defs\RecipeDefs\Recipes_GrainProcessing.xml",
    "Patches\Compatibility\CCTO_StageA.xml",
    "Compatibility\MedievalOverhaul\Patches\MedievalOverhaul_StageA_Wheat.xml",
    "Compatibility\MedievalOverhaul\Patches\MedievalOverhaul_StageA_Base.xml",
    "Compatibility\MedievalOverhaul\Defs\Recipes_MOWheat.xml",
    "loadFolders.xml",
    "BaseWithoutMO\Defs\Plants_Wheat.xml",
    "BaseWithoutMO\Defs\Items_Wheat.xml",
    "BaseWithoutMO\Defs\Items_Flour.xml",
    "BaseWithoutMO\Defs\Recipes_Wheat.xml",
    "BaseWithoutMO\Defs\Recipes_Milling.xml",
    "BaseWithoutMO\Defs\Buildings_Millstone.xml",
    "BaseWithoutMO\Patches\CCTO_Wheat.xml",
    "Defs\RecipeDefs\Recipes_GrainsMilling.xml",
    "Defs\RecipeDefs\Recipes_GrainsFood.xml",
    "Defs\ThingDefs_Items\Items_GrainsFlour.xml",
    "Defs\ThingDefs_Items\Items_GrainsFood.xml",
    "Defs\ThoughtDefs\Thoughts_GrainsFood.xml",
    "Compatibility\MedievalOverhaul\Patches\MedievalOverhaul_GrainsFlour.xml",
    "Compatibility\MedievalOverhaul\Patches\MedievalOverhaul_GrainsMillstone.xml",
    "Tests\E2E\NewVillageSteps.cs",
    "Defs\Scenarios\Scenarios_NewVillage.xml",
    "Defs\PawnKindDefs\PawnKinds_Villager.xml",
    "Defs\ThingDefs_Buildings\Buildings_GrainProcessing.xml",
    "Scripts\Prepare-FixtureLoadFolders.ps1"
)

if ($Profile -ne 'fixture') {
    $trackedFiles = @($trackedFiles | Where-Object { $_ -ne 'Tests\E2E\TestMod\Pickle\Features\stage-a.feature' }) + @(
        'Tests\E2E\GrainsProfileSteps.cs', 'Tests\E2E\GrainsSimulationSteps.cs', "Tests\E2E\Profiles\grains-$Profile.feature",
        'Scripts\GrainsTestProfiles.ps1', 'Scripts\Stage-GrainsTestProfile.ps1',
        'Scripts\Run-GrainsProfiles.ps1', 'Scripts\Prepare-TestSaveData.ps1', 'build-e2e.bat'
    )
}

foreach ($relativePath in $trackedFiles) {
    $fullPath = Join-Path $RepositoryRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath)) {
        throw "Required source-state file was not found: $fullPath"
    }
    $hash = (Get-FileHash -LiteralPath $fullPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $key = ($relativePath -replace '\\','/')
    $lines.Add("sha256[$key]=$hash")
}

$featurePath = Join-Path $RepositoryRoot "Tests\E2E\TestMod\Pickle\Features\stage-a.feature"
if ($Profile -ne 'fixture') { $featurePath = Join-Path $RepositoryRoot "Tests/E2E/Profiles/grains-$Profile.feature" }
foreach ($line in Get-Content -LiteralPath $featurePath -Encoding UTF8) {
    if ($line -match '^\s*Scenario:\s*(.+)$') {
        $lines.Add("feature=$($Matches[1].Trim())")
    }
}

$parent = Split-Path -Parent $OutputPath
if (-not [string]::IsNullOrWhiteSpace($parent)) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
}

[System.IO.File]::WriteAllLines(
    $OutputPath,
    $lines,
    (New-Object System.Text.UTF8Encoding($false))
)

Write-Host "[OK] Wrote AMJ E2E source-state metadata:"
Write-Host "     $OutputPath"
exit 0
