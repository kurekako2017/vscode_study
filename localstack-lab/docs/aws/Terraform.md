# Terraform 学习笔记（中日对照）

Terraform 是基础设施即代码工具，适合学习多云资源管理和环境一致性。

## 1. 这个服务是什么 / このサービスは何か

- 中文：Terraform 用配置文件定义云资源，然后通过计划和应用来创建/变更资源。
- 日本語：Terraform は設定ファイルでクラウドリソースを定義し、plan/apply で変更を管理する IaC ツールです。

## 2. 核心概念 / 基本概念

| 英文 | 中文说明 | 日本語説明 |
|---|---|---|
| Provider | 提供商插件 | プロバイダー |
| Resource | 资源定义 | リソース |
| Module | 模块 | モジュール |
| State | 状态文件 | ステート |
| Plan | 执行计划 | 実行計画 |
| Apply | 应用变更 | 変更適用 |
| Destroy | 销毁资源 | リソース削除 |

## 3. 学习重点 / 学習ポイント

- 中文：理解 provider、resource、module、state 的关系。
- 日本語：provider、resource、module、state の関係を理解する。
- 中文：理解 plan / apply / destroy 的完整工作流。
- 日本語：plan / apply / destroy のワークフローを理解する。
- 中文：理解 Terraform 在多环境管理中的优势。
- 日本語：Terraform の複数環境管理での強みを理解する。

## 4. LocalStack 里怎么练 / LocalStack での練習方法

- 中文：先用 LocalStack 验证最小资源，再考虑模块化。
- 日本語：まず LocalStack で最小構成を検証し、その後モジュール化を考える。
- 中文：把 S3、IAM、Lambda 资源写成 Terraform 配置。
- 日本語：S3、IAM、Lambda リソースを Terraform 設定として書く。

## 5. 常见坑 / よくある落とし穴

- 中文：state 文件管理不当，容易破坏环境。
- 日本語：state ファイルの管理が不適切だと環境を壊しやすい。
- 中文：模块拆分过度，导致配置难维护。
- 日本語：モジュール分割しすぎると保守しづらくなる。
