# chat_cli 处理流程图

下面是 `main.py` 的处理流程图（Mermaid 格式），可在支持 Mermaid 的渲染器中直接预览。

下面是 `main.py` 的处理流程（Mermaid 源）：

```mermaid
flowchart TD
	Start([命令行启动]) --> Parse[parse_args()]

	Parse --> Decide{模式决策\n(--mock/--real/自动)}

	Decide -->|强制 --mock| UseMockTrue[use_mock = True]
	Decide -->|强制 --real| UseMockFalse[use_mock = False]
	Decide -->|自动| AutoCheck[检查环境: OPENAI_API_KEY & SDK]

	AutoCheck -->|无 KEY 或 无 SDK| UseMockTrue
	AutoCheck -->|有 KEY 且 有 SDK| UseMockFalse

	UseMockTrue --> BuildMock[build_mock_answer(prompt)]
	UseMockFalse --> BuildClient[build_client() \n(检查 SDK, 读取 OPENAI_API_KEY, 创建客户端)]

	Parse --> HasPrompt{是否提供一次性 `prompt`} 
	HasPrompt -->|是| OneShot[一次性调用流程]
	HasPrompt -->|否| Interactive[交互模式 run_interactive()]

	OneShot -->|use_mock| BuildMock
	OneShot -->|use_real| AskOnceReal[ask_once(client, model, prompt)]

	Interactive --> LoopStart[(交互循环)]
	LoopStart -->|每次输入| AskOnceLoop[ask_once(...)]
	AskOnceLoop -->|use_mock| BuildMock
	AskOnceLoop -->|use_real| AskOnceReal

	BuildMock --> FormatMock[format_output(answer, max_chars)]
	AskOnceReal --> FormatReal[format_output(answer, max_chars)]

	FormatMock --> Output[输出到终端]
	FormatReal --> Output

	%% 错误处理路径
	AskOnceReal -.->|请求异常| ErrorHandler[打印错误并退出或继续]
	AskOnceLoop -.->|请求异常| LoopContinue[打印错误并返回循环]

	%% 终止
	Output --> End([结束或等待下一次输入])
```

注意：
- 如果你在某些查看器或平台上无法直接渲染 Mermaid（例如某些静态站点或老版本 Markdown 预览器），仓库同时保留了静态 SVG（`assets/flowchart_simple.svg`）和 CI 渲染的 PNG (`docs/flowchart.png`) 作为回退，请按需查看。

如何在本地渲染此 Mermaid 图：

- 推荐（VS Code）：安装 `Markdown Preview Mermaid Support` 或 使用内置的 Mermaid 渲染扩展，在打开此文件或项目的 README 时即可看到图形。
- 使用 `mmdc` (mermaid-cli) 渲染为图片：

```bash
# 安装（需要 Node.js + npm）
npm install -g @mermaid-js/mermaid-cli

# 从文件渲染为 PNG
mmdc -i docs/flowchart.md -o docs/flowchart.png

# 或直接渲染内嵌的 Mermaid 片段（用临时 mermaid 文件）
```

注意：CI 或 GitHub 的 README 渲染页面在某些地方不直接渲染 Mermaid，建议同时保留一个 PNG/SVG 版本以便在不支持 Mermaid 的平台也能查看。

如果你希望我现在生成并添加 PNG/SVG（需要在 runner 或你本地安装 `mmdc`），我可以继续执行；否则我会把这个文档作为独立说明提交。 
