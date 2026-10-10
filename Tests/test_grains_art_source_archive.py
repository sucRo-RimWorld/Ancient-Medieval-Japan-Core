#!/usr/bin/env python3
"""Lock exact current crop/sheaf source bytes and production PNG paths, without game-runtime claims."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "Docs/References/GrainsCropSourceManifest.json"

def git_blob_sha1(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()

def main():
    data = json.loads(M.read_text(encoding="utf-8"))
    assets = data["assets"]
    assert len(assets) == 19, len(assets)
    assert len({r["source"] for r in assets}) == 19
    assert len([r for r in assets if r["state"] == "mature"]) == 7
    assert len([r for r in assets if r["state"] == "immature"]) == 7
    assert len([r for r in assets if r["state"] == "sheaf"]) == 5
    for row in assets:
        source = ROOT / row["source"]
        candidate = ROOT / row["candidate"]
        production = ROOT / row["production"]
        assert source.is_file(), f"missing archived source: {source}"
        assert candidate.is_file(), f"missing exact-byte candidate: {candidate}"
        bytes_ = source.read_bytes()
        assert bytes_ == candidate.read_bytes(), f"archive drift: {source}"
        assert git_blob_sha1(bytes_) == row["git_blob_sha1"], f"blob SHA drift: {source}"
        assert bytes_[:8] == b"\x89PNG\r\n\x1a\n", f"bad source PNG: {source}"
        assert production.is_file(), f"missing production PNG: {production}"
        header = production.read_bytes()[:24]
        assert header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", production
        assert struct.unpack(">II", header[16:24]) == (256, 256), production
        if row["state"] == "sheaf":
            assert production.name.endswith("_a.png"), production
            for suffix in ("_b.png", "_c.png"):
                sibling = production.with_name(production.name[:-6] + suffix)
                assert sibling.is_file(), f"missing stack variant: {sibling}"
                assert production.read_bytes() == sibling.read_bytes(), f"stack drift: {sibling}"
    # AMJ-019: preserve the author's exact accepted high-resolution image and all StackCount variants.
    hulled_source = ROOT / "Art/Sources/Things/Item/Resource/AMJC_Millet/MilletInHull/MilletInHull.png"
    source_bytes = hulled_source.read_bytes()
    assert git_blob_sha1(source_bytes) == "61d6720c7354107424400dd9abf0edc0a118b859", "hulled millet master drift"
    assert source_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", source_bytes[16:24]) == (1429, 1100)
    base = ROOT / "Textures/Things/Item/Resource/AMJC_Millet/MilletInHull"
    pngs = [(base / f"MilletInHull_{suffix}.png").read_bytes() for suffix in ("a", "b", "c")]
    assert pngs[0] == pngs[1] == pngs[2], "millet in-hull StackCount variants differ"
    assert git_blob_sha1(pngs[0]) == "039c6f11bbe5426d169b011a706cfcb3e6802c2f", "hulled millet production drift"
    assert pngs[0][:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", pngs[0][16:24]) == (256, 256)
    xml = (ROOT / "Defs/ThingDefs_Items/Items_StageA_Grains.xml").read_text(encoding="utf-8")
    assert xml.count("<defName>AMJC_MilletInHull</defName>") == 1
    graphic = xml.split("<defName>AMJC_MilletInHull</defName>", 1)[1].split("</ThingDef>", 1)[0]
    assert "<texPath>Things/Item/Resource/AMJC_Millet/MilletInHull</texPath>" in graphic
    assert "<graphicClass>Graphic_StackCount</graphicClass>" in graphic
    print("PASS: exact accepted millet in-hull master, three identical 256px textures and loaded Def path")

    # AMJ-011: exact author-accepted hulled-barley source and isolated StackCount art.
    barley_source = ROOT / "Art/Sources/Things/Item/Resource/AMJC_Barley/BarleyInHull/BarleyInHull.png"
    barley_source_bytes = barley_source.read_bytes()
    assert git_blob_sha1(barley_source_bytes) == "2cb0f5eb972e3b0f574ae61c7b4150336c5adbff", "hulled barley source drift"
    assert barley_source_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", barley_source_bytes[16:24]) == (1429, 1100)
    barley_base = ROOT / "Textures/Things/Item/Resource/AMJC_Barley/BarleyInHull"
    barley_pngs = [(barley_base / f"BarleyInHull_{suffix}.png").read_bytes() for suffix in ("a", "b", "c")]
    assert barley_pngs[0] == barley_pngs[1] == barley_pngs[2], "hulled barley stack drift"
    assert git_blob_sha1(barley_pngs[0]) == "b047aaccdbbc3f31c3a0be3eb57f4077eb42c3d4", "hulled barley PNG drift"
    assert barley_pngs[0][:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", barley_pngs[0][16:24]) == (256, 256)
    assert xml.count("<defName>AMJC_BarleyInHull</defName>") == 1
    barley_xml = xml.split("<defName>AMJC_BarleyInHull</defName>", 1)[1].split("</ThingDef>", 1)[0]
    assert "<texPath>Things/Item/Resource/AMJC_Barley/BarleyInHull</texPath>" in barley_xml
    assert "<graphicClass>Graphic_StackCount</graphicClass>" in barley_xml
    print("PASS: author-accepted hulled barley source, 3 stack PNGs and dedicated graphic path")

    print("PASS: 19 exact original-source blob identities, 19 production texture mappings, five three-stack families")

if __name__ == "__main__":
    main()
