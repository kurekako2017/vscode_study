# AI-Lab 排除三仓后的 2026 覆盖盘点与补齐规划

> 盘点日期：2026-06-21  
> 目标：只使用适合作为长期学习体系的主目录核对 2026 能力目标，并规划缺失文档与可运行示例的新增位置。

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
| `2026/` | 目标能力清单和规划文档，不作为“已实现”的证据 |

### 覆盖等级

| 等级 | 判定标准 |
| --- | --- |
| A 完整覆盖 | 有学习文档、可运行示例、运行说明和基本验收方式 |
| B 基础覆盖 | 有文档和示例，但只覆盖最小概念，缺高级能力或工程化 |
| C 文档覆盖 | 有说明，没有对应可运行示例 |
| D 示例覆盖 | 有代码，但缺系统学习文档、任务和验收标准 |
| E 缺失 | 主学习目录中没有明确文档和示例 |

说明：代码中出现关键词不等于覆盖；纯 Python 的概念模拟也不能替代真实协议、框架或外部组件接入。

## 二、独立盘点结论

排除三个素材仓库后，当前主学习体系可以稳定支撑“LLM 应用基础 → 基础 Agent → RAG/工作流工程入门”，但还不能完整支撑 2026 目标中的“LangGraph 企业能力 → MCP → Multi-Agent 工程化 → Deep Research → 企业作品集”。

当前三层结构本身合理，不建议再建新的平行学习根目录。缺少的内容应按难度归位：

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

截至盘点日，三个目录约有 117 份 Markdown、24 个非缓存 Python 文件，但自动化测试文件极少。数量不小，主要缺口是专题深度、组合项目和可验收性，而不是基础资料数量。

### 总体判断

- 已形成强覆盖：模型调用、结构化输出、基础 RAG、FastAPI API、Tool Calling、固定 Workflow、基础向量库、混合检索、来源引用、权限过滤、Docker 入门。
- 已形成基础覆盖：LCEL、LangGraph State/Node/Edge/Conditional Edge/Loop、角色型 Multi-Agent、RAG 本地评估、React 客户端。
- 明显不足：Runnable 组合模式、高级 RAG 标准模式、LangGraph Checkpoint/Memory/HITL/Subgraph/Streaming、真实 Multi-Agent 图编排、Tracing、系统化测试、CI/CD。
- 完全缺失：MCP Client/Server/Remote/Multi-MCP、Deep Research 主线项目。
- 业务作品集缺口：日本 SES 营业 Agent、面试 Agent、MCP Office Agent、企业客服 Agent、Coding/GitHub Agent 尚未形成完整项目。

## 三、2026 目标覆盖矩阵

### 1. 基础 LLM、LangChain 与服务化

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| Python 面向 LLM 开发 | A | `ai-learn/llm-lab/00-Python学习范围（面向LLM应用开发）.md`、`ai-learn/llm-lab/examples/` | 可增加阶段练习答案与单元测试 |
| 模型调用与供应商切换 | A | `ai-learn/llm-lab/02-模型调用基础.md`、`chat_cli`、`API配置与兼容策略.md` | 缺统一 timeout/retry/rate-limit 示例 |
| 结构化输出与 Pydantic | A | `ai-learn/llm-lab/03-结构化输出.md`、`structured_output_demo` | 缺复杂嵌套 schema 和失败自动修复 |
| Prompt / Message | B | LangChain 笔记、`langchain_chain_demo` | 缺独立 Prompt 测试、版本和注入防护练习 |
| LCEL 基础 | B | `langchain_chain_demo` 的 `prompt | llm | parser` | 缺 Parallel、Branch、Passthrough、batch、stream |
| Tool Calling | A | `ai-learn/agent-lab/03-Tool Calling.md`、`tool_agent_demo` | 可补并行调用、审批与幂等性 |
| FastAPI 服务化 | A | `ai-learn/llm-lab/05-FastAPI与企业集成.md`、`rag_api_demo` | 缺统一 SSE 流式接口模板 |
| React / Java 接入 | B | `rag_api_demo/react-client`、`spring-client`、`chat_ui_demo` | 缺与高级 Agent 的流式联调 |

