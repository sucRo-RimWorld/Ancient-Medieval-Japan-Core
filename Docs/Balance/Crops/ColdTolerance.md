# AMJC作物の耐寒データ

## 責務と正本

AMJC固有作物の耐寒データは、**AMJCが所有・管理する**。CCTOは固定枯死・休眠・情報表示を提供するフレームワークとして利用し、CCTO側にはAMJC固有作物の数値表・DefName一覧・互換XMLを置かない。

- 最低成長温度はAMJC自身のPlantDefに設定する。
- 固定枯死温度・休眠設定は、CCTOが有効な場合だけAMJC側の互換XMLから `CropColdToleranceOverhaul.ColdToleranceExtension` として付与する。
- CCTOは任意依存のまま。未導入時もAMJCの栽培・加工は成立し、低温枯死には元のRimWorldの挙動を使う。
- CCTOが管理するVanilla/MO作物と、AMJC固有作物を区別する。MO小麦 `DankPyon_Plant_Wheat` の温度データはCCTO側のMO対応を利用する。
- 将来AMJC作物を追加・調整する際も、数値・根拠・互換XML・検証はAMJC側で更新する。CCTOには汎用APIに関する変更だけを依頼する。

本資料はCCTOの `Docs/Design.md` / `Docs/ImplementationTable.md` に置かれていたAMJC作物のデータを移管した正本であり、移管に伴う数値変更はない。Stage Aの栽培全体は [Docs/Design.md §4.2.1](../../Design.md) と整合させる。値は現実の耐寒性を参考にした**ゲーム内バランス値**であり、現実の測定値そのものではない。

## 確定した固定枯死・休眠値

最低成長温度は `minGrowthTemperature`、固定枯死温度は `coldDeathTemperature` に対応する。休眠のみの作物には `coldDormancy=true` を設定し、固定枯死温度を設定しない。

| Crop | Minimum growth temperature | Fixed death threshold / behavior |
|---|---:|---:|
| Barley | 0°C | -8°C |
| Daikon | 0°C | -5°C |
| Buckwheat | 5°C | -2°C |
| Barnyard millet | 5°C | -4°C |
| Hemp | 5°C | -6°C |
| Kudzu | 5°C | cold dormancy |
| Foxtail millet | 8°C | -4°C |
| Proso millet | 8°C | -3°C |
| Adzuki bean | 8°C | -1°C |
| Soybean | 8°C | -3°C |
| Perilla | 8°C | -1°C |
| Rice | 10°C | -1°C |
| Taro | 10°C | -1°C |

クズ（Kudzu）は低温で地上部が休眠し、根株が生存して回復できる作物として扱う。休眠は最低成長温度未満で始まり、固定枯死の判定は閾値未満（strict `<`）で行う。閾値ちょうどでは枯死しない。

現時点でPlantDefとCCTO互換XMLが実装されているAMJC作物はアワ `AMJC_Plant_FoxtailMillet_Awa`。最低成長8℃は `Defs/ThingDefs_Plants/Plants_StageA.xml`、固定枯死-4℃は `Patches/Compatibility/CCTO_StageA.xml` が持つ。他の行は今後の作物実装で利用する設計値であり、対応済みの作物一覧ではない。未実装作物のDefNameを先行確定したり、存在しないDefを対象とするPatchを追加したりしない。

## 保存する候補範囲（現在は未使用）

以下は従来のバランス検討で保存していた候補範囲。現在のXML/APIは固定値を利用し、この範囲を自動的に読み込まない。将来CCTOに決定論的な個体差モードが実装され、AMJCで採用を判断した場合の再検討資料として残す。

| Crop | Minimum growth temperature | Candidate death range / behavior |
|---|---:|---:|
| Barley | 0°C | -9 to -7°C |
| Daikon | 0°C | -6 to -4°C |
| Buckwheat | 5°C | -3 to -1°C |
| Barnyard millet | 5°C | -5 to -3°C |
| Hemp | 5°C | -7 to -5°C |
| Kudzu | 5°C | cold dormancy |
| Foxtail millet | 8°C | -4 to -3°C |
| Proso millet | 8°C | -3 to -2°C |
| Adzuki bean | 8°C | -2 to 0°C |
| Soybean | 8°C | -4 to -2°C |
| Perilla | 8°C | -2 to 0°C |
| Rice | 10°C | -1 to 0°C |
| Taro | 10°C | -1 to 0°C |
