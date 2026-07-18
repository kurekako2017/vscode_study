# Enterprise Retail Intelligence Platform（ERIP）手册 V3

本目录是 **Enterprise Retail Intelligence Platform（ERIP）V1.0** 的长期知识库、面试中心与复盘区。

> 历史名称：Retail Insight AI（仅作早期 MVP 说明，不作当前项目名）。

项目简介、当前完成情况与文档治理统一见主项目 [README.md](../../README.md)。

## 目录分区（权威）

| 分区 | 路径 | 用途 |
|---|---|---|
| 项目实战与技术基础 | 本目录（handbook 根） | `01`/`03`/`04`/`05`/`06`/`08`/`09`/`10`/`11`/`12`、`PROJECT_BIBLE`、`AGENTS` |
| **面试材料** | [`interview/`](interview/) | 全部当前权威面试入口（见下表） |
| 历史待删除材料 | [`../_archive_candidate/ai-agent-retail-handbook-v3/`](../_archive_candidate/ai-agent-retail-handbook-v3/) | 旧 Volume 等；**不作面试背诵源** |

## handbook 定位

- 面向面试讲解、项目理解与长期复盘。
- 面试文件统一在 `interview/`；技术与实战章节保留在 handbook 根目录。
- 技术规范以主项目 `docs/` 为唯一维护入口；重复镜像在归档候选区。

## 学习路线（技术基础）

```text
README.md
↓
PROJECT_BIBLE.md
↓
01_日本AI项目实战.md
↓
03_AI核心知识.md   ← 技术版本矩阵 + 技术知识点表
↓
04_日本现场开发.md
↓
05_TL代码审查.md
↓
06_学习路线.md
↓
08_架构图册.md
↓
09_系统设计书.md
↓
11_Project_Structure.md
```

配合主项目学习文档（路径已校验）：

- [../learning/01_Foundation/LEARNING_API_WALKTHROUGH.md](../learning/01_Foundation/LEARNING_API_WALKTHROUGH.md)
- [../learning/01_Foundation/TEST_CASES.md](../learning/01_Foundation/TEST_CASES.md)
- [../learning/01_Foundation/CODE_STUDY_GUIDE.md](../learning/01_Foundation/CODE_STUDY_GUIDE.md)
- [../learning/01_Foundation/RUNBOOK_LOCAL.md](../learning/01_Foundation/RUNBOOK_LOCAL.md)
- [../../VERIFY_CHECKLIST.md](../../VERIFY_CHECKLIST.md)
- [../development/DEPLOYMENT_GUIDE.md](../development/DEPLOYMENT_GUIDE.md)

## 面试路线（权威 · 仅 `interview/`）

```text
interview/new/…_Part01.md（案件开场 / ERIP 介绍）
↓
interview/new/…_Part02.md（Backend）
↓
interview/new/…_Part03.md（Document / RAG）
↓
interview/new/…_Part04.md（Workflow / Approval / SSE）
↓
interview/new/…_Part05.md（AWS / 本番）
↓
interview/new/…_Part06.md（压迫问答 / 比较 / Appendix）
↓
03_AI核心知识.md（handbook 根 · 技术表）
↓
01_日本AI项目实战.md（handbook 根 · 业务主链）
```

补充（口头训练 / 旧 V1 合订本）：

```text
interview/INTERVIEW_GUIDE.md
interview/02_日本AI现场面试.md
interview/07_面试口头训练.md
interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md
```

## 面试材料权威索引（V4 正式版 + V1.0 补充）

