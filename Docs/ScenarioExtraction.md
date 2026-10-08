# 開始シナリオの分離と移行

2026-10-07。所有方針の正本は `Docs/Design.md` の「開始シナリオの独立Mod化」。
独立シナリオModはVanilla単独で成立させ、GrainsとMOは任意互換とする。
ここでは本番の互換用領域、独立リポジトリとの所有者切替、再現可能な検証手順を定義する。
正式名は Ancient & Medieval Japan - Scenarios（略称AMJ - Scenarios）、packageIdは `sucro.ancientmedievaljapan.scenarios`。
作者指定の専用リポジトリは https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Scenarios 。
開発候補ソースを登録したが、Workshop公開・現行配布物の差替えは行わない。
Coreリポジトリは作者により https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Grains へ改名された。
本番packageId `sucro.ancientmedievaljapan.core` とAMJC DefNamesは維持する。

## 移行対象

機械可読台帳は `Tests/Fixtures/ScenarioExtraction/manifest.json`。
下表の3Def・5翻訳は独立Scenariosの同名相対パスを正本とし、Grainsは
`LegacyStartingScenarios/` 配下に従来開始・旧セーブ用の互換コピーを維持する。
台帳の `sourceRoot` はこのGrains互換コピーの入力位置を示す。

| 対象 | 維持する識別子 | Grains側の現行互換コピー（最終所有正本はScenarios） |
|---|---|---|
| ScenarioDef | `AMJC_NewVillage` | `LegacyStartingScenarios/Defs/Scenarios/Scenarios_NewVillage.xml` |
| 開始用FactionDef | `AMJC_PlayerVillage` | `LegacyStartingScenarios/Defs/FactionDefs/Factions_PlayerVillage.xml` |
| 開始用PawnKindDef | `AMJC_Villager` | `LegacyStartingScenarios/Defs/PawnKindDefs/PawnKinds_Villager.xml` |
| 英語・日本語の開始ダイアログ | `AMJC_GameStart_NewVillage` | `LegacyStartingScenarios/Languages/English/Keyed/AMJC_Scenarios.xml` と `LegacyStartingScenarios/Languages/Japanese/Keyed/AMJC_Scenarios.xml` |
| 日本語Def翻訳3ファイル | 上記3つのDefのフィールド | `LegacyStartingScenarios/Languages/Japanese/DefInjected/{ScenarioDef,FactionDef,PawnKindDef}/` |
| MO差分2操作 | Scenario全parts置換・PawnKind衣装タグ追加 | `LegacyStartingScenarios/Compatibility/MedievalOverhaul/Patches/StartingScenarios.xml`（独立Scenariosにも正式な所有ファイルあり） |

Factionはプレイヤー開始専用であり、NPC派閥を追加しない。
Scenario→Faction→PawnKind→Factionの参照を一組として移す。
5人／候補8人、Standing到着、Tribal背景、Medieval技術段階、Cloth衣装素材、
空の初期研究タグ・Techprintタグは維持する。DefNameとダイアログキーを新接頭辞へ改名しない。

穀物Def・レシピ・加工設備・CCTOデータはGrainsに残る。
MO互換ファイルは作物・素材・Straw・加工設備の操作と上記2操作を分割し、
Scenario関連操作を独立シナリオ側へ移す。全ファイルを新Modへ丸ごとコピーしない。

## 試作パッケージ

`Scripts/prepare_scenario_extraction.py` は本番ソースを変更せず、指定した新規フォルダへ
`Grains` と `StartingScenarios` を生成する。既存出力を上書きせず、リポジトリ内への出力も拒否する。
二つのpackageIdは呼出側から指定し、異なる `.extractiontest` 終端のテストIDだけを受け付ける。
本番IDの割当、Modsフォルダへの設置、プレイヤーのModsConfig編集、セーブ書換え、公開は行わない。

試作GrainsのAboutからMO必須依存を外すのは、分離構造のテスト用コピーだけである。
本番Aboutの依存解除ゲートを通過した意味にはならない。
独立シナリオのAboutはGrains/MOへ依存せず、両方へのloadAfterだけを持つ。

