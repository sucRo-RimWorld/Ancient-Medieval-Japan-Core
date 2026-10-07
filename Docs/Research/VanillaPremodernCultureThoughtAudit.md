# Vanilla Premodern Culture / Thought Audit

## Status

Initial audit for a possible standalone AMJ cultural-normalization Mod.

Working name only: **`AMJ - Premodern Culture`**.

This is **not** part of `AMJ - Medieval Overhaul Japanization`. Japanization
patches Medieval Overhaul; this audit covers Vanilla cultural assumptions that
remain even when MO is fully Japanized.

No production ThoughtDef, TraitDef, C#, XML, About metadata or dependency is
changed by this document.

## Why this audit exists

RimWorld Vanilla is written around a far-future interstellar society. Some
mood/social rules are physiological or broadly human, but others encode
specific expectations about furniture, privacy, intoxicants, rooms and social
norms.

Ancient/medieval Japan should not receive a penalty merely because it does not
imitate modern/spacer domestic life.

The design rule is therefore:

> Preserve physiological consequences; audit culturally contingent value
> judgments.

Examples:
- being dangerously hot/cold can remain unpleasant;
- sleeping on bare earth without bedding can remain unpleasant;
- using floor-level bedding or eating in a historically normal floor-seated
  arrangement should not automatically count as animal-like deprivation;
- chemical dependence remains physiological, but the social/cultural framing
  of specific drugs and alcohol may require different treatment.

## Initial verified Vanilla examples

The currently available Core XML mirror exposes several high-priority examples.
Exact RimWorld 1.6 installed-source values must be rechecked before
implementation.

### Dining

`AteWithoutTable`

- duration: 1 day
- mood: **-3**
- text explicitly frames the meal as eating “off the ground” and asks for a
  table.

This is the clearest first audit target.

The problem is not that every floor meal should be pleasant. The problem is
that “not using a RimWorld Table” is being treated as equivalent to uncivilized
ground eating. A Japaneseized system needs to distinguish:

- genuinely improvised eating directly from the ground;
- valid floor-seated dining with a tray/low table/appropriate setting;
- high-status or formal dining arrangements.

The exact implementation should prefer a positive recognition of valid
historical dining furniture/conditions over globally deleting all table-related
mood logic.

### Sleep / privacy

`SleptOnGround`

- mood: **-4**
- text describes sleeping on the ground “like an animal.”

This needs semantic separation between:
- bare-ground sleeping;
- bedding directly on the floor;
- futon/tatami or equivalent historically valid bedding.

A floor-level sleeping culture must not require a raised Western bed solely to
avoid the penalty.

`SleepDisturbed`

- mood: **-1**, stackable;
- text explicitly recommends a private room.

The disturbance itself can remain a valid gameplay cost, but “private bedroom”
should not be assumed to be the only historically normal solution. Room
sharing, partitions, screens, household status and building layout should be
audited separately.

### Temperature

`SleptInCold` and `SleptInHeat`

Both use mood penalties for thermal discomfort. Those effects are primarily
physiological and should not be deleted merely for historical flavor.

However, their descriptions directly invoke modern/spacer expectations such as
heaters and air conditioning. A culture Mod may need text replacement or a
more historically neutral description even if the numeric penalty remains.

### Drug / alcohol cultural framing

Vanilla `DrugDesire` includes:
- chemical fascination;
- chemical interest;
- teetotaler.

The descriptions frame recreational chemical consumption as a broad,
culture-neutral personality spectrum and can trigger drug binges / policy
defiance.

Vanilla also includes social evaluation of intoxication such as `Drunk`
(opinion penalty in the current source mirror).

This requires a much wider audit than simply hiding futuristic drugs:

1. **availability / Tech Level** — whether a specific drug should exist in the
   AMJ profile at all;
2. **substance class** — alcohol, medicine, tobacco/late-contact material,
   fictional psychite/stimulant/combat drug, etc.;
3. **physiology** — tolerance, addiction, withdrawal and impairment;
4. **personal disposition** — whether a trait such as DrugDesire remains useful
   and how broadly it applies;
