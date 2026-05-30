# chat_cli 本地副本说明

> 归位说明：`chat_cli` 的正式 README 和维护入口在 [../../../agent-lab/projects/chat_cli/README.md](../../../agent-lab/projects/chat_cli/README.md)。本目录只是 `llm-lab` 下的可选本地副本，避免学习时来回切目录。

## 1. 这个副本是什么

这个目录是最小模型调用 demo 的副本，用来配合：

- [../../02-模型调用基础.md](../../02-模型调用基础.md)

它的核心作用是帮助你理解：

```text
命令行输入 -> Python 程序 -> LLM API -> 模型回答 -> 终端输出
```

## 2. 不在这里重复维护什么

为了避免和 `agent-lab/projects/chat_cli` 内容重复，本文件不重复维护：

- 完整运行说明
- 代码分层详解
- 学习步骤
- 后续扩展建议

这些统一看：

- [../../../agent-lab/projects/chat_cli/README.md](../../../agent-lab/projects/chat_cli/README.md)
- [../../../agent-lab/projects/chat_cli/main.py](../../../agent-lab/projects/chat_cli/main.py)

## 3. 什么时候看这个目录

| 场景 | 看哪里 |
| --- | --- |
| 想学模型调用基础 | [../../02-模型调用基础.md](../../02-模型调用基础.md) |
| 想运行正式 demo | [../../../agent-lab/projects/chat_cli/README.md](../../../agent-lab/projects/chat_cli/README.md) |
| 想在 `llm-lab` 内部临时修改 | 当前目录 |

## 4. 注意

- 如果源 demo 更新，优先以 `agent-lab/projects/chat_cli` 为准。
- 如果这个副本和源 demo 不一致，应考虑重新复制或直接删除副本。
- 不建议长期同时维护两份不同版本。
