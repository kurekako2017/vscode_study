# Co-creation-projects 运行总览

这份文档整理 `Co-creation-projects/` 下能直接运行的项目入口，尽量统一成“安装 - 配置 - 启动”的格式。

当前仓库根目录已经创建了共享环境 `.venv/`，并完成了基础验证：

- `hello-agents`
- `agentscope`
- `camel`
- `autogen_agentchat`

如果你重新打开终端，先执行：

```bash
source .venv/bin/activate
```

通用原则：

- Python 项目优先使用 `python -m pip`
- FastAPI/Uvicorn 优先使用 `python -m uvicorn ...`
- 前后端分离项目先启动后端，再启动前端
- 每个项目优先参考自己的 `.env.example`

## 通用前置环境

- Python 3.10+
- Node.js 18+
- Jupyter Lab，仅 Notebook 型项目需要
- Gradio，仅对应项目需要

推荐：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

## 1. 单脚本 / CLI 项目

### `Co-creation-projects/939147533-DatabaseAgent`

用途：这是一个“用自然语言查数据库”的示例项目。你可以直接问中文问题，它会尝试把问题转换成 SQL，再去 Oracle 数据库里查结果。适合学习数据库查询和 LLM 生成 SQL 的基本流程。

```bash
cd Co-creation-projects/939147533-DatabaseAgent
python -m pip install -r requirements.txt
cp .env.example .env
python test.py
python main.py
```

需要变量：

- `LLM_MODEL_ID`
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `DB_HOST`
- `DB_PORT`
- `DB_SERVICE_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`

### `Co-creation-projects/Apricity-InnocoreAI`

用途：这是一个面向科研场景的综合助手。它可以帮你找论文、读论文、做分析，还能辅助写作和检查引用。初学者可以把它理解成“论文检索 + 论文分析 + 写作辅助”的一体化系统。

```bash
cd Co-creation-projects/Apricity-InnocoreAI
python -m pip install -r requirements.txt
cp .env.example .env
python install.py
python run.py
```

需要变量：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `OPENAI_MODEL`（可选，默认 `gpt-3.5-turbo`）

### `Co-creation-projects/Yixiang-Wu-LearningAgent`

用途：这是一个学习管理助手。它可以根据你的目标生成学习计划，也能帮你记录知识、做总结、追踪进度。适合用来理解“学习过程如何被拆成计划、笔记和复盘”。

```bash
cd Co-creation-projects/Yixiang-Wu-LearningAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/alexrunner-DataAnalysisAgent`

用途：这是一个偏商业场景的数据分析项目。它通常围绕商品销售数据展开，帮助你自动做图、看趋势、写分析结论。适合练习把原始数据变成可读结论。

```bash
cd Co-creation-projects/alexrunner-DataAnalysisAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/haoye2-UnivesalAgent`

用途：这是一个通用型智能体示例。它既能做信息搜索，也能执行一些受控命令，重点展示“一个 Agent 怎么在不同工具之间切换”。初学者可以重点看它的工具调用逻辑。

```bash
cd Co-creation-projects/haoye2-UnivesalAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/megg-ops-roleplay_agent`

用途：这是一个角色扮演对话项目。你可以自定义角色设定，让 Agent 按角色身份和你对话，甚至在不同角色之间切换。适合学习“人格设定”和“沉浸式交互”。

```bash
cd Co-creation-projects/megg-ops-roleplay_agent
python -m pip install -r requirements.txt
cp .env.example .env
python roleplay_agent.py
```

### `Co-creation-projects/melxy1997-ColumnWriter`

用途：这是一个专栏写作助手。它会先规划主题，再写作、修改和优化，最后形成较完整的专栏内容。适合学习“内容生产流水线”。

```bash
cd Co-creation-projects/melxy1997-ColumnWriter
python -m pip install -r requirements.txt
python main.py
```

### `Co-creation-projects/pamdla-MindEchoAgent`

