# 容器入り資源アイコンの遮蔽・固定範囲調査

調査日：2026-10-06 JST。対象正本：AMJ Core `main`、`5f84061393a844b60fded1ab03128f2da1f6124a`。

## 範囲と結論

作者の指示は「調査結果と、それから分かる対策の記述まで」。本記録は画像制作、マスター／マスク登録変更、合成実装、運用停止を行うものではない。対策は未実装・未検証の設計候補として記録する。

MOの同系統の箱入り11画像では、下部に共通RGBA画素が集中し、内容物と接触する上部では一致率が大きく低下した。自然な重なりには、内容物によって容器の縁・上面の見える場所が変わる余地が必要と考えられる。完成PNG上の容器全可視画素を毎回復元する制約は、その遮蔽を妨げる可能性がある。

AMJの恒等再合成PASSは、登録された殻付きソバ完成例を保持・復元できることを証明する。異なる形の内容物を自然に制作できることは証明しない。空マスターと1枚の完成例の差分は、その組の差分であり、全資源に共通する意味的な許可範囲ではない。

## 公開時の正本差分

本報告の公開直前、別作業のコミット `c8e7f2ff1248a2ec677a9b511f03d217ff53712e` がmainへ入り、v3-layeredの後方枡→透明内容物→前方枡へ切り替わった。以下の「現行方式」は調査時点のv2（冒頭のコミット）を指す。最新の運用正本はマニフェストとGolden Pathを参照する。

本記録はその変更を保持した文書追加であり、v3の実装・検証を行ったものではない。v3が前景木部を固定復元する点と、Occludable領域を内容物で隠せるという本報告の候補は同一ではない。3層化や空マスター再構成の成功だけから、縁に重なる内容物も自然に制作できるとは判断しない。v3についても、別形状の内容物で実画像の遮蔽を確認する余地が残る。

## 1. 観測資料

作者提供 `3219596926.zip` 内の Medieval Overhaul を使用。`About/About.xml` は packageId `DankPyon.Medieval.Overhaul`、modVersion `1.6.2.2`。

ZIP SHA-256：`6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`。

対象は `3219596926/Textures/Things/Item/Resource/PlantFoodRaw/` の次のPNG（全て128×128）。拡縮・位置合わせ・色変換せず、元PNGをRGBAへデコードして比較した。第三者テクスチャ自体は本リポジトリへ転載しない。

| 内容物 | ファイル |
| --- | --- |
| リンゴ | RawApples.png |
| バナナ | RawBanana.png |
| キャベツ | RawCabbage.png |
| ニンジン | RawCarrots.png |
| ニンニク | RawGarlic.png |
| レモン | RawLemons.png |
| レンズ豆 | RawLentils.png |
| キノコ | RawMushrooms.png |
| タマネギ | RawOnions.png |
| カボチャ | RawPumpkins.png |
| トマト | RawTomatoes.png |

`2665554648.zip`、`DBHforMedieval.dll`、`Defs.zip` は今回の比較結果の根拠には使用していない。他Mod一般の制作方法を調査し尽くしたという意味ではない。

## 2. 画素比較と見た目

各座標で「11画像全てのアルファが0より大きい画素」を分母、そのうち「11画像全てでRGBAの4値が完全一致する画素」を分子とした。透明背景の一致で数字が膨らまないようにした。行範囲は0始まり・終端を含まない。

| 行範囲 y | 全画像で可視の画素 | 全画像でRGBA一致 | 一致率 |
| --- | ---: | ---: | ---: |
| 0–31 | 0 | 0 | 対象なし |
| 32–63 | 2,526 | 74 | 2.93% |
| 64–95 | 3,709 | 2,073 | 55.89% |
| 96–127 | 1,817 | 1,663 | 91.52% |

この集計は容器だけをセグメントしたものではない。内容物、アンチエイリアス、色の微差も含まれるため、「下部の容器が全て完全固定」「上部の相違が全て遮蔽由来」とは断定しない。

