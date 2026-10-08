# AMJGrains 日本語説明文・翻訳監査（2026-10-08）

**状態: 2026-10-08に§2の15件の日本語説明・作業文が作者承認済み。日本語DefInjectedと英語Def原文へ反映済み。既存Plantの追加史実監査と実ゲームUI表示は未完了。**

本書はAMJGrains固有の承認済み説明と根拠の正本。共通規則は Project `Docs/HistoricalDescriptionGuidelines.md`。§2の日本語候補は今回の承認により確定し、§6の英訳と共に本番へ反映した。DefName・既存labelは変更せず、同時代比較が未監査の既存植物説明については別途継続する。

## 1. 実装・和訳の監査結果

| 対象 | 現状 | 対応 |
|---|---|---|
| アワ・ヒエ・キビ・ソバ・大麦、収穫物・穀粒 | Plant5件の史実・地域情報は§7で承認済み、収穫物・穀粒には既存の機能説明を維持 | Plant5件の説明を日英で本番反映。**Baseで研究不要の大麦**という実装に反する旧記載も訂正済み |
| `AMJC_Wheat` と `AMJC_Barley` | 前者はMO醸造だけを説明、後者は未実装の麦茶・味噌を予告 | Base/MO共通の実装済み食材用途だけに訂正 |
| 共通加工Recipe（雑穀・ソバ・大麦） | 日本語descriptionに「藁を得る」とあり、Baseでは藁を生成しない | Base/MO共通の「殻付き穀物を得る」説明に訂正 |
| 小麦脱穀Recipe | BaseとMOで同じDefNameだがMOでのみ藁生成 | Base翻訳のみ訂正し、MO翻訳は維持 |
| `Plant_Rice` / `RawRice` | Vanilla米を陸稲化し、陸稲の史実説明§7を日英反映。`RawRice` は再利用 | 別の米Plant/食材を追加したと書かない。水田栽培は別Modの責務 |
| 粉 `AMJC_BuckwheatFlour` / `AMJC_MilletFlour` | ThingDef本体description空、和訳labelのみ | 承認済み、日本語・英語へ反映 |
| 料理 `AMJC_Houtou` / `AMJC_Sobagaki` / `AMJC_MilletDumplings` | ThingDef本体description空、和訳labelのみ | 承認済み、日本語・英語へ反映 |
| 共有の製粉・料理Recipe5件 | description空、和訳labelのみ、英語jobStringが残る | 説明文と作業表示の承認済み、日本語・英語へ反映 |
| 非MOの小麦・小麦束・小麦粉・手動石臼（4 ThingDefs）、小麦製粉Recipe | description空、和訳labelのみ | 承認済み、日本語・英語へ反映 |
| MOの既存小麦粉・石臼 | 外部MO所有Defを条件付きで再利用 | グラフィック・歴史説明の本格的日本化はMO Japanizationの所有。Grainsは自Modの互換説明のみ |

## 2. 承認済み日本語説明文（本番XMLに反映）

### 粉・料理

| DefName | 採用済み日本語description |
|---|---|
| `AMJC_BuckwheatFlour` | **蕎麦粉（そばこ）。** 殻を取った蕎麦の実を挽いた粉。湯で練る蕎麦掻きなど、麺にしない粉食にも利用される。 |
| `AMJC_MilletFlour` | **雑穀粉（ざっこくこ）。** 粟・稗・黍から得た可食穀粒を挽いた粉。AMJGrainsでは三種の雑穀を共通の粉にまとめ、団子の材料にする。 |
| `AMJC_Houtou` | **餺飥（はくたく）。** 小麦粉を練って加熱する古い粉食を表現したもの。平安期の史料に見える餺飥と現在の山梨のほうとうには関係が指摘されるが、料理として同一だったとは断定できない。ここでは現代の具だくさんの味噌煮込みを再現せず、簡素な小麦粉食として扱う。 |
| `AMJC_Sobagaki` | **蕎麦掻き（そばがき）。** 蕎麦粉を湯で練って食べる、麺にしない粉食。蕎麦切りが広く普及する以前にも、蕎麦の実を炊くほか粉を練って食べる方法があった。 |
| `AMJC_MilletDumplings` | **雑穀団子（ざっこくだんご）。** 粟・稗・黍などの粉を水で練って加熱する団子状の食物を、一品として抽象化したもの。近世以降の甘味菓子そのものを再現する料理ではない。 |

