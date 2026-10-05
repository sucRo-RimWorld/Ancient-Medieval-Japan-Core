from pathlib import Path
import xml.etree.ElementTree as ET
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]

def validate_powershell_encoding(path):
    """Windows PowerShell 5.1 reads BOM-less scripts using the ANSI code page."""
    raw = path.read_bytes()
    source = raw.decode("utf-8-sig")
    assert source.isascii() or raw.startswith(b"\xef\xbb\xbf"), (
        f"non-ASCII PowerShell script must use UTF-8 with BOM for Windows PowerShell 5.1: {path}"
    )

for script in sorted(ROOT.rglob("*.ps1")):
    validate_powershell_encoding(script)

def validate_png(path):
    """Reject truncated/corrupted exports even when their IHDR looks valid."""
    png = path.read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n", f"invalid PNG signature: {path}"
    offset = 8
    compressed = bytearray()
    ended = False
    while offset < len(png):
        assert offset + 12 <= len(png), f"truncated PNG chunk header: {path}"
        length = int.from_bytes(png[offset:offset + 4], "big")
        end = offset + 12 + length
        assert end <= len(png), f"truncated PNG chunk: {path} ({length} declared bytes)"
        kind = png[offset + 4:offset + 8]
        data = png[offset + 8:end - 4]
        crc = int.from_bytes(png[end - 4:end], "big")
        assert zlib.crc32(kind + data) == crc, f"invalid PNG CRC: {path} {kind!r}"
        if kind == b"IDAT":
            compressed.extend(data)
        if kind == b"IEND":
            assert length == 0 and end == len(png), f"invalid PNG end: {path}"
            ended = True
        offset = end
    assert ended and compressed, f"missing PNG image/end: {path}"
    width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", png[16:29])
    assert depth == 8 and color in (3, 6) and (compression, filtering, interlace) == (0, 0, 0), f"unexpected AMJ PNG encoding: {path}"
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(compressed) + decoder.flush()
    assert decoder.eof and not decoder.unused_data, f"incomplete PNG compressed stream: {path}"
    stride = width * (4 if color == 6 else 1) + 1
    assert len(pixels) == height * stride, f"invalid PNG scanline size: {path}"
    assert all(pixels[y * stride] <= 4 for y in range(height)), f"invalid PNG filter: {path}"

for texture in sorted((ROOT / "Textures").rglob("*.png")):
    validate_png(texture)

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

def markdown_row(rel, section_heading, first_cell):
    body = (ROOT / rel).read_text(encoding="utf-8")
    assert section_heading in body, f"missing section {section_heading} in {rel}"
    section = body.split(section_heading, 1)[1]
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0] == first_cell:
            return cells
    raise AssertionError(f"missing markdown row {first_cell} under {section_heading} in {rel}")

about = load("About/About.xml")
assert text(about, "packageId") == "sucro.ancientmedievaljapan.core"
deps = [n.findtext("packageId") for n in about.findall("./modDependencies/li")]
assert "DankPyon.Medieval.Overhaul" in deps

ccto_patch = load("Patches/Compatibility/CCTO_StageA.xml")
wheat_patch = load("Patches/MedievalOverhaul_StageA_Wheat.xml")
plants = load("Defs/ThingDefs_Plants/Plants_StageA.xml")
items = load("Defs/ThingDefs_Items/Items_StageA_Grains.xml")
buildings = load("Defs/ThingDefs_Buildings/Buildings_GrainProcessing.xml")
recipes = load("Defs/RecipeDefs/Recipes_GrainProcessing.xml")

