# Medieval Overhaul Japanization Research Audit

## Status

This document is the detailed **first-pass research-tree audit** for `AMJ - Medieval Overhaul Japanization`.

It is a design/research source, not an implementation claim. The classifications below are candidates to drive the next historical and item/recipe-level audit. A row marked “非表示候補” or “再解釈” does **not** mean the upstream Def has already been removed, patched, renamed, or retextured.

### Audited snapshot

- Medieval Overhaul Workshop archive: `3219596926.zip`
- audited 1.6 payload: Medieval Overhaul 1.6.2.2
- archive SHA-256: `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`
- MO-owned `ResearchProjectDef`: **51**
- Vanilla `ResearchProjectDef` moved/reworked by MO: **16**
- combined audit surface: **67 research nodes**

Primary XML inputs:
- `1.6/Defs/ResearchProjectDefs/ResearchProjects_Misc.xml`
- `1.6/Patches/Core/Change_ResearchProjectDef.xml`
- related ThingDef / RecipeDef / Processor patches when tracing unlocks

## Decision rule

Japanization does not ask “is this object Western?” and delete it mechanically. For each MO research node:

1. **維持** — the technology and gameplay role already make sense in ancient/medieval Japan.
2. **再配置** — the function is valid, but MO places it in a Western/fantasy or historically unsuitable prerequisite chain.
3. **再解釈＋リテクスチャ** — preserve the gameplay Def/role where possible, but change the Japanese historical referent, label/description, and MO-owned graphic.
4. **非表示** — no suitable Japanese historical role is needed and removing the normal unlock path does not break progression.
5. **要追加監査 / 再設計** — evidence or item/recipe-level consequences are not yet sufficient for a final choice.

The target chronology is not a rigid era ladder. Broad working bands are:
- **古代基盤** — prehistoric/ancient through Nara–Heian where the technology is already established enough to be a baseline;
- **中世前期** — Kamakura-oriented progression;
- **中世後期** — Muromachi–Sengoku progression;
- **戦国末期** — technologies whose standard Japanese use belongs near the end of AMJ's scope;
- **対象外** — Edo/early-modern completion, industrial technology, fantasy-only progression, or a branch with no justified Japan-side role.

AMJ ends before Edo. A technology can exist earlier without needing a dedicated research node; the node should exist only when it creates useful gameplay progression.

## A. Production, domestic life, craft, infrastructure — 16 MO nodes

| DefName | MO/Vanilla label | 初回分類 | 時代位置 | Japanizationでの扱い |
|---|---|---|---|---|
| `DankPyon_Lumber` | Basic woodworking | **維持** | 古代基盤 | 基礎木工としてそのまま有効。MO Defを維持し、日本語名・説明のみ歴史記述を監査。 |
| `DankPyon_RusticFurniture` | Rustic furniture | **再解釈＋リテクスチャ** | 古代～中世 | 西欧 rustic 家具ではなく、農村の木工・建具・簡素な調度へ置換。機能が同じならDefは増やさない。 |
| `DankPyon_RoyalRusticFurniture` | Royal architecture | **再解釈＋リテクスチャ** | 中世後期 | 上層・格式ある建築/調度へ。王侯制をそのまま日本へ移植せず、解禁物ごとに日本側の対応物を監査。 |
| `DankPyon_RusticStorage` | Rustic storage | **再解釈＋リテクスチャ** | 古代～中世 | 収納機能は再利用。西欧外観を日本の木箱・棚・容器等へ寄せる。 |
| `DankPyon_Presser` | presser | **再解釈＋リテクスチャ** | 中世 | 圧搾技術として残す候補。製紙・搾油等へ使える一方、リンゴ/チーズ等の西欧寄り出力はRecipe単位で監査。 |
| `DankPyon_CarrierBirds` | carrier birds | **要追加監査** | 未確定 | 中世日本の標準技術進行として置く根拠が弱い。標準では非表示候補。Explorationの必須前提にはしない。 |
| `DankPyon_Exploration` | exploration | **再解釈＋再配置** | 中世 | 測量・地誌・旅支度等へ再解釈。Carrier Birds前提を外し、Stonecutting等との接続も再検討。 |
| `DankPyon_LeatherTanning` | leather tanning | **維持** | 古代基盤 | 皮革加工は基礎技術として有効。設備外観・説明のみ日本側監査。 |
| `DankPyon_TextileSpinning` | textile spinning | **再解釈＋リテクスチャ＋前倒し** | 古代基盤 | MOの西洋式spinning wheelを標準形にせず、紡錘・手紡ぎを基準へ。古代の紡錘車資料に合わせて早期化。 |
| `DankPyon_Silk` | silk | **前倒し** | 古代～中世 | 絹・養蚕は中世専用技術ではない。TextileSpinning後の中世Tier固定を外し、工程/設備の実物監査を行う。 |
| `DankPyon_CandleMaking` | candle making | **後期へ再配置** | 中世後期 | 蝋燭の使用自体は古いが、国産化を一般生産技術として置くなら室町後期寄り。輸入/寺社利用と量産を区別する。 |
| `DankPyon_Jewelry` | jewelry | **再解釈** | 古代～中世 | 宝飾一般ではなく装身具・飾金具等として再整理。既存Recipeごとに日本側対応を判定。 |
| `DankPyon_Engineering` | engineering | **再解釈** | 中世 | 機構・土木・大型設備の基礎研究として利用。西欧固有の『engineering』像を日本史へ直訳しない。 |
| `DankPyon_Mining` | mining | **維持** | 古代～中世 | 採鉱技術として維持。資源分布や砂鉄生産は別責務。 |
| `DankPyon_Windmill` | windmill | **非表示候補** | 対象外 | MOの動力風車はAMJ範囲の日本技術として根拠が弱い。DBH for MedievalのWindPumpがこの研究へ接続する点も互換Patchで解消する。 |
| `DankPyon_Watermill` | watermill | **前倒し** | 古代～中世 | 日本書紀系の610年伝来記録があり、中世Engineering後まで遅らせない。MO設備機能は再利用候補。 |


