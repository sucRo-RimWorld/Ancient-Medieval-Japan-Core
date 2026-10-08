# AMJC作物の耐寒データ

## 責務と正本

AMJC固有作物の耐寒データは、**AMJCが所有・管理する**。CCTOは固定枯死・休眠・情報表示を提供するフレームワークとして利用し、CCTO側にはAMJC固有作物の数値表・DefName一覧・互換XMLを置かない。

- 最低成長温度はAMJC自身のPlantDefに設定する。
- 固定枯死温度・休眠設定は、CCTOが有効な場合だけAMJC側の互換XMLから `CropColdToleranceOverhaul.ColdToleranceExtension` として付与する。
- CCTOは任意依存のまま。未導入時もAMJCの栽培・加工は成立し、低温枯死には元のRimWorldの挙動を使う。
- CCTOが管理するVanilla/MO作物と、AMJC固有作物を区別する。MO小麦 `DankPyon_Plant_Wheat` の枯死温度はCCTO側のMO対応を利用する。Vanilla `Plant_Rice` はGrainsが**陸稲として成長温度を再設定**するが、固定枯死温度はCCTOのVanilla米定義（-1℃）を再利用し、Grains専用の `ColdToleranceExtension` は追加しない。
- 将来AMJC作物を追加・調整する際も、数値・根拠・互換XML・検証はAMJC側で更新する。CCTOには汎用APIに関する変更だけを依頼する。

本資料はCCTOの `Docs/Design.md` / `Docs/ImplementationTable.md` に置かれていたAMJC作物のデータを移管した正本である。移管時点では数値変更を行わなかったが、その後の再監査でAMJC側の判断として値を改定する。Stage Aの栽培全体は [Docs/Design.md §4.2.1](../../Design.md) と整合させる。値は現実の耐寒性を参考にした**ゲーム内バランス値**であり、現実の測定値そのものではない。

## 確定した固定枯死・休眠値

最低成長温度は `minGrowthTemperature`、固定枯死温度は `coldDeathTemperature` に対応する。休眠のみの作物には `coldDormancy=true` を設定し、固定枯死温度を設定しない。

| Crop | Minimum growth temperature | Fixed death threshold / behavior |
|---|---:|---:|
| Barley | 0°C | -8°C |
| Wheat fallback (MO absent) | 0°C | -6°C |
| Daikon | 0°C | -5°C |
| Buckwheat | 5°C | -2°C |
| Barnyard millet | 5°C | -2°C |
| Hemp | 5°C | -6°C |
| Kudzu | 5°C | cold dormancy |
| Foxtail millet | 8°C | -3°C |
| Proso millet | 8°C | -3°C |
| Adzuki bean | 8°C | -1°C |
| Soybean | 8°C | -3°C |
| Perilla | 8°C | -1°C |
| Rice | 10°C | -1°C |
| Taro | 10°C | -1°C |

クズ（Kudzu）は低温で地上部が休眠し、根株が生存して回復できる作物として扱う。休眠は最低成長温度未満で始まり、固定枯死の判定は閾値未満（strict `<`）で行う。閾値ちょうどでは枯死しない。

現時点でPlantDefとCCTO互換XMLが実装されているStage AのAMJC作物は、アワ `AMJC_Plant_FoxtailMillet_Awa`、ヒエ `AMJC_Plant_BarnyardMillet_Hie`、キビ `AMJC_Plant_ProsoMillet_Kibi`、ソバ `AMJC_Plant_Buckwheat_Soba`、大麦 `AMJC_Plant_Barley`。各最低成長温度は `Defs/ThingDefs_Plants/Plants_StageA.xml`、固定枯死温度は `Patches/Compatibility/CCTO_StageA.xml` が持つ。他の行は原則として今後の作物実装で利用する設計値だが、**Rice行は例外で既存Vanilla `Plant_Rice` を `Patches/UplandRice.xml` により陸稲化済み**である。Grainsの固定枯死Patchは作らず、CCTOのVanilla米対応を使用する。陸稲の5日・収量11・肥沃度最低0.7・成長10～42℃／最適18～32℃はGrainsの同Patchと `Docs/Design.md §4.2.2` が正本であり、実ゲーム温度挙動は未検証。未実装作物のDefNameを先行確定したり、存在しないDefを対象とするPatchを追加したりしない。

