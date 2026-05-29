# AWS知识点总览（中日对照）

这个文档用来整理 AWS 的核心知识点，适合配合 LocalStack 一起学习。

如果你的目标是“先学 AWS 基础概念，再在本地做验证”，把内容放在 `localstack-lab` 里最合适；如果后面要扩展到真实云环境、生产部署、CI/CD、Terraform 或多账号管理，再单独拆一个 `aws-lab` 也不迟。

## 1. 学习范围 / 学習範囲

- 中文：先掌握 AWS 的通用概念、常见服务、网络与权限模型，再学习 LocalStack 如何模拟这些服务。
- 日本語：まず AWS の共通概念、代表的なサービス、ネットワークと権限モデルを理解し、その後 LocalStack でどう再現するかを学ぶ。

## 2. 核心概念 / 基本概念

| 英文 | 中文说明 | 日本語説明 | LocalStack 关系 |
|---|---|---|---|
| Region | 区域，AWS 资源所在的大地理区域 | リージョン。AWS リソースを配置する地理的な範囲 | 部分资源可指定区域 |
| Availability Zone | 可用区，同一区域内的独立数据中心 | アベイラビリティーゾーン。リージョン内の独立した設備群 | 一般作为架构概念理解 |
| IAM | 访问控制与身份管理 | 権限と認証の管理 | 常配合 CLI/SDK 学习 |
| VPC | 虚拟私有云，网络隔离边界 | 仮想プライベートクラウド。ネットワーク分離の境界 | 重点理解网络模型 |
| Endpoint | 服务访问地址 | サービスの接続先 URL | LocalStack 学习时最常见 |
| ARN | AWS 资源唯一标识 | AWS リソースの一意識別子 | CLI/SDK 常见 |

## 3. 常见服务 / 代表的なサービス

### 3.1 计算 / コンピュート

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| EC2 | 虚拟服务器，可以自己装系统、跑应用 | 仮想サーバー。OS を自由に構成してアプリを実行する | 主要做概念理解 |
| Lambda | 事件驱动的无服务器函数 | イベント駆動のサーバーレス関数 | 可结合事件模型理解 |
| ECS | 容器编排服务 | コンテナオーケストレーションサービス | 与 ECR/Fargate 一起理解 |
| ECR | 容器镜像仓库 | コンテナイメージのリポジトリ | 主要做流程理解 |
| Fargate | 无需管理服务器的容器运行方式 | サーバー管理不要のコンテナ実行基盤 | 主要做概念理解 |
| EKS | Kubernetes 托管服务 | Kubernetes のマネージドサービス | 适合和 K8s 概念一起理解 |

### 3.2 存储 / ストレージ

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| S3 | 对象存储，最常用 | オブジェクトストレージ。最もよく使う | 最适合本地练习 |
| EBS | 块存储，挂载给 EC2 | EC2 に接続するブロックストレージ | 主要做概念理解 |

### 3.3 数据库 / データベース

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| RDS | 托管关系型数据库 | フルマネージドなリレーショナル DB | 主要做架构理解 |
| Aurora | AWS 自研的高性能数据库 | AWS 独自の高性能 DB | 主要做架构理解 |
| DynamoDB | NoSQL 键值数据库 | NoSQL キー値型データベース | 若项目需要可扩展 |

### 3.4 网络 / ネットワーク

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| VPC | 资源网络隔离的基础 | ネットワーク分離の基本単位 | 必学概念 |
| Subnet | 子网，VPC 内的更小网络 | VPC 内のサブネット | 必学概念 |
| Route 53 | DNS 和域名解析服务 | DNS とドメイン管理サービス | 主要做概念理解 |
| ELB / ALB / NLB | 负载均衡服务 | ロードバランサー | 常和 ECS/EC2 配套学习 |

### 3.5 监控与事件 / 監視とイベント

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| CloudWatch | 日志、指标、告警监控 | ログ・メトリクス・アラーム監視 | 常与运维场景一起学 |
| EventBridge | 事件总线与调度 | イベントバスとスケジューリング | 适合事件驱动理解 |
| SNS | 发布/订阅通知 | Pub/Sub 通知サービス | 与告警联动学习 |
| SQS | 消息队列 | メッセージキュー | 与异步任务一起学 |

### 3.6 安全与权限 / セキュリティと権限

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| IAM | 用户、角色、策略、权限边界 | ユーザー・ロール・ポリシー・権限境界 | 重点学习 |
| KMS | 密钥管理服务 | 暗号鍵管理サービス | 主要做概念理解 |
| Secrets Manager | 敏感配置与密钥管理 | 秘密情報の管理 | 主要做概念理解 |

### 3.7 基础设施与交付 / IaC とデリバリー

