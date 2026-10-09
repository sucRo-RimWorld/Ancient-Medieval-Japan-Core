> Workshop common sources moved to Project on 2026-10-08. Workshop entries below retain recovery provenance; their authoritative bytes now live at the linked Project paths.

# Core 元画像保存対象の棚卸し

確認日: 2026-10-07 JST。確認基準: `main` の `957bdd5`。


## 現行の穀類植物・束原本（2026-10-10統合画像）

**19表示状態＝成熟7・未熟7・収穫束5。** この19点は旧Core画像14点の棚卸し件数と別集計。Grainsの本番 `Textures/` およびDef参照はPR #20（`cd52a3d`）で統合済み。今回、既存3点を照合し、不足16点の高解像度制作用原本を同一Git blobで `Art/Sources/` に追加した。
採用済みの既存原本は上書きせず、アワ・ヒエ・キビ未熟の新しい輪郭調整版を別名で保存。最新の未熟7原本は生成原本の輪郭色を正規化した高解像度版で、生成直後の完全な原本は `Art/Candidates/ImmatureUpright-20261009/Sources/` に保持。256px本番はさらに書き出し後の輪郭処理を経ており、元原本の単純縮小とバイト一致するとは主張しない。
**正本対応表：** [Docs/References/GrainsCropSourceManifest.json](../../Docs/References/GrainsCropSourceManifest.json)。原本Git blob SHA、元候補、ゲーム出力パスを固定。検証: `Tests/test_grains_art_source_archive.py`。実ゲームでの描画・ロード後競合確認は未実施。

| 作物 | 段階 | 原本（Art/Sources） |
| --- | --- | --- |
| Awa | immature | `Things/Plants/Immature/AMJC_Awa_Simple/AMJC_Awa_Immature_Outline20261009.png` |
| Hie | immature | `Things/Plants/Immature/AMJC_Hie_Simple/AMJC_Hie_Immature_Outline20261009.png` |
| Kibi | immature | `Things/Plants/Immature/AMJC_Kibi_Simple/AMJC_Kibi_Immature_Outline20261009.png` |
| Soba | immature | `Things/Plants/Immature/AMJC_Soba_Simple/AMJC_Soba_Immature.png` |
| Barley | immature | `Things/Plants/Immature/AMJC_Barley_Simple/AMJC_Barley_Immature.png` |
| Wheat | immature | `Things/Plants/Immature/AMJC_Wheat_Simple/AMJC_Wheat_Immature.png` |
| Rice | immature | `Things/Plants/Immature/AMJC_Rice_Simple/AMJC_Rice_Immature.png` |
| Awa | mature | `Things/Plants/FullGrown/AMJC_Awa_Simple/AMJC_Awa_Mature.png` |
| Hie | mature | `Things/Plants/FullGrown/AMJC_Hie_Simple/AMJC_Hie_Mature.png` |
| Kibi | mature | `Things/Plants/FullGrown/AMJC_Kibi_Simple/AMJC_Kibi_Mature.png` |
| Soba | mature | `Things/Plants/FullGrown/AMJC_Soba_Simple/AMJC_Soba_Mature.png` |
| Barley | mature | `Things/Plants/FullGrown/AMJC_Barley_Simple/AMJC_Barley_Mature.png` |
| Wheat | mature | `Things/Plants/FullGrown/AMJC_Wheat_Simple/AMJC_Wheat_Mature.png` |
| Rice | mature | `Things/Plants/FullGrown/AMJC_Rice_Simple/AMJC_Rice_Mature.png` |
| Millet | sheaf | `Things/Item/Resource/AMJC_Millet/MixedMilletSheafDense/MixedMilletSheafDense.png` |
| Soba | sheaf | `Things/Item/Resource/AMJC_Buckwheat/RawBuckwheatDense/RawBuckwheatDense.png` |
| Barley | sheaf | `Things/Item/Resource/AMJC_Barley/RawBarleyDense/RawBarleyDense.png` |
| Wheat | sheaf | `Things/Item/Resource/AMJC_Wheat/RawWheatDense/RawWheatDense.png` |
| Rice | sheaf | `Things/Item/Resource/AMJC_Rice/RiceSheafDense/RiceSheafDense.png` |

---

## 旧Core画像の回収棚卸し（2026-10-07時点）
## 件数と数え方

| 範囲 | 保存対象点数 | Art/Sources 保存済み | 未保存・要照合 |
| --- | ---: | ---: | ---: |
| ゲーム用の植物・アイテム画像 | 14 | 7 | 7 |
| 共通の枡・Workshop表紙素材 | 5 | 5 | 0 |
| 合計 | 19 | 12 | 7 |

