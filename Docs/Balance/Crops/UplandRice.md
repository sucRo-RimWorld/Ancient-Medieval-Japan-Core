# 陸稲（Vanilla Plant_Rice）バランス

## 所有と実装

GrainsはVanillaの `Plant_Rice` を削除・複製せず、**陸稲**としてPatchする。収穫物はVanilla `RawRice` をそのまま使う。

- 新しい陸稲PlantDef / 米ThingDefは追加しない。
- 普通の畑（`Ground`）で栽培する。Vanillaの `Hydroponic` sowTagは削除する。
- 水田、水管理、水稲Plant、田植え等は将来のRice Cultivationが所有する。
- Rice Cultivation + Grainsでは水稲の収穫後を `RawRice` またはその時点のGrains米加工経路へ合流させる。
- 米粉等の製粉物は具体的な用途が成立した場合だけGrainsで追加する。

## 採用値

| 項目 | 値 |
|---|---:|
| growDays | 8 |
| harvestYield | 20 |
| fertilityMin | 0.7 |
| fertilitySensitivity | 0.9 |
| minGrowthTemperature | 10℃ |
| minOptimalGrowthTemperature | 20℃ |
| maxOptimalGrowthTemperature | 35℃ |
| maxGrowthTemperature | 42℃ |
| sowMinSkill | 0（Vanilla継承） |
| harvestedThingDef | `RawRice` |
| sowTags | `Ground` のみ |

役割は**温暖・肥沃・長い生育期間に向く畑作の米**とする。ソバ・キビの痩せ地／短期、ヒエ・大麦の寒冷、小麦の肥沃地・粉食という既存役割を奪わない。

27代表条件では陸稲は2条件だけ最大収量になる。

- fertility 1.4 / 20℃ / 20日: 60
- fertility 1.4 / 30℃ / 20日: 60

この2条件では小麦56を上回るが、標準肥沃度ではキビ・大麦等が引き続き優位になる。七穀すべてが少なくとも1条件で最大となることを回帰条件にする。

## CCTOとの境界

Grains自身が `Plant_Rice.minGrowthTemperature=10` を設定し、CCTO未導入でも陸稲の温度特性を成立させる。

CCTOは既存のVanilla `Plant_Rice` 対応で固定枯死-1℃を付与する。Grainsは陸稲用の `ColdToleranceExtension` を重複追加しない。CCTO側も最低生育10℃へ設定するため、併用時の最終値は同じになる。

## 根拠と抽象化

- 農研機構は、水田で育てる稲を水稲、畑で育てる稲を陸稲とし、同面積の収量は水稲より低いと説明している。AMJではこの差を「水田設備不要だが、将来の水稲より生産性を低くする」という役割差へ使う。現代の収量比をゲーム数値へ直接コピーしない。
  - https://www.naro.go.jp/laboratory/tarc/rice_faq/growing/025127.html
- 日本の陸稲の呼称についての歴史研究では、中世以降に多数の別名が全国で用いられたことが整理されている。ゲーム上の表示名は曖昧さを避けて「陸稲」とする。
  - https://cir.nii.ac.jp/crid/1050578283038184576

## 日本語説明文のレビュー用草案

**未承認。Productionのdescriptionへはまだ入れない。英訳もしない。**

> 陸稲（りくとう）。水田ではなく畑で育てる稲。おかぼ、畑稲などの呼び名があり、日本では時代や地域によって多様な名称が用いられてきた。\n\n水田を造成せず栽培できる一方、一般に水稲より収量は低い。AMJでは温暖で肥沃な畑に向く米作として表現する。

歴史記述は `Docs/HistoricalDescriptionGuidelines.md` に従い、日本語文面を作者が承認してから英訳・Production反映する。
