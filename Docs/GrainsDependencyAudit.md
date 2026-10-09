# Grains MO依存監査（2026-10-07）

対象はGrains main `644c2c9c60e7fa695d4b50f4aee16eae58b9835c` のProduction XMLと画像参照。所有境界の正本は [`Design.md`](Design.md)、実機検証の正本は [`GrainsProfileTesting.md`](GrainsProfileTesting.md)。Scenariosの静的検証・CIに問題が検出されていないため、作者の指示により追加のセーブ実行アダプター作業を保留し、Grains監査へ戻った。

## 監査時点の結論（以下の実装追記で更新）

**MOのDef識別子・クラス参照はBaseから分離済みだが、3Defの4画像パスがMO提供画像に依存している。Grains単独動作・公開準備の完了ではない。** Production AboutのMO必須依存は維持する。packageId `sucro.ancientmedievaljapan.core` と既存AMJC DefNameも維持する。

| 対象 | 確認結果 | 残る条件 |
|---|---|---|
| Base XMLのMO識別子・クラス | `DankPyon_` / `MedievalOverhaul.` の要素・属性参照なし | Vanilla継承・全Def解決は実ゲーム未検証 |
| MO互換 | 条件付きルートへ分離。旧38明示Def契約を保持 | 実ゲームのPatch・Bill・描画・ERRORゲート |
| 小麦・粉・石臼の供給 | MO不在のフォールバックとMO時の既存供給元を静的検証 | 4構成の実際のロード・工程実行 |
| Straw・研究・材料 | BaseのMO参照を除去、MO互換のみで再接続 | 継承後の実際の値・既存セーブ |
| 画像 | 下表のMO提供4パスを共有Defから無条件参照 | Grains所有画像への置換と全表示状態の検証 |
| About | MO必須依存が残る | 画像・実機・セーブ等のリリースゲート完了後に変更 |
| シナリオ | Scenariosへ物理分離済み。Grains旧コピーはScenarios不在時のみ | 旧セーブ・追加・削除・再保存の実機検証 |

## 監査時点のMO画像の残存依存

確認資料は作者提供 `02-3219596926.zip`。そのAboutはMO **1.6.2.2**、ZIP SHA-256は `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`。以下のパスの画像がMOアーカイブ内に存在し、GrainsのTexturesには同じパスの供給がない。Vanilla全画像の在庫は今回与えられておらず、全プロバイダーの網羅証明ではない。

| Grains Def / 要素 | 参照パス（`Textures/`以下） | MO内で確認した状態 |
|---|---|---|
| `AMJC_Plant_Barley` / `graphicData/texPath` | `Things/Plants/FullGrown/WheatPlant` | `PlantWheat_Mature.png` |
| `AMJC_Plant_Barley` / `plant/immatureGraphicPath` | `Things/Plants/Immature/WheatPlant` | `PlantWheat_Immature.png` |
| `AMJC_GrainProcessingSpot` / `graphicData/texPath` | `Things/Building/Production/StonecuttingSpot` | north/east/south/west画像と各マスク |
| `AMJC_GrainProcessingTable` / `graphicData/texPath` | `Things/Building/Production/Millstone` | east/south画像と各マスク |

参照元は `Defs/ThingDefs_Plants/Plants_StageA.xml` と `Defs/ThingDefs_Buildings/Buildings_GrainProcessing.xml`。いずれも共有ルートにあり、MO不在時にも読み込まれる。`DankPyon_` を含まない汎用パスなので、Def識別子の検査では検出できない。従来の「MO仮画像3件」は**3Def**として正しいが、植物の成熟・未成熟を分けると**4パス**になる。

MO画像の存在だけから再配布権限を推定しない。MO画像をコピーして依存解消とはしない。今後はGrains所有パスへ差し替え、植物の成熟・未成熟、設備の方向・マスクを実際のGraphic設定に合わせて用意する。新規画像生成は今回実施していない。

Base小麦の既存アワ画像、粉類の既存雑穀画像、手動石臼・粉食のVanilla仮画像も完成画の扱いにはしない。PNG構造検査の合格は、texPathの解決や方向・表示状態、画風の完成を証明しない。

## 検証の読み方と次の単位

`Tests/validate_grains_base.py` はBase XMLの識別子・クラス参照、条件付き互換、旧38契約を検証する。出力を「MO identifier/class references 0」へ限定し、画像と実ゲームは対象外と明記した。`test_grains_chain.py`、`test_grains_environment.py`、`test_scenario_extraction.py` は工程・環境・分離の静的回帰検証である。

本監査で選定した単位は上記3Defの画像依存解消（下記の仮参照分離を実装済み）。専用画像制作・レビュー後、4構成（Vanilla / MO / CCTO / MO+CCTO）をGrainsの6穀物ケースでコンパイル・実行し、描画・Bill実行・ERRORを確認する。旧セーブでのMO削除安全性は独立した検証が必要。Scenariosの実開始・旧セーブ試験はScenarios所有の未完了ゲートとして残す。

このクラウド環境ではRimWorld本体・Managed assembly・実セーブがないため、C#コンパイル、ゲーム実行、保存移行は検証していない。静的検証を理由にProductionのMO依存や公開メタデータを変更しない。

## 現行方針：MO併用時もAMJGの所有設定を優先（2026-10-09）

**MO有無にかかわらず、AMJG所有Defの画像・研究・加工台建材はGrainsの確定設定を維持する。** 大麦の成熟・未成熟画像は既存AMJアワの仮画像、脱穀場所・加工台はAMJG側が選択したVanilla石切台の仮画像。大麦は研究不要、`AMJC_GrainProcessingTable` は研究不要かつ Steel 30。これらのMO側旧画像・`DankPyon_BasicAgriculture`・`DankPyon_IronIngot` への復元Patchは廃止した。完成画像や実機表示のPASSを意味しない。

MO提供の小麦Plant／RawWheat／Flour／MillstoneはMO併用時の実Def供給元として引き続き利用するが、Grainsが責務を持つ生育バランス・脱穀工程・副産物はGrainsの条件付きPatchを優先する。MO石臼の研究制限除去、MOの素材カテゴリ追加、脱穀時のStraw接続など、重複機能を増やさないための互換は維持する。MO提供の小麦Plantが元から持つ農業研究条件はそのままとし、AMJG所有の大麦には伝播させない。

旧38件の固定履歴fixtureは書き換えない。静的検証では作者承認済みの **4画像パス＋3旧MO研究・建材上書き** のみ検証用コピーへ過去値を復元し、その他すべての履歴契約を照合する。現在のBase/MO両projectionは7項目でAMJG優先を直接検証し、旧MO上書きを再導入する負例テストを実装する。履歴上の旧MO優先表と旧PatchはGit履歴に保管し、現行仕様として参照しない。

Production `About.xml` のMO必須依存は**別の配布・旧セーブ検証ゲート**により現時点では維持する。この依存宣言はMO併用時の設定優先順位を意味しない。実RimWorldでのロード後優先順位・他Mod競合・旧セーブ・専用画像の検証は別途必要。
