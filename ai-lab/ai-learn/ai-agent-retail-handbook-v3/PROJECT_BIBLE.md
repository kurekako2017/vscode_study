# PROJECT_BIBLE

本文件是 `ai-agent-retail-handbook-v3` 的唯一最高规则，也是 Retail Insight AI 的统一世界观。所有正文文档必须引用并遵守本文件。

# 项目名称

Retail Insight AI

# 日文名称

小売業向け AI 経営分析システム

# 项目世界观

Retail Insight AI 是日本零售行业 AI 经营分析平台。系统围绕经营会议、销售分析、库存分析、商品分析、会员分析、市场调查和管理层报告构建。

所有文档必须把 Retail Insight AI 作为同一个连续项目来讲，不按孤立知识点拆散，不按技术名词堆砌。

# 项目定位

Retail Insight AI 是日本零售行业 AI 经营分析平台。

系统重点是经营分析、KPI、Workflow、Research Agent、日文报告生成和管理层决策支持。

# 项目背景

日本零售企业需要在经营会议前整合 POS、库存、商品、会员、销售、门店、CSV、Excel、日报和月报等数据，形成可以用于经营判断的分析报告。

# 客户背景

客户是日本中大型零售企业，拥有多门店、多商品、多销售渠道和固定经营会议流程。

# 行业背景（日本零售）

日本零售行业重视销售效率、库存周转、商品结构、会员行为、门店表现、促销效果和月次经营报告。系统必须支持数据追溯、经营指标解释、报告生成和 Review。

# 客户组织结构

- 经营层
- 经营企画
- 店铺管理
- 商品部
- 库存管理
- 会员运营
- 数据分析担当
- IT 部门
- 外部开发团队

# 业务流程

1. 收集 POS、库存、商品、会员、销售和门店数据
2. 整理 CSV、Excel、日报、月报
3. 分析 KPI
4. 检测库存和销售异常
5. 调查市场和竞品信息
6. 生成日文经营分析报告
7. 管理层 Review
8. 形成改善行动

# 系统整体架构

Retail Insight AI 由前端、后端、Workflow、Research Agent、数据层、报告生成和运用扩展组成。

核心链路：

```text
React
↓
FastAPI
↓
LangGraph Workflow
↓
固定 KPI 分析 / Research Agent
↓
Streaming
↓
日文经营分析报告
```

# 数据来源

- POS
- 库存
- 商品
- 会员
- 销售
- 门店
- CSV
- Excel
- API
- 日报
- 月报

# 技术架构

- React
- FastAPI
- Python
- LangGraph
- Workflow
- Streaming
- SSE
- Research Agent
- RAG
- Docker
- SQLite

# 我的职责

- Backend
- FastAPI
- API Design
- Workflow
- Prompt
- Streaming
- Research
- Architecture
- Review

统一职责表达：

```text
Retail Insight AI、小売業向け AI 経営分析システムの開発を担当しました。
担当範囲は Backend、FastAPI、API Design、Workflow、Prompt、Streaming、Research、Architecture、Review です。
```

# 项目开发流程

1. 需求分析
2. 基本设计
3. 详细设计
4. API 设计
5. 数据库设计
6. 开发
7. 测试
8. Review
9. 部署
10. 保守

# Production Gap

## 已实现能力

- FastAPI API
- LangGraph Workflow
- Research Agent
- 固定 KPI 分析
- Streaming / SSE
- Report 生成
- SQLite
- Docker
- 基础 Architecture
- Review 观点

## 未来企业版追加能力

- RBAC
- SSO
- Audit Log
- Redis
- OpenSearch
- CI/CD
- Kubernetes
- OpenTelemetry
- RabbitMQ
- VectorDB
- API Gateway
- Secrets Manager
- 多租户
- 权限过滤
- 监控告警
- 负载测试
- 数据备份
- 灾害恢复

# 统一术语

- Retail Insight AI
- 小売業向け AI 経営分析システム
- Research Agent
- Workflow
- KPI
- 经营分析
- 销售分析
- 库存分析
- 商品分析
- 会员分析
- 市场调查
- 日文报告生成
- 管理层报告
- Production Gap

# 统一项目介绍

```text
Retail Insight AI は、日本の小売業向け AI 経営分析システムです。
POS、在庫、商品、会員、売上、店舗、CSV、Excel、日報、月報を統合し、KPI 分析、Workflow、Research Agent、Streaming、レポート生成を通じて、経営判断を支援します。
```

# 统一自我介绍

```text
私は Retail Insight AI、小売業向け AI 経営分析システムの開発を担当しました。
主に Backend、FastAPI、API Design、LangGraph Workflow、Research Agent、Streaming、Report 生成、Docker、Architecture Review を担当しました。
```

# 统一项目说明

所有项目说明必须包含：

- 日本零售行业背景
- 客户业务流程
- POS / 库存 / 商品 / 会员 / 销售 / CSV / Excel / API
- 固定 KPI 分析
- Research Agent
- Workflow
- Streaming / SSE
- 日文报告生成
- 我的职责
- Production Gap

# 统一职责

统一使用“担当”表达：

```text
担当範囲は Backend、FastAPI、API Design、Workflow、Prompt、Streaming、Research、Architecture、Review です。
```

# 统一技术介绍

技术介绍必须回答：

- 该技术在 Retail Insight AI 中负责什么
- 与经营分析业务的关系
- 为什么采用该设计
- TL Review 会关注什么
- Production Gap 如何扩展

# 面试统一回答原则

所有面试回答必须引用本章原则：

1. 先说 Retail Insight AI 的业务背景
2. 再说小売業向け AI 経営分析システム的系统目标
3. 再说自己的担当范围
4. 再说技术设计
5. 最后说 Production Gap 和扩展方向

禁止先从框架名开始回答。

所有文档不得重复定义另一套项目背景、自我介绍、项目说明或职责表达。

# Book First Principle

V3 遵守一本书原则：

- 不拆散知识
- 不新增大量 Markdown
- 不为单个知识点创建文件
- 不为单个面试题创建文件
- 不为单个 Review 创建文件
- 优先使用 Markdown 标题组织章节
- 每个正文 Markdown 都必须像一本可以连续阅读的技术书

# 文档维护规则

- `PROJECT_BIBLE.md` 是唯一最高规则
- `README.md` 只做入口和维护说明
- 正文 Markdown 不超过 6 个
- 新增内容必须回到 Retail Insight AI
- 章节标题统一使用中文
- 技术名保留英文
