param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,
    [Parameter(Mandatory = $true)]
    [string]$MedievalOverhaulRoot,
    [string]$RimWorldRoot = ""
)
$ErrorActionPreference = "Stop"
$Invariant = [System.Globalization.CultureInfo]::InvariantCulture

function Fail([string]$Message) {
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    exit 1
}

function Load-Xml([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { Fail "Required file was not found: $Path" }
    try { return [xml](Get-Content -LiteralPath $Path -Raw -Encoding UTF8) }
    catch { Fail "Failed to parse XML '$Path': $($_.Exception.Message)" }
}

function Node-Text($Node, [string]$XPath, [string]$Context) {
    $value = $Node.SelectSingleNode($XPath)
    if ($null -eq $value) { Fail "$Context is missing XPath '$XPath'." }
    return $value.InnerText.Trim()
}

function Assert-Text([string]$Actual, [string]$Expected, [string]$Context) {
    if ($Actual -ne $Expected) { Fail "$Context expected '$Expected', got '$Actual'." }
}

function Assert-Number([string]$ActualText, [double]$Expected, [string]$Context) {
    $actual = 0.0
    if (-not [double]::TryParse($ActualText, [System.Globalization.NumberStyles]::Float, $Invariant, [ref]$actual)) { Fail "$Context is not numeric: '$ActualText'." }
    if ([math]::Abs($actual - $Expected) -gt 0.0001) { Fail "$Context expected $Expected, got $actual." }
}

function Get-DefNode($Xml, [string]$TypeName, [string]$DefName) {
    $node = $Xml.SelectSingleNode("/Defs/$TypeName[defName='$DefName']")
    if ($null -eq $node) { Fail "Required $TypeName '$DefName' was not found." }
    return $node
}

$RepositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path
# Decode actual image bytes; signature/dimensions alone miss truncated IDAT exports.
Add-Type -AssemblyName System.Drawing
foreach ($texture in Get-ChildItem -LiteralPath (Join-Path $RepositoryRoot "Textures") -Filter *.png -Recurse -File) {
    # GDI+ may tolerate truncated data; enforce complete chunk boundaries first.
    $bytes = [System.IO.File]::ReadAllBytes($texture.FullName)
    $offset = 8L
    $ended = $false
    while ($offset -lt $bytes.Length) {
        if ($offset + 12 -gt $bytes.Length) { Fail "Truncated PNG chunk header: $($texture.FullName)" }
        $length = ([long]$bytes[$offset] * 16777216) + ([long]$bytes[$offset + 1] * 65536) + ([long]$bytes[$offset + 2] * 256) + $bytes[$offset + 3]
        $end = $offset + 12 + $length
        if ($end -gt $bytes.Length) { Fail "Truncated PNG chunk ($length declared bytes): $($texture.FullName)" }
        $kind = [System.Text.Encoding]::ASCII.GetString($bytes, [int]($offset + 4), 4)
        if ($kind -eq "IEND") {
            if ($length -ne 0 -or $end -ne $bytes.Length) { Fail "Invalid PNG end: $($texture.FullName)" }
            $ended = $true
        }
        $offset = $end
    }
    if (-not $ended) { Fail "Missing PNG end: $($texture.FullName)" }
    $stream = [System.IO.File]::OpenRead($texture.FullName)
    $image = $null
    try {
        $image = [System.Drawing.Image]::FromStream($stream, $false, $true)
        $bitmap = New-Object System.Drawing.Bitmap($image)
        try { $null = $bitmap.GetPixel(0, 0) }
        finally { $bitmap.Dispose() }
    }
    catch { Fail "PNG decode failed: $($texture.FullName): $($_.Exception.Message)" }
    finally {
        if ($null -ne $image) { $image.Dispose() }
        $stream.Dispose()
    }
}
$about = Load-Xml (Join-Path $RepositoryRoot "About\About.xml")
$plants = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Plants\Plants_StageA.xml")
$items = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Items\Items_StageA_Grains.xml")
$buildings = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Buildings\Buildings_GrainProcessing.xml")
$recipes = Load-Xml (Join-Path $RepositoryRoot "Defs\RecipeDefs\Recipes_GrainProcessing.xml")
$cctoPatch = Load-Xml (Join-Path $RepositoryRoot "Patches\Compatibility\CCTO_StageA.xml")
$wheatPatch = Load-Xml (Join-Path $RepositoryRoot "Patches\MedievalOverhaul_StageA_Wheat.xml")

Assert-Text (Node-Text $about "/ModMetaData/packageId" "About.xml packageId") "sucro.ancientmedievaljapan.core" "About.xml packageId"
if ($null -eq $about.SelectSingleNode("/ModMetaData/modDependencies/li[packageId='DankPyon.Medieval.Overhaul']")) { Fail "About.xml must require Medieval Overhaul." }

$awa = Get-DefNode $plants "ThingDef" "AMJC_Plant_FoxtailMillet_Awa"
Assert-Text (Node-Text $awa "plant/harvestedThingDef" "Awa harvest target") "AMJC_RawMillet" "Awa harvest target"
Assert-Number (Node-Text $awa "plant/harvestYield" "Awa harvestYield") 13 "Awa harvestYield"
Assert-Number (Node-Text $awa "plant/growDays" "Awa growDays") 6 "Awa growDays"
Assert-Number (Node-Text $awa "plant/fertilityMin" "Awa fertilityMin") 0.5 "Awa fertilityMin"
Assert-Number (Node-Text $awa "plant/fertilitySensitivity" "Awa fertilitySensitivity") 0.4 "Awa fertilitySensitivity"
Assert-Number (Node-Text $awa "plant/minGrowthTemperature" "Awa minGrowthTemperature") 8 "Awa minGrowthTemperature"
Assert-Number (Node-Text $awa "plant/maxGrowthTemperature" "Awa maxGrowthTemperature") 42 "Awa maxGrowthTemperature"

$hie = Get-DefNode $plants "ThingDef" "AMJC_Plant_BarnyardMillet_Hie"
Assert-Text (Node-Text $hie "plant/harvestedThingDef" "Hie harvest target") "AMJC_RawMillet" "Hie harvest target"
Assert-Number (Node-Text $hie "plant/harvestYield" "Hie harvestYield") 12 "Hie harvestYield"
Assert-Number (Node-Text $hie "plant/growDays" "Hie growDays") 6 "Hie growDays"
Assert-Number (Node-Text $hie "plant/fertilityMin" "Hie fertilityMin") 0.5 "Hie fertilityMin"
Assert-Number (Node-Text $hie "plant/fertilitySensitivity" "Hie fertilitySensitivity") 0.5 "Hie fertilitySensitivity"
Assert-Number (Node-Text $hie "plant/minGrowthTemperature" "Hie minGrowthTemperature") 5 "Hie minGrowthTemperature"
Assert-Number (Node-Text $hie "plant/maxGrowthTemperature" "Hie maxGrowthTemperature") 40 "Hie maxGrowthTemperature"
Assert-Number (Node-Text $hie "plant/minOptimalGrowthTemperature" "Hie minOptimalGrowthTemperature") 15 "Hie minOptimalGrowthTemperature"
Assert-Number (Node-Text $hie "plant/maxOptimalGrowthTemperature" "Hie maxOptimalGrowthTemperature") 30 "Hie maxOptimalGrowthTemperature"

$kibi = Get-DefNode $plants "ThingDef" "AMJC_Plant_ProsoMillet_Kibi"
Assert-Text (Node-Text $kibi "plant/harvestedThingDef" "Kibi harvest target") "AMJC_RawMillet" "Kibi harvest target"
Assert-Number (Node-Text $kibi "plant/harvestYield" "Kibi harvestYield") 11 "Kibi harvestYield"
Assert-Number (Node-Text $kibi "plant/growDays" "Kibi growDays") 5 "Kibi growDays"
Assert-Number (Node-Text $kibi "plant/fertilityMin" "Kibi fertilityMin") 0.5 "Kibi fertilityMin"
Assert-Number (Node-Text $kibi "plant/fertilitySensitivity" "Kibi fertilitySensitivity") 0.3 "Kibi fertilitySensitivity"
Assert-Number (Node-Text $kibi "plant/minGrowthTemperature" "Kibi minGrowthTemperature") 8 "Kibi minGrowthTemperature"
Assert-Number (Node-Text $kibi "plant/maxGrowthTemperature" "Kibi maxGrowthTemperature") 42 "Kibi maxGrowthTemperature"
Assert-Number (Node-Text $kibi "plant/minOptimalGrowthTemperature" "Kibi minOptimalGrowthTemperature") 18 "Kibi minOptimalGrowthTemperature"
Assert-Number (Node-Text $kibi "plant/maxOptimalGrowthTemperature" "Kibi maxOptimalGrowthTemperature") 32 "Kibi maxOptimalGrowthTemperature"

$soba = Get-DefNode $plants "ThingDef" "AMJC_Plant_Buckwheat_Soba"
Assert-Text (Node-Text $soba "plant/harvestedThingDef" "Soba harvest target") "AMJC_RawBuckwheat" "Soba harvest target"
Assert-Number (Node-Text $soba "plant/harvestYield" "Soba harvestYield") 8 "Soba harvestYield"
Assert-Number (Node-Text $soba "plant/growDays" "Soba growDays") 4 "Soba growDays"
Assert-Number (Node-Text $soba "plant/fertilityMin" "Soba fertilityMin") 0.4 "Soba fertilityMin"
Assert-Number (Node-Text $soba "plant/fertilitySensitivity" "Soba fertilitySensitivity") 0.25 "Soba fertilitySensitivity"
Assert-Number (Node-Text $soba "plant/minGrowthTemperature" "Soba minGrowthTemperature") 5 "Soba minGrowthTemperature"
Assert-Number (Node-Text $soba "plant/maxGrowthTemperature" "Soba maxGrowthTemperature") 35 "Soba maxGrowthTemperature"
Assert-Number (Node-Text $soba "plant/minOptimalGrowthTemperature" "Soba minOptimalGrowthTemperature") 12 "Soba minOptimalGrowthTemperature"
Assert-Number (Node-Text $soba "plant/maxOptimalGrowthTemperature" "Soba maxOptimalGrowthTemperature") 25 "Soba maxOptimalGrowthTemperature"
Assert-Number (Node-Text $soba "plant/sowMinSkill" "Soba sowMinSkill") 1 "Soba sowMinSkill"

$barley = Get-DefNode $plants "ThingDef" "AMJC_Plant_Barley"
Assert-Text (Node-Text $barley "plant/harvestedThingDef" "Barley harvest target") "AMJC_RawBarley" "Barley harvest target"
Assert-Number (Node-Text $barley "plant/harvestYield" "Barley harvestYield") 22 "Barley harvestYield"
Assert-Number (Node-Text $barley "plant/growDays" "Barley growDays") 10 "Barley growDays"
Assert-Number (Node-Text $barley "plant/fertilityMin" "Barley fertilityMin") 0.5 "Barley fertilityMin"
Assert-Number (Node-Text $barley "plant/fertilitySensitivity" "Barley fertilitySensitivity") 0.6 "Barley fertilitySensitivity"
Assert-Number (Node-Text $barley "plant/minGrowthTemperature" "Barley minGrowthTemperature") 0 "Barley minGrowthTemperature"
Assert-Number (Node-Text $barley "plant/maxGrowthTemperature" "Barley maxGrowthTemperature") 35 "Barley maxGrowthTemperature"
Assert-Number (Node-Text $barley "plant/minOptimalGrowthTemperature" "Barley minOptimalGrowthTemperature") 5 "Barley minOptimalGrowthTemperature"
Assert-Number (Node-Text $barley "plant/maxOptimalGrowthTemperature" "Barley maxOptimalGrowthTemperature") 22 "Barley maxOptimalGrowthTemperature"
Assert-Number (Node-Text $barley "plant/sowMinSkill" "Barley sowMinSkill") 2 "Barley sowMinSkill"
Assert-Text (Node-Text $barley "plant/sowResearchPrerequisites/li" "Barley research prerequisite") "DankPyon_BasicAgriculture" "Barley research prerequisite"

foreach ($case in @(
    @{ DefName = "AMJC_Plant_FoxtailMillet_Awa"; Death = -3 },
    @{ DefName = "AMJC_Plant_BarnyardMillet_Hie"; Death = -2 },
    @{ DefName = "AMJC_Plant_ProsoMillet_Kibi"; Death = -3 },
    @{ DefName = "AMJC_Plant_Buckwheat_Soba"; Death = -2 },
    @{ DefName = "AMJC_Plant_Barley"; Death = -8 }
)) {
    $xpathText = '/Defs/ThingDef[defName="' + $case.DefName + '"]'
    $op = $cctoPatch.SelectSingleNode("/Patch/Operation[@Class='PatchOperationFindMod'][mods/li='Crop Cold Tolerance Overhaul'][match/xpath='$xpathText']")
    if ($null -eq $op) { Fail "CCTO_StageA.xml is missing the patch for $($case.DefName)." }
    $extension = $op.SelectSingleNode("match/value/li[@Class='CropColdToleranceOverhaul.ColdToleranceExtension']")
    if ($null -eq $extension) { Fail "$($case.DefName) is missing ColdToleranceExtension." }
    Assert-Number (Node-Text $extension "coldDeathTemperature" "$($case.DefName) coldDeathTemperature") ([double]$case.Death) "$($case.DefName) coldDeathTemperature"
    $dormancy = $extension.SelectSingleNode("coldDormancy")
    if ($null -ne $dormancy -and $dormancy.InnerText.Trim().ToLowerInvariant() -ne "false") { Fail "$($case.DefName) must not enable cold dormancy." }
}

Assert-Text (Node-Text $awa "graphicData/graphicClass" "Awa mature graphic class") "Graphic_Random" "Awa mature graphic class"
Assert-Text (Node-Text $awa "graphicData/texPath" "Awa mature texture path") "Things/Plants/FullGrown/AMJC_Awa" "Awa mature texture path"
$awaTexturePath = Join-Path $RepositoryRoot "Textures\Things\Plants\FullGrown\AMJC_Awa\AMJC_Awa_Mature.png"
if (-not (Test-Path -LiteralPath $awaTexturePath)) { Fail "Awa mature texture was not found: $awaTexturePath" }
$pngBytes = [System.IO.File]::ReadAllBytes($awaTexturePath)
if ($pngBytes.Length -lt 24) { Fail "Awa mature texture is too small to be a valid PNG." }
$pngSignature = [byte[]](137,80,78,71,13,10,26,10)
for ($i = 0; $i -lt 8; $i++) { if ($pngBytes[$i] -ne $pngSignature[$i]) { Fail "Awa mature texture has an invalid PNG signature." } }
$width = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,16))
$height = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,20))
if ($width -ne 256 -or $height -ne 256) { Fail ("Awa mature texture must be 256x256, got {0}x{1}." -f $width,$height) }

