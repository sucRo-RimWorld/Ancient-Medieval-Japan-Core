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

# Explicitly requested visual changes only. Historical hashes remain immutable;
# validate exact current paths, then normalize only graphics for the MO contract.
AMJ_GRAPHICS = {
    "AMJC_Plant_FoxtailMillet_Awa": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Awa_Simple", "Things/Plants/FullGrown/AMJC_Awa"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Awa_Simple", "Things/Plants/Immature/AMJC_Awa"),
    },
    "AMJC_Plant_BarnyardMillet_Hie": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Hie_Simple", "Things/Plants/FullGrown/AMJC_Hie"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Hie_Simple", "Things/Plants/Immature/AMJC_Hie"),
    },
    "AMJC_Plant_ProsoMillet_Kibi": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Kibi_Simple", "Things/Plants/FullGrown/AMJC_Kibi"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Kibi_Simple", "Things/Plants/Immature/AMJC_Kibi"),
    },
    "AMJC_Plant_Buckwheat_Soba": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Soba_Simple", "Things/Plants/FullGrown/AMJC_Soba"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Soba_Simple", "Things/Plants/Immature/AMJC_Soba"),
    },
    "AMJC_Plant_Barley": {
        "graphicData/texPath": ("Things/Plants/FullGrown/AMJC_Barley_Simple", "Things/Plants/FullGrown/WheatPlant"),
        "plant/immatureGraphicPath": ("Things/Plants/Immature/AMJC_Barley_Simple", "Things/Plants/Immature/WheatPlant"),
    },
    "AMJC_RawMillet": {
        "graphicData/texPath": ("Things/Item/Resource/AMJC_Millet/MixedMilletSheafDense", "Things/Item/Resource/AMJC_Millet/RawMillet"),
    },
    "AMJC_RawBuckwheat": {
        "graphicData/texPath": ("Things/Item/Resource/AMJC_Buckwheat/RawBuckwheatDense", "Things/Item/Resource/AMJC_Buckwheat/RawBuckwheat"),
    },
    "AMJC_RawBarley": {
        "graphicData/texPath": ("Things/Item/Resource/AMJC_Barley/RawBarleyDense", "Things/Item/Resource/AMJC_Millet/RawMillet"),
    },
    "AMJC_GrainProcessingSpot": {
        "graphicData/texPath": ("Things/Building/Production/TableStonecutter", "Things/Building/Production/StonecuttingSpot"),
    },
    "AMJC_GrainProcessingTable": {
        "graphicData/texPath": ("Things/Building/Production/TableStonecutter", "Things/Building/Production/Millstone"),
    },
}


# Immutable MO pre-split hashes include the five shared PlantDef descriptions.
# Do not rewrite that snapshot for author-approved historical localization.
# Check all five present descriptions against the canonical approved English in
# Docs/LocalizationHistoricalReview.md §8, then restore ONLY the historical
# description text on a deep copy for the existing all-fields hash contract.
HISTORICAL_MO_PLANT_DESCRIPTIONS = {
    "AMJC_Plant_FoxtailMillet_Awa": "Foxtail millet (awa), a traditional dryland millet used as a staple grain. It takes longer to mature than kibi but produces more grain per harvest, making it well suited to ordinary main fields.",
    "AMJC_Plant_BarnyardMillet_Hie": "Japanese barnyard millet (hie), a traditional grain crop suited to cool growing conditions. It can keep growing at lower temperatures than awa or kibi, but it is not especially frost hardy.",
    "AMJC_Plant_ProsoMillet_Kibi": "Proso millet (kibi), a fast-growing traditional millet suited to short growing seasons and poorer soils. It matures faster than awa or hie but produces less grain per harvest.",
    "AMJC_Plant_Buckwheat_Soba": "Buckwheat (soba), a very fast-growing grain crop suited to poor soils and short growing seasons. It performs well where richer-soil cereals are inefficient, but it is relatively vulnerable to frost.",
    "AMJC_Plant_Barley": "Barley, a cool-season cereal crop suited to relatively poor soils and cold growing conditions. It takes longer to mature than the Stage A millets but yields a larger harvest and is useful as a staple grain.",
}