用途：这是一个情绪音乐推荐助手。它会根据你的心情或状态推荐合适的音乐。适合学习“基于用户状态的个性化推荐”。

```bash
cd Co-creation-projects/pamdla-MindEchoAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/jjyaoao-CodeReviewAgent`

用途：这是一个代码审查项目。它会自动检查 Python 代码的可读性、结构和潜在问题，并给出优化建议。适合学习“自动评审代码”这一类 Agent 能力。

```bash
cd Co-creation-projects/jjyaoao-CodeReviewAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/laoyouf-aistory`

用途：这是一个故事写作助手。你给它主题、风格和文体，它就能生成故事、短篇小说或类似的创作内容。适合理解“生成式写作 Agent”的基础能力。

```bash
cd Co-creation-projects/laoyouf-aistory
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/lgs-only-NovelGenerator`

用途：这是一个长篇小说生成助手。它不只是生成单段文本，还会尽量维护大纲、剧情连贯性和上下文记忆。适合学习长文本创作时 Agent 如何保持一致性。

```bash
cd Co-creation-projects/lgs-only-NovelGenerator
python -m pip install -r requirements.txt
cp .env.example .env
python src/app.py
python main.py
```

### `Co-creation-projects/lll0807-CodeTutorAgent/programmer`

用途：这是一个编程导师项目。它会帮你规划学习路径、生成练习题，并对你的代码做基础评审。适合把它当成“练习题 + 辅导 + 反馈”的组合教练。

```bash
cd Co-creation-projects/lll0807-CodeTutorAgent/programmer
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/zjzhou-SREOnCallAgent`

用途：这是一个面向运维值班的助手。它会帮助你处理告警分诊、排查原因，并整理成故障复盘报告。适合学习“事件处理流程自动化”。

```bash
cd Co-creation-projects/zjzhou-SREOnCallAgent
python -m pip install -r requirements.txt
cp .env.example .env
python src/api/main.py
```

### `Co-creation-projects/cc1227871-StockInsightAgent`

用途：这是一个股票分析示例项目。它会把行情、财报和新闻等信息汇总起来，再输出结构化分析报告。初学者可以把它看成“金融数据收集 + 观点整理”的自动化流程。

```bash
cd Co-creation-projects/CC1227871-StockInsightAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
python app.py
```

### `Co-creation-projects/kkkano-FinReportAgent`

用途：这是一个金融研报生成项目。它会从多个数据源收集信息，然后整理成更完整的投资分析报告。初学者可以把它理解为“多源信息整合 + 自动写研报”。

```bash
cd Co-creation-projects/kkkano-FinReportAgent
python -m pip install -r requirements.txt
cp .env.example .env
jupyter lab
```

### `Co-creation-projects/1zrj-DataAnalysisAgent`

用途：这是一个数据分析入门案例。你把数据文件给它之后，它会帮你做基础统计、生成图表，并整理成一份更容易阅读的分析报告。适合想理解“数据分析 Agent 能自动化到什么程度”的初学者。

```bash
cd Co-creation-projects/1zrj-DataAnalysisAgent
jupyter lab
```

### `Co-creation-projects/jack6249-GiftGeniusAgent`

用途：这是一个送礼推荐助手。你输入送礼对象、预算和场景，它会帮你一步步筛选并生成更个性化的礼物方案。适合初学者看“需求约束如何影响推荐结果”。

```bash
cd Co-creation-projects/jack6249-GiftGeniusAgent
jupyter lab
```

### `Co-creation-projects/EXAMPLE-ProjectTemplate`

用途：这是一个标准模板项目。它的价值不在功能本身，而在于告诉你一个共创项目通常应该怎么组织目录、怎么写说明、怎么放示例文件。适合拿来当新项目起点。

```bash
cd Co-creation-projects/EXAMPLE-ProjectTemplate
jupyter lab
```

## 2. 前后端分离项目

### `Co-creation-projects/angelen-SoftwareDevHelper`

