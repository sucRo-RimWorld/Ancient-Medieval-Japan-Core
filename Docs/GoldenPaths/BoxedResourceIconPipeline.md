# Boxed Resource Icon Pipeline — Golden Path

## 状態と正本

2026-10-06：MO比較で判明した修正を **v4-contact-study** に反映した。正本の空枡と承認済み殻付きソバ画像は変更していない。新規資源の本番制作は `blocked_pending_occlusion_validation`。領域契約と合成・検査コードの実装完了は、自然な別内容物の量産成功を意味しない。

- マスター：`Textures/Shared/Containers/AMJ_Masu_Empty_Master.png`（承認済みv2、256×256 RGBA）
- マニフェスト：`Docs/References/AMJ_Masu_Template.json`
- 完成例：`Docs/References/AMJ_BuckwheatInHull_Ideal_256.png`
- 高解像度完成例：Library `/AMJ/References/AMJ_BoxedResource_BuckwheatInHull_Ideal.png`
- 調査根拠：[BoxedResourceOcclusionAudit.md](../Research/BoxedResourceOcclusionAudit.md)

各画像・マスクはマニフェストのSHA-256を照合する。殻付きソバの恒等再合成は例示画像の保存・復元の回帰検査であり、汎用性の証明には使わない。

## 領域契約

| 領域 | 責務 | 機械検査 |
| --- | --- | --- |
| HardFixed | 下側の前壁・側壁・下角・下部輪郭の保守的な木部 | 最終RGBA差分0。半透明輪郭も元のRGBAを直接コピー |
| ContactZone / Occludable | 内壁・上面・上縁・前壁上部・側壁上部。内容物で隠れる、接触影が変わる範囲 | 内容物と接触部を一緒に編集。最後に無条件復元しない |
| ExtensionAllowed | 上方・左右へ突出できる独立した余白 | 範囲外の変更を拒否。ソバ完成例のalpha形状を上限にしない |
| RequiredFill | 充填量検査用の内部ガイド | 可視かつマスターから変化した画素の割合。描画・切り抜きには使用しない |
| Forbidden（導出） | 上記3つの許可領域以外の全画素 | 最終RGBA差分0。透明画素のRGBと低alphaも検査 |

HardFixed・ContactZone・ExtensionAllowedは相互排他的。全マスター可視画素をHardFixedまたはContactZoneに分類し、未分類を許さない。RequiredFillはContactZone/ExtensionAllowed内の独立した検査ガイド。

v4初版のHardFixedは、前縁V字の近似線 `y = 173 - abs(x - 127) * 70 / 110` より40px下側のマスター可視画素だけとする。残りの可視木部・内部はContactZone。これにより前壁上部まで接触帯を確保する。ExtensionAllowedは独立矩形 `[8, 8, 248, 196]` 内のマスター透明画素。いずれも**検証用の初版であり、視覚承認済みの境界ではない**。MOの一致率からAMJの具体的な境界が直接証明されたとは扱わない。

同じ契約で3形状を試す。個々の候補を通すためにマスクを広げない。契約改訂が必要なら版・ハッシュ・根拠を更新し、3形状すべてを再検証する。

## 内容物＋接触部の入力

入力は、空枡マスターをそのまま複製した256×256の**描画済みコンテキスト画像**。空枡を見た状態で内容物・遮蔽・接触部の輪郭・控えめな接触影をContactZoneとExtensionAllowedへ描く。何も隠れない木部は元のマスターを残す。

- 透明な内容物だけを単独生成して載せる入力は使用しない。入力には元の空枡の文脈を保持する。
- 完成例との差分マスク、内部の菱形、単純な粒山形状へ内容物をクリップしない。
- ContactZoneでは、覆われる縁の画素や接触影も編集してよい。木部画素を一律禁止する旧規則は廃止。
- 内容物を描き終えたコンテキスト画像を、さらにマスターへalpha合成しない。描画済みの接触・半透明輪郭を二重合成しない。
- マスターへの拡縮、回転、全体色補正、ぼかし、全体量子化は不可。最終サイズを維持する。
- 全体画像を生成し直して共有部品を採用することは不可。生成が明示的に許可された場合も、制作対象はContactZone/ExtensionAllowed内の内容物と接触部だけ。