生成規則は以下とする。

1. Grainsの通常ロード領域から3Defと5翻訳ファイルを除き、`LegacyStartingScenarios` に互換用として置く。
2. 新シナリオModが無効なときだけ互換用領域をロードする。
3. 互換用MO PatchはMOが有効、かつ新シナリオModが無効なときだけロードする。
4. 新シナリオModが有効なら、3Def・翻訳・MO／Grains開始物資差分は新Modが提供する。
5. 新ModではMOのparts置換を先に適用し、その後Grainsの雑穀物資差分を適用する。
   逆順ではMOの全parts置換がGrains差分を消すため、順序も回帰条件とする。

`IfModActive` と `IfModNotActive` を同じloader項目に指定したときの条件はAND。
参照実装は固定コミットの
[ModLoadFolders.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/Verse/ModLoadFolders.cs) と
[LoadFolder.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/Verse/LoadFolder.cs)。
このコード参照と静的投影は、実際にインストールされたゲームでのloader検証を代替しない。

## 開始物資の試案

Grainsありの開始物資・MO研究・素材・衣装は、現行契約を順序も含めて維持する。
Grainsなしでは `AMJC_Millet 200` と `AMJC_RawMillet 100` を残せないため、
**試作用の候補としてRawRice 300** を置く。正式なバランス確定ではない。
加工後300穀粒の代替という数量上の候補であり、加工労働・貯蔵・実際の栄養・食べ方は同等と保証しない。
独立開始の実機比較で調整し、採用値を台帳・正本・テストへ同時反映する。

| 新シナリオModの構成 | 携行食 | 穀物候補／物資 | 初期研究 |
|---|---|---|---|
| Vanillaのみ | Pemmican 1080 | RawRice 300 | なし |
| Grains | Pemmican 1080 | Millet 200、RawMillet 100 | なし |
| MO | MO MealRations 60 | RawRice 300、MO素材差分 | Lumber／RusticFurniture／BasicCooking |
| Grains＋MO | MO MealRations 60 | Millet 200、RawMillet 100、MO素材差分 | 同上 |

その他の道具・医薬品・銀・布は現行Baseを維持する。
MOはWoodLog 200＋RawWood 200、IronIngot 30、鉄素材のナイフへ差替える。
穀物なしのBaseはWoodLog 400、Steel 30、鋼鉄素材のナイフ。
開始物資にMO・Grainsの参照を残すのは対応するModが有効なときだけとする。

## 旧セーブと所有者の切替

| 構成 | 3Defの所有者 | 検証状態 |
|---|---|---|
| 移行対応Grainsのみ | Grainsの互換用領域 | 静的投影で一意性・現行契約一致 |
| 独立シナリオのみ | 独立シナリオ | Vanilla／MOの参照範囲を静的検証 |
| 移行対応Grains＋独立シナリオ | 独立シナリオ | 互換用領域を無効化し、現行契約一致 |
| 更新していない現行Core＋独立シナリオ | 二重定義になる | 禁止する組合せ。負例で検出 |

Grains本番の通常領域から3Def・5翻訳を移動し、MO開始差分2操作を穀物パッチから分割した。
本番loaderは独立ScenarioのpackageId不在時だけ互換コピーを読み込む。
MO互換コピーにはMO有効条件とScenario不在条件の両方を付ける。
改修前のCore/Grainsは引き続き併用不可。改修後も実ゲーム／旧セーブ互換の実測は未完了。
正式移行ではCore/Grainsを先に移行対応版へ更新し、Grainsを維持したまま独立シナリオを追加する。

参照したゲームコードでは、保存済みFactionはFactionDefを、PawnはPawnKindDefを
`Scribe_Defs` で参照し、Scenarioのparts・playerFactionは深いシリアライズで保存する。
[調査用Faction.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/RimWorld/Faction.cs)、
[Pawn.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/Verse/Pawn.cs)、
[Scenario.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/RimWorld/Scenario.cs)。
したがって、保存に現れる同じ名前・同じDef型の提供を維持する方針とする。
これは移行設計の根拠であり、旧セーブ読込成功の実測ではない。

