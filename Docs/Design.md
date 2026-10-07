# Ancient & Medieval Japan Core — 設計書

**文書状態:** Core→Grains再編設計確定・runtime移行前  
**対象:** RimWorld 1.6  
**現行公開名:** Ancient & Medieval Japan Core  
**将来の機能位置づけ:** Grains系独立Mod（公開名・packageId・既存DefNameの変更は移行完了後に別途判断）  
**基本方針:** 現CoreはAMJ全体の共通基盤ではなく、乾田穀物の栽培・一次加工・最低限の粉食を自己完結して提供するGrains系Modへ縮小再編する。Vanilla + Grainsだけで主要ループを成立させ、Medieval Overhaul（MO）は推奨環境・公式互換先とする。現行公開Coreはruntime移行と自動テストが完了するまでMO必須のまま維持する。

---

## 1. 目的

現Coreを再編したGrainsは、RimWorldの乾田農業に、**土地・気温・生育期間によって主食穀物を植え分ける判断**を追加する独立コンテンツModとする。

中心領域:
- アワ・ヒエ・キビ・ソバ・大麦・小麦の乾田栽培
- 穀束、脱穀、殻取り等の一次加工
- 小麦粉・蕎麦粉・雑穀粉と最低限の製粉経路
- 粉を無用途にしないための研究不要・低設備の最低限粉食
- 作物ごとの肥沃度・温度・生育日数・収量・加工価値の差
- MO導入時の小麦・小麦粉・石臼・Straw等の公式互換

Grainsは、水田・米、豆類、繊維、根菜、一般採集、発酵、酒造、保存、建築等を「共通基盤だから」という理由では所有しない。これらは実際の主要ゲームループに最も自然なModへ分け、Grainsとは必要時だけ条件付き互換する。

最終的な対象時代は新石器相当から戦国末期までとするが、Grains自体はその全生活文化を網羅しない。

### 1.1 名称・サブタイトル方針

シリーズ名 **Ancient & Medieval Japan（AMJ）** は維持する。

一方、英語圏では `Medieval Japan` だけだと、侍・城・合戦・戦国武将などの華やかな軍事文化を主題とするModと受け取られやすいため、公開時のサブタイトル・短い紹介文では**江戸以前の一般の人々の生活が主題であること**を明示する。

方針:
- **`pre-Edo Japan`** を、時代感を直感的に伝える有力な表現として使用する
- `rural life`、`village life`、`ordinary people`、`farming and survival` 等を組み合わせ、生活・生産側のModであることを示す
- `samurai warfare` や `Sengoku warfare` を主題と誤解させる表現は避ける
- 固定サブタイトルは公開準備時に決定する。現段階では **“pre-Edo rural/village life”** を中核イメージとする
- 日本語でも「戦国の華やかさ」より、**古代～中世の一般の人々が新しい土地で暮らしを成立させる**ことを前面に出す

---

## 2. 設計思想

### 2.1 農村を基準にする

都市・寺院・上流階級の食文化ではなく、RimWorldの小規模コロニーに近い、

- 農村
- 山村
- 湿地・河川沿いの集落
- 小規模な自給生活

を基準とする。

「京都や江戸で食べられたもの」ではなく、**地方集落が自力で確保・加工できたもの**を優先する。

AMJが主役として想定するのは、武将・大名・上流階級ではなく、**農民・職人・猟師・漁師・流民・下級武士等を含む一般の人々**である。戦国末期までを対象に含むが、「戦国の華やかさ」や武将文化を中心テーマにはしない。

RimWorld / MOのコロニーは、様々な事情で既存共同体を離れた人々が新しい土地で小規模な共同体を作る遊びとして捉える。AMJも、
- 何を植えるか
- どこに水田を作るか
- 冬までに何を蓄えるか
- 木・土・藁・紙等をどう使うか
- 食料をどう加工・保存するか
- 限られた人手をどこへ割くか

といった**生活の成立そのもの**を中心に置く。

米、とくに精製された白米は「最初から当たり前に食べる高性能主食」ではなく、雑穀・麦・芋等で日常を支えながら、土地・水・労働力・加工設備へ余裕ができた時に安定供給できる、**共同体の豊かさを示す食料**として位置づける。

### 2.2 Coreでは各資源に主用途を1つ与える

史実上ひとつの作物・資源に複数用途があっても、Core本体では原則として**主用途を1つだけ実装する**。

目的:
- Coreの役割を「農作物・原材料の基盤」に限定する
- 1つの資源から料理・薬・油・繊維などへ機能が枝分かれし、Coreが肥大化するのを防ぐ
- 中間素材や専用加工設備を、用途のない段階で先行実装しない
- 後続Addonが同じCore資源を拡張しやすくする

例:
- 荏胡麻 → Core採用は保留。採用する場合も種実食材までとし、搾油はCore外
- 葛 → Coreでは葛根として薬草
- 大豆 → Coreでは豆類食材
- 米 → Rice Cultivationでは水田稲作の主食用穀物（Core / Waterworks所有外）
- 栗 → Coreでは食料資源（木そのものは通常の樹木として木材利用可能）

油・発酵・料理・繊維加工・酒造などの追加用途は、それぞれ対応するAddon側で実装する。特に搾油はCoreの進行要件から外し、油を実際に利用する機能側で必要になった時点まで後回しにする。

搾油は、それ単独で十分な規模や独立したゲームループを持たない限り、専用Addonを作らない。
- 食用油としての用途が主なら、**その油を実際に使う保存・発酵・調理等の機能側**で用途とセットで追加する
- 灯火・塗装・生活素材としての用途が主なら Materials / Architecture系Addon
- 複数用途が増え、独立した設備・研究・加工体系が必要になった場合のみ専用Addon化を再検討する

**史実上の多用途性そのものは捨てず、Mod群全体で段階的に解放する。**

### 2.3 史実に根拠を置いたゲーム的抽象化

Coreは古代～中世日本を厳密に再現する歴史シミュレーターではなく、**史実に根拠を置きつつ、RimWorld上で意味のある選択を残すゲーム的抽象化**を行う。

実装判断では「史実に存在したか」だけでなく、**ゲーム内で別の判断を生むか**を重視する。さらに、その工程・設備・資源管理が**UXとして実際に楽しいか、判断や工夫につながるか**を最優先の採用基準とする。史実的に正確でも、単なるクリック数・待ち時間・在庫分裂・作業キュー増加にしかならない要素は省略・統合・自動化してよい。

削ってよい例:

- 実際には複数段階ある加工工程を、ゲーム上意味が薄い場合は1工程にまとめる
- 地域差・時代差の細部を、代表的な仕様へ整理する
- 同じ役割の作物・野草・道具をすべて実装しない
- 歴史上存在していても、既存要素とゲーム上ほぼ同じ役割なら省略または互換で済ませる
- 季節差・栽培差・保存差を、成長速度・耐寒性・保存期間など少数のパラメータへ抽象化する

残すべき例:

- 作物ごとの寒冷・乾燥・痩せ地への適性差
- 米の水田依存
- 大豆などの多用途性（荏胡麻・油料作物はCore採用自体を保留し、必要な用途が成立した段階で再検討）
- 日本側で早期利用できる繊維資源
- 保存・加工に必要な手間
- MOの西欧基準と日本史の時代感がずれる部分

判断基準は、**それを削ることで古代～中世日本らしい選択が失われるか**とする。

### 2.4 歴史的に非必須な技術は「使うと得」にする

史実上、常に必須ではなかった工程・設備・技術は、ゲーム上でも原則として必須化しない。

代わりに、

- 作業時間短縮
- 収量改善
- 保存性改善
- 天候への安定性向上
- 失敗率低下
- 副産物回収効率向上

などの利点を与え、**使えば有利だが、使わなくても生活は成立する**設計を優先する。

稲作ではこの原則を次のように扱う。

- 収穫後の未加工状態は「稲」として保持する
- 通常経路は `稲 → 籾 + Straw → 米` とし、脱穀と籾摺りを2工程に分ける。地干し等の一般的な乾燥は通常経路へ抽象化する
- 任意乾燥は専用の稲架を追加せず、**MO既存のDrying Rack**へ `稲 → 乾燥した稲` のProcessを追加して表現する
- 乾燥経路は `稲 → 乾燥した稲 → 籾 + Straw → 米` とし、脱穀時の**籾の産出量だけを増やす**。Straw産出量は通常経路と同じにする
- 標準乾燥時間は**1ゲーム日**とし、MO / Processor Framework既存の天候連動を再利用する
- 乾燥を行わなくても稲作は成立する
- 完成後の101%超過・過乾燥等の追加監視は実装しない。乾燥設備の占有時間と歩留まり改善だけで選択を成立させ、完成後回収を強制するマイクロ管理を増やさない
- 「籾」は独立した中間アイテムとして保持し、玄米は独立ThingDefにせず、籾摺りから日常食用の「米」までを1工程へ抽象化する

**稲作の具体的な歩留まり・稲架掛けボーナスはRice Cultivationの詳細設計で決定する。Waterworksでは決めない。**

この原則は、史実上地域差・時代差が大きい設備や加工方法にも適用する。

### 2.5 料理バフの設計基準

Core本体では完成料理を大量追加しない。この項目は、**各Addonで必要に応じて追加する専用料理・既存料理Mod互換・将来の料理機能**に適用する。

**独立した Cuisine / Cooking Addon は現時点では計画しない。** 料理名・レシピ数を増やすこと自体にはゲーム上の価値を置かず、同じ性能・同じ材料役割の料理を多数追加して調理Billやメニューの一覧性を悪化させない。新しい料理Recipeは、材料選択・保存性・加工工程・季節性・設備・効果等に**他の料理と区別できるゲーム上の意味がある場合だけ**追加する。

料理の表現は、個別の歴史料理を大量に並べるより、**性能と投入コストを基準に少数の抽象料理へまとめる**ことを優先する。代表例として、上位加工品カテゴリの食材を一定数要求して「豪華な和食」を作り、Vanilla/MOの豪華な食事相当の食事価値にMoodと短時間の健康系バフを加える、といった粗い抽象化を許容する。現時点の目安は**上位カテゴリ加工品4個 → 豪華な和食**だが、必要個数・栄養・Mood・Hediff値は実装時のバランス調整で確定する。

一方で、MOの目玉焼き・狩人のスープ・カボチャのフリットのように、**特定材料を要求すること自体がゲーム上の選択になる料理**は個別Recipeとして厳選してよい。個別料理を追加する基準は、専用材料の確保・材料構成・解禁Tier・保存性・効果・季節性等によって、他の料理と明確に異なる生産判断を生むこととする。単なる料理名違い・見た目違い・史実上の別名だけでは追加しない。個別料理名は原則として説明文やフレーバーへ寄せ、**材料指定そのものに意味がある少数の例外だけRecipe化する。**

個別Recipeの有力候補は、**祝い・祭礼・宴席など日常食ではない特別な機会に作られた料理**とする。日常的に常食する料理より、希少材料・複数加工品・追加作業を要求しやすく、完成時に高いMoodや一時的な健康/能力効果を持たせる理由も作りやすい。したがって、個別料理の追加可否は「歴史的に有名か」より、**特別な場面のために備蓄・加工・調理するというゲーム上の目的が成立するか**を優先して判断する。

料理の一時バフは、**Medieval Overhaul（MO）の料理バランスを基準に設計する**。

基本原則:
- 料理Tierだけで、バフの有無や強さを決めない
- 低Tier料理でも、材料・工程・供給条件に相応のコストがあるなら一時バフを付けてよい
- 高Tier料理でも、研究Tierだけを理由に強いバフを付けない
- 材料側の研究Tier・栽培難度・入手性も料理価値に含める
- 保存性、Mood、食事カテゴリ、栄養、作業量も料理価値の一部として扱い、すべてを能力バフで表現しない
- バフは原則として一時的なHediff・能力補正として実装し、恒常的な能力上昇や恒常的な健康改善は付けない

バフ設計で評価する要素:
- 材料の入手難度
- 材料の供給安定性
- 卵・乳など畜産資源の要求
- 複数系統の材料要求
- 材料側の研究・栽培Tier
- 加工工程と作業量
- 専用設備の必要性
- 保存性そのものが持つ価値
- 食事カテゴリとMood
- 既存MO料理との相対バランス

MOで確認済みの参考例:
- 目玉焼き: 初級料理でも専用材料である卵を要求し、短時間の能力バフを持つ
- マッシュドポテト: 初級料理でもジャガイモに加えて乳製品を要求し、短時間の能力バフを持つ
- カボチャのフリット: 料理研究は初級だが、材料のカボチャ自体は上級農業で解禁される
- 中級料理: 「手の込んだ食事」相当の食事カテゴリ価値を持つ例がある
- 上級料理: 「豪華な食事」相当の食事カテゴリ価値を持つ例がある
- パン: 研究解禁料理でも特別な能力バフを持たない例
- 燻製肉: 保存性が主価値で、付加価値はMood +2程度に留まる例

許容する一時効果の例:
- 意識
- 運動能力
- 指の機能
- 作業速度
- 空腹率
- 消化・免疫・臓器機能などへの短時間補正
- Mood

禁止・抑制するもの:
- 永続的な能力上昇
- 永続的な健康改善
- 料理だけで重い疾病や負傷を治療する効果
- MO既存料理との比較で明らかに過剰なバフ

> **料理バフはTier基準ではなく、材料・手間・研究・保存価値を含む総コストに対して付与する。**

米は水田・温度要求・栽培期間・一次加工など雑穀より重い生産条件を持つため、AMJで米専用料理を追加する場合は、**同程度の料理工程なら米系料理を雑穀系料理よりやや高価値にする**ことを許容する。ただし「米だから無条件に強い」のではなく、栽培・加工を含む総コスト差を根拠に調整する。

また、**酒などの嗜好品は日常食より工程・研究を複雑にしてよい**。生存に必須な主食や日常料理は管理負荷を抑える一方、任意の高付加価値品は、追加精製・選別・発酵・濾過・温度管理・複数研究段階などをゲーム上の遊びとして許容する。複雑さは嗜好品としての価値・希少性・強い一時効果へつながる場合に採用し、単なる作業数の水増しにはしない。

### 2.6 日本・中国・朝鮮半島を一括りにしない

竹・紙・大豆など、共有される素材・技術はあるが、文化そのものは統合しない。

- 日本Coreは日本の生活基盤として作る
- 中国系Modは中国文化として扱う
- 朝鮮半島系Modが存在する場合も別文化として扱う
- 共通素材のみ互換カテゴリで接続する

「East Asian Culture」的な文化混同は避ける。

### 2.7 DLC非依存

CoreはDLCなしで成立させる。

- Ideology前提の宗教・禁忌は扱わない
- 肉食禁忌・精進・寺院制度はCore外
- 神祇信仰などもシステム化せず、必要ならフレーバー程度

### 2.8 依存・基準環境

AMJ各Modは、**AMJシリーズ内の別Modを理由なく必須依存にしない**。各Mod自身の主要ゲームループが成立するために不可欠な前提だけを必須依存とし、他のAMJ Modや外部Modとの接続は原則として任意互換とする。

長期的な構成目標は、中央の「Core」を全Addonが必ず通る依存木ではなく、**独立したAMJ Mod群 + 公式相互連携**である。全要素を一体で遊びたい場合はAMJ一式を導入するが、個別Modだけ、またはVanilla / MO等との一部組み合わせでも、そのMod自身のゲームループが成立する構成を優先する。

依存判断の基準:
- 「その素材・機能を使うと内容が増える」だけなら必須依存にしない
- 「その前提がないとModの主要ゲームループ自体が成立しない」場合のみ必須依存を認める
- AMJ Mod同士の追加レシピ・追加原料・追加Def接続は、両方が存在する場合だけ有効になる互換Patchを基本とする
- 任意互換が増えること自体は避ける理由にしない。RimTest Redux / Pickle / 静的検証等で主要な組み合わせを自動化し、互換マトリクスとして維持する
- 依存関係を減らすために同一概念のDefを各Modへ無秩序に複製しない。所有Modを明確にし、必要なら条件付きPatchで参照する

