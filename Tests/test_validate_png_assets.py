from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from validate_png_assets import PngValidationError, validate_png


def chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def valid_rgba_png() -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    scanline = b"\x00\xff\x00\x00\xff"
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(scanline)) + chunk(b"IEND", b"")


class PngValidatorTests(unittest.TestCase):
    def check_bytes(self, payload: bytes, should_pass: bool) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "asset.png"
            path.write_bytes(payload)
            if should_pass:
                validate_png(path)
            else:
                with self.assertRaises(PngValidationError):
                    validate_png(path)

    def test_valid_png_passes(self) -> None:
        self.check_bytes(valid_rgba_png(), True)

    def test_truncated_idat_is_rejected(self) -> None:
        png = valid_rgba_png()
        idat = png.index(b"IDAT") - 4
        declared = int.from_bytes(png[idat:idat + 4], "big")
        cut = idat + 8 + max(1, declared // 2)
        self.check_bytes(png[:cut], False)

    def test_bad_crc_is_rejected(self) -> None:
        png = bytearray(valid_rgba_png())
        idat = png.index(b"IDAT")
        png[idat + 4] ^= 0x01
        self.check_bytes(bytes(png), False)


if __name__ == "__main__":
    unittest.main()
