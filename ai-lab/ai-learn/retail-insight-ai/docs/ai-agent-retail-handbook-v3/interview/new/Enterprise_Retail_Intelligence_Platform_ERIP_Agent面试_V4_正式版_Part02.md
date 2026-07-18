# Enterprise Retail Intelligence Platform（ERIP）
# Agent 面试指南 V4 正式版
## Part 02：Backend（FastAPI / Repository / JWT / RBAC）

---

- **Version**：V4.0 Official Edition
- **Document Type**：Interview Handbook
- **Language**：日本語中心
- **対象**：AI Engineer / Agent Engineer / Backend Engineer / Solution Architect / Technical Leader
- **前提**：Part01 の後に使用する

# 更新说明

本册は ERIP Backend を日本現場面接形式で整理した正式版である。

- すでに企業案件として完成した前提で記述する
- 将来計画・開発中・Phase 表現は使わない
- 各節は「面接官 → 回答 → 追問 → 回答 → Point」で統一する

---


> **位置付け**：Backend 深掘り备用资料。面试主线は Part01。

# 目录

## Chapter 2　Backend 全体像
- 2.1 Backend の役割
- 2.2 レイヤ構造
- 2.3 呼び出しチェーン
- 2.4 設計理由

## Chapter 3　FastAPI
- 3.1 なぜ FastAPI
- 3.2 実装範囲
- 3.3 Flask / Django 比較
- 3.4 OpenAPI

## Chapter 4　Router
- 4.1 責務と禁止事項
- 4.2 主要 Router とバージョン

## Chapter 5　Service
- 5.1 Service の役割
- 5.2 代表 Service と Workflow 境界

## Chapter 6　Repository Pattern
- 6.1 定義と採用理由
- 6.2 Interface・主要実装

## Chapter 7　Dependency Injection
- 7.1 DI と Depends
- 7.2 テストとの関係

## Chapter 8　Pydantic / Exception
- 8.1 Validation
- 8.2 例外と request_id

## Chapter 9　PostgreSQL / Transaction
- 9.1 なぜ PostgreSQL
- 9.2 トランザクション
- 9.3 Alembic / pgvector

## Chapter 10　InMemory と切替
- 10.1 InMemory の位置
- 10.2 切替設計

## Chapter 11　JWT
- 11.1 JWT の役割
- 11.2 claims と期限

## Chapter 12　RBAC / Permission / CurrentUser
- 12.1 認証と認可
- 12.2 ロールと Permission
- 12.3 実装位置と CurrentUser

## Chapter 13　業務別呼び出し
- 13.1 文書登録
- 13.2 RAG と承認

## Chapter 14　TL 深掘り
- 14.1 層を守る理由
- 14.2 障害・性能・セキュリティ

## Chapter 15　クロージング
- 15.1 30秒 / 2分

---

# Chapter 2　Backend 全体像

## 2.1 Backend の役割

## 面接官

ERIP の Backend は何を担当していますか。

## 回答

ERIP の Backend は、企業向け AI 経営分析プラットフォームの中核です。

認証・認可、文書管理、検索、AI 分析の起動、レポート生成、承認、監査を API として提供します。
Frontend は画面と操作、Backend は業務ルール・権限・データの正しさを担当します。

## 追問

責任分界を一言で説明してください。

## 回答

Frontend は UX、Backend は業務整合性・権限・永続化です。
画面でボタンを隠しても、API 側で権限とバリデーションを必ず実施します。

## Point

- Backend = 業務 + 権限 + 永続化
- セキュリティ境界は API

【面试技巧】

先に『何を守るか』を言い、技術名は後から。

---

## 2.2 レイヤ構造

## 面接官

なぜ Router / Service / Repository に分けましたか。

## 回答

責務分離と変更影響の局所化のためです。

Router は HTTP、Service は業務、Repository は永続化です。
API 変更、業務変更、DB 変更を独立して扱えます。

## 追問

分けないと何が起きますか。

## 回答

Router に SQL や承認判定が混在し、テスト困難・権限漏れ・重複が増えます。
DB 変更時に API 全体改修が必要になります。

## Point

- 目的は保守と安全
- 変更を切り離す

---

## 2.3 呼び出しチェーン

## 面接官

Backend 呼び出しチェーンを説明してください。

## 回答