Assert-Text (Node-Text $awa "plant/immatureGraphicPath" "Awa immature texture path") "Things/Plants/Immature/AMJC_Awa" "Awa immature texture path"
$awaImmatureTexturePath = Join-Path $RepositoryRoot "Textures\Things\Plants\Immature\AMJC_Awa\AMJC_Awa_Immature.png"
if (-not (Test-Path -LiteralPath $awaImmatureTexturePath)) { Fail "Awa immature texture was not found: $awaImmatureTexturePath" }
$pngBytes = [System.IO.File]::ReadAllBytes($awaImmatureTexturePath)
if ($pngBytes.Length -lt 24) { Fail "Awa immature texture is too small to be a valid PNG." }
for ($i = 0; $i -lt 8; $i++) { if ($pngBytes[$i] -ne $pngSignature[$i]) { Fail "Awa immature texture has an invalid PNG signature." } }
$width = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,16))
$height = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,20))
if ($width -ne 256 -or $height -ne 256) { Fail ("Awa immature texture must be 256x256, got {0}x{1}." -f $width,$height) }

$raw = Get-DefNode $items "ThingDef" "AMJC_RawMillet"
$inHull = Get-DefNode $items "ThingDef" "AMJC_MilletInHull"
$millet = Get-DefNode $items "ThingDef" "AMJC_Millet"