用途：这是一个软件开发学习助手。它会根据用户水平出题、检查代码，并给出改进建议，偏向“练习 + 评测 + 反馈”的学习闭环。

后端：

```bash
cd Co-creation-projects/angelen-SoftwareDevHelper
python -m pip install -r requirements.txt
cp .env.example .env
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m uvicorn src.main:app --reload
```

### `Co-creation-projects/usernamedadad-AutoFlow`

用途：这是一个把自然语言转换成流程图的项目。你输入需求，它会生成 Mermaid 图并支持前端预览，适合学习“文本到结构图”的转换。

后端：

```bash
cd Co-creation-projects/usernamedadad-AutoFlow/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

前端：

```bash
cd Co-creation-projects/usernamedadad-AutoFlow/frontend
npm install
npm run dev
```

### `Co-creation-projects/xujikai-SentenceExpandAgent`

用途：这是一个英语句子扩写助手。它会把简单句逐步扩写成更完整的长句，适合练习英语表达和理解多步改写流程。

后端：

```bash
cd Co-creation-projects/xujikai-SentenceExpandAgent/backend
python -m pip install -r requirements.txt
cp .env.example .env
python src/main.py
```

前端：

```bash
cd Co-creation-projects/xujikai-SentenceExpandAgent/frontend
npm install
npm run dev
```

### `Co-creation-projects/afei-GuessWhoAmI`

用途：这是一个互动猜人物游戏。用户通过提问一步步缩小范围，Agent 扮演指定人物进行回应，适合学习对话式交互。

一键脚本：

```bash
cd Co-creation-projects/afei-GuessWhoAmI
bash restart.sh
```

手动模式：

```bash
cd Co-creation-projects/afei-GuessWhoAmI/backend
python -m pip install -r requirements.txt
cp .env.example .env
python main.py

cd ../frontend
python -m http.server 3000
```

### `Co-creation-projects/allen2000-FashionDailyDress`

用途：这是一个天气穿搭建议项目。它会结合天气和穿搭场景给出建议，适合学习生活类推荐系统如何工作。

```bash
cd Co-creation-projects/allen2000-FashionDailyDress
python -m pip install -r requirements.txt
cp .env.example .env
python gradio_app.py
python simple_multi_agent.py
```

### `Co-creation-projects/huailishang-AgentPlatformBase`

用途：这是一个智能体平台底座。它把多个业务 Agent 统一管理起来，适合学习“平台如何调度多个子 Agent”。

```bash
cd Co-creation-projects/huailishang-AgentPlatformBase
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
python smoke_test.py
```

### `Co-creation-projects/lcyting-StockSage-agent`

用途：这是一个股票分析系统。它把行情、财务和新闻信息整合起来，并通过前后端界面提供分析能力，适合看完整应用如何拆分。

后端：

```bash
cd Co-creation-projects/lcyting-StockSage-agent
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

前端：

```bash
cd Co-creation-projects/lcyting-StockSage-agent/frontend
npm install
npm run dev
```

### `Co-creation-projects/JJason-DeepCastAgent`

用途：这是一个 AI 播客制作项目。它会把调研结果整理成更像播客对话的内容，适合学习“把研究内容改写成内容产品”。

后端：

```bash
cd Co-creation-projects/JJason-DeepCastAgent/backend
python -m pip install -r requirements.txt
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

前端：

```bash
cd Co-creation-projects/JJason-DeepCastAgent/frontend
npm install
npm run dev
```

### `Co-creation-projects/Shawnxyxy-HealthRecordAgent`

用途：这是一个健康档案助手。它能解读体检报告、给出饮食建议，并支持后续跟踪，适合理解健康管理闭环。

后端：

```bash
cd Co-creation-projects/Shawnxyxy-HealthRecordAgent/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

前端：

```bash
cd Co-creation-projects/Shawnxyxy-HealthRecordAgent/frontend
python3 -m http.server 8080 --bind 127.0.0.1
```

### `Co-creation-projects/bichchibui5-hub-EmailSmartAssistant`