## B. Military, metal, siege, weapons — 22 MO nodes

| DefName | MO/Vanilla label | 初回分類 | 時代位置 | Japanizationでの扱い |
|---|---|---|---|---|
| `DankPyon_Crossbow` | crossbow | **再解釈＋リテクスチャ＋前倒し** | 古代 | 古代日本の弩へ。8世紀伊治城跡の弩機が根拠。西欧中世crossbow研究としては扱わない。 |
| `DankPyon_HeavyCrossbow` | arbalest | **要追加監査** | 古代候補 | 強弩等への再解釈余地はあるが、MO arbalestの役割・外観を日本側へ対応させる史料監査が必要。 |
| `DankPyon_Ballista` | ballista | **再解釈＋リテクスチャ候補** | 古代 | 古代律令軍には携行型だけでなく設置型の弩も研究対象として確認できる。MO砲台の性能・サイズを監査し、`弩台` 等の据置弩として成立するものだけ再利用する。 |
| `DankPyon_Trebuchet` | trebuchet | **非表示候補** | 対象外 | 元寇では大陸側投石器の記録があるが、日本側の標準的な自前技術進行として置く根拠にはならない。 |
| `DankPyon_RepeaterBallista` | ballista repeater | **非表示候補** | 対象外 | AMJ標準の日本技術枝として維持する根拠が薄い。 |
| `DankPyon_Alchemy` | alchemy | **分解・再解釈** | 古代～中世 | 西欧/幻想錬金術ノードは維持しない。本草・薬学等に再解釈できる出力だけ残し、Steel/Gunpowder/Tarをここから切り離す。Potion類は個別監査。 |
| `DankPyon_Steel` | Steel | **再配置** | 中世 | Alchemy前提を撤回し、SmithingとMO金属加工へ接続。日本製鉄ゲームループ自体はIronmaking所有。 |
| `DankPyon_Plasteel` | Mithril | **非表示** | 対象外 | 幻想金属進行は歴史日本化の標準ツリーから外す。Def削除より非表示/経路切断を優先。 |
| `DankPyon_Tar` | tar | **要追加監査** | 未確定 | 松脂・木タール等として成立する可能性はあるが、MO出力用途が攻城/錬金寄りなのでRecipe単位の用途監査後に判断。 |
| `DankPyon_Gunpowder` | gunpowder | **後期へ再配置＋リテクスチャ** | 戦国末期 | Alchemyから切り離し、1543年以後の火縄銃受容・国内製作へ接続。Handgonne等は火縄銃系へ置換候補、投擲火器は個別監査。 |
| `DankPyon_ProtectiveClothing` | protective clothing | **再解釈＋リテクスチャ** | 古代～中世 | 西欧gambeson等をそのまま残さず、日本側の軽装防具・札/布革防具へ役割対応。 |
| `DankPyon_ChainArmor` | chain armor | **再解釈＋枝分離** | 中世後期 | 鎖帷子等へ対応可能。ただしPlateArmorの必須前提にはせず、別系統の防護技術として扱う。 |
| `DankPyon_HuntingBow` | hunting bow | **再解釈＋リテクスチャ** | 古代～中世 | 日本の狩猟弓として外観・名称を調整。西欧弓の直列発展をそのまま使わない。 |
| `DankPyon_WarBow` | war bow | **再解釈＋リテクスチャ** | 古代～中世 | 戦闘用和弓の上位役割へ。Greatbowとの重複・研究順を整理。 |
| `DankPyon_BasicPolearms` | basic polearms | **再解釈＋リテクスチャ** | 古代～中世 | MOの槍系役割を日本の槍・長柄武器へ写像。個別武器の対応表を別途作る。 |
| `DankPyon_MilitaryPolearms` | military polearms | **再解釈＋リテクスチャ** | 中世 | 槍・薙刀等の軍用長柄武器へ。西欧名称を維持しない。 |
| `DankPyon_NoblePolearms` | noble polearms | **再解釈＋整理** | 中世後期 | 『noble』Tierは撤回候補。高技能/専門長柄武器へ意味を置換し、不要な重複Defは隠す。 |
| `DankPyon_BasicMaces` | basic maces | **再解釈＋整理** | 古代～中世 | 棍棒・金砕棒等へ対応可能なものだけ残す。 |
| `DankPyon_MilitaryMaces` | military maces | **再解釈＋整理** | 中世 | Morning star等、西欧形状を無理に日本武器へ見せ替えず、役割が合うDefだけ再利用。 |
| `DankPyon_NobleMaces` | noble maces | **再解釈＋整理** | 中世後期 | 『noble』Tierは撤回候補。上位打撃武器として独自の役割が残るものだけ採用。 |
| `DankPyon_BasicBlades` | basic blades | **再解釈＋リテクスチャ** | 古代～中世 | 西欧falchion等を日本の刃物/刀剣役割へ再配置。 |
| `DankPyon_MilitaryBlades` | military blades | **再解釈＋リテクスチャ** | 中世 | Arming sword/longsword等の性能枠を日本刀剣へ写像。LongBladesとの段階整理が必要。 |