#### Medieval Overhaulとの関係

作者の標準プレイ環境・主要比較対象としてMOを重視する方針は維持するが、**作者がMO前提で遊ぶことと、GrainsがMOを必須依存にすることは分ける。**

Grains移行後はVanilla + Grainsで、乾田穀物の栽培 → 一次加工 → 製粉 → 最低限の粉食まで成立させる。MO導入時は同じ概念のMO小麦・小麦粉・石臼・Straw等を条件付き互換から実Def供給元として再利用し、同等のAMJ資産を二重表示しない。

Base XMLにはMO DefNameへの無条件参照を残さない。MO固有PatchはMO存在時だけ適用する。About.xmlのMO必須解除は、runtime移行とBase/MO自動テストが完了した最後に行う。

`AMJ - Medieval Overhaul Japanization` はMO本体を古代～中世日本向けに再構成するPatch + Retextureレイヤーであり、責務上MO必須を維持する。World Tech Levelは中世限定世界を作るための強い推奨Modとし、Japanization自身では包括的なTech Level制限を再実装しない。

#### AMJ Mod間の依存方針

現時点の方向性:
- Grains / 現Core: Vanilla単体で乾田穀物・一次加工・製粉・最低限粉食を成立させる。MOは推奨・公式任意互換
- Fermentation: Grainsを必須依存にしない。単独の発酵ループを持たせ、Grains導入時に雑穀等、Rice Cultivation導入時にAMJ米等を追加接続する
- Brewing: Grains / Waterworks / Rice Cultivationのいずれも自動的な必須依存にせず、存在時だけ対応原料・工程を追加接続する
- Ironmaking: Vanilla単体で鉄器加工・砂鉄供給・古代～中世製鉄を成立させる。MO / Environment / Waterworksは公式任意互換。詳細は [IronmakingDesign.md](IronmakingDesign.md)
- Waterworks / Rice Cultivation / Hot Springs / Environment / Events / Factions / Backgrounds等: 責務上必要な前提だけを持ち、Grainsを共通必須基盤にはしない。Waterworksは水利、Rice Cultivationは水田・稲・籾・米・稲作一次加工を所有する

#### Hot Springs / 温泉 Addon

GrainsはHot Springsを所有しない。専用リポジトリ作成前の詳細設計・互換方針はProjectの [HotSpringsCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/HotSpringsCandidate.md) を正本とする。Grains側には、Grainsを必須依存にしないという所有境界だけを残す。
#### 大豆の所有と外部大豆Mod

大豆はGrainsの所有外。未所属の大豆・加工候補と外部Mod比較はProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) と [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) を参照する。Grainsは将来Addon向けの大豆Defを先行所有しない。
#### Core実装識別子

実装開始時点の識別子は以下で固定する。packageIdやDefName prefixは外部Patch・セーブ・互換Modから参照されるため、公開後は原則変更しない。

- packageId: `sucro.ancientmedievaljapan.core`
- Core所有Defのprefix: `AMJC_`
- 最初のStage A栽培スライス: `AMJC_Plant_FoxtailMillet_Awa`
- アワ・ヒエ・キビ共通の未脱穀収穫物: `AMJC_RawMillet`
- CCTOは任意依存のままとし、導入時のみAMJ側互換PatchからCCTOのDefModExtensionを付与する
- AMJC固有作物の耐寒数値・設計表・候補範囲・Def対応・互換XMLはAMJCが所有し、CCTO側には置かない。CCTOはフレームワークとして利用する

#### MO併用プロファイルとしての統合

MO導入時は、既存の農業・研究・設備・素材を可能な限り再利用し、日本側で必要な差分だけAMJが所有する。これは**MOをAMJ全体の必須プラットフォームとする意味ではなく、MO併用時の公式互換設計**である。

再利用の優先順位:
1. MOに同じ概念のDef・設備・素材・研究・カテゴリがある場合は、MO併用Patchからそれを利用する
2. 概念は同じだがAMJ側の数値・研究位置が合わない場合は、MO併用時だけ既存DefをPatchで調整する
3. MOに存在しない日本固有要素、または既存Defではゲーム上の意味が異なる要素はAMJ独自Defとして所有する
4. MOなしの主要ゲームループに必要なDefを、MO側だけに所有させない。逆に、MO互換だけのためにAMJ側へ同一資産を無秩序に複製しない

技術方針:
- MO固有参照・Patchは可能な限り専用ファイル/ディレクトリへ隔離し、MOなしでは読み込まれない条件付き互換として扱う
- base側のPlantDef / ThingDef / Research / Recipe / C#からMO DefNameへの無条件参照を残さないことを、必須解除の移行条件とする
- `MayRequire`、`PatchOperationFindMod` 等は、XML構造に適した方式を選んでMO存在時だけ適用する
- MO更新時はMO互換プロファイルを自動テスト対象として維持する
- Food Drying、DBH、Edo等の他の任意Modも同じく条件付き互換として扱う

`AMJ - Medieval Overhaul Japanization` は例外で、MO本体の研究・Def・Recipe・資産を日本化すること自体が存在理由なのでMO必須を維持する。Grains等の独立AMJ ModはJapanizationを必須依存にしない。

用語:
- **Vanillaプロファイル** — RimWorld + Grains（MO依存解除後の目標）
- **MO併用プロファイル** — RimWorld + MO + Grains
- **現行公開Coreプロファイル** — 移行完了までの RimWorld + MO + AMJ Core。公開版の実装事実を示す語であり、長期依存原則ではない

#### 2026-10-07 Core / MO依存監査結果（初回分類・履歴）

`ARCH-MODULAR-001` の初回実装監査では、現行CoreのStage A / New VillageはMOなしではロード・進行できない直接参照を複数持つ一方、農業ループ自体はMO固有機能を必要としないと判断した。**この初回分類のうちGrains再編で変更された所有判断は、直後の「Grains再編後の最終 Base / MO 所有境界」を優先する。**

監査時点の実装事実:
- 本体には `1.6/` フォルダ、製品C#、製品DLLは存在せず、実行時実装は主にXML Def / Patchで構成される。C#はE2Eテスト側にのみ存在する。
- Production DefのParentNameはVanilla側の `PlantBase` / `PlantFoodRawBase` / `RoughPlantBase` / `BenchBase` 等で、MO ParentDef継承はない。
- MO向け `MayRequire` / `PatchOperationFindMod` は未実装で、`Patches/MedievalOverhaul_StageA_Wheat.xml` はMO存在を前提に無条件で読み込まれる。CCTO互換だけは既に `PatchOperationFindMod` で条件化されている。
- Base側の主な直接MO参照は、`DankPyon_Straw`、`DankPyon_BasicAgriculture`、`DankPyon_IronIngot`、`DankPyon_RawWood`、`DankPyon_Cereal`、MO小麦/RawWheat、New VillageのMO研究・初期物資、`DankPyon_Peasant` apparel tag、MO由来の仮テクスチャである。
- Paper / Paper Press、Salt、MO Drying Rack、Processor Frameworkは現行Stage AのProduction XMLから直接参照されていない。これらは設計上の将来連携であり、Agricultureのハード依存理由にはしない。

依存の分類と所有方針:

| 依存領域 | 分類 | Vanilla / Agriculture側 | MO併用時 |
|---|---|---|---|
| MO小麦そのものへの調整、MO RawWheat/Flour/製粉Recipeの変更、日本語ラベル上書き | **A — MO拡張そのもの** | 読み込まない | 専用互換Patchとして維持 |
| Awa/Hie/Kibi/Soba/Barleyの栽培・脱穀・殻取り | **B — 自己完結可能** | AMJ既存Def/Recipeを正本とする | 同じAMJ Defを利用 |
| Barley / 加工台の `DankPyon_BasicAgriculture` 前提 | **B — 自己完結可能** | AMJ所有の農業進行へ置換するか、研究なしの初期経路として成立させる。正確な研究Def/コストは実装前バランスで確定 | MO研究ツリーへの接続・置換は互換Patch |
| `DankPyon_Straw` を全穀物の脱穀副産物として直接出力 | **C — MO時だけ互換可能** | Strawを主要農業ループの必須出力にしない。Agriculture自身に用途がない段階では重複Straw Defを作らない | MO互換Patchから `DankPyon_Straw` を副産物として追加 |
| `DankPyon_RawWood` StuffCategory | **C — MO時だけ互換可能** | Vanilla `Woody` で成立 | MO時だけ許可素材へ追加 |
| 加工台の `DankPyon_IronIngot` cost | **B — 自己完結可能** | Vanilla資源で建設可能にする。専用AMJ金属Defは不要 | 必要ならMO互換でiron ingot costへ寄せる |
| `DankPyon_Cereal` ThingCategory | **C — MO時だけ互換可能** | Vanilla食事で利用できる食材属性を正本とする | MO汎用製粉・醸造へ接続する対象だけ条件付き登録 |
| MO小麦Plant/RawWheatをStage A小麦そのものとして利用 | **B — 自己完結可能** | 小麦をVanillaプロファイルでも提供するならAMJ所有のフォールバック小麦Plant/収穫物が必要。既存 `AMJC_Wheat` のDefNameは維持 | AMJフォールバック小麦を重複表示・栽培させず、MO小麦を公式互換から利用 |
| MO Flour / 製粉設備 | **C — MO時だけ互換可能**（依存解除の最低条件ではない） | Vanilla料理へ穀粒として消費できれば主要ループ成立。粉食を正式提供する段階でAMJ所有の粉/Recipeを追加。専用新規設備は必須ではない | MO Flour / Millstone / mill系経路を優先再利用 |
| MO仮テクスチャ（Barley wheat art、StonecuttingSpot、Millstone） | **B — 自己完結可能** | Production用AMJ画像へ置換 | 同じAMJ画像を利用してよい |
| New VillageのMO研究・ration/raw wood/iron ingot・knife stuff | **B — 自己完結可能** | Vanilla/AMJ所有要素だけでStartを成立させる | MOらしい研究・物資差分が必要なら条件付きPatch |
| `DankPyon_Peasant` apparel tag | **C — MO時だけ互換可能** | Vanilla `Neolithic` 等だけで成立 | MO時だけtagを追加 |
| MO Paper / Paper Press | **C — MO時だけ互換可能** | Agriculture本体では所有しない。植物/繊維原料までを必要に応じて所有 | MO製紙への原料接続は互換Patch。Vanilla製紙が必要になれば製紙側機能の責務 |
| MO Drying Rack / Processor Framework | **C — MO時だけ互換可能** | Agricultureの依存にしない | MO設備へ接続する機能だけ条件付き利用。別AddonがPFを必要とする場合はMOの推移的依存に頼らず直接依存を宣言 |
| MO Salt | **C — MO時だけ互換可能** | Agriculture本体では所有しない | 塩を必要とするPreservation / Coastal系等の責務側で条件付き接続 |

この監査では、**A分類の存在はCoreをMO必須にする理由にならない**。Aは「MOがある時だけ意味を持つ互換機能」なので、Baseから隔離・条件化する。

##### Agriculture / Waterworks / Rice Cultivation境界

- Agriculture / 現Coreは、畑作作物、畑作物の一次加工、Vanilla料理へ到達する最低限の食材経路を所有する。
- WaterworksはCore非依存のまま、自然取水・開渠・暗渠・分水・温泉引湯等の**水利基盤だけ**を自己完結して所有する。
- Rice CultivationはWaterworks非依存の独立Modとして、水田・稲・籾・米・稲作固有の一次加工を所有する。Waterworksなしでも単体の簡易な水田成立条件で遊べるようにする。
- Waterworks + Rice Cultivation併用時だけ、Rice Cultivation側の水田をWaterworksの有効な水路ネットワークへ接続する公式互換を行う。WaterworksをRice Cultivationの必須依存にはしない。
- MO Drying Rack等を使う稲作上の任意工程はRice Cultivation側の互換責務であり、Agriculture / Waterworksの依存解除条件には含めない。

##### 紙・塩・Processor Framework

- Paper / Paper PressはAgricultureの主要ループではないため、Core/Agriculture本体へVanilla代替を抱え込まない。Agricultureが靭皮繊維等を所有する場合も、製紙そのものはMO互換または将来の製紙/Materials側機能へ接続する。
- SaltもAgriculture本体の主要ループではない。既存設計の「海水採取 → `DankPyon_Salt`」はMO併用時だけ成立する互換案として扱い、BaseにMO Saltへの直接出力を置かない。
- 現行CoreはProcessor Frameworkのclass / ProcessDefを直接利用していない。MOがPFを依存に含めていることを理由に、将来AddonがPFを暗黙利用してはならない。Fermentation等がPFを主要ループに必要と判断した場合は、そのAddon自身が直接依存を宣言する。

##### 識別子・セーブ互換

MO依存解除で、既存の `packageId=sucro.ancientmedievaljapan.core`、公開名、`AMJC_` prefix、既存AMJC DefNameは変更しない。**Coreという名称は当面維持するが、アーキテクチャ上は「AMJ全体の共通必須基盤」ではなくAgriculture相当の独立コンテンツModとして扱う。** 「Core」は歴史的な公開名/識別子であり、他Addonが依存すべきという意味を持たせない。

MO併用の既存セーブでは、現在参照されているMO Defを急にAMJ Defへ置換しない。MOが残っている更新経路では、現在のMO小麦・MO素材・AMJC既存DefNameを条件付き互換から維持する。新規のVanillaフォールバックDefはMO併用時に重複栽培・重複Recipeを標準表示しない。

「Core更新と同時にMOを既存セーブから外す」経路は別の移行ケースであり、依存メタデータを外しただけで安全とは扱わない。実装時に専用のロード/Def参照テストを通すまでは未保証とする。

##### MO必須解除の実装順序

1. **テストを先に分岐**し、Production About.xmlを変更しなくてもMOなしのBase XMLをロードできるテスト用Vanillaプロファイルを用意する。
2. BaseのMO直接参照を除去する。Straw / Cereal / RawWood等はMO互換へ移し、建設材料・研究・ScenarioはVanilla/AMJ側で自己完結させる。
3. Barley/設備のMO仮画像をAMJ-owned Production画像へ置換する。
4. Stage Aで小麦をVanillaプロファイルにも提供する場合は、AMJフォールバック小麦を追加し、MO時の重複を抑止する。粉食は必要な用途が確定した範囲だけ追加する。
5. `Patches/MedievalOverhaul_StageA_Wheat.xml`、MOラベル、MOカテゴリ、MO Scenario/素材差分を明示的な条件付き互換へ隔離する。
6. Vanilla / MO × CCTO有無の自動マトリクスをすべて通し、runtime ERROR 0を確認する。
7. **最後に** About.xmlのMO必須依存・load orderとREADME/Workshop等の公開説明を一括変更する。About.xmlだけを先行変更しない。

##### 自動テスト・サポートマトリクス

最低限、依存解除実装前に次の4プロファイルを常設する。

| プロファイル | 主な自動確認 |
|---|---|
| Vanilla + Grains | 未解決MO Def/class 0、Stage A作物、一次加工、製粉・最低限粉食、Vanilla simple meal受入、New Village、runtime ERROR 0 |
| Vanilla + Grains + CCTO | 上記 + AMJC crop cold-tolerance extension |
| MO + Grains | MO小麦/Flour/Cereal/Straw等の互換Patch、重複小麦・小麦粉・石臼経路なし、New Village MO差分、runtime ERROR 0 |
| MO + Grains + CCTO | MO互換とCCTO互換の同時適用、Stage A回帰、runtime ERROR 0 |

静的XML検証は全プロファイルの前段に置き、Pickleで実ロード後のDef・Recipe・Scenario・Vanilla meal受入・MO互換・runtime ERRORを確認する。RimTest Reduxは、今後C#の移行補助や独立ロジックを追加した場合の単体/ロジック試験を優先し、現行のXML中心実装で無理に代替しない。人間の手動確認は、Production画像/UI/操作感など自動化できない項目に限定する。

