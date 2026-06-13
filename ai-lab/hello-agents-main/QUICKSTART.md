# Hello-Agents 运行总览

这份文档整理了 `hello-agents-main` 里当前能确认入口的可运行代码，并统一成一套尽量一致的环境搭建方式。

如果你之前遇到 `command not found`，优先检查两点：

1. 是否已经激活虚拟环境。
2. 是否用 `python -m pip` / `python -m uvicorn` 这种模块方式，而不是直接依赖全局命令。

## 统一前置环境

- Python 3.10+
- Node.js 18+
- Git
- Godot 4.2+，仅 `code/chapter15/Helloagents-AI-Town` 需要

推荐每个后端项目单独建虚拟环境，不要把不同章节的依赖混在一个环境里。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Windows PowerShell 可改成：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -U pip
```

## 统一环境变量思路

多数项目都围绕这几类变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `DASHSCOPE_API_KEY`
- `AMAP_API_KEY`
- `VITE_API_BASE_URL`

如果项目 README 中没有特别说明，优先按项目自身的 `.env.example` 来填。

## 学习与运行 对照

下面按“示例名称 + 核心功能 + 启动方式”整理，方便你先理解每个例子在演示什么，再决定要跑哪个。

### 1. `code/chapter9`

先读：

- [`code/chapter9/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter9/README.md)
- [`code/chapter9/05_terminal_tool_examples.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter9/05_terminal_tool_examples.py)

用途：第九章上下文工程示例集合，重点演示 ContextBuilder、NoteTool、TerminalTool 和 MemoryTool 如何协同，完成长任务上下文管理、笔记沉淀、终端分析和跨会话记忆。

包含的主要示例：

- `01_context_builder_basic.py`：演示 ContextBuilder 的基本用法、上下文包创建、优先级和 token 控制。
- `02_context_builder_with_agent.py`：演示 ContextBuilder 如何接入智能体，对话历史如何进入上下文管理流程。
- `03_note_tool_operations.py`：演示 NoteTool 的创建、查询、更新、删除、搜索和标签管理。
- `04_note_tool_integration.py`：演示 NoteTool 与 ContextBuilder 联动，用笔记支撑长期任务追踪。
- `05_terminal_tool_examples.py`：演示 TerminalTool 的目录浏览、数据文件查看、日志分析、代码库分析和安全限制。
- `06_three_day_workflow.py`：演示跨三天、跨会话的完整工作流，适合看长周期任务如何持续推进。
- `codebase_maintainer.py`：核心维护助手，把上下文、笔记、终端和记忆组合成一个代码库维护 Agent。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter9
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=''
python 05_terminal_tool_examples.py
```

### 2. `code/chapter10/weather-mcp-server`

先读：

- [`code/chapter10/weather-mcp-server/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter10/weather-mcp-server/README.md)
- [`code/chapter10/weather-mcp-server/server.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter10/weather-mcp-server/server.py)

用途：天气 MCP Server 示例，提供真实天气查询能力，支持 12 个中国主要城市，也支持英文城市名查询全球城市，并暴露标准 MCP 工具接口供客户端接入。

包含的主要能力：

- `get_weather`：查询指定城市的当前天气。
- `list_supported_cities`：列出支持的中文城市。
- `get_server_info`：返回服务器名称、版本和工具列表。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter10/weather-mcp-server
python server.py
```

### 3. `code/chapter6/AutoGenDemo`

先读：

- [`code/chapter6/AutoGenDemo/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AutoGenDemo/README.md)
- [`code/chapter6/AutoGenDemo/autogen_software_team.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AutoGenDemo/autogen_software_team.py)

用途：AutoGen 软件开发团队协作示例，演示产品经理、工程师、代码审查员和用户代理如何围绕一个需求，自动完成需求分析、代码实现、代码审查和测试反馈闭环。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter6/AutoGenDemo
python autogen_software_team.py
```

### 4. `code/chapter6/AgentScopeDemo`

先读：

- [`code/chapter6/AgentScopeDemo/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AgentScopeDemo/README.md)
- [`code/chapter6/AgentScopeDemo/main_cn.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AgentScopeDemo/main_cn.py)

用途：AgentScope 三国狼人杀示例，演示消息驱动架构、并发协作、角色扮演和结构化输出约束，适合观察多智能体游戏流程如何设计。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter6/AgentScopeDemo
export DASHSCOPE_API_KEY='你的_dashscope_key'
python main_cn.py
```

### 5. `code/chapter6/CAMEL`

先读：

- [`code/chapter6/CAMEL/DigitalBookWriting.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/CAMEL/DigitalBookWriting.py)

用途：CAMEL 双角色电子书写作示例，模拟“作家 + 心理学家”围绕拖延症心理学主题协作创作电子书，展示角色对话驱动的内容生成流程。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter6/CAMEL
python DigitalBookWriting.py
```

### 6. `code/chapter6/Langgraph`

先读：

- [`code/chapter6/Langgraph/Dialogue_System.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/Langgraph/Dialogue_System.py)
- [`code/chapter6/Langgraph/requirements.txt`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/Langgraph/requirements.txt)

