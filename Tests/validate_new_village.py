"""Static New Village contract; optional audit against actual game/MO Def XML."""
import argparse
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = {"DankPyon_Lumber", "DankPyon_RusticFurniture", "DankPyon_BasicCooking"}
SUPPLIES = {
    "DankPyon_MealRations": (60, None), "AMJC_Millet": (200, None),
    "AMJC_RawMillet": (100, None), "MedicineHerbal": (20, None),
    "WoodLog": (200, None), "DankPyon_RawWood": (200, None),
    "DankPyon_IronIngot": (30, None), "Cloth": (80, None),
    "Silver": (150, None), "Bow_Short": (2, None),
    "MeleeWeapon_Knife": (2, "DankPyon_IronIngot"), "MeleeWeapon_Club": (1, "WoodLog"),
}

def load(path):
    return ET.parse(path).getroot()

def unique(root, tag, name):
    found = [n for n in root.findall(tag) if n.findtext("defName") == name]
    assert len(found) == 1, f"Expected one {tag} {name}, got {len(found)}"
    return found[0]

def definitions(folder):
    result = {}
    for p in folder.rglob("*.xml"):
        root = load(p)
        if root.tag != "Defs":
            continue
        for n in root:
            name = n.findtext("defName")
            if name:
                result.setdefault((n.tag, name), []).append(n)
    return result