Fermentation / Brewingは、GrainsやMOをハード依存にしない設計を採る場合、それぞれ **Vanilla単独の主要ループ** と **Grains併用時の追加原料接続** を最低限の自動ケースとする。MO設備/原料を正式互換する場合だけMO併用ケースを追加し、CCTOは発酵・酒造側が作物温度Defを直接変更しない限り直積マトリクスへ含めない。Fermentation + Brewing相互のケースも、一方の出力を他方が公式に消費する設計が確定した場合だけ追加する。

##### Grains再編後の最終 Base / MO 所有境界（2026-10-07）

この節は ARCH-MODULAR-001 のGrains再編確定版である。上記の旧Agriculture監査、後段の旧Stage B〜Dロードマップ、MO前提の一次加工記述と矛盾する場合は、Grains移行ターゲットについてはこの節を優先する。旧MO必須版の具体値はMO条件付き互換で保持する。下記のBase/MO表と実装進捗に従う。

| 領域 | Base（Vanilla + Grains） | MO併用時 | 最終所有判断 |
|---|---|---|---|
| アワ・ヒエ・キビ・ソバ・大麦 | AMJ既存Plant・収穫物・一次加工を使用 | 同じAMJ Defを使用 | **Grains** |
| 小麦Plant / 小麦束 | Grains所有の非MO小麦Plant・穀束を供給 | MOの DankPyon_Plant_Wheat / DankPyon_RawWheat を可視の供給元として使い、AMJフォールバックは重複表示しない | **概念・バランスはGrains、MO時の実Def供給元はMO** |
| 脱穀後の小麦穀粒 | 既存 AMJC_Wheat | MO小麦束をGrains脱穀工程へ通し、同じ AMJC_Wheat へ合流 | **Grains**。既存DefName維持 |
| 小麦粉 | Grains所有のフォールバック小麦粉 | DankPyon_Flour を唯一の標準小麦粉として利用し、AMJ小麦粉を二重表示しない | **Base概念はGrains、MO時の実Def供給元はMO** |
| 蕎麦粉 / 雑穀粉 | Grains所有 | Grains所有のまま。MO generic flourへ統合しない | **Grains** |
| 製粉Recipe | Grainsが小麦・蕎麦・雑穀のBase Recipeを所有。製粉では総栄養を保存 | 小麦はMO既存製粉経路へ接続。蕎麦/雑穀のGrains RecipeはMO石臼へ追加 | **工程仕様はGrains** |
| 石臼 / 最低限の製粉設備 | Grains単体で使えるAMJ所有の手動石臼を持つ。最低限経路はMO研究なしで成立 | MOの DankPyon_Millstone を標準設備として再利用し、AMJ石臼は重複表示しない | **BaseはGrains、MO時の実Def供給元はMO** |
| DankPyon_Cereal | 存在しない前提。Base主要ループに使わない | MO既存製粉/醸造へ参加させる対象だけ登録。未脱穀束・ソバ・雑穀を一律登録しない | **MO互換専用** |
| Straw | **AMJ Straw ThingDefを作らない。** Base脱穀では茎葉残渣を非アイテム化 | 脱穀時だけ DankPyon_Straw を副産物として追加。収穫時Hay・製粉時Hay/Strawは出さない | **MO時のみMO所有資産を利用** |
| 作物・加工研究 | Base主要ループからMO ResearchDef参照を除去。最低限の栽培・一次加工・手動製粉はMO研究なしで成立 | MO研究との接続は条件付き互換。MO研究がないとGrains主要ループが止まる構成にしない | **BaseはGrains/MO非依存** |
| 建築材料 | Vanilla / Grains所有のStuff・Thingだけで建設可能 | RawWood / IronIngot等への材料置換・追加は条件付き互換 | **BaseはVanilla/Grains** |
| New Village Scenario | **独立Scenarios Modが所有**。Grainsの旧版互換コピーはScenarios不在時だけ読み込む | ScenariosがGrains/MO導入時の物資・研究差分を任意互換として所有 | **Grainsの最終責務から除外。物理分離済み、実ゲーム・旧セーブ移行は未検証** |
| CCTO | なくてもGrains作物は成立 | CCTO存在時だけ既存互換Patch | **任意互換** |
| 米・水田 | 所有しない | 所有しない | **Waterworks / Rice Cultivation** |
| 豆類 | 所有しない | 所有しない | **Grains外。将来所有先を用途と合わせて決定** |
| 繊維・紡績・製紙 | 所有しない | Grains-MO互換にも置かない | **Grains外。将来のMaterials/Textiles等で決定** |
| 根菜・一般野菜 | 所有しない | 所有しない | **Grains外。将来所有先を決定** |

**小麦統合の固定ルール**

現行コードの残存MO依存と検証範囲は [`GrainsDependencyAudit.md`](GrainsDependencyAudit.md) を参照する。Def識別子の分離完了を、画像・実ゲームを含む独立動作の完了と解釈しない。

- MOなし: Grains小麦Plant → Grains小麦束 → 脱穀 → AMJC_Wheat → Grains小麦粉。
- MOあり: MO小麦Plant → DankPyon_RawWheat（小麦束）→ 脱穀 → AMJC_Wheat → DankPyon_Flour。
- 同一プロファイルでAMJ小麦PlantとMO小麦Plant、AMJ小麦粉とMO小麦粉を標準経路として並存させない。
- 既存MO+Coreセーブで参照されているMO小麦/RawWheatと AMJC_Wheat の関係は維持する。Core更新と同時にMOを既存セーブから外す移行は別ケースとして扱う。
- MO小麦の成長・肥沃度等はGrainsの6穀物バランスに合わせて条件付きPatchし、供給元がMOであることを理由に未調整値へ戻さない。

**Strawの固定ルール**
- Grains単体ではStraw ThingDefを所有しない。
- Vanilla + Grainsの主要ループで独立した需要先を持たず、依存解除のためだけに追加すると用途の薄い在庫を増やすためである。
- MO併用時にはMO Strawの既存需要があるので、穀束の脱穀時だけ DankPyon_Straw を追加する。
- MO Strawの価値が作物選択を過度に歪めないこともMOプロファイルの回帰テスト対象とする。
- 将来、MOなしでも藁を主要資源として消費するAMJ機能が成立した場合は、その自然な所有Modを決めてGrainsと条件付き互換する。

**研究・材料・Scenarioの分離条件**

Base側から次の無条件参照を0にする。
- DankPyon_BasicAgriculture とNew VillageのMO研究
- DankPyon_IronIngot / DankPyon_RawWood
- DankPyon_Peasant
- DankPyon_MealRations 等、ScenarioのMO専用初期物資
- DankPyon_Cereal / DankPyon_Straw
- MO小麦 / RawWheat / Flour / MillstoneへのBase直接参照
- MO由来のProduction仮テクスチャ

Scenarioの旧具体値表は移行中のMOプロファイル互換契約とする。Baseの具体値はCore標準Scenario節に併記する。step 2では同package内でBaseとMO差分を分離済み。2026-10-07の作者決定により、最終所有先は開始シナリオ専用の独立Modとする。物理移行は下記の移行条件を満たしてから実施し、現行Defの存在をGrainsの恒久責務と解釈しない。

**Grainsの存在意義を守る恒久回帰**

最低限、痩せ地/標準/肥沃地、寒冷/温暖、短期/標準/長期の代表環境を組み合わせて評価する。収量・growDays・加工価値に加え、CCTO併用時は固定枯死温度/休眠、MO併用時はStraw等の追加価値も含める。

期待する役割は、ソバ/キビ=短期・痩せ地、ヒエ/大麦=寒冷側、小麦=肥沃地・長期・粉食、アワ=標準〜肥沃地で収穫回数を抑える主力とする。単一穀物が代表条件のほぼ全てで最適になる状態を回帰失敗とする。Environmentは差を強調する推奨姉妹Modだが、**Vanilla + Grainsでもこの選択が消えないこと**をリリース条件とする。

**旧Stage B〜Dとの整合**
- 旧Stage B（豆類）、Stage C（繊維）、Stage D（根菜）はGrainsロードマップから外す。
- これらの歴史的調査・候補記述はAMJ全体の将来候補として参照してよいが、「Grainsが所有する予定」という意味では失効する。
- 大豆をFermentationが使う、繊維を製紙/織物が使う、根菜を将来の食生活機能が使う等の接続は、実際の所有Mod確定後に任意互換で行う。

**移行順序**
1. About.xmlを変えず、MOなしBase XMLをロードできるテスト用プロファイルを先に作る。
2. Base XMLからMO研究・素材・カテゴリ・Straw・Scenario参照を除去する。
3. 非MO小麦Plant/穀束、小麦粉、蕎麦粉、雑穀粉、手動石臼、最低限粉食をGrains Baseへ追加する。
4. MO互換を条件化し、MO小麦/RawWheat/Flour/Millstone/Strawへ上表どおり収束させる。
5. MO仮テクスチャをGrains所有Production画像へ置換する。2026-10-08時点で単体用の既存AMJ/Vanilla仮参照とMO時の従来参照は条件分離済み。専用Production画像・実描画は未完了（`GrainsDependencyAudit.md`）。
6. Vanilla + Grains / Vanilla + Grains + CCTO / MO + Grains / MO + Grains + CCTO の恒久マトリクスに、環境別穀物選択回帰を加えて通す。
7. 最後にAbout.xml、load order、README/Workshop等の公開説明を同期する。

この所有境界確定後の最初のruntime作業は、**テストハーネス分離**とする。

**2026-10-07 ハーネス分離の実装:** `run-grains-tests.bat` と
`Docs/GrainsProfileTesting.md` に、実MO / 実CCTOの有無を選ぶ4プロファイルを追加した。
Production About.xmlを変えずにruntimeファイルをそのままテスト専用コピーへ読み込ませる。
旧MO/CCTO fixtureの8シナリオとは別に、各構成の読み込み・一次加工・任意CCTOを
確認する移行用smokeを置く。step 2でNew Village実開始、step 3で製粉・粉食のロード後契約を追加したが実機未実行であり、環境別6穀物選択を含むリリース条件全件を満たした扱いにはしない。
**2026-10-07 Base分離 step 2:** Base Defs/翻訳からMO研究・素材・カテゴリ・Straw・Scenario・apparel参照を除去した。大麦と加工台はBaseでは研究不要、加工台の金属はSteel 30、簡易加工場はWoodyのみとする。MO併用時は `loadFolders.xml` の IfModActive により `Compatibility/MedievalOverhaul` を読み込み、旧38件の明示AMJC Def/抽象Def契約を保持する。MO小麦脱穀、外部MO小麦PatchとRawWheat翻訳もこの条件付きフォルダへ移した。step 2時点ではBase小麦の脱穀Recipeを非公開とし、次のstep 3で復帰した。

4構成のPickle featureにNew Villageのロード後設定と実開始を追加した（各5シナリオ）。静的projectionはAMJ所有XMLとBase差分Add/Replaceだけを検証し、RimWorldの継承・全Patch・Def解決・描画の代替ではない。step 2時点では小麦・製粉・粉食は未実装だった（次のstep 3でXMLを追加）。MO仮画像3件の置換、実機4構成、セーブ移行は未完了。Production About.xmlのMO必須依存は維持する。

**2026-10-07 step 3 小麦・製粉・最低限粉食の初期実装:**

- `loadFolders.xml` はrootと、MO時の `Compatibility/MedievalOverhaul`、非MO時の `BaseWithoutMO` を排他的に読み込む。IfModNotActiveは添付MO 1.6 LoadFolders.xmlの実使用を確認した。Base専用小麦/小麦束/小麦粉/石臼/小麦製粉がMO時に重複しない。
- 非MO小麦は `AMJC_Plant_Wheat` → `AMJC_RawWheat` →既存 `AMJC_ThreshWheat` / Bulk →既存 `AMJC_Wheat`。12日・収量28・肥沃度最低0.7/感応度0.9、研究なし、束120日、脱穀1:1・Strawなし。最低成長0℃、高温側58℃、最適10～42℃をBaseの明示初期値とする（Vanilla標準値との実機比較は未実施）。CCTO時だけ-6℃固定枯死拡張を付ける。
- 製粉は `AMJC_MillWheat` / `AMJC_MillBuckwheat` / `AMJC_MillMillet`。可食穀粒10→粉10、各0.05栄養で総栄養0.5を保存、workAmount 300、Crafting。粉は60日保存・直接摂食不可。小麦粉 `AMJC_WheatFlour` はBaseだけ、`AMJC_BuckwheatFlour` / `AMJC_MilletFlour` は両プロファイルで所有する。
- Base設備は `AMJC_ManualMillstone`（BlocksGranite 30 / WoodLog 20）。MO時は既存 `DankPyon_CraftFlour` でAMJC_Wheat→DankPyon_Flourへ進み、蕎麦/雑穀製粉を `DankPyon_Millstone` に接続する。最低限製粉を研究で止めないためMO石臼のresearchPrerequisitesを条件付きで除去する。MO小麦の既存研究と旧38件のAMJC契約は維持する。MO側の研究除去Patchは実ソースに対する静的参照確認であり、他Modとの実ロード優先順位は未検証。
- 最低限粉食の初期値は以下。各Recipeは研究・Cooking最低技能なし、Campfire / ElectricStove / FueledStoveで利用可能、workAmount 300、Nutrition換算入力0.5→料理1個0.9、2.5日保存、`AMJC_AteFlourFood` のMood +2（0.5日、stackLimit 1）。MO時だけ餺飥の入力をDankPyon_Flourへ置換する。

| 料理 | ThingDef | RecipeDef | Base入力 | MO入力 |
|---|---|---|---|---|
| 餺飥 | `AMJC_Houtou` | `AMJC_CookHoutou` | `AMJC_WheatFlour` | `DankPyon_Flour` |
| そばがき | `AMJC_Sobagaki` | `AMJC_CookSobagaki` | `AMJC_BuckwheatFlour` | 同左 |
| 雑穀団子 | `AMJC_MilletDumplings` | `AMJC_CookMilletDumplings` | `AMJC_MilletFlour` | 同左 |

新規説明文は日本語先行レビュー前のため空欄とし、未承認の歴史的説明を英訳・公開していない。旧小麦Recipeの説明/翻訳は保持する。新規画像は生成せず、Base小麦は既存AMJアワ、束・粉は既存AMJ雑穀、石臼・料理はVanillaの開発用画像参照を使う。**これらは完成画ではなく、固有画像・日本語説明レビュー→英訳、実機の継承/参照/Graphic/Bill実行、環境別選択・既存セーブ回帰をリリース前に完了する必要がある。** Production About.xmlのMO必須依存はまだ変更しない。開始シナリオも物理移転前の暫定配置を維持する。

`Tests/validate_grains_chain.py` と変異回帰は入力/出力、栄養保存、研究不要、保存/Mood、MO差替え/非重複を静的確認する。旧38件はそのまま照合し、新規11件の共有Defだけ追加許可する。4構成のPickleに製粉/粉食のロード後契約を加え、各6シナリオとした。ゲーム内でBillを完了した証拠ではなく、実機実行自体も未実施。

#### 外部Modとの競合優先順位

AMJを導入している場合、**AMJが責務を持つ機能・資源・バランスについてはAMJの設計を最終優先する。**

- 外部Modと競合しない要素は可能な限り共存させる
- 同じ作物・設備・研究・加工経路・栽培条件等を双方が変更する場合は、AMJ側の定義・数値・研究位置・加工設計へ統一する
- 外部Modの仕様へAMJを合わせるために、AMJ内で確定した肥沃度感応度・温度特性・収量・加工工程等を崩さない
- これは他Modを文化的理由だけで削除する方針ではなく、**AMJが扱う領域の整合性を守るための競合解決規則**である
- 外部Modにしか存在しない非重複要素は、そのまま利用できることを優先する

