# WSL 一键启动 Aider

脚本文件：

```text
softbs/aider/start-aider-wsl.sh
```

终端入口：

```bash
aiderwsl
```

这个命令也已经安装到 `~/.local/bin/aiderwsl`，所以只要 `~/.local/bin` 在 `PATH` 里，就能直接调用。

默认行为：

- 模型：`ollama_chat/qwen2.5-coder:7b`
- 语言：中文
- 编辑格式：`diff`
- 关闭自动提交
- 自动检查并拉起本机 Ollama
- 优先使用当前目录，如果当前目录在 Git 仓库里，会自动切到仓库根目录

常用用法：

```bash
aiderwsl
aiderwsl ~/workspace/vscode_study/ai-lab/hello-agents-main
aiderwsl --architect
aiderwsl --no-stream
aiderwsl --prewarm
```

固定快捷命令：

```bash
aiderwsl-fast
aiderwsl-arch
aiderwsl-no-stream
aiderwsl-prewarm
aiderwsl-3b
aiderwsl-big
```

可覆盖的常用参数：

- `--model <model>`
- `--project-dir <dir>`
- `--chat-language <lang>`
- `--edit-format <format>`
- `--auto-commits`
- `--no-auto-commits`
- `--stream`
- `--no-stream`
- `--architect`
- `--prewarm`

如果你想临时换模型：

```bash
aiderwsl --model ollama_chat/qwen2.5-coder:3b
```

大仓库建议这样起：

```bash
aiderwsl-big
```

等价于：

```bash
aiderwsl --map-tokens 0 --subtree-only
```

适合场景：

- 仓库文件很多；
- repo-map 很重；
- 只想处理一个子目录；
- 只想一次改少量文件。

进入 Aider 以后最常用的交互命令：

```text
/add README.md
/add main.py
/ls
/drop main.py
/model ollama_chat/qwen2.5-coder:7b
/help
/exit
```
