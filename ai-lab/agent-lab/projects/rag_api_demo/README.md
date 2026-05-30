# RAG API Demo — 运行说明

本示例服务支持两种运行方式：

- 本地虚拟环境（推荐用于开发）
- Docker 容器（推荐用于受限环境或当系统无法创建 venv 时）

同时项目提供 `mock_test.py`，可在无任何依赖的情况下快速验证 mock 输出。

## 1) 快速验证（无需依赖）

在项目根目录下运行：

```bash
python3 mock_test.py
```

脚本会打印模拟的 /ask 返回 JSON，适合离线验证逻辑与模板。

## 2) 在本机创建 venv 并运行（需要系统支持 python3-venv）

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

`run-dev.sh` 会尝试：
1. 创建 `.venv`（`python3 -m venv .venv`）
2. 激活并安装 `requirements.txt`
3. 以 `RAG_API_MOCK=1` 启动 `uvicorn main:app`（mock 模式）

若遇到 `ensurepip is not available` 或类似错误，请在 Debian/Ubuntu 上安装系统包后重试：

```bash
sudo apt update && sudo apt install python3-venv
```

## 3) 使用 Docker（当系统无法创建 venv 或希望在容器中运行时）

构建镜像并运行（会在容器内以 mock 模式运行）：

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
docker build -t rag_api_demo:dev .
docker run -e RAG_API_MOCK=1 -p 8000:8000 rag_api_demo:dev
```

运行后访问：`http://localhost:8000/ask`（POST 接口）或根据项目示例使用 curl 测试。

## 常见问题
- 如果系统受管（无法创建 venv）且也没有 Docker，请在具有权限的开发机或 CI 中运行上述 Docker 步骤。
- 如果需要我把示例 curl 请求或简单的 health-check 脚本加入仓库，请回复我会追加。

---
文件位于：`ai-lab/agent-lab/projects/rag_api_demo/`。
# rag_api_demo

最小可运行的 `FastAPI` 版 `RAG` 后端示例。

这个样例的目标是把 `doc_qa_agent` 的本地文档问答能力包装成一个更贴近日本案件要求的后端接口服务。

这次版本已经补了 `PDF` 支持。

这是优先级更高的一步，因为日本现场的这些资料经常就是 `PDF`：

- 规程
- 手顺书
- 设计资料
- 说明书
- 帳票样例

它对应的典型场景是：

- 社内検索 API
- ナレッジ検索 API
- 生成 AI 后端服务
- `Python + FastAPI + RAG` PoC

## 1. 前置条件

- Python 3.10+
- 已安装依赖
- 已配置 `OPENAI_API_KEY`

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 3. 配置环境变量

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:RAG_API_DOCS_DIR="d:/dev/source_code/vscode_study/java-lab"
```

Windows CMD:

```cmd
set OPENAI_API_KEY=your_api_key
set RAG_API_DOCS_DIR=d:/dev/source_code/vscode_study/java-lab
```

macOS / Linux:

```bash
export OPENAI_API_KEY="your_api_key"
export RAG_API_DOCS_DIR="/path/to/docs"
```

## 4. 启动方式

```bash
uvicorn main:app --reload
```

默认监听：

- `http://127.0.0.1:8000`

## 5. 接口

### `GET /health`

健康检查。

### `POST /ask`

请求示例：

```json
{
  "question": "对日项目里的 RAG 和 Tool Calling 哪个优先学？",
  "model": "gpt-5"
}
```

### `POST /reload`

重新加载本地文档并重建内存中的检索数据。

## 6. 返回内容

`/ask` 会返回：

- `answer`
- `model`
- `docs_dir`
- `source_count`
- `sources`

## 7. 这个 demo 的定位

这是一个“案件导向”的最小后端版本：

- 有 API
- 有请求结构
- 有返回结构
- 有健康检查
- 有重载动作
- 支持 `md / txt / pdf`

它还不是正式企业版，但已经更接近：

- `FastAPI`
- `RAG`
- `社内検索`
- 后端服务化

## Python 处理流程（main.py 详细）

下面是 `main.py` 的详细处理流程图（静态 SVG，兼容 GitHub），展示从 FastAPI 启动、文档索引加载，到 `/ask` 请求检索、上下文构建、模型回答和结构化 JSON 返回的完整顺序：

![Python 处理流程（main.py 详细）](assets/main_py_flow.svg)

说明：此图详细展示 `startup_event()`、`load_state()`、`read_document_text()`、`chunk_text()`、`resolve_mode()`、`ask()`、`retrieve()`、`build_context()`、`answer_question()` 与 `AskResponse` 返回逻辑。

## 8. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加向量检索
2. 增加认证
3. 增加日志和评估
4. 增加检索质量测试
