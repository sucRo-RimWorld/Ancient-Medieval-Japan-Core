# Medieval Overhaul Japanization Domestic / Production Audit

## Status

This document is the production, food and domestic follow-up to the 67-node
research audit for `AMJ - Medieval Overhaul Japanization`.

It records the actual MO 1.6.2.2 Def families gated by cooking, preservation,
pressing, textile, milling/power and broad domestic research. It is a design
audit, not an implementation claim.

Audited archive:

- `3219596926.zip`
- Medieval Overhaul 1.6.2.2
- SHA-256 `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`

## Core conclusion

MO research nodes are often **content bundles**, not coherent historical
technologies. Japanization therefore cannot preserve the upstream research
tree and only rename its labels.

Examples from the loaded XML:

- `DankPyon_Presser` mixes apple juice, cheese and paper pressing;
- `Pemmican` / MO “food preservation” mixes drying racks with packaged
  rations;
- `DankPyon_IntermediateCooking` is dominated by Western pies/cakes/quiche,
  grilled cheese and similar named dishes;
- `DankPyon_Oven` gates bread together with multiple pies/cakes;
- `Smithing` also unlocks cooking pots, lamps, furniture and padded helmets;
- `DankPyon_RusticFurniture` reaches well over one hundred Defs across
  furniture, production, decoration and other domains;
- `Stonecutting` reaches castle walls and many fleur-de-lys / Versailles /
  other Western floor patterns in addition to genuinely generic stoneworking.

Japanization must therefore curate **unlock outputs**, not only research
prerequisites.

---

## 1. Cooking tiers

### Basic Cooking — 12 directly gated recipes

MO directly gates:

- fried eggs;
- mashed potatoes;
- pumpkin fritters;
- sausage;
- spice;
- tallow;
- bulk versions of the above.

### First-pass treatment

Do not preserve “Basic Cooking” as a package of these exact Western recipes.

- generic egg cooking can remain if its gameplay role is useful;
- generic animal-fat rendering / tallow can remain as a material process where
  it serves other MO systems;
- sausage should not be renamed into a Japanese preserved food merely to retain
  the Def;
- potato/pumpkin recipes depend on crop/content history and should be evaluated
  independently;
- spice manufacture should be separated from “basic cooking” if it represents
  a material/process rather than a meal tier.

### Intermediate Cooking — 27 directly gated recipes

The node includes:

- apple pie;
- bread soup;
- carrot cake;
- grilled cheese;
- hunter's stew;
- lemon cake;
- pumpkin pie;
- pumpkin soup;
- quiche;
- sweet pancakes;
- tomato omelette;
- bulk variants.

### First-pass treatment

**Do not Japanize this node by translating the dish names.**

Most of the node is a Western recipe bundle. Retain individual recipes only
when all of the following are true:

1. its ingredient structure can truthfully represent a Japanese dish or generic
   cooking method;
2. its equipment/process remains appropriate;
3. it provides a distinct gameplay choice under AMJ's recipe-count policy.

Otherwise hide the recipe from the standard Japanization profile while keeping
the upstream Def for compatibility.

### Advanced Cooking — 9 directly gated recipes

- cheese soup;
- griffon-berry pie;
- Rox steak;
- steak with wine;
- bulk variants.

### First-pass treatment

This is **not a reusable Japanese “advanced cuisine” tier**.

- fantasy griffon/Rox dishes belong with the fantasy-content audit;
- cheese/wine dishes should not be repainted as Japanese cuisine;
- the node can be removed from the visible historical progression if no
  retained recipes justify it.

AMJ's existing design principle remains: special recipes should survive because
their materials/process/effects create a distinct gameplay decision, not
because a named historical dish list is large.

---

## 2. Grill / pot / oven / smoker

### Grill

`DankPyon_Grill` gates five recipes:

- grilled cheese bulk;
- grilled sausages;
- grilled skewers;
- bulk variants.

**Direction:** preserve the **direct-fire cooking role**, not the Western recipe
bundle. The equipment can be Japanized toward an appropriate hearth/grilling
implementation if its footprint/behavior fits. Western cheese/sausage recipes
are curated separately.

### Stew Pot

`DankPyon_StewPot` reaches 17 Defs:

- boiled lentils/onion;
- bone soup;
- hunter's stew;
- mushroom soup;
- pumpkin soup;
- vegetable pot;
- winter lentil soup;
- slop / fondue / ragout pots;
- bulk versions.

