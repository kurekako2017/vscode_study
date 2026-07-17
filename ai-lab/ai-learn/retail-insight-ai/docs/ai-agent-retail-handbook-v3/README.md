# Enterprise Retail Intelligence Platform（ERIP）手册 V3

本目录是 **Enterprise Retail Intelligence Platform（ERIP）V1.0** 的长期知识库、面试中心与复盘区。

> 历史名称：Retail Insight AI（仅作早期 MVP 说明，不作当前项目名）。

项目简介、当前完成情况与文档治理统一见主项目 [README.md](../../README.md)。

## handbook 定位

- 面向面试讲解、项目理解与长期复盘。
- 保留 `01~12` 章节、`INTERVIEW_GUIDE`、`PROJECT_BIBLE`、权威 Volume01。
- 技术规范以主项目 `docs/` 为唯一维护入口；重复镜像在归档候选区。

## 学习路线

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

## 面试路线（权威）

```text
Enterprise_Retail_Intelligence_Platform_ERIP_日本Agent面试_Volume01.md
↓
02_日本AI现场面试.md
↓
07_面试口头训练.md
↓
03_AI核心知识.md
↓
01_日本AI项目实战.md
↓
INTERVIEW_GUIDE.md
```

## 面试材料权威合并索引（V1.0）

| 优先级 | 文件 | 用途 | 状态 |
|---|---|---|---|
| 1 | `Enterprise_Retail_Intelligence_Platform_ERIP_日本Agent面试_Volume01.md` | **Volume01 唯一权威**（已合并旧 Volume 有价值问答） | 活动 |
| 2 | `01_日本AI项目实战.md` | 业务主链、架构、担当 | 活动 |
| 3 | `02_日本AI现场面试.md` | 自介、深掘、压迫 | 活动 |
| 4 | `03_AI核心知识.md` | **技术版本矩阵 + 技术知识点表** | 活动 |
| 5 | `07_面试口头训练.md` | 开口训练 | 活动 |
| 6 | `INTERVIEW_GUIDE.md` | 讲解稿 | 活动 |

| 历史文件 | 处理 |
|---|---|
| `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | **已合并并移至待删除区** [`../_archive_candidate/ai-agent-retail-handbook-v3/`](../_archive_candidate/ai-agent-retail-handbook-v3/)；有价值内容已并入 ERIP Volume01 |

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

## 根目录活动文档

- [README.md](README.md)
- [AGENTS.md](AGENTS.md)
- [PROJECT_BIBLE.md](PROJECT_BIBLE.md)
- [01_日本AI项目实战.md](01_日本AI项目实战.md)
- [02_日本AI现场面试.md](02_日本AI现场面试.md)
- [03_AI核心知识.md](03_AI核心知识.md)
- [04_日本现场开发.md](04_日本现场开发.md)
- [05_TL代码审查.md](05_TL代码审查.md)
- [06_学习路线.md](06_学习路线.md)
- [07_面试口头训练.md](07_面试口头训练.md)
- [08_架构图册.md](08_架构图册.md)
- [09_系统设计书.md](09_系统设计书.md)
- [09_系统设计书_7.0_Technical_Architecture_增补_修改版.md](09_系统设计书_7.0_Technical_Architecture_增补_修改版.md)
- [10_Production_Roadmap.md](10_Production_Roadmap.md)
- [11_Project_Structure.md](11_Project_Structure.md)
- [12_ADR.md](12_ADR.md)
- [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)
- [Enterprise_Retail_Intelligence_Platform_ERIP_日本Agent面试_Volume01.md](Enterprise_Retail_Intelligence_Platform_ERIP_日本Agent面试_Volume01.md)

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
- [../_archive_candidate/ai-agent-retail-handbook-v3/](../_archive_candidate/ai-agent-retail-handbook-v3/)（旧 Volume01）
- [../_archive_candidate/handbook-docs/](../_archive_candidate/handbook-docs/)
- [../_archive_candidate/handbook-root/](../_archive_candidate/handbook-root/)

## 维护规则

- 不直接删除文档；完成合并后移入 `_archive_candidate`。
- 面试背诵只使用上表「活动」文件。
- 活动文档链接必须指向真实存在的路径。

## 更新日志

- V3: handbook 统一结构。
- V1.0 Final Doc Pass: ERIP 名称、数字、版本表。
- **V1.0 Volume 合并 (2026-07-17)**: ERIP Volume01（旧稿已归档） 真合并；旧 Volume 移入 `_archive_candidate/ai-agent-retail-handbook-v3/`；`03` 版本矩阵+知识点表定稿；活动文档链接修复。
