"""Stage-2 boundary and pre-split MO contracts; no runtime/art/wheat-chain claim."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from copy import deepcopy
from amj_profile_xml import ROOT, MO_FOLDER, profile_xml, contract_signature

MO_GRAPHIC_PATHS = {
    "Things/Plants/FullGrown/WheatPlant",
    "Things/Plants/Immature/WheatPlant",
    "Things/Building/Production/StonecuttingSpot",
    "Things/Building/Production/Millstone",
}

# Author-approved visual changes only. Historical hashes remain immutable;
# normalize these exact four fields for the otherwise unchanged MO contract.
AMJ_GRAPHICS = {
    "AMJC_Plant_Barley": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Awa", "Things/Plants/FullGrown/WheatPlant"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Awa", "Things/Plants/Immature/WheatPlant"),
    },
    "AMJC_GrainProcessingSpot": {
        "graphicData/texPath": ("Things/Building/Production/TableStonecutter", "Things/Building/Production/StonecuttingSpot"),
    },
    "AMJC_GrainProcessingTable": {
        "graphicData/texPath": ("Things/Building/Production/TableStonecutter", "Things/Building/Production/Millstone"),
    },
}


def validate():
    # MO identifiers/classes must be absent from Base Defs and localization.
    for folder in ("Defs", "Languages", "BaseWithoutMO", "LegacyStartingScenarios/Defs", "LegacyStartingScenarios/Languages"):
        for path in sorted((ROOT / folder).rglob("*.xml")):
            document = ET.parse(path).getroot()
            for node in document.iter():
                text = " ".join([str(node.tag), (node.text or "").strip(), *node.attrib.values()])
                assert not re.search(r"DankPyon_|MedievalOverhaul\.", text), f"Base MO reference: {path} {node.tag}"
    assert not (ROOT / "Patches/MedievalOverhaul_StageA_Wheat.xml").exists()
    assert not (ROOT / "Languages/Japanese/DefInjected/ThingDef/AMJC_MO_Overrides.xml").exists()
    for path in (ROOT / "Patches").rglob("*.xml"):
        assert "DankPyon_" not in path.read_text(encoding="utf-8"), f"MO patch escaped conditional load folder: {path}"
    conditional_label = ROOT / MO_FOLDER / "Languages/Japanese/DefInjected/ThingDef/AMJC_MO_Overrides.xml"
    assert ET.parse(conditional_label).findtext("DankPyon_RawWheat.label") == "小麦束"

    base = profile_xml("vanilla")
    mo = profile_xml("mo")
    for name, paths in AMJ_GRAPHICS.items():
        for document in (base, mo):
            target = document.find('ThingDef[defName="' + name + '"]')
            assert target is not None, name
            for element, (expected, historical) in paths.items():
                assert target.findtext(element) == expected, "AMJ graphics priority lost: " + name + "/" + element
    for node in base.iter():
        if node.tag in {"texPath", "immatureGraphicPath"}:
            assert (node.text or "").strip() not in MO_GRAPHIC_PATHS, "Base MO texture reference: " + str(node.text)
    base_recipes = {n.findtext("defName") for n in base.findall("RecipeDef")}
    for path in list((ROOT / "Languages").glob("*/DefInjected/RecipeDef/*.xml")) + list((ROOT / "BaseWithoutMO/Languages").glob("*/DefInjected/RecipeDef/*.xml")):
        for translation in ET.parse(path).getroot():
            assert translation.tag.split(".")[0] in base_recipes, f"Base orphan RecipeDef translation: {translation.tag}"
    names = [n.findtext("defName") or n.get("Name") for n in mo]
    assert len(names) == len(set(names)), "Duplicate explicit AMJ Def/Parent name"
    golden = json.loads((ROOT / "Tests/Fixtures/MO_PreSplit_Contracts.json").read_text())
    for source, expected in golden["movedFileSha256"].items():
        assert hashlib.sha256((ROOT / MO_FOLDER / source).read_bytes()).hexdigest() == expected, source
    translations = {}
    for path in (ROOT / "Languages/Japanese/DefInjected/RecipeDef/AMJC_StageA.xml",
                 ROOT / MO_FOLDER / "Languages/Japanese/DefInjected/RecipeDef/AMJC_MOWheat.xml"):
        for node in ET.parse(path).getroot():
            assert node.tag not in translations, f"Duplicate RecipeDef translation: {node.tag}"
            translations[node.tag] = node.text
    assert translations == golden["recipeTranslations"], "MO recipe translations changed during split"
    actual = {}
    for node in mo:
        name = node.findtext("defName") or node.get("Name")
        if name and name.startswith("AMJC_"):
            normalized = deepcopy(node)
            for element, (expected, historical) in AMJ_GRAPHICS.get(name, {}).items():
                normalized.find(element).text = historical
            raw = json.dumps(contract_signature(normalized), ensure_ascii=False, separators=(",", ":"))
            actual[node.tag + ":" + name] = hashlib.sha256(raw.encode()).hexdigest()
    from validate_grains_chain import SHARED_NAMES
    assert set(actual) == set(golden["sha256"]) | {n.tag+":"+n.findtext("defName") for n in mo if n.findtext("defName") in SHARED_NAMES}, "Unknown MO AMJC contract"
    assert {k: actual[k] for k in golden["sha256"]} == golden["sha256"], "MO-loaded explicit AMJC contracts differ from the pre-split snapshot"
    def get(name):
        matches = [node for node in base if node.findtext("defName") == name]
        assert len(matches) == 1, name
        return matches[0]
    assert get("AMJC_Plant_Barley").find("plant/sowResearchPrerequisites") is None
    barley = get("AMJC_Plant_Barley")
    for element, folder in (("graphicData/texPath", "FullGrown"), ("plant/immatureGraphicPath", "Immature")):
        stem = barley.findtext(element)
        assert stem == "Things/Plants/" + folder + "/AMJC_Awa", "Unexpected Base barley placeholder"
        assert any((ROOT / "Textures" / stem).glob("*.png")), "Missing AMJ barley placeholder family"
    table = get("AMJC_GrainProcessingTable")
    assert table.findtext("costList/Steel") == "30" and table.find("researchPrerequisites") is None
    assert [n.text for n in get("AMJC_GrainProcessingSpot").findall("stuffCategories/li")] == ["Woody"]
    assert [n.text for n in get("AMJC_Villager").findall("apparelTags/li")] == ["Neolithic"]
    for node in base.findall("RecipeDef"):
        assert node.find("products/DankPyon_Straw") is None
        if (node.findtext("defName") or "").startswith("AMJC_Thresh"):
            assert len(node.findall("products/*")) == 1
    assert any(n.findtext("defName") == "AMJC_ThreshWheat" for n in base)
    print("Grains Base MO identifier/class references 0; 38 pre-split MO contracts preserved except 4 approved AMJ-priority texture paths: PASS")
    print("Known MO texture paths absent from Base: PASS; inherited/full game references and runtime texture resolution are not validated; see Docs/GrainsDependencyAudit.md")


if __name__ == "__main__":
    validate()