**Direction:** the underlying **pot cooking** role is highly reusable. Keep a
generic pot-cooking branch, retexture/relabel the MO equipment, and curate the
recipes individually. Do not preserve “fondue pot” merely as a Japanese pot
name.

National Museum of Japanese History material notes that the spread of iron
pots and mortars materially changed medieval daily cooking. This supports a
meaningful pot/utensil progression without requiring MO's Western stew names.

### Oven

`DankPyon_Oven` gates 25 Defs:

- bread recipes;
- apple/carrot/lemon/pumpkin/griffon pies and cakes;
- quiche;
- rustic and large stone ovens;
- optional VFE Medieval sweetroll bulk recipes.

**Direction:** remove the oven from the **core ancient/medieval Japanese daily
cooking line**.

Bread and European/Nanban baked goods entered Japan in the 16th century through
Portuguese contact, near the end of AMJ's scope. Therefore:

- an oven may be retained only as a **late-Sengoku / Nanban optional branch**
  if its gameplay value justifies it;
- it must not remain an early or generic prerequisite for Japanese flour food;
- Grains' own minimal flour-food loop must not depend on this MO oven;
- pies/cakes/quiche are not automatically preserved merely because the oven
  survives.

### Smoker

The MO smoker is a Processor Framework building gated by
`DankPyon_Smoker` + `DankPyon_RusticFurniture` and processes smoked meat;
optional compatibility adds smoked fish.

**Direction:** keep as a **candidate generic preservation technique**, but do
not make it part of Japanization merely because MO has it.

Before final retention:

- compare with Food Drying, which AMJ already prefers for generic drying;
- confirm smoking adds a distinct preservation/processing choice rather than
  duplicate labor;
- keep the existing PF implementation if retained; do not rewrite it in C#.

---

## 3. Food preservation / drying racks

MO repurposes Vanilla `Pemmican` as “food preservation.”

The loaded dependency family includes:

- `DankPyon_DryingRack_Small`;
- `DankPyon_DryingRack_Big`;
- packaged-ration recipes, including vegetarian variants.

### Direction

Split the concept:

- **drying racks:** strong reuse candidates; the device/process is generic and
  already useful to AMJ integrations;
- **packaged rations:** separate item/recipe audit; do not relabel a packaged
  ration as a Japanese preserved meal without matching ingredients/process;
- **Pemmican DefName:** upstream identifier may remain internally, but the
  public research meaning should no longer imply that Japanese preservation
  derives from pemmican.

This also keeps Rice Cultivation's optional drying use and Food Drying
compatibility conceptually separate from generic ration production.

---

## 4. Brewing

Vanilla `Brewing`, as modified by MO, reaches at least:

- ale;
- cider;
- mead;
- grape wine;
- mulberry/ice/griffon wines;
- wort / must / apple-juice fermentation recipes.

### Direction

Do **not** rename the MO Western alcohol family into sake.

AMJ Brewing/Sake is an independent gameplay Mod because Japanese brewing has
its own raw materials and processing design.

For Japanization:

- standard historical profile may hide the Western alcohol production branch
  or leave only content that is independently justified;
- Japanization + future AMJ Brewing may connect the MO research UI/material
  ecosystem conditionally, but Japanization must not absorb Brewing;
- a late-Sengoku foreign/Nanban alcohol branch is possible only if there is
  enough independent gameplay value; it is not required for baseline AMJ.

---

## 5. Presser

`DankPyon_Presser` is a particularly mixed node.

The dependency audit finds:

- apple juice / apple-mince processing;
- cheese / goat cheese / sheep cheese;
- paper pressing;
- the actual `DankPyon_Presser` building (“cheese press”).

### Direction

The upstream node should be **split conceptually by output**.

- **paper pressing:** retain/reconnect under papermaking if the MO Paper/Paper
  Press chain is reused;
- **fruit pressing:** retain only if a historically/gameplay-relevant Japanese
  fruit/liquid chain uses it;
- **cheese pressing:** do not keep as a baseline Japanese technology merely to
  justify the building;
- **building visual/name:** if retained for paper/oil/other pressing, retexture
  and relabel as a generic press rather than a cheese press.

Japanization may reuse the mechanical processor, but output ownership remains
with the relevant content system.

---

## 6. Milling and agriculture research

### Basic Agriculture

Directly gates:

- `DankPyon_GardeningBox`;
- `DankPyon_Millstone`.

