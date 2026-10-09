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
    print("PASS: 19 exact original-source blob identities, 19 production texture mappings, five three-stack families")

if __name__ == "__main__":
    main()
