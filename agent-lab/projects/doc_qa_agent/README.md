# doc_qa_agent

最小可运行的本地文档问答 `RAG` 示例。

这个样例解决的问题是：

- 扫描本地文档目录
- 对文档做简单切分
- 按用户问题做关键词检索
- 把检索结果交给模型生成回答
- 在回答里附带引用来源

它是这条学习线里很关键的一个样例，因为按日本 IT 现场和派遣案件来看，`RAG / 社内検索` 往往比复杂 Agent 更优先落地。

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
```

Windows CMD:

```cmd
set OPENAI_API_KEY=your_api_key
```

macOS / Linux:

```bash
export OPENAI_API_KEY="your_api_key"
```

## 4. 运行方式

默认会读取当前目录下的 `md` / `txt` 文件：

```bash
python main.py "这个目录里数据库相关内容主要讲了什么？"
```

指定文档目录：

```bash
python main.py --docs d:/dev/source_code/vscode_study/java-lab "对日项目里的 RDS 和 Aurora 有什么区别？"
```

指定模型：

```bash
python main.py --model gpt-5 --docs d:/dev/source_code/vscode_study/java-lab "总结数据库移行的重点"
```

## 5. 这个 demo 的实现范围

这是一个“最小 RAG”：

- 文档类型：`md`、`txt`
- 检索方式：本地关键词检索
- 切分方式：按固定大小切分文本
- 结果生成：把 Top-K 片段交给模型总结

它还不是完整企业版 `RAG`，但足够先把这条主线跑通。

## 6. 输出内容

程序会输出：

1. 最终回答
2. 命中的引用片段列表

## 7. 代码说明

- 不依赖向量库
- 不依赖外部检索服务
- 先用最简单的本地检索跑通链路
- 方便后面再升级成向量检索、数据库检索或 API 检索

## 8. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加 `FastAPI` 包装
2. 增加向量检索
3. 增加 PDF 解析
4. 增加检索评估
