# AMJ Authoritative Art Sources

This directory stores accepted high-resolution source artwork that must survive independently of production-resolution exports.

## Rules

- Source files here are authoritative masters once accepted by the author.
- Never overwrite a source merely to make a 256×256 game texture.
- Derive production PNGs from a copy/export and write them under `Textures/`.
- Preserve the source file's original pixel dimensions and alpha unless the author explicitly approves a new master.
- Prefer mirroring the `Textures/` relative path beneath `Art/Sources/` so source and derivative are easy to pair.
- Do not substitute a generated approximation or a production-resolution derivative when the exact accepted high-resolution source is missing.