用途：这是一个邮件智能助手。它可以分类邮件、生成回复草稿、提炼重点，适合学习信息整理型 Agent。

```bash
cd Co-creation-projects/bichchibui5-hub-EmailSmartAssistant
python -m pip install -r requirements.txt
python demo.py
```

### `Co-creation-projects/Apricity-InnocoreAI`

用途：这是一个科研创新助手的服务化入口。它会把论文检索、分析、写作和引用能力通过 API 暴露出来，适合学习如何把研究类 Agent 做成服务。

这个项目同时也有 `api/main.py`，如果你想作为服务运行，可使用：

```bash
cd Co-creation-projects/Apricity-InnocoreAI
python -m pip install fastapi uvicorn python-multipart python-dotenv pydantic httpx requests
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. Web / Web UI / 服务化项目

### `Co-creation-projects/meiguanxiHXX-historyReviewAgent`

用途：这是一个历史讨论和辩论项目。它会从不同视角分析历史问题，适合学习多角色、多立场的内容生成。

Web 界面：

```bash
cd Co-creation-projects/meiguanxiHXX-historyReviewAgent
python -m pip install -r requirements.txt
pip install -e .
cp .env.example .env
python run_web.py
```

命令行：

```bash
python -m historical_review.run_agent -y "你的历史议题"
```

### `Co-creation-projects/tino-chen-HelloClaw`

用途：这是一个个性化 AI 助手项目。它支持身份定制、记忆、工具调用和前后端交互，适合学习一个完整 AI 助手是怎样搭起来的。

后端：

```bash
cd Co-creation-projects/tino-chen-HelloClaw
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload --port 8000
```

前端：

```bash
cd Co-creation-projects/tino-chen-HelloClaw/frontend
npm install
npm run dev
```

### `Co-creation-projects/czxgg0630-ProductAnalysisAgent`

用途：这是一个竞品分析工具。它会收集多个产品的信息并生成对比分析，适合学习“收集 - 对比 - 输出报告”的流程。

```bash
cd Co-creation-projects/czxgg0630-ProductAnalysisAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/chen070808-ProgrammingTutor`

用途：这是一个编程教学项目。它可以帮你规划学习路径、生成练习题，并对代码做评审，适合学习教学型 Agent。

```bash
cd Co-creation-projects/chen070808-ProgrammingTutor
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/healer-666-Academic-Data-Agent`

用途：这是一个科研数据处理助手。它主要面向表格和 PDF 文献，帮助提取主表信息并做分析，适合学习文献数据抽取。

```bash
cd Co-creation-projects/healer-666-Academic-Data-Agent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### `Co-creation-projects/lh2021739-pixel-Personal_Information_Signaling_System`

用途：这个目录更像素材和资源集合，不是完整交互应用。里面主要是人物、提醒和主题相关的图片或配置文件。

```bash
cd Co-creation-projects/lh2021739-pixel-Personal_Information_Signaling_System
python -m pip install -r requirements.txt
python main.py
```

### `Co-creation-projects/jjyaoao-CodeReviewAgent`

用途：这是一个代码审查项目。它会自动检查 Python 代码的可读性、结构和潜在问题，并给出优化建议。

Notebook-based project. 推荐：

```bash
cd Co-creation-projects/jjyaoao-CodeReviewAgent
jupyter lab
```

### `Co-creation-projects/bichchibui5-hub-EmailSmartAssistant`

用途：这是一个笔记本加演示脚本的邮件助手项目。它适合直接跑 demo 看效果，理解邮件分类和自动回复的工作流。

Notebook + demo 脚本。推荐直接跑：

```bash
cd Co-creation-projects/bichchibui5-hub-EmailSmartAssistant
python demo.py
```

## 4. Notebook-only 项目

这些项目主要以 `main.ipynb` 为主，建议用 Jupyter 打开。它们通常更适合边看代码、边看输出、边理解整个 Agent 流程。

