# AMJ Retexture Implementation Guidelines

This document is the shared technical source of truth for implementing retextures in Ancient & Medieval Japan (AMJ) and related modules.

It complements the ownership/design rule in `Docs/Design.md §8.5.1`. Art direction remains owned by each content repository. This document defines **how prerequisite-mod graphics are overridden, how conflicts are resolved, and what must be validated**.

## 1. Purpose

AMJ retextures are not an optional cosmetic pack layered independently from gameplay ownership. AMJ-owned Defs and Vanilla prerequisite assets normally follow gameplay/environment ownership. **Medieval Overhaul is the explicit exception:** MO-owned assets that are changed specifically to present MO as ancient-to-medieval Japan are owned centrally by `AMJ - Medieval Overhaul Japanization`, so multiple AMJ feature Mods do not compete to overwrite the same MO graphics.

The technical goals are:

- deterministic ownership;
- minimal dependence on arbitrary mod-list position;
- no duplication of gameplay Defs solely to change art;
- no unnecessary C#;
- clean optional-mod handling;
- complete coverage of graphics states actually used by the target Def;
- automated detection of missing paths, stale upstream assumptions, and competing AMJ ownership.

## 2. Prior-art audit

The following representative RimWorld retexture approaches were reviewed before fixing the AMJ implementation rule.

| Prior art | Observed approach | AMJ takeaway |
|---|---|---|
| Vanilla Textures Expanded (Workshop 2016436324; public GitHub source) | Large parts use textures at Vanilla-compatible paths. It also uses XML path replacements for states/special cases and conditional `loadFolders.xml` entries for compatibility. | Same-path replacement is simple, but the hybrid design shows that secondary states and engine-specific cases still need explicit Def patches. |
| Vanilla Textures Expanded - Variations (2493234474; public GitHub source) | Adds VE Framework random-building-graphic comps and alternate paths; conditional DLC/mod folders. | Useful precedent for conditional integration, but not suitable for AMJ's canonical fixed art because it intentionally provides selectable/random variation. |
| ReGrowth 2 (2260097569; public GitHub source) | Explicit `graphicData/texPath` and plant-state path replacement to ReGrowth-owned paths; DLC folders are conditionally loaded; optional settings can wrap retexture patches. | Strong precedent for AMJ plant/tree work: explicit unique paths and state-by-state patching are deterministic and auditable. |
| Medieval Overhaul 1.6.2.2 (3219596926; current distributed payload audited) | Mixes explicit `texPath` / full `graphicData` replacement, conditional compatibility folders, stack/multi graphics, and optional retexture settings. Some files also mix gameplay changes with visual changes because MO is an overhaul. | Use its conditional/path-handling precedent, but **do not** copy the practice of mixing unrelated gameplay balance into a pure AMJ retexture patch. |
| Clean Textures (2865361569) | Workshop description states that it contains no code and directly replaces textures with analogues bearing identical names. | Good for a generic user cosmetic pack, but AMJ should not rely on same-name shadowing for assets it formally owns. |
| Van's Retextures (representative: Melee Weapons 2922441211, Mechanitor 2943977908, Quarry 3145950235) | Narrow retexture packs tell users to place them after competing packs so their graphics win. | Simple and appropriate for user-selected cosmetic overrides; too load-order-dependent for AMJ's own canonical prerequisite-asset ownership. |
| Misc. Training Medieval Retexture (3271602770) | Loads after the original and combines retexture work with a small material patch. | Confirms that themed retextures often drift into gameplay changes; AMJ must keep those responsibilities separate. |
| Primitive Storage Retexture (3030732174) / Adaptive Primitive Storage (3400037215) | Original retexture relies on load order and some graphic-position patches; later Adaptive port uses a storage framework for stateful/fullness graphics. | Framework-driven graphics are justified for genuinely stateful storage, not for ordinary fixed AMJ retextures. |
| [CF] Better Looking Plants (3167083455) | Workshop describes it as a texture-only replacement for a small group of crops/items. | Confirms that simple same-path packs remain common; not a reason to give up deterministic AMJ ownership. |
| Plants and Mushrooms Retexture (3620131414) | Broad 1.6 plant/mushroom visual replacement. Public description does not provide enough implementation detail to use it as a technical precedent. | Useful coverage comparison only; do not infer internal mechanisms without source inspection. |