**Vanilla Plants Expanded - More Plants（VPE More Plants）**
- 必須依存にはしない。Vanilla基準で水田・追加作物を実装した先行例として参考にする
- アワ・ヒエ・大麦等、AMJと役割が重なる作物が併用環境に存在する場合は、AMJ側で重複非表示・統合・数値上書き等を行い、AMJ設計を優先する
- AMJで確定した growDays、収量、肥沃度感応度、温度特性、研究、一次加工等をVPE値へ合わせない
- VPEの水生栽培が肥沃度を無視する設計はAMJ水田へ採用しない。AMJ作物では水田でも作物固有の肥沃度感応度を維持し、土地条件を農業上の選択として残す
- VPE水田とAMJ水田を併用する場合の具体的なDef統合・栽培可否は、Rice Cultivation実装時に互換Patchとして決める

**種システム系Modは要望ベース互換とする。**
- AMJ Core標準では、種アイテム・播種時の種消費・種在庫管理を導入しない
- Progression: Agriculture、SeedsPlease系等は、初期の正式互換対象には含めない
- 外部Mod側の自動対応でAMJ作物が正常に扱える場合は、専用Patchを追加しない
- 利用者から具体的な対応要望または不具合報告が出た場合に、対象Modの保守状況・利用状況・AMJ/MO研究体系との競合を確認した上で任意互換Patchを検討する
- 特に外部ModがMOの農業研究を削除・置換する場合は、AMJ側の研究進行・作物解禁設計を崩さないことを優先する

Vanilla Expanded Frameworkなども、必要な機能が小さい限り必須依存にはしない。

### 2.9 Grainsと別Modの境界

Grainsの責務は、**乾田穀物の栽培・収穫・一次加工・製粉・最低限の粉食を一つのゲームループとして成立させること**に限定する。

#### Grainsに入れる基準

- アワ・ヒエ・キビ・ソバ・大麦・小麦
- 穀束・殻付き中間物・可食穀粒
- 脱穀・殻取り・製粉と、その最小設備
- 小麦粉・蕎麦粉・雑穀粉
- 粉を無用途にしないための最低限粉食
- 各穀物の肥沃度・温度・生育日数・収量・保存性・加工価値
- Vanilla自己完結に必要なフォールバック
- MO存在時だけ適用する公式互換

#### Grainsに入れない基準

- 水田・稲・籾・米・稲作水利
- 小豆・大豆等の豆類
- 大麻・カラムシ等の繊維作物、紡績、製紙
- 里芋・大根等の根菜・一般野菜
- 採集一般、山菜、きのこ、果樹
- 発酵、酒造、塩蔵、一般乾燥保存
- 一般水利、温泉
- 開始シナリオ、開始用Faction/PawnKind、初期研究・物資
- 建築、衣服、武具、派閥、背景、イベント
- 将来Addonが使うかもしれないという理由だけの共通素材

旧Stage B（豆類）・C（繊維）・D（根菜）はGrainsロードマップから外す。内容自体を永久不採用としたわけではなく、主要ゲームループと自然な所有先が確定した時点で別機能として再評価する。

#### 開始シナリオの独立Mod化（2026-10-07 作者確定）

「新しい村」のScenario、開始用プレイヤーFaction/PawnKind、初期研究・物資は、**開始シナリオ専用の独立Mod**が所有する。Grainsは穀物・一次加工・製粉・最低限粉食を所有し、村の開始条件を含めない。NPC派閥を追加するAMJ Factionsとも別責務とする。正式名称は **Ancient & Medieval Japan - Scenarios**（略称AMJ - Scenarios）、packageIdは `sucro.ancientmedievaljapan.scenarios`。作者指定により専用リポジトリ [`Ancient-Medieval-Japan-Scenarios`](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Scenarios) で所有する。Coreリポジトリは作者により `Ancient-Medieval-Japan-Grains` へ改名された。リポジトリ改名だけでは本番ModのpackageId・DefName・About依存を変更しない。 移行対象台帳・二つの試作パッケージの生成規則・旧セーブ検証計画は [`Docs/ScenarioExtraction.md`](ScenarioExtraction.md) を正本とする。

- 開始シナリオModはVanilla単独で成立させる。Grains・MOを必須依存にしない。
- Grains導入時だけ雑穀等の開始物資と加工経路への接続を適用し、MO導入時だけMO研究・素材・携行食等の差分を適用する。両方導入した構成も開始シナリオMod側の任意互換で扱う。
- Grains側から開始シナリオModへの必須依存も設けない。穀物を使うために専用開始を選ぶ必要はない。
- 今回は所有方針の確定であり、物理移行は未実施。step 2のScenario/Base/MO差分とテストは移行中の契約として現パッケージに残す。Vanillaだけの新Mod開始物資の具体値は移行設計で決め、現在のAMJC物資を無条件で持ち込まない。

**物理移行の前提・完了条件**
1. `AMJC_NewVillage`、`AMJC_PlayerVillage`、`AMJC_Villager` と関連翻訳・開始ダイアログ・互換Patch・Quickstart/テストの移転対象を監査する。既存DefNameを維持し、旧パッケージとの同時導入でも各Defの供給者を1つにする。
2. 旧Coreで開始した既存セーブの読込、Grains単独、新シナリオMod単独、両方導入を検証する。旧Coreを外す／新Modを加える場合の移行手順と、互換保持Defが必要かを実装・実機検証で決める。安全な削除・差替えを未検証のまま保証しない。
3. 新規開始の恒久テストは開始シナリオModへ移す。Vanilla単独、Grains併用、MO併用、Grains+MO併用を検証し、既存セーブ回帰とruntime ERROR gateを適用する。Grainsの恒久テストから専用Scenarioの存在要求を外すのは物理移行と同時とする。
4. 現行38件のMO契約snapshotは削除して回避せず、移転したScenario/Faction/PawnKindの契約を移転先で継承し、穀物側の契約と分けて維持する。
5. 所有先・依存・セーブ互換の実装に合わせて双方のAbout/README/Workshop/2gameとテスト手順を同期する。現時点の公開説明を分離済みへ書き換えない。

#### 詳細設計前の先行Mod監査

AMJ横断の先行Mod監査・比較候補はProjectの [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) を正本とする。GrainsにはGrains自身の依存・互換・実装判断だけを残す。
#### 先行Mod監査の現時点結論（2026-10）

横断的な結論と未所属候補はProjectの [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) へ移管済み。Grains固有の現行互換方針は本書のFood Drying・MO統合・互換優先度の各節を正本とする。
#### Mod構成そのものを設定として扱う

AMJ群では、巨大なSettings画面で多数の機能をON/OFFさせるより、**導入するModそのものによって機能構成を決める**設計を優先する。

方針:
- 機能単位で十分に独立できるものは別Modへ分割する
- 各Modは、導入した時点のデフォルト設定でそのModらしい遊びが成立することを目標とする
- 「Enable Fishing」「Enable Japanese Factions」「Enable Fermentation」のような大項目ON/OFFを大量に設けない
- Settingsは数値調整、難易度、互換上必要な例外、デバッグ等に限定する
- ただし、**同じ機能構成のまま難度・数値・互換挙動を変える**ように、Mod分割では不自然な差はオプション化してよい
- ユーザーが多数のAMJ系Modを併用することを前提にし、**Modリスト自体を構成画面として扱う**
- Mod数が増えること自体より、巨大Mod化によって不要機能・競合範囲・保守範囲が増えることを避ける

Addonの基本的な役割は、Coreで粗く抽象化している生活・生産工程を**必要な分野だけ細かい作業粒度へ展開すること**とする。Addonを追加するほど、専用設備・中間素材・温度管理・追加加工・研究段階・物流管理などが増え、プレイヤーが扱う生産工程は原則として複雑になり、難度も上がる方向でよい。これは意図した進行であり、Addonを「入れるほど単純に強くなる追加コンテンツ」にはしない。

ただし細分化そのものを目的にはしない。各Addon内部でも、**判断・在庫・設備配置・季節/温度管理・投入コストなどにゲーム上の意味があり、かつUXとして遊んで面白い工程だけを残し、意味のない史実上の微細工程は引き続き抽象化する。** 面倒さそのものを難度として扱わず、選択・計画・リスク管理・設備運用などの遊びに変換できない負荷は削る。したがって「Coreより粒度は細かいが、そのAddon内では必要以上に細かくしない」を共通原則とする。

#### 基礎Addon

Salt Preservation、Fermentation / Brewing、Sake等の専用リポジトリ作成前の詳細設計はProjectの [FermentationBrewingPreservationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/FermentationBrewingPreservationCandidate.md) を正本とする。Grainsはそれらを必須依存にしない。
#### AMJ容器（甕）— 既存Mod・時代考証監査後の方針

容器・甕・陶器の横断設計はProjectの [ContainersPotteryCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ContainersPotteryCandidate.md) へ移管済み。Grainsは汎用容器システムを所有せず、必要な収納・加工設備は各機能の所有Modで判断する。
#### Japanese Environment / 日本環境Mod

日本の気候・地形・河川・海岸線・バイオーム・野生植生・季節景観は、AMJ Coreへ統合せず、**独立姉妹Mod `Ancient-Medieval-Japan-Environment`** が所有する。

- Repository: `sucRo-RimWorld/Ancient-Medieval-Japan-Environment`
- EnvironmentはAMJ Coreを必須にしない
- Grains側は乾田穀物と、その作物固有の成長温度・肥沃度感応度・収量・一次加工・製粉を所有する。水田・稲・米は独立したRice Cultivation Modが所有する
- Environment側は、それらが置かれる外部環境である気候・標高/Hilliness・河川・海岸線・バイオーム・野生植生等を所有する
- AMJ Core / CCTO / MO等との接続は必要に応じて任意互換とする

Environment固有の詳細数値・世界生成仕様はCore側へ重複記載せず、**Environmentリポジトリの `Docs/Design.md` を正本**とする。

#### Hunting & Gathering / 狩猟採集Mod

未所属の狩猟採集・山野資源・沿岸採集設計はProjectの [HuntingGatheringCoastalCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/HuntingGatheringCoastalCandidate.md) を正本とする。Grainsは採集システムを所有しない。
#### AMJ Backgrounds / 背景Mod

未所属の背景Mod候補はProjectの [SocietyModulesCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/SocietyModulesCandidate.md) を正本とする。GrainsはBackstoryを所有しない。
#### AMJ Clothing / 一般生活者の衣服Mod

未所属の一般生活者衣服候補と既存和服Mod比較はProjectの [SocietyModulesCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/SocietyModulesCandidate.md) を正本とする。Grainsは衣服Defを所有しない。
#### AMJ Factions / 派閥Mod

未所属のFaction・集落生成候補はProjectの [SocietyModulesCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/SocietyModulesCandidate.md) と [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) を正本とする。GrainsはNPC派閥を所有しない。
#### AMJ Events / 生活・社会イベントMod

未所属の生活・社会イベント候補はProjectの [SocietyModulesCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/SocietyModulesCandidate.md) を正本とする。GrainsはイベントModの実装仕様を保持しない。
#### AMJ - Medieval Overhaul Japanization / MO日本化レイヤー

JapanizationはGrainsの機能ではない。専用リポジトリ作成前の設計正本はProjectの [MedievalOverhaulJapanizationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/MedievalOverhaulJapanizationCandidate.md)、詳細監査はProject `Docs/Research/MedievalOverhaulJapanization*.md` とする。GrainsはMOとの自分自身の互換Patchだけを所有する。
#### Vanilla生活文化・心情はJapanizationへ抱え込まない

VanillaのThought / Trait / drug attitude / room・家具期待等を前近代日本へ合わせる構想は、MO固有PatchであるJapanizationの責務外とする。**独立Modとして切り出される前の構想・監査は `sucRo-RimWorld/Ancient-Medieval-Japan-Project` が正本**であり、Grainsでは詳細仕様を保持しない。

Project側の現行候補は仮称 `AMJ - Premodern Culture`。詳細は Project `Docs/Ideas.md`、`Docs/Roadmap.md`、`Docs/Research/VanillaPremodernCultureThoughtAudit.md` を参照する。Japanization側では、将来同Modが成立した場合のMO家具・食事・酒等との任意互換境界だけを扱う。

MO 1.6.2.2の研究ツリー全67ノード（MO独自51 + MOが移動/再構成するVanilla 16）の初回分類、史料アンカー、未解決監査項目は [Project MedievalOverhaulJapanizationResearchAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/MedievalOverhaulJapanizationResearchAudit.md) を詳細正本とする。研究・武器・料理等の個別分類は同文書の監査を経て実装へ落とし込み、チャット上の一時分類だけでXMLを変更しない。

### 2.10 MOの研究フローを古代～中世日本史へ再構成する

MO全体の研究再構成はGrainsの責務外で、AMJ - Medieval Overhaul Japanizationが所有する。専用リポジトリ作成前の詳細設計はProjectの [MedievalOverhaulJapanizationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/MedievalOverhaulJapanizationCandidate.md) を正本とする。Grainsは自分が所有する作物・加工の研究解禁と、MO併用時の条件付き接続だけを管理する。
## 3. Grains本体（他AMJ Modなし）の位置づけ

現CoreはAMJ Mod群すべての共通基盤ではなく、**乾田穀物の選択と一次加工を扱うGrains系独立コンテンツMod**として再編する。

他のAMJ Modを導入しなくても、RimWorld + Grainsだけで「栽培 → 収穫 → 脱穀/殻取り → 可食穀粒 → 必要に応じて製粉 → 最低限の粉食」まで成立させる。

発酵・酒造・水利・温泉・派閥・イベント・豆類・繊維・根菜はGrainsの自己完結条件に含めない。MO併用時はMOの小麦・粉・石臼・Straw等を条件付き公式互換から再利用する。

### 鉄資源を前提にしたAMJ側コスト設計

Core自身は鉄鉱床・砂鉄等の**供給量や生成分布を変更しない**。一方で、Coreを含むAMJ側の設備・レシピ・加工経路は、**鉄を潤沢な汎用建材として浪費しない**ことを前提にコスト設計する。

ただし、**鉄を不足させること自体をゲーム目的にはしない**。希少性を導入するのは、それが「何に鉄を使うか」「何を別素材で代替するか」「採掘・砂鉄・交易のどの供給経路を選ぶか」といった判断を生み、プレイの違いにつながる場合に限る。単に必要量に対して供給を減らし、待ち時間・作業量・詰まりだけを増やす調整は避ける。

方針:
- 日本側で木・石・土・竹等による現実的な代替が成立する設備は、鉄を必須にしないか、使用量を抑える
- 刃物・金具等、機能上鉄が必要な箇所へ重点的に鉄を使う
- 同じ役割を持つMO側の西洋的設備・工程とAMJ側ルートが併存する場合、**AMJを導入しているならAMJ側ルートを選ぶことに資源上の意味がある**バランスを許容する
- 通常AMJ環境ではMO側ルートを強制削除せず、鉄消費・材料構成・工程差によってAMJ側を自然な選択肢にする
- Japanizationでは、MO側の西洋的ルートを日本の同等技術へ再解釈できる場合は研究/名称/外観を置換し、対応する意味がなく除去しても進行が成立する場合は無効化・非表示化できる。独立した日本側ゲームループの追加は各所有Modの責務とする
- 最低限の砂鉄供給・製鉄はIronmakingが所有する。既存鉱床の希少化・大規模地域分布変更はCoreでもIronmaking導入時の標準変更でもなく、将来の資源分布Mod候補として保留する
- **修理・再利用そのものは日本固有要素ではないためCoreの責務にしない**。既存の汎用修理Mod（R⁴等）または必要時のみ独立したRepair & Reuse機能枠で扱う
- **AMJの資源バランスはRepair & Reuseなしでも成立させる**。同Modによる修理・素材回収を前提に、鉄・布・革等の供給量やAMJレシピを不足側へ追い込まない
- Repair & Reuseは資源効率・継戦能力・装備寿命を改善する**強く推奨する補助システム**であって、AMJ進行を成立させるための隠れた必須依存にはしない
- 鉄が不足したときは、**代替素材・低鉄消費のAMJ設備・砂鉄・採掘・交易・優先順位付け**など、複数の対処経路を持たせる
- 鉄の希少性によって「どの設備を先に作るか」「武具へ回すか農具へ回すか」「現地調達を続けるか交易へ頼るか」等の選択が生じることを狙う
- どの経路を選んでも恒常的な待機や単純作業だけが増える状態、または鉄不足によってMO/AMJの主要進行が事実上停止する状態は、**バランス失敗**として扱う

