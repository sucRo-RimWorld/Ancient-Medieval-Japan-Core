from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return ET.parse(ROOT / rel).getroot()

def find_def(root, tag, name):
    for node in root.findall(tag):
        d = node.find("defName")
        if d is not None and d.text == name:
            return node
    raise AssertionError(f"missing {tag} {name}")

def text(node, path):
    child = node.find(path)
    assert child is not None and child.text is not None, f"missing {path}"
    return child.text.strip()

def num(node, path):
    return float(text(node, path))

about = load("About/About.xml")
assert text(about, "packageId") == "sucro.ancientmedievaljapan.core"
deps = [n.findtext("packageId") for n in about.findall("./modDependencies/li")]
assert "DankPyon.Medieval.Overhaul" in deps

plants = load("Defs/ThingDefs_Plants/Plants_StageA.xml")
items = load("Defs/ThingDefs_Items/Items_StageA_Grains.xml")
buildings = load("Defs/ThingDefs_Buildings/Buildings_GrainProcessing.xml")
recipes = load("Defs/RecipeDefs/Recipes_GrainProcessing.xml")

awa = find_def(plants, "ThingDef", "AMJC_Plant_FoxtailMillet_Awa")
assert num(awa, "plant/growDays") == 6
assert num(awa, "plant/harvestYield") == 13
assert num(awa, "plant/fertilityMin") == 0.5
assert num(awa, "plant/fertilitySensitivity") == 0.4
assert num(awa, "plant/minGrowthTemperature") == 8
assert num(awa, "plant/maxGrowthTemperature") == 42
assert num(awa, "plant/minOptimalGrowthTemperature") == 18
assert num(awa, "plant/maxOptimalGrowthTemperature") == 32
assert num(awa, "plant/sowMinSkill") == 0
assert text(awa, "plant/harvestedThingDef") == "AMJC_RawMillet"

jp = load("Languages/Japanese/DefInjected/ThingDef/AMJC_StageA.xml")
assert text(jp, "AMJC_RawMillet.label") == "雑穀束"
mo_jp = load("Languages/Japanese/DefInjected/ThingDef/AMJC_MO_Overrides.xml")
assert text(mo_jp, "DankPyon_RawWheat.label") == "小麦束"
assert text(awa, "graphicData/graphicClass") == "Graphic_Random"
assert text(awa, "graphicData/texPath") == "Things/Plants/FullGrown/AMJC_Awa"
awa_texture = ROOT / "Textures/Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png"
assert awa_texture.is_file()
png = awa_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256
assert text(awa, "plant/immatureGraphicPath") == "Things/Plants/Immature/AMJC_Awa"
awa_immature_texture = ROOT / "Textures/Things/Plants/Immature/AMJC_Awa/AMJC_Awa_Immature.png"
assert awa_immature_texture.is_file()
png = awa_immature_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256

raw = find_def(items, "ThingDef", "AMJC_RawMillet")
in_hull = find_def(items, "ThingDef", "AMJC_MilletInHull")
millet = find_def(items, "ThingDef", "AMJC_Millet")

def assert_stack_graphic(node, tex_path, rel_dir, stem):
    assert text(node, "graphicData/graphicClass") == "Graphic_StackCount"
    assert text(node, "graphicData/texPath") == tex_path
    for suffix in ("a", "b", "c"):
        p = ROOT / rel_dir / f"{stem}_{suffix}.png"
        assert p.is_file(), f"missing stack texture {p}"
        png = p.read_bytes()
        assert png[:8] == b"\x89PNG\r\n\x1a\n"
        assert int.from_bytes(png[16:20], "big") == 256
        assert int.from_bytes(png[20:24], "big") == 256

assert_stack_graphic(
    raw,
    "Things/Item/Resource/AMJC_Millet/RawMillet",
    "Textures/Things/Item/Resource/AMJC_Millet/RawMillet",
    "RawMillet",
)
assert_stack_graphic(
    in_hull,
    "Things/Item/Resource/AMJC_Millet/MilletInHull",
    "Textures/Things/Item/Resource/AMJC_Millet/MilletInHull",
    "MilletInHull",
)
assert_stack_graphic(
    millet,
    "Things/Item/Resource/AMJC_Millet/Millet",
    "Textures/Things/Item/Resource/AMJC_Millet/Millet",
    "Millet",
)

