# tool_agent_demo

最小可运行的工具调用 Agent 示例。

这个 demo 是什么：

```text
一个让模型通过 Tool Calling 使用本地文件工具的最小 Agent 示例。
```

日语现场可以说成：

```text
モデルがローカルファイル操作ツールを呼び出す最小構成の AI エージェントです。
```

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

## 业务场景说明

- 谁会用：需要让模型读取真实项目文件的开发人员，例如代码调查、文档搜索和项目交接场景。
- 现实中的问题：新成员接手一个项目，想知道“登录功能写在哪个文件里”。模型本身看不到电脑里的最新代码，如果只凭已有知识回答，很可能猜错。
- 这个例子怎么解决：给模型提供列出文件、读取文件和搜索文字三个工具。模型先判断需要哪个工具，程序执行工具，再把真实结果交回模型继续回答。
- 现实例子：用户问“请找出项目中提到 `OPENAI_API_KEY` 的文件并说明用途”，模型会先调用搜索工具找到文件，再读取相关内容，最后根据实际代码给出说明。
- 初学者重点：模型只负责决定“调用什么工具和传什么参数”，真正读取文件的是 Python 函数；工作目录限制可以避免读取范围失控。

## 业务例子：去北京旅游时怎么理解工具调用

如果把这个 demo 放到“去北京旅游”的场景里，可以这样理解：

```text
目标：去北京玩 3 天，想知道怎么安排最省时间
```

对应关系如下：

| 工具调用环节 | 旅游场景里的作用 | 例子 |
| --- | --- | --- |
| 用户提问 | 提出旅行目标 | “帮我安排北京 3 天游，预算 3000 元” |
| 模型判断 | 决定要查什么 | 判断先查天气、路线、景点顺序 |
| `list_files` | 看有哪些资料 | 类似先看看有哪些景点备选、有哪些酒店区域 |
| `search_text` | 查关键内容 | 类似搜索“故宫”“地铁”“机场大巴”这些关键词 |
| `read_file` | 读具体内容 | 类似把某个景点说明或行程细则详细看一遍 |
| `Tool Result` | 返回真实信息 | 把查到的路线、时间、价格交给模型 |
| `Agent` | 组合答案 | 根据真实资料生成旅游计划，而不是凭空猜 |

可以把这个过程记成一条很短的链：

```text
先想要查什么 -> 再让程序去查 -> 再把结果交回模型 -> 最后生成答案
```

如果你想把它再细一点理解：

1. 你说“帮我规划北京旅游”。
2. 模型先判断是否需要查资料。
3. 如果需要，它会先调用 `search_text` 找相关内容。
4. 找到线索后，再调用 `read_file` 读具体段落。
5. Python 程序把结果回填给模型。
6. 模型根据真实信息给出最终建议。

### 北京旅游版流程图

```mermaid
graph TD
    U["用户<br/>帮我安排北京 3 天游"] --> M["模型判断<br/>要不要查资料"]
    M --> S["search_text<br/>先找关键词和线索"]
    S --> R["read_file<br/>读详细内容"]
    R --> P["Python 程序<br/>把真实结果回填"]
    P --> A["Agent / LLM<br/>整理成旅游方案"]
    A --> O["最终输出<br/>路线、时间、预算建议"]
```

这个图想表达的就是：

- 模型先判断要不要查
- 程序负责真的去查
- 查到结果以后再交回模型
- 模型基于真实信息生成最终答案

## 1. 前置条件

- Python 3.10+
- 已安装依赖
- 已配置 `OPENAI_API_KEY`

## 2. 安装依赖

