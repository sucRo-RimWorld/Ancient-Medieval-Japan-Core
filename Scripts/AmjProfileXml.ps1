# Explicit AMJ-owned XML projection only; not a substitute for RimWorld loading.
function Get-AmjProfileXml([string]$RepositoryRoot, [string]$Profile = 'mo') {
    if ($Profile -notin @('vanilla','mo')) { throw "Unknown XML profile: $Profile" }
    [xml]$doc = '<Defs/>'
    $folders = @((Join-Path $RepositoryRoot 'Defs'))
    if ($Profile -eq 'mo') { $folders += Join-Path $RepositoryRoot 'Compatibility/MedievalOverhaul/Defs' }
    foreach ($folder in $folders) {
        foreach ($file in Get-ChildItem -LiteralPath $folder -Recurse -File -Filter *.xml | Sort-Object FullName) {
            [xml]$source = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
            foreach ($node in $source.DocumentElement.ChildNodes) {
                if ($node.NodeType -eq 'Element') { [void]$doc.DocumentElement.AppendChild($doc.ImportNode($node, $true)) }
            }
        }
    }
    if ($Profile -eq 'mo') {
        [xml]$patch = Get-Content -LiteralPath (Join-Path $RepositoryRoot 'Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_StageA_Base.xml') -Raw -Encoding UTF8
        foreach ($operation in $patch.Patch.Operation) {
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