- ゲーム用 `Textures/` は26 PNG。SHA-256でまとめると14種類で、6アイテム群の `_a/_b/_c` は各群で同一バイト。各群は1点と数える。共有Defからの参照数は加算しない。
- 「19点」は保存対象の種類・役割の数。「7点」は元画像の照合・回収が残る対象数であり、回収可能な元ファイル7枚が確定したという意味ではない。
- 雑穀の殻付き・精製後は同じ歴史的素材シートの候補に含まれる。そのシートが両画像の正本と確定すれば、2対象を1ファイルで保存できる。したがって現一覧の未保存対象は、全対象の元画像が回収できる場合、共通シートを使えば6ファイル、個別の正本を使えば7ファイルが目安。未回収や別の共有元が判明した場合は再集計する。
- 空枡の `.xcf` は保存済みの編集ファイル1件として別記し、同じ枡を画像2点とは数えない。SVGはベクタ元画像として1点。
- 初回は棚卸しのみ。その後、G08ソバ未熟株、G13殻付きソバ、W02承認済みCore表紙参照、W03表紙共通ラスター、W04表紙可変マスク、G03ヒエ成熟株、G04ヒエ未熟株、G05キビ成熟株を1枚ずつ照合・保存し、件数を更新した。新しい画像の生成・本番テクスチャ変更は行っていない。

## ゲーム用14種類

以下の本番パスは `Textures/` からの相対パス。アイテムのディレクトリは `_a/_b/_c` の3ファイルをまとめて示す。

| ID | 画像 | 本番パス | 元画像保存状態 | 候補・次の確認 | 作り直しとの関係 |
| --- | --- | --- | --- | --- | --- |
| G01 | アワ成熟株 | `Things/Plants/FullGrown/AMJC_Awa/AMJC_Awa_Mature.png` | 未保存・採用版未確認 | 太い輪郭への更新があるため初期版を採用しない。`AMJ-004` / `AMJ-005` の最終承認と候補を照合 | 再制作対象と断定しない |
| G02 | アワ未熟株 | `Things/Plants/Immature/AMJC_Awa/AMJC_Awa_Immature.png` | 未保存・縮小前の正本未確認 | `AMJC_Awa_Immature.png` は実測256×256。高解像度元画像扱いにしない | 同上 |
| G03 | ヒエ成熟株 | `Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png` | 保存済み | `Art/Sources/Things/Plants/FullGrown/AMJC_Hie/AMJC_Hie_Mature.png`、1254×1254 RGBA。`ヒエの穂が揺れる可愛い植物アイコン.png` をAMJ-016採用記録・現本番と照合。SHA-256 `58bc4a98f4557d5df112f97c2094d7cbb5681ea8f46c36246064b10da3c573db` | 保存完了 |
| G04 | ヒエ未熟株 | `Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png` | 保存済み | `Art/Sources/Things/Plants/Immature/AMJC_Hie/AMJC_Hie_Immature.png`、1254×1254 RGBA。`直立したヒエの植物アイコン.png` をAMJ-016承認・修復履歴・現本番と照合。SHA-256 `1d1d8bd67d1bd2c28cbb3e783dab043d07f5e6877eab053a7df869b8ad703538` | 保存完了 |
| G05 | キビ成熟株 | `Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png` | 保存済み | `Art/Sources/Things/Plants/FullGrown/AMJC_Kibi/AMJC_Kibi_Mature.png`、1254×1254 RGBA。`黄金のキビ穂アイコン.png` をAMJ-016承認・修復履歴・現本番と照合。SHA-256 `53af394e4bcef8b9f45fe97237a05c9c7606fef71bdacc3e743fc64644d831e2` | 保存完了 |
| G06 | キビ未熟株 | `Things/Plants/Immature/AMJC_Kibi/AMJC_Kibi_Immature.png` | 未保存・縮小前の正本未確認 | `AMJC_Kibi_Immature.png` は実測256×256。元の生成・編集入力を確認 | 同上 |
| G07 | ソバ成熟株 | `Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png` | 保存済み | `Art/Sources/Things/Plants/FullGrown/AMJC_Soba/AMJC_Soba_Mature.png`、1247×1261。保存コミット `575308e842b160b44b25cfd4b3ec0065edcd3f56` | 保存完了 |
| G08 | ソバ未熟株 | `Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png` | 保存済み | `Art/Sources/Things/Plants/Immature/AMJC_Soba/AMJC_Soba_Immature.png`、1448×1086。三株構成の `黒背景の芽吹く植物アイコン(1).png` を記録・目視照合。SHA-256 `194e4b67ea25ab77d73a07f973bbbf7bfaba4ededbda9eb1366c08bc7a2e75b4` | 保存完了 |
| G09 | 雑穀束 | `Things/Item/Resource/AMJC_Millet/RawMillet/` | 未保存・最終採用版未確認 | `穀物の束の収穫アイコン.png` は候補。`AMJ-005` の後の太い輪郭版と照合。旧 loose-grain 図案は採用しない | 束と脱穀後画像を区別 |
| G10 | 殻付き雑穀 | `Things/Item/Resource/AMJC_Millet/MilletInHull/` | 未保存・共通シート候補あり | `中世風ミレット素材アイコンセット.png`、実測1448×1086。G11と共有する元シートか照合 | 作者指示の脱穀後再制作対象。旧正本の保存とは別の状態 |
| G11 | 精製後雑穀 | `Things/Item/Resource/AMJC_Millet/Millet/` | 未保存・共通シート候補あり | 同じシート内の淡色粒。G10と共有する元シートか照合 | 同上 |
| G12 | ソバ束 | `Things/Item/Resource/AMJC_Buckwheat/RawBuckwheat/` | 未保存・最終採用版未確認 | `素朴なハーブの束アイコン.png` と後の `束ねられた種花のブーケ.png` 等を照合。直近の差替えと縦横比修正の正本を優先 | 初期統合版を自動採用しない |
| G13 | 殻付きソバ | `Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/` | 保存済み | `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/BuckwheatInHull/BuckwheatInHull.png`、1254×1254 RGBA。登録正本のSHA-256 `cd1dce01d4847289edef107d513cd73de10e8291d6d0acb421bd9c9aa672f6f6` と一致。LANCZOS縮小は本番a/b/cとRGBA差分0 | 保存完了 |
| G14 | 精製後ソバ | `Things/Item/Resource/AMJC_Buckwheat/Buckwheat/` | 保存済み | `Art/Sources/Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat.png`、1429×1100 | 人間が最終編集した正本 |