### Licensing rule

Prior-art inspection is for **implementation and compatibility design**. Do not copy third-party artwork into AMJ unless the license and project decision explicitly permit it.

In particular, public VTE/ReGrowth repositories currently use restrictive CC BY-NC-ND terms for their art; ReGrowth also explicitly prohibits reuse/modification of its assets without permission. AMJ therefore keeps independently authored replacement art even when it adopts a similar XML/compatibility pattern.

## 3. AMJ standard implementation

### 3.1 Use AMJ-owned unique texture paths

For an asset formally owned by an AMJ module, the default implementation is:

1. keep the original gameplay Def;
2. store the replacement image under an **AMJ-owned unique texture path**;
3. patch the loaded Def's graphic path to that AMJ path;
4. preserve gameplay data and unrelated rendering metadata.

Do **not** make same-path texture shadowing the canonical AMJ mechanism for prerequisite assets.

Same-path shadowing can be useful for generic cosmetic packs, but AMJ needs to be able to assert which module owns the final graphic and which path must be loaded.

### 3.2 Patch the narrowest rendering field possible

Prefer changing only the path field that must change:

- `graphicData/texPath`;
- `plant/leaflessGraphicPath`;
- `plant/immatureGraphicPath`;
- `plant/pollutedGraphicPath`;
- `plant/leaflessImmatureGraphicPath`;
- `plant/snowOverlayGraphicPath`;
- `plant/leaflessSnowOverlayGraphicPath`;
- `plant/immatureSnowOverlayGraphicPath`;
- an explicit UI/blueprint/state path when the target Def actually defines and uses one.

Preserve the source Def's:

- `graphicClass`;
- shader and shader parameters;
- draw size / draw offsets;
- transparency behavior;
- color/material rules;
- gameplay stats and comps;

unless the new artwork **cannot function correctly** with the existing rendering metadata. If rendering metadata must change, document and test that as part of the graphic implementation. It is still not permission to change gameplay balance.

Replace the entire `graphicData` block only when a path-only patch cannot represent the required graphic correctly.

### 3.3 A retexture target is a graphic-state family, not one PNG

Before declaring a prerequisite Def fully retextured, inspect the **loaded 1.6 Def** and enumerate every non-empty graphic state that can appear in normal play.

For plants/trees, audit at minimum:

- base/mature;
- leafless;
- immature;
- polluted;
- leafless immature;
- snow overlay;
- leafless snow overlay;
- immature snow overlay.

For other ThingDefs, also audit applicable:

- directional N/E/S/W graphics;
- stack-count variants;
- blueprint/minified graphics;
- damaged/active/inactive states;
- explicit UI icons.

Do not invent a state that the target Def does not use merely to make the folder set symmetrical. Conversely, do not mark a Def complete while a visible secondary state still falls back to a visually incompatible Vanilla/MO/broad-pack asset.

The **loaded Def is authoritative**, not a memorized list of files from an older RimWorld version.

### 3.4 Optional parent Mods

For an optional prerequisite:

- keep AMJ replacement textures in the owning AMJ module;
- isolate the Def patch in a clearly named compatibility/retexture patch;
- guard it with the parent package ID using `MayRequire`, `PatchOperationFindMod`, or a conditional load folder;
- never copy or edit the parent Mod's distributed image file in place.

For **MO specifically**, the owning module for MO-to-Japan visual conversion is `AMJ - Medieval Overhaul Japanization`. Other AMJ Mods may patch MO gameplay for their own compatibility, but should not ship a competing Japanization retexture for the same MO target. AMJ-owned Def art remains with the Mod that owns that Def.