用途：LangGraph + Tavily 搜索助手示例，演示如何把“理解问题 -> 搜索信息 -> 综合回答”组织成一个可复用的工作流，并带上会话记忆。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter6/Langgraph
python Dialogue_System.py
```

### 7. `code/chapter12`

先读：

- [`code/chapter12/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter12/README.md)
- [`code/chapter12/01_basic_agent_example.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter12/01_basic_agent_example.py)

用途：智能体评估示例集合，覆盖基础 ReAct 智能体、BFCL 评估、GAIA 评估以及数据生成质量评估，适合学习“如何衡量智能体能力”。

包含的主要示例：

- `01_basic_agent_example.py`：基础智能体示例，说明为什么需要做评估。
- `02_bfcl_quick_start.py`：BFCL 一键快速评估。
- `03_bfcl_custom_evaluation.py`：BFCL 自定义评估，展示底层组件的拼装方式。
- `04_run_bfcl_evaluation.py`：BFCL 评估最佳实践与对比分析。
- `05_gaia_quick_start.py`：GAIA 一键快速评估。
- `06_gaia_best_practices.py`：GAIA 评估最佳实践与结果解读。
- `07_data_generation_complete_flow.py`：AIME 题目生成的完整评估流程。
- `08_data_generation_llm_judge.py`：使用 LLM Judge 评估生成题目质量。
- `09_data_generation_win_rate.py`：使用 Win Rate 指标比较生成结果。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter12
python 01_basic_agent_example.py
python 02_bfcl_quick_start.py
```

### 8. `code/chapter13/helloagents-trip-planner`

先读：

- [`code/chapter13/helloagents-trip-planner/README.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter13/helloagents-trip-planner/README.md)
- [`code/chapter13/helloagents-trip-planner/backend/app/api/main.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter13/helloagents-trip-planner/backend/app/api/main.py)

用途：智能旅行助手示例，后端用 FastAPI 提供规划能力，前端用 Vue 展示结果，核心是让 Agent 自动调用高德地图 MCP 工具生成多日旅行计划。

主要功能：

- 景点搜索与 POI 发现
- 路线规划，支持步行、驾车和公共交通
- 天气查询，辅助安排每日行程
- 餐饮、住宿和时间分配建议

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter13/helloagents-trip-planner/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 9. `code/chapter14/helloagents-deepresearch`

先读：

- [`code/chapter14/helloagents-deepresearch/backend/src/main.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter14/helloagents-deepresearch/backend/src/main.py)
- [`code/chapter14/helloagents-deepresearch/backend/src/config.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter14/helloagents-deepresearch/backend/src/config.py)

用途：自动化深度研究智能体示例，后端提供研究接口，前端提供交互界面，重点演示多轮搜索、任务拆解、笔记记录和流式报告输出。

主要功能：

- 接收研究主题并自动拆解子任务
- 调用搜索引擎收集资料
- 将过程中间结论写入笔记
- 输出 Markdown 格式的研究报告
- 支持流式返回，便于前端实时展示进度

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter14/helloagents-deepresearch/backend
python src/main.py
```

### 10. `code/chapter15/Helloagents-AI-Town`

先读：

- [`code/chapter15/Helloagents-AI-Town/SETUP_GUIDE.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter15/Helloagents-AI-Town/SETUP_GUIDE.md)
- [`code/chapter15/Helloagents-AI-Town/backend/main.py`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter15/Helloagents-AI-Town/backend/main.py)

用途：赛博小镇示例，使用 Godot 客户端和 FastAPI 后端构建 AI NPC 对话系统，演示 NPC 记忆、好感度、批量状态刷新和实时交互。

主要功能：

- 玩家与单个 NPC 的实时对话
- NPC 批量自主对话生成，降低 API 调用成本
- 短期和长期记忆管理
- 好感度系统和 NPC 状态管理
- Godot 游戏内交互与日志查看

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd code/chapter15/Helloagents-AI-Town/backend
python main.py
```

### 11. `Co-creation-projects/`

先读：

- [`Co-creation-projects/QUICKSTART.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/QUICKSTART.md)
- [`Co-creation-projects/RUNBOOK_SHORT.md`](/home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/RUNBOOK_SHORT.md)

用途：共创项目集合，这里是大量独立的 Agent 应用案例入口。每个项目都对应一个具体业务场景，通常会包含自己的 README、依赖和启动方式。

可直接运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main
source .venv/bin/activate
cd Co-creation-projects/angelen-SoftwareDevHelper
python -m pip install -r requirements.txt
cp .env.example .env
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m uvicorn src.main:app --reload
```

## 已确认可运行的代码

### 第 6 章

#### `code/chapter6/AutoGenDemo`

用途：AutoGen 多智能体协作示例。

安装与运行：

```bash
cd code/chapter6/AutoGenDemo
python -m pip install -r requirements.txt
python autogen_software_team.py
```

如果目录里只有 `.env copy` 这种示例文件，请手动另存为 `.env`。

另一个可独立运行的示例：

```bash
streamlit run output.py
```

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`