| 优先级 | 文件 | 用途 | 状态 |
|---|---|---|---|
| 1 | [`interview/new/…_Part01.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part01.md) | **V4 面试主文档** 开场 + **全体架构** + **LangChain/LangGraph** | 活动 |
| 2 | [`interview/new/…_Part02.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part02.md) | **V4 正式版** Backend | 活动 |
| 3 | [`interview/new/…_Part03.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part03.md) | **V4 正式版** Document / RAG | 活动 |
| 4 | [`interview/new/…_Part04.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part04.md) | **V4 正式版** Workflow / Approval / SSE | 活动 |
| 5 | [`interview/new/…_Part05.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part05.md) | **V4 正式版** AWS / 本番 | 活动 |
| 6 | [`interview/new/…_Part06.md`](interview/new/Enterprise_Retail_Intelligence_Platform_ERIP_Agent_Part06.md) | **V4 正式版** 压迫 / 比较 / Appendix | 活动 |
| 7 | [`interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md`](interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md) | V1.0 合订本（补充对照） | 活动 |
| 8 | [`interview/INTERVIEW_GUIDE.md`](interview/INTERVIEW_GUIDE.md) | 讲解稿 | 活动 |
| 9 | [`interview/02_日本AI现场面试.md`](interview/02_日本AI现场面试.md) | 自介、深掘、压迫补充 | 活动 |
| 10 | [`interview/07_面试口头训练.md`](interview/07_面试口头训练.md) | 开口训练 | 活动 |
| 11 | [`01_日本AI项目实战.md`](01_日本AI项目实战.md) | 业务主链、架构、担当 | 活动 |
| 12 | [`03_AI核心知识.md`](03_AI核心知识.md) | **技术版本矩阵 + 技术知识点表** | 活动 |

| 历史文件 | 处理 |
|---|---|
| `interview/new/*Part02-1*` / `*Part02-2*` 等碎片草稿 | **已归档** [`../_archive_candidate/ai-agent-retail-handbook-v3/interview-new-drafts/`](../_archive_candidate/ai-agent-retail-handbook-v3/interview-new-drafts/)；**不作背诵源** |
| `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | **已合并并移至待删除区** [`../_archive_candidate/ai-agent-retail-handbook-v3/`](../_archive_candidate/ai-agent-retail-handbook-v3/) |
| handbook 根目录下的 `02`/`07`/`INTERVIEW_GUIDE`/旧 Volume 路径 | **不再作为入口**；文件已迁至 `interview/` |

**统一业务主链：**

```text
登录/JWT/RBAC → 文書 Upload/Import/Chunk → RAG/Citation
→ 显式 AI分析(low_cost) → 取締役会报告(high_quality)
→ ReportVersion → Approval → Persistent Audit → LLM Usage Ledger
```

**统一基线：** PG **297/6 skip** · InMemory **286/62 skip** · FE **116/116** · Alembic **`20260717_08_ai_runtime`** · 默认 LLM **stub** · 正式 Repository **PostgreSQL** · 本地 **5173** / Compose **8080**。

## 知识路线

```text
PROJECT_BIBLE.md → 03_AI核心知识.md → 08_架构图册.md → 09_系统设计书.md → 12_ADR.md
```

## 根目录活动文档（项目实战与技术基础）

- [README.md](README.md)
- [AGENTS.md](AGENTS.md)
- [PROJECT_BIBLE.md](PROJECT_BIBLE.md)
- [01_日本AI项目实战.md](01_日本AI项目实战.md)
- [03_AI核心知识.md](03_AI核心知识.md)
- [04_日本现场开发.md](04_日本现场开发.md)
- [05_TL代码审查.md](05_TL代码审查.md)
- [06_学习路线.md](06_学习路线.md)
- [08_架构图册.md](08_架构图册.md)
- [09_系统设计书.md](09_系统设计书.md)
- [09_系统设计书_7.0_Technical_Architecture_增补_修改版.md](09_系统设计书_7.0_Technical_Architecture_增补_修改版.md)
- [10_Production_Roadmap.md](10_Production_Roadmap.md)
- [11_Project_Structure.md](11_Project_Structure.md)
- [12_ADR.md](12_ADR.md)

## 面试材料（`interview/`）

- [interview/INTERVIEW_GUIDE.md](interview/INTERVIEW_GUIDE.md)
- [interview/02_日本AI现场面试.md](interview/02_日本AI现场面试.md)
- [interview/07_面试口头训练.md](interview/07_面试口头训练.md)
- [interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md](interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md)

## 技术规范引用

- [API 合同](../contracts/API_CONTRACT.md)
- [架构](../architecture/ARCHITECTURE.md)
- [事件合同](../contracts/EVENT_CONTRACT.md)
- [错误码](../contracts/ERROR_CATALOG.md)
- [数据库](../database/DATABASE.md)
- [部署](../development/DEPLOYMENT_GUIDE.md)
- [CHANGELOG](../governance/CHANGELOG.md)
- [Backlog](../governance/PROJECT_BACKLOG.md)

## 归档

- [../_archive_candidate/](../_archive_candidate/)
- [../_archive_candidate/ai-agent-retail-handbook-v3/](../_archive_candidate/ai-agent-retail-handbook-v3/)（旧 Volume 历史稿）
- [../_archive_candidate/handbook-docs/](../_archive_candidate/handbook-docs/)
- [../_archive_candidate/handbook-root/](../_archive_candidate/handbook-root/)

## 维护规则

- 不直接删除文档；完成合并后移入 `_archive_candidate`。
- 面试背诵只使用上表「活动」且位于 `interview/` 的面试文件 + 根目录 `01`/`03`。
- 活动文档链接必须指向真实存在的路径；**禁止**再把 handbook 根下的旧 `02`/`07`/`INTERVIEW_GUIDE`/旧 Volume 文件名当作当前入口。

## 更新日志

- V3: handbook 统一结构。
- V1.0 Final Doc Pass: ERIP 名称、数字、版本表。
- **V1.0 Volume 合并 (2026-07-17)**: ERIP 权威面试指南真合并；旧 Volume 移入 `_archive_candidate/ai-agent-retail-handbook-v3/`；`03` 版本矩阵+知识点表定稿。
- **V1.0 interview 目录 (2026-07-17)**: 用户将面试材料迁入 `interview/`，权威文件名为 `Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md`；索引与全库链接同步。
