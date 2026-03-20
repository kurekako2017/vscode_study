# tool_agent_demo

最小可运行的工具调用 Agent 示例。

这个样例让模型具备 3 个最基础的本地工具能力：

- 列目录
- 读文件
- 搜索文本

它适合作为 `structured_output_demo` 之后的第三个样例，因为这一阶段的重点是：

- 定义工具 schema
- 让模型决定何时调用工具
- 执行工具后把结果再交回模型
- 让模型基于工具结果给出最终回答

如果按日本现场和派遣案件来看，这个样例更适合作为 `RAG` 之后的进阶练习，而不是最开始就优先做的东西。

因为企业现场更常见的是：

- 先做知识检索
- 再做有限工具调用
- 最后才逐步走向 Agent 化

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

默认会在当前目录工作：

```bash
python main.py "帮我看看这个目录里有哪些 markdown 文件，并总结 README 重点"
```

指定工作目录：

```bash
python main.py --workdir d:/dev/source_code/vscode_study/agent-lab "列出文件并读取 README"
```

指定模型：

```bash
python main.py --model gpt-5 --workdir d:/dev/source_code/vscode_study/java-lab "帮我找数据库相关文档"
```

## 5. 内置工具

### `list_files`

- 输入：相对路径
- 输出：目录下的文件与子目录列表

### `read_file`

- 输入：相对文件路径
- 输出：文件内容

### `search_text`

- 输入：关键字、相对路径
- 输出：匹配到的文件和行号

## 6. 安全边界

- 所有工具只能访问 `--workdir` 指定目录内的文件
- 不支持写文件
- 不支持执行命令

## 7. 代码说明

- 使用官方 `Responses API`
- 使用自定义 `function tools`
- 用一个最小循环处理工具调用
- 工具输出统一回填给模型，直到拿到最终文本答案

## 8. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加内部文档搜索工具
2. 增加数据库查询或 API 工具
3. 增加任务计划和步骤日志