### Intermediate Agriculture

Directly gates:

- `DankPyon_Post`.

### Advanced Agriculture

No direct loaded Def was found by the current dependency extraction.

### Plowed Soil

Directly gates:

- `DankPyon_PlowedSoil`.

### Direction

This confirms that MO's Basic / Intermediate / Advanced labels are poor
proxies for a Japanese historical agriculture ladder.

Japanization should:

- preserve the millstone function as a reusable processing tool;
- move/rename the research according to actual technique rather than “basic
  agriculture”;
- keep plowed soil early unless its mechanical bonus requires a later balance
  gate;
- audit `GardeningBox` and `Post` by actual function before retaining;
- remove empty/meaningless tier nodes if their only value disappears after
  output redistribution.

Grains / Rice Cultivation remain owners of their crops and primary processing.
Japanization only connects retained MO equipment/research.

---

## 7. Textile spinning

`DankPyon_TextileSpinning` gates:

- cotton -> cloth recipes;
- wool -> cloth recipes;
- flax -> linen recipes;
- bulk versions;
- `DankPyon_SpinningWheel`.

### Direction

The **fiber-processing function** is reusable; the MO Western spinning-wheel
presentation is not the default Japanese reference.

- move the concept toward early hand spinning / spindle technology;
- retexture/rename the equipment if the same processor behavior can represent
  an appropriate Japanese-period tool;
- audit cotton, flax/linen and wool separately for Japanese historical fit and
  external content ownership;
- do not add extra processing stages solely to make the Japanese version look
  more detailed than MO.

`DankPyon_Silk` currently directly gates only a silk bed in this extraction,
which is evidence that the research node is not a coherent sericulture/silk
technology package. Silk production/history needs a separate output audit
rather than retaining the node unchanged.

---

## 8. Candle making and lighting

`DankPyon_CandleMaking` directly gates:

- beeswax candle;
- candles;
- candle stand;
- candelabra.

### Direction

Candles can exist in earlier periods through imports/elite/religious use, but
routine domestic production in Japan is a later question. Existing research
evidence places domestic candle manufacture by the late Muromachi period.

Therefore:

- if retained, place candle manufacture in a later medieval branch;
- do not make candles the default early Japanese lighting technology;
- MO oil-lamp content should be separately audited as a potentially stronger
  general lighting basis;
- retexture candelabra/stands when the Western form is visually unsuitable.

---

## 9. Windmill and watermill

Direct dependencies are simple:

- `DankPyon_Windmill` -> `DankPyon_WindMill`;
- `DankPyon_Watermill` -> `DankPyon_WaterMill`.

### Direction

- **watermill:** strong retain/retexture candidate and should be moved much
  earlier than MO's Engineering end branch;
- **power windmill:** hide from the baseline Japanization research tree unless
  better premodern Japanese evidence is established;
- **DBH for Medieval:** its wind pump currently connects to the MO windmill
  research, so Japanization must re-route that DBH unlock if the windmill node
  is hidden.

This decision concerns power machinery, not decorative wind devices.

---

## 10. Broad overloaded research nodes

### Rustic Furniture

The dependency crawler reaches **131 MO Defs** through
`DankPyon_RusticFurniture`, including furniture, beds, shelves, tents,
lighting, decoration, bookshelves, production/support furniture and other
objects.

This is not a single historical “technology.”

**Direction:** keep the upstream node only as an internal compatibility anchor
if useful, while Japanization redistributes visible unlocks by actual craft /
domestic function. Do not force every retained Japaneseized object behind one
“rustic furniture” research merely because MO did.

### Stonecutting

The crawler reaches **68 MO Defs**, including:

- generic stone/cobble floors;
- kiln and ice cellar;
- castle wall / embrasures;
- Tudor wall;
- many fleur-de-lys, Versailles, herringbone and other Western decorative
  floors;
- reinforced trench;
- large oven;
- storage/display piles.

**Direction:** preserve generic stoneworking, but curate the Western
architecture/decorative outputs separately.

A Japanization patch must not equate:

> “stone can be cut” = “European castle wall, Tudor wall and fleur-de-lys floors
> are now Japanese.”

### Complex Furniture

The current direct family includes colored rustic beds and a reinforced log
gate. Treat this as an output bundle, not a technology that needs literal
translation.

---

## 11. Historical anchors