| 服务 | 中文说明 | 日本語説明 | LocalStack |
|---|---|---|---|
| CloudFormation | 用模板描述 AWS 资源 | AWS リソースをテンプレートで定義する | 很适合做本地验证 |
| CDK | 用代码生成云资源 | コードでインフラを定義する | 适合工程化学习 |
| Terraform | 多云基础设施即代码 | マルチクラウド対応の IaC | 和 LocalStack 配合度高 |
| CodeCommit | Git 托管服务 | Git リポジトリサービス | 主要做概念理解 |
| CodeBuild | 构建服务 | ビルドサービス | 与 CI 概念一起学 |
| CodeDeploy | 部署服务 | デプロイサービス | 与发布流程一起学 |
| CodePipeline | 持续交付流水线 | 継続的デリバリーパイプライン | 与 CI/CD 一起学 |

## 4. CLI / SDK / Endpoint

- 中文：LocalStack 学习里最重要的是“把 AWS CLI 指到本地 endpoint”，这样命令的写法和真实 AWS 尽量一致。
- 日本語：LocalStack 学習で最も大事なのは、AWS CLI の接続先をローカル endpoint に向けることです。これで実際の AWS に近い操作感を維持できます。

常见写法：

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
```

## 5. 推荐学习顺序 / おすすめの学習順序

1. IAM、Region、VPC 这类基础概念。
2. S3、EC2、RDS 这类最常见服务。
3. Lambda、SQS、SNS、EventBridge 这类事件驱动服务。
4. ECS、ECR、Fargate 这类容器服务。
5. CloudFormation、CDK、Terraform 这类 IaC 工具。
6. 最后再结合 LocalStack 做本地实操。

## 6. 什么时候建 aws-lab / aws-lab を作るタイミング

建议先放在 `localstack-lab`：

- 中文：你现在的重点是“学 AWS + 本地练习 + 避免影响其他项目”。
- 日本語：現時点では「AWS を学ぶ + ローカルで試す + 他プロジェクトに影響を与えない」ことが目的です。

适合单独建 `aws-lab` 的情况：

- 中文：需要真实云账号、真实部署、Terraform 多环境、CI/CD 或多项目统一治理。
- 日本語：実際のクラウドアカウント、本番デプロイ、Terraform の複数環境、CI/CD、複数プロジェクトの統合管理が必要になったとき。

## 7. 学习备注 / 学習メモ

- 中文：这个文档先做“总纲”，后面可以按服务拆成 S3、EC2、IAM、VPC、Lambda 等单页笔记。
- 日本語：この文書はまず全体像を整理し、後で S3、EC2、IAM、VPC、Lambda などに分けて詳細ノートに展開できます。

## 8. 单页笔记索引 / 個別ノート一覧

- [AWS 单页笔记索引](./aws/README.md)
- [S3 学习笔记](./aws/S3.md)
- [EC2 学习笔记](./aws/EC2.md)
- [IAM 学习笔记](./aws/IAM.md)
- [VPC 学习笔记](./aws/VPC.md)
- [Lambda 学习笔记](./aws/Lambda.md)
- [SQS 学习笔记](./aws/SQS.md)
- [SNS 学习笔记](./aws/SNS.md)
- [CloudWatch 学习笔记](./aws/CloudWatch.md)
- [ECR 学习笔记](./aws/ECR.md)
- [ECS 学习笔记](./aws/ECS.md)
- [Fargate 学习笔记](./aws/Fargate.md)
- [EKS 学习笔记](./aws/EKS.md)
- [KMS 学习笔记](./aws/KMS.md)
- [Secrets Manager 学习笔记](./aws/SecretsManager.md)
- [Route 53 学习笔记](./aws/Route53.md)
- [CloudFormation 学习笔记](./aws/CloudFormation.md)
- [CDK 学习笔记](./aws/CDK.md)
- [Terraform 学习笔记](./aws/Terraform.md)

## 9. 高频架构组合 / 高頻アーキテクチャ組み合わせ

| 组合 | 简单功能描述 | 日本語の簡単説明 |
|---|---|---|
| [高频架构组合索引](./aws/combos/README.md) | 组合场景总入口，适合学习如何把单服务串成完整链路。 | 組み合わせ学習の総合入口で、単体サービスをつなぐ流れを学べます。 |
| [S3 + CloudFront](./aws/combos/S3_CloudFront.md) | S3 存静态资源，CloudFront 做全球分发，适合学习静态站点加速。 | S3 の静的資産を CloudFront で配信し、静的サイト配信を学べます。 |
| [EC2 + ALB](./aws/combos/EC2_ALB.md) | EC2 承载应用，ALB 负责流量分发，适合学习 Web 服务负载均衡。 | EC2 を ALB で振り分け、Web サービスの負荷分散を学べます。 |
| [SQS + Lambda](./aws/combos/SQS_Lambda.md) | 队列缓冲消息，Lambda 异步消费，适合学习解耦和异步处理。 | キューを Lambda が非同期処理し、疎結合を学べます。 |
| [ECS + ECR + Fargate](./aws/combos/ECS_ECR_Fargate.md) | 镜像入库后由 ECS/Fargate 运行容器，适合学习容器交付链路。 | ECR のイメージを ECS/Fargate で実行し、コンテナ配信を学べます。 |
| [Docker / ECR / ECS](./aws/combos/Docker_ECR_ECS.md) | Docker 打镜像，ECR 存镜像，ECS 跑容器服务，适合学习容器化发布。 | Docker でイメージ化し、ECR に保存し、ECS で実行する流れを学べます。 |
| [RDS + CloudWatch](./aws/combos/RDS_CloudWatch.md) | RDS 提供数据库，CloudWatch 监控告警，适合学习运维监控。 | RDS を CloudWatch で監視し、運用監視を学べます。 |
| [S3 + Lambda](./aws/combos/S3_Lambda.md) | S3 事件触发 Lambda 自动处理，适合学习上传后通知和后续异步联动。 | S3 イベントで Lambda を起動し、アップロード後通知と非同期連携を学べます。 |
| [SQS + SNS](./aws/combos/SQS_SNS.md) | SNS 广播消息，SQS 负责排队消费，适合学习发布订阅与缓冲。 | SNS 配信を SQS で受け、Pub/Sub とバッファリングを学べます。 |
| [S3 + SNS](./aws/combos/S3_SNS.md) | S3 事件通知 SNS 再分发给订阅者，适合学习对象事件联动。 | S3 イベントを SNS で配信し、オブジェクトイベント連携を学べます。 |
| [SQS + Lambda + DLQ](./aws/combos/SQS_Lambda_DLQ.md) | 失败消息进入 DLQ，适合学习兜底补偿和失败重试。 | 失敗メッセージを DLQ で受け、補償処理と再試行を学べます。 |
| [RDS + Lambda](./aws/combos/RDS_Lambda.md) | Lambda 查询或同步 RDS 数据，适合学习轻量数据任务。 | Lambda が RDS を検索・同期し、軽量データ処理を学べます。 |
| [S3 + Athena](./aws/combos/S3_Athena.md) | Athena 直接查询 S3 上的数据，适合学习无服务器分析。 | Athena が S3 を直接検索し、サーバーレス分析を学べます。 |
| [Glue + S3](./aws/combos/Glue_S3.md) | Glue 负责编目、转换和 ETL，适合学习数据准备流程。 | Glue がカタログ化と ETL を担い、データ準備を学べます。 |
| [Kinesis + Lambda](./aws/combos/Kinesis_Lambda.md) | Kinesis 提供流数据，Lambda 近实时处理，适合学习实时处理。 | Kinesis のストリームを Lambda で処理し、リアルタイム処理を学べます。 |
| [Redshift + S3](./aws/combos/Redshift_S3.md) | S3 落地数据，Redshift 做仓库分析，适合学习数仓分析。 | S3 のデータを Redshift で分析し、DWH を学べます。 |
| [Athena + Glue](./aws/combos/Athena_Glue.md) | Glue 提供目录，Athena 基于目录查询，适合学习元数据联动。 | Glue のメタデータで Athena が検索し、メタデータ連携を学べます。 |
| [Kinesis + Firehose](./aws/combos/Kinesis_Firehose.md) | Kinesis 接流，Firehose 自动投递落地，适合学习实时摄取。 | Kinesis の流を Firehose で配信し、リアルタイム取り込みを学べます。 |
| [Lake Formation + Glue](./aws/combos/LakeFormation_Glue.md) | Lake Formation 管权限，Glue 管目录，适合学习数据治理。 | Lake Formation が権限、Glue がカタログを担い、データガバナンスを学べます。 |
| [Athena + QuickSight](./aws/combos/Athena_QuickSight.md) | Athena 查询结果给 QuickSight 可视化，适合学习报表展示。 | Athena の結果を QuickSight で可視化し、レポート作成を学べます。 |
| [Redshift + QuickSight](./aws/combos/Redshift_QuickSight.md) | Redshift 分析结果直接做 BI 展示，适合学习数仓报表。 | Redshift の結果を BI 表示し、DWH レポートを学べます。 |
| [Lake Formation + Athena](./aws/combos/LakeFormation_Athena.md) | Lake Formation 控制受控查询边界，适合学习权限查询。 | Lake Formation がクエリ境界を制御し、権限制御クエリを学べます。 |
| [QuickSight + Lake Formation](./aws/combos/QuickSight_LakeFormation.md) | 报表基于受控数据访问共享，适合学习权限驱动的看板。 | 共有レポートを制御データで使い、権限制御ダッシュボードを学べます。 |
| [Redshift + Lake Formation](./aws/combos/Redshift_LakeFormation.md) | 数据仓库纳入统一权限治理，适合学习仓库治理。 | DWH を統一権限で管理し、データウェアハウス治理を学べます。 |
| [Web Project 部署流程](./aws/combos/WebProject_Deployment.md) | 用 Route 53、ALB、EC2 说明 Web 部署，适合学习站点上线流程。 | Route 53、ALB、EC2 で Web デプロイを学び、公開手順を理解できます。 |
| [Batch 部署流程](./aws/combos/Batch_Deployment.md) | 用 Scheduler、Lambda、S3、SQS 说明批处理部署，适合学习定时任务和异步联动。 | Scheduler、Lambda、S3、SQS でバッチを学び、定期実行と非同期連携を理解できます。 |

## 10. AWS 与 Azure 对照 / AWS と Azure の対応表

- [AWS 与 Azure 服务对照表](./AWS_vs_Azure.md)