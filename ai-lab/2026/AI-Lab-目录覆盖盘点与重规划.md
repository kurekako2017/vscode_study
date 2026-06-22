# AI-Lab 目录覆盖盘点与重规划

> 盘点日期：2026-06-22
>
> 说明：本文是当前 `ai-lab` 主学习体系的覆盖总览，重点反映排除三仓后的真实目录状态。已落地内容以 [2026/2026补齐实施状态.md](./2026补齐实施状态.md) 为准；本文负责给出目录职责、覆盖分层和后续归位原则。

---

# 一、盘点范围

## 目标来源

本次盘点仍然以 `2026/` 目录中的学习路线和项目规划为目标地图，覆盖：

- LangChain 1.x / LCEL
- 结构化输出
- Tool Calling
- RAG 2.0
- LangGraph
- Checkpoint / Memory / Human In The Loop
- MCP Client / Server / Remote / Multi MCP
- Multi-Agent
- Deep Research
- 企业知识库、SES 营业、面试、Office、客服、Coding / GitHub 作品集
- 前端、FastAPI、部署、评估、运维、测试、面试

## 当前仓库主要目录

| 目录 | 当前定位 |
| --- | --- |
| `ai-learn/llm-lab/` | LLM 基础、模型调用、结构化输出、基础 RAG、FastAPI、评估、岗位准备 |
| `ai-learn/agent-lab/` | Tool Calling、工作流、RAG 工具化、流式服务化 |
| `ai-learn/agent-advanced/` | LCEL、LangGraph、MCP、高级 RAG、Multi-Agent、Tracing、业务作品集 |
| `2026/` | 总纲、覆盖盘点、实施状态、路线入口 |
| `ai-agents-from-zero/`、`all-in-rag-main/`、`hello-agents-main/` | 仍作为素材仓库，不作为主线依赖 |

---

# 二、总体结论

`ai-lab` 目前已经不是“缺基础能力”，而是“主线目录已经齐备，剩余差距集中在生产化与真实外部集成”。

目前可以稳定支撑的内容：

- 基础 LLM、结构化输出、Runnable / LCEL、Tool Calling、基础 RAG、FastAPI。
- 高级 RAG、混合检索、引用、权限过滤、RAG 评估。
- LangGraph 企业能力、真实 Multi-Agent 图编排、MCP 全链路、Deep Research、Tracing。
- 日本 SES 营业、面试、MCP Office、企业客服、Coding / GitHub 等业务 MVP。

仍需继续补强的内容：

- 生产级持久化和远程协议认证。
- 真实 reranker、真实搜索抓取、事实核验。
- 统一测试模板、覆盖率门槛、CI/CD。
- 业务作品集的 API / UI / Docker / 回归测试整合。

因此，目录重规划的重点不再是“新增大类”，而是“统一入口 + 统一交付标准 + 统一状态跟踪”。

---

# 三、覆盖等级说明

| 等级 | 含义 |
| --- | --- |
| 完整覆盖 | 有学习文档、可运行 demo、运行说明和验收方式 |
| 基础覆盖 / MVP | 有文档和示例，能演示，仍缺生产级细节 |
| 文档覆盖 | 有说明，没有对应可运行示例，或只保留为规划 |
| 示例覆盖 | 有代码，但缺系统学习文档、任务和验收标准 |
| 缺失 | 当前主学习目录没有明确文档和示例 |

---

# 四、能力清单覆盖矩阵

## 1. 基础 LLM 与结构化输出

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| Python 面向 LLM 开发 | 完整覆盖 | `ai-learn/llm-lab/00-Python学习范围（面向LLM应用开发）.md`、`ai-learn/llm-lab/examples/` | 可继续补练习题和测试 |
| 模型调用 | 完整覆盖 | `ai-learn/llm-lab/02-模型调用基础.md`、`ai-learn/agent-lab/projects/chat_cli/` | 已形成稳定入口 |
| 结构化输出 | 完整覆盖 | `ai-learn/llm-lab/03-结构化输出.md`、`ai-learn/agent-lab/projects/structured_output_demo/` | 可继续补复杂 schema |
| Prompt / Message | 基础覆盖 | `ai-learn/agent-advanced/projects/langchain_chain_demo/`、课程笔记 | 还可补 Prompt 测试与注入防护 |
| Pydantic / Schema | 完整覆盖 | `structured_output_demo`、`rag_api_demo` | 可继续补失败修复示例 |