def assert_ccto_patch(def_name, death_temp):
    matches = []
    for op in ccto_patch.findall("Operation"):
        if op.attrib.get("Class") != "PatchOperationFindMod":
            continue
        mods = [li.text.strip() for li in op.findall("./mods/li") if li.text]
        if mods != ["Crop Cold Tolerance Overhaul"]:
            continue
        xpath_node = op.find("./match/xpath")
        if xpath_node is not None and xpath_node.text and def_name in xpath_node.text:
            matches.append(op)
    assert len(matches) == 1, f"expected exactly one CCTO patch for {def_name}"
    op = matches[0]
    assert text(op, "match/xpath") == f'/Defs/ThingDef[defName="{def_name}"]'
    match = op.find("match")
    assert match is not None and match.attrib.get("Class") == "PatchOperationAddModExtension"
    extensions = [node for node in op.findall("./match/value/li") if node.attrib.get("Class") == "CropColdToleranceOverhaul.ColdToleranceExtension"]
    assert len(extensions) == 1, f"{def_name} must add exactly one ColdToleranceExtension"
    assert num(extensions[0], "coldDeathTemperature") == death_temp
    dormancy = extensions[0].find("coldDormancy")
    assert dormancy is None or dormancy.text.strip().lower() == "false"

def assert_crop(def_name, grow_days, harvest_yield, fertility_min, fertility_sensitivity,
                min_temp, max_temp, min_opt, max_opt, sow_min_skill, harvested_def):
    crop = find_def(plants, "ThingDef", def_name)
    assert num(crop, "plant/growDays") == grow_days
    assert num(crop, "plant/harvestYield") == harvest_yield
    assert num(crop, "plant/fertilityMin") == fertility_min
    assert num(crop, "plant/fertilitySensitivity") == fertility_sensitivity
    assert num(crop, "plant/minGrowthTemperature") == min_temp
    assert num(crop, "plant/maxGrowthTemperature") == max_temp
    assert num(crop, "plant/minOptimalGrowthTemperature") == min_opt
    assert num(crop, "plant/maxOptimalGrowthTemperature") == max_opt
    assert num(crop, "plant/sowMinSkill") == sow_min_skill
    assert text(crop, "plant/harvestedThingDef") == harvested_def
    return crop

awa = assert_crop("AMJC_Plant_FoxtailMillet_Awa", 6, 13, 0.5, 0.4, 8, 42, 18, 32, 0, "AMJC_RawMillet")
hie = assert_crop("AMJC_Plant_BarnyardMillet_Hie", 6, 12, 0.5, 0.5, 5, 40, 15, 30, 0, "AMJC_RawMillet")
kibi = assert_crop("AMJC_Plant_ProsoMillet_Kibi", 5, 11, 0.5, 0.3, 8, 42, 18, 32, 0, "AMJC_RawMillet")
soba = assert_crop("AMJC_Plant_Buckwheat_Soba", 4, 8, 0.4, 0.25, 5, 35, 12, 25, 1, "AMJC_RawBuckwheat")
barley = assert_crop("AMJC_Plant_Barley", 10, 22, 0.5, 0.6, 0, 35, 5, 22, 2, "AMJC_RawBarley")
assert text(barley, "plant/sowResearchPrerequisites/li") == "DankPyon_BasicAgriculture"

assert_ccto_patch("AMJC_Plant_FoxtailMillet_Awa", -3)
assert_ccto_patch("AMJC_Plant_BarnyardMillet_Hie", -2)
assert_ccto_patch("AMJC_Plant_ProsoMillet_Kibi", -3)
assert_ccto_patch("AMJC_Plant_Buckwheat_Soba", -2)
assert_ccto_patch("AMJC_Plant_Barley", -8)

for design_name, crop, death in (
    ("アワ", awa, "-3℃"),
    ("ヒエ", hie, "-2℃"),
    ("キビ", kibi, "-3℃"),
    ("ソバ", soba, "-2℃"),
    ("大麦", barley, "-8℃"),
):
    row = markdown_row("Docs/Design.md", "### 4.2.1 Stage A畑作6作物の確定バランス", design_name)
    assert float(row[1]) == num(crop, "plant/growDays")
    assert float(row[2]) == num(crop, "plant/harvestYield")
    assert float(row[3]) == num(crop, "plant/fertilityMin")
    assert float(row[4]) == num(crop, "plant/fertilitySensitivity")
    assert row[7] == death

wheat_design = markdown_row("Docs/Design.md", "### 4.2.1 Stage A畑作6作物の確定バランス", "小麦（MO）")
assert float(wheat_design[1]) == 12
assert float(wheat_design[2]) == 28
assert float(wheat_design[3]) == 0.7
assert float(wheat_design[4]) == 0.9
assert wheat_design[7] == "-6℃"