- National Museum of Japanese History: medieval cooking change associated with
  the spread of iron pots and mortars; the same material also notes the
  15th-century arrival of the large saw and plane changes in woodworking.
  - https://www.rekihaku.ac.jp/assets/upload/column_20210724_pdf_01.pdf
- National Diet Library reference: Portuguese-derived bread entered Japan in
  the Tenbun period; another NDL reference on Nanban confectionery places
  Portuguese breads/sweets in the 16th-century contact context.
  - https://crd.ndl.go.jp/reference/entry/reference/show?id=1000034821
  - https://crd.ndl.go.jp/reference/entry/reference/show?id=1000077165
- Existing research-audit anchors remain applicable for watermills, candles and
  oil production:
  - watermill: `日本書紀` traditional 610 transmission / Heian-period use;
  - domestic candle production: late Muromachi;
  - egoma-oil production/trade: medieval oil guilds.

These anchors justify structural placement only. They do not automatically
validate a specific MO recipe as a Japanese historical food.

---

## 12. Ownership boundary

### Japanization owns

- curation of MO recipes/buildings exposed in the Japanized MO profile;
- MO research prerequisite redistribution;
- MO-owned retextures/labels/descriptions;
- hiding Western/fantasy MO recipes where no honest mapping exists;
- conditional research/material connections to other AMJ Mods.

### Other AMJ Mods keep ownership of their gameplay loops

- **Grains:** dry-field grain crops, primary processing and minimal flour foods;
- **Rice Cultivation:** rice/paddies and rice primary processing;
- **Fermentation / Brewing:** Japanese fermentation and alcohol systems;
- **Preservation / Food Drying compatibility:** independent preservation
  gameplay where adopted;
- **Ironmaking:** Japanese iron production;
- **Waterworks:** gravity-fed water-management network.

Japanization may reuse MO equipment for these systems when both Mods are
loaded, but it must not turn their independent gameplay into a Japanization hard
dependency.

## Next audit

Before production XML:

1. build the exact MO cooking RecipeDef -> product -> ingredient -> effect
   ledger;
2. determine which recipes remain because they create a distinct AMJ gameplay
   choice;
3. audit architecture/furniture output bundles, especially
   `RusticFurniture`, `Stonecutting` and royal furniture;
4. audit MO oil lamps and other lighting before fixing the candle progression;
5. trace Processor Framework processes behind presser, drying rack, smoker,
   millstone and watermill;
6. validate optional Grains / DBH for Medieval / future Fermentation/Brewing
   connections remain conditional.


---

## 13. Exact cooking RecipeDef / effect follow-up

The MO 1.6.2.2 XML was re-audited at exact RecipeDef level for the cooking
research/equipment surface. The important result is that Japanization must
curate **mechanical effects as well as names, ingredients and graphics**.

### Exact recipe counts in the loaded snapshot

- `DankPyon_BasicCooking`: **12 RecipeDefs**
- `DankPyon_IntermediateCooking`: **27 RecipeDefs**
- `DankPyon_AdvancedCooking`: **9 RecipeDefs**
- `DankPyon_Grill`: **5 RecipeDefs**
- `DankPyon_StewPot`: **14 RecipeDefs**
- `DankPyon_Oven`: **23 RecipeDefs** in the current loaded XML surface,
  including optional VFE Medieval sweetroll bulk recipes; several recipes are
  counted under both a cooking tier and an equipment prerequisite

### Ingredient/output facts that matter for curation

Basic Cooking is not a coherent Japanese “basic cuisine” tier. It contains:

- fat + salt -> tallow;
- raw herb -> spice;
- raw meat + spice -> sausage;
- eggs -> fried eggs;
- potato + milk -> mashed potatoes;
- pumpkin + flour -> pumpkin fritters.

Intermediate Cooking is predominantly a Western/post-contact bundle:

- bread soup;
- apple pie;
- lemon cake;
- hunter's stew based on sausage/cabbage/onion/garlic;
- grilled cheese;
- quiche;
- sweet pancakes;
- tomato omelette;
- pumpkin soup/pie;
- carrot cake.

Advanced Cooking is even less reusable as a baseline Japanese tier:

- cheese soup using ale;
- steak with wine;
- Rox steak using ale;
- griffon-berry pie.

The reusable equipment paths are much narrower than the research labels:

- **Stew pot:** bone soup, lentil soup, mushroom soup, generic vegetable pot,
  lentil/onion dish, hunter's stew, pumpkin soup.
