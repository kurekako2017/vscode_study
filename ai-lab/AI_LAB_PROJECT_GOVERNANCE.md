# AI-LAB Project Governance V2

最后更新：2026-06-29

## 1. 适用范围

本规范适用于 `ai-lab/` 下所有正式维护项目。第三方教材、历史 Demo 和嵌套示例优先由其项目根目录统一治理，除非用户明确要求独立治理。

## 2. 规则继承顺序

```text
ai-lab/AGENTS.md
        ↓
项目/AGENTS.md
        ↓
项目/ROADMAP.md
        ↓
项目/docs/PROJECT_BACKLOG.md
        ↓
项目/TASK.md
        ↓
开始开发
```

距离当前项目更近的规则优先，但不得降低全局安全、历史保护和敏感信息规则。

## 3. 项目标准结构

```text
project/
├── AGENTS.md
├── README.md
├── TASK.md
├── ROADMAP.md
└── docs/
    ├── PROJECT_BACKLOG.md
    ├── CHANGELOG.md
    ├── ARCHITECTURE.md
    └── DECISIONS.md
```

## 4. 文件职责

| 文件 | 职责 | 更新时机 |
| --- | --- | --- |
| `AGENTS.md` | 项目规则、安全边界和 AI 行为约束 | 规则变化时 |
| `README.md` | 项目入口、运行方式和能力边界 | 用户流程或运行方式变化时 |
| `ROADMAP.md` | 当前阶段、下一阶段和长期规划 | 阶段变化时 |
| `TASK.md` | 当前 Sprint、当前任务、下一任务和阻塞项 | 每次工作完成后 |
| `docs/PROJECT_BACKLOG.md` | 永久任务清单和技术债 | 每次工作开始与完成时 |
| `docs/CHANGELOG.md` | 日期、修改内容和影响文件 | 每次工作完成后 |
| `docs/ARCHITECTURE.md` | 技术、系统、Agent、RAG 和 MCP 架构 | 实现或架构变化时 |
| `docs/DECISIONS.md` | Architecture Decision Record | 重要决策形成时 |

## 5. 开发前流程

1. 读取项目 `AGENTS.md`。
2. 读取项目 `ROADMAP.md`。
3. 读取项目 `docs/PROJECT_BACKLOG.md`。
4. 读取项目 `TASK.md`。
5. 检查 README、技术债、已知问题和阻塞项。
6. 选择最高优先级且可执行的任务。

治理文件缺失时必须先报告并补齐，禁止绕过 Backlog 直接编码。

## 6. 开发后流程

1. 将完成任务从 `[ ]` 改为 `[x]`，不得删除。
2. 更新 `TASK.md` 的当前任务、下一任务和阻塞项。
3. 更新 `docs/PROJECT_BACKLOG.md` 的新任务、技术债和已知问题。
4. 更新 `docs/CHANGELOG.md`，记录日期、修改内容和影响文件。
5. 阶段发生变化时更新 `ROADMAP.md`。
6. 架构发生变化时更新 `ARCHITECTURE.md`。
7. 形成重要决策时在 `DECISIONS.md` 新增 ADR，不覆盖旧 ADR。

## 7. ADR 格式

```markdown
## ADR-001

日期：YYYY-MM-DD

决策：

原因：

备选方案：

影响：
```

ADR 编号递增。决策被替代时保留原记录，并标记状态及替代它的新 ADR。

## 8. 架构文档规则

- Mermaid 图必须与真实代码和部署方式一致。
- 尚未实现的 Agent、RAG 或 MCP 能力必须标记为规划或不适用。
- 不得把目标架构写成当前实现。
- 必须说明系统边界、数据边界、外部依赖、权限和失败处理。

## 9. 项目优先级

### P0：正在开发项目

1. `retail-insight-ai`
2. `internal-knowledge-approval-agent`
3. `stock-agent`
4. `deepsearch-agents-main`
5. `shopkeeper-agent-main`

### P1：学习项目

1. `ai-learn`
2. `agent-advanced`
3. `agent-lab`
4. `llm-lab`
5. `ai-agent-retail-handbook-v3`
6. `knowledge-base-draft`

### P2：历史 Demo 项目

1. `ai-agents-from-zero`
2. `all-in-rag-main`
3. `hello-agents-main`

## 10. 新项目初始化

1. 创建全部 V2 标准文件。
2. 在 AGENTS 中声明继承 AI-LAB 全局规则。
3. 根据真实项目填写 Roadmap 和 Architecture，不长期保留“待确认”。
4. 在 DECISIONS 中登记采用 V2 治理的 ADR。
5. 在 Backlog 中登记项目结构、安全、运行和测试任务。
6. 完成治理检查后才开始编码。

## 11. 历史与安全

- 禁止删除 Backlog、CHANGELOG、ADR 和历史任务。
- 禁止覆盖 README 或用模板替换已有项目说明。
- 禁止在治理文档中记录 API Key、Token、密码或客户原始数据。
- 涉及 `.env`、private 数据和真实业务资料时，必须先检查 `.gitignore` 与 Git 跟踪状态。

## 12. 当前治理状态

- V2 标准化项目：14
- 已创建 Roadmap：14
- 已创建 Architecture：14
- 已创建 Decisions：14
- 已更新项目 AGENTS：14

详细的 V1 修复记录参见 [AI_LAB_PROJECT_AUDIT.md](AI_LAB_PROJECT_AUDIT.md)。
