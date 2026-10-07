# Medieval Overhaul Japanization Military Mapping Audit

## Status and scope

This document is the Def-level follow-up to
`Docs/Research/MedievalOverhaulJapanizationResearchAudit.md`.

It audits the actual Medieval Overhaul 1.6.2.2 military/equipment Defs gated by
research nodes that `AMJ - Medieval Overhaul Japanization` intends to
restructure. It is a **design audit**, not an implementation claim.

Audited archive:

- Workshop archive: `3219596926.zip`
- MO payload: 1.6.2.2
- SHA-256: `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`

The counts below include Defs whose `recipeMaker/researchPrerequisite` or
`researchPrerequisites` requires the node, including multi-prerequisite
adorned items. Upstream DefNames should be preserved wherever practical.

## Mapping rule

Japanization should not invent a Japanese name merely to keep every Western MO
weapon visible.

For each MO Def:

1. **Retexture + relabel** only if the gameplay role, material meaning and
   broad historical period map cleanly to a Japanese counterpart.
2. **Keep function, change research branch** if the object is valid but MO puts
   it in a Western/fantasy progression.
3. **Hide from normal production** if no honest Japanese counterpart is needed.
   Prefer hiding/disconnecting over deleting the upstream Def, to reduce
   compatibility breakage.
4. **Do not collapse distinct gameplay stats** merely for historical tidiness.
   If two MO Defs provide genuinely different gameplay roles and both have
   defensible Japanese referents, both may remain.
5. **Do not preserve redundant Western variation** solely because the upstream
   art has many variants. Heraldic/faction/color variants can be consolidated
   or hidden when they do not add Japanese gameplay value.

---

## 1. Crossbow and fixed-bow branch

### Actual MO coupling

`DankPyon_Crossbow` gates:

- `DankPyon_Crossbow` — handheld crossbow
- `DankPyon_Turret_Scorpio` — fixed scorpio
- scorpio bolt recipes

`DankPyon_HeavyCrossbow` gates:

- `DankPyon_CrossbowHeavy` — arbalest
- `DankPyon_Turret_Ballista` — fixed ballista
- ballista bolt recipes

`DankPyon_Ballista` additionally gates both fixed weapons and both ammunition
families.

`DankPyon_Trebuchet` gates:

- `DankPyon_Turret_Trebuchet`
- stone-boulder ammunition recipes

`DankPyon_RepeaterBallista` gates:

- `DankPyon_Turret_RepeaterBallista`

### Japanization direction

| MO Def / group | First-pass treatment | Rationale |
|---|---|---|
| `DankPyon_Crossbow` | **Retexture + relabel candidate: 弩** | Eighth-century Japanese military crossbow mechanisms are directly attested. Move to ancient state-military technology rather than a late Western crossbow branch. |
| `DankPyon_CrossbowHeavy` | **Further audit** | A stronger handheld crossbow may be defensible, but “arbalest” should not be translated mechanically. Preserve only if stats support a meaningful strong-bow/strong-crossbow distinction. |
| `DankPyon_Turret_Scorpio` | **Retexture + relabel candidate: fixed 弩 / 弩台** | Japanese scholarship distinguishes portable and installed crossbow use. Exact MO footprint, crew model, rate of fire and ammunition must fit before final naming. |
| `DankPyon_Turret_Ballista` | **Retexture candidate, pending stat/size audit** | Could represent a heavier installed 弩 if it remains an ancient defensive emplacement rather than a Roman/European siege engine in behavior. |
| `DankPyon_Turret_Trebuchet` | **Hide by default** | Yuan/Mongol forces brought stone-throwing weapons to Japan, but that does not justify a normal domestic Japanese technology branch. |
| `DankPyon_Turret_RepeaterBallista` | **Hide by default** | No sufficiently strong AMJ-period Japanese standard-tech justification has been established. |

### Structural correction

MO currently couples handheld crossbows and fixed siege weapons. Japanization
should split the unlock logic into at least:

- **portable 弩 technology**;
- **installed 弩 technology** (if final equipment audit passes);
- **foreign/unsupported siege equipment hidden from normal research**.

Do not retain the upstream linear
`Crossbow -> Heavy Crossbow -> Ballista -> Trebuchet/Repeater` progression.

---

## 2. Light protection, shields and chain branch

### `DankPyon_ProtectiveClothing`: 17 MO Defs

The node currently gates a mixed family:

- padded chausses;
- light lamellar;
- padded armor;
- leather boots/gloves;
- padded flat-top / kettle / nasal helmets;
- Zweihander hat;
- round shield;
- four heraldic heater-shield variants;
- kite shield;
- Lindwurm shield;
- living-tree shield.

### Direction

The **research concept** can remain as an early defensive-equipment branch, but
the content cannot be retained wholesale.

