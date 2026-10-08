# Grains 日本語説明文・翻訳監査（2026-10-08）

**状態: 現行Defと和訳の監査・日本語候補作成済み。作者未承認、英訳・本番の新規歴史description未反映。**

本書はGrains固有の説明文候補と根拠の正本。共通規則は Project `Docs/HistoricalDescriptionGuidelines.md` を参照。DefNameと既存labelは変更せず、歴史的説明は日本語確認後に英語へ翻訳する。

## 1. 実装・和訳の監査結果

| 対象 | 現状 | 対応 |
|---|---|---|
| アワ・ヒエ・キビ・ソバ・大麦、収穫物・穀粒 | 和訳descriptionあり、史実・地域情報は薄く、ゲーム数値中心 | 歴史説明の再審査は未承認。**Baseで研究不要の大麦**という実装に反する記載を訂正 |
| `AMJC_Wheat` と `AMJC_Barley` | 前者はMO醸造だけを説明、後者は未実装の麦茶・味噌を予告 | Base/MO共通の実装済み食材用途だけに訂正 |
| 共通加工Recipe（雑穀・ソバ・大麦） | 日本語descriptionに「藁を得る」とあり、Baseでは藁を生成しない | Base/MO共通の「殻付き穀物を得る」説明に訂正 |
| 小麦脱穀Recipe | BaseとMOで同じDefNameだがMOでのみ藁生成 | Base翻訳のみ訂正し、MO翻訳は維持 |
| `Plant_Rice` / `RawRice` | Vanilla米を陸稲化。陸稲の和訳label/descriptionあり | 別の米Plant/食材を追加したと書かない。史実説明の拡張案は審査待ち |
| 粉 `AMJC_BuckwheatFlour` / `AMJC_MilletFlour` | ThingDef本体description空、和訳labelのみ | 日本語候補あり、未承認 |
| 料理 `AMJC_Houtou` / `AMJC_Sobagaki` / `AMJC_MilletDumplings` | ThingDef本体description空、和訳labelのみ | 日本語候補あり、未承認 |
| 共有の製粉・料理Recipe5件 | description空、和訳labelのみ、英語jobStringが残る | 説明文と作業表示の日本語候補あり、未承認 |
| 非MOの小麦・小麦束・小麦粉・手動石臼（4 ThingDefs）、小麦製粉Recipe | description空、和訳labelのみ | 日本語候補あり、未承認 |
| MOの既存小麦粉・石臼 | 外部MO所有Defを条件付きで再利用 | グラフィック・歴史説明の本格的日本化はMO Japanizationの所有。Grainsは自Modの互換説明のみ |

## 2. 日本語説明文の候補（作者承認前、まだゲーム内へ反映しない）

### 粉・料理

| DefName | 日本語description候補 |
|---|---|
| `AMJC_BuckwheatFlour` | **蕎麦粉（そばこ）。** 殻を取った蕎麦の実を挽いた粉。湯で練る蕎麦掻きなど、麺にしない粉食にも利用される。 |
| `AMJC_MilletFlour` | **雑穀粉（ざっこくこ）。** 粟・稗・黍から得た可食穀粒を挽いた粉。Grainsでは三種の雑穀を共通の粉にまとめ、団子の材料にする。 |
| `AMJC_Houtou` | **餺飥（はくたく）。** 小麦粉を練って加熱する古い粉食を表現したもの。平安期の史料に見える餺飥と現在の山梨のほうとうには関係が指摘されるが、料理として同一だったとは断定できない。ここでは現代の具だくさんの味噌煮込みを再現せず、簡素な小麦粉食として扱う。 |
| `AMJC_Sobagaki` | **蕎麦掻き（そばがき）。** 蕎麦粉を湯で練って食べる、麺にしない粉食。蕎麦切りが広く普及する以前にも、蕎麦の実を炊くほか粉を練って食べる方法があった。 |
| `AMJC_MilletDumplings` | **雑穀団子（ざっこくだんご）。** 粟・稗・黍などの粉を水で練って加熱する団子状の食物を、一品として抽象化したもの。近世以降の甘味菓子そのものを再現する料理ではない。 |

**表現上の留保:** 餺飥の存在は文献で知られる一方、平安期の餺飥と現代山梨のほうとうが同一の料理であるとの確証はない。麺を打つ工程もGrainsには個別実装しない。雑穀団子も「特定時代の特定レシピ」を忠実再現したとは主張しない。

### 非MOの小麦・石臼

| DefName | 日本語description候補 |
|---|---|
| `AMJC_Plant_Wheat` | **小麦（こむぎ）。** 日本へは弥生期に伝わり、奈良時代にも栽培が確認される穀物。実は食材になるほか挽いて粉食に利用できる。Grainsでは刈り取った小麦束を脱穀して使う。 |
| `AMJC_RawWheat` | **小麦束（こむぎたば）。** 穂と茎を付けたまま収穫した小麦。未脱穀のままでは食べられず、脱穀によって小麦穀粒になる。 |
| `AMJC_WheatFlour` | **小麦粉（こむぎこ）。** 小麦穀粒を石臼で挽いた粉。Grainsでは餺飥を作るために使う。 |
| `AMJC_ManualMillstone` | **石臼（いしうす）。** 手で穀粒を挽いて粉にする石製の道具。Grainsでは小麦・蕎麦・雑穀の製粉に使用する。 |

### 加工・粉食Recipe（入出力を現行XMLと一致させる案）

| Recipe | description候補 | jobString候補 |
|---|---|---|
| `AMJC_MillWheat` | 脱穀した小麦穀粒10個を挽いて、小麦粉10個にする。 | 小麦を製粉している。 |
| `AMJC_MillBuckwheat` | 殻を取ったソバ穀粒10個を挽いて、蕎麦粉10個にする。 | 蕎麦を製粉している。 |
| `AMJC_MillMillet` | 雑穀10個を挽いて、雑穀粉10個にする。 | 雑穀を製粉している。 |
| `AMJC_CookHoutou` | 小麦粉から餺飥を1個調理する。 | 餺飥を調理している。 |
| `AMJC_CookSobagaki` | 蕎麦粉からそばがきを1個調理する。 | そばがきを調理している。 |
| `AMJC_CookMilletDumplings` | 雑穀粉から雑穀団子を1個調理する。 | 雑穀団子を調理している。 |

粉食Recipeは**Nutrition 0.5相当の粉**を要求する（粉1個のNutritionは0.05）。上表の製粉数量と混同しない。

### 既存Plant和訳の次回レビュー候補

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

## 4. 反映ゲート

1. 現行の**表示上の事実誤認**（MOなしでの大麦研究必須、非MOでの藁生成、未実装料理への誘導等）は史実の新主張を加えずに日本語DefInjectedを訂正。
2. 本書の§2は**未承認の日本語案**。本番のThingDef/RecipeDef descriptionやjobStringと英語原文はまだ変更しない。
3. 作者が日本語を確認・承認した後、DefInjectedと英語原文を意味・段落構造に合わせ、DefName/ロード条件/翻訳キーを静的テストで照合する。
4. 最後にVanilla、Vanilla+CCTO、MO、MO+CCTOで実際の表示・言語切替・ERROR 0を確認する。

**監査完成は、説明文の正式承認・英訳完成・実機UI表示確認を意味しない。**