## 共通・表紙5点

| ID | 対象 | 状態 | 正本 / 保存先 |
| --- | --- | --- | --- |
| C01 | 現行空枡 | 保存済み | `Art/Sources/Shared/Containers/AMJ_Masu_Empty_Master.png`、1429×1100。隣の同名 `.xcf` も保存済み |
| W01 | Workshop表紙SVGテンプレート | 保存済み | [Art/Sources/Workshop/AMJ_WorkshopCover_Template.svg](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Art/Sources/Workshop/AMJ_WorkshopCover_Template.svg)。`Docs/References/` の参照コピーと重複加算しない |
| W02 | 承認済みCore表紙参照 | 保存済み | [Art/Sources/Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Art/Sources/Workshop/AMJ_WorkshopCover_Core_Approved_Reference.jpg)、960×540 RGB JPEG、92,308 bytes。登録SHA-256 `ef662e1eb2e399c594adfb6a4d594f1e2727559a73e380f312638b1bc8585658` 一致 |
| W03 | 表紙共通ラスター | 保存済み | [Art/Sources/Workshop/AMJ_WorkshopCover_CommonBase.png](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Art/Sources/Workshop/AMJ_WorkshopCover_CommonBase.png)、960×540 RGB PNG、149,866 bytes。登録SHA-256 `a738d175bf1997e95f02456843686f8d2d59571d47849e55d04a957707514362` 一致 |
| W04 | 表紙可変マスク | 保存済み | [Art/Sources/Workshop/AMJ_WorkshopCover_VariableMask.png](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Art/Sources/Workshop/AMJ_WorkshopCover_VariableMask.png)、960×540 L PNG、1,216 bytes。登録SHA-256 `e2bbf3547587eebafabc404f0adf3fdad7ffc29df84b0018b871af31c8689622` 一致 |

W02–W04は `Docs/References/AMJ_WorkshopCover_Manifest.md` と `Docs/GoldenPaths/WorkshopCoverPipeline.md` に登録された別ファイル。SVGの保存で置き換え済みと扱わない。`About/preview.png` は配布用画像として別途確認対象だが、この棚卸しでは表紙の追加正本1枚として加算しない。既存の表紙正本で生成元が説明できるかを回収時に確認する。

## 補助候補と対象外

次の2点は本体19点から分離する。前景パーツや校正参照の保存必要性を確認後、補助枠へ追加する。

| 対象 | 現在の扱い | 理由 |
| --- | --- | --- |
| `AMJ_Masu_Empty_Master_Upper.png` | 補助候補1点、Library現存確認 | 人間の前景合成用パーツ。保存済みXCFから同一の書き出しを再現できるか未確認。空枡本体と同一画像ではない |
| `AMJ_BoxedResource_LineHierarchy_Rice_Test.png` | 校正参照候補1点、Library現存確認 | 正式パイプラインの線階層校正用。承認済みの米本番アイコンではない |