**表現上の留保:** 餺飥の存在は文献で知られる一方、平安期の餺飥と現代山梨のほうとうが同一の料理であるとの確証はない。麺を打つ工程もAMJGrainsには個別実装しない。雑穀団子も「特定時代の特定レシピ」を忠実再現したとは主張しない。

### 非MOの小麦・石臼

| DefName | 採用済み日本語description |
|---|---|
| `AMJC_Plant_Wheat` | **小麦（こむぎ）。** 日本へは弥生期に伝わり、奈良時代にも栽培が確認される穀物。小麦の穀粒は食事の材料に使え、石臼で挽けば小麦粉として粉食にも利用できる。AMJGrainsでは刈り取った小麦束を脱穀して使う。 |
| `AMJC_RawWheat` | **小麦束（こむぎたば）。** 穂と茎を付けたまま収穫した小麦。未脱穀のままでは食べられず、脱穀によって小麦穀粒になる。 |
| `AMJC_WheatFlour` | **小麦粉（こむぎこ）。** 小麦穀粒を石臼で挽いた粉。AMJGrainsでは餺飥を作るために使う。 |
| `AMJC_ManualMillstone` | **石臼（いしうす）。** 手で穀粒を挽いて粉にする石製の道具。AMJGrainsでは小麦・蕎麦・雑穀の製粉に使用する。 |

### 加工・粉食Recipe（入出力を現行XMLと一致させる案）

| Recipe | 採用済みdescription | 採用済みjobString |
|---|---|---|
| `AMJC_MillWheat` | 脱穀した小麦穀粒10個を挽いて、小麦粉10個にする。 | 小麦を製粉している。 |
| `AMJC_MillBuckwheat` | 殻を取ったソバ穀粒10個を挽いて、蕎麦粉10個にする。 | 蕎麦を製粉している。 |
| `AMJC_MillMillet` | 雑穀10個を挽いて、雑穀粉10個にする。 | 雑穀を製粉している。 |
| `AMJC_CookHoutou` | 小麦粉から餺飥を1個調理する。 | 餺飥を調理している。 |
| `AMJC_CookSobagaki` | 蕎麦粉からそばがきを1個調理する。 | そばがきを調理している。 |
| `AMJC_CookMilletDumplings` | 雑穀粉から雑穀団子を1個調理する。 | 雑穀団子を調理している。 |

粉食Recipeは**Nutrition 0.5相当の粉**を要求する（粉1個のNutritionは0.05）。上表の製粉数量と混同しない。

### 既存Plant和訳の歴史説明（§7で承認・反映済み）

- アワ・ヒエ・キビ: 「粟（あわ）」「稗（ひえ）」「黍（きび）」の名形を確認。史実の気候耐性とゲームの収量・枯死値は分けて説明する。
- ソバ・大麦: 「蕎麦（そば）」「大麦（おおむぎ）」の名形を確認。江戸期の蕎麦切り普及を中世の標準食としない。
- 陸稲: 「陸稲（おかぼ）」の読みと栽培形態を確認。水田・苗代の機能をGrainsが提供すると書かない。
- 中間物: 雑穀・ソバ・大麦の「未脱穀→殻付き→可食」を維持し、同一ThingDefへ集約されるアワ/ヒエ/キビを別々の食材として誤記しない。

## 3. 主な典拠（史実の日本語確認用）

- 小麦/大麦の伝来と奈良時代の栽培: 農林水産省「特集1 麦(1)」 https://www.maff.go.jp/j/pr/aff/1602/spe1_01.html
- 餺飥と現在のほうとうの概要: 農林水産省「ほうとう」 https://www.maff.go.jp/j/keikaku/syokubunka/traditional-foods/menu/hoto.html
- 平安期の「はくたく」と現代ほうとうの直接的なつながりが未確定: 国土交通省「ほうとう」 https://www.mlit.go.jp/tagengo-db/R1-00166.html
- そばがき・蕎麦切りの歴史的な違い: 農林水産省「特集2 新そば」 https://www.maff.go.jp/j/pr/aff/1811/characterinformation.html
- 団子状の粉食に関する長い歴史: 農林水産省「和菓子の歴史」 https://www.maff.go.jp/j/pr/aff/2002/spe2_01.html
- 地域ごとの雑穀食: 文化庁「にし阿波地域の雑穀食」 https://www.bunka.go.jp/seisaku/bunkazai/joseishien/syokubunka_story/93727709.html