def approved_plant_descriptions(root):
    text = (root / "Docs/LocalizationHistoricalReview.md").read_text(encoding="utf-8")
    assert "## 8. English descriptions translated" in text, "Missing approved English crop section"
    chapter = text.split("## 8.", 1)[1]
    entries = {}
    for row in chapter.splitlines():
        if not row.startswith("| `"):
            continue
        cells = [value.strip() for value in row.split("|")]
        name = cells[1].strip("`")
        assert name not in entries, "Duplicate approved English crop description: " + name
        entries[name] = cells[2]
    assert set(entries) == set(HISTORICAL_MO_PLANT_DESCRIPTIONS) | {"Plant_Rice"}, (
        "Approved English crop list changed"
    )
    return entries


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
    # The 2026-10-08 approved *functional* wording correction removes the
    # unsupported claim of a Straw byproduct in the common/Base locale.
    # Preserve the immutable MO pre-split fixture, compare this exactly
    # allowlisted translation delta, then compare ALL other keys unchanged.
    # (MO still gets Straw from its conditional thresh Recipe.)
    neutral_descriptions = {
        'AMJC_ThreshMillet.description': '雑穀束を脱穀し、殻付き雑穀にする。',
        'AMJC_ThreshMilletBulk.description': '雑穀束10個をまとめて脱穀し、殻付き雑穀にする。',
        'AMJC_ThreshBuckwheat.description': 'ソバ束を脱穀し、殻付きソバにする。',
        'AMJC_ThreshBuckwheatBulk.description': 'ソバ束10個をまとめて脱穀し、殻付きソバにする。',
        'AMJC_ThreshBarley.description': '大麦束を脱穀し、殻付き大麦にする。',
        'AMJC_ThreshBarleyBulk.description': '大麦束10個をまとめて脱穀し、殻付き大麦にする。',
    }
    for key, value in neutral_descriptions.items():
        assert translations[key] == value, 'Approved neutral processing text changed: ' + key
        translations[key] = golden["recipeTranslations"][key]
    assert translations == golden["recipeTranslations"], "MO recipe translations changed during split"
    crop_descriptions = approved_plant_descriptions(ROOT)
    actual = {}
    for node in mo:
        name = node.findtext("defName") or node.get("Name")
        if name and name.startswith("AMJC_"):
            normalized = deepcopy(node)
            for element, (expected, historical) in AMJ_GRAPHICS.get(name, {}).items():
                normalized.find(element).text = historical
            if name in HISTORICAL_MO_PLANT_DESCRIPTIONS:
                assert normalized.findtext("description") == crop_descriptions[name], (
                    "Approved English crop description changed: " + name
                )
                normalized.find("description").text = HISTORICAL_MO_PLANT_DESCRIPTIONS[name]
            raw = json.dumps(contract_signature(normalized), ensure_ascii=False, separators=(",", ":"))
            actual[node.tag + ":" + name] = hashlib.sha256(raw.encode()).hexdigest()
    from validate_grains_chain import SHARED_NAMES
    rice_names = {"ThingDef:AMJC_RiceSheaf", "ThingDef:AMJC_RiceInHull",
                  "RecipeDef:AMJC_RiceProcessingBase",
                  "RecipeDef:AMJC_ThreshRice", "RecipeDef:AMJC_ThreshRiceBulk",
                  "RecipeDef:AMJC_HullRice", "RecipeDef:AMJC_HullRiceBulk"}
    assert set(actual) == set(golden["sha256"]) | {n.tag+":"+n.findtext("defName") for n in mo if n.findtext("defName") in SHARED_NAMES} | rice_names, "Unknown MO AMJC contract"
    assert {k: actual[k] for k in golden["sha256"]} == golden["sha256"], "MO-loaded explicit AMJC contracts differ from the pre-split snapshot"
    def get(name):
        matches = [node for node in base if node.findtext("defName") == name]
        assert len(matches) == 1, name
        return matches[0]
    assert get("AMJC_Plant_Barley").find("plant/sowResearchPrerequisites") is None
    barley = get("AMJC_Plant_Barley")
    for element, folder in (("graphicData/texPath", "FullGrown"), ("plant/immatureGraphicPath", "Immature")):
        stem = barley.findtext(element)
        assert stem == "Things/Plants/" + folder + "/AMJC_Barley_Simple", "Unexpected Base barley graphic"
        assert any((ROOT / "Textures" / stem).glob("*.png")), "Missing AMJ barley graphic family"
    wheat = get("AMJC_Plant_Wheat")
    for element, folder in (("graphicData/texPath", "FullGrown"), ("plant/immatureGraphicPath", "Immature")):
        stem = wheat.findtext(element)
        assert stem == "Things/Plants/" + folder + "/AMJC_Wheat_Simple"
        assert any((ROOT / "Textures" / stem).glob("*.png"))
    for name, folder, stem in (("AMJC_RawMillet", "AMJC_Millet", "MixedMilletSheafDense"),
                               ("AMJC_RawBuckwheat", "AMJC_Buckwheat", "RawBuckwheatDense"),
                               ("AMJC_RawBarley", "AMJC_Barley", "RawBarleyDense"),
                               ("AMJC_RawWheat", "AMJC_Wheat", "RawWheatDense")):
        path = "Things/Item/Resource/" + folder + "/" + stem
        assert get(name).findtext("graphicData/texPath") == path
        slots = [(ROOT / "Textures" / path / (stem + "_" + suffix + ".png")).read_bytes() for suffix in "abc"]
        assert slots[0] == slots[1] == slots[2], "Unexpected sheaf stack-variant mismatch: " + name
    table = get("AMJC_GrainProcessingTable")
    assert table.findtext("costList/Steel") == "30" and table.find("researchPrerequisites") is None
    assert [n.text for n in get("AMJC_GrainProcessingSpot").findall("stuffCategories/li")] == ["Woody"]
    assert [n.text for n in get("AMJC_Villager").findall("apparelTags/li")] == ["Neolithic"]
    for node in base.findall("RecipeDef"):
        assert node.find("products/DankPyon_Straw") is None
        if (node.findtext("defName") or "").startswith("AMJC_Thresh"):
            assert len(node.findall("products/*")) == 1
    assert any(n.findtext("defName") == "AMJC_ThreshWheat" for n in base)
    print("Grains Base MO identifier/class references 0; pre-split MO contracts preserved except explicitly allowlisted visual paths: PASS")
    print("Known MO texture paths absent from Base: PASS; inherited/full game references and runtime texture resolution are not validated; see Docs/GrainsDependencyAudit.md")


if __name__ == "__main__":
    validate()
