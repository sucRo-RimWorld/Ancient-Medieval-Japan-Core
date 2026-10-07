# Explicit AMJ-owned XML projection only; not a substitute for RimWorld loading.
function Get-AmjProfileXml([string]$RepositoryRoot, [string]$Profile = 'mo') {
    if ($Profile -notin @('vanilla','mo')) { throw "Unknown XML profile: $Profile" }
    [xml]$doc = '<Defs/>'
    $folders = @((Join-Path $RepositoryRoot 'Defs'), (Join-Path $RepositoryRoot 'LegacyStartingScenarios/Defs'))
    if ($Profile -eq 'mo') { $folders += Join-Path $RepositoryRoot 'Compatibility/MedievalOverhaul/Defs' }
    else { $folders += Join-Path $RepositoryRoot 'BaseWithoutMO/Defs' }
    foreach ($folder in $folders) {
        foreach ($file in Get-ChildItem -LiteralPath $folder -Recurse -File -Filter *.xml | Sort-Object FullName) {
            [xml]$source = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
            foreach ($node in $source.DocumentElement.ChildNodes) {
                if ($node.NodeType -eq 'Element') { [void]$doc.DocumentElement.AppendChild($doc.ImportNode($node, $true)) }
            }
        }
    }
    if ($Profile -eq 'mo') {
        $operations = @()
        foreach ($name in @('MedievalOverhaul_StageA_Base.xml','MedievalOverhaul_GrainsFlour.xml')) {
            [xml]$patch = Get-Content -LiteralPath (Join-Path $RepositoryRoot ("Compatibility/MedievalOverhaul/Patches/$name")) -Raw -Encoding UTF8
            $operations += @($patch.Patch.Operation)
        }
        [xml]$legacyPatch = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'LegacyStartingScenarios/Compatibility/MedievalOverhaul/Patches/StartingScenarios.xml') -Raw -Encoding UTF8
        $operations += @($legacyPatch.Patch.Operation)
        foreach ($operation in $operations) {
            $targets = @($doc.SelectNodes([string]$operation.xpath))
            if ($targets.Count -ne 1) { throw "Expected one AMJ-owned patch target: $($operation.xpath)" }
            $target = $targets[0]
            if ($operation.Class -eq 'PatchOperationAdd') {
                foreach ($node in $operation.value.ChildNodes) {
                    if ($node.NodeType -eq 'Element') { [void]$target.AppendChild($doc.ImportNode($node, $true)) }
                }
            } elseif ($operation.Class -eq 'PatchOperationReplace') {
                $parent = $target.ParentNode
                foreach ($node in $operation.value.ChildNodes) {
                    if ($node.NodeType -eq 'Element') { [void]$parent.InsertBefore($doc.ImportNode($node, $true), $target) }
                }
                [void]$parent.RemoveChild($target)
            } else { throw "Unsupported static Base-difference operation: $($operation.Class)" }
        }
    }
    return $doc
}