これらは歴史説明を起案する根拠であり、特定地域の近世以降の習俗をすべて中世へ遡らせる根拠ではない。

## 4. 反映済み・未完了ゲート

1. §2の**日本語15件が作者承認済み**。共通/非MO各フォルダのThingDef/RecipeDef日本語descriptionと6件のjobStringへ反映した。Grainsの名称を表示文中では **AMJGrains** に統一し、小麦の「実は」の両義性も修正した。
2. §6の英文は承認済み日本語から翻訳し、各ThingDef/RecipeDefの英語原文のdescriptionおよびjobStringへ反映した。日本語だけにない新しい歴史断定を追加しない。既存label・DefName・packageId・料理内容は変更しない。
3. `Tests/test_grains_localization.py` は§2/§6の承認済み文面・ローカライズキー・読み込み対象ファイルと本番XMLの一致を静的検証し、将来の一方だけの文面改変を検出する。
4. §7の六作物の歴史説明は追加承認後に日英へ反映済み。**実ゲーム4構成での表示・言語切替・ERROR 0** は別ゲートのまま。静的検証を実機成功と扱わない。

## 5. 旧MO翻訳Fixtureとの整合（2026-10-08 CI回帰）

`Tests/Fixtures/MO_PreSplit_Contracts.json` は過去のMO必須版を固定する履歴データであり、今後のBase/MO両立を妨げる目的ではない。共通日本語RecipeDefの脱穀説明6件を、Baseでも事実になる「殻付き穀物を得る」記述へ修正したため、旧FixtureにあるMO限定の藁記述から意図的に差分が生じた。

`Tests/validate_grains_base.py` はこの6件だけを**現行の中立表現へ完全一致**で検査し、その後歴史Fixtureの旧文言へ検証用メモリ上で戻して、残りの翻訳・ゲーム仕様・MO互換の履歴ハッシュを照合する。旧Fixtureファイルは一文字も変更しない。未承認の翻訳・加工成果物の変更が紛れても通過しないよう、固定翻訳と中立化6件の負例テストを追加した。


## 6. English localization (translated from approved Japanese, 2026-10-08)

The following descriptions and jobStrings are the approved Japanese-first implementation translations. They are the English Def original strings; do not add unsupported historical claims to this table without revisiting the Japanese source.

| DefName | English description | English jobString, if Recipe |
|---|---|---|
| `AMJC_BuckwheatFlour` | Buckwheat flour (sobako). Flour made from buckwheat grains after their hulls have been removed. It is used in flour-based foods such as sobagaki, made by mixing the flour with hot water rather than forming noodles. | — |
| `AMJC_MilletFlour` | Millet flour (zakkokuko). Flour ground from edible grains of awa, hie, and kibi. In AMJGrains, these three millets share one flour item used to prepare dumplings. | — |
| `AMJC_Houtou` | Hakutaku (餺飥). A dish representing an old kind of wheat-flour food prepared by kneading flour and heating it. Hakutaku in Heian-period records has been linked to present-day Yamanashi hoto, but the two cannot be assumed to be the same dish. Here it represents a simple wheat-flour food, not a modern miso-simmered dish with many ingredients. | — |
| `AMJC_Sobagaki` | Sobagaki (蕎麦掻き). A flour-based dish made by stirring buckwheat flour into hot water instead of shaping it into noodles. Before soba noodles became widespread, buckwheat was also eaten as cooked grains or kneaded flour. | — |
| `AMJC_MilletDumplings` | Millet dumplings (雑穀団子). A single game dish representing dumpling-like foods made by mixing flour from awa, hie, or kibi with water and cooking it. It does not recreate the sweet confections of the early modern period or later. | — |
| `AMJC_Plant_Wheat` | Wheat (komugi). A cereal introduced to Japan in the Yayoi period and known to have been cultivated during the Nara period. Wheat grains can be used in meals or ground into flour for flour-based dishes. In AMJGrains, harvested wheat sheaves must be threshed before use. | — |
| `AMJC_RawWheat` | Wheat sheaf (komugitaba). Harvested wheat with the heads and stalks still attached. It cannot be eaten before threshing, which produces edible wheat grains. | — |
| `AMJC_WheatFlour` | Wheat flour (komugiko). Flour ground from wheat grains using a stone mill. In AMJGrains, it is used to prepare hakutaku. | — |
| `AMJC_ManualMillstone` | Stone mill (ishi-usu). A stone tool for grinding grains into flour by hand. In AMJGrains, it is used to mill wheat, buckwheat, and millet. | — |
| `AMJC_MillWheat` | Grind 10 threshed wheat grains into 10 units of wheat flour. | Milling wheat. |
| `AMJC_MillBuckwheat` | Grind 10 dehulled buckwheat grains into 10 units of buckwheat flour. | Milling buckwheat. |
| `AMJC_MillMillet` | Grind 10 units of edible millet into 10 units of millet flour. | Milling millet. |
| `AMJC_CookHoutou` | Prepare one serving of hakutaku using wheat flour. | Cooking hakutaku. |
| `AMJC_CookSobagaki` | Prepare one serving of sobagaki using buckwheat flour. | Cooking sobagaki. |
| `AMJC_CookMilletDumplings` | Prepare one serving of millet dumplings using millet flour. | Cooking millet dumplings. |