def fertility_growth_factor(crop, fertility):
    sensitivity = num(crop, "plant/fertilitySensitivity")
    return fertility * sensitivity + (1.0 - sensitivity)

thin_soil_fertility = 0.50
for crop in (soba, kibi, awa, hie, barley):
    assert num(crop, "plant/fertilityMin") <= thin_soil_fertility

assert float(wheat_design[3]) > thin_soil_fertility

expected_thin_soil_factors = (
    (soba, 0.875),
    (kibi, 0.85),
    (awa, 0.80),
    (hie, 0.75),
    (barley, 0.70),
)
for crop, expected in expected_thin_soil_factors:
    assert abs(fertility_growth_factor(crop, thin_soil_fertility) - expected) < 0.0001

actual_order = [
    fertility_growth_factor(crop, thin_soil_fertility)
    for crop in (soba, kibi, awa, hie, barley)
]
assert actual_order == sorted(actual_order, reverse=True)

for cold_name, min_temp, death in (
    ("Foxtail millet", "8°C", "-3°C"),
    ("Barnyard millet", "5°C", "-2°C"),
    ("Proso millet", "8°C", "-3°C"),
    ("Buckwheat", "5°C", "-2°C"),
    ("Barley", "0°C", "-8°C"),
):
    row = markdown_row("Docs/Balance/Crops/ColdTolerance.md", "## 確定した固定枯死・休眠値", cold_name)
    assert row[1] == min_temp
    assert row[2] == death

def top_wheat_patch(class_name, xpath):
    matches = [
        op for op in wheat_patch.findall("Operation")
        if op.attrib.get("Class") == class_name and op.findtext("xpath") == xpath
    ]
    assert len(matches) == 1, f"expected one {class_name} operation for {xpath}"
    return matches[0]

fertility_op = top_wheat_patch(
    "PatchOperationConditional",
    '/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/plant/fertilityMin',
)
assert num(fertility_op, "match/value/fertilityMin") == 0.7
assert num(fertility_op, "nomatch/value/fertilityMin") == 0.7

thing_class_op = top_wheat_patch(
    "PatchOperationReplace",
    '/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/thingClass',
)
assert text(thing_class_op, "value/thingClass") == "Plant"

top_wheat_patch(
    "PatchOperationRemove",
    '/Defs/ThingDef[defName="DankPyon_Plant_Wheat"]/modExtensions/li[@Class="MedievalOverhaul.SecondaryPlantDropExtension"]',
)

raw_wheat_category_op = top_wheat_patch(
    "PatchOperationReplace",
    '/Defs/ThingDef[defName="DankPyon_RawWheat"]/thingCategories',
)
assert text(raw_wheat_category_op, "value/thingCategories/li") == "Foods"

flour_rot_op = top_wheat_patch(
    "PatchOperationReplace",
    '/Defs/ThingDef[defName="DankPyon_Flour"]/comps/li[@Class="CompProperties_Rottable"]/daysToRotStart',
)
assert num(flour_rot_op, "value/daysToRotStart") == 60

for recipe_name in ("DankPyon_CraftFlour_Manual", "DankPyon_CraftFlour", "DankPyon_CraftFlourBulk"):
    top_wheat_patch(
        "PatchOperationRemove",
        f'/Defs/RecipeDef[defName="{recipe_name}"]/products/Hay',
    )

