# Medieval Overhaul Japanization Faction / Loadout Audit

## Status

This document is the faction and PawnKind follow-up to:

- `MedievalOverhaulJapanizationResearchAudit.md`
- `MedievalOverhaulJapanizationMilitaryMapping.md`

It records why military Japanization cannot stop at research and ThingDef
visibility. Medieval Overhaul 1.6.2.2 directly selects Western weapons and
apparel through PawnKind `weaponTags`, `apparelTags`, and
`apparelRequired`.

This is a design audit, not an implementation claim.

Audited archive:

- `3219596926.zip`
- MO 1.6.2.2
- SHA-256 `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`

## Core conclusion

**Japanization must patch MO PawnKinds/loadouts together with the weapon and
armor research/Def changes.**

Hiding a Western item from player production is insufficient when a PawnKind
still:

- requires that exact Def through `apparelRequired`;
- selects it through an apparel/weapon tag;
- belongs to an MO faction whose role/name is explicitly Western or fantasy.

The compatibility-safe approach is:

1. keep upstream ThingDefs where practical;
2. decide which Defs remain visible/usable under Japanization;
3. patch MO PawnKinds to select only the retained Japanese-mapped equipment;
4. patch exact `apparelRequired` references that point to hidden/repurposed
   Western equipment;
5. validate every affected pawn kind can still generate legal gear;
6. then patch faction-facing names/presentation as needed.

## 1. Exact required-item dependencies

Representative hard requirements in the 1.6.2.2 PawnKind XML include:

### Player / scenario pawn kinds

- `DankPyon_HedgeKnight`
  - requires `DankPyon_Footwear_BootsPlate`
  - requires `DankPyon_Handwear_GlovesPlate`
  - uses `DankPyon_Longsword` weapon tag
  - uses hedge-knight apparel tags
- `DankPyon_PlayerMercenary`
  - selects arming sword, morning star, military pick, handaxe, falchion,
    boar spear, billhook, polehammer and longsword tags
  - uses mercenary/heavy-mercenary apparel tags

### Settlement / noble-house pawn kinds

- `DankPyon_SettlementArcher`
  - uses crossbow weapon tag
  - requires quiver and chain-kettle helmet
- `DankPyon_SettlementFootman`
  - uses billhook / polehammer / pike tags
  - requires a closed chain flat-top helmet
- `DankPyon_SettlementKnight`
  - uses morning-star / arming-sword tags
  - requires full plate
- `DankPyon_SettlementLord`
  - selects named greatsword/flanged-mace/greataxe/two-handed-hammer roles
  - requires Zweihander helmet and Zweihander cuirass
- Amboise / Soren / Oswin / Hesse variants
  - directly require heraldic hauberks, heraldic great helms and heater shields.

### General medieval pawn kinds

- `DankPyon_Medieval_Arbalester`
  - uses crossbow and arbalest weapon tags
- `DankPyon_Zweihander`
  - uses greatsword
  - requires full plate + plate boots + plate gloves
- `DankPyon_Medieval_Knight`
  - uses greatsword / two-handed hammer
  - requires full plate + plate boots + plate gloves
- `DankPyon_Medieval_Lord`
  - requires gilded armet + gilded full plate + plate boots/gloves
- `DankPyon_BrigandLeader`
  - selects noble sword, warhammer, arming sword, two-handed hammer,
    greatsword and named greataxe
  - requires splinted boots/gloves.

### Ulrik faction pawn kinds

- `DankPyon_Ulrik_Initiate`
  - requires adorned mail and splinted hand/foot protection
- `DankPyon_Ulrik_Warrior`
  - requires adorned warrior armor and adorned chain headgear
- `DankPyon_Ulrik_Oathbound` / `DankPyon_Ulrik_Lord`
  - require adorned heavy plate, adorned great helm, plate boots/gloves.

### Cultist pawn kinds

Cultist tiers directly require several Western garment/armor Defs and use
hunting-bow/crossbow/arbalest or generic medieval melee tags.

## 2. Weapon-tag dependencies

The XML relies heavily on tags rather than exact ThingDefs. Important tag
families include:

- `DankPyon_ArmingSword`
- `DankPyon_Longsword`
- `DankPyon_Greatsword`
- `DankPyon_NobleSword`
- `DankPyon_MorningStar`
- `DankPyon_Warhammer`
- `DankPyon_Polehammer`
- `DankPyon_Billhook`
- `DankPyon_Pike`
- `DankPyon_Crossbow`
- `DankPyon_Arbalest` / spelling variants used by MO
- `DankPyon_HuntingBow`
- `DankPyon_GreatBow`
- `DankPyon_Warbow`.

### Consequence

When Japanization hides or repurposes a ThingDef, it must audit whether the
Def still participates in a tag used by MO pawn generation.

Preferred options:

1. retain the Def and retexture/relabel it, so existing tag-based selection
   continues to work;
2. remove the Def from the relevant selection surface and ensure another
   retained Def still satisfies the tag;
3. patch the PawnKind to a new/retained tag.

Do not leave a PawnKind with a tag whose only eligible weapon has been hidden
or made unavailable.

## 3. Apparel-tag dependencies

MO uses role tags such as:

