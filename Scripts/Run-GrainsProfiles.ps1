param(
    [Parameter(Mandatory = $true)][string]$RimWorldRoot,
    [ValidateSet('all','vanilla','vanilla-ccto','mo','mo-ccto')][string]$Profile = 'all'
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'GrainsTestProfiles.ps1')
. (Join-Path $PSScriptRoot 'GrainsSourceState.ps1')
$repo = Split-Path -Parent $PSScriptRoot
$profiles = @($Profile)
if ($Profile -eq 'all') { $profiles = @('vanilla','vanilla-ccto','mo','mo-ccto') }
$matrixRoot = Join-Path $repo 'TestResults/Grains'
New-Item -ItemType Directory -Force -Path $matrixRoot | Out-Null
$matrix = New-Object 'System.Collections.Generic.List[object]'
$lock = [IO.File]::Open((Join-Path $matrixRoot 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $sourceState = Get-GrainsSourceState $repo
    Write-Host "[OK] Grains matrix source SHA256: $($sourceState.Hash)"
    @("sourceSnapshotHash=$($sourceState.Hash)") + @($sourceState.Lines) |
        Set-Content -LiteralPath (Join-Path $matrixRoot 'matrix-source-state.txt') -Encoding UTF8
    $matrixPath = Join-Path $matrixRoot 'matrix.json'
    if (Test-Path -LiteralPath $matrixPath) { Remove-Item -LiteralPath $matrixPath -Force }
    foreach ($name in $profiles) {
        $spec = Get-GrainsTestProfile $name
        $root = Join-Path $matrixRoot $name
        if (Test-Path -LiteralPath $root) { Remove-Item -LiteralPath $root -Recurse -Force }
        $report = Join-Path $root 'Pickle'
        $savedata = Join-Path $root 'SaveData'
        $log = Join-Path $report 'Player.log'
        New-Item -ItemType Directory -Force -Path $report | Out-Null
        $result = 2
        $launched = $false
        $diagnostic = ''
        try {
            Assert-GrainsSourceState $repo $sourceState.Hash
            & (Join-Path $repo 'build-e2e.bat') $RimWorldRoot $name
            if ($LASTEXITCODE -ne 0) { throw "Build failed: $LASTEXITCODE" }
            & (Join-Path $PSScriptRoot 'Prepare-TestSaveData.ps1') -OutputRoot $savedata -Profile $name -RimWorldRoot $RimWorldRoot
            if ($LASTEXITCODE -ne 0) { throw "Profile preparation failed: $LASTEXITCODE" }
            & (Join-Path $PSScriptRoot 'Write-TestSourceState.ps1') -RepositoryRoot $repo -OutputPath (Join-Path $report 'source-state.txt') -Profile $name
            if ($LASTEXITCODE -ne 0) { throw "Source-state capture failed: $LASTEXITCODE" }
            $recordedHash = @(Get-Content -LiteralPath (Join-Path $report 'source-state.txt') |
                Where-Object { $_ -like 'sourceSnapshotHash=*' })
            if ($recordedHash.Count -ne 1 -or $recordedHash[0] -ne "sourceSnapshotHash=$($sourceState.Hash)") {
                throw 'Profile source attribution does not match the matrix snapshot.'
            }
            Copy-Item -LiteralPath (Join-Path $savedata 'providers.json') -Destination $report
            $testRoot = Join-Path $RimWorldRoot 'Mods/AncientMedievalJapanCore.E2E'
            Copy-Item -LiteralPath (Join-Path $testRoot 'profile.json') -Destination $report
            # Hash the complete staged payload, compiled steps and installed provider bytes.
            $hashes = @()
            $payloads = @((Join-Path $RimWorldRoot 'Mods/AncientMedievalJapanCore.E2ETarget'), $testRoot)
            $providers = Get-Content -LiteralPath (Join-Path $report 'providers.json') -Raw -Encoding UTF8 | ConvertFrom-Json
            $payloads += @($providers | Where-Object { $_.PackageId -notlike 'ludeon.*' } | ForEach-Object { $_.Root })
            foreach ($payload in @($payloads | Select-Object -Unique)) {
                foreach ($file in Get-ChildItem -LiteralPath $payload -File -Recurse) {
                    $hashes += "$((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant())  $($file.FullName)"
                }
            }
            $hashes | Set-Content -LiteralPath (Join-Path $report 'payload-sha256.txt') -Encoding UTF8
            if (-not (Test-Path -LiteralPath (Join-Path $RimWorldRoot 'RimWorldWin64.exe'))) { throw 'RimWorld executable missing.' }
            $launched = $true
            & (Join-Path $PSScriptRoot 'Run-RimWorldWithTimeout.ps1') -ExePath (Join-Path $RimWorldRoot 'RimWorldWin64.exe') -SavedataFolder $savedata -ReportDir $report -LogPath $log -RunFilter $spec.Feature -TimeoutSeconds 540 -PickleRunTimeoutMinutes 7
            $result = $LASTEXITCODE
        } catch { $diagnostic = $_.Exception.Message; Write-Host "[ERROR] $name - $diagnostic"; $result = 2 }

        # Evaluate both gates even on a failing process/scenario run. Never accept stale reports.
        if ($launched) {
            try { & (Join-Path $PSScriptRoot 'Validate-GrainsPickleSummary.ps1') -SummaryPath (Join-Path $report 'summary.json') -Profile $name }
            catch { Write-Host "[FAIL] $($_.Exception.Message)"; if ($result -eq 0) { $result = 2 } }
            try {
                & (Join-Path $PSScriptRoot 'Validate-RuntimeLog.ps1') -LogPath $log -ModIdPrefixes 'sucro.ancientmedievaljapan.core' -FailOnAnyError
                if ($LASTEXITCODE -ne 0 -and $result -eq 0) { $result = 2 }
            } catch { Write-Host "[FAIL] $($_.Exception.Message)"; if ($result -eq 0) { $result = 2 } }
        }
        try { Assert-GrainsSourceState $repo $sourceState.Hash }
        catch { $diagnostic = $_.Exception.Message; Write-Host "[FAIL] $diagnostic"; $result = 2 }
        $matrix.Add([pscustomobject]@{ Profile = $name; Launched = $launched; ExitCode = $result; Diagnostic = $diagnostic; Report = $report; SourceHash = $sourceState.Hash })
        $matrix | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $matrixRoot 'matrix.json') -Encoding UTF8
    }
} finally { $lock.Dispose() }
if (@($matrix | Where-Object { $_.ExitCode -ne 0 }).Count -gt 0) { exit 2 }
exit 0