```text
React → FastAPI → Router → Service → Repository → PostgreSQL
```

JWT 認証、CurrentUser 確定、Permission 認可の後、Service が業務を実行し、Repository が PostgreSQL へ保存・取得します。

## 追問

RAG や Workflow はどこに入りますか。

## 回答

Service 配下です。

```text
Service → Workflow / Retrieval / LLM Gateway → Repository
```

AI 処理があっても永続化境界は Repository に統一します。

## Point

- 主鎖を先に暗記
- AI は Service 配下

【学习提示】

面试先背主链，再讲 RAG/Workflow 分支。

---

## 2.4 設計理由

## 面接官

なぜこの設計にしたのですか。

## 回答

権限、監査、承認、永続化、テスト容易性が必須だったためです。
単一ファイル API では安全に拡張できません。

## 追問

最大のメリットは。

## 回答

変更耐性です。認証強化や Repository 実装切替でも、Service の公開面を安定維持できます。

## Point

- 企業要件が根拠
- 長期保守

---

# Chapter 3　FastAPI

## 3.1 なぜ FastAPI

## 面接官

なぜ FastAPI を採用しましたか。

## 回答

Python で AI/RAG/Workflow を実装しつつ、企業 API の堅牢性が必要でした。
非同期、Pydantic 検証、OpenAPI、DI が標準で揃い、契約を明確に保てます。

## 追問

性能だけが理由ですか。

## 回答

いいえ。主目的は開発速度と API 契約の明確化です。Frontend/Backend の齟齬を減らす実務価値があります。

## Point

- AI と業務 API の統合
- 契約明確化

【容易说错】

『流行だから』は失分。

---

## 3.2 実装範囲

## 面接官

FastAPI で何を実装しましたか。

## 回答

認証、文書、RAG/分析、レポート、承認、管理（AI Runtime）、ヘルス/レディネスです。
統一例外、request_id、権限制御を Middleware と Depends で共通化しました。

## 追問

最重要 API は。

## 回答

業務は文書→検索→レポート→承認の一連。基盤は JWT/RBAC と監査が同等に重要です。

## Point

- 業務と基盤の両輪

---

## 3.3 Flask / Django 比較

## 面接官

なぜ Flask や Django ではないのですか。

## 回答

どちらも優秀です。ただし ERIP は React + API 中心で、Schema 駆動と DI、AI 統合を標準化したかったため FastAPI が適合しました。
Flask は小規模/既存資産、Django はフルスタック画面中心案件で強みがあります。

## 追問

DRF では駄目ですか。

## 回答

可能です。今回は AI エコシステム親和性と Pydantic 契約を優先して FastAPI を選びました。

## Point

- 否定せず適合性で比較

【面试技巧】

比较题は相手技術を肯定してから适配性を話す。

---

## 3.4 OpenAPI

## 面接官

OpenAPI はどう使いましたか。

## 回答

API 契約の共通言語として、実装参照・結合確認・障害時仕様確認に使います。

## 追問

本番で Swagger 公開しますか。

## 回答

環境制御します。本番は情報露出を制限し、開発検証では活用します。

## Point

- OpenAPI = 契約

---

# Chapter 4　Router

## 4.1 責務と禁止事項

## 面接官

Router の責務と、書いてはいけないことは何ですか。

## 回答

責務はパス定義、受信、認証認可適用、Service 呼び出し、レスポンス返却です。
直接 SQL、複雑な業務判定の本体、LLM 詳細実装、監査実装の散在は書きません。

## 追問

Permission を Router で見るのは正しいですか。

## 回答

正しいです。入口で不足なら Service を呼びません。状態依存の細かい判定は Service でも実施します。

## Point

- 薄い Router
- 入口で AuthZ

【容易说错】

『完全不校验』も誤り。

---

## 4.2 主要 Router とバージョン

## 面接官

主要 Router と API バージョン方針は。

## 回答

認証、文書、RAG/分析、レポート、承認、管理、ヘルスです。
`/api/v1` で互換性を管理し、破壊的変更時にバージョン戦略を使います。

## 追問

管理系を分ける理由は。

## 回答

権限境界の明確化です。AI Runtime 等は強い Permission を要求します。

## Point

- 機能境界 = 権限境界

---

# Chapter 5　Service

## 5.1 Service の役割