## C. Agriculture, cooking, armor decoration — 13 MO nodes

| DefName | MO/Vanilla label | 初回分類 | 時代位置 | Japanizationでの扱い |
|---|---|---|---|---|
| `DankPyon_BasicAgriculture` | basic agriculture | **再設計** | 古代基盤 | 汎用栽培基盤として残す候補。作物の強弱だけでTier分けせず、AMJ作物の解禁は各所有Modが決める。 |
| `DankPyon_IntermediateAgriculture` | intermediate agriculture | **再設計** | 古代～中世 | 中級という抽象Tierではなく、実際の栽培技術/設備差へ意味を持たせる。 |
| `DankPyon_AdvancedAgriculture` | advanced agriculture | **再設計** | 中世 | 同上。日本での成立時期とゲーム上の設備差がないならノード統合も候補。 |
| `DankPyon_TreeGriffonBerry` | griffon berry | **非表示** | 対象外 | MO幻想作物専用研究。歴史日本化ツリーから外す。 |
| `DankPyon_PlowedSoil` | plowed soil | **維持＋前倒し** | 古代基盤 | 耕起そのものを中世高位技術にしない。具体設備・効果のみバランス監査。 |
| `DankPyon_BasicCooking` | basic cooking | **再設計** | 基盤 | 調理基盤として残すが、MO西欧料理の一括解禁ノードにはしない。Recipeを個別選別。 |
| `DankPyon_IntermediateCooking` | intermediate cooking | **再設計** | 中世 | パン・パイ等の料理名Tierをそのまま日本化しない。工程差が残る料理だけ接続。 |
| `DankPyon_AdvancedCooking` | advanced cooking | **再設計** | 中世後期 | 高級料理の名前違いで増やさず、材料/工程/効果に独立価値があるRecipeのみ残す。 |
| `DankPyon_Smoker` | smoker | **要追加監査** | 未確定 | Food Drying等との重複と、日本側で燻煙が独立設備としてゲーム判断を生むかを先に監査。 |
| `DankPyon_Grill` | grill | **再解釈＋リテクスチャ** | 基盤～中世 | 炉端・直火焼き等へ置換可能。専用西欧grill外観は日本化。 |
| `DankPyon_StewPot` | stews | **再解釈＋リテクスチャ** | 基盤～中世 | 鍋による煮炊きへ。西欧stew料理群はRecipe単位で整理。 |
| `DankPyon_Oven` | baking | **非表示/再解釈候補** | 未確定 | MOのパン・パイ・ケーキ中心枝をそのまま維持しない。Grainsの粉食と競合しない最低限用途がある場合のみ再解釈。 |
| `DankPyon_AdornedArmor` | Adorned armor | **再解釈＋リテクスチャ** | 中世後期 | 格式・装飾を備えた日本甲冑へ。NobleApparel前提も日本側の身分/工芸進行へ再設計。 |


