# ERIP 产品路线图（V1.0 / V2.0 / V3.0）

> 本文档用于规划 ERIP 后续版本，不影响 V1.0 已完成项目的面试口径。

---

# V1.0（Enterprise Business Edition）【已完成】

定位：

> 面向大型流通集团经营分析部门的企业 AI 平台。

目标：

- 可交付
- 可演示
- 可面试
- 企业业务流程完整

核心能力：

- React + FastAPI
- PostgreSQL + pgvector
- Document Import
- Chunk
- Keyword / Vector Retrieval
- Internal RAG
- Report
- Approval
- Audit
- JWT / RBAC
- Usage Ledger
- Repository 抽象

部署想定：

```text
CloudFront
ALB
ECS Fargate
Amazon RDS PostgreSQL
Amazon S3（规划）
CloudWatch
Secrets Manager
```

说明：

V1.0 面试时统一按照"已经完成并交付"进行介绍，不讨论 V2、V3 或未来计划。

---

# V2.0（Enterprise Production Edition）

定位：

> 企业生产部署版本。

目标：

在保持 V1.0 业务流程不变的前提下，实现 AWS 企业生产部署能力。

## Phase 1 StorageService

- [ ] StorageService
- [ ] LocalStorageProvider
- [ ] S3StorageProvider
- [ ] MinIOStorageProvider
- [ ] Object Key
- [ ] Presigned Upload
- [ ] Presigned Download

## Phase 2 LLM 企业化

- [ ] Bedrock Provider
- [ ] Provider Config
- [ ] Prompt Version
- [ ] Model Version
- [ ] Budget
- [ ] Provider Health Check

## Phase 3 AWS

- [ ] Amazon ECR
- [ ] ECS Task Definition
- [ ] ECS Service
- [ ] Auto Scaling
- [ ] ALB
- [ ] Route53
- [ ] ACM

## Phase 4 Amazon S3

- [ ] Bucket
- [ ] Lifecycle
- [ ] IAM
- [ ] Multipart Upload
- [ ] Checksum

## Phase 5 Database

- [ ] RDS Backup
- [ ] Performance Insights
- [ ] Parameter Group
- [ ] Multi-AZ（按生产需要）

## Phase 6 Security

- [ ] Secrets Manager
- [ ] IAM Task Role
- [ ] S3 Encryption
- [ ] KMS（可选）
- [ ] WAF（按需要）
- [ ] CloudTrail（按需要）

## Phase 7 Monitoring

- [ ] CloudWatch Logs
- [ ] Dashboard
- [ ] Metrics
- [ ] Alarm
- [ ] ECS Health Check

## Phase 8 CI/CD

- [ ] GitHub Actions
- [ ] Docker Build
- [ ] Push ECR
- [ ] Deploy ECS
- [ ] Alembic Migration

完成后定位：

```text
CloudFront
      │
ALB
      │
ECS Fargate
├── API
└── Worker
      │
├── RDS PostgreSQL + pgvector
├── Amazon S3
├── Bedrock（或企业批准LLM）
├── CloudWatch
└── Secrets Manager
```

---

# V3.0（Enterprise Group Edition）

定位：

> 面向集团级企业平台。

仅在业务规模确实需要时实施。

规划能力：

- [ ] Organization
- [ ] Department
- [ ] Store
- [ ] Enterprise SSO
- [ ] Tenant
- [ ] Multi-Region
- [ ] API Gateway
- [ ] EventBridge / SQS
- [ ] 集团 AI Gateway
- [ ] 数据湖集成
- [ ] 集团级成本中心
- [ ] 集团 AI Governance

可选能力（根据客户平台决定）：

- Amazon EKS
- Kubernetes
- Kafka / MSK
- Service Mesh
- SIEM
- WORM Audit

说明：

V3.0 并不是 V2.0 的必做内容，而是根据客户规模、组织结构、SRE 能力和集团平台标准决定是否实施。

---

# 三个版本的关系

```text
V1.0
企业业务能力
RAG
Approval
Audit
Repository
        │
        ▼
V2.0
AWS 企业生产部署
StorageService
S3
Bedrock
CloudWatch
CI/CD
        │
        ▼
V3.0
集团平台
Organization
SSO
Tenant
EKS（按需要）
Multi-Region
```

原则：

- V1.0 保持稳定，作为作品集与面试版本。
- V2.0 专注企业生产能力。
- V3.0 根据真实客户需求逐步演进，避免过度设计。
