param(
    [Parameter(Mandatory = $true)][string]$RepositoryRoot,
    [Parameter(Mandatory = $true)][string]$MedievalOverhaulRoot,
    [string]$RimWorldRoot = ""
)
$ErrorActionPreference = "Stop"

function Fail([string]$Message) { Write-Host "[FAIL] New Village: $Message" -ForegroundColor Red; exit 1 }
function Load-Xml([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { Fail "Required file missing: $Path" }
    try { return [xml](Get-Content -LiteralPath $Path -Raw -Encoding UTF8) }
    catch { Fail "Invalid XML: $Path ($($_.Exception.Message))" }
}
function Check([bool]$Condition, [string]$Message) { if (-not $Condition) { Fail $Message } }
function Def-Node($Xml, [string]$Type, [string]$Name) {
    $nodes = @($Xml.SelectNodes("/Defs/$Type[defName='$Name']"))
    Check ($nodes.Count -eq 1) "Expected one $Type '$Name', found $($nodes.Count)."
    return $nodes[0]
}
function Source-Index([string]$Folder) {
    Check (Test-Path -LiteralPath $Folder) "Source Defs directory missing: $Folder"
    $index = @{}
    foreach ($file in @(Get-ChildItem -LiteralPath $Folder -Recurse -File -Filter *.xml)) {
        $xml = Load-Xml $file.FullName
        foreach ($node in @($xml.SelectNodes("/Defs/*[defName]"))) {
            $key = $node.Name + ":" + $node.SelectSingleNode("defName").InnerText
            if (-not $index.ContainsKey($key)) { $index[$key] = @() }
            $index[$key] += @($node)
        }
    }
    return $index
}
function Require-Source($Index, [string]$Type, [string]$Name) {
    $key = $Type + ":" + $Name
    Check ($Index.ContainsKey($key) -and @($Index[$key]).Count -eq 1) "Source must contain exactly one $Type '$Name'."
    return $Index[$key][0]
}

. (Join-Path $PSScriptRoot "AmjProfileXml.ps1")
$scenarioXml = Get-AmjProfileXml $RepositoryRoot
$scen = Def-Node $scenarioXml "ScenarioDef" "AMJC_NewVillage"
$faction = Def-Node $scenarioXml "FactionDef" "AMJC_PlayerVillage"
$pawn = Def-Node $scenarioXml "PawnKindDef" "AMJC_Villager"
Check ($scen.ParentName -eq "ScenarioBase") "ScenarioBase inheritance differs."
Check ($faction.ParentName -eq "PlayerFactionBase") "PlayerFactionBase inheritance differs."
Check ($pawn.ParentName -eq "BasePlayerPawnKind") "BasePlayerPawnKind inheritance differs."
Check ($scen.scenario.playerFaction.factionDef -eq "AMJC_PlayerVillage") "Player faction differs."
Check ($faction.isPlayer -eq "true" -and $faction.techLevel -eq "Medieval") "Village faction type differs."
Check ($faction.basicMemberKind -eq "AMJC_Villager" -and $pawn.race -eq "Human") "Villager kind/race differs."
Check ($pawn.defaultFactionDef -eq "AMJC_PlayerVillage") "Villager default faction differs."
Check ([double]$pawn.techHediffsChance -eq 0) "Villager implant-generation chance differs."
foreach ($field in @("startingResearchTags", "startingTechprintsResearchTags")) {
    $node = $faction.SelectSingleNode($field)
    Check ($null -ne $node -and $node.ChildNodes.Count -eq 0) "$field must explicitly be empty."
}

$classes = @{
    ScenPart_ConfigPage_ConfigureStartingPawns = "ConfigPage_ConfigureStartingPawns"
    ScenPart_PlayerPawnsArriveMethod = "PlayerPawnsArriveMethod"
    ScenPart_StartingResearch = "StartingResearch"
    ScenPart_StartingThing_Defined = "StartingThing_Defined"
    ScenPart_GameStartDialog = "GameStartDialog"
}
$parts = @($scen.SelectNodes("scenario/parts/li"))
Check ($parts.Count -eq 18) "Unexpected explicit Scenario part count."
foreach ($part in $parts) {
    Check ($classes.ContainsKey([string]$part.Class)) "Unexpected Scenario part: $($part.Class)"
    Check ($part.def -eq $classes[[string]$part.Class]) "Scenario part def/class mismatch."
}
$configure = @($parts | Where-Object { $_.Class -eq "ScenPart_ConfigPage_ConfigureStartingPawns" })
Check ($configure.Count -eq 1 -and $configure[0].pawnCount -eq "5" -and $configure[0].pawnChoiceCount -eq "8") "Start must choose five out of eight."
$arrival = @($parts | Where-Object { $_.Class -eq "ScenPart_PlayerPawnsArriveMethod" })
Check ($arrival.Count -eq 1 -and $arrival[0].method -eq "Standing") "Start must arrive Standing."
$research = @("DankPyon_Lumber", "DankPyon_RusticFurniture", "DankPyon_BasicCooking")
$projects = @($parts | Where-Object { $_.Class -eq "ScenPart_StartingResearch" } | ForEach-Object { [string]$_.project })
Check ($projects.Count -eq 3 -and @($projects | Sort-Object -Unique).Count -eq 3) "Expected three unique starting research projects."
foreach ($name in $research) { Check ($projects -contains $name) "Starting research is missing $name." }
$supplies = @{
    DankPyon_MealRations = 60; AMJC_Millet = 200; AMJC_RawMillet = 100
    MedicineHerbal = 20; WoodLog = 200; DankPyon_RawWood = 200
    DankPyon_IronIngot = 30; Cloth = 80; Silver = 150
    Bow_Short = 2; MeleeWeapon_Knife = 2; MeleeWeapon_Club = 1
}
$items = @($parts | Where-Object { $_.Class -eq "ScenPart_StartingThing_Defined" })
Check ($items.Count -eq $supplies.Count) "Starting supply count differs."
$design = Get-Content -LiteralPath (Join-Path $RepositoryRoot "Docs/Design.md") -Raw -Encoding UTF8
$designSection = ($design -split '### Core標準Scenario', 2)[1] -split "\r?\n### ", 2 | Select-Object -First 1
Check ($designSection.Contains("候補8人から5人")) "Design pawn counts differ."
foreach ($name in $supplies.Keys) {
    $item = @($items | Where-Object { $_.thingDef -eq $name })
    Check ($item.Count -eq 1 -and [int]$item[0].count -eq $supplies[$name]) "Starting quantity differs for $name."
    $expectedStuff = ""
    if ($name -eq "MeleeWeapon_Knife") { $expectedStuff = "DankPyon_IronIngot" }
    if ($name -eq "MeleeWeapon_Club") { $expectedStuff = "WoodLog" }
    Check ([string]$item[0].stuff -eq $expectedStuff) "Starting material differs for $name."
    $rowPattern = '\| [' + [char]96 + ']' + [regex]::Escape($name) + '[' + [char]96 + '][^|]*\| ' + $supplies[$name] + ' \|'
    Check ([regex]::IsMatch($designSection, $rowPattern)) "Design supply row differs for $name."
}
$jp = Load-Xml (Join-Path $RepositoryRoot "Languages/Japanese/DefInjected/ScenarioDef/AMJC_NewVillage.xml")
Check ($jp.LanguageData.'AMJC_NewVillage.label' -eq "新しい村") "Japanese scenario label differs."
Check (-not [string]::IsNullOrWhiteSpace($jp.LanguageData.'AMJC_NewVillage.scenario.summary')) "Japanese summary missing."
foreach ($language in @("Japanese", "English")) {
    $keyed = Load-Xml (Join-Path $RepositoryRoot "Languages/$language/Keyed/AMJC_Scenarios.xml")
    Check (-not [string]::IsNullOrWhiteSpace($keyed.LanguageData.AMJC_GameStart_NewVillage)) "$language start text is missing."
}

$active = $MedievalOverhaulRoot
if (Test-Path -LiteralPath (Join-Path $active "1.6")) { $active = Join-Path $active "1.6" }
$mo = Source-Index (Join-Path $active "Defs")
foreach ($name in $research) { $null = Require-Source $mo "ResearchProjectDef" $name }
foreach ($name in @($supplies.Keys | Where-Object { $_.StartsWith("DankPyon_") })) { $null = Require-Source $mo "ThingDef" $name }
$iron = Require-Source $mo "ThingDef" "DankPyon_IronIngot"
Check (@($iron.SelectNodes("stuffProps/categories/li") | ForEach-Object { $_.InnerText }) -contains "Metallic") "MO iron cannot be used as metallic weapon stuff."
$rustic = Require-Source $mo "ResearchProjectDef" "DankPyon_RusticFurniture"
Check ($rustic.prerequisites.li -eq "DankPyon_Lumber") "Re-audit MO rustic-furniture prerequisites."

if (-not [string]::IsNullOrWhiteSpace($RimWorldRoot)) {
    $corePath = Join-Path $RimWorldRoot "Data/Core/Defs"
    $core = Source-Index $corePath
    foreach ($name in @($supplies.Keys | Where-Object { -not $_.StartsWith("DankPyon_") -and -not $_.StartsWith("AMJC_") })) {
        $null = Require-Source $core "ThingDef" $name
    }
    foreach ($case in @(
        @{ File = "Scenarios/Scenarios_Classic.xml"; Type = "ScenarioDef"; Parent = "ScenarioBase" },
        @{ File = "FactionDefs/Factions_Player.xml"; Type = "FactionDef"; Parent = "PlayerFactionBase" },
        @{ File = "PawnKindDefs_Humanlikes/PawnKinds_Player.xml"; Type = "PawnKindDef"; Parent = "BasePlayerPawnKind" }
    )) {
        $xml = Load-Xml (Join-Path $corePath $case.File)
        Check (@($xml.SelectNodes("/Defs/$($case.Type)[@Name='$($case.Parent)']")).Count -eq 1) "Core parent definition missing: $($case.Parent)."
    }
    foreach ($part in $parts) {
        $native = Require-Source $core "ScenPartDef" ([string]$part.def)
        Check ([string]$native.scenPartClass -eq [string]$part.Class) "Installed Core Scenario part class differs: $($part.def)."
    }
    $null = Require-Source $core "ScenPartDef" "PlayerFaction"
    $null = Require-Source $core "CultureDef" "Corunan"
    foreach ($weaponName in @("MeleeWeapon_Knife", "MeleeWeapon_Club")) {
        $weapon = Require-Source $core "ThingDef" $weaponName
        $category = "Metallic"
        if ($weaponName -eq "MeleeWeapon_Club") { $category = "Woody" }
        Check (@($weapon.SelectNodes("stuffCategories/li") | ForEach-Object { $_.InnerText }) -contains $category) "Installed Core weapon stuff differs: $weaponName."
    }
}
else {
    Write-Host "[WARN] New Village installed Core reference audit skipped: no RimWorldRoot supplied."
}

Write-Host "[OK] New Village static design/XML and supplied source references match." -ForegroundColor Green
exit 0