- 新しいScenario開始物資・研究を、既存セーブへ再配布・再付与しない。
- 独立シナリオだけでは、旧セーブ中のAMJC作物・加工品・設備等を提供できない。
  旧Core全体を新シナリオModだけで置き換える手順にはしない。
- 新シナリオを外してGrainsだけを残す場合も、互換用3Defがあることだけでは安全な削除と保証しない。
- MOの既存アイテムやポーン等を含むセーブからMOを外す安全性は、この分離で解決しない。
- packageId差分に伴うMod構成警告、セーブ再保存、既存Scenario parts内の参照、
  ワールドFaction・開始ポーン・死人・他マップの参照は実機移行テストで確認する。

## 再現と検証

Python 3.9以降、標準ライブラリだけで実行する。

```text
python Tests/test_scenario_extraction.py
python Tests/validate_scenario_pair.py --scenario-root <独立Scenariosリポジトリ>
python Scripts/prepare_scenario_extraction.py --output <新規・リポジトリ外のフォルダ> --grains-package-id sucro.amj.grains.extractiontest --scenario-package-id sucro.amj.scenarios.extractiontest
```

`source-state.json` は入力ソースと生成ファイルのSHA-256、テストpackageId、試案の状態を記録する。
生成パッケージは本番セーブへ設置せず、隔離したSaveData・Mod構成で検証する。

静的テストは6構成で、明示XMLの重複、内部参照、BaseのMO漏出、開始物資、衣装、初期研究を確認する。
Grainsありの4構成は**全ての明示Def契約**を現行Base/MOと比較し、穀物側の変更を取り落とさない。
翻訳の原文バイトも維持する。負例は互換用領域のガード欠落、MOガード欠落、Patch順序逆転、
Grains物資の無条件ロード、未更新Coreとの重複、本番ID・既存出力の使用を検出する。

未検証の範囲はVanilla/MO継承・全クロスリファレンス・画像・ゲームloader・新規開始・旧セーブ読込。
LegacyStartingScenariosは本番配布対象であり、Workshop validatorがDef・翻訳・MO Patchを許可する。
実際のgit archiveと.rimignoreの一致を確認し、通常／fixtureテスト配置にもこの領域をコピーする。
fixtureのMO条件置換は穀物・旧開始の2項目へ適用し、Scenario不在条件を維持する。
CIは独立Scenariosのレビュー済みコミット `cbd5e313f9cb0871f7227e447d3faa7497fd962e` を別checkoutし、
本番の二つのソースで6構成の一意性・全明示契約一致を確認する。試作生成だけの検証にしない。
NewVillageStepsとNewVillage QuickstartをScenariosへ移管し、4構成×3シナリオのソースと隔離ランナーを用意した。
Grainsの通常4構成は穀物専用6件。LegacyVillageStepsとAmjLegacyVillageQuickstartは旧fixture8件の互換検証へ残す。
旧38契約とERRORゲートは維持し、通常Grainsの専用Scenario存在要件は外した。
GrainsのStage A Quickstartと環境／収穫／Billテストを巻き込まない。
新Modの4構成開始と旧セーブ／追加／削除のテストも、非表示だが描画を維持しERROR 0を必須とする。

専用リポジトリに3Def・5翻訳・任意MO/Grainsパッチ・静的テストを登録済み。
独立候補のGrains互換は現行packageIdを参照し、リポジトリ名をMod条件には使わない。
Grains本番の3Def・翻訳は条件付き互換領域へ移動済み。
実行時テストの所有・起動配線はScenariosへ移管済み。手順とコピー側のprovider別名対応は
Scenarios `Docs/RuntimeTesting.md` が正本。配置／設定生成の静的・PowerShellテストは実ゲーム開始成功ではない。
次はゲーム環境で4構成をコンパイル・実行し、旧セーブ・追加・削除の自動検証を実装すること。
AboutのMO依存解除・旧互換用領域の削除・安全なMod差替えの案内は、対応する実機ゲートが通るまで行わない。
