# 05_LangChain_LangGraph_MCP

## LangChain

LangChain は Prompt、Model、Parser、Retriever、Tool を組み合わせるためのアプリケーションフレームワークとして扱う。开发初期では `langchain_chain_demo` と `runnable_composition_demo` が対応する。

## LangGraph

LangGraph は状態、分岐、ループ、checkpoint、Human-in-the-loop が必要な場合に使う。开发初期では `langgraph_workflow_demo`、`graph_team_demo`、`japan_retail_analysis_agent` が対応する。

## MCP

MCP は Agent が利用する外部ツールや社内システムを標準化して接続するための考え方として扱う。开发初期では `mcp_office_agent` と `agent-advanced/mcp` が対応する。

## 面试说明

面接では「LangChain は処理部品の組み合わせ、LangGraph は状態を持つワークフロー、MCP は外部ツール接続の標準化」と整理して説明する。

<!-- ENTERPRISE-UPGRADE-V1 -->

---

# 小売業向け AI 経営分析システム Handbook Extension

## Design Decision

- 为什么 LangChain：适合组合 Prompt、Model、Parser、Retriever、Runnable。
- 为什么不是手写函数：链路复杂、需要 batch/stream/trace 时框架价值更高。
- 为什么 LangGraph：适合状态、分支、循环、checkpoint、人审和恢复。
- 为什么不是普通 Workflow/FSM/Airflow：普通 Workflow 缺 LLM/工具状态语义；FSM 对动态上下文不友好；Airflow 偏离线调度。
- 什么时候不建议 LangGraph：一次性问答、简单 API、无状态链路、团队还不能维护图状态时。
- 为什么 MCP：统一模型面向工具的发现、schema、调用和结果回填，但不替代业务 API。

### Alternatives

手写 service、传统 FSM、Temporal、Airflow、REST/RPC API、RPA。

### Fit / Not Fit

- 适用场景：系统开发已经证明业务价值，需要进入架构评审、面试说明或運用版设计。
- 不适用场景：临时脚本、无多人维护、无审计需求、无需长期运用的场景。

### Pros / Cons / Cost

- 优点：可解释、可 Review、可扩展。
- 缺点：比最小 demo 多设计和治理成本。
- 成本：需要维护 schema、日志、测试、评估、部署和监控。
- 维护成本：随着数据、模型、工具和组织复杂度增加，需要定期 Review。
- 扩展性：应通过分层、接口契约、状态管理和观测性扩展。

## TL Review

日本企业 TL 最可能追问：

- なぜこの設計にしましたか。
- なぜ他の方式を使わなかったのですか。
- 本格運用に向けた拡張ポイントはどこですか。
- 性能、復旧、セキュリティ、ログ、監視はどう設計しますか。
- 100 倍のデータ量、1000 TPS、外部サービス障害にどう対応しますか。

## Enterprise Practice

多步骤研究报告、审批 Agent、企业知识库 Agent、开发者平台、Office/GitHub 工具集成。

真实项目通常先明确业务范围、系统边界和 Review 观点，再由 TL 和 Architect 判断扩展路线。日本现场会要求基本设计、详细设计、レビュー票、障害票、运维和改修路线。

## Production Gap

缺 checkpoint store 选型、interrupt/resume UI、MCP auth、transport security、tool audit、model routing、cost tracing。

这些是未来扩展目标，これらは本格運用に向けて設計・拡張する項目です。

## Continue Learning

继续学习 LangGraph StateGraph、checkpoint、interrupt、Command resume、MCP official SDK、LangChain Runnable tracing。

为什么值得学：这些内容决定候选人能否从“会跑 demo”升级为“能做小売業向け AI 経営分析システム开发、能参与架构评审、能通过日本现场面试”的工程师。

## References

- 公共企业架构章节：`knowledge/00_Enterprise_AI_Architecture_Handbook.md`
- 项目案例：`projects/`
- 面试手册：`01_日本AI现场面试宝典.md`
