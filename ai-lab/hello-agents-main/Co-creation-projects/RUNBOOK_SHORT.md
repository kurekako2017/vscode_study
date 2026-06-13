# Co-creation-projects 快速运行手册

这是一份可直接复制执行的短清单，优先收录常见运行模式。
这里整理的是命令，不是已经帮你搭好的运行环境。
如果你要直接跑，先安装依赖，再按下面分组执行。

当前仓库已经在根目录创建了共享环境 `.venv/`，并验证过：

- `hello-agents`
- `agentscope`
- `camel`
- `autogen_agentchat`

如果你重新打开终端，先激活环境：

```bash
source .venv/bin/activate
```

## 通用

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

## 单脚本 / CLI

### `939147533-DatabaseAgent`

```bash
cd Co-creation-projects/939147533-DatabaseAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Apricity-InnocoreAI`

```bash
cd Co-creation-projects/Apricity-InnocoreAI
python -m pip install -r requirements.txt
cp .env.example .env
python run.py
```

### `Yixiang-Wu-LearningAgent`

```bash
cd Co-creation-projects/Yixiang-Wu-LearningAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `alexrunner-DataAnalysisAgent`

```bash
cd Co-creation-projects/alexrunner-DataAnalysisAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `haoye2-UnivesalAgent`

```bash
cd Co-creation-projects/haoye2-UnivesalAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `megg-ops-roleplay_agent`

```bash
cd Co-creation-projects/megg-ops-roleplay_agent
python -m pip install -r requirements.txt
cp .env.example .env
python roleplay_agent.py
```

### `lgs-only-NovelGenerator`

```bash
cd Co-creation-projects/lgs-only-NovelGenerator
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

## 前后端分离 / Web

### `afei-GuessWhoAmI`

```bash
cd Co-creation-projects/afei-GuessWhoAmI
bash restart.sh
```

### `angelen-SoftwareDevHelper`

```bash
cd Co-creation-projects/angelen-SoftwareDevHelper
python -m pip install -r requirements.txt
cp .env.example .env
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m uvicorn src.main:app --reload
```

### `usernamedadad-AutoFlow`

```bash
cd Co-creation-projects/usernamedadad-AutoFlow/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd ../frontend
npm install
npm run dev
```

### `xujikai-SentenceExpandAgent`

```bash
cd Co-creation-projects/xujikai-SentenceExpandAgent/backend
python -m pip install -r requirements.txt
cp .env.example .env
python src/main.py

cd ../frontend
npm install
npm run dev
```

### `Shawnxyxy-HealthRecordAgent`

```bash
cd Co-creation-projects/Shawnxyxy-HealthRecordAgent/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

cd ../frontend
python3 -m http.server 8080 --bind 127.0.0.1
```

### `JJason-DeepCastAgent`

```bash
cd Co-creation-projects/JJason-DeepCastAgent/backend
python -m pip install -r requirements.txt
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

cd ../frontend
npm install
npm run dev
```

### `lcyting-StockSage-agent`

```bash
cd Co-creation-projects/lcyting-StockSage-agent
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

cd frontend
npm install
npm run dev
```

### `huailishang-AgentPlatformBase`

```bash
cd Co-creation-projects/huailishang-AgentPlatformBase
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
python smoke_test.py
```

## Gradio / Notebook

### `allen2000-FashionDailyDress`

```bash
cd Co-creation-projects/allen2000-FashionDailyDress
python -m pip install -r requirements.txt
cp .env.example .env
python gradio_app.py
```

### `pamdla-MindEchoAgent`

```bash
cd Co-creation-projects/pamdla-MindEchoAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `kkkano-FinReportAgent`

```bash
cd Co-creation-projects/kkkano-FinReportAgent
python -m pip install -r requirements.txt
jupyter lab
```

### `1zrj-DataAnalysisAgent`

```bash
cd Co-creation-projects/1zrj-DataAnalysisAgent
jupyter lab
```

### `EXAMPLE-ProjectTemplate`

```bash
cd Co-creation-projects/EXAMPLE-ProjectTemplate
jupyter lab
```

## 一、只需要 OpenRouter 的项目

### 1) 全局环境

```bash
export OPENROUTER_API_KEY='你的_openrouter_key'
export LLM_API_KEY="$OPENROUTER_API_KEY"
export OPENAI_API_KEY="$OPENROUTER_API_KEY"
export LLM_BASE_URL='https://openrouter.ai/api/v1'
export OPENAI_BASE_URL='https://openrouter.ai/api/v1'
export LLM_MODEL_ID='~openai/gpt-latest'
export LLM_MODEL='~openai/gpt-latest'
```

### 2.1 已验证可直接运行的无 key 示例

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter9
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=''
.venv/bin/python 05_terminal_tool_examples.py
```

### 2) 只要 OpenRouter 就能跑

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter10/weather-mcp-server
python -m pip install -r requirements.txt
python server.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AutoGenDemo
python -m pip install -r requirements.txt
python autogen_software_team.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/CAMEL
python -m pip install -r requirements.txt
python DigitalBookWriting.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter9
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=''
python 05_terminal_tool_examples.py
```

## 二、还需要额外 key / 服务的项目

### 1) 额外 key / 服务

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AgentScopeDemo
python -m pip install -r requirements.txt
export DASHSCOPE_API_KEY='你的_dashscope_key'
python main_cn.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter13/helloagents-trip-planner/backend
python -m pip install -r requirements.txt
cp .env.example .env
export AMAP_API_KEY='你的_高德服务端_key'
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/afei-GuessWhoAmI/backend
python -m pip install -r requirements.txt
cp .env.example .env
export LLM_API_KEY='你的_modelscope_key'
export LLM_BASE_URL='https://api-inference.modelscope.cn/v1/'
export TAVILY_API_KEY='你的_tavily_key'
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/939147533-DatabaseAgent
python -m pip install -r requirements.txt
cp .env.example .env
export DB_HOST='127.0.0.1'
export DB_PORT='1521'
export DB_SERVICE_NAME='ORCL'
export DB_USERNAME='your_user'
export DB_PASSWORD='your_password'
python main.py
```
