param([Parameter(Mandatory = $true)][string]$TargetRoot)
$ErrorActionPreference = 'Stop'
# Legacy fixture metadata only. Production/real-profile loader bytes are untouched.
$path = Join-Path $TargetRoot 'loadFolders.xml'
[xml]$loader = Get-Content -LiteralPath $path -Raw -Encoding UTF8
$entries = @($loader.SelectNodes('/loadFolders/v1.6/li[@IfModActive="DankPyon.Medieval.Overhaul"]'))
if ($entries.Count -ne 2) { throw 'Expected grain and legacy scenario conditional MO load folders.' }
foreach ($entry in $entries) { $entry.SetAttribute('IfModActive', 'sucro.ancientmedievaljapan.core.mofixture') }
$fallback = @($loader.SelectNodes('/loadFolders/v1.6/li[@IfModNotActive="DankPyon.Medieval.Overhaul"]'))
if ($fallback.Count -ne 1) { throw 'Expected one MO-free fallback load folder.' }
$fallback[0].SetAttribute('IfModNotActive', 'sucro.ancientmedievaljapan.core.mofixture')
$loader.Save($path)