jp = load("Languages/Japanese/DefInjected/ThingDef/AMJC_StageA.xml")
assert text(jp, "AMJC_Plant_FoxtailMillet_Awa.label") == "アワ"
assert text(jp, "AMJC_Plant_BarnyardMillet_Hie.label") == "ヒエ"
assert text(jp, "AMJC_Plant_ProsoMillet_Kibi.label") == "キビ"
assert text(jp, "AMJC_Plant_Buckwheat_Soba.label") == "ソバ"
assert text(jp, "AMJC_Plant_Barley.label") == "大麦"
assert text(jp, "AMJC_RawMillet.label") == "雑穀束"
assert text(jp, "AMJC_RawBuckwheat.label") == "ソバ束"
assert text(jp, "AMJC_BuckwheatInHull.label") == "殻付きソバ"
assert text(jp, "AMJC_Buckwheat.label") == "ソバ穀粒"
assert text(jp, "AMJC_RawBarley.label") == "大麦束"
assert text(jp, "AMJC_BarleyInHull.label") == "殻付き大麦"
assert text(jp, "AMJC_Barley.label") == "大麦穀粒"
assert text(jp, "AMJC_Wheat.label") == "小麦穀粒"
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

assert text(hie, "graphicData/graphicClass") == "Graphic_Random"
assert text(hie, "graphicData/texPath") == "Things/Plants/FullGrown/AMJC_Hie"
hie_texture = ROOT / "Textures/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png"
assert hie_texture.is_file()
png = hie_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256
assert text(hie, "plant/immatureGraphicPath") == "Things/Plants/Immature/AMJC_Hie"
hie_immature_texture = ROOT / "Textures/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png"
assert hie_immature_texture.is_file()
png = hie_immature_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256

assert text(kibi, "graphicData/graphicClass") == "Graphic_Random"
assert text(kibi, "graphicData/texPath") == "Things/Plants/FullGrown/AMJC_Kibi"
kibi_texture = ROOT / "Textures/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png"
assert kibi_texture.is_file()
png = kibi_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256
assert text(kibi, "plant/immatureGraphicPath") == "Things/Plants/Immature/AMJC_Kibi"
kibi_immature_texture = ROOT / "Textures/Things/Plants/Immature/AMJC_Kibi/AMJC_Kibi_Immature.png"
assert kibi_immature_texture.is_file()
png = kibi_immature_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256

assert text(soba, "graphicData/graphicClass") == "Graphic_Random"
assert text(soba, "graphicData/texPath") == "Things/Plants/FullGrown/AMJC_Soba"
soba_texture = ROOT / "Textures/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png"
assert soba_texture.is_file()
png = soba_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256
assert text(soba, "plant/immatureGraphicPath") == "Things/Plants/Immature/AMJC_Soba"
soba_immature_texture = ROOT / "Textures/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png"
assert soba_immature_texture.is_file()
png = soba_immature_texture.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert int.from_bytes(png[16:20], "big") == 256
assert int.from_bytes(png[20:24], "big") == 256

raw = find_def(items, "ThingDef", "AMJC_RawMillet")
in_hull = find_def(items, "ThingDef", "AMJC_MilletInHull")
millet = find_def(items, "ThingDef", "AMJC_Millet")
raw_buckwheat = find_def(items, "ThingDef", "AMJC_RawBuckwheat")
buckwheat_in_hull = find_def(items, "ThingDef", "AMJC_BuckwheatInHull")
buckwheat = find_def(items, "ThingDef", "AMJC_Buckwheat")
raw_barley = find_def(items, "ThingDef", "AMJC_RawBarley")
barley_in_hull = find_def(items, "ThingDef", "AMJC_BarleyInHull")
barley_grain = find_def(items, "ThingDef", "AMJC_Barley")
wheat_grain = find_def(items, "ThingDef", "AMJC_Wheat")

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

assert_stack_graphic(
    buckwheat_in_hull,
    "Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull",
    "Textures/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull",
    "BuckwheatInHull",
)

def rot_days(node):
    for comp in node.findall("./comps/li"):
        if comp.attrib.get("Class") == "CompProperties_Rottable":
            return float(text(comp, "daysToRotStart"))
    raise AssertionError("missing rottable comp")

assert rot_days(raw) == 120
assert rot_days(in_hull) == 120
assert rot_days(millet) == 90
assert rot_days(raw_buckwheat) == 120
assert rot_days(buckwheat_in_hull) == 120
assert rot_days(buckwheat) == 60
assert rot_days(raw_barley) == 120
assert rot_days(barley_in_hull) == 120
assert rot_days(barley_grain) == 90
assert rot_days(wheat_grain) == 90
assert num(millet, "statBases/Nutrition") == 0.05
assert num(buckwheat, "statBases/Nutrition") == 0.05
assert num(barley_grain, "statBases/Nutrition") == 0.05
assert num(wheat_grain, "statBases/Nutrition") == 0.05