## D. Vanilla research nodes moved/reworked by MO — 16 nodes

| DefName | MO/Vanilla label | 初回分類 | 時代位置 | Japanizationでの扱い |
|---|---|---|---|---|
| `Devilstrand` | Devilstrand | **MOタブから退避候補** | 対象外 | MOが中世タブへ取り込んでいるだけで、日本化対象として意味を付けない。Vanilla側の扱いを壊さない形でMO歴史ツリーから外す候補。 |
| `PsychoidBrewing` | Psychoid brewing | **MOタブから退避候補** | 対象外 | 日本中世技術としてMOツリーへ組み込む理由がない。Vanilla機能自体の削除とは分ける。 |
| `Smithing` | Smithing | **維持＋再配置** | 古代～中世 | 金属加工の中核。MO SteelとIronmaking互換の接続点として再設計。 |
| `CarpetMaking` | Carpet making | **要追加監査** | 未確定 | 敷物・編組への再解釈余地はあるが、畳/ござ等を単なるcarpetへ置換するかは既存和風Modとの重複も含め監査。 |
| `PassiveCooler` | Passive cooler | **MOタブから退避候補** | 対象外/未確定 | MO日本史ツリーの必須要素にはしない。Vanilla機能を消すかは別判断。 |
| `ComplexFurniture` | Complex furniture | **再解釈** | 中世 | 木工・指物・格式ある調度へ接続。Vanilla資産まで一律に日本化するかは別途所有監査。 |
| `TreeSowing` | Tree sowing | **維持** | 古代～中世 | 樹木栽培一般として有効。対象樹種の歴史適合性は各Plant/Environment側で監査。 |
| `Cocoa` | Fruit tree sowing | **再解釈** | 古代～中世 | MOが既に果樹栽培一般へ改称。Cocoa固有の意味は切り離し、日本で扱う果樹だけ接続。 |
| `Pemmican` | food preservation | **再解釈** | 古代～中世 | 保存技術一般として利用余地あり。ただしPemmicanそのものを日本食へ見せ替えず、Recipe/設備単位で接続先を監査。 |
| `Brewing` | Brewing | **再設計/非表示候補** | 未確定 | MOのale/cider/wine等をそのまま標準日本化しない。AMJ Brewingは独立Modなので必須にせず、併用時のみ研究接続する。 |
| `Stonecutting` | Stonecutting | **維持** | 古代～中世 | 石材加工として維持。RusticFurniture必須というMO順序は再検討。 |
| `RecurveBow` | archery | **再解釈＋再配置** | 古代～中世 | 日本弓術の基礎研究へ。HuntingBow/Greatbow/WarBowの直列関係を日本側武器役割で再構成。 |
| `Greatbow` | Greatbow | **再解釈** | 古代～中世 | 大型戦闘弓の性能枠を和弓へ写像する候補。個別武器の画像/名称は別監査。 |
| `ComplexClothing` | tailoring | **再解釈** | 古代～中世 | 裁縫・仕立て一般へ。日本衣服DefをJapanizationへ抱え込まず、既存和服Mod/将来AMJ Clothingとの接続点にする。 |
| `PlateArmor` | Plate armor | **再解釈＋後期化** | 戦国後期 | 西欧plate suitではなく、室町末～桃山の板物を増した当世具足等へ役割対応。ChainArmor必須前提は撤回候補。 |
| `LongBlades` | Long blades | **再解釈＋リテクスチャ** | 中世 | MO長剣Tierを日本刀剣の上位鍛造/長寸刀剣へ写像。Basic/Military Bladesとの重複を整理。 |