これにより、Ironmakingや資源分布Mod未導入でもAMJ側の設備・工程は鉄を節約する設計として成立する。Ironmakingは任意の砂鉄・製鉄経路を追加し、既存供給を強制的に減らさない。Repair & Reuseを併用すれば資源循環は改善するが、未導入でもAMJの基本的な生活・生産・進行は破綻しない。

### Repair & Reuse / 修理・再利用Mod（仮）

Grainsは修理・再利用を所有しない。独自実装の要否とR⁴ / Simple Mending比較はProjectの [RepairReuseCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/RepairReuseCandidate.md) を正本とする。
### Core標準Scenario

> **Grains移行注記:** 作者承認により最終所有先は開始シナリオ専用の独立Modとする（上の独立Mod化節）。物理移行までは現パッケージに暫定保持。step 2でBaseと条件付きMO差分を実装した。以下のAlpha表はMO併用時の既存互換契約、Base物資表はMOなし構成の契約とする。Scenario/Faction/PawnKindの既存DefNameを維持する。ScenarioはGrainsの主要機能ではない。

現行公開CoreのScenarioは **「新しい村」 / New Village**（`AMJC_NewVillage`）とする。様々な事情で元の共同体を離れた一般の人々が、新しい土地で小さな村を興す。武将・大名・特権階級の開始にはしない。

#### Alpha開始条件（2026-10-04）

| 項目 | 初期条件 | 意図 |
|---|---|---|
| 人数 | 候補8人から5人を選ぶ | 畑作・調理・建築を分担できる小共同体 |
| 到着 | Standing（徒歩で到着した状態） | 通常の地上開始 |
| プレイヤー派閥 | `AMJC_PlayerVillage`、Medieval | 中世研究を進められる村の技術水準 |
| 基本PawnKind | `AMJC_Villager`、Human | 一般住民。技能・情熱・特性・年齢は固定しない |
| 背景 | Vanilla/MOのTribalフィルタ | AMJ Backgroundsなしで生成できる暫定基盤 |
| 衣服 | Neolithic / MOのDankPyon_Peasantタグ、Cloth素材 | 一般住民向けの通常生成。戦闘装備一式を与えない |
| 技術由来Hediff | 自動付与確率0 | SFインプラントの自動付与を避ける |
| 初期研究 | `DankPyon_Lumber`、`DankPyon_RusticFurniture`、`DankPyon_BasicCooking`の3件 | 基本木工・素朴な家具・初期料理を生活の土台とする |
| 研究タグ / Techprintタグ | 空 | MO中世開始・部族開始タグ経由で研究を追加しない |
| キャラバン採集係数 | 1.0 | 部族開始の採集倍率を追加しない |
| 家畜・ペット | なし | 初期の飼育負担を増やさない |

開始人数と「生活に必要な技術だけ」の方針は作者選択。研究3件と物資の具体値はAlpha実装の初期バランスとして下記に定め、開始の遊び心地を見て調整する。

石切り・蝋燭・鞣し・ペミカン・植林・農業・醸造・鍛造等は初期完了にしない。既存派閥の `startingResearchTags` を引き継ぐ代わりに、Scenarioの `ScenPart_StartingResearch` で3件だけ指定する。基本農業未研究でもアワ・ヒエ・キビ・ソバを栽培し、木10で簡易穀物加工場を建てて脱穀・脱殻できる。大麦・小麦・本格加工台は `DankPyon_BasicAgriculture` 研究後に進む。

#### 初期物資

| DefName | 数量 | 用途 |
|---|---:|---|
| `DankPyon_MealRations` | 60 | 採集・狩猟・調理へ移るまでの携行食 |
| `AMJC_Millet` | 200 | すぐ調理できる雑穀 |
| `AMJC_RawMillet` | 100 | 簡易加工場で初期の脱穀・脱殻を体験する雑穀束 |
| `MedicineHerbal` | 20 | 当面の治療 |
| `WoodLog` | 200 | 加工済み木材。簡易加工場・住居等の立ち上げ |
| `DankPyon_RawWood` | 200 | 燃料・木材加工に使う原木 |
| `DankPyon_IronIngot` | 30 | 小量の金属備蓄。鍛造設備・武装を完成済みにしない |
| `Cloth` | 80 | 少量の布備蓄 |
| `Silver` | 150 | 小規模な交易の余地 |
| `Bow_Short` | 2 | 採集以外の食料調達・自衛 |
| `MeleeWeapon_Knife`（鉄インゴット製） | 2 | 簡単な近接武器 |
| `MeleeWeapon_Club`（WoodLog製） | 1 | 簡単な近接武器 |

#### Base開始条件・物資（2026-10-07）

Baseは初期研究0件、衣服タグNeolithicのみとする。人数・到着・派閥・背景・空研究タグ等は上表と共通。大麦と加工台は研究不要で、Steel 30を使う。step 3で小麦のBase栽培・製粉を追加した（実機未検証）。MO併用時は旧3研究、Peasantタグ、上の12物資と鉄製ナイフを条件付き差分で復元する。

| DefName | 数量 | 用途 |
|---|---:|---|
| `Pemmican` | 1080 | Vanilla携行食で初期栄養54を確保 |
| `AMJC_Millet` | 200 | 即時調理用雑穀 |
| `AMJC_RawMillet` | 100 | 初期一次加工用 |
| `MedicineHerbal` | 20 | 治療 |
| `WoodLog` | 400 | 木材と原木の備蓄400を単一Vanilla素材へ置換 |
| `Steel` | 30 | Vanilla金属備蓄 |
| `Cloth` | 80 | 布備蓄 |
| `Silver` | 150 | 交易 |
| `Bow_Short` | 2 | 食料調達・自衛 |
| `MeleeWeapon_Knife`（Steel製） | 2 | 近接武器 |
| `MeleeWeapon_Club`（WoodLog製） | 1 | 近接武器 |

Pemmicanは初期携行食のゲーム上の代理であり、日本中世の同名食を主張しない。MO食糧60×Nutrition 0.9 = 54に、Vanilla Pemmican 1080×0.05 = 54を合わせる。耐久・嗜好・市場価値まで等価とはしない。ペミカン研究は与えず、ロード後の栄養値はruntime assertionで検証する。実機の開始体験・食糧日数は未検証とする。

物資は全て開始地点へ `ScenPart_StartingThing_Defined` で与え、追加の全域散布や隠れた初期物資は設けない。建築済み設備・コンポーネント・石材・追加鎧は与えない。持ち込んだ食料だけで初回収穫や冬越しが保証される量にはせず、早期の採集・狩猟・作付けを必要とする。寒冷地・冬開始など、どの環境でも成立することは保証しない。

#### 責務と互換

- 最終所有者は開始シナリオ専用の独立Mod。現CoreによるScenario・開始用プレイヤーFaction/PawnKindの供給は移行までの暫定措置。NPC派閥群を追加するAMJ Factionsとは別責務。
- Vanilla/MOの既存Scenario・Faction・研究タグ・PawnKindは書き換えない。AMJCのScenario以外の開始条件を変更しない。
- AMJ Backgroundsなしで動作する。導入時のAMJ背景優先生成は将来の互換作業で扱い、Alphaでは実装済みとしない。
- 日本風の衣装・固有背景・種族選択を強制しない。標準PawnKindは人間であり、HAR種族別開始の対応はこのScenarioの完了条件に含めない。
- Scenarioの初期条件は新規開始に適用する。既存セーブの人数・物資・研究は変更しない。
- このScenarioで作成したセーブはAMJC独自Faction/PawnKindを参照するため、Core削除の安全性は保証しない。

#### 自動テスト

静的検証は人数・到着方法・初期研究（Base 0件 / MO 3件）・研究タグの空集合・物資/素材・日本語表示と設計の一致を確認する。ローカル検証では実際のRimWorld 1.6/MO 1.6の参照Def・ScenarioBase・PlayerFactionBase・BasePlayerPawnKindも確認する。

Pickleには読み込み後のScenario/Faction/PawnKind検証と、実Scenarioを選択する `AmjNewVillageQuickstart` による開始検証を追加する。後者は5人の生成・開始派閥・プロファイル別初期研究のみの完了・開始物資数量/素材・未研究で利用できる簡易加工経路を確認する。物資の定義数量は厳密一致、生成済みマップでは別途生成される品を許容して必要量以上の存在を確認する。移行中の旧fixture suiteは8件、実providerの4プロファイルは各5件であり、隔離ログERRORゲートを使用する。物理分離時には開始検証を開始シナリオModへ移し、Grains単独にScenarioを要求しない。MOは既存方針どおり軽量XML fixtureで参照を供給するため、これをMO全体の統合テスト成功とは扱わない。実ゲーム開始テストの成功が確認されるまでAMJ-015はIN PROGRESSを維持する。

調査基盤は添付MO 1.6の `Defs/Scenarios`、`Defs/FactionDefs/Factions_Player.xml`、`Defs/PawnKindDefs_Humanlikes/PawnKinds_Player.xml` とRimWorld Dataの1.6形式（OdysseyのsurfaceLayerを含む）である。Quickstarts/Pickleの接続仕様は各開発元のソースで確認する。手動確認は日本語UIと開始の遊び心地に限定する。

### 最初の公開Alphaテーマ

**「古代～中世前期日本の畑作・雑穀農業OH」**

Grainsの公開・依存解除に鉄資源ModやIronmakingの同時公開を要求しない。**Ironmakingは独立開発・任意導入**とし、最低限の砂鉄供給・製鉄を所有する。旧Japanese Iron Resourcesの同時公開案は撤回し、既存鉱床の地域化だけを将来候補として再評価する。

最初の公開Alphaでは、まず**水田を必要としない畑作作物**を中心に完成させる。

最優先目標は、

> バニラ/MOの「最も効率のよい一種類を大量栽培する農業」から、  
> 気候・土地・季節によって作物を植え分ける農業へ変える。

こと。

#### Grainsの存在意義・存続条件

Grainsの存在意義は「日本の穀物Defを増やすこと」ではなく、**コロニーマップの環境条件に応じて主食穀物を選び分ける農業判断を成立させること**に置く。

- 土壌肥沃度、気温、生育可能期間、霜・低温耐性、収量、加工先等の組み合わせによって、代表的な環境ごとに有利な穀物が変わること
- ソバ/キビの短期・痩せ地適性、ヒエ/大麦の寒冷側、小麦の肥沃地・粉食価値、アワの標準～肥沃地での収穫回数削減等、既存の役割差を維持すること
- Environmentは土地・気候差を強く見せる推奨姉妹Modとするが、Grains単体でもVanillaマップ条件の範囲で可能な限り役割差が残ること
- 自動評価では複数の代表環境を使い、単一穀物がほぼ全条件で最適解になっていないことを回帰確認する
- 将来の調整で環境ごとの使い分けが実質的に消えた場合は、史実上存在するという理由だけで穀物数を維持せず、数値再調整・役割統合・削減を行う

この条件を満たす限り、Grainsは独立Modとして一旦十分なゲーム上の存在意義を持つものとする。

---

## 4. 最初の公開Alpha実装範囲

### 4.1 作物

最初の公開Alphaの中心作物は以下とする。

| 作物 | 主な役割 | ゲーム上の方向性 |
|---|---|---|
| 粟（アワ） | 標準畑の主力雑穀 | キビより生育は長いが1回の収量が多い。普通～高肥沃度の主力畑で、播種・収穫回数を抑えやすい |
| 稗（ヒエ） | 寒冷地向け雑穀 | 3種の中で低温側の成長域が広く、春秋・寒冷地で栽培期間を確保しやすい |
| 黍（キビ） | 最短期・低肥沃度向け雑穀 | 3種の中で最短期。肥沃度低下による成長減速も小さく、痩せ地や残り生育期間が短い状況に向く |
| 大麦 | 日常主食＋将来の加工用途 | 寒冷寄り。粒食可能。後に麦味噌・麦茶へ拡張 |
| 小麦 | 製粉・粉食向け | 粒食より加工価値を重視 |
| 蕎麦 | 短期・痩せ地向け | 成長が速く肥沃度依存が小さい。霜には弱め |

### 4.2 作物の差別化軸

単なる収量違いにはしない。

- 成長速度
- 最低成長温度
- 低温耐性
- 枯死耐性
- 最低栽培可能肥沃度
- 肥沃度感応度
- 必要栽培スキル
- 収量
- 保存期間
- 生食可否
- 一次加工先

**注意:**  
「低温に強い」を安易に「氷点下でも成長」にしない。  
冬越し・低温成長・霜耐性は別要素として扱う。

最初の公開AlphaではXMLだけで表現可能な範囲を優先する。低温枯死についてはCore独自のC#実装を重複して持たず、独立姉妹Mod **Crop Cold Tolerance Overhaul（CCTO）** が導入されている場合に、AMJ側の互換PatchからCCTOのXML-facing extensionを付与して固定枯死温度を設定する。CCTO未導入時も、AMJ PlantDef自身の成長速度・肥沃度・最低成長温度・加工等のCore仕様は成立させる。

AMJC固有作物の耐寒値と保存候補範囲の正本は [AMJC作物の耐寒データ](Balance/Crops/ColdTolerance.md) に置く。最低成長温度はAMJCのPlantDef、固定枯死・休眠はAMJC側の条件付き互換XMLが持ち、CCTOの実装予定表から参照・転載する運用は行わない。

### 4.2.1 Stage A畑作6作物の確定バランス

2026-10-01〜02のStage A詳細設計で確定していた数値を、現行公開版のMO併用プロファイルとCCTO独立姉妹Mod方針に基づく初期値として正本化する。**この表のMO研究名・小麦供給元は現行MO必須実装のスナップショットであり、Grains移行後の所有境界は §2.8 の最終Base / MO所有境界を優先する。** growDays・収量・肥沃度・温度等の6穀物バランス値は移行後も原則維持し、変更する場合は競合作物をまとめて再監査する。

| 作物 | growDays | 可食穀粒の基準収量 | fertilityMin | fertilitySensitivity | 成長可能温度 | 最適温度 | CCTO固定枯死温度 | sowMinSkill | 栽培解禁 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ソバ | 4 | 8 | 0.4 | 0.25 | 5～35℃ | 12～25℃ | -2℃ | 1 | 初期 |
| キビ | 5 | 11 | 0.5 | 0.3 | 8～42℃ | 18～32℃ | -3℃ | 0 | 初期 |
| アワ | 6 | 13 | 0.5 | 0.4 | 8～42℃ | 18～32℃ | -3℃ | 0 | 初期 |
| ヒエ | 6 | 12 | 0.5 | 0.5 | 5～40℃ | 15～30℃ | -2℃ | 0 | 初期 |
| 大麦 | 10 | 22 | 0.5 | 0.6 | 0～35℃ | 5～22℃ | -8℃ | 2 | MO `DankPyon_BasicAgriculture` |
| 小麦（MO） | 12 | 28 | 0.7 | 0.9 | 最低0℃。高温側はMO/RimWorld基準を維持 | MO/RimWorld基準 | -6℃ | 0（MO 1.6で明示なし） | MO `DankPyon_BasicAgriculture` |

アワ・ヒエ・キビについて、プレイヤーが「どの土地・気温・残り生育期間ならどれを植えるか」を判断できるよう、肥沃度・温度のゲーム内式を含む比較資料を [`Docs/Balance/Crops/Millet_Cultivation_Balance.md`](Balance/Crops/Millet_Cultivation_Balance.md) に置く。そこに掲載する数値・グラフは**現実の農業値ではなく、史実・農学的特徴を参考にAMJへ落とし込んだゲーム内バランス値**である。

