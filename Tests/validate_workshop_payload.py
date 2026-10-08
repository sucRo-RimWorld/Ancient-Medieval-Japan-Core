#!/usr/bin/env python3
"""Audit YADA exclusions against the actual tracked inventory or a final payload.

Scanner semantics: inherited case-insensitive basename patterns. Paths and
negation are intentionally rejected. See Project Docs/WorkshopPackaging.md.
"""
import argparse
import io
import zipfile
import xml.etree.ElementTree as ET
import fnmatch
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = {
    "About": {".xml", ".png", ".jpg", ".jpeg", ".txt"},
    "Assemblies": {".dll"}, "Defs": {".xml"}, "Patches": {".xml"},
    "Languages": {".xml"}, "Textures": {".png", ".jpg", ".jpeg", ".dds"},
    "Sounds": {".ogg", ".wav"},
}


def patterns(text):
    result = [s.strip() for s in text.splitlines() if s.strip() and not s.strip().startswith("#")]
    bad = [p for p in result if "/" in p or "\\" in p or p.startswith("!") or "[" in p or "**" in p]
    if bad:
        raise ValueError("Unsupported YADA basename rules: " + repr(bad))
    return result


def ignored(path, rules):
    return any(fnmatch.fnmatchcase(part.lower(), rule.lower())
               for part in PurePosixPath(path).parts for rule in rules)


def subscriber_file(path):
    p = PurePosixPath(path)
    if p.name in {"LICENSE", "LICENSE.txt", "NOTICE", "NOTICE.txt", "COPYING", "COPYING.txt"}:
        return True
    if path == "loadFolders.xml":
        return True
    parts = p.parts
    if parts[:2] == ("Compatibility", "MedievalOverhaul"):
        parts = parts[2:]
    elif parts[:3] == ("LegacyStartingScenarios", "Compatibility", "MedievalOverhaul"):
        parts = parts[3:]
    elif parts[:1] == ("LegacyStartingScenarios",):
        parts = parts[1:]
    elif parts[:1] == ("BaseWithoutMO",):
        parts = parts[1:]
    if len(parts) > 1 and parts[0] in RUNTIME:
        return p.suffix.lower() in RUNTIME[parts[0]]
    return False


def audit(paths, rules):
    kept = sorted(p for p in paths if not ignored(p, rules))
    leaks = [p for p in kept if not subscriber_file(p)]
    lost = [p for p in paths if subscriber_file(p) and ignored(p, rules)
            and PurePosixPath(p).name != "_LocalTest.xml"
            and not any(fnmatch.fnmatchcase(PurePosixPath(p).name.lower(), pat)
                        for pat in ("*.quicktests.dll", "*.tests.dll", "*.e2e.dll", "*.bak", "*.tmp"))]
    return kept, leaks, lost


def self_test():
    rules = patterns("Art\nDocs\nSource\nTests\nTestResults\nDevQuickstarts\n*.bat\n*.pdb\n_LocalTest.xml\n*.Tests.dll\n")
    unwanted = ["Art/Sources/master.png", "TestResults/SourceSync/Defs/Plants.xml",
                "Docs/description.txt", "Tests/Fixture/About/About.xml", "Source/code.cs",
                "DevQuickstarts/Assemblies/Quick.dll", "build.bat", "Assemblies/mod.pdb",
                "Patches/_LocalTest.xml", "Assemblies/Mod.Tests.dll"]
    runtime = ["About/About.xml", "About/Preview.png", "About/PublishedFileId.txt",
               "Defs/Plants.xml", "Languages/Japanese/Keyed/Mod.xml", "Textures/Plant.png",
               "Assemblies/Mod.dll", "Patches/Compatibility/Mod.xml", "loadFolders.xml", "LICENSE",
               "BaseWithoutMO/Defs/Wheat.xml", "BaseWithoutMO/Patches/CCTO.xml",
               "BaseWithoutMO/Languages/Japanese/DefInjected/ThingDef/Wheat.xml",
               "Compatibility/MedievalOverhaul/Defs/Recipes.xml",
               "Compatibility/MedievalOverhaul/Patches/MO.xml",
               "Compatibility/MedievalOverhaul/Languages/Japanese/DefInjected/ThingDef/MO.xml",
               "LegacyStartingScenarios/Defs/Scenarios/Village.xml",
               "LegacyStartingScenarios/Languages/Japanese/Keyed/Scenario.xml",
               "LegacyStartingScenarios/Compatibility/MedievalOverhaul/Patches/StartingScenarios.xml"]
    kept, leaks, lost = audit(unwanted + runtime, rules)
    assert kept == sorted(runtime) and not leaks and not lost
    assert audit(["NewDeveloperFolder/data.json"], rules)[1]
    assert audit(["Defs/Plants.xml"], rules + ["*.xml"])[2]
    assert ignored("art/Sources/X.png", rules)
    try:
        patterns("Patches/_LocalTest.xml")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported path rule accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, help="JSON array of repository paths (read-only remote audit)")
    parser.add_argument("--payload", type=Path, help="Audit final package without applying exclusions")
    parser.add_argument("--expected-assembly", help="Required runtime DLL basename for compiled Mods")
    args = parser.parse_args()
    self_test()
    rules = patterns((ROOT / ".rimignore").read_text(encoding="utf-8-sig"))
    if args.payload:
        paths = [p.relative_to(args.payload).as_posix() for p in args.payload.rglob("*") if p.is_file()]
        kept, leaks, lost = audit(paths, [])
        leaks += [p for p in paths if ignored(p, rules)]
        if "About/About.xml" not in paths:
            leaks.append("MISSING About/About.xml")
        if "LICENSE" not in paths:
            leaks.append("MISSING LICENSE")
        if args.expected_assembly and "Assemblies/" + args.expected_assembly not in paths:
            leaks.append("MISSING runtime assembly " + args.expected_assembly)
    else:
        if args.expected_assembly:
            parser.error("--expected-assembly requires --payload")
        paths = json.loads(args.inventory.read_text()) if args.inventory else subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").rstrip("\0").split("\0")
        kept, leaks, lost = audit(paths, rules)
    if not args.payload:
        # Current Core archive/publisher adapters must match the same authority.
        legacy = ROOT / ".workshopignore"
        publisher = ROOT / "_PublisherPlus.xml"
        if legacy.exists() and patterns(legacy.read_text()) != rules:
            leaks.append(".workshopignore diverges from .rimignore")
        if publisher.exists() and [e.text for e in ET.parse(publisher).findall("./Excluded/exclude")] != rules:
            leaks.append("PublisherPlus diverges from .rimignore")
        if (ROOT / ".gitattributes").exists() and not args.inventory:
            data = subprocess.check_output(["git", "archive", "--format=zip", "HEAD"], cwd=ROOT)
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                actual = sorted(p for p in archive.namelist() if not p.endswith("/"))
            if actual != kept:
                leaks.append("git archive differs from YADA filter: extra=" + repr(sorted(set(actual)-set(kept)))
                             + "; missing=" + repr(sorted(set(kept)-set(actual))))
    # Release metadata must be present in both filtered checkout and actual upload root.
    actual = paths if args.payload else kept
    for required in ("About/Manifest.xml", "About/Changelog.txt"):
        if required not in actual:
            leaks.append("MISSING " + required)
    if leaks or lost:
        raise SystemExit("FAIL: subscriber-unnecessary files=" + repr(sorted(set(leaks)))
                         + "; excluded runtime/legal files=" + repr(lost))
    print(f"PASS: Workshop filter self-tests; {len(kept)} subscriber files kept, {len(paths)-len(kept)} excluded")


if __name__ == "__main__":
    main()
