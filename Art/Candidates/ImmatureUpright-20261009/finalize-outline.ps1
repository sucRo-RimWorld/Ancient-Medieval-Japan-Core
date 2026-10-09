. "$PSScriptRoot/normalize-outline.ps1"
$finalDir = Join-Path $PSScriptRoot 'Final'
New-Item -ItemType Directory -Path $finalDir -Force | Out-Null
foreach ($asset in $manifest.assets.PSObject.Properties) {
 $name = $asset.Name + '.png'
 [void][GrainOutlinePalette]::Export((Join-Path $PSScriptRoot "Exports/$name"),(Join-Path $finalDir $name))
}
