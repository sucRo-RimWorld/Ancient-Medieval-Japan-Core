# A profile-independent fingerprint of production bytes and the complete E2E harness.
# Do not include machine paths, timestamps, git HEAD, reports or design documents.
function Get-GrainsSourceState([string]$RepositoryRoot) {
    $root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
    $paths = New-Object 'System.Collections.Generic.List[string]'
    foreach ($folder in @('About','Defs','Patches','BaseWithoutMO','Compatibility',
        'LegacyStartingScenarios','Languages','Textures','Tests/E2E','Scripts')) {
        $directory = Join-Path $root $folder
        if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
            throw "Required source-state directory was not found: $directory"
        }
        foreach ($file in Get-ChildItem -LiteralPath $directory -File -Recurse) {
            if ($file.FullName -match '[\\/]__pycache__[\\/]' -or $file.Extension -eq '.pyc') { continue }
            $paths.Add(($file.FullName.Substring($root.Length + 1) -replace '\\','/'))
        }
    }
    foreach ($path in @('loadFolders.xml','build-e2e.bat','run-grains-tests.bat')) {
        if (-not (Test-Path -LiteralPath (Join-Path $root $path) -PathType Leaf)) {
            throw "Required source-state file was not found: $path"
        }
        $paths.Add($path)
    }
    $ordered = [string[]]$paths.ToArray()
    [Array]::Sort($ordered, [StringComparer]::Ordinal)
    $lines = New-Object 'System.Collections.Generic.List[string]'
    foreach ($path in $ordered) {
        $hash = (Get-FileHash -LiteralPath (Join-Path $root $path) -Algorithm SHA256).Hash.ToLowerInvariant()
        $lines.Add("sha256[$path]=$hash")
    }
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes([string]::Join("`n", $lines.ToArray()) + "`n")
        $digest = ([BitConverter]::ToString($algorithm.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    } finally { $algorithm.Dispose() }
    [pscustomobject]@{ Hash = $digest; Lines = $lines.ToArray() }
}

function Assert-GrainsSourceState([string]$RepositoryRoot, [string]$ExpectedHash) {
    $current = Get-GrainsSourceState $RepositoryRoot
    if ($current.Hash -ne $ExpectedHash) {
        throw "Grains source changed during the profile matrix. Expected $ExpectedHash; found $($current.Hash). Rerun the requested profiles from one unchanged source snapshot."
    }
}
