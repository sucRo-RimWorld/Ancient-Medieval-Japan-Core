"""Project AMJ-owned Base/MO explicit XML contracts for static validation.

This applies only AMJ's Base-difference Add/Replace operations, not the whole
RimWorld patch engine, inheritance, cross-refs, localization or external MO patches.
"""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MO_FOLDER = "Compatibility/MedievalOverhaul"


def profile_xml(profile="mo", root=ROOT):
    assert profile in {"vanilla", "mo"}
    loader = ET.parse(root / "loadFolders.xml").getroot()
    entries = loader.findall("v1.6/li")
    assert len(entries) == 2 and (entries[0].text or "").strip() == "/"
    assert entries[1].text == MO_FOLDER
    assert entries[1].get("IfModActive") == "DankPyon.Medieval.Overhaul"
    defs = ET.Element("Defs")
    folders = [root / "Defs"]
    if profile == "mo":
        folders.append(root / MO_FOLDER / "Defs")
    for folder in folders:
        for path in sorted(folder.rglob("*.xml")):
            document = ET.parse(path).getroot()
            assert document.tag == "Defs", path
            defs.extend(deepcopy(list(document)))
    if profile == "mo":
        patch = ET.parse(root / MO_FOLDER / "Patches/MedievalOverhaul_StageA_Base.xml").getroot()
        for operation in patch.findall("Operation"):
            selector = operation.findtext("xpath")
            assert selector and selector.startswith("/Defs/")
            targets = defs.findall("./" + selector[len("/Defs/"):])
            assert len(targets) == 1, f"Expected one AMJ target: {selector}"
            value = operation.find("value")
            assert value is not None and len(value) > 0, selector
            target = targets[0]
            if operation.get("Class") == "PatchOperationAdd":
                target.extend(deepcopy(list(value)))
            elif operation.get("Class") == "PatchOperationReplace":
                parents = {child: parent for parent in defs.iter() for child in parent}
                parent = parents[target]
                index = list(parent).index(target)
                parent.remove(target)
                for offset, child in enumerate(value):
                    parent.insert(index + offset, deepcopy(child))
            else:
                raise AssertionError("Unsupported static Base difference: " + str(operation.attrib))
    return defs


def contract_signature(node):
    groups = {}
    for child in node:
        groups.setdefault(child.tag, []).append(contract_signature(child))
    return [node.tag, sorted(node.attrib.items()), (node.text or "").strip(), sorted(groups.items())]