## 面接官

Service 層の役割は何ですか。

## 回答

業務ユースケースの実行単位です。妥当性確認、追加判定、Workflow 起動、保存、監査調整を行います。
HTTP 詳細を知らずに業務を完遂します。

## 追問

Repository を Router から直接呼ぶ問題は。

## 回答

業務ルールが散らばり、承認などの複雑判定が重複・修正漏れします。
Service で単一実行経路を作ります。

## Point

- ユースケース調整
- 単一経路

---

## 5.2 代表 Service と Workflow 境界

## 面接官

代表 Service と Workflow の境界は。

## 回答

Document / Retrieval / Task / Approval など業務境界で分割します。
単純 CRUD は Service+Repository、多段・状態遷移は Workflow です。全部 Workflow にすると過剰です。

## 追問

肥大化したら。

## 回答

業務境界で分割し、必要なら Workflow へ委譲。循環依存は避けます。

## Point

- 単純は Service
- 多段は Workflow

---

# Chapter 6　Repository Pattern

## 6.1 定義と採用理由

## 面接官

Repository Pattern とは何ですか。なぜ必要でしたか。

## 回答

業務から保存詳細を隠す永続化境界です。Service は意図だけ呼び、SQL に依存しません。
テスト容易性、InMemory/PostgreSQL 切替、業務コード安定化が採用理由です。

## 追問

DAO と同じですか。

## 回答

近いですが、業務単位の操作（例：承認履歴込み保存）を提供する境界として設計します。

## Point

- 永続化境界
- 切替可能性

---

## 6.2 Interface・主要実装

## 面接官

Interface 分離と主要 Repository は。

## 回答

Service は Interface 依存、InMemory/Postgres を DI 注入します。
Document、Chunk、Task、Report/Version、Approval、Audit、AI Runtime 等が中心です。

## 追問

Prompt を DB 代わりにしますか。

## 回答

しません。監査可能な業務事実（誰が何を承認したか、根拠文書）は Repository に永続化します。

## Point

- 業務事実は DB
- 過剰抽象しない

【学习提示】

状态在哪里 → 永远是 Repository/DB。

---

# Chapter 7　Dependency Injection

## 7.1 DI と Depends

## 面接官

DI と FastAPI Depends を説明してください。

## 回答

依存を利用側が new せず外部注入する設計です。
Depends で CurrentUser、Permission、Service、Repository を注入し、差し替えと再利用を容易にします。

## 追問

Middleware との違いは。

## 回答

Middleware は横断処理、Depends はエンドポイント単位の明示依存です。組み合わせて使います。

## Point

- 差し替えとテスト
- 標準機能を活用

---

## 7.2 テストとの関係

## 面接官

DI はテストにどう効きますか。

## 回答

DB や外部 LLM を差し替え、権限・状態遷移・エラー処理を高速検証できます。
単体と結合の役割分担で品質を支えます。

## 追問

結合テストは不要か。

## 回答

必要です。単体で業務を守り、結合で API→DB 経路を確認します。

## Point

- 単体 + 結合

---

# Chapter 8　Pydantic / Exception

## 8.1 Validation

## 面接官

Pydantic と Request/Response 分離の理由は。

## 回答

不正入力を入口で拒否し、契約をコードで強制するためです。
Request は最小入力、Response は確定情報。Entity 生返却は内部変更が外部破壊になるため避けます。

## 追問

失敗時は。

## 回答

400 系と統一エラー形式。詳細はログ、クライアントは必要十分、request_id で追跡。

## Point

- 契約と防御
- Entity 生返却しない

---

## 8.2 例外と request_id

## 面接官

統一例外処理と request_id の意義は。

## 回答

エラー契約を統一し Frontend/運用を安定させます。
ビジネス例外（権限・状態）とシステム例外を分け、業務エラーを安易に 500 にしません。
request_id は HTTP 追跡、task_id は業務追跡です。

## 追問

スタックトレースは返すか。

## 回答

返しません。サーバログのみです。

## Point

- 例外分類
- 通信追跡と業務追跡

【容易说错】

业务错误一律 500 は失分。

---

# Chapter 9　PostgreSQL / Transaction

## 9.1 なぜ PostgreSQL

## 面接官

なぜ PostgreSQL を正式ストアにしましたか。

## 回答