## 7. 既存六作物の承認済み歴史説明（2026-10-08）

**本節の六作物は日本語説明を作者承認済みです。** 先に確定した§2の15件とは別に、§7の日本語を正本として日本語DefInjectedへ反映し、対応する英語を§8に収録して本番XMLへ反映しました。labelは既存の「アワ・ヒエ・キビ・ソバ・大麦・陸稲」を維持し、ゲーム挙動・栽培数値・料理・DefNameは変更していません。

| DefName | 承認済み日本語description | 設計値の照合 |
|---|---|---|
| `AMJC_Plant_FoxtailMillet_Awa` | **粟（あわ）。** 弥生時代の遺跡でも栽培が確認される畑作の雑穀で、米だけに頼らない食料の一つだった。AMJGrainsではキビより生育に時間がかかるが、一度の収穫量が多い。収穫後は脱穀と殻取りを行う。 | 6日／収量13。遺跡資料は吉野ヶ里歴史公園。 |
| `AMJC_Plant_BarnyardMillet_Hie` | **稗（ひえ）。** 古くから栽培され、地域によっては米よりも日常的に食べられた雑穀。山間部で稗をふだんの主食として利用した記録も残る。AMJGrainsではアワやキビより低温で生育できるが、霜への強さまで保証するものではない。収穫後は脱穀と殻取りを行う。 | 成長最低5℃（アワ・キビ8℃）。日常食は農水省の宮崎県北部事例であり全国一律の歴史ではない。 |
| `AMJC_Plant_ProsoMillet_Kibi` | **黍（きび）。** 米・麦・粟などと並び、「五穀」の一つに数えられることもある雑穀。AMJGrainsではアワ・ヒエより早く成熟し、肥沃度の影響も比較的小さい一方、一度の収穫量は少ない。収穫後は脱穀と殻取りを行う。 | 5日／収量11／肥沃度感応0.3。「五穀」には黍に代えて稗を含める異説あり。 |
| `AMJC_Plant_Buckwheat_Soba` | **蕎麦（そば）。** 古代には凶作に備える作物として栽培を勧められ、山間部や痩せた土地でも育てられてきた。AMJGrainsでは短期栽培に向くが霜には弱く、収穫後に脱穀・殻取りを行う。古い蕎麦の食べ方と、江戸期に広まる麺状の蕎麦切りは区別する。 | 4日／収量8／最低肥沃度0.4。農水省の救荒作物・蕎麦切り史。 |
| `AMJC_Plant_Barley` | **大麦（おおむぎ）。** 弥生時代に日本へ伝わり、奈良時代にも栽培が確認される麦類。米とともに食生活を支えてきた。AMJGrainsでは冷涼な気温での栽培に向き、雑穀より生育期間は長いが収量が多い。収穫後は脱穀と殻取りを行う。 | 10日／収量22／成長最低0℃。農水省「特集1 麦(1)」。 |
| `Plant_Rice` | **陸稲（おかぼ・りくとう）。** 水田で育てる水稲と異なり、畑に作付けする稲。日本でも水稲と併せて栽培されてきたが、20世紀半ば以降は栽培が大幅に縮小した。AMJGrainsではバニラの稲を陸稲として扱い、温暖な気温と一定以上の肥沃度を必要とする。収穫物は従来の米を使い、水田栽培は別Modに委ねる。 | Vanilla `Plant_Rice` Patch：5日／収量11／最低肥沃度0.7／成長10～42℃。陸稲の古代の普及割合は確定していない。 |