## High-confidence structural changes from the first pass

These are stronger than the individual item mapping and should guide the next pass:

- **Break the MO `Alchemy -> Steel / Tar / Gunpowder` trunk.** Steel belongs with metalworking; gunpowder belongs at the late-Sengoku end; alchemy/fantasy-potion content must be split into historically supportable pharmacology/technical content versus content to hide.
- **Do not keep `ChainArmor -> PlateArmor` as a mandatory linear path.** Japanese chain protection and late plate-heavy/tōsei-gusoku development are not a single European armor ladder.
- **Move crossbow technology to the ancient side and split handheld from fixed weapons.** The Japanese `弩` is directly attested archaeologically in an eighth-century state-military context, and research literature distinguishes portable and installed forms. MO currently mixes a handheld crossbow with a Scorpio turret under `DankPyon_Crossbow`, and an arbalest with a Ballista turret under `DankPyon_HeavyCrossbow`; Japanization must not preserve that coupling blindly.
- **Move water power much earlier than MO's Engineering end branch, while hiding the MO power windmill by default.**
- **Replace the Western spinning-wheel visual/meaning with spindle/hand-spinning unless a specific historically valid wheel is proven for the target period.**
- **Do not preserve MO's “Basic / Intermediate / Advanced” agriculture and cooking tiers merely because they exist.** Keep only distinctions that correspond to an actual technique, equipment, material-processing step, or meaningful gameplay choice.
- **Treat weapon Japanization as a Def-preserving mapping problem first.** If a MO weapon's performance and recipe role map cleanly to a Japanese weapon, keep the Def and replace label/description/graphic. Hide or consolidate outputs that would require a misleading one-to-one mapping.
- **World Tech Level remains the broad world/tech filter.** This audit is about restructuring MO, not filtering every external Mod.

## Historical anchors already strong enough to use

These sources support the structural decisions above; they do not by themselves finalize every item-level mapping.

- **Ancient crossbow / 弩:** 文化遺産オンライン, 「弩機　伊治城跡出土」. The item is dated Nara–Heian and interpreted as a portable crossbow mechanism belonging to an eighth-century frontier garrison.  
  https://online.bunka.go.jp/heritages/detail/430282
  宮城県の指定文化財解説も同資料を8世紀後半の実戦用携行弩とし、奈良文化財研究所系資料では律令軍の配備、CiNii掲載論文では携行型/設置型の運用が研究対象となっている。  
  https://www.pref.miyagi.jp/soshiki/bunkazai/kouko10-doki.html  
  https://repository.nabunken.go.jp/dspace/bitstream/11177/8274/1/BA62154222_2_090_114.pdf  
  https://cir.nii.ac.jp/crid/1520853832330876416
- **Spindle technology:** 文化遺産オンライン, 「紡錘車」, Yayoi 2nd–3rd century, and related Yayoi/古墳 finds. This supports early hand-spinning while not proving MO's Western spinning-wheel form.  
  https://online.bunka.go.jp/heritages/detail/593979  
  https://online.bunka.go.jp/heritages/detail/473061
- **Watermill:** コトバンク「水車」 records the traditional date of transmission in 610 and `日本書紀`'s account of 曇徴 making a `碾磑`; NDL reference material also notes waterwheels in use from the Heian period.  
  https://kotobank.jp/word/%E6%B0%B4%E8%BB%8A-82926  
  https://crd.ndl.go.jp/reference/entry/reference/show?id=1000071776
- **Power windmill:** コトバンク「風」 describes the first modern power windmill in Japan as an 1869 Yokohama installation. This makes MO's medieval power-windmill branch a poor default Japanization fit; a separate audit remains necessary if evidence for another premodern wind-power device is proposed.  
  https://kotobank.jp/word/%E9%A2%A8-44718
- **Gun / matchlock:** MLIT Kyushu records the 1543 introduction of firearms to Tanegashima and subsequent domestic copying and mass spread during the Sengoku period.  
  https://www.qsr.mlit.go.jp/suishin/story2019/03_8.html
