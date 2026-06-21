# Agent 进阶扩展计划

> 归位说明：Agent 的主学习路线统一看 [01-学习路线.md](./01-学习路线.md)。本文不再重复“模型调用 -> RAG -> API -> Tool Calling -> Workflow”的基础路线，只记录主线完成后的进阶扩展方向。

## 1. 这个文档是什么

这份文档是 `agent-lab` 的进阶计划，不是入门路线。

如果你还在学习下面这些内容：

- 模型调用
- 结构化输出
- RAG
- FastAPI
- Tool Calling
- Agent Workflow

请先看：

- [01-学习路线.md](./01-学习路线.md)
- [Agent系统框架与术语.md](./Agent系统框架与术语.md)

本文只回答一个问题：

```text
基础 demo 都跑通之后，下一步怎样把 Agent 做得更接近真实项目？
```

## 2. 和其他文档的分工

| 文档 | 负责什么 |
| --- | --- |
| [../llm-lab/README.md](../llm-lab/README.md) | LLM 应用主线：模型调用、结构化输出、RAG、FastAPI、评估 |
| [01-学习路线.md](./01-学习路线.md) | Agent 入门主线：场景、demo、每阶段学习顺序 |
| [Agent系统框架与术语.md](./Agent系统框架与术语.md) | Agent 系统知识、角色、术语 |
| 本文 | 主线完成后的进阶扩展计划 |

## 3. 进入本文前应具备什么

进入本文前，建议你已经能做到：

| 能力 | 对应 demo |
| --- | --- |
| 会调模型 | `projects/chat_cli` |
| 会让模型输出结构化 JSON | `projects/structured_output_demo` |
| 会做本地文档问答 | `projects/doc_qa_agent` |
| 会把 RAG 做成 API | `projects/rag_api_demo` |
| 会让模型调用只读工具 | `projects/tool_agent_demo` |
| 会做三阶段工作流 | `projects/workflow_agent` |

如果这些还没跑通，先不要急着看多 Agent、复杂框架或自动执行。

## 4. 进阶方向 1：把 RAG 工具化

### 是什么

把 RAG 从“用户问，系统答”改成“Agent 可以按需调用的知识工具”。

```text
Agent 判断需要资料
  -> 调用 search_docs(query)
  -> 得到 chunk + source
  -> 根据资料继续回答或计划下一步
```

### 对应文件

| 文件 | 学什么 |
| --- | --- |
| [04-RAG.md](./04-RAG.md) | Agent 中的 RAG 定位 |
| [03-Tool Calling.md](./03-Tool%20Calling.md) | 怎么把能力包装成工具 |
| [projects/doc_qa_agent/main.py](./projects/doc_qa_agent/main.py) | `retrieve()` 和 `build_context()` |
| [projects/tool_agent_demo/main.py](./projects/tool_agent_demo/main.py) | `build_tools()` 和 `call_tool()` |

### 完成标志

- 能设计 `search_docs(query, top_k)` 工具。
- 工具返回结果里包含 `content` 和 `source`。
- Agent 没查到资料时不会硬答。

## 5. 进阶方向 2：增加工具安全边界

### 是什么

真实 Agent 不能想做什么就做什么，必须限制权限和范围。

当前 `tool_agent_demo` 已经用 `resolve_path()` 限制只能访问 `workdir`。

下一步可以扩展：

| 安全边界 | 说明 |
| --- | --- |
| 文件范围 | 只能读指定目录 |
| 工具白名单 | 只能调用允许的工具 |
| 写操作确认 | 写文件、执行 SQL 前需要人工确认 |
| 输出审查 | 最终回答必须带来源或说明资料不足 |

### 对应文件

- [projects/tool_agent_demo/main.py](./projects/tool_agent_demo/main.py)
- [projects/tool_agent_demo/测试观点.md](./projects/tool_agent_demo/测试观点.md)

## 6. 进阶方向 3：从固定工作流到半自动 Agent

### 是什么