#### `code/chapter6/AgentScopeDemo`

用途：AgentScope 三国狼人杀。

安装与运行：

```bash
cd code/chapter6/AgentScopeDemo
python -m pip install -r requirements.txt
python main_cn.py
```

需要变量：

- `DASHSCOPE_API_KEY`

#### `code/chapter6/Langgraph`

用途：LangGraph + Tavily 搜索助手。

安装与运行：

```bash
cd code/chapter6/Langgraph
python -m pip install -r requirements.txt
python Dialogue_System.py
```

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`
- `TAVILY_API_KEY`

#### `code/chapter6/CAMEL`

用途：CAMEL 双角色电子书写作示例。

安装与运行：

```bash
cd code/chapter6/CAMEL
python -m pip install -r requirements.txt
python DigitalBookWriting.py
```

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`

### 第 9 章

#### `code/chapter9`

用途：上下文工程示例集合。

推荐先把嵌入模型切到最省事的 `tfidf`，这样不需要额外下载模型：

```bash
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=""
```

可直接运行的脚本：

```bash
cd code/chapter9
python 03_note_tool_operations.py
python 05_terminal_tool_examples.py
python 06_three_day_workflow.py
```

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`

说明：

- `05_terminal_tool_examples.py` 不依赖 LLM，也适合先验证环境。
- `project/main.py` 是最小可运行示例，只输出一段文本。

### 第 10 章

#### `code/chapter10/weather-mcp-server`

用途：天气 MCP Server。

安装与运行：

```bash
cd code/chapter10/weather-mcp-server
python -m pip install -r requirements.txt
python server.py
```

这个服务不要求 API Key，适合作为最小可用的 MCP 调试目标。

### 第 12 章

#### `code/chapter12`

用途：智能体评估示例集合。

安装：

```bash
cd code/chapter12
python -m pip install hello-agents[evaluation]==0.2.3
```

运行示例：

```bash
python 01_basic_agent_example.py
python 02_bfcl_quick_start.py
python 05_gaia_quick_start.py
python 07_data_generation_complete_flow.py 30 3.0
```

需要变量：

- `OPENAI_API_KEY`
- `HF_TOKEN`

### 第 13 章

#### `code/chapter13/helloagents-trip-planner`

用途：智能旅行助手，后端 FastAPI + 前端 Vue。

后端安装与运行：

```bash
cd code/chapter13/helloagents-trip-planner/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

前端安装与运行：

```bash
cd code/chapter13/helloagents-trip-planner/frontend
cp .env.example .env
npm install
npm run dev
```

需要变量：

- `AMAP_API_KEY`
- `LLM_API_KEY` 或 `OPENAI_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`
- `VITE_API_BASE_URL`
- `VITE_AMAP_WEB_KEY`
- `VITE_AMAP_WEB_JS_KEY`

### 第 14 章

#### `code/chapter14/helloagents-deepresearch`

用途：自动化深度研究智能体，后端 FastAPI + 前端 Vue。

后端安装与运行：

```bash
cd code/chapter14/helloagents-deepresearch/backend
python -m pip install -e .
python src/main.py
```

前端安装与运行：

```bash
cd code/chapter14/helloagents-deepresearch/frontend
npm install
npm run dev
```

需要变量：

- `SEARCH_API`
- `LLM_PROVIDER`
- `LLM_MODEL_ID`
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `TAVILY_API_KEY`
- `OPENAI_API_KEY` 或本地模型地址相关变量

### 第 15 章

#### `code/chapter15/Helloagents-AI-Town`

用途：赛博小镇，Godot 客户端 + FastAPI 后端。

后端安装与运行：

```bash
cd code/chapter15/Helloagents-AI-Town/backend
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

前端是 Godot 项目：

- 打开 `code/chapter15/Helloagents-AI-Town/helloagents-ai-town/project.godot`
- 使用 Godot 4.2+ 导入后运行 `scenes/main.tscn`

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`
- `API_HOST`
- `API_PORT`

## 运行顺序建议

如果你想先验证整个仓库的环境，按这个顺序跑最稳：

1. `code/chapter10/weather-mcp-server`
2. `code/chapter6/AutoGenDemo`
3. `code/chapter6/AgentScopeDemo`
4. `code/chapter6/Langgraph`
5. `code/chapter6/CAMEL`
6. `code/chapter9`
7. `code/chapter13/helloagents-trip-planner`
8. `code/chapter14/helloagents-deepresearch`
9. `code/chapter15/Helloagents-AI-Town`

## 共创项目区

`Co-creation-projects/` 里还有很多独立项目，大多数都能按各自 `README.md` 和 `requirements.txt` 启动。

它们的共同模式通常是：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

或者前后端分离：

```bash
python -m pip install -r backend/requirements.txt
npm install
npm run dev
```

如果你希望我继续把共创项目也整理成“可直接复制执行”的清单，我可以再按项目逐个展开。
