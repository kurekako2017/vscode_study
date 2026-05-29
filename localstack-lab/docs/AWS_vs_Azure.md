# AWS 与 Azure 服务对照表（中日对照）

这个页面把 AWS 常见服务和 Azure 的对应服务放在一起，方便在学习云服务时快速建立映射。

## 0. 说明概要 / 説明概要

- 中文：下面的表格是学习导向的“常见一一对应”，不同云厂商在功能边界和命名上会有差异。
- 日本語：以下は学習用の「代表的な対応表」です。クラウドごとに機能範囲や名称は少し異なります。

## 1. AWS vs Azure 一览 / 一覧表

| AWS | Azure | 中文说明 | 日本語説明 |
|---|---|---|---|
| EC2 | Virtual Machines | 虚拟机 | 仮想マシン |
| ECS | Azure Container Apps / AKS | 容器编排 | コンテナオーケストレーション |
| EKS | AKS | Kubernetes 托管服务 | Kubernetes のマネージドサービス |
| ECR | Azure Container Registry | 容器镜像仓库 | コンテナレジストリ |
| Lambda | Azure Functions | 无服务器函数 | サーバーレス関数 |
| S3 | Blob Storage | 对象存储 | オブジェクトストレージ |
| EBS | Managed Disks | 块存储 | ブロックストレージ |
| RDS | Azure SQL / Azure Database for PostgreSQL/MySQL | 托管数据库 | マネージド DB |
| DynamoDB | Cosmos DB | NoSQL 数据库 | NoSQL データベース |
| VPC | Virtual Network | 私有网络 | 仮想ネットワーク |
| Route 53 | Azure DNS | 域名解析 | DNS |
| ALB / ELB | Application Gateway / Load Balancer | 负载均衡 | ロードバランサー |
| CloudWatch | Azure Monitor | 监控与日志 | 監視とログ |
| SNS | Service Bus Topics / Notification Hubs | 发布订阅通知 | Pub/Sub 通知 |
| SQS | Service Bus Queues / Storage Queues | 消息队列 | メッセージキュー |
| IAM | Microsoft Entra ID / Azure RBAC | 身份与权限管理 | ID と権限管理 |
| KMS | Key Vault | 密钥管理 | 鍵管理 |
| Secrets Manager | Key Vault Secrets | 密钥与机密信息 | 機密情報管理 |
| CloudFormation | ARM Templates / Bicep | 基础设施即代码 | IaC |
| CDK | Bicep / Terraform | 代码化基础设施 | コードで IaC |
| Terraform | Terraform | 多云 IaC | マルチクラウド IaC |
| EventBridge | Event Grid / Scheduler | 事件总线与调度 | イベント連携とスケジュール |
| CloudFront | Azure Front Door / CDN | CDN 分发 | CDN 配信 |
| Step Functions | Durable Functions | 工作流编排 | ワークフロー制御 |

## 2. 使用提示 / 使い方のヒント

- 中文：不要把对照表当成完全等价表，重点是建立心智映射。
- 日本語：完全な同義表としてではなく、概念マッピングとして使うのがポイントです。
- 中文：如果你已经会 AWS，再看 Azure 时就先找“同类服务”，再看差异。
- 日本語：AWS を知っているなら、Azure はまず「同系統サービス」を探して差分を見ると理解しやすいです。
- 中文：如果后面要做多云方案设计，这张表可以作为起点。
- 日本語：将来的にマルチクラウド設計をするなら、この表が出発点になります。