当前 `workflow_agent` 是固定流程：

```text
分析 -> 计划 -> 总结
```

进阶后可以让 Agent 在某些步骤中做判断：

```text
分析任务
  -> 判断是否需要查资料
  -> 如果需要，调用 RAG 工具
  -> 判断是否需要再查一次
  -> 生成最终建议
```

### 对应文件

| 文件 | 学什么 |
| --- | --- |
| [05-Agent工作流.md](./05-Agent工作流.md) | Workflow 和 Agent 的区别 |
| [projects/workflow_agent/main.py](./projects/workflow_agent/main.py) | 三阶段流程和状态传递 |
| [projects/tool_agent_demo/main.py](./projects/tool_agent_demo/main.py) | 工具调用循环 |

### 完成标志

- 能解释什么时候用固定 workflow。
- 能解释什么时候需要 Agent 自己判断下一步。
- 能为循环设置最大轮次和终止条件。

## 7. 进阶方向 4：增加评估和日志

### 是什么

Agent 能跑不等于能交付。进阶阶段要能复盘每一步：

- 用户输入是什么
- Agent 为什么调用某个工具
- 工具返回了什么
- 最终回答是否基于真实结果
- 失败时原因是什么

### 可以记录的日志

| 日志项 | 作用 |
| --- | --- |
| `task_id` | 追踪一次任务 |
| `tool_name` | 看调用了哪个工具 |
| `tool_args` | 检查参数是否合理 |
| `tool_result_summary` | 记录工具返回概要 |
| `final_answer` | 记录最终输出 |
| `error` | 记录失败原因 |

### 对应资料

- [../llm-lab/06-评估与运维.md](../llm-lab/06-评估与运维.md)
- [projects/tool_agent_demo/测试观点.md](./projects/tool_agent_demo/测试观点.md)
- [projects/rag_api_demo/试验结果报告.md](./projects/rag_api_demo/试验结果报告.md)

## 8. 进阶方向 5：多 Agent 只作为后段专题

### 是什么

多 Agent 是把不同职责分给多个 Agent，例如：

```text
Planner Agent -> Research Agent -> Reviewer Agent
```

但初学阶段不要过早做多 Agent，因为很容易出现：

- 多个 Agent 重复工作
- 上下文越来越乱
- 成本失控
- 不知道错误发生在哪个 Agent

### 什么时候再考虑

只有满足这些条件后再考虑：

- 单 Agent 工作流已经稳定。
- 工具调用有边界。
- 日志能复盘。
- 任务确实需要不同角色分工。

## 9. 日本现场表达

| 中文 | 日本語 | 现场表达 |
| --- | --- | --- |
| 工具型 Agent | ツール利用 Agent | 外部ツールを利用する Agent を作成します |
| RAG 工具 | RAG ツール | Agent から社内検索ツールを呼び出します |
| 半自动 Agent | 半自動 Agent | 最終実行前に人手確認を入れます |
| 工作流化 | ワークフロー化 | 処理を段階化して制御します |
| 安全边界 | 安全制御 / ガードレール | 権限外アクセスや危険操作を防ぎます |
| 执行日志 | 実行ログ | Agent の判断とツール実行結果を記録します |

## 10. 推荐进阶顺序

1. 把 `doc_qa_agent` 的检索逻辑包装成工具。
2. 把这个工具接进 `tool_agent_demo`。
3. 给工具结果增加 source 和 score。
4. 给 Agent 增加“资料不足时不回答”的规则。
5. 给每次工具调用记录日志。
6. 把 `workflow_agent` 改成“先分析，再决定是否调用 RAG 工具”。
7. 最后再考虑多 Agent 或复杂框架。

## 11. 最重要的判断

进阶 Agent 不是追求“自动化程度最高”，而是追求：

- 能查到真实资料
- 能说明依据
- 能限制权限
- 能复盘过程
- 能让人确认高风险动作

这比一开始做复杂多 Agent 更贴近日本现场的开发和交付。