補足:
- 収量列は、穀束・殻付き中間物を経由する場合も含めた**最終的な可食穀粒量のバランス基準**であり、PlantDefの未脱穀物 `harvestYield` をそのままこの値にするという意味ではない。未脱穀物の収量とRecipe変換比率は、この最終基準値を再現するよう実装時に決める。
- アワ・ヒエ・キビは栽培中のみ別PlantDefとし、収穫後は共通の「雑穀束」→殻付き雑穀→「雑穀」へ統合するため、収穫後の性能差を残さない。
- **現行MO必須版では**MO 1.6の `DankPyon_Plant_Wheat` を利用する。Grains移行後はBaseにフォールバック小麦Plant/穀束を持ち、MO併用時だけMO小麦を可視供給元として利用する。growDays 12、収量28、fertilitySensitivity 0.9、AMJ基準 `fertilityMin=0.7` の役割は両プロファイルで維持する。
- CCTO固定枯死温度は**CCTO導入時のAMJ互換値**である。AMJ CoreはCCTOを内部実装として複製せず、CCTOの `ColdToleranceExtension` を条件付き互換Patchから利用する。小麦はCCTOのMO 1.6バランス（最低成長0℃・固定枯死-6℃）をそのまま使う。
- 2026-10-04の再監査では、低温で成長できる性質と凍霜害への耐性を分離して評価した。キビは-3℃を維持、アワは-4℃から-3℃、ヒエは-4℃から-2℃へ改定した。詳細な根拠・確度は `Docs/Balance/Crops/ColdTolerance.md` を正本とする。
- CCTOの固定枯死判定は閾値未満（strict `<`）で発生するため、表の温度ちょうどでは生存する。

#### 穀物の保存期間・一次加工

Stage Aの穀物は、加工前後の保存性も作物選択と備蓄判断に使う。共通基準は **未脱穀穀束120日 → 殻付き穀粒120日 → 可食穀粒90日 → 粉60日** とし、ソバと小麦に下記の例外を持たせる。

| 作物 | 一次加工経路 | 保存期間 | 収穫直後の生食 |
|---|---|---|---|
| アワ / ヒエ / キビ | 雑穀束 → 脱穀 → 殻付き雑穀 → 殻取り → 雑穀 | 120日 → 120日 → 90日 | 不可。可食化は殻取り後 |
| 大麦 | 穀束 → 脱穀 → 殻付き大麦 → 殻取り → 大麦穀粒 | 120日 → 120日 → 90日 | 不可。可食化は殻取り後 |
| 小麦（MO） | 小麦束 → 脱穀 → 小麦穀粒 + `DankPyon_Straw` → 必要に応じてMO製粉 | 120日 → 90日。小麦粉は60日 | 不可。小麦は殻付き中間状態を省略 |
| ソバ | 穀束 → 脱穀 → 殻付きソバ → 殻取り → ソバ穀粒 | 120日 → 120日 → 60日。蕎麦粉を実装する場合は30日 | 不可。可食化は殻取り後 |

- 雑穀粉は具体的用途を追加する段階で実装し、その場合の保存期間は一般粉の60日を基準とする。
- 蕎麦粉は蕎麦切り・蕎麦がき等の用途とセットで追加し、Stage Aで用途がなければThingDefだけを先行追加しない。
- 大麦の製粉は具体的用途が必要になった段階で決める。Stage Aでは可食大麦穀粒までを基本経路とする。
- Straw副産物は製粉ではなく脱穀段階へ統一する。ただし `DankPyon_Straw` はMO併用時だけ出力し、BaseではStraw ThingDefを所有しない。
- **MO併用時は** `DankPyon_Plant_Wheat` / `DankPyon_RawWheat` を可視供給元として再利用し、`DankPyon_RawWheat` を未脱穀の小麦束として `DankPyon_Cereal` から外す。脱穀後の `AMJC_Wheat` だけをMO製粉へ接続する。BaseではGrains所有の小麦Plant/穀束を同じ `AMJC_Wheat` へ合流させる。
- MO 1.6標準では小麦収穫時の `Plant_SecondaryDrop` と製粉Recipeの両方でHayが生じるが、AMJでは収穫時副産物を外し、製粉側のHayも削除する。藁はAMJ脱穀Recipeでのみ `DankPyon_Straw` として発生させる。
- MO `DankPyon_Flour` の保存期間はAMJ共通粉基準に合わせて60日へ調整する。

この確定表は「一種類の最適作物」を作らないための基準である。短期・痩せ地はソバ/キビ、標準～肥沃な畑で収穫回数を抑える雑穀はアワ、寒冷側はヒエ/大麦、肥沃地で長期高収量・粉食は小麦、という役割差を維持する。

### 4.3 低肥沃度環境との接続

自然に生成される土壌品質・TerrainDef・マップ上の分布は、独立姉妹Mod **Ancient & Medieval Japan: Environment** の責務とする。Coreは自然Terrainを重複定義せず、**作物側の `fertilityMin` と `fertilitySensitivity` を所有する**。

Environment側の正本は `sucRo-RimWorld/Ancient-Medieval-Japan-Environment:Docs/Design.md §10 Natural soil fertility`。AlphaではVanilla/MOの既存地形を再利用しつつ、Environmentが耕作可能な `AMJ_ThinSoil`（fertility 0.50）を追加する。0.40の第二の極端な痩せ地TerrainはAlphaでは追加しない。

Core側では0.50を代表的な低肥沃度テスト点として扱う。Stage A確定値では:

| 作物 | fertilityMin | fertilitySensitivity | fertility 0.50で播種 | 肥沃度成長倍率 |
|---|---:|---:|---|---:|
| ソバ | 0.4 | 0.25 | 可 | 87.5% |
| キビ | 0.5 | 0.3 | 可 | 85% |
| アワ | 0.5 | 0.4 | 可 | 80% |
| ヒエ | 0.5 | 0.5 | 可 | 75% |
| 大麦 | 0.5 | 0.6 | 可 | 70% |
| 小麦（MO） | 0.7 | 0.9 | **不可** | — |

これにより、Environment併用時はThin Soil上で小麦を外しつつ、短期・低投入のソバ/キビほど減速が小さいというStage Aの土地適性がそのまま表れる。

ソバの `fertilityMin=0.4` は、Environmentへ0.40 Terrain追加を要求する値ではない。外部Terrain Mod・将来の土地設計との互換余地、および作物自身の最低条件として保持する。Environment側で0.40帯を追加するのは、0.50/0.70の既存段階では不足する具体的なゲームプレイ上の理由が確認された場合だけとする。

現行のCore + MOプロファイルでも穀物農業・一次加工は成立し、VanillaのGravel 0.70でも肥沃度感応度差は働く。GrainsのVanillaプロファイルでも同じ土地適性原則を維持する。EnvironmentはGrainsの必須依存ではなく、**自然地形分布によって土地選択をより強く表現する推奨姉妹Mod**と位置づける。

### 4.4 ワールド地形・Hillinessの責務

ワールドHilliness、標高、気候、河川、海岸線、およびそれらに連動する自然土壌分布は **Ancient & Medieval Japan: Environment** が所有する。Coreはワールド生成Patch・Hilliness補正・自然土壌GenStepを持たない。

以前のCore案にあった「Flat→Small Hills等を一定確率で昇格する」「Hillinessに応じてCore自身が痩せ地を生成する」という設計は廃止し、Environmentの実装・検証済み世界生成へ一本化する。具体的なHilliness比率、地形分布、生成アルゴリズム、検証値はEnvironmentリポジトリの `Docs/Design.md` を唯一の正本とし、Core側へ複製しない。

Coreが保持するのは、生成された土地条件に対して各作物がどう反応するかという農業バランスである。


---

## 5. 最初の公開Alphaの一次加工

完成料理を大量追加しない。

最初の公開Alphaで必要なのは、作物を既存の食事体系へ自然に流すための最小限の加工。

### 5.1 基本方針

- BaseはMO設備なしで穀束→可食穀粒→粉まで自己完結する。
- 脱穀・殻取りは既存AMJC穀物加工設備をGrains側設備として維持する。
- 製粉はGrains単体用の手動石臼を持ち、MO併用時はMO Millstoneへ差し替える。
- 粉食Recipeは研究不要とし、専用上位料理設備を要求しない。
- Baseの主要経路にMO ResearchDef / ThingDef / StuffCategory / ThingCategoryを直接参照しない。
- MO併用時だけ同等資産を条件付き互換から再利用する。
- 同一プロファイルに同目的のAMJ石臼とMO石臼、AMJ小麦とMO小麦、AMJ小麦粉とMO小麦粉を標準経路として並存させない。

### 5.2 Grainsで追加する一次加工の考え方

Baseの穀類フロー:
- アワ・ヒエ・キビ: 穀束 → 脱穀 → 殻付き雑穀 → 殻取り → 雑穀 → 必要なら雑穀粉
- ソバ: 穀束 → 脱穀 → 殻付きソバ → 殻取り → ソバ穀粒 → 蕎麦粉
- 大麦: 穀束 → 脱穀 → 殻付き大麦 → 殻取り → 大麦穀粒
- 小麦: 小麦束 → 脱穀 → AMJC_Wheat → 小麦粉

Baseでは脱穀時のStrawをThingDef化しない。MO併用時のみ上記脱穀Recipeへ DankPyon_Straw を副産物として追加する。

Grainsは小麦粉・蕎麦粉・雑穀粉を一次加工の出力として所有する。Baseの小麦粉はGrains所有、MO併用時だけ DankPyon_Flour を実Def供給元として利用する。蕎麦粉・雑穀粉はMO generic flourへ統合しない。

可食穀粒→粉の製粉では総栄養を原則保存し、製粉そのもので食料を増加させない。粉を作れるだけの状態にはせず、§5.3の最低限粉食へ接続する。

#### 穀物一次加工設備

- **簡易穀物加工場所 / AMJC_GrainProcessingSpot:** 初期から使える低速の脱穀・殻取り設備。
- **穀物加工台 / AMJC_GrainProcessingTable:** 同じ脱穀・殻取りRecipeを高速に処理する上位設備。BaseではMO研究・MO素材を要求しない。
- **Grains手動石臼:** Baseで小麦・ソバ・雑穀を製粉するAMJ所有設備。最低限の製粉経路はMO研究なしで成立させる。step 3初期実装は `AMJC_ManualMillstone`、BlocksGranite 30 + WoodLog 20、WorkToBuild 500。設備・製粉Recipeに研究前提は置かないが、石材の入手はVanillaの採掘・加工・交易等に依存し、全マップで初日建設できることは保証しない。
- MO併用時は DankPyon_Millstone を標準石臼として使い、Grains手動石臼は重複表示しない。
- MOのCraftingSpot手挽き等を残す場合も、未脱穀穀束から直接粉へ飛ばないようGrains工程順を維持する。
- x10等のBulk Recipeは単品処理より作業量を減らし、大量処理時のBill/Job負荷を抑える。
- Recipeの作業Skillは既存Stage Aとの互換を考慮し、移行実装時にBase/MO両プロファイルで統一して検証する。

### 5.3 完成料理

最初の公開Alphaでは専用料理を最小限にする。

優先順位:

1. 既存の「簡単な食事」等へ原料として利用可能
2. 既存料理ModのIngredientCategoryで利用可能
3. 歴史的・ゲーム的に必要な場合のみ専用料理を追加

#### Grains再編時の最低限の粉食

現CoreをGrainsへ再編して製粉まで自己完結させる場合、**粉を作るだけで食文化が西欧パンへ吸収されないよう、日本の古代～中世に根拠のある簡易粉食を少数だけ持つ。** 料理Mod化はせず、穀物の一次加工を食用へ接続するための最低限のRecipeに限定する。

- **餺飥（ほうとう系）** — 小麦粉を水で練って煮る前近代の粉食を代表させる。現代山梨の味噌・具材を固定した「ほうとう鍋」そのものではなく、平安期以来の餺飥系粉食をゲーム上1料理へ抽象化する。小麦は弥生期には存在し、鎌倉中期頃から稲の裏作としての栽培が進み、鎌倉～室町期には製粉具と小麦粉食の利用が拡大したため、中世小麦の主要用途として扱う。
- **そばがき** — 蕎麦粉を練って食べる簡易粉食。蕎麦切りを標準料理にせず、江戸以前のソバ利用として簡素な粉食を優先する。
- **雑穀団子** — 雑穀粉を水で練り、茹でる/蒸す類の粉食を1料理へ抽象化する。アワ団子・キビ団子等を別Recipeへ分割せず、共通雑穀粉の利用先とする。

小麦粉について、中世に存在した饅頭・うどん・素麺・麩等をすべてGrainsへ実装しない。饅頭は餡・菓子、麩は寺院/精進料理、麺類の高度化は追加の料理・加工体系へ広がるため、具体的なゲーム上の役割が生じた場合だけ後続機能で再検討する。

**Grains粉食の解禁・MOパンとのバランス原則:**
- 餺飥・そばがき・雑穀団子は**研究不要**とする。粉を作れる状態になった時点で利用可能にし、料理そのものへ追加研究ゲートを置かない
- 石窯等の専用上位設備は要求せず、既存の簡易調理設備で作れる日常粉食として扱う
- 代わりに、MOパンのような大きな栄養増幅・長い保存性・高い加工価値を与えない
- **Grains粉食はVanillaの「簡単な食事」相当を基準にしつつ、製粉という追加工程への小さな報酬としてMood等をわずかに上乗せする。** 初期バランス基準は粉0.5栄養相当 → 完成0.9栄養相当、Mood +2程度とし、栄養効率そのものはVanilla簡単な食事を大きく上回らせない
- 保存性はVanilla簡単な食事より短め（初期目安2～3日）を基本とし、「作り置きに強い上位食」にはしない
- MO 1.6のパンは粉0.25栄養からパン2個（合計0.8栄養）、作業量350、石窯とOven研究を要求し、8日保存できる。Grains粉食はこの効率を直接模倣せず、**研究不要・低設備・短保存・標準的な食料効率**を基本に差別化する
- Grains側の進行ゲートが必要な場合は料理Recipeではなく、作物・製粉設備・製粉工程側へ置く。粉を得た後に「その粉を簡単に食べる」ための追加研究は要求しない
- 正確な個数、workAmount、保存期間、Mood値は自動バランステストで微調整するが、**製粉で総栄養を増やさないこと**と、**粉食をパン級の栄養増幅へしないこと**は固定方針とする

---

## 5.4 Grains食材の料理接続対応表

| 食材 | Grains Base | MO併用時 |
|---|---|---|
| 雑穀 | 既存Vanilla食事へ使用可。必要に応じて雑穀粉へ製粉 | 同左。MO generic Cerealへ自動登録しない |
| 大麦 | 可食穀粒として既存食事へ | 同左。Generic Flour/Ale参加は意図がある場合だけ互換 |
| 小麦 | AMJC_Wheatを既存食事・Grains製粉へ | AMJC_WheatをMO製粉へ接続し DankPyon_Flour を得る |
| ソバ | 可食穀粒として既存食事へ。蕎麦粉へ製粉 | 同左。MO generic flourへ統合しない |
| 雑穀粉 | Grains粉食へ | 同左 |
| 蕎麦粉 | そばがき等のGrains粉食へ | 同左 |
| 小麦粉 | Grains所有のフォールバック粉 | DankPyon_Flour を標準小麦粉として利用 |

原則:
- Vanilla + Grainsだけでも「栽培できるが食べられない」「粉を作れるが用途がない」状態を作らない。
- アワ・ヒエ・キビは栽培中だけ別PlantDefとし、収穫後は共通雑穀チェーンへ統合する。
- 蕎麦粉・雑穀粉は小麦粉と別ThingDefを維持し、材料由来の料理差を表現する。
- 米・豆・根菜・繊維はこの表の対象外でありGrains所有ではない。
- MOカテゴリへの登録は、具体的なMO Recipeへ参加させたい場合だけ条件付きで行う。

## 6. MO併用プロファイル設計

この章は**MOを導入した場合の公式統合仕様**を定める。現行公開CoreではMOがまだ必須だが、依存監査・分離後はこの章を条件付きMO互換として維持する。

### 6.1 基本方針

MO併用時は、Grains Baseと同じ目的の設備・素材を二重に並べず、**MO資産を実Def供給元として差し替える公式互換**を行う。

