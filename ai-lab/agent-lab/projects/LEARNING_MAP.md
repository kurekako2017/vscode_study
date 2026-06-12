# Agent Lab 示例总导航（按章节学习）

这是一页式学习导航。
目标是让你按章节直接进入每个示例，快速完成：

1. 运行
2. 观察输入输出
3. 做最小改造练习

建议顺序：先 CLI 基础，再结构化输出，再工作流，再工具调用，再 RAG。

---

## 第 1 章：chat_cli（最小对话闭环）

- 路径：`chat_cli/main.py`
- 学习目标：参数解析、模式切换、输出格式化
- 补充代码例子：`chat_cli/README_LEARN.md`、`chat_cli/STAGE2_MAX_CHARS_GUIDE.md`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/chat_cli
python3 main.py "给我一个三步学习计划"
python3 main.py --mock "给我一个三步学习计划"
python3 main.py --mock --max-chars 120 "请详细解释 agent 和 workflow 的区别"
```

### 输入输出

- 输入：prompt、`--mock/--real`、`--max-chars`
- 输出：模型或 mock 回答，支持字符截断

### 练习任务

1. 增加 `--max-lines` 参数，限制输出行数。
2. 把 mock 响应拆成多个模板，通过参数切换。
3. 把模式决策逻辑抽成独立策略类。

---

## 第 2 章：structured_output_demo（结构化输出）

- 路径：`structured_output_demo/main.py`
- 学习目标：用 Pydantic 约束模型输出，减少解析不稳定
- 补充代码例子：`structured_output_demo/README_LEARN.md`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/structured_output_demo
python3 main.py "做一个客服 Agent 的开发计划"
python3 main.py "给我一个 RAG 学习路线" --model gpt-4o
```

### 输入输出

- 输入：自然语言需求
- 输出：通过 schema 校验后的 JSON（`AgentPlan`）

### 练习任务

1. 在 `AgentPlan` 中新增 `timeline` 字段。
2. 增加结果落盘参数，例如 `--save plan.json`。
3. 为字段增加最小长度或枚举校验。

---

## 第 3 章：workflow_agent（三阶段工作流）

- 路径：`workflow_agent/main.py`
- 学习目标：把复杂任务拆成分析、计划、总结三阶段
- 补充代码例子：`workflow_agent/README_LEARN.md`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/workflow_agent
python3 main.py "我要做一个面向日本现场的需求整理 Agent"
python3 main.py "帮我规划 4 周的 LLM 学习与作品集计划"
```

### 输入输出

- 输入：一个完整任务描述
- 输出：analysis、结构化 plan、final summary 三段结果

### 练习任务

1. 给 plan 新增 `effort_estimate` 字段。
2. 打印每个阶段耗时。
3. 增加参数支持跳过总结阶段。

---

## 第 4 章：tool_agent_demo（工具调用闭环）

- 路径：`tool_agent_demo/main.py`
- 学习目标：模型决策调用本地工具，再基于证据回答
- 补充代码例子：`tool_agent_demo/README_LEARN.md`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/tool_agent_demo
python3 main.py "请概览当前目录结构" --workdir .
python3 main.py "请搜索 README 里的 RAG 关键词并总结" --workdir .
```

### 输入输出

- 输入：任务文本 + 可访问目录 `--workdir`
- 输出：模型最终回答（中间隐式执行工具循环）

### 练习任务

1. 新增 `write_file` 工具并加路径白名单。
2. 给搜索工具增加文件类型过滤参数。
3. 记录每轮工具调用日志到本地文件。

---

## 第 5 章：doc_qa_agent（本地文档问答 RAG）

- 路径：`doc_qa_agent/main.py`
- 学习目标：文档切分、关键词检索、基于上下文回答
- 补充代码例子：`doc_qa_agent/README_LEARN.md`、`doc_qa_agent/简单测试用例表.md`、`doc_qa_agent/测试观点.md`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/doc_qa_agent
python3 main.py "请总结这个目录中的 RAG 思路" --docs .
python3 main.py "哪些文件提到了 tool calling" --docs ../../..
```

### 输入输出

- 输入：question、`--docs`、`--model`
- 输出：答案 + 来源 chunk 列表（含分数）

### 练习任务

1. 增加 `--top-k` 参数，覆盖默认检索数量。
2. 在答案后追加每个来源的摘要行。
3. 把关键词检索替换为向量检索（后续章节可做）。

---

## 第 6 章：rag_api_demo（FastAPI 版 RAG 服务）

- 路径：`rag_api_demo/main.py`
- 学习目标：把 RAG 能力封装成 API 服务（health/reload/ask）
- 补充代码例子：`rag_api_demo/README_LEARN.md`、`rag_api_demo/mock_test.py`、`rag_api_demo/run_demo.sh`、`rag_api_demo/run-dev.sh`、`rag_api_demo/smoke_check.sh`、`rag_api_demo/smoke_local.sh`

### 快速运行

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

服务启动后，再在另一个终端执行：

```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档重点"}'
```

### 输入输出

- 输入：HTTP JSON 请求 + 本地文档目录
- 输出：结构化 JSON（answer、sources、source_count）

### 练习任务

1. 给 `/ask` 增加可选 `top_k` 参数。
2. 增加 `/config` 接口返回当前 chunk 配置。
3. 把文档加载封装到独立服务类，便于测试。

---

## 每章通用学习法（建议）

1. 先跑通最小命令，确认环境与依赖。
2. 只改一个点，观察输入输出变化。
3. 每章至少做一个参数扩展练习。
4. 改完后再回归运行，确保行为与预期一致。

按这个节奏走完 6 章，你会形成可迁移的 Agent 工程骨架能力。

---

## 每章代码例子总表

如果你是想“直接找代码看”，可以先从下面这些文件开始：

| 章节 | 主入口 | 适合一起看的代码例子 |
|---|---|---|
| `chat_cli` | `chat_cli/main.py` | `chat_cli/README_LEARN.md`、`chat_cli/STAGE2_MAX_CHARS_GUIDE.md` |
| `structured_output_demo` | `structured_output_demo/main.py` | `structured_output_demo/README_LEARN.md` |
| `workflow_agent` | `workflow_agent/main.py` | `workflow_agent/README_LEARN.md` |
| `tool_agent_demo` | `tool_agent_demo/main.py` | `tool_agent_demo/README_LEARN.md` |
| `doc_qa_agent` | `doc_qa_agent/main.py` | `doc_qa_agent/README_LEARN.md`、`doc_qa_agent/简单测试用例表.md`、`doc_qa_agent/测试观点.md` |
| `rag_api_demo` | `rag_api_demo/main.py` | `rag_api_demo/README_LEARN.md`、`rag_api_demo/mock_test.py`、`rag_api_demo/smoke_check.sh`、`rag_api_demo/smoke_local.sh`、`rag_api_demo/run_demo.sh`、`rag_api_demo/run-dev.sh` |