def validate(mo_root=None, core_defs=None):
    scen = unique(load(ROOT / "Defs/Scenarios/Scenarios_NewVillage.xml"), "ScenarioDef", "AMJC_NewVillage")
    faction = unique(load(ROOT / "Defs/FactionDefs/Factions_PlayerVillage.xml"), "FactionDef", "AMJC_PlayerVillage")
    pawn = unique(load(ROOT / "Defs/PawnKindDefs/PawnKinds_Villager.xml"), "PawnKindDef", "AMJC_Villager")
    assert scen.get("ParentName") == "ScenarioBase"
    assert faction.get("ParentName") == "PlayerFactionBase"
    assert pawn.get("ParentName") == "BasePlayerPawnKind"
    assert scen.findtext("scenario/playerFaction/def") == "PlayerFaction"
    assert scen.findtext("scenario/playerFaction/factionDef") == "AMJC_PlayerVillage"
    assert faction.findtext("isPlayer") == "true"
    assert faction.findtext("techLevel") == "Medieval"
    assert faction.findtext("basicMemberKind") == "AMJC_Villager"
    assert pawn.findtext("race") == "Human"
    assert pawn.findtext("defaultFactionDef") == "AMJC_PlayerVillage"
    assert float(pawn.findtext("techHediffsChance")) == 0
    assert {n.text for n in pawn.findall("apparelTags/li")} == {"Neolithic", "DankPyon_Peasant"}
    assert [n.text for n in faction.findall("backstoryFilters/li/categories/li")] == ["Tribal"]
    assert [n.text for n in pawn.findall("backstoryCategories/li")] == ["Tribal"]
    assert [n.text for n in faction.findall("apparelStuffFilter/thingDefs/li")] == ["Cloth"]
    for field in ("startingResearchTags", "startingTechprintsResearchTags"):
        node = faction.find(field)
        assert node is not None and len(node) == 0, f"{field} must explicitly be empty"

    parts = scen.findall("scenario/parts/li")
    allowed = {
        "ScenPart_ConfigPage_ConfigureStartingPawns": "ConfigPage_ConfigureStartingPawns",
        "ScenPart_PlayerPawnsArriveMethod": "PlayerPawnsArriveMethod",
        "ScenPart_StartingResearch": "StartingResearch",
        "ScenPart_StartingThing_Defined": "StartingThing_Defined",
        "ScenPart_GameStartDialog": "GameStartDialog",
    }
    assert len(parts) == 18, "Unexpected number of explicit Scenario parts"
    for p in parts:
        assert p.get("Class") in allowed, f"Unexpected Scenario part: {p.get('Class')}"
        assert p.findtext("def") == allowed[p.get("Class")]
    def by_class(name):
        return [p for p in parts if p.get("Class") == name]
    configure, = by_class("ScenPart_ConfigPage_ConfigureStartingPawns")
    assert configure.findtext("pawnCount") == "5"
    assert configure.findtext("pawnChoiceCount") == "8"
    arrival, = by_class("ScenPart_PlayerPawnsArriveMethod")
    assert arrival.findtext("method") == "Standing"
    projects = [p.findtext("project") for p in by_class("ScenPart_StartingResearch")]
    assert len(projects) == 3 and set(projects) == RESEARCH
    items = by_class("ScenPart_StartingThing_Defined")
    assert len(items) == len(SUPPLIES)
    actual = {p.findtext("thingDef"): (int(p.findtext("count")), p.findtext("stuff")) for p in items}
    assert actual == SUPPLIES, f"Starting supplies differ: {actual}"
    dialog, = by_class("ScenPart_GameStartDialog")
    assert dialog.findtext("textKey") == "AMJC_GameStart_NewVillage"
    assert dialog.findtext("closeSound") == "GameStartSting"
    for lang in ("English", "Japanese"):
        assert load(ROOT / f"Languages/{lang}/Keyed/AMJC_Scenarios.xml").findtext("AMJC_GameStart_NewVillage")
    jp = load(ROOT / "Languages/Japanese/DefInjected/ScenarioDef/AMJC_NewVillage.xml")
    assert jp.findtext("AMJC_NewVillage.label") == "新しい村"
    assert jp.findtext("AMJC_NewVillage.description")
    assert jp.findtext("AMJC_NewVillage.scenario.summary")
    for typ, name, fields in (
        ("FactionDef", "AMJC_PlayerVillage", ("label", "description", "pawnSingular", "pawnsPlural")),
        ("PawnKindDef", "AMJC_Villager", ("label",)),
    ):
        jp = load(ROOT / f"Languages/Japanese/DefInjected/{typ}/{name}.xml")
        for field in fields:
            assert jp.findtext(f"{name}.{field}"), f"Missing Japanese {name}.{field}"

    design = (ROOT / "Docs/Design.md").read_text()
    section = design.split("### Core標準Scenario", 1)[1].split("\n### ", 1)[0]
    for name, (count, _) in SUPPLIES.items():
        assert re.search(r"\| `" + re.escape(name) + r"`[^|]*\| " + str(count) + r" \|", section), f"Design supplies differ: {name}"
    for name in RESEARCH:
        assert f"`{name}`" in section
    assert "候補8人から5人" in section
    assert "研究タグ / Techprintタグ | 空" in section

    feature = (ROOT / "Tests/E2E/TestMod/Pickle/Features/stage-a.feature").read_text()
    names = re.findall(r"^  Scenario: (.+)$", feature, re.M)
    assert len(names) == 7 and len(set(names)) == 7
    assert "@quickstart:AmjNewVillageQuickstart\n  Scenario: New Village starts" in feature
    summary = (ROOT / "Scripts/Validate-PickleSummary.ps1").read_text()
    assert all(f'"{name}"' in summary for name in names)
    assert "$summary.total -ne 7" in summary and "$summary.passed -ne 7" in summary
    quickstart = (ROOT / "Tests/E2E/AmjStageAQuickstart.cs").read_text()
    assert "sealed class AmjNewVillageQuickstart" in quickstart
    assert 'DefDatabase<ScenarioDef>.GetNamed("AMJC_NewVillage")' in quickstart
    batch = (ROOT / "build-e2e.bat").read_text()
    assert batch.count('"%ROOT%Tests\\E2E\\NewVillageSteps.cs"') == 2
    assert 'MOFixture\\Defs" "%MO_FIXTURE_DIR%\\Defs" /E /I /Y' in batch
    runtime = (ROOT / "run-e2e.bat").read_text()
    assert "-FailOnAnyError" in runtime

    fixture = definitions(ROOT / "Tests/E2E/MOFixture/Defs")
    for typ, name in [("ThingDef", n) for n in SUPPLIES if n.startswith("DankPyon_")] + [("ResearchProjectDef", n) for n in RESEARCH]:
        assert len(fixture.get((typ, name), [])) == 1, f"Missing/duplicate typed fixture: {typ} {name}"
    iron = fixture[("ThingDef", "DankPyon_IronIngot")][0]
    assert iron.findtext("stuffProps/categories/li") == "Metallic"

    if mo_root:
        mo_root = Path(mo_root)
        active = mo_root / "1.6" if (mo_root / "1.6").is_dir() else mo_root
        mo = definitions(active / "Defs")
        for typ, name in [("ThingDef", n) for n in SUPPLIES if n.startswith("DankPyon_")] + [("ResearchProjectDef", n) for n in RESEARCH]:
            assert len(mo.get((typ, name), [])) == 1, f"MO 1.6 reference not unique: {typ} {name}"
        assert mo[("ThingDef", "DankPyon_IronIngot")][0].findtext("stuffProps/categories/li") == "Metallic"
        assert mo[("ResearchProjectDef", "DankPyon_RusticFurniture")][0].findtext("prerequisites/li") == "DankPyon_Lumber"
        print("New Village supplied MO 1.6 reference audit: PASS")
    if core_defs:
        native = definitions(Path(core_defs))
        for name in SUPPLIES:
            if not name.startswith(("DankPyon_", "AMJC_")):
                assert len(native.get(("ThingDef", name), [])) == 1, f"Core reference not unique: {name}"
        for path, tag, parent in (
            ("Scenarios/Scenarios_Classic.xml", "ScenarioDef", "ScenarioBase"),
            ("FactionDefs/Factions_Player.xml", "FactionDef", "PlayerFactionBase"),
            ("PawnKindDefs_Humanlikes/PawnKinds_Player.xml", "PawnKindDef", "BasePlayerPawnKind"),
        ):
            assert any(n.get("Name") == parent for n in load(Path(core_defs) / path).findall(tag))
        for part in parts:
            native_part, = native.get(("ScenPartDef", part.findtext("def")), [])
            assert native_part.findtext("scenPartClass") == part.get("Class"), "Native Scenario part class differs"
        assert len(native.get(("ScenPartDef", "PlayerFaction"), [])) == 1
        assert len(native.get(("CultureDef", "Corunan"), [])) == 1
        print("New Village supplied Core Def reference audit: PASS")
    print("AMJ New Village static validation: PASS")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mo-root", type=Path)
    parser.add_argument("--core-defs", type=Path)
    args = parser.parse_args()
    validate(args.mo_root, args.core_defs)