- **Grill:** grilled sausage, grilled skewers, grilled cheese.
- **Oven:** bread plus Western pies/cakes/quiche and optional sweetrolls.

This reinforces the existing rule: preserve a process/equipment Def when it has
a valid Japanese gameplay role, but curate its recipes individually.

### MO food effects are not cosmetic

Many MO meals apply `IngestionOutcomeDoer_GiveHediff` and therefore have
significant temporary stat/capacity effects. Representative loaded values:

- `DankPyon_AteFriedEggs`: WorkSpeedGlobal **+5%** plus small
  Consciousness/Moving/Manipulation offsets, about 12 hours;
- `DankPyon_AteMashedPotatoes`: hunger-rate offset **-15%** plus small
  capacity offsets, about 12 hours;
- `DankPyon_AteGrill`: WorkSpeedGlobal **+5%**;
- `DankPyon_AteGrillFine`: WorkSpeedGlobal **+10%**;
- `DankPyon_AteGrillLavish`: WorkSpeedGlobal **+20%**;
- `DankPyon_AteSoup`: ImmunityGainSpeedFactor **+5%**, about 24 hours;
- `DankPyon_AteSoupFine`: ImmunityGainSpeedFactor **+10%**;
- `DankPyon_AteSoupLavish`: ImmunityGainSpeedFactor **+20%**;
- `DankPyon_AteSweetPancakes`: WorkSpeedGlobal **+15%** plus movement /
  manipulation offsets;
- `DankPyon_AteSteakWithWine`: WorkSpeedGlobal **+20%**;
- `DankPyon_AteRoxSteak` and `DankPyon_AteGriffonBerryPie`: WorkSpeedGlobal
  **+20%**, ImmunityGainSpeedFactor **+40%**, and multiple large capacity /
  physiological offsets.

Therefore a retained MO RecipeDef must pass four separate checks:

1. historically/semantically valid ingredients and cooking method;
2. equipment and research placement;
3. nutrition/market-value and labor balance;
4. **Hediff / Thought effect balance** against AMJ's existing rule that cooking
   buffs are justified by total material/work/research cost, not by recipe tier
   alone.

Do not keep a strong MO buff merely because the underlying Def was convenient
to retexture. Conversely, the MO effect system is useful prior art for AMJ's
own limited special-food buffs and may be reused where the cost/role still
matches.

### First-pass recipe-family disposition

- **Strong retain candidates:** generic grilled skewers; generic mushroom /
  vegetable pot; bone soup if the bone-resource loop remains useful; direct-fire
  cooking and pot-cooking equipment.
- **Retain only after ingredient/content-owner audit:** fried eggs, spice,
  rendered fat/tallow, pumpkin dishes, bread.
- **Hide from baseline or late-Nanban-only candidates:** bread-soup as a
  European bread derivative, pies, cakes, quiche, grilled cheese, cheese soup,
  steak with wine.
- **Hide from the historical baseline:** Rox and griffon-berry dishes.
- **Do not relabel into Japanese food:** sausage, cheese/wine dishes and
  Western pastries are not acceptable one-to-one targets merely because their
  stats are useful.

Bulk RecipeDefs follow the disposition of their single-batch counterpart; they
do not need independent historical justification.

---

## 14. Architecture / furniture output curation follow-up

The direct research gates confirm that the broad furniture nodes should be
split by actual object role rather than translated wholesale.

### `DankPyon_RusticFurniture` direct outputs

The current direct-gate set includes:

- cooking tools;
- baking tools;
- rustic door, gate and slab door;
- ice chest;
- cup-and-dice table;
- tarocco table;
- `Rim of War` game table;
- lamp post and oil lamp;
- rustic hearth;
- market tent/stall;
- water barrel;
- tavern sign;
- lectern;
- rustic oven;
- stew pot;
- apiary;
- mending bench;
- smoker;
- ice-block mold.

First-pass curation:

- **retain/retexture:** generic doors/gates, oil lamp, hearth, market stall,
  water container, stew pot, mending bench;
- **strong reinterpret candidate:** a generic board-game table can use a
  historically valid Japanese game such as go rather than preserving a
  Western fantasy-board presentation; go is well attested in Japan long before
  and throughout the medieval period;
- **late/conditional:** baking tools/oven;
- **hide or separate audit:** tarocco, tavern-specific signage, ice-block mold,
  smoker, apiary and any object whose actual mechanic cannot honestly map to a
  Japanese referent;
