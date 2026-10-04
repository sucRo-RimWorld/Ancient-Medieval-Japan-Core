# Ancient & Medieval Japan Core

**RimWorld 1.6 — Development build**

Ancient & Medieval Japan Core (AMJC) extends Medieval Overhaul with agriculture, primary processing, materials, and village-life systems inspired by ordinary life in pre-Edo Japan.

The current development slice focuses on field crops and the processing needed to make them useful in a small colony.

## Millet crop choices

AMJC intentionally gives **Awa (foxtail millet), Hie (Japanese barnyard millet), and Kibi (proso millet)** different cultivation roles rather than making them interchangeable crops.

| Crop | Best used when... | Main trade-off |
|---|---|---|
| **Kibi / キビ** | the growing season is short or soil fertility is poor | smallest harvest per crop and more frequent sow/harvest work |
| **Awa / アワ** | you have ordinary-to-fertile main fields and enough time to finish the crop | slower than Kibi, but gives more grain per harvest |
| **Hie / ヒエ** | cold temperatures shorten the useful growing season | lower nominal output in ordinary conditions, but keeps growing better on the cold side |

The exact balance values are **gameplay abstractions, not literal real-world measurements**. Real agronomic traits are used as reference points, then translated into RimWorld growth time, fertility sensitivity, and temperature curves.

**Detailed comparison:** [Millet cultivation balance — Awa / Hie / Kibi](Docs/Balance/Crops/Millet_Cultivation_Balance.md)

The detailed page includes bilingual graphs for:
- fertility → growth-rate modifier;
- fertility → theoretical grain-output index;
- temperature → growth-rate modifier.

## Dependencies

Required:
- Medieval Overhaul

Optional:
- Crop Cold Tolerance Overhaul (CCTO), used as the framework for explicit cold-death/dormancy behavior when installed. AMJC owns its custom crops' temperature data and optional compatibility XML.

[AMJC crop cold-tolerance values and data ownership](Docs/Balance/Crops/ColdTolerance.md)

## Save compatibility

Adding to or removing from existing saves has not been verified. AMJC adds custom crops, items, processing content, and will add map/world systems during development. Safe removal is not guaranteed.

## Development documents

- [Core design](Docs/Design.md)
- [Millet cultivation balance](Docs/Balance/Crops/Millet_Cultivation_Balance.md)
- [Art style](Docs/ArtStyle.md)
- [Development tools and testing](Docs/DevelopmentTools.md)