`contact_patch_min_defined_coverage = 0.98` は、元マスターが可視の接触帯で入力alphaが8以上の割合を検査する。透明素材で枡の大半を消す誤入力の検出用であり、正しい遮蔽や自然さの証明ではない。

## 決定的合成

1. ハッシュ、寸法、マスクの二値性・分類・重複・RequiredFillの包含を確認する。
2. 完全なマスターを複製したscaffoldで内容物と接触部を編集する。
3. 入力のForbidden変更を検出する。許可範囲外を切り落として合格にはしない。
4. 描画済み画像を保持し、HardFixedのRGBAだけ正本から直接復元する。元枡を相補的な前後ラスターへ分割しない。
5. HardFixedとForbiddenの最終RGBA差分0、充填、寸法、PNG構造を確認する。
6. 正本完成例との256px/約64px比較で、縁の前後関係・粒の切断・貼り付け感・ハロー・左右上部の汚染を確認する。

RequiredFillの現行0.65閾値は **bulk_grain** 用の構造的最低条件。透明消去は充填として数えない。大きな塊や長い物体の本番制作には、形状に適した別の充填プロファイルを登録・検証する。単一の65%基準を全資源の自然さ判定に一般化しない。

## 検証と本番を分離する

`scaffold` / `compose` は本番入口であり、現在は停止する。検証専用入口を使う：

```bash
python Scripts/Art/fixed_template.py scaffold-study Docs/References/AMJ_Masu_Template.json --output /tmp/masu-study/context.png
# 元の空枡を見ながら、内容物と接触部を許可領域内に描く
python Scripts/Art/fixed_template.py compose-study Docs/References/AMJ_Masu_Template.json /tmp/masu-study/context.png --output /tmp/masu-study/final.png
python Scripts/Art/fixed_template.py validate Docs/References/AMJ_Masu_Template.json /tmp/masu-study/final.png
python Scripts/Art/boxed_resource_review.py Docs/References/AMJ_Masu_Template.json /tmp/masu-study/final.png --output /tmp/masu-study/review.png
python Tests/test_masu_template.py
python Tests/validate_png_assets.py
```

study出力は `Textures` と `Docs/References` へ書けない。マスター・参照・全マスク・恒等素材・入力の上書きも禁止する。構造検査のPASSで本番状態は変化しない。Windowsでは `/tmp/masu-study` を通常テクスチャとして使われない一時フォルダーへ置き換える。

比較シートは `boxed_resource_review.py` が登録済み `representative_final` のSHA-256を検証して作る。別の記憶・生成画像・ローカル別名へ参照を差し替えない。

## 視覚的な有効化条件

同じマスター・同じ領域契約を変更せず、**低い粒状物／大きな塊／前縁へ強く重なる形** の3例で以下を満たすこと。

- HardFixed/Forbidden差分0、許可範囲外の漏れ0、適した充填条件を満たす。
- 内容物に応じた縁の隠れ方、接触、輪郭、陰影が自然。
- 256pxと約64pxの双方で枡に入っていると読める。直線的な切断・貼り付け感・左右上部の残存色がない。
- 自己QC後に視覚承認を記録する。合成図形テストやソバの恒等PASSを視覚承認に代用しない。

すべて通ったときにだけ `production_status` と `new_resource_production_status` を有効化し、マスク版・承認根拠・適用可能な充填プロファイルを正式記録する。

## 実行の意味と候補の扱い

「作成」「制作」「続けて」「修正」は登録素材によるローカル制作・合成・検査の指示であり、ImageGenの許可ではない。明示的な「生成」と対象Golden Pathの許可が必要。本番停止を生成指示だけで解除しない。

誤参照、旧分割、不正クリップ、全体再生成、汚染画素から派生した候補は失効し、候補・比較シート・派生物を破棄してmain Coordinationへ記録する。正本・承認済み完成例・明確に隔離された診断証拠を保持する。

旧 `replace_rgba` 差分マスクと恒等素材は履歴診断専用。旧 `rear_contents_front` の実装入口は削除され、本番にも検証にも使用しない。