- **ice storage:** audit for `氷室`-type reinterpretation rather than assuming
  a Western ice chest is the correct visible object.

### `Stonecutting` direct outputs

Directly gated objects include:

- Tudor wall;
- castle wall;
- reinforced trench;
- ice cellar;
- large oven;
- kiln.

First-pass curation:

- **kiln:** retain/retexture; this is a strong generic craft/infrastructure
  reuse target;
- **reinforced trench:** retain only if the loaded behavior can represent
  Japanese field earthworks/defensive ditching without Western fortification
  semantics;
- **ice cellar:** strong reinterpret candidate as a Japanese ice-storage
  facility if the mechanic fits;
- **large oven:** late Nanban/conditional at most;
- **Tudor wall:** never keep under a translated name; either retexture/redefine
  it as a historically supportable Japanese wall construction with matching
  stats or hide it;
- **castle wall:** do not automatically call a freestanding European-style
  heavy wall `石垣`. Japanese castle stone bases and a RimWorld vertical wall
  are not mechanically/visually identical; item-level architecture audit is
  still required.

### `DankPyon_RoyalRusticFurniture` direct outputs

Directly gates royal closet/bookshelf/armchair/throne/tables/end table/dresser,
royal Tudor bed and royal chest.

This set should **not** be retained as a one-for-one “Japanese royal furniture”
pack.

- chests/storage and some tables/bookshelves may have valid high-status
  Japanese counterparts;
- armchair, throne, end-table, dresser and Tudor-bed forms require much more
  caution because elite Japanese interiors used a different floor-seating /
  furnishing system;
- where no honest counterpart exists, hide the MO object rather than creating a
  misleading Japanese skin;
- if a retained function maps cleanly, retexture the existing MO Def rather
  than adding a duplicate AMJ Def.

Culture Agency material on tatami notes that it began as elite movable
seat/bedding and spread to room-wide use around the Muromachi period. This
supports a Japanization strategy based on floor-level furnishings rather than
simply reskinning every Western high-status chair/bed.

### `ComplexFurniture` direct outputs

The current direct set is small:

- reinforced log gate;
- red rustic single bed;
- red rustic double bed.

The reinforced gate is a straightforward retain/retexture candidate. Beds
should be audited against Japanese bedding presentation; a retexture is
possible if the footprint/interaction remains honest, but Japanization should
not create redundant bedding Defs when an external Japanese furniture Mod is
already the chosen supplier.

---

## Updated next audit

Before production XML:

1. classify the remaining unresolved food/product effects and write the
   retained-recipe list;
2. trace Processor Framework processes behind presser, drying rack, smoker,
   millstone and watermill;
3. finish lighting: MO oil lamps versus candle progression;
4. finish furniture/architecture object-level mapping, especially Tudor/castle
   walls, royal furniture, ice storage, games and market/tavern assets;
5. validate optional Grains / DBH for Medieval / future Fermentation/Brewing
   connections remain conditional;
6. add automated static ledgers so an MO update cannot silently add Western
   recipes/furniture behind a retained Japanization research node.


---

## 15. Processor Framework process tracing

The current MO processors were traced at ProcessDef + building level.

### Presser / paper press

The generic `DankPyon_Presser` is visually/verbally a cheese press and embeds
four PF processes directly:

- cow-milk cheese;
- goat cheese;
- sheep cheese;
- apple pressing.

Paper is **not** merely another process on the same building. MO has a separate
`DankPyon_Press_Paper` building with its own
`DankPyon_Press_PaperProcess`, converting paper mixture to paper over one
game day.

Implication:

- do not keep the cheese-press building just because papermaking is useful;
- Japanization can retain/retexture the dedicated paper press independently;
- cheese/apple pressing remain separate content decisions;
- if a future AMJ oil/fruit process wants a press, its owning Mod may reuse a
  compatible MO processor conditionally, but Japanization does not invent that
  gameplay loop.

### Drying racks

MO drying racks run Processor Framework processes for:

- ordinary dried meat;
- human meat;
- insect meat;
- optional fish integrations.

The normal meat process is weather-sensitive:

- 2.5 game days;
- 0.8 base efficiency;
- faster with more sun/wind;
- rain and snow can reduce progress to zero;
- output efficiency can scale from ingredient Nutrition.

This is a strong reusable **generic preservation mechanic**. The equipment and
process behavior are more reusable than MO's packaged-ration research bundle.

