# AI-LAB 项目治理审计报告

最后更新：2026-06-29

## 审计范围

本次按照 AI-LAB 全局规则检查以下标准治理文件：

- `AGENTS.md`
- `README.md`
- `TASK.md`
- `docs/PROJECT_BACKLOG.md`
- `docs/CHANGELOG.md`

所有项目原有 `README.md` 均保留且未修改。已有治理文件没有覆盖或删除。

## 项目检查与自动修复

| 项目名称 | 项目路径 | 修复后是否完整 | 修复前缺失文件 | 自动修复内容 | 推荐优先级 |
| --- | --- | --- | --- | --- | --- |
| ai-agents-from-zero | `ai-agents-from-zero/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P2 |
| deepsearch-agents-main | `ai-agents-from-zero/deepsearch-agents-main/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P0 |
| shopkeeper-agent-main | `ai-agents-from-zero/shopkeeper-agent-main/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P0 |
| ai-learn | `ai-learn/` | 是 | TASK、PROJECT_BACKLOG、CHANGELOG | 保留原AGENTS，创建3份治理文件 | P1 |
| agent-advanced | `ai-learn/agent-advanced/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P1 |
| agent-lab | `ai-learn/agent-lab/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P1 |
| ai-agent-retail-handbook-v3 | `ai-learn/ai-agent-retail-handbook-v3/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P1 |
| internal-knowledge-approval-agent | `ai-learn/internal-knowledge-approval-agent/` | 是 | TASK、PROJECT_BACKLOG、CHANGELOG | 保留原AGENTS，创建3份治理文件 | P0 |
| knowledge-base-draft | `ai-learn/knowledge-base-draft/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P1 |
| llm-lab | `ai-learn/llm-lab/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P1 |
| retail-insight-ai | `ai-learn/retail-insight-ai/` | 是 | 无 | 无；保留全部既有治理文件 | P0 |
| all-in-rag-main | `all-in-rag-main/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P2 |
| hello-agents-main | `hello-agents-main/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P2 |
| stock-agent | `stock-agent/` | 是 | AGENTS、TASK、PROJECT_BACKLOG、CHANGELOG | 创建4份治理文件 | P0 |

## 优先级说明

### P0：正在开发项目

- `retail-insight-ai`
- `internal-knowledge-approval-agent`
- `stock-agent`
- `deepsearch-agents-main`
- `shopkeeper-agent-main`

建议优先把模板中的“待确认”替换为项目实际阶段，并完成项目结构、Docker、`.gitignore` 和 README 检查。

### P1：学习项目

- `ai-learn`
- `agent-advanced`
- `agent-lab`
- `ai-agent-retail-handbook-v3`
- `knowledge-base-draft`
- `llm-lab`

建议根据现有学习路线登记真实目标、当前章节、下一项练习和长期技术债。

### P2：历史 Demo 项目

- `ai-agents-from-zero`
- `all-in-rag-main`
- `hello-agents-main`

建议将第三方原始内容保持只读，在 Backlog 中记录本地学习目标、上游版本和是否允许修改。

## 审计结论

- 标准化项目数：14
- 修复前完整项目数：1
- 自动补全项目数：13
- 新增治理文件数：50
- 修复后完整项目数：14
- 被覆盖或删除的既有文件数：0

本次只建立本地治理文件和审计报告，没有修改项目代码。