for node in (raw, in_hull, millet, raw_buckwheat, buckwheat_in_hull, buckwheat, raw_barley, barley_in_hull, barley_grain):
    cats = [li.text for li in node.findall("./thingCategories/li")]
    assert "DankPyon_Cereal" not in cats

wheat_categories = [li.text for li in wheat_grain.findall("./thingCategories/li")]
assert "DankPyon_Cereal" in wheat_categories

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
    "AMJC_ThreshBuckwheat": (15, "AMJC_RawBuckwheat", 1, {"AMJC_BuckwheatInHull": 1, "DankPyon_Straw": 1}),
    "AMJC_ThreshBuckwheatBulk": (120, "AMJC_RawBuckwheat", 10, {"AMJC_BuckwheatInHull": 10, "DankPyon_Straw": 10}),
    "AMJC_HullBuckwheat": (10, "AMJC_BuckwheatInHull", 1, {"AMJC_Buckwheat": 1}),
    "AMJC_HullBuckwheatBulk": (80, "AMJC_BuckwheatInHull", 10, {"AMJC_Buckwheat": 10}),
    "AMJC_ThreshBarley": (15, "AMJC_RawBarley", 1, {"AMJC_BarleyInHull": 1, "DankPyon_Straw": 1}),
    "AMJC_ThreshBarleyBulk": (120, "AMJC_RawBarley", 10, {"AMJC_BarleyInHull": 10, "DankPyon_Straw": 10}),
    "AMJC_HullBarley": (10, "AMJC_BarleyInHull", 1, {"AMJC_Barley": 1}),
    "AMJC_HullBarleyBulk": (80, "AMJC_BarleyInHull", 10, {"AMJC_Barley": 10}),
    "AMJC_ThreshWheat": (15, "DankPyon_RawWheat", 1, {"AMJC_Wheat": 1, "DankPyon_Straw": 1}),
    "AMJC_ThreshWheatBulk": (120, "DankPyon_RawWheat", 10, {"AMJC_Wheat": 10, "DankPyon_Straw": 10}),
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

soba_thresh = recipe("AMJC_ThreshBuckwheat")
soba_hull = recipe("AMJC_HullBuckwheat")
assert product_count(soba_thresh, "AMJC_BuckwheatInHull") == 1
assert product_count(soba_thresh, "DankPyon_Straw") == 1
assert product_count(soba_hull, "AMJC_Buckwheat") == 1
assert 8 * product_count(soba_thresh, "AMJC_BuckwheatInHull") * product_count(soba_hull, "AMJC_Buckwheat") == 8

barley_thresh = recipe("AMJC_ThreshBarley")
barley_hull = recipe("AMJC_HullBarley")
assert product_count(barley_thresh, "AMJC_BarleyInHull") == 1
assert product_count(barley_thresh, "DankPyon_Straw") == 1
assert product_count(barley_hull, "AMJC_Barley") == 1
assert 22 * product_count(barley_thresh, "AMJC_BarleyInHull") * product_count(barley_hull, "AMJC_Barley") == 22

wheat_thresh = recipe("AMJC_ThreshWheat")
assert product_count(wheat_thresh, "AMJC_Wheat") == 1
assert product_count(wheat_thresh, "DankPyon_Straw") == 1
assert 28 * product_count(wheat_thresh, "AMJC_Wheat") == 28

fixture = load("Tests/E2E/MOFixture/Defs/AMJ_MO_Prereqs.xml")
fixture_names = {n.findtext("defName") for n in fixture}
for needed in ("DankPyon_RawWood", "DankPyon_IronIngot", "DankPyon_Straw", "DankPyon_BasicAgriculture"):
    assert needed in fixture_names

from validate_new_village import validate as validate_new_village
validate_new_village()

print("AMJ Stage A static validation: PASS")