11画像の並列目視では、共通した箱の前面・側面・下部が読み取れる一方、接触部の形は内容物に依存していた。レンズ豆は低い山、キャベツ・ニンニクは大きな塊、ニンジンは横長の形になり、バナナ・キノコ等は箱上面や前側へ重なる。上縁と内容物の境界を、1種類の粒山の形だけで制約する根拠は得られない。

**制作方法は未確認。** 配布PNGの共通画素から部品再利用は推測できるが、元のレイヤー、編集履歴、作者の工程説明はない。AI生成、手描き、一体生成、粒単位の合成、手修正の有無は判別できない。「AI生成Modもできているからこの方法なら必ず成功する」という結論にはしない。

再計測の最小手順（Python + Pillow + NumPy、ZIPは別途用意）：

```python
import io, zipfile
import numpy as np
from PIL import Image

names = ['RawApples', 'RawBanana', 'RawCabbage', 'RawCarrots',
         'RawGarlic', 'RawLemons', 'RawLentils', 'RawMushrooms',
         'RawOnions', 'RawPumpkins', 'RawTomatoes']
prefix = '3219596926/Textures/Things/Item/Resource/PlantFoodRaw/'
with zipfile.ZipFile('3219596926.zip') as archive:
    pixels = []
    for name in names:
        with Image.open(io.BytesIO(archive.read(prefix + name + '.png'))) as im:
            pixels.append(np.array(im.convert('RGBA')))
a = np.stack(pixels)
same = np.all(a == a[0], axis=(0, 3))
visible = np.all(a[:, :, :, 3] > 0, axis=0)
for lo, hi in [(0, 32), (32, 64), (64, 96), (96, 128)]:
    total = int(visible[lo:hi].sum())
    equal = int((same[lo:hi] & visible[lo:hi]).sum())
    print(lo, hi, total, equal, equal / total if total else None)
```

## 3. AMJ現行方式の検証範囲

確認した正本：

- `AGENTS.md`、`Docs/ArtStyle.md`、`Docs/GoldenPaths/TextureAssetPipeline.md`
- `Docs/GoldenPaths/BoxedResourceIconPipeline.md`、`Docs/GoldenPaths/FixedImageTemplates.md`
- `Docs/References/AMJ_Masu_Template.json`
- `Scripts/Art/fixed_template.py`、`Tests/test_masu_template.py`

調査時点のマニフェストは v2 / `active` / `replace_rgba`。editable bbox `[35, 44, 223, 169]`、required-fill bbox `[52, 54, 208, 157]`、editable patch defined coverage 0.98、required-fill差分coverage 0.65を登録している。

恒等レイヤーを `replace_rgba` で戻すテストは、登録完成例との0差分と、マスターの保護領域との0差分を検証する。scaffoldとcoverage検査は、透明素材だけで内部を消してしまう不具合や、未充填の状態を防ぐ。しかし、画素の色が変わるだけでも差分coverageは増える。充填・遮蔽・粒の形が自然であることをcoverageやbboxだけでは保証できない。

正本内には「exact variable maskを将来の材質差分の構造的基礎とする」「恒等PASS後は新資源に同じ契約を使える」という記述がある。今回の調査で分かったのは、その一般化を支える別内容物の制作実証がない点である。恒等テストは有用な回帰検査として残せるが、汎用テンプレートの十分条件ではない。

本調査では恒等テストを再実行していない。0差分PASSは既存記録・コードの検証対象として記述しており、新たな実行PASSを主張しない。

## 4. 対策案（未採用・未実装）

### 意味を持つ領域を分ける