### 根拠・留保

- 粟・稗の弥生期遺跡：https://www.yoshinogari.jp/ym/episode04/foods01.html
- 稗を日常食とした宮崎県北部の事例：https://www.maff.go.jp/j/keikaku/syokubunka/k_ryouri/search_menu/menu/hie_zushii_miyazaki.html
- 黍と稗をめぐる「五穀」の異説：https://www.maff.go.jp/j/keikaku/syokubunka/traditional-foods/bunrui/mamerui-kakou.html
- 蕎麦の救荒作物としての歴史と蕎麦切り：https://www.maff.go.jp/j/pr/aff/1811/characterinformation.html
- 大麦の日本への伝来と奈良時代の栽培：https://www.maff.go.jp/j/pr/aff/1602/spe1_01.html
- 陸稲・水稲の歴史と1955年頃以降の陸稲減少：https://www.maff.go.jp/j/syouan/keikaku/soukatu/okome_summary/07/environ_ment_03.html

**史実・ゲーム値の線引き:** ゲームで設定した最低生育温度を史実の絶対的な耐霜性とは解釈しません。地域の郷土食の記録を古代から全国一律の慣習とすることも避けます。表示名を「アワ」から「粟」等へ改めるかは本節では決めず、現行labelを維持しています。追加機能（稲の田植えや酒造等）も予告しません。


## 8. English descriptions translated from §7 approved Japanese (2026-10-08)

These six English strings are translations of the author-approved Japanese §7 descriptions. The five shared plants use `Defs/ThingDefs_Plants/Plants_StageA.xml`; the reused Vanilla `Plant_Rice` is patched by `Patches/UplandRice.xml`. Earlier §2/§6 approved food, milling, and non-MO wheat descriptions remain unchanged.

| DefName | English description |
|---|---|
| `AMJC_Plant_FoxtailMillet_Awa` | Foxtail millet (awa). A dry-field millet found at archaeological sites from the Yayoi period, and one of the grain foods eaten alongside rice. In AMJGrains it takes longer to grow than kibi but yields more grain per harvest. Harvested grain must be threshed and dehulled. |
| `AMJC_Plant_BarnyardMillet_Hie` | Japanese barnyard millet (hie). A grain cultivated since ancient times and eaten more routinely than rice in some regions. Records from mountain communities also describe its use as an everyday staple. In AMJGrains it grows at lower temperatures than awa or kibi, but this does not guarantee greater resistance to frost. Harvested grain must be threshed and dehulled. |
| `AMJC_Plant_ProsoMillet_Kibi` | Proso millet (kibi). A millet sometimes counted among the traditional five grains, together with rice, mugi and awa. In AMJGrains it matures sooner than awa or hie and is relatively less affected by soil fertility, but yields less grain per harvest. It must be threshed and dehulled after harvest. |
| `AMJC_Plant_Buckwheat_Soba` | Buckwheat (soba). In ancient Japan it was recommended as a crop to guard against poor harvests, and it has been grown in mountain regions and on less fertile land. In AMJGrains it grows quickly but is vulnerable to frost, and requires threshing and dehulling. Older ways of eating buckwheat are distinct from cut soba noodles, which became widespread in the Edo period. |
| `AMJC_Plant_Barley` | Barley (omugi). A cereal introduced to Japan in the Yayoi period and known to have been cultivated during the Nara period. It has long contributed to diets alongside rice. In AMJGrains it grows well in cooler conditions, takes longer to mature than the millets, and yields a larger harvest. Harvested grain must be threshed and dehulled. |
| `Plant_Rice` | Upland rice (okabo, rikuto). Rice grown in dry fields rather than flooded paddies. It has been cultivated in Japan alongside paddy rice, but its cultivation declined sharply after the middle of the twentieth century. In AMJGrains Vanilla rice is treated as upland rice and requires warm temperatures and sufficiently fertile soil. It yields the existing rice item; paddy cultivation belongs to a separate mod. |

**Static verification:** `Tests/test_grains_localization.py` checks approved Japanese/English text against loaded-source XML/DefInjected and verifies the `Plant_Rice` description Patch. Game-loaded language switching, UI readability and four-profile ERROR 0 are still pending.