结论：基础层已经足够，不需要再分裂成新的目录。

## 2. LangChain 1.x / LCEL

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| LCEL / Runnable | 完整覆盖 | `ai-learn/llm-lab/examples/runnable_composition_demo/`、`ai-learn/agent-advanced/projects/langchain_chain_demo/` | 已可作为路线入口 |
| RunnableLambda / Parallel / Branch | 基础覆盖 | `langchain_chain_demo` | 可继续拆分为更细练习 |
| Tool Calling in LangChain | 完整覆盖 | `ai-learn/agent-lab/projects/tool_agent_demo/` | 已可演示 |
| AgentExecutor 迁移认知 | 文档覆盖 | `2026` 目录与课程资料 | 已不作为主路线核心 |

## 3. RAG 2.0 / 企业知识库

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| 基础 RAG | 完整覆盖 | `ai-learn/llm-lab/04-RAG.md`、`ai-learn/agent-lab/projects/doc_qa_agent/` | 入门闭环已完成 |
| RAG API 化 | 完整覆盖 | `ai-learn/llm-lab/05-FastAPI与企业集成.md`、`ai-learn/agent-lab/projects/rag_api_demo/` | 有 API 与客户端 |
| 向量库基础 | 完整覆盖 | `ai-learn/agent-advanced/projects/vector_db_demo/` 等 | 可继续补统一选型 |
| 高级 RAG 模式 | 基础覆盖 / MVP | `ai-learn/agent-advanced/rag/advanced-patterns/` | 适合教学，不是生产级实现 |
| Hybrid Search | 完整覆盖 | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/` | 可作为企业知识库底座 |
| 权限过滤与引用 | 完整覆盖 | `internal_hybrid_rag_demo` | 后续可补租户隔离测试 |
| RAG 评估 | 基础覆盖 | `ai-learn/llm-lab/06-评估与运维.md`、`ai-learn/agent-advanced/eval/rag_eval_demo/` | 还缺统一数据集和门槛 |

## 4. LangGraph 与 Multi-Agent

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| State / Node / Edge | 完整覆盖 | `ai-learn/agent-advanced/projects/langgraph_workflow_demo/` | 入门已够用 |
| Conditional Edge / Loop | 完整覆盖 | `langgraph_workflow_demo` | 可继续补业务场景 |
| Checkpoint / Memory / HITL / Subgraph / Streaming | 完整覆盖 | `ai-learn/agent-advanced/langgraph-enterprise/` | 教学闭环已经落地 |
| Multi-Agent 角色认知 | 完整覆盖 | `ai-learn/agent-advanced/multi-agent/graph_team_demo/` | 已能作为示例 |
| Supervisor / Handoff | 基础覆盖 | `ai-learn/agent-advanced/multi-agent/README.md`、`graph_team_demo` | 可继续增强路由与评审 |
| 失败恢复、预算与终止 | 基础覆盖 | `multi-agent`、`deep-research` | 还可补 guardrail 规则 |

## 5. MCP、Deep Research 与业务项目

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| MCP 概念与安全边界 | 完整覆盖 | `ai-learn/agent-advanced/mcp/README.md` | 已有主线入口 |
| MCP Server / Client / Router | 完整覆盖 | `ai-learn/agent-advanced/mcp/server.py`、`client.py`、`multi_router.py` | 已形成闭环 |
| Remote MCP | 基础覆盖 | `ai-learn/agent-advanced/mcp/` | 还需生产级认证和 TLS |
| LangGraph + MCP | 基础覆盖 | `2026` 路线与目录链路 | 可继续补真实组合样例 |
| Deep Research | 基础覆盖 / MVP | `ai-learn/agent-advanced/deep-research/` | 已可作为学习索引和项目入口 |
| 企业知识库 Agent | 基础覆盖 / MVP | `internal_hybrid_rag_demo` | 还可收敛成单一成品 |
| 日本 SES 营业 Agent | 基础覆盖 / MVP | `business-agents/japan_ses_sales_agent/` | 仍需 API / UI / Docker / 测试 |
| 面试 Agent | 基础覆盖 / MVP | `business-agents/interview_agent/` | 仍需会话历史与 rubric 校准 |
| MCP Office Agent | 基础覆盖 / MVP | `business-agents/mcp_office_agent/` | 仍需真实 Office MCP 适配 |
| 企业客服 Agent | 基础覆盖 / MVP | `business-agents/enterprise_customer_service_agent/` | 仍需高级 RAG 与评估 |
| Coding / GitHub Agent | 基础覆盖 / MVP | `business-agents/coding_github_agent/` | 仍需 GitHub App、sandbox、PR 流程 |

## 6. 工程化与交付

| 目标能力 | 覆盖等级 | 当前位置 | 说明 |
| --- | --- | --- | --- |
| Docker / 健康检查 | 完整覆盖 | `deployment/container_demo`、`rag_api_demo` | 有可用入门材料 |
| 测试与 smoke check | 基础覆盖 | `rag_api_demo/mock_test.py`、`smoke_check.sh` | 还缺统一 pytest 模板 |
| 日志 / Tracing / 可观测 | 基础覆盖 | `observability/tracing_demo` | 还可接真实 tracing 后端 |
| 安全 / 权限 | 基础覆盖 | `internal_hybrid_rag_demo`、`mcp`、业务 agent 限制 | 还可补审计与 injection 测试 |
| 成本 / 限流 / 重试 | 文档覆盖 | 各路线文档中 | 还缺统一中间件实现 |
| CI/CD | 文档覆盖 | 规划中 | 还缺实际 workflow |

---

# 五、目录归位原则

1. `ai-learn/llm-lab/` 只放单能力基础练习，不放复杂 Agent 项目。
2. `ai-learn/agent-lab/` 只放基础 Agent、通用执行约束和服务化过渡示例。
3. `ai-learn/agent-advanced/` 承接高级框架、协议、组合系统、工程模板和作品集。
4. 新专题统一采用 `README → 最小 demo → 练习任务 → 测试 → 验收标准` 的结构。
5. 优先扩展现有目录，不再依赖三仓作为主路线内容。
6. 默认保留离线 / mock 路径；真实协议、数据库和远程服务保留独立运行路径。

---

# 六、实施优先级

## P0：工程化底座

| 顺序 | 内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 1 | 统一测试模板 | `ai-learn/agent-advanced/` 及其子项目 | 一条命令跑通核心 demo 的正常、异常、权限路径 |
| 2 | CI/CD 门禁 | `.github/workflows/` 或统一模板 | 覆盖测试、lint、基础构建 |
| 3 | 业务项目共用交付模板 | `business-agents/` | README、需求概要、基本设计、测试观点、用例表统一 |

## P1：真实外部集成

| 顺序 | 内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 4 | Remote MCP 生产化 | `ai-learn/agent-advanced/mcp/` | 认证、TLS、超时、错误路径说明完整 |
| 5 | 高级 RAG 真实后端 | `ai-learn/agent-advanced/rag/advanced-patterns/` | 至少一个真实 reranker 或真实检索后端接入 |
| 6 | Deep Research 真实搜索与事实核验 | `ai-learn/agent-advanced/deep-research/` | 计划、检索、去重、引用、审校闭环可验收 |

## P2：业务作品集收口

| 顺序 | 项目 | 后续动作 |
| --- | --- | --- |
| 7 | 日本 SES 营业 Agent | 补 API / UI / 持久化 / 测试 / Docker |
| 8 | 面试 Agent | 补会话历史、rubric 校准与前端展示 |
| 9 | MCP Office Agent | 接真实 Office MCP 服务并补审计 |
| 10 | 企业客服 Agent | 统一 RAG、HITL、评估与观测 |
| 11 | Coding / GitHub Agent | 补 GitHub App、sandbox 和 PR 工作流 |

---

# 七、统一交付标准

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

---

# 八、最终目录职责

```text
2026/                 目标、阶段计划、覆盖盘点、实施状态、验收总纲
ai-learn/llm-lab/     LLM 应用基础和单能力练习
ai-learn/agent-lab/   基础 Agent、工具、工作流和服务化过渡
ai-learn/agent-advanced/
                      高级框架、协议、组合系统、工程模板和作品集
```

本规划的新增文档和示例限定在上述四个目录内；三个排除目录继续保持独立，不作为主学习路线依赖。

---

# 九、与实施状态的关系

本文不承担实时完成度登记职责。已经落地的内容统一以 [2026/2026补齐实施状态.md](./2026补齐实施状态.md) 为准；后续新增内容先更新实施状态，再回写本文的覆盖矩阵和优先级。

