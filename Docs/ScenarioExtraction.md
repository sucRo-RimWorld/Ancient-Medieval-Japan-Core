# 開始シナリオの分離と移行

2026-10-07。所有方針の正本は `Docs/Design.md` の「開始シナリオの独立Mod化」。
独立シナリオModはVanilla単独で成立させ、GrainsとMOは任意互換とする。
ここでは移行対象と、分離後のパッケージを検証する再現可能な試作を定義する。
正式なMod名・packageId・専用リポジトリは未確定。公開・現行配布物の差替えは行わない。

## 移行対象

機械可読台帳は `Tests/Fixtures/ScenarioExtraction/manifest.json`。

| 対象 | 維持する識別子 | 現在の正本 |
|---|---|---|
| ScenarioDef | `AMJC_NewVillage` | `Defs/Scenarios/Scenarios_NewVillage.xml` |
| 開始用FactionDef | `AMJC_PlayerVillage` | `Defs/FactionDefs/Factions_PlayerVillage.xml` |
| 開始用PawnKindDef | `AMJC_Villager` | `Defs/PawnKindDefs/PawnKinds_Villager.xml` |
| 英語・日本語の開始ダイアログ | `AMJC_GameStart_NewVillage` | 両言語の `Keyed/AMJC_Scenarios.xml` |
| 日本語Def翻訳3ファイル | 上記3つのDefのフィールド | `DefInjected/ScenarioDef`、`FactionDef`、`PawnKindDef` |
| MO差分2操作 | Scenario全parts置換・PawnKind衣装タグ追加 | `Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_StageA_Base.xml` |

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

現行mainはまだ「更新していない現行Core」である。
生成試作は移行対応版を別に組み立てたもので、現行Coreとの併用を保証するものではない。
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
python Scripts/prepare_scenario_extraction.py --output <新規・リポジトリ外のフォルダ> --grains-package-id sucro.amj.grains.extractiontest --scenario-package-id sucro.amj.scenarios.extractiontest
```

`source-state.json` は入力ソースと生成ファイルのSHA-256、テストpackageId、試案の状態を記録する。
生成パッケージは本番セーブへ設置せず、隔離したSaveData・Mod構成で検証する。

静的テストは6構成で、明示XMLの重複、内部参照、BaseのMO漏出、開始物資、衣装、初期研究を確認する。
Grainsありの4構成は**全ての明示Def契約**を現行Base/MOと比較し、穀物側の変更を取り落とさない。
翻訳の原文バイトも維持する。負例は互換用領域のガード欠落、MOガード欠落、Patch順序逆転、
Grains物資の無条件ロード、未更新Coreとの重複、本番ID・既存出力の使用を検出する。

未検証の範囲はVanilla/MO継承・全クロスリファレンス・画像・ゲームloader・新規開始・旧セーブ読込。
試作のLegacyStartingScenarios領域は現行Workshop配布ルートではなく、正式移行時に
Workshop validatorの許可ルートと配布用アダプタも同時に更新・検証する。
本番Defは移動せず、既存8シナリオ／ERRORゲートを緩めない。
正式テスト移管ではNewVillageStepsとNewVillage Quickstartだけを新Mod所有へ切り出す。
GrainsのStage A Quickstartと環境／収穫／Billテストを巻き込まない。
新Modの4構成開始と旧セーブ／追加／削除のテストも、非表示だが描画を維持しERROR 0を必須とする。

次の実装段階は正式IDと専用保存先を確定し、この試作構造を本番へ適用して、テスト所有も切り替えること。
AboutのMO依存解除・旧互換用領域の削除・安全なMod差替えの案内は、対応する実機ゲートが通るまで行わない。
