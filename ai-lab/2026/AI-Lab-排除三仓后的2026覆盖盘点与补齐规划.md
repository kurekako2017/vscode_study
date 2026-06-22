# AI-Lab 排除三仓后的 2026 覆盖盘点与补齐规划

> 盘点日期：2026-06-22
>
> 说明：本稿是 2026-06-21 第一轮补齐完成后的复核版。当前完成度以 [2026/2026补齐实施状态.md](./2026补齐实施状态.md) 为准；本文只负责说明在排除三仓后，`ai-lab` 主学习体系的覆盖情况、仍需补强的工程化短板，以及后续目录归位原则。

## 一、范围与判定规则

### 明确排除

本报告不读取、不引用、也不把以下目录计入覆盖证据：

- `all-in-rag-main/`
- `hello-agents-main/`
- `ai-agents-from-zero/`

后续补齐内容也不得写入上述三个目录。

### 纳入盘点

| 目录 | 在体系中的定位 |
| --- | --- |
| `ai-learn/llm-lab/` | Python、模型调用、结构化输出、基础 RAG、FastAPI、评估与岗位准备 |
| `ai-learn/agent-lab/` | Tool Calling、固定工作流、RAG 工具化、基础 Agent 产品化 |
| `ai-learn/agent-advanced/` | LangChain、LangGraph、高级 RAG、Multi-Agent、前端、评估与部署 |
| `2026/` | 目标能力清单、盘点与实施状态，不作为“已实现”证据 |

### 覆盖等级

| 等级 | 判定标准 |
| --- | --- |
| A 完整覆盖 | 有学习文档、可运行示例、运行说明和基本验收方式 |
| B 基础覆盖 / MVP | 有文档和示例，且已经可以演示，但距离生产级仍有差距 |
| C 文档覆盖 | 有说明，没有对应可运行示例或只作为规划存在 |
| D 示例覆盖 | 有代码，但缺系统学习文档、任务和验收标准 |
| E 缺失 | 主学习目录中没有明确文档和示例 |

说明：代码中出现关键词不等于覆盖；纯 Python 的概念模拟也不能替代真实协议、框架或外部组件接入。

## 二、当前总判断

排除三个素材仓库后，`ai-lab` 现在已经不再是“缺主线”，而是“主线已成型，剩余问题集中在生产化和真实外部集成”。

当前三层结构保持合理，不需要再新增新的平行学习根目录。能力归位仍然遵循：

```text
llm-lab
  基础知识、单功能练习
      ↓
agent-lab
  Tool Calling、受控工作流、服务化基础
      ↓
agent-advanced
  LangGraph、MCP、高级 RAG、Multi-Agent、Deep Research、工程交付
```

### 当前已形成的覆盖面

- 基础 LLM、结构化输出、基础 RAG、FastAPI、React / Spring 接入已经形成闭环。
- Runnable / LCEL、Tool Calling、Streaming Agent API、LangGraph 企业能力、MCP、真实 Multi-Agent、Deep Research、Tracing、五个业务 Agent 已经落地为文档加示例或 MVP。
- `ai-learn/agent-advanced/` 已经成为 2026 主线的承接目录，不再只是“规划中的目标目录”。

### 当前仍需补强的部分

- 生产级持久化、真实 reranker、真实搜索抓取、事实核验、Remote MCP 的认证与 TLS。
- 统一测试模板、覆盖率门槛、CI/CD 质量门禁。
- 业务项目从 MVP 进一步提升到 API、UI、持久化、Docker、回归测试完整交付。

## 三、2026 目标覆盖矩阵