- `DankPyon_Apparel_Light_Lamellar` is the strongest direct reuse candidate:
  lamellar construction maps much more naturally to Japanese armor than the
  Western padded/plate ladder.
- Generic padded protection may remain where its gameplay role is culture-neutral.
- Western helmet silhouettes (nasal, kettle, flat-top) require Japanese
  retexture/relabel or hiding.
- Heater/kite/heraldic shield variants should not survive merely as renamed
  Japanese shields. Japanization should keep only shield roles that have a
  defensible Japanese counterpart and gameplay purpose.
- Lindwurm/living-tree fantasy shields should be hidden from the historical
  Japanization path.
- The “Zweihander” identity is explicitly Western and must not survive unchanged.

### `DankPyon_ChainArmor`: 23 gated MO Defs

This node gates:

- hauberk / heavy hauberk;
- splinted chausses, boots and gloves;
- chain coif / full chain coif;
- chain nasal, kettle and flat-top helmet families;
- heavy barbrute, open bascinet, Zweihander helmet;
- four Zweihander heraldic variants;
- four adorned mail/chain items that also require `DankPyon_AdornedArmor`.

### Direction

Do **not** treat this as a ready-made Japanese “chain armor tier.”

Japanese chain protection can justify retaining a **limited chain-equipment
branch**, but the MO set is overwhelmingly Western in garment and helmet form.
The node should therefore be curated Def-by-Def:

- preserve a small number of distinct chain-protection gameplay roles if a
  Japanese referent and period are supportable;
- retexture/relabel those retained roles;
- hide redundant bascinet/flat-top/nasal/Zweihander variants rather than invent
  fictional Japanese equivalents;
- remove `ChainArmor` as a mandatory prerequisite for the later Japanese
  armor branch.

A medieval Japanese chain mapping remains lower-confidence than the lamellar /
dōmaru / later plate-heavy mapping and needs dedicated historical verification
before final labels are selected.

---

## 3. Plate armor and late armor branch

### Vanilla `PlateArmor` gates 23 MO Defs

The full XML dependency audit finds these MO-gated items:

Body / limb armor:

- `DankPyon_Apparel_Brigandine`
- `DankPyon_Apparel_Breast_Plate`
- `DankPyon_Apparel_Zweihanders_Cuirass`
- `DankPyon_Apparel_Zweihanders_CuirassFloof`
- `DankPyon_Apparel_FullPlateGilded`
- `DankPyon_Apparel_Lindwurm`
- `DankPyon_Apparel_ChaussesPlate`
- `DankPyon_Footwear_BootsPlate`
- `DankPyon_Handwear_GlovesPlate`
- `DankPyon_Apparel_AdornedHeavyPlate` (also `DankPyon_AdornedArmor`)

Helmets:

- armet / gilded armet;
- closed bascinet;
- klappvisor bascinet variants;
- hounskull;
- great helm;
- sallet variants;
- wolf-ribs bascinet;
- Lindwurm scale helmet;
- adorned great helm (also `DankPyon_AdornedArmor`).

### Japanization direction

The **research role** should become a late-medieval Japanese advanced-armor
branch rather than “European plate armor.”

Historical anchors support:

- high-quality `胴丸` in the Muromachi period;
- later plate-heavy `当世具足`;
- late-16th-century adoption and Japanese manufacture of armor influenced by
  European cuirasses (`南蛮胴具足`).

This does **not** mean every MO plate item maps one-to-one to a Japanese suit.
Instead:

- select a small set of body/helmet roles that correspond to meaningful stages
  or equipment tradeoffs;
- map those to Japanese armor families through label/description/retexture;
- hide redundant Western helmet subtypes and faction variants;
- hide Lindwurm fantasy armor;
- avoid using “plate armor” as the Japanese public label if the surviving Def
  family represents Japanese composite armor rather than a European full-plate
  suit.

The final late-armor research may unlock several retained MO Defs while hiding
the rest; it does not need to preserve the upstream count.

---

## 4. Adorned armor

`DankPyon_AdornedArmor` gates six Ulrik/oathbound-flavored items:

- adorned mail shirt;
- adorned warrior armor;
- adorned heavy plate;
- adorned heavy mail coif;
- adorned flat-top chainveil helmet;
- adorned great helm.

Descriptions explicitly refer to trophies/holy symbols and MO's Western
religious/heraldic context.

### Direction

Do not merely translate “adorned” into a Japanese label.

Two possible final outcomes:

1. **reinterpret as high-status decorative armor** if the stat premium and
   crafting cost provide an independent gameplay role, with Japanese decorative
   fittings/lacing/heraldic presentation; or
2. **hide/consolidate** if the distinction is primarily Ulrik/Western flavor.

This node should no longer depend mechanically on an unchanged European
`ChainArmor -> PlateArmor` ladder.

---

## 5. Bow branch

MO-specific direct unlocks:

- `DankPyon_HuntingBow` -> `DankPyon_Bow_Hunting`
- `DankPyon_WarBow` -> `Bow_War`

MO also relocates Vanilla `RecurveBow` as “archery” and uses Vanilla
`Greatbow`.

### Direction

Retain the **gameplay distinction** if the stats support it, but rebuild the
research meaning around Japanese bows rather than Western bow evolution.

Candidate structure:

- early hunting/ordinary bow;
- military archery / `弓術`;
- stronger or specialist war-bow role only where it produces a useful gameplay
  distinction.

Do not infer a strict historical Japanese progression merely from MO damage
tiers. Final Def names/images must be selected after stat comparison.

---

## 6. Polearms

Actual MO outputs:

### Basic

- militia spear;
- warfork;
- pitchfork;
- hooked blade.

### Military

- boar spear;
- spetum;
- billhook;
- pike + four heraldic pike variants;
- swordlance.

### Noble

- halberd.

### Direction

The three MO tiers should not survive as
“basic / military / noble polearms.”

Japanization should instead curate a Japanese long-weapon family:

- spear roles -> `槍` / long-spear roles;
- suitable bladed-polearm roles -> `薙刀` or related long-blade families where
  stats and animation fit;
- suitable long-blade-on-pole role -> `長巻` only if the weapon behavior fits;
- selected fork/hook agricultural tools may remain tools rather than military
  prestige progression;
- heraldic pike variants should be consolidated or hidden unless they provide
  non-cosmetic value;
- halberd/spetum/billhook must not each receive an invented Japanese equivalent
  merely to preserve every Def.

Historical evidence supports naginata use before and through the medieval
period and spear prominence in late medieval warfare, but final one-to-one
mapping must follow the MO weapon stats.

---

## 7. Maces, hammers and picks

MO outputs:

### Basic

- bludgeon;
- goedendag;
- two-handed mace;
- two-handed mallet.

### Military

- blacksmith hammer;
- pickaxe;
- military pick;
- two-handed hammer;
- polehammer;
- nomad mace;
- morning star;
- winged mace.

### Noble

- warhammer;
- two-handed flanged mace.

### Direction

This is a **curation branch**, not a translation branch.

- Keep culture-neutral work tools where their dual combat role still makes sense.
- Retain only a small number of dedicated blunt-weapon performance niches when
  a Japanese counterpart is historically defensible.
- Do not invent Japanese “morning star,” “winged mace,” “goedendag,” etc.
- If several Western Defs collapse onto the same Japanese gameplay concept,
  choose the best stat/material slot and hide the redundant ones.
- Rename/remove the “noble” tier.

Exact kanabō/tetsubō mappings are intentionally **not fixed yet**; stronger
historical sourcing and stat/graphic comparison are required first.

---

## 8. Blades and axes

### `DankPyon_BasicBlades`

- butcher's cleaver;
- hatchet;
- woodcutter's axe;
- falchion.

### `DankPyon_MilitaryBlades`

- handaxe;
- bardiche;
- longaxe;
- longsword.

### Vanilla `LongBlades` additionally gates MO

- fencing sword;
- fighting axe;
- greataxe;
- greatsword.

### Direction

Split **tools/axes** from **swordcraft** conceptually.

Tool-side candidates:

- cleaver / hatchet / wood axe -> Japanese utility chopping/cleaving roles such
  as `鉈` / `手斧` / `斧` where stats fit;
- keep only enough axe variants to preserve meaningful tool/combat tradeoffs.

Sword-side candidates:

- use the strongest fitting MO stat slots to represent Japanese blade families
  such as `太刀`, later `打刀`, and oversized battlefield sword roles;
- do not map falchion/longsword/fencing sword/greatsword one-for-one by shape;
- Heian/Kamakura tachi and late-medieval uchigatana/large-sword forms give
  historical anchors, but exact Def allocation requires damage, cooldown,
  material and work-cost comparison.

The current European
`BasicBlades -> MilitaryBlades -> LongBlades`
ladder should be replaced by a Japanese craft/use progression, not translated.

---

## 9. Gunpowder branch

`DankPyon_Gunpowder` gates:

- gunpowder gathering recipes;
- `DankPyon_Handgonne`;
- acid flask;
- fire pot;
- flash pot;
- smoke pot.

### Direction

The research itself moves to the **late-Sengoku end of AMJ** and is detached
from `Alchemy`.

- `DankPyon_Handgonne` is a strong candidate to become a matchlock /
  `火縄銃` role **only if** its gameplay stats and animation are suitable.
- Fire/smoke projectile containers require separate historical/use audit.
- Acid/flash fantasy/chemical items should not survive simply because they are
  technically under the same upstream research.
- Gunpowder manufacture, firearm adoption and special thrown munitions may need
  separate unlock groups even if upstream uses one node.