$milletGraphics = @(
    @{ Node = $raw; Name = "Raw millet"; TexPath = "Things/Item/Resource/AMJC_Millet/RawMillet"; RelativeDir = "Textures\Things\Item\Resource\AMJC_Millet\RawMillet"; Stem = "RawMillet" },
    @{ Node = $inHull; Name = "Millet in hull"; TexPath = "Things/Item/Resource/AMJC_Millet/MilletInHull"; RelativeDir = "Textures\Things\Item\Resource\AMJC_Millet\MilletInHull"; Stem = "MilletInHull" },
    @{ Node = $millet; Name = "Millet"; TexPath = "Things/Item/Resource/AMJC_Millet/Millet"; RelativeDir = "Textures\Things\Item\Resource\AMJC_Millet\Millet"; Stem = "Millet" }
)
foreach ($graphic in $milletGraphics) {
    Assert-Text (Node-Text $graphic.Node "graphicData/graphicClass" "$($graphic.Name) graphic class") "Graphic_StackCount" "$($graphic.Name) graphic class"
    Assert-Text (Node-Text $graphic.Node "graphicData/texPath" "$($graphic.Name) texture path") $graphic.TexPath "$($graphic.Name) texture path"
    foreach ($suffix in @("a","b","c")) {
        $texturePath = Join-Path $RepositoryRoot (Join-Path $graphic.RelativeDir "$($graphic.Stem)_$suffix.png")
        if (-not (Test-Path -LiteralPath $texturePath)) { Fail "$($graphic.Name) stack texture was not found: $texturePath" }
        $pngBytes = [System.IO.File]::ReadAllBytes($texturePath)
        if ($pngBytes.Length -lt 24) { Fail "$($graphic.Name) stack texture is too small to be a valid PNG: $texturePath" }
        for ($i = 0; $i -lt 8; $i++) { if ($pngBytes[$i] -ne $pngSignature[$i]) { Fail "$($graphic.Name) stack texture has an invalid PNG signature: $texturePath" } }
        $width = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,16))
        $height = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($pngBytes,20))
        if ($width -ne 256 -or $height -ne 256) { Fail ("{0} stack texture must be 256x256, got {1}x{2}: {3}" -f $graphic.Name,$width,$height,$texturePath) }
    }
}
Assert-Number (Node-Text $raw "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Raw millet rot days") 120 "Raw millet rot days"
Assert-Number (Node-Text $inHull "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Millet-in-hull rot days") 120 "Millet-in-hull rot days"
Assert-Number (Node-Text $millet "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Edible millet rot days") 90 "Edible millet rot days"