Japanization should therefore keep drying-rack compatibility available while
curating the actual accepted ingredients/outputs by profile. Rice Cultivation
or other AMJ Mods may add their own conditional PF processes without becoming
Japanization dependencies.

### Smoker

The smoker embeds three baseline PF processes:

- ordinary smoked meat;
- smoked human meat;
- smoked insect meat;

plus optional fish compatibility.

The normal process:

- takes 1 game day;
- requires fuel;
- uses a hot ideal temperature range;
- is affected by rain/snow;
- outputs a dedicated smoked-meat item.

The loaded `efficiency` is **0.10**, unlike the drying rack's 0.8, so this is
not mechanically interchangeable with generic drying. Before retention, audit
the actual input/output nutrition and spoilage values to determine whether the
smoker creates a meaningful high-loss/fast-preservation tradeoff or is simply
an upstream balance artifact.

Do not retain human/insect smoked-meat outputs as a historical-Japan feature;
those remain normal RimWorld content-policy/gameplay choices and should not
drive the Japanization technology tree.

### Millstone

`DankPyon_Millstone` is **not** a PF processor. It is a normal
`Building_WorkTable` with Bills, unlocked by MO Basic Agriculture.

This is advantageous for AMJ:

- Grains can continue to own its own Base milling recipes;
- MO-loaded profiles can map compatible recipes to the MO millstone without
  importing Processor Framework semantics;
- Japanization only needs to reposition/relabel/retexture the MO equipment and
  manage research visibility.

### Watermill

The MO watermill directly embeds two PF processes:

1. `DankPyon_WaterMillProcess`
   - any `DankPyon_Cereal` -> `DankPyon_Flour`;
   - 0.25 game day;
   - efficiency 1.0;
   - bonus Hay output;
2. `DankPyon_WaterLumberMillProcess`
   - MO raw-wood category -> `WoodLog`;
   - 0.25 game day;
   - efficiency 2.0.

Thus MO's “watermill” is actually a combined **grain mill + sawmill**.

Japanization should not automatically preserve that combined scope merely
because water power itself is historically valid in Japan.

First-pass direction:

- retain the water-powered building and water-placement mechanics as a strong
  reuse candidate;
- evaluate grain milling and wood sawing as independent process toggles;
- Grains may connect its grain categories/recipes conditionally;
- woodworking/sawing must be checked against Japanese tool chronology and
  balance before the 2x raw-wood conversion is retained;
- do not make Waterworks a requirement for the MO watermill. If later
  interoperability is valuable, add it as an optional boundary.

### Windmill

The MO windmill embeds the same conceptual dual role—automated grinding and
sawing—but uses MO windmill-specific placement/airflow logic.

Since the power windmill itself is outside the baseline Japanization
technology path, its processor convenience is **not** a reason to keep the
building visible. DBH for Medieval unlocks that currently depend on
`DankPyon_Windmill` need an alternative research connection.

---

## 16. Lighting follow-up

MO already contains several lighting families before candle research:

- rustic torch lamp;
- wall oil lamp;
- lamp post;
- rustic oil lamp.

Candle research separately gates candle/candle-stand/candelabra families.

This means Japanization does **not** need candles merely to preserve a
pre-electric lighting progression.

First-pass direction:

- use oil/torch lighting as the baseline premodern branch where the loaded
  mechanics and fuel inputs fit;
- retexture clearly Western lamp-post/wall fixtures to historically supportable
  Japanese forms only when the same placement/behavior remains honest;
- keep candle manufacture as a later-medieval optional branch rather than a
  basic-lighting prerequisite;
- candelabra and other strongly Western forms should be hidden or independently
  mapped, not translated wholesale;
- do not automatically turn every oil lamp into an andon: paper-framed andon
  form, fuel, freestanding/wall placement and light behavior must match before
  that label/graphic is used.

---

## Revised next audit

Before production XML:

1. inspect smoker input/output nutrition, spoilage and value to decide whether
   its fast/high-loss tradeoff is worth keeping;
2. audit the exact watermill lumber process against woodworking chronology and
   AMJ resource balance;
3. finish object-level lighting mapping;
4. finish furniture/architecture object mapping and retained-output lists;
5. compare weapon stats/material costs before final MO Def -> Japanese weapon
   mappings;
6. resolve Carrier Birds, Heavy Crossbow, Tar, Smoker and Carpet Making;
7. create static update ledgers so upstream MO changes cannot silently re-open
   hidden Western/fantasy outputs.