関係整合性が必要な業務データ（文書・承認・監査・権限）を扱うためです。
ACID と運用実績があり、pgvector でベクトル検索も同一基盤化できます。

## 追問

AI だから DB は軽くて良い？

## 回答

誤りです。AI があるからこそ根拠と承認を厳密に残す必要があり、DB 重要性は上がります。

## Point

- 正式 = PostgreSQL
- AI でも RDB 必須

---

## 9.2 トランザクション

## 面接官

トランザクションで何を守りますか。

## 回答

複数更新の原子性です。承認では状態・履歴・監査・版数を整合させます。
外部 LLM 呼び出し自体を長時間 TX で囲まず、結果反映の更新を TX で守ります。

## 追問

部分更新をどう防ぐか。

## 回答

TX 境界、状態機械、一意制約、楽観ロック（expected_version）を組み合わせます。

## Point

- 原子性
- 外部 I/O と TX を分離

---

## 9.3 Alembic / pgvector

## 面接官

マイグレーションと pgvector の位置付けは。

## 回答

Alembic でスキーマ変更を履歴管理し、手作業適用を避けます。
pgvector はチャンク埋め込みの類似検索用で、当面は運用複雑性を抑える一体構成です。

## 追問

専用 VectorDB は。

## 回答

規模・性能要件で検討。現設計は要件充足と運用負荷のバランスです。

## Point

- 履歴管理
- 一体運用

---

# Chapter 10　InMemory と切替

## 10.1 InMemory の位置

## 面接官

InMemory Repository とは何ですか。

## 回答

Interface のテスト/開発補助実装です。正式業務データの保存先ではありません。
正式環境は PostgreSQL です。

## 追問

面接での正しい言い方は。

## 回答

『正式は PostgreSQL。InMemory は自動化テスト用実装』と対で説明します。片方だけだと誤解されます。

## Point

- 正 = PostgreSQL
- InMemory = テスト

【面试技巧】

先说正式路径，再补充测试适配器。

【容易说错】

线上也是 InMemory と言わない。

---

## 10.2 切替設計

## 面接官

Repository 切替はどう実現しますか。

## 回答

Service は Interface 依存、DI と設定で実装注入します。
分岐は組成箇所に閉じ込め、業務メソッド内に if を散らしません。

## 追問

設定ミス対策は。

## 回答

起動時ログとヘルス可視化、非永続実装の誤運用ガードです。重要業務は必ず PostgreSQL で検証します。

## Point

- 組成箇所に閉じ込める
- 可視化とガード

---

# Chapter 11　JWT

## 11.1 JWT の役割

## 面接官

JWT を説明し、採用理由を述べてください。

## 回答

認証トークンです。ログイン後に発行し、各 API で利用者を識別します。
API/SPA 分離構成に適合し、識別後に RBAC で認可します。

## 追問

セッション方式との違いは。

## 回答

トークン検証中心で進めやすい一方、失効・鍵管理は別途設計が必要です。方式名より AuthN/AuthZ 分離が本質です。

## Point

- JWT = Authentication

---

## 11.2 claims と期限

## 面接官

JWT に権限を全部詰めますか。期限はどうしますか。

## 回答

詰めすぎません。主に識別、認可は RBAC。最小 claims、機密非搭載です。
期限は UX と漏洩リスクのバランス。漏洩時は鍵管理・失効・HTTPS・最小権限で多層防御します。

## Point

- 最小 claims
- 認可は RBAC

【学习提示】

JWT 认人、RBAC 认权。

---

# Chapter 12　RBAC / Permission / CurrentUser

## 12.1 認証と認可

## 面接官

Authentication と Authorization の違いは。

## 回答

認証は誰か、認可は何をしてよいかです。
ERIP は JWT で認証、RBAC/Permission で認可します。片方だけでは企業要件を満たしません。

## 追問

RBAC とは。

## 回答

Role Based Access Control。ユーザー→ロール→権限で操作を制御します。企業の役割構造と相性が良いです。

## Point

- Who / What allowed

【容易说错】

JWT=权限系统、RBAC=登录 は失分。

---

## 12.2 ロールと Permission

## 面接官

ERIP のロールと Permission 粒度は。

## 回答