$rawBuckwheat = Get-DefNode $items "ThingDef" "AMJC_RawBuckwheat"
$buckwheatInHull = Get-DefNode $items "ThingDef" "AMJC_BuckwheatInHull"
$buckwheat = Get-DefNode $items "ThingDef" "AMJC_Buckwheat"
Assert-Number (Node-Text $rawBuckwheat "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Raw buckwheat rot days") 120 "Raw buckwheat rot days"
Assert-Number (Node-Text $buckwheatInHull "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Buckwheat-in-hull rot days") 120 "Buckwheat-in-hull rot days"
Assert-Number (Node-Text $buckwheat "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Edible buckwheat rot days") 60 "Edible buckwheat rot days"
Assert-Number (Node-Text $buckwheat "statBases/Nutrition" "Buckwheat nutrition") 0.05 "Buckwheat nutrition"

$rawBarley = Get-DefNode $items "ThingDef" "AMJC_RawBarley"
$barleyInHull = Get-DefNode $items "ThingDef" "AMJC_BarleyInHull"
$barleyGrain = Get-DefNode $items "ThingDef" "AMJC_Barley"
Assert-Number (Node-Text $rawBarley "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Raw barley rot days") 120 "Raw barley rot days"
Assert-Number (Node-Text $barleyInHull "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Barley-in-hull rot days") 120 "Barley-in-hull rot days"
Assert-Number (Node-Text $barleyGrain "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Edible barley rot days") 90 "Edible barley rot days"
Assert-Number (Node-Text $barleyGrain "statBases/Nutrition" "Barley nutrition") 0.05 "Barley nutrition"

