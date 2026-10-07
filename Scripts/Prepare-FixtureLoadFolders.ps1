param([Parameter(Mandatory = $true)][string]$TargetRoot)
$ErrorActionPreference = 'Stop'
# Legacy fixture metadata only. Production/real-profile loader bytes are untouched.
$path = Join-Path $TargetRoot 'loadFolders.xml'
[xml]$loader = Get-Content -LiteralPath $path -Raw -Encoding UTF8
$entries = @($loader.SelectNodes('/loadFolders/v1.6/li[@IfModActive="DankPyon.Medieval.Overhaul"]'))
if ($entries.Count -ne 1) { throw 'Expected one conditional MO load folder.' }
$entries[0].SetAttribute('IfModActive', 'sucro.ancientmedievaljapan.core.mofixture')
$loader.Save($path)