- `Co-creation-projects/1zrj-DataAnalysisAgent`：适合看数据分析 Agent 如何把原始数据变成图表和结论。
- `Co-creation-projects/EXAMPLE-ProjectTemplate`：适合了解一个共创项目的标准目录和写法。
- `Co-creation-projects/jack6249-GiftGeniusAgent`：适合看推荐类 Agent 如何结合对象、预算和场景给建议。
- `Co-creation-projects/jjyaoao-CodeReviewAgent`：适合看代码审查是怎么被拆成分析和建议两个步骤的。
- `Co-creation-projects/kkkano-FinReportAgent`：适合看金融研报如何从多源信息自动生成。
- `Co-creation-projects/laoyouf-aistory`：适合看故事生成任务如何从主题扩展成完整文本。
- `Co-creation-projects/chen070808-ProgrammingTutor`：适合看编程教学型 Agent 如何规划、出题和评审。
- `Co-creation-projects/haoye2-UnivesalAgent`：适合看通用 Agent 如何在搜索和命令执行之间切换。
- `Co-creation-projects/healer-666-Academic-Data-Agent`：适合看论文表格和 PDF 数据是怎样被抽取出来的。
- `Co-creation-projects/zjzhou-SREOnCallAgent`：适合看告警、排查、复盘这条运维流程如何被自动化。
- `Co-creation-projects/pamdla-MindEchoAgent`：适合看情绪和音乐推荐是怎样做关联的。
- `Co-creation-projects/tino-chen-HelloClaw`：适合看一个较完整的个性化 AI 助手在 notebook 里如何搭建。

## 常见环境变量

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_ID`
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `DASHSCOPE_API_KEY`
- `AMAP_API_KEY`
- `VITE_API_BASE_URL`
- `DB_HOST`
- `DB_PORT`
- `DB_SERVICE_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`

## OpenRouter 优先运行清单

### 全局环境

```bash
export OPENROUTER_API_KEY='你的_openrouter_key'
export LLM_API_KEY="$OPENROUTER_API_KEY"
export OPENAI_API_KEY="$OPENROUTER_API_KEY"
export LLM_BASE_URL='https://openrouter.ai/api/v1'
export OPENAI_BASE_URL='https://openrouter.ai/api/v1'
export LLM_MODEL_ID='~openai/gpt-latest'
export LLM_MODEL='~openai/gpt-latest'
export LLM_PROVIDER='custom'
```

### 已验证可直接运行的无 key 示例

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter9
export EMBED_MODEL_TYPE=tfidf
export EMBED_MODEL_NAME=''
.venv/bin/python 05_terminal_tool_examples.py
```

### 只要 OpenRouter 就能跑，或本身不额外要 key

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter10/weather-mcp-server
python -m pip install -r requirements.txt
python server.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter6/AutoGenDemo
python -m pip install -r requirements.txt
python autogen_software_team.py
streamlit run output.py
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
python 06_three_day_workflow.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter12
python -m pip install hello-agents[evaluation]==0.2.3
python 01_basic_agent_example.py
python 02_bfcl_quick_start.py
python 03_bfcl_custom_evaluation.py
python 04_run_bfcl_evaluation.py
python 07_data_generation_complete_flow.py 30 3.0
python 08_data_generation_llm_judge.py
python 09_data_generation_win_rate.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter14/helloagents-deepresearch/backend
python -m pip install -e .
export SEARCH_API=duckduckgo
python src/main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter15/Helloagents-AI-Town/backend
python -m pip install -r requirements.txt
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/angelen-SoftwareDevHelper
python -m pip install -r requirements.txt
cp .env.example .env
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m uvicorn src.main:app --reload
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/usernamedadad-AutoFlow/backend
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/xujikai-SentenceExpandAgent/backend
python -m pip install -r requirements.txt
cp .env.example .env
python src/main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/meiguanxiHXX-historyReviewAgent
python -m pip install -r requirements.txt
python -m pip install -e .
cp .env.example .env
python run_web.py
python -m historical_review.run_agent -y "你的历史议题"
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/tino-chen-HelloClaw
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn src.main:app --reload --port 8000
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/pamdla-MindEchoAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/lgs-only-NovelGenerator
python -m pip install -r requirements.txt
cp .env.example .env
python src/app.py
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/huailishang-AgentPlatformBase
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
python smoke_test.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/lll0807-CodeTutorAgent/programmer
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/haoye2-UnivesalAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/alexrunner-DataAnalysisAgent
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

