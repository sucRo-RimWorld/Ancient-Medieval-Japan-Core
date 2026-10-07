# 六穀の環境比較回帰

2026-10-07。実装値の正本は各PlantDefと `Docs/Balance/Crops/Millet_Cultivation_Balance.md`。
この比較は既存値を変更せず、有限の成長時間で成熟収穫できる量を固定する。

| 軸 | 代表値 |
|---|---|
| 肥沃度 | 0.5 / 1.0 / 1.4 |
| 定温 | 10 / 20 / 30℃ |
| 有効成長日 | 5 / 10 / 20日 |

有効成長日は完全光量・休眠なしで成長できる時間の合計であり、暦日ではない。
種まき・収穫・加工の労働時間、初期成長、部分成熟収穫、作物間の栄養差、
播種研究の取得、天候、病害、霜、室内設備、栽培者技能・難易度は評価へ混ぜない。
初期成長は0、成熟収穫後の再播種は即時、共通の難易度・収穫技能倍率は1とする。

計算は `floor(有効成長日 × 肥沃度係数 × 温度係数 / growDays) × harvestYield`。
肥沃度が fertilityMin 未満なら播種できないため0。肥沃度係数は
`1 - fertilitySensitivity + 肥沃度 × fertilitySensitivity`。
温度係数は minGrowthTemperature ～ minOptimalGrowthTemperature で0→1、
最適範囲で1、maxOptimalGrowthTemperature ～ maxGrowthTemperature で1→0。
境界の浮動小数点誤差だけを1e-6で補う。成熟未満の端数は収量に算入しない。

Base小麦は明示値0/10/42/58℃、MO小麦の静的モデルは0/6/42/58℃を仮定する。
提供されたMO 1.6 Plants_Cultivated_Farm.xml はPlantBaseを継承し温度を指定しない。
参照したPlantPropertiesの既定値に基づく仮定であり、他ModのPatchやVanilla XMLの
継承を静的投影で再現したものではない。今回の10/20/30℃のセルでは両者の結果は等しい。
Pickle側はロード済みDefと実ゲームのPlantUtilityで別途検証する。

ゲーム実装参照（インストール済みゲームの代わりにはしない）:
[PlantUtility.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/RimWorld/PlantUtility.cs)、
[PlantProperties.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/RimWorld/PlantProperties.cs)、
[Plant.cs](https://github.com/Chillu1/RimWorldDecompiled/blob/2d508035082e7cb0c8e29e230d26bda6e546928f/RimWorld/Plant.cs)。
係数関数とgrowDaysの時間単位を確認した。休眠等を外した範囲を上記で明示する。

27セル中23セルで成熟収穫が可能。最大収量の回数（同率を両方へ算入）は
Awa 1、Hie 2、Kibi 8、Soba 4、Barley 4、Wheat 6。
同率があるため回数の合計は有効セル数と一致しない。

| 穀物 | 最大収量となる代表セル（肥沃度 / 温度 / 有効成長日） | 収量 |
|---|---|---:|
| アワ | 0.5 / 30℃ / 10日 | 13 |
| ヒエ | 1.4 / 20℃ / 5日 | 12 |
| キビ | 1.0 / 20℃ / 5日 | 11 |
| ソバ | 0.5 / 10℃ / 10日 | 8 |
| 大麦 | 1.0 / 10℃ / 10日 | 22 |
| 小麦 | 1.4 / 20℃ / 20日 | 56 |

回帰条件は全セルの成熟収量・勝者の固定、六穀それぞれの代表用途維持、
単一穀物が有効セルの2/3以上で最大にならないこと。
2/3は回帰の警戒線であり、普遍的なゲームバランスの証明ではない。
CCTOの枯死・耐霜差とMO Strawの価値はこの穀粒収量へ金額や隠れた重みを足さず、
別の実機生存・副産物評価で扱う。本比較だけで環境リリースゲート全体を完了としない。

実行: `python Tests/test_grains_environment.py`。
意図的に値を変更するときはCultivation正本・XML・回帰Fixture・説明を同時に更新し、
影響する代表セルをレビューする。Fixtureだけを自動更新して失敗を消さない。