5. **social judgment** — whether intoxication/use should produce the same
   opinion/mood effects in every period and social context.

The culture audit must not simply replace “drug-friendly spacer society” with
a blanket “medieval people disliked drugs.” Different substances and contexts
need separate treatment.

## First audit categories

### A. Dining and furniture norms

Audit:
- `AteWithoutTable`;
- Table/Chair job requirements;
- low tables, trays, floor seating and external Japanese furniture compatibility;
- comfort/recreation effects that assume chair-based dining.

Likely design goal:
- valid Japanese floor dining should count as proper dining;
- genuinely eating from the ground with no dining setup may still carry a
  penalty.

### B. Sleep and domestic space

Audit:
- `SleptOnGround`;
- bedroom/barracks impressiveness;
- sleep disturbance/private-room assumptions;
- bed/futon/tatami semantics;
- comfort scores and room ownership expectations.

Likely design goal:
- distinguish bare ground from proper floor bedding;
- do not require a Western raised bed or private room as the only civilized
  sleeping arrangement.

### C. Drugs, alcohol and intoxication

Audit:
- `DrugDesire` trait;
- social intoxication thoughts;
- drug-policy assumptions;
- all Vanilla recreational-drug availability in an AMJ + World Tech Level
  profile;
- late-Sengoku contact substances separately from ancient/medieval baseline.

Likely design goal:
- keep physiological addiction/withdrawal where the substance exists;
- stop treating all pleasurable chemicals as one timeless cultural category;
- prevent out-of-period spacer drugs from defining normal medieval social life.

### D. Room quality / privacy / furniture expectations

Audit:
- bedroom and barracks Thoughts;
- dining/rec-room impressiveness;
- chairs/tables/dressers/end tables and similar assumptions;
- whether room impressiveness should be satisfied by Japanese architectural
  features rather than Western furniture count.

This may require compatibility hooks for existing Japanese furniture Mods
rather than AMJ adding duplicate furniture.

### E. Ethics and social norms

Later-pass audit:
- prisoner sale/execution;
- organ harvesting;
- relationship/privacy norms;
- nudity/modesty;
- corpse/butchery;
- beauty/disfigurement social effects;
- slavery and status systems where relevant.

These are much more sensitive to class, religion, local custom and gameplay
abstraction than dining furniture. They should not be changed casually merely
because “medieval Japan was different.”

## Mod-boundary rule

If the implementation changes Vanilla ThoughtDef/TraitDef/Needs/social behavior
independently of Medieval Overhaul, it belongs in the separate cultural Mod
candidate rather than Japanization.

Japanization may provide **optional compatibility** so that:
- MO furniture/retextures are recognized as valid cultural furniture;
- MO alcohol/food systems feed the cultural Thought rules;
- Japanization-specific retained equipment does not accidentally reintroduce
  Vanilla spacer assumptions.

The culture Mod must remain optional. Grains, Waterworks, Rice Cultivation,
Hot Springs and other AMJ content Mods must not depend on it merely for their
core gameplay.

## Implementation caution

Many Thoughts are generated by C# workers or Jobs rather than simple XML
values. Before implementation, inventory:

- ThoughtDefs;
- ThoughtWorkers;
- JobDriver eating/sleeping checks;
- furniture/building tags used for dining/sleep satisfaction;
- TraitDefs and drug-policy logic;
- Ideology overrides when DLC is present;
- compatibility behavior with Japanese furniture Mods.

Do not patch only the visible Thought text if the triggering condition is still
wrong.

## Next step

Build a complete Vanilla 1.6 cultural-assumption ledger, starting with:
1. eating/table;
2. sleeping/bed/private-room;
3. room impressiveness/comfort;
4. drugs/alcohol;
5. recreation/furniture;
6. then social/ethical Thoughts.

For each entry classify:
- universal/physiological — keep;
- wording-only anachronism — rewrite;
- culturally contingent trigger — change condition;
- period-inappropriate content — hide/disable in the AMJ culture profile;
- DLC/Ideology-owned — leave to DLC or provide conditional compatibility.