Use a conditional `loadFolders.xml` directory when a substantial compatibility set benefits from being completely absent unless the parent is active. For small isolated patches, guarded XML is sufficient.

### 3.5 Do not use C# for static texture substitution

Static prerequisite-asset retextures should be Def/XML/load-folder work.

C# or a framework graphic component is justified only when the desired presentation is genuinely dynamic and cannot be represented by the normal graphic system, such as a storage graphic that changes with contents or a deliberate player-selectable variation system.

## 4. Conflict policy with other retexture Mods

### 4.1 AMJ-owned targets win inside the AMJ scope

When Core/Environment has formally claimed a prerequisite Def under the 1-asset-1-owner rule, AMJ's graphic is the canonical AMJ presentation.

Do not automatically surrender that Def to whichever broad texture pack happens to load later. Doing so would make AMJ's visual coherence dependent on arbitrary user load order.

Users remain free to install a deliberate post-AMJ override, but that state is outside AMJ's guaranteed visual baseline.

### 4.2 Same-path packs

A pack that only replaces the original texture file at the same path normally ceases to conflict once AMJ explicitly changes the Def to an AMJ-owned path.

Therefore do not add unnecessary `loadAfter` rules solely for same-path packs such as ordinary narrow Van-style replacements or Clean-Textures-style replacement.

### 4.3 Mods that patch the same Def path

If another active Mod explicitly patches the same `texPath`/state field, patch order matters.

Known examples in the audited set include ReGrowth 2 and parts of VTE.

For each AMJ retexture target:

1. identify known explicit-path competitors;
2. ensure the AMJ patch is applied after them when AMJ is intended to own that target;
3. add a narrow optional `loadAfter` hint only when a real same-field conflict exists;
4. regression-test the final loaded path with that known competitor enabled.

Do not accumulate broad load-order metadata for Mods that do not touch the target.

## 5. Upstream-change resilience

A prerequisite update can rename a Def, remove a state field, change `graphicClass`, or change the source path.

AMJ patches must fail visibly during validation rather than silently falling back to mixed art.

When a retexture target is implemented, validation should lock:

- target package ID / DefName;
- expected state fields;
- expected AMJ path for each owned state;
- texture file existence and PNG integrity;
- relevant graphic class/rendering assumptions;
- optional-parent behavior.

A failed XPath after an upstream update is a maintenance signal. Do not weaken the XPath until the new upstream Def has been inspected.

## 6. Retexture target manifest

When the first prerequisite-asset retexture is committed in an owning repository, add a machine-readable or otherwise automatically validated target manifest containing, at minimum:

- owner module;
- source package;
- DefName;
- graphic-state field;
- expected AMJ texPath;
- activation condition;
- known explicit-path competitors, if any.

The manifest/test must reject duplicate AMJ ownership of the same source Def + state.

For plant/tree families, the manifest should be generated or checked against the loaded Def-state audit so newly introduced upstream states are not overlooked.

## 7. Acceptance boundary

Automated checks should verify:

- target/field still exists;
- final loaded path is the AMJ-owned path;
- optional parent absent => no broken patch;
- all required files resolve;
- all applicable multi-state graphics resolve;
- no BadTex/error regression;
- PNG structure/integrity;
- known explicit-path competitor profile resolves to the intended AMJ path;
- one AMJ owner per source Def/state.

Human review remains responsible for:

- visual quality;
- silhouette/readability;
- scale;
- palette and art-style coherence;
- whether the historical visual interpretation is appropriate.

## 8. Environment-specific application

AMJ Environment tree retextures should follow this shared implementation rule plus Environment's own:

- `Docs/ArtDirection.md`;
- `Docs/GoldenPaths/RetextureGeneration.md`;
- `Docs/GoldenPaths/TextureAssetPipeline.md`.

For Vanilla and MO trees, completion means the **entire loaded graphic-state family used in normal play** has been audited and either retextured or explicitly documented as a deliberate exception. A list that only counts mature/leafless sprites is not by itself proof that the Def's visible states are fully harmonized.
