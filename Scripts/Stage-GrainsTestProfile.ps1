param(
    [Parameter(Mandatory = $true)][string]$RepositoryRoot,
    [Parameter(Mandatory = $true)][string]$ModsRoot,
    [Parameter(Mandatory = $true)][ValidateSet('vanilla','vanilla-ccto','mo','mo-ccto')][string]$Profile
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'GrainsTestProfiles.ps1')
$spec = Get-GrainsTestProfile $Profile
$RepositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$target = Join-Path $ModsRoot 'AncientMedievalJapanCore.E2ETarget'
$test = Join-Path $ModsRoot 'AncientMedievalJapanCore.E2E'

# Stage a disposable target; production About.xml and all runtime bytes stay intact.
foreach ($path in @($target, $test)) {
    if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Recurse -Force }
    New-Item -ItemType Directory -Force -Path (Join-Path $path 'About') | Out-Null
}
foreach ($folder in @('Defs','Patches','Textures','Languages','Compatibility','Assemblies','1.6')) {
    $source = Join-Path $RepositoryRoot $folder
    if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination $target -Recurse }
}
foreach ($file in @('loadFolders.xml','LoadFolders.xml')) {
    $source = Join-Path $RepositoryRoot $file
    if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination $target; break }
}
[xml]$about = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'About/About.xml') -Raw -Encoding UTF8
$about.ModMetaData.name = '[DEV] AMJ Grains E2E Target'
$about.ModMetaData.packageId = 'sucro.ancientmedievaljapan.core.e2etarget'
$about.ModMetaData.description = 'Test-only staged runtime copy; dependency metadata differs during Grains migration. Do not publish.'
foreach ($node in @($about.ModMetaData.SelectNodes('modDependencies|loadAfter'))) {
    [void]$about.ModMetaData.RemoveChild($node)
}
$after = $about.CreateElement('loadAfter')
foreach ($id in $spec.Providers) {
    $li = $about.CreateElement('li'); $li.InnerText = $id; [void]$after.AppendChild($li)
}
[void]$about.ModMetaData.AppendChild($after)
$about.Save((Join-Path $target 'About/About.xml'))
Copy-Item -LiteralPath (Join-Path $RepositoryRoot 'Tests/E2E/TestMod/About/About.xml') -Destination (Join-Path $test 'About/About.xml')
foreach ($folder in @('Assemblies','Pickle/Assemblies','Pickle/Features')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $test $folder) | Out-Null
}
Copy-Item -LiteralPath (Join-Path $RepositoryRoot "Tests/E2E/Profiles/$($spec.Feature)") -Destination (Join-Path $test 'Pickle/Features')
$spec | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $test 'profile.json') -Encoding UTF8
Write-Host "[OK] Staged $Profile with unchanged runtime Def/Patch/texture bytes; no API fixtures or graphics substitutions."