- 小麦Plant/穀束: MO DankPyon_Plant_Wheat / DankPyon_RawWheat
- 脱穀後小麦: Grains AMJC_Wheat
- 小麦粉: MO DankPyon_Flour
- 石臼: MO DankPyon_Millstone
- Straw: MO DankPyon_Straw
- ソバ・大麦・雑穀および蕎麦粉・雑穀粉: Grains所有

MO資産を使っても、Grainsの工程順・6穀物バランス・粉食バランスは維持する。MO固有PatchはMO存在時だけ適用し、Base XMLからMO DefNameを参照しない。

### 6.2 MO研究ツリーとの統合

Grains Baseの主要ループはMO ResearchDefを必要としない。MO併用時の研究接続は追加の進行統合として条件付きで行う。

- Baseで栽培・脱穀・殻取り・最低限の手動製粉がMO研究なしで成立することを優先する。
- MO小麦やMO石臼に既存研究前提がある場合、Grains主要ループを止めるかを監査し、必要ならMO互換Patchで前提を調整する。
- 研究Tierを作物性能の帳尻合わせに使わない。
- MO全研究ツリーの全面改変はGrainsの責務にしない。
- 繊維・製紙・水利等、Grains外の研究統合は各所有Modが担当する。

### 6.3 稲作任意工程（Rice Cultivation設計・暫定引き継ぎ）

以下は**Rice Cultivation所有**の暫定引き継ぎであり、Waterworksの仕様ではない。このWaterworks作業ではこれ以上詳細化しない。

現時点で確定している最小事項:
- 稲作はWaterworksなしでも単体成立させる
- 稲の加工は雑穀と**同じ加工段階の型**を参考にするが、雑穀と同じThingDefへ統合しない
- 稲架掛けは必須工程ではなく任意ボーナス扱いとする
- **稲架掛け米は通常米とは別ThingDefとして維持する**
- 稲架、途中状態、歩留まり、保存性、必要時間、MO Drying Rack等との互換はRice Cultivation側で別途決める

### 6.4 稲から米への一次加工と保存性（Rice Cultivation設計・暫定引き継ぎ）

稲作は、他の殻付き穀物と**加工段階の構造だけを揃え、同じアイテムへ統合しない**。雑穀の `穀束 → 殻付き穀粒 → 可食穀粒` に対応して、稲作は独立した `稲束 → 籾 → 米` のThingDef列を持つ。籾は殻付き中間状態として独立ThingDefにし、玄米は独立ThingDefにせず、籾摺りから日常食用の米までを1工程へ抽象化する。**稲架掛け由来の米は通常の米とは別ThingDefとして維持する**が、その具体的な性能・工程はRice Cultivation側で別途検討する。

この変更により、籾には「すぐ食べられない代わりに殻付き状態で保存できる」というゲーム上の役割が生じる。工程を増やす目的は史実工程の網羅ではなく、**加工労働と保存状態のトレードオフを作ること**とする。

基本フロー:

- 通常系は `稲束 → 籾 + Straw → 米` の段階構造とする
- 稲架掛け系は通常系と同じ基本段階を使いつつ、**最終的な稲架掛け米を通常米とは別ThingDef**として扱う。途中状態・歩留まり・設備はRice Cultivation側で別途確定する

保存性は加工状態の差として扱う。

- **未加工・不可食の「稲」**を長期保存側に置く
- **殻付きの「籾」**を独立した保存状態として置く
- 籾摺り・日常精米をまとめた**可食の「米」**は殻付き状態より保存期間を短くする
- 将来の米粉は米よりさらに短くし、穀束 → 殻付き穀粒 → 可食穀粒 → 粉の段階差を維持する
- 保存期間の具体値、稲架掛け米の保存性ボーナス、途中状態の要否はRice Cultivation側で再確定する。Waterworks側では数値を所有しない

日常食用の通常米については、**うるち米・もち米をRice Cultivationでは別ThingDefに分けず、「米」へ抽象化する。** ただし稲架掛け米は通常米とは別ThingDefとして扱う。

将来、餅・団子・菓子等の具体的な料理機能を実装する場合も、もち米専用ThingDefを前提にせず、通常の「米」からRecipeとして用途を表現する。米を粉にする場合も、現実には米粉・道明寺粉・白玉粉など製法・粒度・原料米が異なるが、ゲーム上の用途差が小さい限り**1つの「米粉」**へまとめる。

これはMOの小麦粉が強力粉・薄力粉等を分けていないのと同じ抽象化方針とする。素材を分ける基準は現実の分類数ではなく、**別在庫として管理させるだけのゲーム上の選択・性能差があるか**とする。

将来の酒造では、この日常食用の米からさらに任意の追加精米・選別を行い、酒造用精白米を得る別工程を設けてよい。この追加加工はRice Cultivationの日常食用米を作る工程とは別物とする。**AMJの古代〜中世範囲では酒造専用品種のPlantDefを追加せず、同じ「米」から選別・精米して酒造向け原料を得る形へ抽象化する。** 酒造Addonでは必要に応じて、通常の酒造用米と、より多くの精米・選別・原料ロスを要求する上位の酒造用米を**別ThingDef**として持たせてよい。これは汎用的な食材品質システムではなく、酒造工程そのものの差として扱う。

酒造用精白米および上位の酒造用米は、**食べようと思えば通常の植物性食材として食べられ、一般料理にも使用可能**とする。ただし料理Ingredientとしての価値は通常の「米」と同じ**生野菜1相当**に留め、追加精米・選別を理由に栄養・料理価値・Mood等を上げない。酒造用米を作る段階で原料ロスと追加作業が発生するため、一般料理へ回すのは意図的にコストパフォーマンスが悪い選択となる。

米糠はRice Cultivationでは独立アイテム化しない。Fermentation Addon等で糠漬けなど明確な用途が生じた時点で追加を検討する。

### 6.5 稲藁・MO藁体系の統合方針（Rice Cultivation設計・暫定引き継ぎ）

稲専用の最終素材として「Rice Straw」を別Def化することは原則避け、MO側の共通 `Straw` 体系へ統合する。

想定フロー:

- 通常系と稲架掛け系の双方で、稲作固有のThingDef列を維持する。通常米と稲架掛け米は別ThingDefとし、藁のDef統合・歩留まり差・途中状態はRice Cultivation側で確定する

ゲーム上は、史実上の工程をすべて分解するのではなく、**脱穀と殻取りだけを別の判断として残し、玄米以降の細分化は省略する**。

目的:

- 稲藁専用Defの増殖を避ける
- 小麦・稲など異なる穀物由来の藁を、ゲーム上同じ基礎素材として扱う
- MO既存レシピとの接続をそのまま利用する
- 稲架掛けを任意ボーナスとして成立させる。具体設備はRice Cultivation側で決め、MO Drying Rackを必須前提にしない

実装前に現行環境のDefName・Recipe/Processor経路を監査し、MOの実装方法に合わせて接続する。

### 6.6 Def・カテゴリの所有方針

GrainsはBase主要ループに必要なDefを自分で所有し、MO併用時だけ同等資産の供給元を条件付きでMOへ差し替える。

**Grainsが常時所有**
- アワ・ヒエ・キビ・ソバ・大麦
- 各穀束・殻付き中間物・可食穀粒
- AMJC_Wheat
- 雑穀粉・蕎麦粉
- 脱穀・殻取りRecipe
- Base用製粉Recipe・最低限粉食Recipe
- Base用穀物加工設備
- 各穀物の栽培・保存・加工バランス

**Base用フォールバック**
- 非MO小麦Plant / 小麦束
- 非MO小麦粉
- 手動石臼

**MO併用時の供給元**
- DankPyon_Plant_Wheat / DankPyon_RawWheat
- DankPyon_Flour
- DankPyon_Millstone
- DankPyon_Straw
- 必要なMO研究・素材・カテゴリ接続

**Grainsが所有しない**
- AMJ独自Straw
- 米・水田
- 豆類
- 繊維・紡績・紙
- 根菜・一般野菜
- 塩・粘土等、Grains主要ループ外の横断資源

### 6.7 MO 1.6基盤資産の所有監査

| 分野 | MO側の正本 | Grains側の扱い |
|---|---|---|
| 小麦 | DankPyon_Plant_Wheat / DankPyon_RawWheat | MO時の可視供給元。GrainsバランスPatchを適用 |
| 小麦粉 | DankPyon_Flour | MO時の唯一の標準小麦粉 |
| 製粉設備 | DankPyon_Millstone、CraftingSpot手挽き、Windmill / Watermill系 | MO時に再利用。未脱穀束から工程を飛ばさない |
| 藁 | DankPyon_Straw | MO時だけ脱穀副産物として利用 |
| 穀物カテゴリ | DankPyon_Cereal | MO製粉/醸造へ参加させる対象だけ条件付き登録 |
| 農業研究 | DankPyon_BasicAgriculture 等 | Grains主要ループの必須依存にはしない |

#### DankPyon_Cereal は汎用穀物カテゴリとして使わない

MO 1.6では DankPyon_Cereal は製粉RecipeとAle wort Recipeの入力契約である。このため、Grains作物を「穀物だから」という理由だけで登録しない。

- DankPyon_RawWheat は未脱穀小麦束としてCereal入力から外す。
- 脱穀後の AMJC_Wheat はMO小麦粉へ接続するため登録してよい。
- 雑穀・ソバは専用粉を持つためgeneric Cerealへ登録しない。
- 大麦はMO generic Flour/Aleへ参加させる具体的な意図が確定した場合だけ登録する。
- Strawの発生点はカテゴリではなく脱穀Recipeで制御する。

#### MO紙・紡績等はGrains外

旧Core案にあった麻・カラムシ、MO Paper、Spinning Wheel、Paper Press等の統合は、Grains再編後はGrainsの責務ではない。設計知見は将来の繊維/Materials系機能の参考として保持してよいが、Grains BaseにもGrains-MO互換にも実装しない。

## 7. Food Drying 連携

Food Dryingは**必須依存にしない**。

ただし思想が合っているため、積極的に互換する。

### 屋根下乾燥の方針

**AMJ側で汎用の屋根下乾燥設備を新規追加する計画はいったん外す。**

- 一般食品の乾燥はFood Dryingへ任意互換する
- 稲架掛け等の稲作固有の任意工程はRice Cultivation側で別途設計する。MO既存Drying Rackは必須前提にしない
- 「屋根下でも使える日本式乾燥設備」という外観・利便性だけを理由に、既存乾燥システムと重複するBuildingを追加しない
- 将来、特定のAMJ生産物に既存設備では表現できない乾燥条件やゲーム上の選択が生じた場合だけ、その機能を所有するAddon側で専用設備を再検討する
### Grains側

- 乾燥システムを重複実装しない
- Food Dryingは `paseri.FoodDrying` の任意互換対象として扱い、存在確認付きPatchだけを使う
- 互換は**意味の合う乾燥先が存在する食材単位**で追加し、別作物の乾燥品へ便宜的に変換しない
- Stage Aの雑穀・大麦・小麦・ソバは、脱穀・殻取り後の穀粒自体が乾燥保存食であり、現行Food DryingのDried Rice等へ変換する利益より食材同一性の破壊が大きいため、公開Alphaでは互換対象外とする
- Food Dryingを導入しなくてもVanilla + Grainsの穀物農業は成立する

Food Drying 1.6はProcessor Frameworkを利用し、米・ジャガイモ・トウモロコシ・果物・きのこ等に専用の乾燥品を持ち、乾燥品から元食材へ戻す再水和経路も持つ。このため互換では入出力の意味を一致させることを必須条件とする。将来、山菜・きのこ・果実・根菜等を追加した段階で互換価値が大きくなる。

---

## 8. 最初の公開Alphaでは実装しないもの

### 8.1 米・水田（Rice Cultivationへ移管）

Coreでは実装しない。**水田・稲作はWaterworksからも分離し、独立したRice Cultivation Modとして後続実装する。**

理由:

- 水田
- 灌漑
- 水源
- 稲
- 脱穀
- 精米
- 稲藁

まで連鎖し、一つの大きなシステムになるため。

水利と稲作は責務と規模が大きいため**別Modへ分離する**。Waterworksは自然取水・用水路・分水・暗渠・引湯等の水利を所有し、Rice Cultivationは水田・稲・籾・米・稲作一次加工を所有する。両者は相互に必須依存せず、併用時だけ公式互換で接続する。

#### Waterworks / 水利Modの基本方針

WaterworksはGrainsとは独立した水利Modであり、正式な詳細設計は `sucRo-RimWorld/Ancient-Medieval-Japan-Waterworks:Docs/Design.md` を正本とする。Grainsは水田・水利を所有しない。

現行v1の最小境界:
- プレイヤーが素掘り水路を掘る
- 水路の連結成分が川・池等の有効な自然淡水へ上下左右で直接接していれば通水する
- 通水時は濡れた水路、非通水時は乾いた溝として表示する
- 水路は埋め戻せる
- 別個の取水口Building、水門、暗渠、温泉水区分、DBH Adapter等はv1必須ではなく、実際の利用先が必要とした段階でWaterworks側が再評価する
- Rice CultivationはWaterworksを必須依存にせず、併用時のみ任意接続する

### 8.2 大豆

大豆はGrains外。将来の所有先・発酵用途・既存大豆Modとの比較はProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) と [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) を正本とする。
### 8.3 発酵食品

Grains外。詳細候補はProjectの [FermentationBrewingPreservationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/FermentationBrewingPreservationCandidate.md) を正本とする。
### 8.4 酒造

Grains外。酒造・Sake / Morohaku候補はProjectの [FermentationBrewingPreservationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/FermentationBrewingPreservationCandidate.md) を正本とする。
### 8.5 漁業・貝塚

Grains外。一般釣りを重複実装しない方針と沿岸採集・貝塚候補はProjectの [HuntingGatheringCoastalCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/HuntingGatheringCoastalCandidate.md) を正本とする。
### 8.5.1 AMJ共通リテクスチャ方針

技術実装・既存リテクスチャMod監査・競合規則の共通正本は [`Docs/RetextureImplementationGuidelines.md`](RetextureImplementationGuidelines.md) とする。**AMJが所有する前提Mod資産は、AMJ固有texPathへ明示的にPatchする方式を標準とし、同名texture pathのロード順上書きだけには依存しない。** 対象は1枚のPNGではなく、実際にロードされたDefが使用するgraphic state一式として監査する。

AMJでいう**リテクスチャ**は、AMJ独自Defの画像制作だけを指さない。**各AMJ Modが、自分の責務範囲で使用・再利用するVanilla / Medieval Overhaul等の前提Mod資産についても、AMJ追加資産と並べた際に画風・輪郭・色数・陰影・情報密度・解像感が統一されるよう、必要なテクスチャをAMJ側から差し替えること**を含む。

目的は「前提Modを日本風に全面変換すること」ではなく、**各Modを導入したとき、そのModが担当するゲーム領域の見た目が一つのアートセットとして成立すること**である。

#### 所有原則

- **各AMJ Modは、自分の機能・景観責務に属する前提Mod資産の画風統一までを原則として所有する。**
- Coreは、Coreが直接扱う作物、食材、一次加工品、資源、農業・一次加工設備、Core責務の収納等について、Vanilla / MO等の既存テクスチャも必要に応じてCore内でリテクスチャする。
- Environmentは樹木・植物・地形・自然景観等をEnvironment側で所有する。Fermentation / Sake等のAddonも、それぞれが所有する工程・設備・容器等の前提資産を自Mod内で統一する。
- **同一Def / 同一前提資産のテクスチャを複数のAMJ Modが競合して上書きしない。AMJ内で1資産1所有Modを原則とする。**
- 所有先が曖昧な場合は、その資産の**主要なゲーム上の責務を持つMod**を正本とする。単に先に作業したModへ置く、ロード順で勝たせる、といった運用はしない。
- 1つの前提資産が複数Modから広く利用され、自然な所有先を決められない場合だけ、共通Retexture Modへの分離を再検討する。**前提資産をリテクスチャするという理由だけで最初から専用Retexture Modへ集約しない。**

#### 変更範囲

