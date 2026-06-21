# chat_cli

最小可运行的大模型命令行对话示例。这个项目把“命令行输入 -> 模式决策 -> 模型调用 -> 终端输出”压缩到最小闭环，适合用来练参数解析、交互循环、Mock/Real 切换和输出截断。

支持的能力：

- 自动模式：有 `OPENROUTER_API_KEY` 或 `OPENAI_API_KEY` 时走真实 API，没有则自动降级为 Mock
- `--mock`：强制 Mock
- `--real`：强制真实 API
- 一次性提问和交互模式
- `--model` 和 `--max-chars`

如果你暂时没有 API Key，先用 `--mock` 把流程跑通，再切换到 `--real`。

## 业务场景说明

- 谁会用：第一次练习大模型 API 的开发者、需要快速验证模型连通性的测试人员。
- 现实中的问题：正式网页、数据库和登录还没做完，但团队已经要确认“输入一句话，程序能不能返回回答”。
- 这个例子怎么解决：先用命令行接收问题，再调用模型并打印回答；没有 Key 时改走 Mock，先练完整控制流。
- 现实例子：输入“请把这封客户邮件整理成三条重点”，程序在终端输出整理结果。确认模型、参数和输出都正常后，再把能力接到正式产品里。

## 安装

```bash
pip install -r ai-learn/agent-lab/projects/chat_cli/requirements.txt
```

## 快速上手

### 1) 自动模式一次性提问

```bash
python3 ai-learn/agent-lab/projects/chat_cli/main.py "用一句话解释什么是 agent"
```

如果没有配置真实 Key，程序会自动切到 Mock。

### 2) 强制 Mock 一次性提问

```bash
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock "用一句话解释什么是 agent"
```

### 3) 强制真实 API 一次性提问

```bash
OPENROUTER_API_KEY=your_api_key python3 ai-learn/agent-lab/projects/chat_cli/main.py --real "给我一个三步学习计划"
```

如果你使用的是 OpenAI 官方 Key，也可以这样：

```bash
OPENAI_API_KEY=your_api_key python3 ai-learn/agent-lab/projects/chat_cli/main.py --real "给我一个三步学习计划"
```

### 4) 交互模式

```bash
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock
python3 ai-learn/agent-lab/projects/chat_cli/main.py --real
```

进入后可连续输入问题，输入 `exit`、`quit`，或者按 `Ctrl+C` / `Ctrl+D` 退出。

### 5) 参数组合练习

```bash
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --model gpt-5 "解释一下 Tool Calling"
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --max-chars 80 "请用较长内容解释 agent、tool calling 和 rag 的区别，并举例说明"
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --model gpt-5 --max-chars 80 "请用较长内容解释 agent、tool calling 和 rag 的区别，并举例说明"
```

### 6) `--max-chars` 练习

```bash
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock "请写一个稍长一点的学习建议"
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --max-chars 60 "请写一个稍长一点的学习建议"
python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --max-chars 80
```

观察点：

- 第二条命令会更短，并带有 `...[truncated N chars]`
- 交互模式下每一轮都会走同一套 `format_output()` 规则
- `--max-chars` 必须大于 0

## 推荐测试清单

| 场景 | 命令 | 预期 |
| --- | --- | --- |
| 自动模式一次性提问 | `python3 ai-learn/agent-lab/projects/chat_cli/main.py "用一句话解释什么是 agent"` | 没有 Key 时自动降级为 Mock |
| 强制 Mock 一次性提问 | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock "用一句话解释什么是 agent"` | 始终使用本地 Mock |
| 强制真实 API 一次性提问 | `OPENROUTER_API_KEY=... python3 ai-learn/agent-lab/projects/chat_cli/main.py --real "给我一个三步学习计划"` | 真实调用成功 |
| 交互 Mock | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock` | 连续输入，`exit` 退出 |
| 交互 Real | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --real` | 真实对话，`exit` 退出 |
| 指定模型 | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --model gpt-5 "解释一下 Tool Calling"` | 模型参数生效 |
| 输出截断 | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --max-chars 80 "请用较长内容解释 agent、tool calling 和 rag 的区别，并举例说明"` | 输出被截断 |
| 参数组合 | `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --model gpt-5 --max-chars 80 "..."` | 多参数同时生效 |

## 代码分层导读

| 文件 / 函数 | 层次 | 作用 |
| --- | --- | --- |
| `main.py` | 程序入口 | 串起参数、调用与输出 |
| `parse_args()` | 输入层 | 读取 `prompt`、`--model`、`--mock`、`--real`、`--max-chars` |
| `resolve_mode()` | 配置层 | 决定自动 / mock / real |
| `build_client()` | 基础设施层 | 真实模式创建 OpenAI 兼容客户端 |
| `build_mock_answer()` | 练习辅助层 | 生成固定风格 mock 响应 |
| `ask_once()` | 调用层 | 按模式走 mock 或真实 API 调用 |
| `format_output()` | 业务逻辑层 | 按 `--max-chars` 截断输出 |
| `run_interactive()` | 控制层 | 连续提问、退出、异常处理 |

## 流程图

![学习闭环流程图](assets/flowchart_simple.svg?v=5b74d8b)

![Python 处理流程（main.py 详细）](assets/flowchart_detailed.svg?v=5b74d8b)

如果平台不支持直接显示 SVG，可以把对应文件转成 PNG 后再引用。

## 建议练习顺序

1. 先跑 `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock`，确认交互和退出逻辑。
2. 再跑 `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --max-chars 80 "..."`，确认输出截断。
3. 再跑 `python3 ai-learn/agent-lab/projects/chat_cli/main.py --mock --model gpt-5 "..."`，确认参数透传。
4. 最后切到 `--real`，验证同一控制流可以复用到真实 API。

## 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加 JSON 结构化输出
2. 把 mock 分支改成可插拔策略
3. 再进入 Tool Calling / RAG

## 业务场景总结

- 输入：命令行问题或交互消息
- 输出：模型回答及实际使用的模型信息
- 生产环境差距：会话持久化、token 裁剪、流式输出、鉴权、限流和内容安全