```bash
pip install -r ai-learn/agent-lab/projects/tool_agent_demo/requirements.txt
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

在 `ai-lab/` 根目录执行时，请把 `--workdir` 指向这个项目目录：
```bash
python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py "帮我列出当前目录的文件" --workdir ai-learn/agent-lab/projects/tool_agent_demo
```
```bash
python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py "读取 README 内容" --workdir ai-learn/agent-lab/projects/tool_agent_demo
```
```bash
python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py "搜索包含 README 的地方" --workdir ai-learn/agent-lab/projects/tool_agent_demo
```

默认会在当前目录工作；如果你在 `ai-lab/` 根目录执行，就需要显式传 `--workdir`：
```bash
python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py "帮我看看这个目录里有哪些 markdown 文件，并总结 README 重点" --workdir ai-learn/agent-lab/projects/tool_agent_demo
```

指定工作目录：

```bash
python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py --workdir ai-learn/agent-lab/projects/tool_agent_demo "列出文件并读取 README"
```

指定模型：

```bash
OPENROUTER_API_KEY=your_api_key python3 ai-learn/agent-lab/projects/tool_agent_demo/main.py --real --model gpt-5 --workdir ai-learn/agent-lab/projects/tool_agent_demo "帮我找数据库相关文档"
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

## Python 处理流程（main.py 详细）

下面是 `main.py` 的详细处理流程图（静态 SVG，兼容 GitHub），展示从参数解析、工作目录校验、工具 schema 构建，到模型工具调用循环、工具结果回填和最终回答输出的完整顺序：

![Python 处理流程（main.py 详细）](assets/main_py_flow.svg)

说明：此图详细展示 `parse_args()`、`resolve_mode()`、`build_client()`、`build_tools()`、`run_agent()`、`call_tool()` 与工具执行闭环。

## 8. 关键名词理解

| 名词 | 日语 | 是什么 | 核心作用 |
| --- | --- | --- | --- |
| Tool Agent | ツール利用エージェント | 可以调用外部工具的 Agent | 让模型能基于真实工具结果完成任务 |
| Tool Schema | ツールスキーマ | 工具名称、参数、说明的结构定义 | 告诉模型工具能做什么、参数怎么传 |
| Tool Call | ツール呼び出し要求 | 模型发出的工具调用请求 | 表示模型选择了某个工具 |
| Tool Result | ツール実行結果 | Python 工具执行后的真实结果 | 回填给模型继续推理 |
| Workdir | 作業ディレクトリ | 工具允许访问的工作目录 | 限制文件操作范围，保证安全 |

## 9. 中文 / 日语现场对照

| 中文 | 日语 | 日本项目现场常见表达 |
| --- | --- | --- |
| 工具调用 Agent | ツール利用エージェント | 外部ツールを利用する Agent を作成します |
| 列出文件 | ファイル一覧取得 | 指定ディレクトリのファイル一覧を取得します |
| 读取文件 | ファイル読み込み | テキストファイルの内容を読み込みます |
| 搜索文本 | テキスト検索 | 指定キーワードでファイル内を検索します |
| 安全边界 | 安全制御 | 作業ディレクトリ外へのアクセスを禁止します |

## 10. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加内部文档搜索工具
2. 增加数据库查询或 API 工具
3. 增加任务计划和步骤日志

## 11. Python 处理流程（速查）

1. **parse_args**：处理命令行输入（任务、--model、--workdir、--mock/--real）。
2. **resolve_mode**：判断运行模式（自动 / mock / real）。
3. **build_client**：准备外部服务（真实模式创建 OpenAI 客户端）。
4. **build_mock_agent_response**：生成 mock 数据（本地返回固定风格答案）。
5. **核心业务**：`build_tools()` 暴露工具 schema，`run_agent()` 驱动工具调用闭环，`call_tool()` 调度 `list_files/read_file/search_text`。
6. **main**：总流程入口，校验工作目录 -> 启动 agent 循环 -> 输出最终回答。

## 业务场景（完整说明）

- **使用者**：需要让 Agent 安全读取、列出和搜索工作区文件的开发者。
- **要解决的问题**：让模型选择工具，同时把所有文件访问限制在指定 workdir 内。
- **输入与输出**：输入自然语言任务和工作目录；输出工具调用、工具结果及最终回答。
- **生产环境差距**：需要用户身份、细粒度权限、沙箱、工具超时、审批、审计和注入防护。

## 整体流程图

```mermaid
graph TD
    A[用户任务] --> B[校验 Workdir]
    B --> C{Real 或 Mock}
    C --> D[模型或规则选择工具]
    D --> E{工具类型}
    E --> F[List Files]
    E --> G[Read File]
    E --> H[Search Text]
    F --> I[工具结果回填]
    G --> I
    H --> I
    I --> J[最终回答]
```
