# Ancient & Medieval Japan - Grains（中世日本 - 穀類）

**RimWorld 1.6 — Development build**

A standalone grain-growing and food-processing Mod inspired by agriculture in pre-Edo Japan. Formerly AMJ Core; the historical `sucro.ancientmedievaljapan.core` packageId and existing AMJC DefNames remain unchanged to retain stable identifiers for cross-Mod compatibility.

## Features

- Awa, Hie and Kibi, with different growing seasons, soil fertility requirements and temperature preferences.
- Soba, barley, wheat and upland rice (using Vanilla `Plant_Rice`).
- Harvested sheaves, threshing and hulling, grain milling, and basic flour foods.
- Vanilla-only wheat, wheat flour and manual millstone when Medieval Overhaul is absent.
- MO wheat/RawWheat/flour/millstone reuse and thresh-time Straw integration when MO is present, without duplicate default wheat or milling routes. AMJG-owned balance and processing settings take priority.

The balancing model and crops are specified in [Design](Docs/Design.md) and [cultivation balance](Docs/Balance/Crops/Millet_Cultivation_Balance.md).

## Dependencies and compatibility

**Required:** RimWorld 1.6. **No mandatory additional Mods or DLC.**

**Optional:** Medieval Overhaul (MO) and [Crop Cold Tolerance Overhaul](https://steamcommunity.com/sharedfiles/filedetails/?id=3812412548) (CCTO).

The `loadAfter` entry for MO is an **optional ordering hint, not a hard dependency**. MO-specific definitions and patches load only when MO is active through `loadFolders.xml`; `BaseWithoutMO` supplies the fallback path otherwise. CCTO adds explicit cold-death support when installed.

New Village is now owned by the separate AMJ Scenarios Mod. Grains keeps a conditional legacy compatibility copy only when Scenarios is absent.

## Development status

The author confirmed on 2026-10-10 that Grains has not been installed or used. **There are no existing Grains saves to migrate.** Historical save migration, enabling/disabling mid-save and removing MO from old saves are **out of scope**, not release blockers.

The mandatory MO dependency has been removed. Previous fresh-start Vanilla / MO × CCTO tests passed on their tested revisions; current-revision game loading and native Bills, final graphics, UI/language and gameplay balance remain to be verified. This development build has not been publicly released.

## Documentation

- [Design and ownership](Docs/Design.md)
- [MO dependency audit](Docs/GrainsDependencyAudit.md)
- [Four-profile testing and open runtime gates](Docs/GrainsProfileTesting.md)
- [Crop cold tolerance](Docs/Balance/Crops/ColdTolerance.md)
- [Development tools](Docs/DevelopmentTools.md)
