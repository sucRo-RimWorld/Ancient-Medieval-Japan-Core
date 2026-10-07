param(
    [Parameter(Mandatory = $true)][string]$SummaryPath,
    [Parameter(Mandatory = $true)][ValidateSet('vanilla','vanilla-ccto','mo','mo-ccto')][string]$Profile
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'GrainsTestProfiles.ps1')
$spec = Get-GrainsTestProfile $Profile
if (-not (Test-Path -LiteralPath $SummaryPath)) { throw "Missing fresh summary: $SummaryPath" }
$summary = Get-Content -LiteralPath $SummaryPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($summary.total -ne 3 -or $summary.passed -ne 3 -or $summary.failed -ne 0 -or $summary.skipped -ne 0) {
    throw "Profile $Profile requires exactly 3/3 passes with no failures/skips."
}
$names = @($summary.scenarios | ForEach-Object { [string]$_.name })
foreach ($name in $spec.Scenarios) {
    if (@($names | Where-Object { $_ -eq $name }).Count -ne 1) { throw "Expected exactly one scenario: $name" }
}
Write-Host "[OK] $Profile fresh migration smoke summary 3/3. This is not the full Grains release gate."