### 2. RAG 2.0 与企业知识库

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| 基础文档 RAG | A | `ai-learn/llm-lab/04-RAG.md`、`doc_qa_agent` | 已足够作为入门 |
| 向量库与 metadata | A | `vector_db_demo`、Qdrant/Chroma demo | 缺统一选型与迁移练习 |
| Query Rewrite / Multi Query | B | `advanced_rag_pipeline_demo` 有本地 query variants | 不是框架 Retriever，也缺召回对比实验 |
| Rerank | B | `advanced_rag_pipeline_demo` 有规则重排 | 缺真实 cross-encoder/reranker 接入 |
| Hybrid Search | A | `internal_hybrid_rag_demo` | 当前是教学型本地实现，可再接真实检索后端 |
| 来源引用与权限过滤 | A | `internal_hybrid_rag_demo` | 缺租户隔离和越权测试 |
| Parent Document Retriever | E | 无 | 缺文档和示例 |
| Contextual Compression | E | 无 | 缺文档和示例 |
| HyDE | E | 无 | 缺文档和示例 |
| Self-RAG / Corrective RAG | E | 无 | 缺路由图、检索判断和回退示例 |
| GraphRAG | E | 无 | 可列为选修，不应先于核心能力 |
| RAG 评估 | B | `ai-learn/llm-lab/06-评估与运维.md`、`rag_eval_demo` | 缺数据集规范、检索指标和 CI 回归门槛 |

### 3. LangGraph 与 Multi-Agent

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| State / Node / Edge | A | `frameworks/langgraph/README.md`、`langgraph_workflow_demo` | 已适合作为入门 |
| Conditional Edge / Loop | A | `langgraph_workflow_demo` | 缺最大步数和异常分支示例 |
| Reducer / MessagesState | E | 无明确专题 | 缺状态合并与消息状态示例 |
| ToolNode | E | 无 | 缺 LangGraph 工具节点示例 |
| Checkpoint / Thread | E | 无 | 缺 SQLite/Postgres 持久化示例 |
| 短期/长期 Memory | E | 无 | 缺与 checkpoint、store 的边界说明 |
| Human In The Loop | E | 无 | 缺 interrupt、审批和恢复运行示例 |
| Subgraph | E | 无 | 缺模块化子图示例 |
| Streaming | E | 无 LangGraph 前后端闭环 | 缺 graph stream → SSE → React 展示 |
| Time Travel / Replay | E | 无 | P2 选修 |
| Multi-Agent 角色认知 | B | `multi_agent_team_demo` | 当前是纯 Python 顺序调用，不是真实 Agent 编排 |
| Supervisor / Handoff | C | `multi-agent/README.md` 有概念 | 缺 LangGraph supervisor/handoff 示例 |
| 失败恢复、预算与终止 | C | 文档中有提示 | 缺可执行 guardrail 和测试 |

### 4. MCP、Deep Research 与业务项目

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| MCP 概念与安全边界 | E | 无 | 需新建专题入口 |
| MCP Server / FastMCP | E | 无 | 需最小 stdio server |
| MCP Client | E | 无 | 需工具发现、调用与错误处理 |
| Remote MCP | E | 无 | 需远程 transport、认证、超时说明 |
| Multi-MCP Router | E | 无 | 需多 server 路由与冲突处理 |
| LangGraph + MCP | E | 无 | 需组合项目 |
| Deep Research | E | 无 | 需规划、搜索、证据、写作、审校闭环 |
| 企业知识库 Agent | B | 多个 RAG demo 可组合 | 缺统一 API、评估、观测和部署成品 |
| 日本 SES 营业 Agent | E | 只有岗位/业务背景文档 | 缺需求、数据模型、匹配算法和 UI/API |
| 面试准备 Agent | E | 只有作品集和面试准备文档 | 缺可运行项目 |
| MCP Office Agent | E | 无 | 应在 MCP 基础完成后实施 |
| 企业客服 Agent | E | 无完整项目 | 可复用 RAG 与 HITL，但尚未组合 |

### 5. 工程化与交付

| 2026 目标 | 等级 | 当前证据 | 主要缺口 |
| --- | --- | --- | --- |
| Docker / 健康检查 | A | `deployment/container_demo`、`rag_api_demo` | 可补 Compose 多服务 |
| 测试与 smoke check | B | `rag_api_demo/mock_test.py`、脚本与测试观点 | 缺统一 pytest、fixture、覆盖率和回归规范 |
| 日志 / Tracing / 可观测 | C | 多份文档有说明 | 缺实际 trace、结构化日志和指标示例 |
| 安全 / 权限 | B | 工具 workdir 边界、RAG ACL | 缺 prompt injection、密钥、审计和租户测试 |
| 成本 / 限流 / 重试 | C | 文档覆盖 | 缺统一中间件和可运行示例 |
| CI/CD | C | 部署文档提到 | 缺实际 workflow 和质量门禁模板 |
| 交付清单 | A | `开发测试部署流程.md`、`交付前检查清单.md` | 应转成每个项目共用模板 |