### 1. 基础 LLM、LangChain 与服务化

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| Python 面向 LLM 开发 | A | `ai-learn/llm-lab/00-Python学习范围（面向LLM应用开发）.md`、`ai-learn/llm-lab/examples/` | 可继续补阶段练习题 |
| 模型调用与供应商切换 | A | `ai-learn/llm-lab/02-模型调用基础.md`、`ai-learn/agent-lab/projects/chat_cli/`、`API配置与兼容策略.md` | 可继续补统一 timeout / retry / rate-limit 示例 |
| 结构化输出与 Pydantic | A | `ai-learn/llm-lab/03-结构化输出.md`、`ai-learn/agent-lab/projects/structured_output_demo/` | 可继续补复杂嵌套 schema 和失败修复 |
| Prompt / Message | B | `ai-learn/agent-advanced/projects/langchain_chain_demo/`、相关课程笔记 | 缺独立 Prompt 测试与注入防护专题 |
| LCEL / Runnable | A | `ai-learn/llm-lab/examples/runnable_composition_demo/`、`ai-learn/agent-advanced/projects/langchain_chain_demo/` | 可继续补更完整的 batch / stream 对照 |
| Tool Calling | A | `ai-learn/agent-lab/03-Tool Calling.md`、`ai-learn/agent-lab/projects/tool_agent_demo/` | 可继续补并行调用、审批、幂等性 |
| FastAPI 服务化 | A | `ai-learn/llm-lab/05-FastAPI与企业集成.md`、`ai-learn/agent-lab/projects/rag_api_demo/` | 可继续补统一 SSE 流式模板 |
| React / Java 接入 | B | `ai-learn/agent-lab/projects/rag_api_demo/react-client/`、`spring-client/`、`ai-learn/agent-advanced/frontend/chat_ui_demo/` | 缺与高级 Agent 的完整联调 |

### 2. RAG 2.0 与企业知识库

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| 基础文档 RAG | A | `ai-learn/llm-lab/04-RAG.md`、`ai-learn/agent-lab/projects/doc_qa_agent/` | 已足够作为入门 |
| 向量库与 metadata | A | `ai-learn/agent-advanced/projects/vector_db_demo/`、`vector_db_qdrant_demo/`、`vector_db_chroma_demo/` | 可继续补统一选型说明 |
| Query Rewrite / Multi Query | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 仍以教学实现为主，缺真实召回对比实验 |
| Rerank | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 缺真实 cross-encoder / reranker 接入 |
| Hybrid Search | A | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/`、`ai-learn/agent-advanced/rag/社内文件与Wiki混合检索RAG.md` | 可再接真实检索后端 |
| 来源引用与权限过滤 | A | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/` | 可继续补租户隔离和越权测试 |
| Parent Document Retriever | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 仍是简化教学实现，缺更大规模数据集 |
| Contextual Compression | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 缺与真实压缩组件的对比 |
| HyDE | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 缺更完整评估集 |
| Self-RAG / Corrective RAG | B | `ai-learn/agent-advanced/rag/advanced-patterns/` | 缺更强的路由/回退评估 |
| GraphRAG | C | 仍以规划和外部资料为主 | 可列为选修，不抢核心路线优先级 |
| RAG 评估 | B | `ai-learn/llm-lab/06-评估与运维.md`、`ai-learn/agent-advanced/eval/rag_eval_demo/` | 缺统一数据集规范和 CI 回归门槛 |

### 3. LangGraph 与 Multi-Agent

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| State / Node / Edge | A | `ai-learn/agent-advanced/projects/langgraph_workflow_demo/`、`ai-learn/agent-advanced/frameworks/langgraph/README.md` | 已适合作为入门 |
| Conditional Edge / Loop | A | `ai-learn/agent-advanced/projects/langgraph_workflow_demo/` | 可继续补最大步数和异常分支 |
| Reducer / MessagesState | B | `ai-learn/agent-advanced/langgraph-enterprise/` | 教学闭环已成型，仍可补更多状态合并案例 |
| ToolNode | B | `ai-learn/agent-advanced/langgraph-enterprise/` | 可继续补与真实工具链的对照 |
| Checkpoint / Thread | A | `ai-learn/agent-advanced/langgraph-enterprise/` | 生产级 Postgres 持久化仍可增强 |
| 短期 / 长期 Memory | A | `ai-learn/agent-advanced/langgraph-enterprise/` | 可继续补 store 边界说明 |
| Human In The Loop | A | `ai-learn/agent-advanced/langgraph-enterprise/` | 可继续补更复杂审批流 |
| Subgraph | A | `ai-learn/agent-advanced/langgraph-enterprise/` | 可继续补跨子图共享状态 |
| Streaming | B | `ai-learn/agent-advanced/langgraph-enterprise/`、`ai-learn/agent-advanced/frontend/chat_ui_demo/` | 仍可继续增强前后端联动 |
| Time Travel / Replay | C | 作为选修保留 | 不作为当前主线优先项 |
| Multi-Agent 角色认知 | A | `ai-learn/agent-advanced/multi-agent/graph_team_demo/` | 后续可接更严格质量/成本评估 |
| Supervisor / Handoff | B | `ai-learn/agent-advanced/multi-agent/README.md`、`graph_team_demo` | 仍可补更复杂的图路由 |
| 失败恢复、预算与终止 | B | `ai-learn/agent-advanced/multi-agent/README.md`、`deep-research` | 可继续补可执行 guardrail |

