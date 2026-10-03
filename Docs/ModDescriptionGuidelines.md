# AMJ関連Modの説明フォーマット

**決定日:** 2026-10-04（日本時間）  
**対象:** AMJ Core・Environment・CCTOおよび今後の関連Mod

## 基準と改善方針

基本フォーマットはCCTOの説明に合わせ、公開・利用時のフィードバックを受けて継続的にブラッシュアップする。見出しや順序は基準を共有し、各Mod固有の長い説明まで機械的に複製しない。

基準資料:
- [CCTO README（公開内容の正本）](https://github.com/sucRo-RimWorld/RimWorld-Crop-Cold-Tolerance-Overhaul/blob/main/README.md)
- [CCTO Workshop説明](https://github.com/sucRo-RimWorld/RimWorld-Crop-Cold-Tolerance-Overhaul/blob/main/Docs/WorkshopDescription.md)
- [CCTO 日本語説明](https://github.com/sucRo-RimWorld/RimWorld-Crop-Cold-Tolerance-Overhaul/blob/main/Docs/SteamWorkshopDescription-ja.txt)

## 基本構成

1. 名称・概要: 何を変え、どのような遊びを提供するか。
2. 主な変更・対象範囲: 具体的な機能と責務。
3. バランス・設計方針、必要に応じて変更例。
4. 対応範囲・対応言語。
5. 必須Mod・任意Mod・互換情報。
6. **セーブ互換性: 既存セーブへの追加と途中削除を必ず明記する。**
7. Alpha / Betaの状況、フィードバック先、検証状況。
8. AI支援について、ライセンス、バージョン、支援リンク。

独立Mod化の経緯・フレームワークAPI・個別FAQ等は必要なModにだけ追加する。ゲーム内About.xmlは概要・依存関係・セーブ互換性を簡潔にまとめる。

## セーブ互換性の共通表記

追加・削除とも安全なModには次の文言を入れる。

- 日本語: **既存のセーブに追加または削除しても安全です。**
- 英語: **Safe to add to or remove from an existing save.**

全Mod共通なのは「セーブ互換性を記載すること」。安全性の結論は実装に合わせる。新規Def、保存される独自クラス・コンポーネント、ワールド生成等を確認し、条件付き・新規ゲーム必要・削除非推奨・未検証の場合は、その条件を明示する。追加の安全性と削除の安全性、既存ワールドへの反映範囲は区別する。

現在の扱い:
- **CCTO:** 既存PlantDefと挙動へのPatchで、独自の保存クラス・コンポーネントを追加しないため共通の安全表記を使用。読み込み後に既存植物にも新しい温度ルールが適用される。枯死済みの植物は削除しても復元されない。他Modの必須依存がある場合は維持する。実装確認に基づく判断であり、追加・削除専用の実機試験を実施済みとは記載しない。
- **AMJ Core:** 追加・削除の安全性は未検証。独自作物・収穫物・加工品等を含むため、一律の安全表記は使用しない。
- **AMJ Environment:** ワールド・地形生成を確認するには新規ゲームで使用する。独自BiomeDef・TerrainDefを使用したセーブからの削除は推奨しない。既存セーブへの追加の安全性は未検証。

## 正本・同期・確認

- 各ModのREADMEを公開内容の正本とする。未整備の開発版は設計書・本ガイドラインを基に公開準備時に整える。
- README → Workshop説明 → 貼り付け用の英語・日本語BBCodeの順で同期する。About.xmlの概要・依存関係・互換情報も整合させる。
- Workshopは対応するBBCodeを使い、表タグや長いコードブロックを避ける。数値の詳細はREADMEへ誘導する。
- 英語・日本語それぞれの説明をUTF-8で8,000バイト以内に収める。
- バージョン・対象数・検証状況を揃える。既存の検証結果を別の試験の証拠に転用しない。
- GitHub上の説明ファイルの更新と、Steam Workshopの公開ページ反映は別作業として記録する。