### 还需要额外 key / 服务的项目

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
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/code/chapter13/helloagents-trip-planner/frontend
cp .env.example .env
export VITE_API_BASE_URL='http://localhost:8000'
export VITE_AMAP_WEB_KEY='你的_高德Web服务Key'
export VITE_AMAP_WEB_JS_KEY='你的_高德JSAPIKey'
npm install
npm run dev
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/afei-GuessWhoAmI/backend
python -m pip install -r requirements.txt
cp .env.example .env
export LLM_MODEL_ID='qwen-flash'
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

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/Apricity-InnocoreAI
python -m pip install -r requirements.txt
cp .env.example .env
export TTS_API_KEY='你的_tts_key'
export TAVILY_API_KEY='你的_tavily_key'
python run.py
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/hello-agents-main/Co-creation-projects/CC1227871-StockInsightAgent
python -m pip install -r requirements.txt
cp .env.example .env
export MX_APIKEY='你的_mx_apikey'
python main.py
python app.py
```

## 共创项目逐项总览

这部分把每个项目用初学者更容易理解的话说明一下，主要回答三个问题：

- 这个项目是什么
- 它能帮你做什么
- 你应该从哪里切入理解

具体安装和启动命令继续沿用上面的分类区。

配置现状先说明一下：

- 有些项目已经有本地默认值，能先把服务或界面启动起来
- 但凡涉及 LLM、搜索、地图、金融数据、数据库登录的功能，通常还是要你自己填真实凭据
- 我能补的是默认值、模板和更清晰的说明，不能凭空生成可用的 API Key 或数据库密码

### `1zrj-DataAnalysisAgent`
用途：这是一个数据分析入门案例。你把数据文件给它之后，它会帮你做基础统计、生成图表，并整理成一份更容易阅读的分析报告。适合想理解“数据分析 Agent 能自动化到什么程度”的初学者。

### `939147533-DatabaseAgent`
用途：这是一个“自然语言查数据库”的示例。你可以直接用中文问问题，它会尝试把问题翻译成 SQL，再去 Oracle 数据库里查结果。适合学习数据库查询和 LLM 生成 SQL 的入门场景。

### `Apricity-InnocoreAI`
用途：这是一个面向科研场景的综合型助手。它可以帮你找论文、读论文、做分析，还能辅助写作和检查引用。初学者可以把它理解成“论文检索 + 论文分析 + 写作辅助”的组合系统。

### `AstrumPush-Smart-Recipe-Agent`
用途：这是一个智能菜谱助手。你输入饮食需求、口味偏好或限制条件，它会帮你整理菜谱建议、配料和做法。适合学习“任务型 Agent 如何根据用户约束生成结果”。

### `CC1227871-StockInsightAgent`
用途：这是一个股票分析示例项目。它会把行情、财报和新闻等信息汇总起来，再输出结构化分析报告。初学者可以把它看成“金融数据收集 + 观点整理”的自动化流程。

### `EXAMPLE-ProjectTemplate`
用途：这是一个标准模板项目。它的价值不在功能本身，而在于告诉你一个共创项目通常应该怎么组织目录、怎么写说明、怎么放示例文件。适合拿来当新项目起点。

### `JJason-DeepCastAgent`
用途：这是一个“把研究内容转成播客”的项目。它先把资料整理清楚，再把结果改写成更像双人对谈的口语化内容。适合理解“内容再加工”型 Agent。

### `Shawnxyxy-HealthRecordAgent`
用途：这是一个健康管理助手。它会根据体检报告或健康记录给出解读、饮食建议和后续跟踪建议。初学者可以把它理解成“读报告 + 提建议 + 追踪执行”的闭环系统。

### `YYHDBL-HelloCodeAgentCli`
用途：这是一个本地代码助手命令行工具。它可以陪你多轮对话、探索代码仓库、生成补丁，并在你确认后真正修改文件。`code_agent/` 是核心逻辑，`prompts/` 放的是行为提示词，适合学习“代码 Agent 如何做检索、规划和修改”。

### `Yixiang-Wu-LearningAgent`
用途：这是一个学习管理助手。它能根据你的学习目标生成计划，也能帮你记录知识、做总结、跟踪进度。适合初学者理解“如何把学习过程拆成计划、笔记和复盘”。

### `afei-GuessWhoAmI`
用途：这是一个互动猜人物游戏。Agent 会扮演某个历史人物、神话人物或公众人物，你通过提问慢慢缩小范围来猜身份。它更偏向趣味交互，适合学习对话式 Agent 的基本玩法。

### `alexrunner-DataAnalysisAgent`
用途：这是一个偏商业场景的数据分析项目。它通常围绕商品销售数据展开，帮助你自动做图、看趋势、写分析结论。适合练习把原始数据变成可读结论。

### `allen2000-FashionDailyDress`
用途：这是一个天气穿搭建议系统。它会先看天气，再结合穿衣场景给出当天怎么穿更合适的建议。适合初学者理解“多智能体协作处理日常生活问题”。

### `angelen-SoftwareDevHelper`
用途：这是一个面向程序学习者的辅助工具。它会记住你的水平，给你出题，帮你检查代码，再给出评分和建议。适合学习“教学型 Agent 如何做个性化反馈”。

### `bichchibui5-hub-EmailSmartAssistant`
用途：这是一个邮件处理助手。它可以帮你把邮件分类、提炼重点、生成回复草稿，还能顺手做提醒安排。适合初学者理解“信息整理型 Agent”的作用。

### `chen070808-ProgrammingTutor`
用途：这是一个编程教学项目。它可以帮你规划学习路径、生成练习题，并对你的代码做基础评审。适合把它当成“练习题 + 辅导 + 反馈”的组合教练。

### `czxgg0630-ProductAnalysisAgent`
用途：这是一个竞品分析工具。它会收集多个产品或服务的信息，然后按维度做对比，最后输出分析报告。适合学习“信息收集 + 对比总结”的工作流。

### `haoye2-UnivesalAgent`
用途：这是一个通用型智能体示例。它既能做信息搜索，也能执行一些受控命令，重点展示“一个 Agent 怎么在不同工具之间切换”。初学者可以重点看它的工具调用逻辑。

### `healer-666-Academic-Data-Agent`
用途：这是一个科研数据处理助手。它主要面向表格数据和 PDF 文献，帮助你提取主表信息并做进一步分析。适合学习“文献数据抽取”这类任务。

### `huailishang-AgentPlatformBase`
用途：这是一个智能体平台底座，不是单一功能应用。它统一管理多个业务智能体，比如深度研究和 RSS 摘要，所以更适合学习“一个平台如何调度多个 Agent”。

### `jack6249-GiftGeniusAgent`
用途：这是一个送礼推荐助手。你输入送礼对象、预算和场景，它会帮你一步步筛选并生成更个性化的礼物方案。适合初学者看“需求约束如何影响推荐结果”。

### `jjyaoao-CodeReviewAgent`
用途：这是一个代码审查项目。它会自动检查 Python 代码的可读性、结构和潜在问题，并给出优化建议。适合学习“自动评审代码”这一类 Agent 能力。

### `kkkano-FinReportAgent`
用途：这是一个金融研报生成项目。它会从多个数据源收集信息，然后整理成更完整的投资分析报告。初学者可以把它理解为“多源信息整合 + 自动写研报”。

### `laoyouf-aistory`
用途：这是一个故事写作助手。你给它主题、风格和文体，它就能生成故事、短篇小说或类似的创作内容。适合理解“生成式写作 Agent”的基础能力。

### `lcyting-StockSage-agent`
用途：这是一个前后端联动的股票分析系统。它把行情、财务、新闻等信息整合起来，再通过界面和后端服务对外提供分析能力。适合学习完整应用是怎么拆分前后端的。

### `lgs-only-NovelGenerator`
用途：这是一个长篇小说生成助手。它不只是生成单段文本，还会尽量维护大纲、剧情连贯性和上下文记忆。适合学习长文本创作时 Agent 如何保持一致性。

### `lh2021739-pixel-Personal_Information_Signaling_System`
用途：这个目录当前更像素材和资源集合，不是一个完整的交互应用。里面主要是人物、提醒和主题相关的图片或配置文件。初学者可以先把它当成资源目录理解。

### `lll0807-CodeTutorAgent`
用途：这是一个编程导师项目族。`programmer/` 是主要实现，`data/` 放的是示例资源，整体围绕学习路径、出题和代码评审展开。适合对比它和其他教学型 Agent 的实现方式。

### `megg-ops-roleplay_agent`
用途：这是一个角色扮演对话项目。你可以自定义角色设定，让 Agent 按角色身份和你对话，甚至在不同角色之间切换。适合学习“人格设定”和“沉浸式交互”。

### `meiguanxiHXX-historyReviewAgent`
用途：这是一个历史讨论和辩论项目。它会从正史、野史、政治语境和怀疑论等不同视角讨论历史问题，帮助你看到不同立场的分析方式。适合初学者理解“多视角生成”。

### `melxy1997-ColumnWriter`
用途：这是一个专栏写作助手。它会先规划主题，再写作、修改和优化，最后形成较完整的专栏内容。适合学习“内容生产流水线”。

### `pamdla-MindEchoAgent`
用途：这是一个情绪音乐推荐助手。它会根据你的心情或状态推荐合适的音乐。适合学习“基于用户状态的个性化推荐”。

### `tino-chen-HelloClaw`
用途：这是一个个性化 AI 助手项目。它支持身份定制、记忆、工具调用和前后端交互，功能比较完整。初学者可以把它当成“一个可配置的 AI 助手平台”来理解。

### `usernamedadad-AutoFlow`
用途：这是一个流程图生成工具。你输入自然语言，它会帮你转成 Mermaid 流程图，并支持实时预览。适合学习“文本到结构化图形”的转换思路。

### `xujikai-SentenceExpandAgent`
用途：这是一个英语句子扩写项目。它会把简单句逐步扩写成更复杂、更自然的长句，偏向语言学习场景。适合理解“分步骤改写”的协作流程。

### `zjzhou-SREOnCallAgent`
用途：这是一个面向运维值班的助手。它会帮助你处理告警分诊、排查原因，并整理成故障复盘报告。适合学习“事件处理流程自动化”。

### `huailishang-AgentPlatformBase/agents/deep_research`
用途：这是平台里的深度研究智能体。它负责长时间调研、整理资料和输出研究报告，属于“做深做细”的那一类 Agent。

### `huailishang-AgentPlatformBase/agents/rss_digest`
用途：这是平台里的 RSS 摘要智能体。它负责抓取资讯、提取重点并生成简报，适合学习“定时信息聚合”。

### `YYHDBL-HelloCodeAgentCli/code_agent`
用途：这是 CLI 的核心代码区域。它把上下文、终端操作、笔记、记忆等能力封装起来，是理解整个命令行 Agent 的关键入口。

### `YYHDBL-HelloCodeAgentCli/code_agent/prompts`
用途：这是 CLI 的提示词资源目录。里面存放的是角色设定、工作流步骤和工具使用方式相关的 prompt，属于 Agent 行为的“说明书”。