## 四、补齐内容的目录归位原则

1. `ai-learn/llm-lab/` 只补单一基础能力，不放复杂 Agent 项目。
2. `ai-learn/agent-lab/` 只补 Agent 基础、通用执行约束和服务化过渡示例。
3. `ai-learn/agent-advanced/` 承接全部 2026 高级专题和作品集项目。
4. 新专题统一采用“README → 最小 demo → 练习任务 → 测试 → 验收标准”的结构。
5. 优先扩展现有目录，不复制三个排除仓库的章节或代码。
6. 默认提供离线/mock 路径；涉及真实协议或数据库时，同时保留真实运行路径。

## 五、建议新增目录与文件

```text
ai-learn/llm-lab/
├── 11-可靠模型调用与Prompt安全.md
└── examples/
    ├── retry_timeout_example.py
    └── structured_output_repair_example.py

ai-learn/agent-lab/
├── 07-Agent执行安全与可靠性.md
└── projects/
    └── streaming_agent_api_demo/
        ├── README.md
        ├── main.py
        ├── test_main.py
        └── requirements.txt

ai-learn/agent-advanced/
├── langgraph-enterprise/
│   ├── README.md
│   ├── 01-state-reducer-messages.md
│   ├── 02-toolnode-routing.md
│   ├── 03-checkpoint-memory.md
│   ├── 04-human-in-the-loop.md
│   ├── 05-subgraph-streaming.md
│   └── demos/
│       ├── checkpoint_memory_demo/
│       ├── hitl_approval_demo/
│       └── streaming_subgraph_demo/
├── mcp/
│   ├── README.md
│   ├── 01-协议与安全边界.md
│   ├── server_fastmcp_demo/
│   ├── client_stdio_demo/
│   ├── remote_mcp_demo/
│   └── multi_mcp_router_demo/
├── rag/advanced-patterns/
│   ├── README.md
│   ├── parent_document_demo/
│   ├── contextual_compression_demo/
│   ├── hyde_demo/
│   └── corrective_rag_graph_demo/
├── deep-research/
│   ├── README.md
│   ├── 需求与评估标准.md
│   └── deep_research_demo/
├── observability/
│   ├── README.md
│   └── tracing_cost_demo/
├── platform-template/
│   ├── README.md
│   ├── tests/
│   ├── docker-compose.yml
│   └── .github/workflows/ci.yml
└── business-agents/
    ├── README.md
    ├── enterprise_knowledge_agent/
    ├── japan_ses_matching_agent/
    ├── interview_coach_agent/
    └── mcp_office_agent/
```

`GraphRAG`、Time Travel、企业客服和 Coding Agent 暂不抢占第一批目录；先完成可复用底座，再以项目形式增加。

## 六、实施优先级

### P0：补齐主线断层

| 顺序 | 新增内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 1 | 2026 主路线索引 | `2026/README.md` | 只指向三条主学习线和本报告，阶段、产物、验收一致 |
| 2 | LangGraph 企业基础 | `ai-learn/agent-advanced/langgraph-enterprise/` | checkpoint 可恢复；HITL 可中断/批准/继续；有测试 |
| 3 | MCP 基础闭环 | `ai-learn/agent-advanced/mcp/` | client 可发现并调用 server 工具；非法参数有明确错误 |
| 4 | LangGraph + MCP 组合示例 | `ai-learn/agent-advanced/mcp/langgraph_mcp_agent_demo/` | 图节点可调用 MCP；有超时、失败分支与调用日志 |
| 5 | 测试模板 | `ai-learn/agent-advanced/platform-template/` | `pytest` 一条命令通过；覆盖正常、异常、权限路径 |

### P1：补齐 2026 核心深度

| 顺序 | 新增内容 | 目标落点 | 最小验收 |
| --- | --- | --- | --- |
| 6 | 高级 RAG 模式 | `ai-learn/agent-advanced/rag/advanced-patterns/` | 每种模式有基线对比和固定评估集 |
| 7 | 流式 Agent API | `ai-learn/agent-lab/projects/streaming_agent_api_demo/` | 后端 SSE、取消/异常事件、前端消费说明完整 |
| 8 | Deep Research | `ai-learn/agent-advanced/deep-research/` | 计划、检索、去重、引用、审校闭环；限制最大步骤和预算 |
| 9 | 可观测与成本 | `ai-learn/agent-advanced/observability/` | 单次运行可查看 trace、耗时、token/成本和失败原因 |
| 10 | 企业知识库成品 | `business-agents/enterprise_knowledge_agent/` | API、权限、引用、评估、测试、Docker 全部可验收 |