The historical anchor is the 1543 Tanegashima introduction followed by
domestic copying and rapid Sengoku diffusion.

---

## 10. Smithing and tailoring are cross-domain nodes

The Def audit shows that broad Vanilla research nodes are not cleanly scoped.

### `Smithing` currently gates at least 22 MO Defs

Including:

- anvil, bellows, furnace, grinding wheel, quenching bucket;
- repair tools / weapon and armor mending;
- mining tools and tool rack;
- metal strongbox / royal chest;
- oil lamp;
- embedded cleaver;
- slop/ragout/fondue cooking pots;
- the MO handgonne;
- several padded Western helmets.

Therefore Japanization cannot treat `Smithing` as “metal weapons only.”
The node needs unlock redistribution by function.

### `ComplexClothing` currently reaches at least 49 MO Defs

The inherited dependency family includes:

- Western garments and under-armor;
- cloth spinner;
- apparel mending;
- many patched cloth/leather/animal/heraldic rugs.

Therefore:

- tailoring can remain a generic craft concept;
- Western garments require individual Japanization/hide decisions;
- decorative carpet/rug content should not all be retained merely because the
  parent Def inherits `ComplexClothing`;
- MO's industrial cloth spinner should not leak into the historical
  Japanization path.

This is also evidence that automated validation must inspect the **loaded final
Def graph**, not only research XML.

---

## 11. Historical anchors

These are evidence anchors for the family-level decisions, not automatic
one-to-one mappings.

- 文化遺産オンライン / 宮城県: `弩機 伊治城跡出土` — eighth-century
  practical military crossbow mechanism.
  - https://online.bunka.go.jp/heritages/detail/430282
  - https://www.pref.miyagi.jp/soshiki/bunkazai/kouko10-doki.html
- 奈良文化財研究所 / related scholarship: ancient state military crossbow
  deployment; research also distinguishes portable and installed crossbows.
  - https://repository.nabunken.go.jp/dspace/bitstream/11177/8274/1/BA62154222_2_090_114.pdf
  - https://cir.nii.ac.jp/crid/1520853832330876416
- e-Museum: 15th-century Muromachi `胴丸`, demonstrating sophisticated
  Japanese composite armor well before the late plate-heavy branch.
  - https://emuseum.nich.go.jp/detail?content_base_id=100513
- e-Museum: 16th-century `南蛮胴具足` and Japanese manufacture influenced by
  imported European cuirasses, useful as a late-period endpoint rather than a
  generic European plate ladder.
  - https://emuseum.nich.go.jp/detail?content_base_id=100509
- 文化遺産オンライン: Kamakura tachi and later Japanese sword examples.
  - https://bunka.nii.ac.jp/heritages/detail/192513
  - https://bunka.nii.ac.jp/heritages/detail/178082
- ColBase: 16th-century Muromachi `打刀` mounting.
  - https://colbase.nich.go.jp/collection_items/tnm/F-15807
- MLIT Kyushu: 1543 firearm introduction at Tanegashima and subsequent
  domestic copying/spread.
  - https://www.qsr.mlit.go.jp/suishin/story2019/03_8.html

---

## 12. Implementation consequences

Before production XML or texture work:

1. Generate a machine-readable **research -> final loaded Def** ledger for the
   audited MO version.
2. For each retained MO weapon/apparel Def, record:
   - Japanese referent;
   - historical band;
   - label/description action;
   - texPath replacement;
   - research replacement;
   - whether material/recipe changes are required.
3. For each hidden Def, ensure:
   - no visible recipe still produces it;
   - no faction/loadout requires it without fallback;
   - no visible research is blocked by its hidden node;
   - external MO-compatibility mods fail gracefully.
4. Do not delete upstream Defs merely to clean the Architect/research UI.
5. Validate faction pawn kinds and traders after armor/weapon hiding: MO factions
   may explicitly request the Western items Japanization intends to hide.
6. Separate historical Japanization from balance redesign:
   keep upstream combat stats unless a stat itself prevents a truthful mapping.
7. Retexture the **complete loaded graphic-state family** of each retained target
   under `Docs/RetextureImplementationGuidelines.md`.

## Faction / PawnKind follow-up

The faction/loadout dependency audit is maintained in
[MedievalOverhaulJapanizationFactionLoadoutAudit.md](MedievalOverhaulJapanizationFactionLoadoutAudit.md).
It records hard `apparelRequired` references, weapon/apparel tags, and MO faction
presentation consequences. Military Def hiding/retexture decisions are not
implementation-ready until that loadout audit's generation gate is satisfied.

## Next audit

The next Def-level pass should cover:

- exact weapon stats/material costs to choose the surviving Japanese mappings;
- cooking/food research outputs;
- domestic/production buildings;
- DBH for Medieval research links after the MO tree is rewritten.