- peasant;
- mercenary / heavy mercenary;
- footman;
- knight;
- archer / arbalester helmet;
- brigand;
- lord;
- faction/heraldic variants.

These tags select families whose visual identity is strongly Western.

### Direction

Japanization should prefer **retaining the role tag while changing its eligible
MO apparel family** if the tag is otherwise useful. This minimizes PawnKind
rewrite.

However, when a tag's meaning itself is Western/faction-specific (for example
Zweihander or four heraldic noble-house sets), the tag can be replaced or the
PawnKind can be rewritten.

The final ledger must prove:

- every PawnKind has valid apparel for every required body/layer slot;
- no hidden fantasy/Western item remains as a hard `apparelRequired`;
- no Japanized role accidentally equips mixed Western/Japanese sets through a
  broad inherited tag.

## 4. MO faction presentation

MO 1.6.2.2 contains several faction families with different implications.

### Brigands

`DankPyon_BrigandFaction` is functionally generic banditry.

**First-pass treatment:** retain gameplay role, Japanize presentation/loadouts.

Bandits/raiders are a natural generic role for a medieval-Japan setting. The
Japanization layer can relabel/regear the existing faction without inventing a
new social system.

### Noble House

MO's noble-house content uses:

- `duke` leader title;
- OldWorlder culture;
- castle/heraldic visuals;
- knight/footman/arbalester style PawnKinds;
- Amboise/Soren/Oswin/Hesse heraldic equipment families.

**First-pass treatment:** MO gameplay may be retained, but Western feudal
presentation must not remain unchanged.

Japanization responsibility is limited to making the existing MO faction
consistent with the Japanese setting: labels/titles, MO-owned loadouts and
visuals, and any content that would otherwise expose Western knight/heraldic
gear.

**AMJ Factions remains the owner of new historical Japanese faction structure,
settlement society, temples/shrines, village communities, local powers,
traders and other new faction gameplay.** Japanization must not absorb that
project merely because it patches an MO faction.

### Player kingdom / lone adventurer / mercenary company

These scenario/player FactionDefs use labels such as “New Tavern,”
“New Lone Adventure,” and “New Mercenary Company,” OldWorlder culture, and
Western PawnKinds.

Japanization should patch their presentation/loadouts if they remain available.
Scenario ownership itself remains with the standalone AMJ Scenarios direction
where AMJ-specific starts are provided.

### Knights of Ulrik

`DankPyon_UlrikFaction` is explicitly a Western/fantasy knightly order and its
PawnKinds require adorned mail/full plate tied to Ulrik symbolism.

**First-pass treatment: hide from the standard historical Japanization
profile**, unless a later audit finds a gameplay system that cannot safely be
separated.

Do not relabel “Ulrik” into a Japanese religion or warrior order while keeping
the same religious/fantasy semantics. If its gameplay role is valuable, that
role should be reimplemented or reused only after a separate system-level
audit.

### Cultists / Shadow Sect

The faction is hidden and tied to MO hideout/raid content; its description even
warns not to deactivate it if MO hideouts are to be raided.

**First-pass treatment: compatibility audit required before suppression.**

Unlike a simple visible faction, removing it may break site/quest generation.
Japanization should first determine whether:

- it can remain hidden as an implementation faction while its pawn visuals are
  Japanized;
- the hideout system can target another compatible faction;
- the content should be disabled together as one branch.

Do not remove the FactionDef in isolation.

### Forest / witch / giant-creature factions

These are hidden animal/fantasy factions. Historical Japanization should not
automatically convert European-fantasy monsters into yōkai by relabeling them.

**First-pass treatment:** separate fantasy-content audit; default historical
profile should not depend on them.

## 5. Boundary with AMJ Factions

The responsibilities are:

### Japanization owns

- patching MO FactionDefs enough to remove overt Western/fantasy presentation
  from the retained MO gameplay;
- patching MO PawnKinds/loadouts so retained factions use the Japanized MO
  equipment set;
- suppressing MO faction/content branches that are incompatible with the
  historical profile when safe to do so;
- compatibility with MO quests/sites that depend on those FactionDefs.

### AMJ Factions owns

- new Japanese historical faction archetypes and social structure;
- Japanese settlement/role design that does not already exist as a reusable MO
  gameplay role;
- historically differentiated village, local-warrior, temple/shrine,
  outlaw/trader, etc. systems if implemented;
- new faction-specific mechanics and content.

Thus Japanization may transform an MO “noble house” presentation enough to
avoid a Western castle/knight leak, but it must not become the repository where
the complete AMJ Japanese faction system is designed.

## 6. Implementation gate

Before any military Def is hidden in production XML, an automated audit must
cover at least:

1. all MO PawnKinds and inherited PawnKind parents;
2. exact `apparelRequired` references;
3. `specificApparelRequirements`;
4. weapon/apparel tag resolution after all patches;
5. traders/rewards/loot tables that can still generate the hidden Defs;
6. FactionDefs and PawnGroupMakers;
7. scenario/player FactionDefs;
8. quests/sites that reference Ulrik, cultists, noble houses or brigands;
9. runtime generation of every retained MO combat PawnKind with ERROR 0.

The military retexture/visibility pass is incomplete until this loadout gate
passes.