### 4. MCP、Deep Research 与业务项目

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| MCP 概念与安全边界 | A | `ai-learn/agent-advanced/mcp/README.md` | 可继续补协议级安全讲解 |
| MCP Server / FastMCP | A | `ai-learn/agent-advanced/mcp/server.py` | 可继续补更明确的运行说明 |
| MCP Client | A | `ai-learn/agent-advanced/mcp/client.py` | 可继续补工具发现与错误处理细化 |
| Remote MCP | B | 已有设计与目录位 | 仍需生产级认证、TLS 与部署说明 |
| Multi-MCP Router | A | `ai-learn/agent-advanced/mcp/multi_router.py` | 可继续补冲突处理与审计 |
| LangGraph + MCP | B | 已进入主线规划与目录链路 | 可继续补真实组合示例 |
| Deep Research | B | `ai-learn/agent-advanced/deep-research/` | 仍需真实搜索、抓取和事实评估强化 |
| 企业知识库 Agent | B | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/` 可承接 | 还未收敛成单一成品 |
| 日本 SES 营业 Agent | B | `ai-learn/agent-advanced/business-agents/japan_ses_sales_agent/` | 还需 API / UI / 持久化 / 测试 / Docker |
| 面试 Agent | B | `ai-learn/agent-advanced/business-agents/interview_agent/` | 还需会话历史和 rubric 校准 |
| MCP Office Agent | B | `ai-learn/agent-advanced/business-agents/mcp_office_agent/` | 还需真实 Office MCP 适配 |
| 企业客服 Agent | B | `ai-learn/agent-advanced/business-agents/enterprise_customer_service_agent/` | 还需高级 RAG、HITL API 和评估 |
| Coding / GitHub Agent | B | `ai-learn/agent-advanced/business-agents/coding_github_agent/` | 还需 GitHub App、sandbox 和 PR 工作流 |

### 5. 工程化与交付

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| Docker / 健康检查 | A | `ai-learn/agent-advanced/deployment/container_demo/`、`ai-learn/agent-lab/projects/rag_api_demo/` | 可继续补 Compose 多服务 |
| 测试与 smoke check | B | `ai-learn/agent-lab/projects/rag_api_demo/mock_test.py`、`smoke_check.sh` 等 | 缺统一 pytest / fixture / 覆盖率门槛 |
| 日志 / Tracing / 可观测 | B | `ai-learn/agent-advanced/observability/tracing_demo/` | 可继续接真实 tracing 后端 |
| 安全 / 权限 | B | 工具边界、RAG ACL、MCP allowlist、业务 agent 限制 | 可继续补 prompt injection 与审计测试 |
| 成本 / 限流 / 重试 | C | 文档中已有说明 | 仍缺统一中间件和标准示例 |
| CI/CD | C | 规划中 | 仍缺实际 workflow 和质量门禁模板 |
| 交付清单 | A | `ai-learn/agent-advanced/交付前检查清单.md`、`开发测试部署流程.md` | 可继续转成项目通用模板 |

## 四、补齐内容的目录归位原则

1. `ai-learn/llm-lab/` 只补单一基础能力，不放复杂 Agent 项目。
2. `ai-learn/agent-lab/` 只补 Agent 基础、通用执行约束和服务化过渡示例。
3. `ai-learn/agent-advanced/` 承接全部 2026 高级专题和作品集项目。
4. 新专题统一采用“README → 最小 demo → 练习任务 → 测试 → 验收标准”的结构。
5. 优先扩展现有目录，不复制三个排除仓库的章节或代码。
6. 默认提供离线/mock 路径；涉及真实协议或数据库时，同时保留真实运行路径。

## 五、现状下的实施优先级

### P0：补齐工程化底座

| 顺序 | 内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 1 | 统一 pytest / fixture / coverage 模板 | `ai-learn/agent-advanced/` 下的通用模板或现有项目公共测试规范 | 一条命令跑通核心 demo 的 happy path、异常路径、权限路径 |
| 2 | CI/CD 质量门禁 | `.github/workflows/` 或统一模板 | 至少覆盖测试、lint、基础构建 |
| 3 | 业务项目的共用交付模板 | `ai-learn/agent-advanced/business-agents/` | README、需求概要、基本设计、测试观点、用例表统一 |

### P1：补强真实外部集成

| 顺序 | 内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 4 | Remote MCP 生产化 | `ai-learn/agent-advanced/mcp/` | 认证、TLS、超时、错误路径说明完整 |
| 5 | 高级 RAG 的真实后端 | `ai-learn/agent-advanced/rag/advanced-patterns/` | 至少一个真实 reranker 或真实检索后端接入 |
| 6 | Deep Research 的真实搜索与事实核验 | `ai-learn/agent-advanced/deep-research/` | 计划、检索、去重、引用、审校闭环可验收 |

### P2：业务作品集收口

| 顺序 | 项目 | 后续动作 |
| --- | --- | --- |
| 7 | 日本 SES 营业 Agent | 补 API / UI / 持久化 / 测试 / Docker |
| 8 | 面试 Agent | 补会话历史、rubric 校准与前端展示 |
| 9 | MCP Office Agent | 接真实 Office MCP 服务并补审计 |
| 10 | 企业客服 Agent | 统一 RAG、HITL、评估与观测 |
| 11 | Coding / GitHub Agent | 进一步补 GitHub App、sandbox 和 PR 工作流 |

## 六、统一交付标准

以后新增的每份示例至少满足：

- `README.md`：目标、前置知识、架构、运行命令、输入输出、限制。
- 可运行入口：默认离线/mock 可跑，真实模式的依赖和配置明确。
- `requirements.txt` 或统一依赖声明：避免隐式依赖。
- 自动化测试：至少包含 happy path、异常路径、边界 / 权限路径。
- 示例数据：小、固定、可重复，不能依赖排除目录。
- 观测信息：关键步骤、耗时、失败原因可见；高级项目补 token / 成本。
- 安全边界：目录访问、工具权限、密钥、远程调用和审批点明确。
- 验收标准：不能只写“运行成功”，需定义结果质量和失败行为。

业务作品集还应增加：

- `需求概要.md`
- `基本设计.md`
- `测试观点.md`
- `简单测试用例表.md`
- 架构 / 数据流图
- Docker 与一键启动方式
- 简历说明和面试讲解要点

## 七、最终目录职责

```text
2026/                 目标、阶段计划、覆盖盘点、实施状态、验收总纲
ai-learn/llm-lab/     LLM 应用基础和单能力练习
ai-learn/agent-lab/   基础 Agent、工具、工作流和服务化过渡
ai-learn/agent-advanced/
                      高级框架、协议、组合系统、工程模板和作品集
```

本规划的所有新增文档和示例都限定在上述四个目录内；三个排除目录继续保持独立，不作为主学习路线依赖。

## 八、与实施状态的关系

本文件不再承担“实时完成度登记”的职责。凡是已经落地的内容，统一以 [2026/2026补齐实施状态.md](./2026补齐实施状态.md) 为准；凡是后续新补的内容，先更新实施状态，再回写本文的覆盖矩阵和优先级。

这样可以避免规划正文和实际代码再次失同步。