### P2：形成岗位向作品集

| 顺序 | 项目 | 前置依赖 |
| --- | --- | --- |
| 11 | 日本 SES 营业 Agent | 结构化输出、RAG、LangGraph、评估 |
| 12 | 面试准备 Agent | RAG、HITL、流式 UI |
| 13 | MCP Office Agent | MCP、权限审计、HITL |
| 14 | 企业客服 Agent | 企业知识库、HITL、可观测 |
| 15 | GraphRAG / Coding Agent 选修 | 核心路线完成后再立项 |

## 七、建议的 24 周执行路线

| 周期 | 学习与建设内容 | 主要交付物 |
| --- | --- | --- |
| 第 1-3 周 | 复核 `llm-lab` 基础；补可靠调用、结构化修复 | 2 份基础示例和测试 |
| 第 4-5 周 | LCEL 组合、batch、stream、错误处理 | 扩展 `langchain_chain_demo` 或新增组合 demo |
| 第 6-8 周 | 高级 RAG 模式与评估 | 4 个小模式 demo、固定评估集、对比报告 |
| 第 9-12 周 | LangGraph checkpoint、memory、HITL、subgraph、streaming | 3 个可恢复工作流 demo |
| 第 13-15 周 | MCP Server、Client、Remote、Multi-MCP | MCP 基础闭环和安全说明 |
| 第 16-18 周 | LangGraph + MCP、真实 Multi-Agent、Deep Research | 2 个组合项目 |
| 第 19-21 周 | pytest、Tracing、成本、Docker Compose、CI | 可复用平台模板 |
| 第 22-24 周 | 企业知识库 + 一个岗位向项目 | 2 个可演示、可测试、可部署作品集 |

## 八、统一交付标准

以后新增的每份示例至少满足：

- `README.md`：目标、前置知识、架构、运行命令、输入输出、限制。
- 可运行入口：默认离线/mock 可跑，真实模式的依赖和配置明确。
- `requirements.txt` 或统一依赖声明：避免隐式依赖。
- 自动化测试：至少包含 happy path、异常路径、边界/权限路径。
- 示例数据：小、固定、可重复，不能依赖排除目录。
- 观测信息：关键步骤、耗时、失败原因可见；高级项目补 token/成本。
- 安全边界：目录访问、工具权限、密钥、远程调用和审批点明确。
- 验收标准：不能只写“运行成功”，需定义结果质量和失败行为。

业务作品集还应增加：

- `需求概要.md`
- `基本设计.md`
- `测试观点.md`
- `简单测试用例表.md`
- 架构/数据流图
- Docker 与一键启动方式
- 简历说明和面试讲解要点

## 九、推荐先执行的最小批次

第一批不要同时铺开全部目录。建议只实施以下 5 项：

1. 新增 `2026/README.md`，确定唯一主路线。
2. 新增 `ai-learn/agent-advanced/langgraph-enterprise/README.md` 和 `checkpoint_memory_demo/`。
3. 新增 `ai-learn/agent-advanced/langgraph-enterprise/hitl_approval_demo/`。
4. 新增 `ai-learn/agent-advanced/mcp/README.md`、最小 server 和 client。
5. 建立统一 `pytest` 项目模板，并把上述三个 demo 纳入测试。

完成后再进入高级 RAG、Deep Research 和业务 Agent。这样能够先打通 2026 路线最大的两个结构性断点：LangGraph 企业能力和 MCP，同时避免再次形成只有目录与说明、没有可验收代码的资料堆积。

## 十、最终目录职责

```text
2026/          目标、阶段计划、覆盖盘点、验收总纲
ai-learn/llm-lab/       LLM 应用基础和单能力练习
ai-learn/agent-lab/     基础 Agent、工具、工作流和服务化过渡
ai-learn/agent-advanced/高级框架、协议、组合系统、工程模板和作品集
```

本规划的所有新增文档和示例都限定在上述四个目录内；三个排除目录继续保持独立，不作为主学习路线依赖。

## 十一、实施更新（2026-06-21）

本规划的第一轮补齐已经实施。Runnable、LangGraph 企业能力、MCP 全链路和真实 Multi-Agent 图编排达到教学闭环；高级 RAG、Tracing、Deep Research 与五个业务作品集达到可演示 MVP。统一测试和 CI/CD 按本轮范围延后。

逐项完成等级、实现位置与剩余差距见 [2026补齐实施状态.md](./2026补齐实施状态.md)。该状态表是后续更新完成标记的唯一入口，避免规划正文与实际代码再次失同步。
