# CDK 学习笔记（中日对照）

CDK 是用代码定义基础设施的工具，适合学习 IaC 的工程化写法。

## 1. 这个服务是什么 / このサービスは何か

- 中文：CDK 允许你用 TypeScript、Python、Java 等语言定义 AWS 资源。
- 日本語：CDK では TypeScript、Python、Java などで AWS リソースを定義できます。

## 2. 核心概念 / 基本概念

| 英文 | 中文说明 | 日本語説明 |
|---|---|---|
| App | 应用入口 | アプリの入口 |
| Stack | 基础设施堆栈 | スタック |
| Construct | 构造块 | コンストラクト |
| Synthesis | 合成生成模板 | 合成（テンプレート生成） |
| Deployment | 部署 | デプロイ |

## 3. 学习重点 / 学習ポイント

- 中文：理解 Construct、Stack、App 的分层。
- 日本語：Construct、Stack、App の階層を理解する。
- 中文：理解“用代码复用基础设施定义”。
- 日本語：「コードでインフラ定義を再利用する」考え方を理解する。
- 中文：理解 CDK 最终仍会生成 CloudFormation 模板。
- 日本語：CDK が最終的に CloudFormation テンプレートを生成することを理解する。

## 4. LocalStack 里怎么练 / LocalStack での練習方法

- 中文：先定义一个小 Stack，再逐步拆成多个 Construct。
- 日本語：まず小さな Stack を定義し、徐々に複数の Construct に分ける。
- 中文：把 S3、Lambda、IAM 的定义写成代码练习。
- 日本語：S3、Lambda、IAM の定義をコードで書いて練習する。

## 5. 常见坑 / よくある落とし穴

- 中文：把 CDK 和 CloudFormation 的关系搞混。
- 日本語：CDK と CloudFormation の関係を混同する。
- 中文：构造层级设计过深，代码难读。
- 日本語：コンストラクト階層を深くしすぎて読みにくくなる。