- 純粋なリテクスチャでは、対象Defの機能、容量、Recipe、カテゴリ、研究、数値バランス等を変更しない。必要なXML Patchはgraphic / texPath等の表示差し替えに限定する。
- 機能変更も必要な場合は、リテクスチャに便乗させず、その機能を所有する設計節・Modで別途仕様化する。
- 既存DefNameや外部参照は可能な限り維持し、前提Modとの互換性を壊さない。
- AMJ画風への統一が主目的であり、**全ての前提Mod画像を機械的に描き直すことは目標にしない。** AMJ追加物と並べて明確に浮く、頻繁に表示される、シリーズとして統一感へ大きく影響する資産を優先する。

#### 時代考証

- リテクスチャも通常のAMJ時代考証対象とする。
- 画風を揃えるだけなら元の機能・物体同一性を保つ。形状を日本の器物・建築・道具へ変更する場合は、その形態がAMJ対象時代に存在することを確認する。
- 「和風に見える」という理由だけで江戸以降の意匠へ置き換えない。
- 既存前提資産を歴史的に不適切な別物へ見せ替える必要がある場合は、単純リテクスチャではなく、Def追加・互換・除去等を含めて責務を再検討する。

#### 他Modとの境界

- **MO本体の日本化リテクスチャは `AMJ - Medieval Overhaul Japanization` が所有する。** AMJ独自Defの画像は各所有Modが引き続き所有し、同一MO資産を複数AMJ Modから競合上書きしない。
- 汎用の専用Retexture Modは標準構成では作らない。ただしJapanizationはMO全体を日本化するPatch Modであり、その責務の一部としてMO Retextureを同梱する明示的な例外とする。
- 外部Modそのものの配布物を改変・再配布するのではなく、AMJが権利上問題のない独自テクスチャを持ち、必要なPatchから参照させる。

#### 開発順

機能設計が不安定なAlpha段階ではプレースホルダーを許容するが、**公開版で担当領域の見た目を完成させる最終アート工程には、AMJ独自資産だけでなく必要な前提Mod資産のリテクスチャも含める。** 「前提Modの画像だから別作業」として無期限に後回しにはしない。


### 8.6 建築

Grains外。大型建築Addonを安易に作らず既存MO/和風家具を優先する横断方針はProjectの [ArchitectureAndReligionBoundaries.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ArchitectureAndReligionBoundaries.md) を正本とする。Grains固有の加工設備だけはGrainsが所有する。
### 8.7 宗教・価値観

Grains外。現在の境界記録はProjectの [ArchitectureAndReligionBoundaries.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ArchitectureAndReligionBoundaries.md) を参照する。
### 8.8 塩蔵

Grains外。塩蔵・非発酵保存候補はProjectの [FermentationBrewingPreservationCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/FermentationBrewingPreservationCandidate.md) を正本とする。
## 9. 将来のCore候補

v1以降にCore本体へ追加する候補。

### Core + Environment 自動ゲームプレイ評価方針

AMJでは「値が設計どおりロードされたか」だけでなく、**その値の組み合わせが実際に異なる選択肢を生んでいるか**についても、機械的に判定できる範囲は自動テストへ寄せる。

自動化対象:
- Stage A各作物の成長日数、収量、肥沃度最低値・感応度、成長温度、研究解禁、加工工程等の最終ロード値;
- 作物間の役割差が将来の調整で潰れていないこと。例として、短期作と高収量作、寒冷適応、痩せ地適応、研究前後の選択差を関係式として検証する;
- Environment併用時の実マップ土壌分布とCore作物の接続。自然土壌4段階で、薄い土壌を利用できる作物と利用できない作物が実際に分かれること、肥沃度感応度から実効成長倍率に差が出ることを検証する;
- Environmentの年間温度サンプルとCore/CCTO側の成長温度・枯死温度を接続し、暖地・温帯・寒冷地・高地の温度機会が同一化していないことを検証する;
- New Villageの開始人数・研究・物資・初期加工可能性;
- 加工時の数量保存、作業量、研究ゲート、食材カテゴリ接続、保存日数;
- 自動テストでRimWorldを起動する場合のERRORゼロゲート。

Stage Aでは、Pickleに**「作物の値が一致する」テストに加えて「作物の役割差が維持されている」回帰テスト**を置く。Core + Environment統合時はEnvironment側の固定バイオームQuickstartで実マップ土壌を生成し、Core作物の播種可能範囲と平均肥沃度成長倍率を評価する。

自動評価で扱わない / 最終的に人間の判断を残すもの:
- 画面上の統一感、シルエット、読みやすさ;
- 「選択肢が存在する」ことを超えた、面白さ・煩雑さ・テンポ・判断疲れ;
- 通常プレイでの長期的な体感、AI挙動や偶発イベントを含む総合的な村運営感;
- 日本語UIや説明文の自然さ。

したがって、手動プレイで最初に確認するのは「数値差があるか」ではなく、**自動テストで差が成立していることを前提に、その差が実際に面白い判断として感じられるか**に限定する。機械判定できる既知条件を毎回人間に再確認させない。

### Grains実装ロードマップ

Grainsの主要実装は、次の順で管理する。

| Stage | 主題 | 主な内容 | 現在の状態 |
|---|---|---|---|
| **Stage A / 現行実装** | 乾田穀物 | アワ・ヒエ・キビ・ソバ・大麦・MO小麦統合、脱穀・殻取り、穀物加工設備、New Village | MO必須版として実装済み |
| **Grains分離移行** | Vanilla自己完結 | 非MO小麦、小麦粉・蕎麦粉・雑穀粉、手動石臼、最低限粉食、BaseからMO参照除去、MO条件付き互換 | **step 3 小麦・製粉・最低限粉食XML実装・実機未検証** |
| **回帰固定** | 環境別穀物選択 | Base/MO/CCTO各プロファイルで単一穀物がほぼ全条件の最適解にならないことを自動確認 | 分離移行と同時に追加 |

旧Stage B（豆類）、Stage C（繊維）、Stage D（根菜）はGrainsロードマップから削除する。将来必要なら、それぞれの主要用途と自然な所有Modを決めて別途設計する。

### Grains外へ移した旧Core候補

旧Core由来でGrainsの所有外となった未所属候補はProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) に移管した。Grainsには「所有しない」という境界だけを適用する。
### 旧Core候補の履歴（Grains外）

履歴と再検討条件はProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) を正本とする。
### Grainsに入れない / 旧Coreで保留した農作物・植物

未所属・保留・不採用候補の詳細台帳はProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) へ移管した。Grainsの実装範囲は本書4章の乾田穀物に限定する。
### 冬季加工の拡張候補

Grains外の保存・発酵候補としてProjectの [DeferredPlantsAndProcessing.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/DeferredPlantsAndProcessing.md) へ移管済み。
### 既存Mod側を優先し、Coreは互換中心

採集・困窮食等の未所属互換候補はProjectの [HuntingGatheringCoastalCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/HuntingGatheringCoastalCandidate.md) と [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) へ移管した。Grains自身に必要な互換だけを本リポジトリで管理する。
### 別アドオン / 姉妹Mod寄り

AMJ全体の未所属・将来Mod一覧は `Ancient-Medieval-Japan-Project/Docs/Roadmap.md` を正本とする。Grainsでは自分の所有外であることと、必要な互換境界だけを記録する。
### Ironmaking / 古代・中世製鉄（2026-10-07 作者確定）

IronmakingはGrains外の独立Modコンセプト。専用リポジトリ作成前の設計正本はProjectの [IronmakingDesign.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/IronmakingDesign.md) とする。GrainsはIronmakingを必須依存にせず、必要な互換だけを将来条件付きで持つ。
## 10. 推奨バイオーム

初期の動作・バランス確認は以下3種に絞る。

- 温帯森林
- 温帯湿地
- 針葉樹林

目的:

- 日本列島に近い環境幅
- 温暖・湿潤・寒冷の差を作物性能へ反映しやすい
- 作物ごとの個性を確認しやすい

他バイオームでの動作は禁止しないが、v1の主要バランス対象にはしない。

Hilliness補正についてはバイオームとは独立したワールド側の基礎傾向として扱う。初期テストではFlat / Small Hills / Large Hills / Mountainousをそれぞれ含むワールドを生成し、平地の希少化と丘陵・山岳増加が過剰でないか確認する。

---

## 11. 互換対象の優先順位

### 基準環境

- RimWorld Vanilla
- Medieval Overhaul（公式互換・主要比較対象）

### 優先度A

- Medieval Overhaul互換の継続回帰
- Food Drying

### 優先度B

- Dubs Bad Hygiene
- Famine Food
- Vanilla Plants Expanded - More Plants
- Medieval Kingdoms: The Later Tang

### 優先度C

- ReGrowth 2
- RimImmortal / 仙路系
- Edo Themed Expansion
- MoeLotl
- Yuran
- VGP系
- その他竹・紙・農業素材Mod

### 評価待ちの互換候補

Grains以外の将来機能に関わる評価待ち候補はProjectの [ExistingModAudit.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) に移管済み。Grainsの具体的な互換対象として採用された時点で、本節ではなく対応するGrains互換設計へ戻す。
### Faction / Background系の互換方針

Faction / Background / Eventsの横断互換はGrainsの責務外。専用リポジトリ作成前の詳細方針はProjectの [SocietyModulesCandidate.md](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/SocietyModulesCandidate.md) を正本とする。Grains固有Defとの直接競合が発生した場合だけ、本リポジトリに互換仕様を追加する。
## 12. グラフィック方針

### 12.1 目標

Medieval Overhaulと並べても違和感が少ない、**ベクター画像的な整理されたゲームアート**を目標とする。

重視する特徴:

- 輪郭が明快で、シルエットだけでも判別しやすい
- 細かな筆致より、面の分割と色のまとまりを優先する
- 過度なテクスチャ・グラデーション・描き込みを避ける
- 木・石・金属などの材質は、細密表現より記号化して分かりやすくする
- RimWorldの斜め上視点で形状を読み取りやすくする
- 小サイズ表示でも情報が潰れないよう、要素数を絞る
- MO既存テクスチャの輪郭線、陰影量、彩度、情報密度を基準にする

「手描きらしさ」を目的にはせず、**ベクターで形を組み、必要最小限の陰影や質感を加えたような見た目**を基準とする。

#### 12.1.1 AMJ画風の正本

2026-10-03に、MOの実物テクスチャ（成熟小麦・Leather・Hide）との反復比較を経て、AMJの標準画風を確定した。以後の画像生成・手動作画では、**RimWorld VanillaではなくMedieval Overhaulのフラットさを基準**とし、詳細な再現ルールは `Docs/ArtStyle.md` を正本とする。

特に以下を固定ルールとする。

- 少数の大きな色面で構成し、グラデーションや写実的な陰影を使わない
- 太めの暖色系暗色輪郭を維持する
- 植物は「個々の粒・葉脈」よりシルエットを優先する
- アイテムは植物以上に陰影を減らし、1素材あたり基本色＋補助1面程度を目安にする
- MO小麦・Leather・Hideより情報密度が高くなった場合は、完成度を上げるのではなく情報を削る
- 生成時は比較表やUI画像ではなく、最終的に**透明背景の単独アセット**を出力する
- 256×256と約64px相当の両方で確認し、小サイズでの判別性を優先する

アワ成熟株で採用した「大きな穂形状・少数の葉・オリーブ系緑＋黄土系の穂＋共通暗色輪郭」を最初のスタイルアンカーとし、他の作物・収穫物・加工品も同程度の色数・陰影量・情報密度へ揃える。

#### 12.1.2 縦切り実装の画像完了条件

機能単位の縦切り開発では、成熟画像1枚だけを完成させて「画像完了」としない。**その実装でプレイヤーが通常見る主要な表示状態を一通り本番画像へ置き換え、ゲーム内で確認してから次の機能へ進む。**

作物の場合の基本確認対象:
- 未成熟状態
- 成熟状態
- 収穫直後のアイテム
- その作物専用または当該スライスで新規追加した主要中間素材・最終素材

ただし、複数作物が同じThingDefへ合流する場合は、同じ共有画像を作物ごとに重複制作しない。アワ・ヒエ・キビでは、栽培中のPlantDef画像は各作物ごとに持つが、収穫後の `雑穀束 → 殻付き雑穀 → 雑穀` は共有ThingDefとして一度だけ制作・確認する。

設備も、その機能でAMJ固有BuildingDefを追加した場合は仮画像のまま機能完了とせず、数値・動作確認後に本番画像へ置き換えて通常ズームで確認する。

これにより「仮画像で実装 → 動作/数値確認 → 主要な可視状態を本番画像化 → ゲーム内見た目確認 → 次機能」の順を守る。

### 12.2 制作環境

用途別に使い分ける。

**Krita**
- 作物・有機物など、多少の手描き調整が必要な素材
- 図形・選択範囲・変形を使った面構成
- 最終的な陰影・輪郭調整

**Inkscape等のベクターツール**
- 石臼
- 桶
- 作業台


### Grains 環境・実ジョブ回帰の追加（2026-10-07）

六穀の有限成長時間比較を `Docs/Balance/Crops/GrainsEnvironment.md` に定義し、
肥沃度3×温度3×季節3の27セルで成熟穀粒収量と勝者を回帰固定する。
全六穀に代表的な最大収量条件を残し、有効セルの2/3以上を単一穀物が占めない。
光量・休眠・労働・霜死・Straw価値を除いた分析モデルであり、リリースの環境ゲート全体は未完。
既存PlantDefの値・About依存・開始シナリオの分離方針は変更しない。

四プロファイルのPickleは穀物専用6シナリオ（開始シナリオ2件はScenariosへ移管）。ロード済みPlantUtilityの環境係数比較と、
New Villageに依存しないStage A Quickstart上の六穀の実収穫＋11回の加工・製粉・調理Billを追加する。
成熟株の配置を開始点とし、収穫物・加工品はテスト側で生成しない。
現在はC#ソースと起動配線の追加までであり、実ゲームのビルド・実行・ERROR 0は未検証。
実ジョブ経路と検証境界の正本は `Docs/GrainsProfileTesting.md`。


実ジョブの経路確認により、AMJ加工Spot/TableとBase手動石臼にWorkGiverの接続がないことを確認した。
共有 `AMJC_DoGrainProcessing` と非MO限定 `AMJC_DoGrainsMilling` を追加し、
CraftingのWorkGiver_DoBillから固定対象へ通常作業を割り当てる。
レシピのrecipeUsersだけではWorkGiver_DoBillの固定対象一覧へ追加されないため、両方を持つ。
MO石臼は既存MO WorkGiverを利用し、重複作業Defを追加しない。既存38契約は変更しない。


### 開始シナリオの分離と条件付き互換領域（2026-10-07）

`Scripts/prepare_scenario_extraction.py` と機械可読台帳から、本番を変更せずに
移行対応Grains／独立シナリオのテスト用パッケージを生成できる。
新シナリオが有効なときはGrainsの旧3Def・翻訳・MO開始差分をロードせず、
同名・同型のDefを新Mod側が一意に提供する。無効時はGrainsの互換用領域が提供する。
MO差分の後にGrains物資差分を適用し、Grains併用時の全明示契約は現行値と順序を維持する。

Vanilla/MO単独時の穀物代替は試案RawRice 300。正式名・packageId・専用リポジトリは確定済み。
Grains本番の3Def・5翻訳・MO開始差分は `LegacyStartingScenarios` へ移動し、
新Modが無効なときだけ提供する。穀物側のMO操作・既存38契約を維持する。
実行時テストソース・専用Quickstart・4構成ランナーはScenarios所有へ移管した。
Grainsの通常6件から専用Scenario要件を外し、旧fixtureの8件にはLegacy開始回帰を残す。
正式な単独バランス採用・C#コンパイル／ゲーム実行・セーブ移行の実測は未完了。改修前Coreのまま新Modと併用すると重複するため、
移行対応版への更新を先に行う。静的な一意性・契約一致は旧セーブ読込／安全な削除の実測を代替しない。
詳細と未完ゲートは `Docs/ScenarioExtraction.md`。
