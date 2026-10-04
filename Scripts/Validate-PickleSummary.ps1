param(
    [Parameter(Mandatory = $true)]
    [string]$SummaryPath
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $SummaryPath)) {
    Fail "Pickle summary was not produced: $SummaryPath"
}

try {
    $summary = Get-Content -LiteralPath $SummaryPath -Raw -Encoding UTF8 | ConvertFrom-Json
}
catch {
    Fail "Failed to parse Pickle summary: $($_.Exception.Message)"
}

$required = @(
    "Loaded AMJ Stage A crop and grain Defs match the design values",
    "Loaded Awa CCTO compatibility data matches the AMJC cold tolerance design",
    "Loaded AMJ grain processing buildings and recipes match the design values",
    "Thirteen raw millet is conserved through bulk plus remainder processing",
    "Edible millet is accepted by the vanilla simple meal ingredient filter"
)

if ([int]$summary.total -ne 5) {
    Fail "AMJ Stage A integration suite scenario count is $($summary.total), expected 5."
}

if ([int]$summary.passed -ne 5 -or [int]$summary.failed -ne 0 -or [int]$summary.skipped -ne 0) {
    Fail "AMJ Stage A integration suite is not a clean 5/5 pass. passed=$($summary.passed), failed=$($summary.failed), skipped=$($summary.skipped)"
}

$names = @($summary.scenarios | ForEach-Object { [string]$_.name })
foreach ($scenario in $required) {
    if ($names -notcontains $scenario) {
        Fail "Required AMJ scenario is missing from Pickle summary: $scenario"
    }
}

Write-Host "[OK] Fresh AMJ Pickle summary contains all 5 required passing scenarios." -ForegroundColor Green
exit 0
