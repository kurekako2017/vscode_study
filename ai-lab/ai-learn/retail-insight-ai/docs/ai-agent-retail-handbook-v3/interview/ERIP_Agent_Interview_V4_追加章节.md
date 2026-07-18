# ERIP Agent 面试指南 V4 追加内容（建议合并到 V3）

> 本文档仅包含 V4 新增章节，可直接合并到《Enterprise Retail Intelligence Platform（ERIP）Agent 面试指南 V3》。

---

# 第0章 案件別オープニング

> 放置位置：第1章之前

## 0.1 共通自己紹介（60秒）

```text
2007年に来日し、日本で約20年間システム開発業務に従事してまいりました。

これまで20件以上のプロジェクトに参画し、
要件定義から運用保守まで幅広く担当しております。

役割としては
SE、
ブリッジSE、
TL
の経験があります。

技術面では、
Java、Python、C#、ABAPを中心に、

AWS、
Azure、
SAP、
Dynamics365、
AIシステム開発まで経験しております。

案件に応じて、
直近の関連プロジェクトをご紹介いたします。
```

---

## 0.2 Java案件

```text
今回の案件はJavaが中心になりますので、
経歴書No.25をご紹介いたします。

JavaシステムのAWS移行プロジェクトに参画し、
既存BatchをAWS Lambda（Java）およびAWS Lambda（Python）へ移行しました。

あわせて一部Web画面改修、
テスト、
運用支援まで担当しております。
```

---

## 0.3 SAP案件

```text
今回SAP案件になりますので、
No.24をご紹介いたします。

SAP S/4HANA移行案件において、
SD領域を中心に、
データ移行、
IF連携、
テスト、
運用支援まで担当しました。
```

---

## 0.4 Dynamics365案件

```text
今回Dynamics365案件になりますので、
関連プロジェクトをご紹介いたします。

Dynamics365およびPower Platformを利用した
業務システム開発を担当しました。

画面開発、
Plugin、
Workflow、
API連携などを担当しております。
```

---

## 0.5 AI Agent案件（ERIP）

```text
今回AI Agent案件になりますので、
No.26をご紹介いたします。

Enterprise Retail Intelligence Platform（ERIP）
という大手流通グループ向けAI経営分析プラットフォームを担当しました。

経営企画部門向けに、

社内文書を登録し、

RAG検索により根拠を取得し、

AIによる経営分析、

取締役会向けレポート生成、

Approval、

Auditまでを一連の業務フローとして実装しました。

私は主に

FastAPI

React

PostgreSQL

JWT/RBAC

RAG

AI Workflow

などの設計・実装を担当しました。
```

---

## 0.6 面接クロージング

```text
以上になります。

案件に合わせて、
詳細をご説明できればと思います。

本日はよろしくお願いいたします。
```

---

# 新增章节：2.5 AWS本番構成 想定質問

> 建议放在 2.4 项目规模定位之后。

## Q1

**なぜ ECS Fargate を採用しましたか。**

```text
コンテナ運用の標準化と運用負荷の削減を目的として
ECS Fargate を採用しました。

EC2 のようなサーバ管理が不要で、
FastAPI API をコンテナ単位でデプロイでき、
Auto Scaling にも対応できます。

ERIP の規模では
運用性と保守性のバランスが良いと判断しました。
```

---

## Q2

**なぜ EC2 ではありませんか。**

```text
EC2 は

OS管理、
パッチ適用、
Capacity管理などを自分たちで行う必要があります。

APIサービス中心の構成では、
ECS Fargate の方が運用負荷を抑えられます。
```

---

## Q3

**なぜ ALB を利用しますか。**

```text
HTTPS終端、
負荷分散、
Health Check、
Path Routing を提供できるためです。

Frontend と Backend の入口として利用します。
```

---

## Q4

**CloudFront を利用する理由は何ですか。**

```text
静的コンテンツの配信高速化、
キャッシュ、
HTTPS、
CDN による負荷分散を目的としています。
```

---

## Q5

**Amazon S3 の役割は何ですか。**

```text
文書ファイル、
添付資料、
レポートPDFなどの
オブジェクトデータを保存します。

DBにはメタデータを保持し、
実ファイルは S3 に保存する想定です。
```

---

## Q6

**Amazon RDS を採用した理由は何ですか。**

```text
PostgreSQL の運用をマネージドサービス化し、

バックアップ、
監視、
障害復旧、
パッチ適用の運用負荷を削減するためです。
```

---

## Q7

**CloudWatch は何を監視しますか。**

```text
APIログ、
コンテナログ、
CPU、
Memory、
ALB、
RDSなどを監視し、
障害調査にも利用します。
```

---

## Q8

**Secrets Manager を利用する理由は何ですか。**

```text
DB Password、
API Key、
JWT Secretなどを
コードや設定ファイルに保存しないためです。

IAM Role を利用して安全に取得します。
```

---

## Q9

**ECS と EKS の使い分けは何ですか。**

```text
ECS はシンプルなコンテナ運用に適しています。

EKS は
大規模マイクロサービス、
複数チーム、
Kubernetes 標準運用が必要な場合に選択します。

ERIP の構成では ECS Fargate が適しています。
```

---

# 第21章 案件別プロジェクト紹介

- 21.1 Java（No.25）
- 21.2 SAP（No.24）
- 21.3 Dynamics365
- 21.4 AI Agent（No.26）

> 面试时只展开对应项目，不连续介绍 No.24 / No.25 / No.26。