比較シート、ゲーム画面、旧不採用試作、研究用マスク・診断画像、配布用縮小PNGの重複は元画像の回収件数に加算しない。既にGit内にあるグラフ・パレットSVG・診断用PNGに新たな移動は不要。借用するMO建物・大麦画像の原本はCoreが所有する元画像対象に含めない。Environment/CCTOや未来のAddonの画像は各所有リポジトリの棚卸しで扱う。

## 候補の識別情報

候補の存在は最終採用の証明ではない。以下の識別子は照合対象を固定するためのもの。

| 候補 | Library identity | 今回の確認 |
| --- | --- | --- |
| 雑穀共通シート | `libfile_cf10c90c239c8191b9b17c02851f0eac` | 1448×1086 RGBA。シートを実見し、殻付き・淡色の粒が同居。SHA-256 `cd5ccedde150cfd49151031609bf6cc54d84c1181504d8fcbe69947979860611` |
| アワ未熟候補 | `libfile_35cfa54468888191b1d0a4b6e31e71a4` | 実測256×256。縮小前の正本と認定しない |
| ヒエ未熟候補 | `libfile_58a9e15953248191955aebc1eeea34a9` | 実測256×256。同上 |
| キビ未熟候補 | `libfile_c169bab639f88191aeb7cc400e8743d8` | 実測256×256。同上 |
| ヒエ成熟正本 | `libfile_81f9f17fbb988191916144a698e3bfa5` | 実測1254×1254 RGBA、909,425 bytes。採用コミット・三本の黄金色の垂れ穂と葉/茎構成を現本番と照合。元バイト保存済み。歴史的配置・パレット書き出し手順の完全再現は未確認 |
| ヒエ未熟正本（旧G03候補） | `libfile_b626dec6725c8191bc318e25fa265b58` | `直立したヒエの植物アイコン.png`、実測1254×1254 RGBA、656,097 bytes。G03から除外後、G04の採用構成と一致する三本の緑色穂・葉・茎を照合。現本番は承認版のPNG修復で復元された最終化コミットのblobと一致。元バイト保存済み。歴史的パレット書き出しの完全再現は未確認 |
| キビ成熟正本 | `libfile_cd4a791d96048191bde27c7f903d5dd9` | `黄金のキビ穂アイコン.png`、実測1254×1254 RGBA、940,212 bytes。枝分かれした黄金色の穂・葉・茎を現本番と照合。本番は承認版のPNG修復で復元された最終化コミットのblobと一致。元バイト保存済み。歴史的パレット書き出しの完全再現は未確認 |
| ソバ未熟候補 / `(1)` | `libfile_9ec7d48ed7b8819187bd2d476617ae7e` / `libfile_3f5c688ff0088191b57c3583709cbf94` | 両方1448×1086 RGBAを実見。`(1)` の三株構成が本番と一致し保存済み。無印の追加株を含む別構成は除外。歴史的書き出し手順の完全再現は未確認 |
| 雑穀束候補 | `libfile_ea9499a650bc8191ae5d7beac47a0c6d` | 最終輪郭版の照合待ち |
| ソバ束の旧候補 / 後の候補 | `libfile_f0aec464d0f08191bda2ffe3df6d5c15` / `libfile_4156e957eed48191b6bcdab3b1f8b571` | 直近の最終採用・修正との照合待ち |
| 殻付きソバ正本 | `libfile_5a34c43373188191a48e3796290482af` | 実測1254×1254 RGBA、869,790 bytes。登録SHA-256一致、元バイトを保存済み。本番3画像との縮小後RGBA差分0 |
| Core表紙参照 | `libfile_f0ec7d3c94f88191ab304f0fbdb13946` | 実測960×540 RGB JPEG、92,308 bytes。登録ハッシュ一致・完全デコード確認、元バイトを保存済み |
| 表紙共通ラスター | `libfile_1730eee945f8819198690f7cb988c96c` | 実測960×540 RGB PNG、149,866 bytes。登録ハッシュ一致・PNG構造/完全デコード確認、元バイトを保存済み |
| 表紙可変マスク | `libfile_f831c30d1cac819192ed282dbf430698` | 実測960×540 L PNG、1,216 bytes。登録ハッシュ・編集可能領域一致、PNG構造/完全デコード確認、元バイトを保存済み |
| 空枡前景パーツ | `libfile_4bb3c4248cec8191beb2974b351329b6` | メタデータで現存確認 |
| 米の線階層校正参照 | `libfile_c9664515325881918040b202398a628e` | 同上 |

この時点で元画像が失われたと確定した対象はない。256px候補しか確認できなかった3対象のうちG04は高解像度正本を別途回収済み。G02/G06は引き続き原入力を探す。採用版が確定しない候補は移動しない。保存後はこの一覧の状態・件数とREADMEを更新し、作業進捗は `main:Docs/Coordination.md` に記録する。