def rot_days(node):
    for comp in node.findall("./comps/li"):
        if comp.attrib.get("Class") == "CompProperties_Rottable":
            return float(text(comp, "daysToRotStart"))
    raise AssertionError("missing rottable comp")

assert rot_days(raw) == 120
assert rot_days(in_hull) == 120
assert rot_days(millet) == 90
assert num(millet, "statBases/Nutrition") == 0.05

for node in (raw, in_hull, millet):
    cats = [li.text for li in node.findall("./thingCategories/li")]
    assert "DankPyon_Cereal" not in cats

spot = find_def(buildings, "ThingDef", "AMJC_GrainProcessingSpot")
table = find_def(buildings, "ThingDef", "AMJC_GrainProcessingTable")
assert num(spot, "costStuffCount") == 10
assert num(spot, "statBases/WorkTableWorkSpeedFactor") == 0.5
assert num(table, "costList/DankPyon_IronIngot") == 30
assert num(table, "statBases/WorkTableWorkSpeedFactor") == 1.0
assert text(table, "researchPrerequisites/li") == "DankPyon_BasicAgriculture"

def recipe(name):
    return find_def(recipes, "RecipeDef", name)

def recipe_users(node):
    users = [li.text for li in node.findall("./recipeUsers/li")]
    if users:
        return sorted(users)

    parent_name = node.attrib.get("ParentName")
    assert parent_name, "recipe has no direct recipeUsers and no ParentName"

    parent = None
    for candidate in recipes.findall("RecipeDef"):
        if candidate.attrib.get("Name") == parent_name:
            parent = candidate
            break

    assert parent is not None, f"missing RecipeDef parent {parent_name}"
    return sorted(li.text for li in parent.findall("./recipeUsers/li"))

def product_count(node, name):
    p = node.find(f"./products/{name}")
    assert p is not None and p.text is not None, f"missing product {name}"
    return int(p.text)

expected_users = sorted(["AMJC_GrainProcessingSpot", "AMJC_GrainProcessingTable"])

cases = {
    "AMJC_ThreshMillet": (15, "AMJC_RawMillet", 1, {"AMJC_MilletInHull": 1, "DankPyon_Straw": 1}),
    "AMJC_ThreshMilletBulk": (120, "AMJC_RawMillet", 10, {"AMJC_MilletInHull": 10, "DankPyon_Straw": 10}),
    "AMJC_HullMillet": (10, "AMJC_MilletInHull", 1, {"AMJC_Millet": 1}),
    "AMJC_HullMilletBulk": (80, "AMJC_MilletInHull", 10, {"AMJC_Millet": 10}),
}

for name, (work, input_def, input_count, products) in cases.items():
    r = recipe(name)
    assert num(r, "workAmount") == work
    assert recipe_users(r) == expected_users
    assert text(r, "ingredients/li/filter/thingDefs/li") == input_def
    assert num(r, "ingredients/li/count") == input_count
    for p, count in products.items():
        assert product_count(r, p) == count

thresh_one = recipe("AMJC_ThreshMillet")
thresh_bulk = recipe("AMJC_ThreshMilletBulk")
hull_one = recipe("AMJC_HullMillet")
hull_bulk = recipe("AMJC_HullMilletBulk")

raw_count = 13
bulk, rem = divmod(raw_count, 10)
hulls = bulk * product_count(thresh_bulk, "AMJC_MilletInHull") + rem * product_count(thresh_one, "AMJC_MilletInHull")
straw = bulk * product_count(thresh_bulk, "DankPyon_Straw") + rem * product_count(thresh_one, "DankPyon_Straw")
hbulk, hrem = divmod(hulls, 10)
edible = hbulk * product_count(hull_bulk, "AMJC_Millet") + hrem * product_count(hull_one, "AMJC_Millet")

assert hulls == 13
assert straw == 13
assert edible == 13
assert num(thresh_bulk, "workAmount") < num(thresh_one, "workAmount") * 10
assert num(hull_bulk, "workAmount") < num(hull_one, "workAmount") * 10

fixture = load("Tests/E2E/MOFixture/Defs/AMJ_MO_Prereqs.xml")
fixture_names = {n.findtext("defName") for n in fixture}
for needed in ("DankPyon_RawWood", "DankPyon_IronIngot", "DankPyon_Straw", "DankPyon_BasicAgriculture"):
    assert needed in fixture_names

print("AMJ Stage A static validation: PASS")