| 領域 | 候補となる責務 | 検査の考え方 |
| --- | --- | --- |
| Hard fixed | 承認された前面・側面・下部・角・外輪郭の固定領域 | 最終RGBAがマスターと0差分 |
| Occludable | 内容物が手前に来れば隠れてよい上面・内縁・上縁等 | 隠れていない部分はマスターを再利用し、隠れた部分を最終復元しない |
| Extension | 内容物が上・必要な横方向へ張り出してよい領域 | 許可した範囲外へのはみ出しを拒否 |
| Required fill | 満杯の表現で最低限占める内部 | 差分coverageに加え内容物としての形・量を確認 |

これらは「同じ意味の相互排他的な4マスク」ではない。Required fillは内容物の許可範囲に含まれる検査用ガイドであり、Hard fixedとOccludableは固定保証と遮蔽許可の区別である。外周・前面まで自然な重なりが必要なら、対象部分を明示的にOccludableへ分類する設計判断が必要。無条件に前面全域を固定しながら、同じ画素を内容物で覆うことはできない。

同じ枡を使うことと、隠れた場所まで最終PNG上で同じ画素にすることを区別する。マスターの容器構造は再利用しつつ、物体の前後関係が変わる接触部を可変にする。後から保護画素を全面復元して粒を切り落とす方法、1枚の完成例の差分形状へ全内容物をクリップする方法、目視不良をcoverage PASSで正当化する方法は避ける。

### 接触境界を含む制作単位を試す

「内容物だけ生成して貼る」に限定せず、「上面・上縁・内容物・接触境界」を一体として描く／編集する方法を候補とする。固定下部は決定的合成で戻し、接触部は許可領域内で処理する。ただし、一体生成が最適という実証はまだない。レイヤー合成、手描き編集とも比較する余地がある。

これは現行の生成許可・共通パーツ固定ルールを変更するものではない。ImageGenの呼出し、マスク拡張、新しい領域契約の登録は別作業。既存マスクを候補ごとに広げて検査を通すことは認めない。

### 汎用性の検証を恒等テストと分ける

次回の工程改訂では、恒等再合成に加えて、接触形の異なる内容物を同じ領域契約で制作する試験が必要。例として、細粒の山、大きな豆／塊、平らな粉を使い、以下を同時に確認する。

1. Hard fixed領域のRGBA差分が0。
2. 許可範囲外の新しい画素、ハロー、切れ、継ぎ目がない。
3. 縁の前後関係が物体の形と整合する。縁の無条件復元で内容物が切れない。
4. 256pxと約64pxで、枡に自然に入っていると読める。
5. 同じマスターと許可領域で再現でき、各画像の都合でマスクを変更していない。

機械検査と見た目の検査は別の証拠とする。ここまで成功してから、再利用可能な工程として正本・マニフェスト・コード・回帰検査を整合させる。

## 5. この調査記録で変更しないものと次作業

画像、マスター、マスク、マニフェストの `active` 状態、合成コード、CI・テストは変更しない。既存の殻付きソバ承認画像と恒等テストも失効させない。既存手順には今回の検証限界への参照を付ける。

次に工程改訂を行う場合は、本記録の候補を実画像で検証し、採用範囲を決めてから実装する。現時点で「4領域化で問題が解決した」「自然な別内容物の量産工程が完成した」とは報告しない。

## 6. 2026-10-06 integration follow-up

After this audit was pushed, visual review of the separate v3-layered implementation found actual pixel damage at its complementary rear/front split boundary. That v3 split is therefore superseded.

The audit and the author's three-layer proposal are reconciled as follows: keep the complete canonical masu master intact as the base/rear layer; render contents/contact artwork over it; then reassert only a conservative hard-fixed foreground subset copied exactly from the master. Do **not** create the rear layer by subtracting a foreground polygon from the master. Do **not** clip contents with a cavity/pile polygon. The upper/contact region remains occludable, consistent with the MO comparison in this report.

This revised model is not yet activated for new-resource production. Core now fails closed until contrasting-content-shape tests and 256px/~64px visual checks establish that one region contract works without per-image mask changes.