## 2026-10-04 アワ・ヒエ・キビの凍霜害再監査

栽培可能な低温域と、凍結・霜で枯死する温度は別特性として扱う。

| Crop | 採用値 | 判断 |
|---|---:|---|
| Proso millet / キビ | **-3°C** | 維持。レビューでは低温感受性が概ね +2～-3°C、品種別の霜感受性が -1.5～-4.1°C とされ、-3°Cは代表値として妥当。さらにアワより冷涼地に適応しやすいとの比較記述がある |
| Foxtail millet / アワ | **-3°C** | -4°Cから改定。-4°C処理では6時間から生存率が低下し、10～12時間で生存率が16.4%→4.8%まで落ちる。CCTOの固定閾値では持続時間を表現できないため、-4°Cを安全に耐える設定を避けて-3°Cへ丸める |
| Barnyard millet / ヒエ | **-2°C** | -4°Cから改定。低温条件での生育性は高い一方、Japanese milletは公的・普及資料でfrost-sensitive / winter-killedとされる。直接の致死温度実験値が不足するため、-2°Cはゲーム用の保守的な丸め値で、3種中もっとも確度が低い |

このため、ヒエの個性は「凍結に強い」ではなく、**凍らない低温域でも成長しやすい**ことに置く。CCTO導入時には、5～15°C付近でアワ・キビより成長しやすい一方、氷点下へ入れば特別に強くないという性格になる。

主な根拠:
- Cavers & Kane (2016), *The Biology of Canadian Weeds: 155. Panicum miliaceum L.* — proso milletの低温・霜感受性（-1.5～-4.1°Cの品種差）とfoxtail milletより冷涼地へ適応しやすい旨。 https://doi.org/10.1139/cjps-2015-0152
- Zhao et al. (2023), *Transcriptome Analysis Reveals Brassinolide Signaling Pathway Control of Foxtail Millet Seedling Starch and Sucrose Metabolism under Freezing Stress, with Implications for Growth and Development* — アワ苗を-4°Cで処理し、時間経過とともに生存率が大幅低下。 https://doi.org/10.3390/ijms241411590
- Tasmanian Department of Primary Industries, *Millet - Japanese (Echinochloa utilis)* — Japanese milletを “not at all tolerant of frost” と整理。
- Midwest Cover Crops Council, *Japanese Millet* — winter-killed / sensitive to frost と整理。

**注意:** `coldDeathTemperature` は現実の単一の致死温度を再現する値ではない。品種、生育段階、低温への曝露時間、馴化状態による差を、RimWorld上の明確な閾値へ丸めたゲーム内値である。

## 保存する候補範囲（現在は未使用）

以下は従来のバランス検討で保存していた候補範囲。現在のXML/APIは固定値を利用し、この範囲を自動的に読み込まない。将来CCTOに決定論的な個体差モードが実装され、AMJCで採用を判断した場合の再検討資料として残す。

| Crop | Minimum growth temperature | Candidate death range / behavior |
|---|---:|---:|
| Barley | 0°C | -9 to -7°C |
| Daikon | 0°C | -6 to -4°C |
| Buckwheat | 5°C | -3 to -1°C |
| Barnyard millet | 5°C | -3 to -1°C |
| Hemp | 5°C | -7 to -5°C |
| Kudzu | 5°C | cold dormancy |
| Foxtail millet | 8°C | -4 to -3°C |
| Proso millet | 8°C | -4 to -2°C |
| Adzuki bean | 8°C | -2 to 0°C |
| Soybean | 8°C | -4 to -2°C |
| Perilla | 8°C | -2 to 0°C |
| Rice | 10°C | -1 to 0°C |
| Taro | 10°C | -1 to 0°C |

## 2026-10-07 Base小麦の追加