$wheatGrain = Get-DefNode $items "ThingDef" "AMJC_Wheat"
Assert-Number (Node-Text $wheatGrain "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "Wheat grain rot days") 90 "Wheat grain rot days"
Assert-Number (Node-Text $wheatGrain "statBases/Nutrition" "Wheat grain nutrition") 0.05 "Wheat grain nutrition"
Assert-Text (Node-Text $wheatGrain "thingCategories/li" "Wheat grain cereal category") "DankPyon_Cereal" "Wheat grain cereal category"

foreach ($node in @($raw,$inHull,$millet,$rawBuckwheat,$buckwheatInHull,$buckwheat,$rawBarley,$barleyInHull,$barleyGrain)) {
    if ($null -ne $node.SelectSingleNode("thingCategories/li[text()='DankPyon_Cereal']")) {
        Fail "$($node.defName) must not be registered to DankPyon_Cereal."
    }
}

$fertilityPatch = $wheatPatch.SelectSingleNode('/Patch/Operation[@Class="PatchOperationConditional"][xpath=''/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/plant/fertilityMin'']')
if ($null -eq $fertilityPatch) { Fail "Wheat patch is missing fertilityMin conditional." }
Assert-Number (Node-Text $fertilityPatch "match/value/fertilityMin" "Wheat patch match fertilityMin") 0.7 "Wheat patch match fertilityMin"
Assert-Number (Node-Text $fertilityPatch "nomatch/value/fertilityMin" "Wheat patch nomatch fertilityMin") 0.7 "Wheat patch nomatch fertilityMin"

$thinSoilFertility = 0.50
foreach ($cropCase in @(
    @{ Name = "Soba"; Node = $soba; Expected = 0.875 },
    @{ Name = "Kibi"; Node = $kibi; Expected = 0.85 },
    @{ Name = "Awa"; Node = $awa; Expected = 0.80 },
    @{ Name = "Hie"; Node = $hie; Expected = 0.75 },
    @{ Name = "Barley"; Node = $barley; Expected = 0.70 }
)) {
    $fertilityMin = [double](Node-Text $cropCase.Node "plant/fertilityMin" "$($cropCase.Name) fertilityMin")
    if ($fertilityMin -gt $thinSoilFertility + 0.0001) {
        Fail "$($cropCase.Name) must remain sowable at fertility 0.50."
    }

    $sensitivity = [double](Node-Text $cropCase.Node "plant/fertilitySensitivity" "$($cropCase.Name) fertilitySensitivity")
    $factor = $thinSoilFertility * $sensitivity + (1.0 - $sensitivity)
    if ([math]::Abs($factor - [double]$cropCase.Expected) -gt 0.0001) {
        Fail "$($cropCase.Name) fertility 0.50 growth factor expected $($cropCase.Expected), got $factor."
    }
}

$wheatFertilityMin = [double](Node-Text $fertilityPatch "match/value/fertilityMin" "Wheat patched fertilityMin")
if ($wheatFertilityMin -le $thinSoilFertility + 0.0001) {
    Fail "MO wheat must remain unsowable at fertility 0.50."
}

$thingClassPatch = $wheatPatch.SelectSingleNode('/Patch/Operation[@Class="PatchOperationReplace"][xpath=''/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/thingClass'']')
if ($null -eq $thingClassPatch) { Fail "Wheat patch is missing thingClass replacement." }
Assert-Text (Node-Text $thingClassPatch "value/thingClass" "Wheat patch thingClass") "Plant" "Wheat patch thingClass"

$secondaryDropPatch = $wheatPatch.SelectSingleNode('/Patch/Operation[@Class="PatchOperationRemove"][xpath=''/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/modExtensions/li[@Class="MedievalOverhaul.SecondaryPlantDropExtension"]'']')
if ($null -eq $secondaryDropPatch) { Fail "Wheat patch must remove MO harvest-time secondary drop." }

$rawWheatCategoryPatch = $wheatPatch.SelectSingleNode('/Patch/Operation[@Class="PatchOperationReplace"][xpath=''/Defs/ThingDef[defName="DankPyon_RawWheat"]/thingCategories'']')
if ($null -eq $rawWheatCategoryPatch) { Fail "Wheat patch is missing RawWheat category replacement." }
Assert-Text (Node-Text $rawWheatCategoryPatch "value/thingCategories/li" "Raw wheat patched category") "Foods" "Raw wheat patched category"

$flourRotPatch = $wheatPatch.SelectSingleNode('/Patch/Operation[@Class="PatchOperationReplace"][xpath=''/Defs/ThingDef[defName="DankPyon_Flour"]/comps/li[@Class="CompProperties_Rottable"]/daysToRotStart'']')
if ($null -eq $flourRotPatch) { Fail "Wheat patch is missing flour rot replacement." }
Assert-Number (Node-Text $flourRotPatch "value/daysToRotStart" "Patched flour rot days") 60 "Patched flour rot days"

foreach ($recipeName in @("DankPyon_CraftFlour_Manual","DankPyon_CraftFlour","DankPyon_CraftFlourBulk")) {
    $expectedXpath = '/Defs/RecipeDef[defName="' + $recipeName + '"]/products/Hay'
    $removeCount = @($wheatPatch.SelectNodes('/Patch/Operation[@Class="PatchOperationRemove"]') | Where-Object {
        $xpathNode = $_.SelectSingleNode("xpath")
        $null -ne $xpathNode -and $xpathNode.InnerText.Trim() -eq $expectedXpath
    }).Count
    if ($removeCount -ne 1) { Fail "Wheat patch must remove Hay exactly once from $recipeName." }
}

$spot = Get-DefNode $buildings "ThingDef" "AMJC_GrainProcessingSpot"
$table = Get-DefNode $buildings "ThingDef" "AMJC_GrainProcessingTable"
Assert-Number (Node-Text $spot "costStuffCount" "Simple processing spot cost") 10 "Simple processing spot cost"
Assert-Number (Node-Text $spot "statBases/WorkTableWorkSpeedFactor" "Simple processing spot speed") 0.5 "Simple processing spot speed"
Assert-Number (Node-Text $table "costList/DankPyon_IronIngot" "Grain processing table iron cost") 30 "Grain processing table iron cost"
Assert-Number (Node-Text $table "statBases/WorkTableWorkSpeedFactor" "Grain processing table speed") 1 "Grain processing table speed"
Assert-Text (Node-Text $table "researchPrerequisites/li" "Grain processing table research") "DankPyon_BasicAgriculture" "Grain processing table research"

function Get-RecipeUsers($RecipeNode) {
    $users = @($RecipeNode.SelectNodes("recipeUsers/li") | ForEach-Object { $_.InnerText.Trim() })
    if ($users.Count -gt 0) {
        return $users
    }

    $parentName = $RecipeNode.GetAttribute("ParentName")
    if ([string]::IsNullOrWhiteSpace($parentName)) {
        Fail "$($RecipeNode.defName) has no direct recipeUsers and no ParentName."
    }

    $parent = $recipes.SelectSingleNode("/Defs/RecipeDef[@Name='$parentName']")
    if ($null -eq $parent) {
        Fail "$($RecipeNode.defName) refers to missing RecipeDef parent '$parentName'."
    }

    return @($parent.SelectNodes("recipeUsers/li") | ForEach-Object { $_.InnerText.Trim() })
}

function Assert-Recipe([string]$DefName,[double]$WorkAmount,[string]$InputDef,[double]$InputCount,[hashtable]$Products) {
    $recipe = Get-DefNode $recipes "RecipeDef" $DefName
    Assert-Number (Node-Text $recipe "workAmount" "$DefName workAmount") $WorkAmount "$DefName workAmount"
    $users = @(Get-RecipeUsers $recipe)
    foreach ($requiredUser in @("AMJC_GrainProcessingSpot","AMJC_GrainProcessingTable")) {
        if ($users -notcontains $requiredUser) { Fail "$DefName is missing recipe user $requiredUser." }
    }
    Assert-Text (Node-Text $recipe "ingredients/li/filter/thingDefs/li" "$DefName input") $InputDef "$DefName input"
    Assert-Number (Node-Text $recipe "ingredients/li/count" "$DefName input count") $InputCount "$DefName input count"
    foreach ($productDef in $Products.Keys) {
        Assert-Number (Node-Text $recipe "products/$productDef" "$DefName product $productDef") ([double]$Products[$productDef]) "$DefName product $productDef"
    }
}

Assert-Recipe "AMJC_ThreshMillet" 15 "AMJC_RawMillet" 1 @{ AMJC_MilletInHull = 1; DankPyon_Straw = 1 }
Assert-Recipe "AMJC_ThreshMilletBulk" 120 "AMJC_RawMillet" 10 @{ AMJC_MilletInHull = 10; DankPyon_Straw = 10 }
Assert-Recipe "AMJC_HullMillet" 10 "AMJC_MilletInHull" 1 @{ AMJC_Millet = 1 }
Assert-Recipe "AMJC_HullMilletBulk" 80 "AMJC_MilletInHull" 10 @{ AMJC_Millet = 10 }
Assert-Recipe "AMJC_ThreshBuckwheat" 15 "AMJC_RawBuckwheat" 1 @{ AMJC_BuckwheatInHull = 1; DankPyon_Straw = 1 }
Assert-Recipe "AMJC_ThreshBuckwheatBulk" 120 "AMJC_RawBuckwheat" 10 @{ AMJC_BuckwheatInHull = 10; DankPyon_Straw = 10 }
Assert-Recipe "AMJC_HullBuckwheat" 10 "AMJC_BuckwheatInHull" 1 @{ AMJC_Buckwheat = 1 }
Assert-Recipe "AMJC_HullBuckwheatBulk" 80 "AMJC_BuckwheatInHull" 10 @{ AMJC_Buckwheat = 10 }
Assert-Recipe "AMJC_ThreshBarley" 15 "AMJC_RawBarley" 1 @{ AMJC_BarleyInHull = 1; DankPyon_Straw = 1 }
Assert-Recipe "AMJC_ThreshBarleyBulk" 120 "AMJC_RawBarley" 10 @{ AMJC_BarleyInHull = 10; DankPyon_Straw = 10 }
Assert-Recipe "AMJC_HullBarley" 10 "AMJC_BarleyInHull" 1 @{ AMJC_Barley = 1 }
Assert-Recipe "AMJC_HullBarleyBulk" 80 "AMJC_BarleyInHull" 10 @{ AMJC_Barley = 10 }
Assert-Recipe "AMJC_ThreshWheat" 15 "DankPyon_RawWheat" 1 @{ AMJC_Wheat = 1; DankPyon_Straw = 1 }
Assert-Recipe "AMJC_ThreshWheatBulk" 120 "DankPyon_RawWheat" 10 @{ AMJC_Wheat = 10; DankPyon_Straw = 10 }

$moActiveRoot = $MedievalOverhaulRoot
$mo16Candidate = Join-Path $MedievalOverhaulRoot "1.6"
if (Test-Path -LiteralPath $mo16Candidate) { $moActiveRoot = $mo16Candidate }
$moActiveXmlFiles = @(Get-ChildItem -LiteralPath $moActiveRoot -Recurse -File -Filter *.xml)

function Get-MoDef([string]$TypeName,[string]$DefName) {
    $pattern = "<defName>$DefName</defName>"
    $matches = New-Object System.Collections.Generic.List[System.Xml.XmlNode]

    foreach ($file in $moActiveXmlFiles) {
        if (-not (Select-String -LiteralPath $file.FullName -Pattern $pattern -SimpleMatch -Quiet)) {
            continue
        }

        $xml = Load-Xml $file.FullName
        $node = $xml.SelectSingleNode("/Defs/$TypeName[defName='$DefName']")
        if ($null -ne $node) {
            $matches.Add($node)
        }
    }

    if ($matches.Count -ne 1) {
        Fail "Expected exactly one active MO $TypeName '$DefName', found $($matches.Count)."
    }

    return $matches[0]
}

$moWheatPlant = Get-MoDef "ThingDef" "DankPyon_Plant_Wheat"
Assert-Number (Node-Text $moWheatPlant "plant/growDays" "MO wheat growDays") 12 "MO wheat growDays"
Assert-Number (Node-Text $moWheatPlant "plant/harvestYield" "MO wheat harvestYield") 28 "MO wheat harvestYield"
Assert-Number (Node-Text $moWheatPlant "plant/fertilitySensitivity" "MO wheat fertilitySensitivity") 0.9 "MO wheat fertilitySensitivity"
Assert-Text (Node-Text $moWheatPlant "plant/harvestedThingDef" "MO wheat harvestedThingDef") "DankPyon_RawWheat" "MO wheat harvestedThingDef"
Assert-Text (Node-Text $moWheatPlant "plant/sowResearchPrerequisites/li" "MO wheat research prerequisite") "DankPyon_BasicAgriculture" "MO wheat research prerequisite"
Assert-Text (Node-Text $moWheatPlant "thingClass" "MO wheat thingClass") "MedievalOverhaul.Plant_SecondaryDrop" "MO wheat thingClass"
$moSecondaryDrop = $moWheatPlant.SelectSingleNode("modExtensions/li[@Class='MedievalOverhaul.SecondaryPlantDropExtension']")
if ($null -eq $moSecondaryDrop) { Fail "Installed MO wheat no longer has the expected SecondaryPlantDropExtension; re-audit AMJ wheat patch." }
Assert-Text (Node-Text $moSecondaryDrop "secondaryDrop" "MO wheat secondary drop") "Hay" "MO wheat secondary drop"
Assert-Number (Node-Text $moSecondaryDrop "secondaryDropAmountRange" "MO wheat secondary drop amount") 40 "MO wheat secondary drop amount"

$moRawWheat = Get-MoDef "ThingDef" "DankPyon_RawWheat"
Assert-Number (Node-Text $moRawWheat "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "MO raw wheat rot days") 120 "MO raw wheat rot days"
Assert-Text (Node-Text $moRawWheat "thingCategories/li" "MO raw wheat cereal category") "DankPyon_Cereal" "MO raw wheat cereal category"

$moFlour = Get-MoDef "ThingDef" "DankPyon_Flour"
Assert-Number (Node-Text $moFlour "comps/li[@Class='CompProperties_Rottable']/daysToRotStart" "MO flour source rot days") 90 "MO flour source rot days"

foreach ($case in @(
    @{ DefName = "DankPyon_CraftFlour_Manual"; Flour = 1; Hay = 1 },
    @{ DefName = "DankPyon_CraftFlour"; Flour = 1; Hay = 1 },
    @{ DefName = "DankPyon_CraftFlourBulk"; Flour = 10; Hay = 10 }
)) {
    $moRecipe = Get-MoDef "RecipeDef" $case.DefName
    Assert-Number (Node-Text $moRecipe "products/DankPyon_Flour" "$($case.DefName) source flour product") ([double]$case.Flour) "$($case.DefName) source flour product"
    Assert-Number (Node-Text $moRecipe "products/Hay" "$($case.DefName) source Hay product") ([double]$case.Hay) "$($case.DefName) source Hay product"
    Assert-Text (Node-Text $moRecipe "ingredients/li/filter/categories/li" "$($case.DefName) source cereal input") "DankPyon_Cereal" "$($case.DefName) source cereal input"
}

$moXmlFiles = @(Get-ChildItem -LiteralPath $MedievalOverhaulRoot -Recurse -File -Filter *.xml)
foreach ($defName in @("DankPyon_Straw","DankPyon_IronIngot","DankPyon_BasicAgriculture","DankPyon_RawWood")) {
    $pattern = "<defName>$defName</defName>"
    if (-not (Select-String -Path $moXmlFiles.FullName -Pattern $pattern -SimpleMatch -Quiet)) { Fail "Installed Medieval Overhaul does not contain required Def '$defName'." }
}

$moBarleyDef = Select-String -Path $moXmlFiles.FullName -Pattern '<defName>[^<]*Barley[^<]*</defName>' -CaseSensitive:$false
if ($null -ne $moBarleyDef) {
    Fail "Installed Medieval Overhaul now contains a Barley-named Def. Re-audit AMJC Barley ownership before keeping the duplicate crop."
}

& (Join-Path $RepositoryRoot "Scripts/Validate-NewVillage.ps1") -RepositoryRoot $RepositoryRoot -MedievalOverhaulRoot $MedievalOverhaulRoot -RimWorldRoot $RimWorldRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[OK] AMJ Stage A static validation passed." -ForegroundColor Green
exit 0
