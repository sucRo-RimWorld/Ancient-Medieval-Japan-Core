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

## 2026-10-08 単体用仮画像の分離（MO復元方針は下記の作者指示で廃止）

共有Defの4パスをMO以外の開発用参照へ変更し、既存のMO条件付き `MedievalOverhaul_StageA_Base.xml` に4つのReplaceを追加した。MO導入時の明示Def契約38件は画像設定も含めて従来と一致する。これは**参照の条件分離**であり、専用Production画像の完成ではない。

| Def / 状態 | MOなし | MOあり |
|---|---|---|
| 大麦・成熟 | `Things/Plants/FullGrown/AMJC_Awa` | 従来のMO WheatPlant |
| 大麦・未成熟 | `Things/Plants/Immature/AMJC_Awa` | 従来のMO WheatPlant |
| 脱穀場所 | `Things/Building/Production/TableStonecutter` | 従来のMO StonecuttingSpot |
| 脱穀台 | `Things/Building/Production/TableStonecutter` | 従来のMO Millstone |

AMJ植物画像は既存PNGファミリーをそのまま参照する。設備は既存のBase手動石臼と同じVanilla仮参照を採用し、既存の方向・描画サイズ等を保持する。両設備は同じ仮画像となり、建物サイズに合う見た目や方向・マスクの実描画は未確認。専用画の制作と実機確認を公開前ゲートに残す。

Base境界検証は既知のMO4パス再侵入を拒否し、大麦の既存AMJ PNGファミリーの存在も確認する。MO画像復元の欠落は旧38契約照合で拒否する。未知の第三者画像パス・Vanilla全在庫・継承後の全参照・実際のTextureロードまで網羅する検証ではない。新規画像生成・既存PNG変更はない。Production AboutのMO必須依存は引き続き維持する。

## 現行方針：MO併用時もAMJの画像設定を優先

作者の指示により、MO併用時に旧画像へ戻す4つのReplaceを削除した。**AMJ所有DefはMO有無にかかわらずAMJが選んだ共有画像設定を使う。** 現在の大麦成熟・未成熟は既存AMJアワ、脱穀場所・脱穀台はAMJが選んだVanilla石切台の仮参照。AMJ専用設備画像が完成したという意味ではない。今後の専用画像差し替えも共有Def側で行う。

前節の表の「MOあり」列は現在すべて「MOなし」列と同じ参照となる。MO画像への復元Patch、復元漏れを拒否する旧テストは廃止した。数値・工程・研究・材料・Straw・供給元・DefName・packageIdは変更しない。

旧38契約の履歴fixtureは書き換えず、**作者が変更を指示した3Defの4パスだけ**を検証用コピーで旧値に正規化して歴史的ハッシュと照合する。その前にBase/MO両projectionでAMJ側の現行4パスを明示検証する。画像以外の変更は正規化対象にせず、対象設備の耐久値変更も回帰テストで拒否する。「旧38契約完全一致」ではなく「承認済み4画像パス以外は旧38契約を保持」と報告する。

MO併用時の旧画像上書きを再追加する変更も検証で拒否する。実ゲームの他ModとのPatch競合・ロード順・描画は未検証。専用画像、実機・セーブ等のゲートとAboutのMO必須指定は維持する。
