# EKS 学习笔记（中日对照）

EKS 是 AWS 提供的 Kubernetes 托管服务，适合把 K8s 的概念和 AWS 的托管能力放在一起理解。

## 0. 说明概要 / 説明概要

- 中文：EKS 负责托管 Kubernetes 控制平面，用户主要管理节点、工作负载、网络和权限。
- 日本語：EKS は Kubernetes のコントロールプレーンを管理し、利用者は主にノード、ワークロード、ネットワーク、権限を管理します。

## 1. 这个服务是什么 / このサービスは何か

- 中文：Kubernetes（K8s）是容器编排平台，EKS 是 AWS 上的托管实现。
- 日本語：Kubernetes（K8s）はコンテナオーケストレーション基盤で、EKS は AWS 上のマネージド実装です。

## 2. 组合中的角色 / 役割分担

| 组件 | 中文说明 | 日本語説明 |
|---|---|---|
| Kubernetes | 容器编排平台 | コンテナオーケストレーション基盤 |
| EKS | AWS 托管 Kubernetes | AWS のマネージド Kubernetes |
| Worker Node | 运行 Pod 的节点 | Pod を実行するノード |
| Pod | 最小部署单元 | 最小のデプロイ単位 |
| Service | 访问入口与服务发现 | アクセス入口とサービス発見 |
| Ingress | HTTP/HTTPS 流量入口 | HTTP/HTTPS の入口 |
| ConfigMap / Secret | 配置与敏感信息 | 設定と機密情報 |

## 3. 典型流程 / 典型フロー

1. 开发者编写 Kubernetes YAML 或 Helm Chart。
2. 镜像推送到 ECR。
3. EKS 根据 Deployment 创建 Pod。
4. Service / Ingress 暴露访问入口。
5. CloudWatch / Logs 记录运行状态。

日本語：
1. 開発者が Kubernetes YAML か Helm Chart を作成する。
2. イメージを ECR に push する。
3. EKS が Deployment に基づいて Pod を作成する。
4. Service / Ingress でアクセス口を公開する。
5. CloudWatch / Logs が稼働状態を記録する。

## 4. 学习重点 / 学習ポイント

- 中文：理解 K8s 的对象模型，不只记住部署命令。
- 日本語：K8s のオブジェクトモデルを理解し、コマンドだけを覚えない。
- 中文：理解 EKS 负责托管控制平面，业务仍要自己设计。
- 日本語：EKS はコントロールプレーンを管理するが、業務設計は別途必要。
- 中文：理解镜像、节点、网络、权限之间的关系。
- 日本語：イメージ、ノード、ネットワーク、権限の関係を理解する。

## 5. 和 LocalStack 的关系 / LocalStack との関係

- 中文：LocalStack 主要用于 AWS 通用服务模拟，EKS/Kubernetes 更多是概念学习与外部集群实践。
- 日本語：LocalStack は主に AWS サービスの模擬に使い、EKS/Kubernetes は概念学習や外部クラスタでの実践が中心です。