- **Late medieval armor:** 文化遺産オンライン documents Muromachi `胴丸` and Momoyama `当世具足` / `南蛮胴具足`, supporting a late armor branch that is Japanese rather than a European plate-suit ladder.  
  https://online.bunka.go.jp/heritages/search/freetext:%E8%83%B4%E4%B8%B8  
  https://online.bunka.go.jp/heritages/detail/155228
- **Candle production:** コトバンク's candle history records imported/elite use much earlier but domestic production in the late Muromachi period. This supports separating “candle exists” from “colony can routinely manufacture candles.”  
  https://kotobank.jp/word/%E8%A0%9F%E7%87%AD-1217471
- **Medieval oil production:** コトバンク「油座」 records medieval production and trade of lamp oil, especially egoma oil, with oil guilds active from late Heian through Kamakura/Muromachi. This supports reusing a press as a Japanese oil-pressing function rather than preserving only Western food-processing outputs.  
  https://kotobank.jp/word/%E6%B2%B9%E5%BA%A7-26837
- **Foreign siege weapons at the Mongol invasions:** NDL Reference Collaborative Database describes `石弓（投石器）` among weapons brought by the Yuan forces. This is evidence for encounter with such weapons, not evidence that a trebuchet should be a standard Japanese domestic research branch.  
  https://crd.ndl.go.jp/reference/detail?page=ref_view&id=1000187318

## Def-level military mapping

The military/equipment follow-up is now maintained in
[MedievalOverhaulJapanizationMilitaryMapping.md](MedievalOverhaulJapanizationMilitaryMapping.md).
It records the actual MO Defs gated by the crossbow/siege, armor, bow, polearm,
mace, blade, gunpowder, Smithing and tailoring research families. Its Def-level
mapping takes precedence over any earlier node-only shorthand in this document.

## Remaining item-level audits before XML design

The 67-node table is not enough to implement safely. Before production patches:

1. Enumerate every building, weapon, apparel, recipe, plant and processor unlocked by each node after the full MO 1.6 load.
2. For every reinterpreted weapon/armor node, create a **MO Def -> Japanese referent** mapping with:
   - same gameplay role?
   - same material/recipe meaning?
   - historical period?
   - retexture only, label+retexture, or hide?
3. For agriculture/cooking, separate research structure from content ownership:
   - Grains / Rice Cultivation own their crops and primary processing;
   - Fermentation / Brewing / Preservation remain independent;
   - Japanization only curates MO outputs and optional cross-Mod connections.
4. Audit every node whose proposed treatment is “要追加監査”, especially:
   - Carrier Birds;
   - Heavy Crossbow / Ballista;
   - Tar;
   - Smoker;
   - Carpet Making;
   - MO Oven;
   - Western alcohol recipes.
5. Build a dependency graph and prove that hiding/replacing a node does not orphan recipes/buildings or break third-party MO compatibility.
6. Keep upstream DefNames wherever possible. Prefer hiding/repositioning/patching over deleting Defs.
7. Add automated validation for:
   - no visible orphan research;
   - no hidden prerequisite blocking a visible node;
   - every Japanization retexture target resolves to an AMJ-owned texPath;
   - optional DBH for Medieval / Ironmaking / Grains integrations remain conditional;
   - runtime ERROR 0 in supported profiles.

## DBH for Medieval consequences already identified

DBH for Medieval currently connects some functionality to MO research. Japanization must re-route those connections as the MO tree changes.

- its wind pump is connected to `DankPyon_Windmill`; if the MO power-windmill node is hidden, the wind-pump unlock must not become orphaned;
- manual pump / well / sanitation / irrigation research should be placed according to their own technical role, not inherited blindly from MO's Western tree;
- DBH for Medieval's pipe-based irrigation canal/sluice remains distinct from Waterworks' gravity-fed natural-water canal network;
- Japanization may rework DBH for Medieval labels, materials, research placement and graphics, but must not reimplement its C# plumbing behavior.

## Ownership reminder

- **Japanization:** MO research restructuring, MO-owned Japanization retextures, MO/DBH-for-Medieval compatibility around those changes.
- **Ironmaking:** Japanese iron-production game loop.
- **Grains / Rice Cultivation:** crop and primary-processing balance.
- **Waterworks:** gravity-fed natural-water canal network.
- **Hot Springs:** hot-spring generation, bathing/tōji loop.
- **World Tech Level:** broad tech-level/world filtering.

Japanization is an integration layer, not a common dependency hub.