`AMJC_Plant_Wheat` はMOなし時だけ `BaseWithoutMO/Defs/Plants_Wheat.xml` からロードする。最低成長0℃、CCTO有効時だけ `BaseWithoutMO/Patches/CCTO_Wheat.xml` で固定枯死-6℃を追加する。MO併用時はこのDef/Patchをロードせず、従来どおりCCTO側のMO小麦対応を利用する。静的・配置検証は実装済み、実機温度挙動は未検証。


## 暦＋温度を制御するnative播種試験（2026-10-08追加、実機未実行）

Grainsは最終的な気候マップの選定を所有しない。既存7穀の本番成長温度値を変更せず、孤立したQuickstart上でのnative `WorkGiver_GrowerSow` と `Plant.TickLong` の接続を別途検証する。25℃の陸稲播種、15日後・5℃での陸稲播種不可/成長停止と大麦の播種可/成長、25℃への復温後の陸稲成長を検査する。

温度は試験中のみ `BiomeDef.constantOutdoorTemperature` で固定し、テスト専用の暦移動を使用する。生育0℃大麦、10℃陸稲という生育温度の差の実機効果を対象とし、自然の季節気象モデル・降雪・CCTO固定枯死温度の実死判定は対象外。試験後は元値へ復元し、ユーザーのMod設定や本番Defsを変更しない。四構成の最新版実機結果は未取得。


## 制御温度実播種テストの日照・休息時刻補正（2026-10-08）

作者ログ`automated-gates(5).log`で、MOなし2構成およびMO+CCTOは6/6・ERROR 0、MO単独は復温後の陸稲`TickLong`成長増加が確認できず失敗。ゲーム実装では`Plant.Resting`時間に成長が止まるため、最後の復温を任意の夜間時刻に開始すると**温度制御試験ではなく昼夜差で失敗し得る**。復温前にローカル正午と実天空光を再同期し、光量・生命段階・成長率を検査してから2,200tickを進めるようE2Eを補正した（実機未再確認）。成長温度や固定枯死温度、CCTO依存の設計値は変更していない。正式結果と制約は`Docs/GrainsProfileTesting.md`。


## MO再検証結果（2026-10-08）

`automated-gates(6).log` にて、正午・天空光の補正を施したネイティブ播種/生育テストを含むMO単独実機構成がPickle 6/6・ERROR 0を達成した。旧ログ(5)の失敗は当該再実行では再発せず、既存の最低成長温度0℃（大麦）/10℃（陸稲）と本番XMLの値は変更していない。Vanilla・Vanilla+CCTO・MO+CCTOは補正前版で各6/6・ERROR 0を確認済みだが、修正版の全4構成一括実行は未確認。試験は5/25℃へ固定した屋外温度・暦移動に限定し、CCTO固定枯死の実発生、自然天候/季節温度履歴の正否は未検証。証拠と運用は `Docs/GrainsProfileTesting.md` を参照。


## 2026-10-08 制御温度テストの照明同期方式変更（実機再確認待ち）

(7)の4構成実機ログでは3構成にPickle `NullReferenceException` が発生し、`mo-ccto` だけ6/6・ERROR 0となった。前回修正時の手動`SkyManagerUpdate()`呼び出しが描画・影・天候更新も実行するため原因候補となるが、スタックがないので未確定。より狭いテスト経路として、正午のネイティブ太陽光`GenCelestial.CurCelestialSunGlow(map)`を読み、隔離マップの`ForceSetCurSkyGlow`キャッシュだけ同期、復元する。Plantの休息や実成長処理は回避しない。ゲーム本番の気象・低温枯死やCCTO機能には手を加えていない。最終判定は`Docs/GrainsProfileTesting.md`。


## 照明同期修正後のVanilla実機結果（2026-10-08）

`automated-gates(8).log` は修正後のVanilla単独でC#ビルド、Pickle 6/6、実行時ERROR 0を確認した。以前のNREはこの実行では再発しない。Vanilla+CCTO / MO / MO+CCTOの同修正版は確認待ちであり、旧版の合格と混ぜて4構成完了にはしない。5/25℃・暦移動・実播種/成長の試験範囲と、自然気象/CCTO枯死が未検証という制約は維持する。証拠hashと同一ソースでのマトリクス確認手順は `Docs/GrainsProfileTesting.md` を正本とする。
