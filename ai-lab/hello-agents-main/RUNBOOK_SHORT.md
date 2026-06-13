# Hello-Agents 快速运行手册

这是一份更短的执行版清单，适合你按目录直接跑代码。

## 先决条件

- Python 3.10+
- Node.js 18+
- Godot 4.2+，仅第 15 章需要

统一建议：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

## 通用规则

- Python 项目优先用 `python -m pip` 安装依赖。
- 启动 FastAPI/uvicorn 时优先用 `python -m uvicorn ...`，避免 `uvicorn: command not found`。
- 前端先 `npm install`，再 `npm run dev`。
- 每个项目单独配置自己的 `.env`。

## 可运行项目

### `code/chapter10/weather-mcp-server`

```bash
cd code/chapter10/weather-mcp-server
python -m pip install -r requirements.txt
python server.py
```

### `code/chapter6/AutoGenDemo`

```bash
cd code/chapter6/AutoGenDemo
python -m pip install -r requirements.txt
python autogen_software_team.py
streamlit run output.py
```

### `code/chapter6/AgentScopeDemo`

```bash
cd code/chapter6/AgentScopeDemo
python -m pip install -r requirements.txt
python main_cn.py
```

### `code/chapter6/Langgraph`

```bash
cd code/chapter6/Langgraph
python -m pip install -r requirements.txt
python Dialogue_System.py
```

### `code/chapter6/CAMEL`

```bash
cd code/chapter6/CAMEL
python -m pip install -r requirements.txt
python DigitalBookWriting.py
```

### `code/chapter9`

```bash
cd code/chapter9
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=""
python 05_terminal_tool_examples.py
python 06_three_day_workflow.py
```

### `code/chapter12`

```bash
cd code/chapter12
python -m pip install hello-agents[evaluation]==0.2.3
python 01_basic_agent_example.py
python 02_bfcl_quick_start.py
```

### `code/chapter13/helloagents-trip-planner`

```bash
cd code/chapter13/helloagents-trip-planner/backend
python -m pip install -r requirements.txt
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000

cd ../frontend
npm install
npm run dev
```

### `code/chapter14/helloagents-deepresearch`

```bash
cd code/chapter14/helloagents-deepresearch/backend
python -m pip install -e .
python src/main.py

cd ../frontend
npm install
npm run dev
```

### `code/chapter15/Helloagents-AI-Town`

```bash
cd code/chapter15/Helloagents-AI-Town/backend
python -m pip install -r requirements.txt
python main.py
```

然后在 Godot 里打开 `code/chapter15/Helloagents-AI-Town/helloagents-ai-town/project.godot`。

## 常见环境变量

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `DASHSCOPE_API_KEY`
- `AMAP_API_KEY`
- `VITE_API_BASE_URL`