一般利用者（参照・検索・分析依頼）、マネージャー（承認）、管理者（権限/AI Runtime）など。
Permission は documents.read、retrieval.query、analysis.execute、approval.approve、security.manage 等の機能単位です。

## 追問

粗すぎ/細かすぎは。

## 回答

粗いと事故影響が広い。細かすぎると運用破綻。業務機能境界に合わせます。最小特権が原則です。

## Point

- 最小特権
- 機能単位 Permission

---

## 12.3 実装位置と CurrentUser

## 面接官

権限チェック位置と CurrentUser の意義は。

## 回答

入口（Router/Depends）で必須チェック、状態依存は Service でも実施。
CurrentUser は操作主体コンテキストで、監査・承認者判定・アクセス制御に必須です。
UI 非表示は UX であり、最終判定は Backend です。

## 追問

401 と 403 は。

## 回答

401 未認証、403 認証済み権限不足。拒否も統一エラーで、必要なら拒否自体を監査します。

## Point

- UI ≠ セキュリティ
- 401/403 を使い分け

---

# Chapter 13　業務別呼び出し

## 13.1 文書登録

## 面接官

文書登録の呼び出しを説明してください。

## 回答

Frontend → documents API → JWT/権限 → DocumentService → Repository 保存 →
Import/Chunk → 監査 → 返却。登録完了と検索可能状態は分離管理します。

## 追問

直後に検索できるか。

## 回答

状態による。チャンク化等完了後に検索対象になります。

## Point

- 登録 ≠ 検索可能

---

## 13.2 RAG と承認

## 面接官

RAG 検索と承認の呼び出し要点は。

## 回答

RAG：権限確認 → Retrieval（Keyword/Vector/Hybrid）→ 必要時 LLM → Citation 返却 → 監査。
承認：提出 → 状態遷移検証 → 承認/差戻し → Version/History → Audit。生成は確定ではありません。

## 追問

権限外文書は出るか。なぜ人承認か。

## 回答

権限外は出さない。経営レポートは影響が大きく、自動化と責任分界の両立が必要なため人承認を挟みます。

## Point

- 回答+根拠
- 生成 ≠ 確定

---

# Chapter 14　TL 深掘り

## 14.1 層を守る理由

## 面接官

Service に SQL、Router に業務を書かない理由は。

## 回答

境界破壊でテスト・切替・再利用が壊れ、権限/監査漏れが増えるためです。
『動けば良い』と『保守できる』は別です。

## Point

- 境界を守る
- 動く ≠ 保守できる

---

## 14.2 障害・性能・セキュリティ

## 面接官

障害切り分け、ボトルネック、セキュリティの要点は。

## 回答

障害は request_id → 認証/業務分類 → Service 状態 → DB → 外部 LLM → 監査突合。
性能は DB/検索/LLM の内訳を測ってから最適化。
セキュリティは JWT/RBAC 強制、入力検証、機密ログ禁止、最小特権、監査です。

## 追問

Prompt 全文をログに出すか。

## 回答

出しません。機密・個人情報・全文・API キーは禁止です。

## Point

- 測ってから直す
- ログにも機密境界

---

# Chapter 15　クロージング

## 15.1 30秒 / 2分

## 面接官

Backend を 30 秒と 2 分で説明してください。

## 回答

30秒：FastAPI で Router/Service/Repository 分離。JWT/RBAC の下で文書・検索・分析・承認・監査を提供し、正式データは PostgreSQL。

2分：入口で Validation と認証認可、Service で業務、Repository で永続化。正式は PostgreSQL、テストは InMemory。統一例外と request_id で追跡。AI があっても権限と業務事実は Backend が担保。

## 追問

技術選定を一言で。

## 回答

『権限・監査・永続化を守りながら AI 業務を安全提供する API 基盤』。FastAPI は手段です。

## Point

- 主鎖 → 責務 → 権限 → 永続化

【面试技巧】

收尾は业务価値に戻る。

---

# Part 02 要点总结

1. 呼び出しチェーン：React → FastAPI → Router → Service → Repository → PostgreSQL
2. 責務分離：入口 / 業務 / 永続化
3. JWT = Authentication、RBAC = Authorization
4. 正式データは PostgreSQL、InMemory はテスト実装
5. 企業要件：権限、承認、監査、トランザクション、追跡性

技術名の前に「何を守る Backend か」を先に言う。
