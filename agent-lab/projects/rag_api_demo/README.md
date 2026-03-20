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

## 8. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加向量检索
2. 增加认证
3. 增加日志和评估
4. 增加检索质量测试
