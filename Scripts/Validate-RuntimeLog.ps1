param(
    [Parameter(Mandatory = $true)]
    [string]$LogPath,

    [Parameter(Mandatory = $true)]
    [string]$ModIdPrefixes
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $LogPath)) {
    Fail "Runtime log was not produced: $LogPath"
}

$text = Get-Content -LiteralPath $LogPath -Raw -Encoding UTF8
$prefixes = @(
    $ModIdPrefixes.Split(';') |
        ForEach-Object { $_.Trim().ToLowerInvariant() } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
)

if ($prefixes.Count -eq 0) {
    Fail "No mod-id prefixes were supplied for runtime log validation."
}

$errors = New-Object System.Collections.Generic.List[string]
$blocks = [regex]::Matches(
    $text,
    '(?ms)^Timestamp:\s*.*?(?=^Timestamp:\s*|\z)'
)

foreach ($match in $blocks) {
    $block = $match.Value
    if ($block -notmatch '(?m)^Level:\s*ERROR\s*$') {
        continue
    }

    $idMatch = [regex]::Match($block, '(?mi)^mod_id:\s*([^\r\n]+)')
    $channelMatch = [regex]::Match($block, '(?mi)^Channel:\s*Mod\.([^\r\n]+)')

    $candidates = @()
    if ($idMatch.Success) {
        $candidates += $idMatch.Groups[1].Value.Trim().ToLowerInvariant()
    }
    if ($channelMatch.Success) {
        $candidates += $channelMatch.Groups[1].Value.Trim().ToLowerInvariant()
    }

    foreach ($candidate in $candidates) {
        $owned = $false
        foreach ($prefix in $prefixes) {
            if ($candidate.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $owned = $true
                break
            }
        }

        if ($owned) {
            $errors.Add($block.Trim())
            break
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "[FAIL] AMJ Core-origin runtime ERROR entries were found:" -ForegroundColor Red
    $limit = [Math]::Min($errors.Count, 5)
    for ($i = 0; $i -lt $limit; $i++) {
        Write-Host ""
        Write-Host $errors[$i]
    }
    if ($errors.Count -gt $limit) {
        Write-Host ""
        Write-Host "... plus $($errors.Count - $limit) more AMJ Core runtime ERROR entries."
    }
    exit 1
}

Write-Host "[OK] No AMJ Core-origin runtime ERROR entries were found." -ForegroundColor Green
exit 0
