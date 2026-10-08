param(
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot,

    [ValidateSet('fixture','vanilla','vanilla-ccto','mo','mo-ccto')]
    [string]$Profile = 'fixture',

    [string]$RimWorldRoot,

    [string]$SourceModsConfigPath = "$env:USERPROFILE\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Config\ModsConfig.xml"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SourceModsConfigPath)) {
    Write-Host "[ERROR] RimWorld ModsConfig.xml was not found:" -ForegroundColor Red
    Write-Host "        $SourceModsConfigPath"
    exit 2
}

try {
    [xml]$source = Get-Content -LiteralPath $SourceModsConfigPath -Raw
}
catch {
    Write-Host "[ERROR] Failed to parse the normal RimWorld ModsConfig.xml:" -ForegroundColor Red
    Write-Host "        $($_.Exception.Message)"
    exit 2
}

$required = @(
    "brrainz.harmony",
    "ludeon.rimworld",
    "sucro.ancientmedievaljapan.core.mofixture",
    "sucro.ancientmedievaljapan.core.cctofixture",
    "sucro.ancientmedievaljapan.core.e2etarget",
    "rimworks.rimlogging",
    "rimworks.pickle",
    "rimworks.quickstarts",
    "sucro.ancientmedievaljapan.core.e2e"
)

if ($Profile -ne 'fixture') {
    . (Join-Path $PSScriptRoot 'GrainsTestProfiles.ps1')
    $spec = Get-GrainsTestProfile $Profile
    if (-not $RimWorldRoot) { throw 'RimWorldRoot is required for real Grains profiles.' }
    $installed = @{}
    $scanRoots = @((Join-Path $RimWorldRoot 'Data'), (Join-Path $RimWorldRoot 'Mods'),
        (Join-Path $RimWorldRoot '../../workshop/content/294100'))
    foreach ($scanRoot in $scanRoots) {
        if (-not (Test-Path -LiteralPath $scanRoot)) { continue }
        foreach ($dir in Get-ChildItem -LiteralPath $scanRoot -Directory) {
            $aboutPath = Join-Path $dir.FullName 'About/About.xml'
            if (-not (Test-Path -LiteralPath $aboutPath)) { continue }
            [xml]$metadata = Get-Content -LiteralPath $aboutPath -Raw -Encoding UTF8
            $id = ([string]$metadata.ModMetaData.packageId).Trim().ToLowerInvariant()
            if (-not $id) { continue }
            if ($installed.ContainsKey($id)) {
                $installed[$id].Duplicates += $dir.FullName
            } else {
                $installed[$id] = [pscustomobject]@{ Xml = $metadata; Root = $dir.FullName; Duplicates = @() }
            }
        }
    }
    $required = @(Get-GrainsActiveMods $spec $installed)
    foreach ($id in $required) {
        if ($installed[$id].Duplicates.Count -eq 0) { continue }
        $locations = @($installed[$id].Root) + @($installed[$id].Duplicates)
        # Only CCTO has a defined preference for parallel local/Workshop
        # installations. Do not modify the user's installed mod copies.
        if ($id -ne 'sucro.cropcoldtoleranceoverhaul') {
            throw "Ambiguous installed package $id at $($locations -join ', ')"
        }
        $localRoot = [IO.Path]::GetFullPath((Join-Path $RimWorldRoot 'Mods')) + [IO.Path]::DirectorySeparatorChar
        $localMatches = @($locations | Where-Object {
            [IO.Path]::GetFullPath($_).StartsWith($localRoot, [StringComparison]::OrdinalIgnoreCase)
        })
        if ($localMatches.Count -ne 1) {
            throw "Ambiguous installed CCTO provider; expected exactly one local Mods copy: $($locations -join ', ')"
        }
        $installed[$id].Root = $localMatches[0]
        $installed[$id].Duplicates = @()
        Write-Host "[OK] CCTO has local and Workshop copies; isolated provider manifest selects local Mods: $($localMatches[0])"
    }
    New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
    @($required | ForEach-Object { [pscustomobject]@{ PackageId = $_; Root = $installed[$_].Root } }) |
        ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $OutputRoot 'providers.json') -Encoding UTF8
}

$configDir = Join-Path $OutputRoot "Config"
$configPath = Join-Path $configDir "ModsConfig.xml"
$sourceConfigDir = Split-Path -Parent $SourceModsConfigPath
$sourcePrefsPath = Join-Path $sourceConfigDir "Prefs.xml"
$testPrefsPath = Join-Path $configDir "Prefs.xml"
$devModeDisabledPath = Join-Path $configDir "DevModeDisabled"

New-Item -ItemType Directory -Force -Path $configDir | Out-Null

if (Test-Path -LiteralPath $devModeDisabledPath) {
    Remove-Item -LiteralPath $devModeDisabledPath -Force
}

$doc = New-Object System.Xml.XmlDocument
$declaration = $doc.CreateXmlDeclaration("1.0", "utf-8", $null)
$null = $doc.AppendChild($declaration)

$root = $doc.CreateElement("ModsConfigData")
$null = $doc.AppendChild($root)

$version = $doc.CreateElement("version")
$version.InnerText = [string]$source.ModsConfigData.version
$null = $root.AppendChild($version)

$activeMods = $doc.CreateElement("activeMods")
foreach ($packageId in $required) {
    $li = $doc.CreateElement("li")
    $li.InnerText = $packageId
    $null = $activeMods.AppendChild($li)
}
$null = $root.AppendChild($activeMods)

$knownExpansions = $doc.CreateElement("knownExpansions")
foreach ($expansion in @($source.ModsConfigData.knownExpansions.li)) {
    $value = ([string]$expansion).Trim()
    if ([string]::IsNullOrWhiteSpace($value)) {
        continue
    }

    $li = $doc.CreateElement("li")
    $li.InnerText = $value
    $null = $knownExpansions.AppendChild($li)
}
$null = $root.AppendChild($knownExpansions)

$settings = New-Object System.Xml.XmlWriterSettings
$settings.Indent = $true
$settings.Encoding = New-Object System.Text.UTF8Encoding($false)

$writer = [System.Xml.XmlWriter]::Create($configPath, $settings)
try {
    $doc.Save($writer)
}
finally {
    $writer.Dispose()
}

if (-not (Test-Path -LiteralPath $sourcePrefsPath)) {
    Write-Host "[ERROR] RimWorld Prefs.xml was not found:" -ForegroundColor Red
    Write-Host "        $sourcePrefsPath"
    exit 2
}

try {
    [xml]$prefs = Get-Content -LiteralPath $sourcePrefsPath -Raw
}
catch {
    Write-Host "[ERROR] Failed to parse RimWorld Prefs.xml:" -ForegroundColor Red
    Write-Host "        $($_.Exception.Message)"
    exit 2
}

$devModeNode = $prefs.SelectSingleNode("//devMode")
if ($null -eq $devModeNode) {
    $devModeNode = $prefs.CreateElement("devMode")
    $devModeNode.InnerText = "True"
    $null = $prefs.DocumentElement.AppendChild($devModeNode)
}
else {
    $devModeNode.InnerText = "True"
}

$writer = [System.Xml.XmlWriter]::Create($testPrefsPath, $settings)
try {
    $prefs.Save($writer)
}
finally {
    $writer.Dispose()
}

Write-Host "[OK] Prepared isolated AMJ test save-data profile."
Write-Host "     $OutputRoot"
Write-Host "[OK] The normal RimWorld ModsConfig.xml was not changed."
Write-Host ""
Write-Host "Active test mods:"
foreach ($packageId in $required) {
    Write-Host "  - $packageId"
}

exit 0
