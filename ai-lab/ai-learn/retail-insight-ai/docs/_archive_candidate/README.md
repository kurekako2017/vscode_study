# 待人工确认废弃文档区

这里是“待人工确认废弃文档区”。

放进这里的文件不代表立刻删除。只有确认内容已经合并到唯一主文档后，未来才可以删除。

## 为什么归档

归档用于处理已经完成内容迁移、已经有主文档承接、并且不应该继续双线维护的 Markdown。

## 什么时候删除

未来删除必须同时满足：

- README 仍然有替代入口。
- 主文档已经承接所有有价值内容。
- 人工确认归档文件没有独有内容。
- 删除动作被单独记录在 `docs/CHANGELOG.md` 和 `docs/governance/PROJECT_BACKLOG.md`。

## 归档原则

```text
补充 Append
↓
合并 Merge
↓
移动 Move
↓
归档 Archive
↓
未来人工确认 Delete
```

禁止事项：

- 不能直接删除文档。
- 不能把未迁移内容放进这里。
- 不能继续把这里的文件当主文档维护。

## 当前归档候选文件

| 文件 | 原路径 | 主维护文件 | 为什么移动 | 是否已合并 | 是否停止维护 | 未来删除条件 |
|---|---|---|---|---|---|---|
| [RUNBOOK_LOCAL.md](RUNBOOK_LOCAL.md) | `RUNBOOK_LOCAL.md` | `README.md`、`docs/LEARNING_API_WALKTHROUGH.md`、`docs/TEST_CASES.md`、`VERIFY_CHECKLIST.md` | 启动、Swagger、ReDoc、OpenAPI、验证、测试和排错内容已由主文档承接 | 是 | 是 | 人工确认没有独有排错内容 |
| [root/STUDY_PLAN_DAY1_DAY3.md](root/STUDY_PLAN_DAY1_DAY3.md) | `STUDY_PLAN_DAY1_DAY3.md` | `README.md`、`docs/LEARNING_API_WALKTHROUGH.md`、`docs/TEST_CASES.md`、`CODE_STUDY_GUIDE.md` | 三日学习路线已由 README 学习路线和主学习文档承接 | 是 | 是 | 人工确认没有独有学习安排 |
| [handbook-root/TASK.md](handbook-root/TASK.md) | `docs/ai-agent-retail-handbook-v3/TASK.md` | `TASK.md` | handbook 侧任务文档与根任务文档重复 | 是 | 是 | 人工确认无需保留 handbook 侧任务镜像 |
| [handbook-root/ROADMAP.md](handbook-root/ROADMAP.md) | `docs/ai-agent-retail-handbook-v3/ROADMAP.md` | `ROADMAP.md` | handbook 侧路线图与根路线图重复 | 是 | 是 | 人工确认无需保留 handbook 侧路线图镜像 |
| [handbook-docs/AI_AGENT_DESIGN_GUIDE.md](handbook-docs/AI_AGENT_DESIGN_GUIDE.md) | `docs/ai-agent-retail-handbook-v3/docs/AI_AGENT_DESIGN_GUIDE.md` | `docs/AI_AGENT_DESIGN_GUIDE.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/API_CONTRACT.md](handbook-docs/API_CONTRACT.md) | `docs/ai-agent-retail-handbook-v3/docs/API_CONTRACT.md` | `docs/API_CONTRACT.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/ARCHITECTURE.md](handbook-docs/ARCHITECTURE.md) | `docs/ai-agent-retail-handbook-v3/docs/ARCHITECTURE.md` | `docs/ARCHITECTURE.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/CHANGELOG.md](handbook-docs/CHANGELOG.md) | `docs/ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | `docs/CHANGELOG.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/CODING_STANDARD.md](handbook-docs/CODING_STANDARD.md) | `docs/ai-agent-retail-handbook-v3/docs/CODING_STANDARD.md` | `docs/CODING_STANDARD.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/DECISIONS.md](handbook-docs/DECISIONS.md) | `docs/ai-agent-retail-handbook-v3/docs/DECISIONS.md` | `docs/DECISIONS.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/DEVELOPMENT_GUIDE.md](handbook-docs/DEVELOPMENT_GUIDE.md) | `docs/ai-agent-retail-handbook-v3/docs/DEVELOPMENT_GUIDE.md` | `docs/DEVELOPMENT_GUIDE.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/ERROR_CATALOG.md](handbook-docs/ERROR_CATALOG.md) | `docs/ai-agent-retail-handbook-v3/docs/ERROR_CATALOG.md` | `docs/ERROR_CATALOG.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/EVENT_CONTRACT.md](handbook-docs/EVENT_CONTRACT.md) | `docs/ai-agent-retail-handbook-v3/docs/EVENT_CONTRACT.md` | `docs/EVENT_CONTRACT.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/MASTER_PROMPT.md](handbook-docs/MASTER_PROMPT.md) | `docs/ai-agent-retail-handbook-v3/docs/MASTER_PROMPT.md` | `docs/MASTER_PROMPT.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/governance/PROJECT_BACKLOG.md](handbook-docs/governance/PROJECT_BACKLOG.md) | `docs/ai-agent-retail-handbook-v3/docs/governance/PROJECT_BACKLOG.md` | `docs/governance/PROJECT_BACKLOG.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/PROMPT_STANDARD.md](handbook-docs/PROMPT_STANDARD.md) | `docs/ai-agent-retail-handbook-v3/docs/PROMPT_STANDARD.md` | `docs/PROMPT_STANDARD.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |
| [handbook-docs/UPLOAD_POLICY.md](handbook-docs/UPLOAD_POLICY.md) | `docs/ai-agent-retail-handbook-v3/docs/UPLOAD_POLICY.md` | `docs/UPLOAD_POLICY.md` | handbook 技术规范镜像，改为引用主 docs | 是 | 是 | 人工确认镜像无独有内容 |

## 仍保留的重复关系

| 文档 | 为什么仍保留 |
|---|---|
| `README.md` vs `docs/ai-agent-retail-handbook-v3/README.md` | 根 README 是项目唯一入口，handbook README 是长期知识库入口，职责不同 |
| `docs/LEARNING_API_WALKTHROUGH.md` vs `docs/ai-agent-retail-handbook-v3/06_学习路线.md` | 前者是接口学习细节，后者是长期学习路线 |
| `docs/TEST_CASES.md` vs `docs/ai-agent-retail-handbook-v3/interview/07_面试口头训练.md` | 前者是测试学习，后者是口头面试训练 |
| `CODE_STUDY_GUIDE.md` vs `docs/ai-agent-retail-handbook-v3/11_Project_Structure.md` | 前者是源码阅读路线，后者是 handbook 项目结构理解 |

## 人工确认重点

- 归档文件是否还有主文档未承接的独有内容。
- handbook 根目录文档是否继续承担长期学习价值。
- 任何未来删除动作都必须先确认 README 仍有替代入口。

## ai-agent-retail-handbook-v3（见下）

| 文件 | 说明 |
|---|---|
| `handbook-interview/Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | 旧 Volume01；已并入 ERIP 权威 Volume01 后移入此处 |

**唯一权威 Volume01：** `docs/ai-agent-retail-handbook-v3/interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md`

## ai-agent-retail-handbook-v3（待删除区 · 2026-07-17）

| 文件 | 说明 |
|---|---|
| `ai-agent-retail-handbook-v3/Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | 旧 Volume01；已合并入 ERIP 权威 Volume01 后移入本目录 |

**唯一权威 Volume01：** `docs/ai-agent-retail-handbook-v3/interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md`

