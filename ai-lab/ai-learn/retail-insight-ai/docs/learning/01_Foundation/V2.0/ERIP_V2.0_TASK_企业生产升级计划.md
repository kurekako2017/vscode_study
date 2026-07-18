# ERIP V2.0 TASK（AWS 企业生产版升级计划）

> 目标：在保持 ERIP V1.0 业务流程不变的前提下，达到推荐的 **方案B（AWS ECS Fargate + RDS + S3）** 企业生产部署能力。

## 一、目标架构

```text
CloudFront
      │
Application Load Balancer
      │
ECS Fargate
├── FastAPI API
└── Worker
      │
├── Amazon RDS PostgreSQL + pgvector
├── Amazon S3
├── Amazon Bedrock（或企业指定LLM）
├── CloudWatch
└── Secrets Manager
```

---

# Phase 1：StorageService（最高优先级）

## 已完成
- PostgreSQL 持久化
- Repository 抽象
- 文档 Import / Chunk
- RAG 主流程

## 待完成
- [ ] StorageService 接口
- [ ] LocalStorageProvider
- [ ] S3StorageProvider
- [ ] MinIOStorageProvider
- [ ] Storage 配置切换
- [ ] Object Key 设计
- [ ] 文件迁移工具
- [ ] Presigned URL 上传
- [ ] Presigned URL 下载

完成后：
- DocumentService 无需修改即可切换 Local/S3/MinIO。

---

# Phase 2：LLM Provider 企业化

## 已完成
- Gateway
- Provider 链
- Runtime
- Usage Ledger

## 待完成
- [ ] Bedrock Provider
- [ ] OpenAI Provider（可选）
- [ ] Provider 配置中心
- [ ] Prompt Version 管理
- [ ] Model Version 管理
- [ ] Token 配额
- [ ] 部门级预算
- [ ] Provider 健康检查

---

# Phase 3：AWS 企业部署

## ECS

- [ ] Docker Image 优化
- [ ] Amazon ECR
- [ ] ECS Task Definition
- [ ] ECS Service
- [ ] Auto Scaling

## 网络

- [ ] ALB
- [ ] ACM HTTPS
- [ ] Route53
- [ ] VPC
- [ ] Security Group

---

# Phase 4：对象存储

- [ ] Amazon S3 Bucket
- [ ] 生命周期管理
- [ ] Bucket Policy
- [ ] IAM Role
- [ ] Multipart Upload
- [ ] 文件校验（Checksum）

---

# Phase 5：数据库

## 已完成
- PostgreSQL
- Alembic
- pgvector

## 待完成
- [ ] RDS 自动备份
- [ ] Multi-AZ（按生产需要）
- [ ] Performance Insights
- [ ] 参数组优化

---

# Phase 6：安全

- [ ] Secrets Manager
- [ ] ECS Task Role
- [ ] KMS（可选）
- [ ] S3 加密
- [ ] CloudTrail（可选）
- [ ] WAF（可选）

---

# Phase 7：监控

- [ ] CloudWatch Logs
- [ ] Metrics
- [ ] Alarm
- [ ] Dashboard
- [ ] ECS Health Check
- [ ] RDS Monitoring

---

# Phase 8：CI/CD

- [ ] GitHub Actions
- [ ] Build Docker
- [ ] Push ECR
- [ ] Deploy ECS
- [ ] Alembic 自动迁移

---

# Phase 9：企业能力

- [ ] 企业 SSO（OIDC/SAML）
- [ ] 组织/部门模型
- [ ] 成本中心
- [ ] AI 使用统计 Dashboard
- [ ] 企业配置中心

---

# 不建议进入 V2.0

以下能力不建议作为 V2.0 必做：

- EKS/Kubernetes
- Kafka / MSK
- Service Mesh
- Multi-Region
- Data Lake
- 微服务拆分
- SIEM/WORM
- 集团级多租户

这些更适合作为 V3.x 或客户明确要求时实施。

---

# V2.0 完成后的定位

完成上述任务后，ERIP 可以定位为：

- 企业生产可部署（AWS）
- ECS Fargate + RDS + S3 标准架构
- StorageService / LLMProvider 可切换
- 企业级日志、监控、安全、对象存储
- 保持 V1.0 业务流程不变，仅增强基础设施能力
