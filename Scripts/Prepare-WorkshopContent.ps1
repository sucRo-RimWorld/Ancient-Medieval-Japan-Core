[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [string]$Ref = "HEAD"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outputFull = [System.IO.Path]::GetFullPath(
    $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDir)
)
$repoPrefix = $repoRoot.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar

if ($outputFull.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Workshop staging output must be outside the source repository: $outputFull"
}

Push-Location $repoRoot
try {
    $status = @(& git status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "git status failed."
    }
    if ($status.Count -gt 0) {
        throw "Refusing Workshop staging from a dirty worktree. Commit/push the intended release state first."
    }

    & git rev-parse --verify "$Ref^{commit}" *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot resolve Git ref: $Ref"
    }

    $archive = Join-Path ([System.IO.Path]::GetTempPath()) ("amjc-workshop-{0}.zip" -f [System.Guid]::NewGuid())
    & git archive --format=zip --output="$archive" $Ref
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $archive)) {
        throw "git archive failed."
    }
}
finally {
    Pop-Location
}

try {
    if (Test-Path $outputFull) {
        Remove-Item -LiteralPath $outputFull -Recurse -Force
    }
    New-Item -ItemType Directory -Path $outputFull -Force | Out-Null
    Expand-Archive -LiteralPath $archive -DestinationPath $outputFull -Force

    $forbidden = Join-Path $outputFull "Art\Sources"
    if (Test-Path $forbidden) {
        throw "FAIL: developer source assets leaked into Workshop staging: $forbidden"
    }

    Write-Host "[PASS] Workshop staging prepared without Art/Sources:"
    Write-Host "       $outputFull"
}
finally {
    if ($archive -and (Test-Path $archive)) {
        Remove-Item -LiteralPath $archive -Force
    }
}
