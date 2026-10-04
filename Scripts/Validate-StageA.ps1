param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,
    [Parameter(Mandatory = $true)]
    [string]$MedievalOverhaulRoot
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
$about = Load-Xml (Join-Path $RepositoryRoot "About\About.xml")
$plants = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Plants\Plants_StageA.xml")
$items = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Items\Items_StageA_Grains.xml")
$buildings = Load-Xml (Join-Path $RepositoryRoot "Defs\ThingDefs_Buildings\Buildings_GrainProcessing.xml")
$recipes = Load-Xml (Join-Path $RepositoryRoot "Defs\RecipeDefs\Recipes_GrainProcessing.xml")
$cctoPatch = Load-Xml (Join-Path $RepositoryRoot "Patches\Compatibility\CCTO_StageA.xml")

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

foreach ($case in @(
    @{ DefName = "AMJC_Plant_FoxtailMillet_Awa"; Death = -3 },
    @{ DefName = "AMJC_Plant_BarnyardMillet_Hie"; Death = -2 },
    @{ DefName = "AMJC_Plant_ProsoMillet_Kibi"; Death = -3 },
    @{ DefName = "AMJC_Plant_Buckwheat_Soba"; Death = -2 }
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

if ($items.OuterXml -match "<li>DankPyon_Cereal</li>") { Fail "AMJ millet stages must not be registered to DankPyon_Cereal." }

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

$moXmlFiles = @(Get-ChildItem -LiteralPath $MedievalOverhaulRoot -Recurse -File -Filter *.xml)
foreach ($defName in @("DankPyon_Straw","DankPyon_IronIngot","DankPyon_BasicAgriculture","DankPyon_RawWood")) {
    $pattern = "<defName>$defName</defName>"
    if (-not (Select-String -Path $moXmlFiles.FullName -Pattern $pattern -SimpleMatch -Quiet)) { Fail "Installed Medieval Overhaul does not contain required Def '$defName'." }
}

Write-Host "[OK] AMJ Stage A static validation passed." -ForegroundColor Green
exit 0
