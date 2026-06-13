# VSCode + WSL 本地运行 Aider + Ollama + Qwen2.5-Coder 3B/7B 教程

适合环境：Windows 11 + VSCode Remote WSL + Ubuntu + Ollama + 本地 Qwen2.5-Coder 模型。  
目标：在 VSCode 终端里使用 `aider`，连接本地 Ollama 的 `qwen2.5-coder:3b` 或 `qwen2.5-coder:7b`，练习本地 AI 编程 / Agent 开发。

---

## 0. 先理解整体结构

运行结构是这样：

```text
VSCode WSL 终端
    ↓
Aider CLI
    ↓
Ollama API: http://127.0.0.1:11434
    ↓
qwen2.5-coder:3b / qwen2.5-coder:7b
```

也就是说：

- VSCode 只是编辑器；
- WSL 终端里运行 `aider`；
- Aider 通过 Ollama 调用本地模型；
- 不需要 OpenAI API Key；
- 不消耗 Codex / ChatGPT Plus 流量。

---

## 1. 选择 3B 还是 7B

| 模型 | 适合用途 | 速度 | 能力 |
|---|---|---|---|
| `qwen2.5-coder:3b` | 入门、快速练习、Agent workflow | 快 | 足够练 Tool Calling / 小项目 |
| `qwen2.5-coder:7b` | 更像正式 Coding Assistant | 中等 | 文档理解、代码修改、Agent 能力更好 |

建议：

```text
日常快速练习：3B
认真改代码 / 文档总结 / Aider 多文件修改：7B
复杂任务：以后再接 NVIDIA NIM / Codex CLI
```

Qwen2.5-Coder 在 Ollama 上提供 0.5B、1.5B、3B、7B、14B、32B 等尺寸，官方说明它主要提升了代码生成、代码推理和代码修复能力。  
参考：
- https://ollama.com/library/qwen2.5-coder
- https://ollama.com/library/qwen2.5-coder:7b

---

## 2. 确认 Ollama 已经安装

在 VSCode 的 WSL 终端里执行：

```bash
ollama --version
```

如果能显示版本号，说明 Ollama 已安装。

再确认 Ollama 服务可用：

```bash
ollama list
```

如果命令能执行，说明基本正常。

---

## 3. 下载 Qwen2.5-Coder 3B / 7B

### 下载 3B

```bash
ollama pull qwen2.5-coder:3b
```

### 下载 7B

```bash
ollama pull qwen2.5-coder:7b
```

### 测试模型能不能运行

```bash
ollama run qwen2.5-coder:3b
```

或者：

```bash
ollama run qwen2.5-coder:7b
```

出现聊天界面后，随便输入：

```text
用中文解释什么是 Python Agent
```

能回答就说明模型正常。

退出 Ollama 聊天：

```text
/bye
```

---

## 4. 安装 Aider：推荐用 pipx

Ubuntu 24 / Debian 新版本不建议直接：

```bash
pip install aider-chat
```

因为很容易报错：

```text
externally-managed-environment
```

所以推荐用 `pipx`，它会把 Aider 安装到独立环境里，比较干净。

Aider 官方安装文档也推荐用 `pipx install aider-chat`。  
参考：
- https://aider.chat/docs/install.html

---

## 5. 安装 pipx

在 WSL 终端执行：

```bash
sudo apt update
sudo apt install pipx -y
```

然后执行：

```bash
pipx ensurepath
```

执行后很重要：

```text
关闭当前 VSCode 终端，然后重新打开一个新的 WSL 终端
```

不需要重启电脑，也不一定要重启 WSL。

---

## 6. 安装 Aider

重新打开终端后执行：

```bash
pipx install aider-chat
```

检查是否安装成功：

```bash
aider --version
```

如果能看到版本号，说明成功。

如果提示 `aider: command not found`，执行：

```bash
pipx ensurepath
```

然后重新打开终端再试。

---

## 7. 配置 Ollama API 地址

Aider 官方文档推荐配置 Ollama API 地址：

```bash
export OLLAMA_API_BASE=http://127.0.0.1:11434
```

参考：
- https://aider.chat/docs/llms/ollama.html

这个命令只对当前终端有效。

如果想永久生效，写入 `~/.bashrc`：

```bash
echo 'export OLLAMA_API_BASE=http://127.0.0.1:11434' >> ~/.bashrc
source ~/.bashrc
```

确认：

```bash
echo $OLLAMA_API_BASE
```

应该输出：

```text
http://127.0.0.1:11434
```

---

## 8. 在项目目录启动 Aider

Aider 最好在 Git 项目目录里运行。

比如你的项目在：

```bash
cd ~/workspace/vscode_study/ai-lab/hello-agents-main
```

如果目录还不是 Git 仓库，可以先初始化：

```bash
git init
```

查看当前目录：

```bash
pwd
```

如果你是在一个很大的仓库里启动 Aider，不要直接让它吃完整个 repo-map。

更稳的做法是：

```bash
aider --map-tokens 0 --model ollama_chat/qwen2.5-coder:7b
```

如果你只想处理当前子目录，或者只想让 Aider 聚焦一个更小的范围，再加上：

```bash
aider --map-tokens 0 --subtree-only --model ollama_chat/qwen2.5-coder:7b
```

原则很简单：

- 大仓库先关掉 repo-map；
- 尽量只在小目录里起 Aider；
- 只把要改的少量文件加进上下文；
- 不要一开始就 `/add` 整个项目。

---

## 9. 使用 3B 启动 Aider

```bash
aider --model ollama_chat/qwen2.5-coder:3b
```

适合：

- 快速练习；
- 小文件修改；
- README 总结；
- Agent workflow 练习；
- LangChain / LangGraph 入门。

如果是在大仓库里，还可以直接用一键入口：

```bash
aiderwsl-big
```

它会默认使用大仓库模式：

- `--map-tokens 0`
- `--subtree-only`
- 默认继续使用 `ollama_chat/qwen2.5-coder:7b`

---

## 10. 使用 7B 启动 Aider

```bash
aider --model ollama_chat/qwen2.5-coder:7b
```

适合：

- 更认真地改代码；
- 多文件理解；
- 文档总结；
- Python bug 修复；
- 本地 Coding Agent 练习。

如果 7B 感觉慢，换回 3B：

```bash
aider --model ollama_chat/qwen2.5-coder:3b
```

---

## 11. 为什么用 `ollama_chat/` 而不是 `ollama/`

Aider 官方现在推荐 Ollama 使用：

```text
ollama_chat/<model-name>
```

比如：

```bash
aider --model ollama_chat/qwen2.5-coder:7b
```

参考：
- https://aider.chat/docs/llms/ollama.html

---

## 12. Aider 常用命令

进入 Aider 后，可以使用这些命令。

### 添加文件到上下文

```text
/add README.md
```

```text
/add main.py
```

### 查看当前加入的文件

```text
/ls
```

### 删除某个文件上下文

```text
/drop main.py
```

### 查看帮助

```text
/help
```

### 退出

```text
/exit
```

---

## 13. 第一次推荐练习

### 练习 1：解释项目

先添加 README：

```text
/add README.md
```

然后问：

```text
用中文解释这个项目的目录结构和运行方式
```

---

### 练习 2：让 Aider 修改一个 Python 文件

添加文件：

```text
/add main.py
```

然后说：

```text
请帮我给这个文件增加中文注释，不要改变原有逻辑
```

---

### 练习 3：写一个 Calculator Agent

你可以新建一个文件：

```bash
touch calculator_agent.py
```

进入 Aider 后：

```text
/add calculator_agent.py
```

然后输入：

```text
请用 Python 写一个最小版 ReAct 风格 Calculator Agent。要求：
1. 有 add/subtract/multiply/divide 四个工具函数
2. 用户输入自然语言问题
3. 模型决定调用哪个工具
4. 工具执行后输出最终答案
5. 代码尽量简单，适合初学者学习
```

---

## 14. 推荐建立 `.aider.conf.yml`

如果你每次都不想输入模型参数，可以在项目根目录创建：

```bash
touch .aider.conf.yml
```

写入 3B 配置：

```yaml
model: ollama_chat/qwen2.5-coder:3b
auto-commits: false
show-diffs: true
```

以后在项目目录里直接执行：

```bash
aider
```

如果想改成 7B：

```yaml
model: ollama_chat/qwen2.5-coder:7b
auto-commits: false
show-diffs: true
```

---

## 15. 推荐工作流

### 小任务

```bash
aider --model ollama_chat/qwen2.5-coder:3b
```

适合：

```text
解释代码、写小函数、总结文档、练习 Agent 结构
```

### 中等任务

```bash
aider --model ollama_chat/qwen2.5-coder:7b
```

适合：

```text
多文件修改、复杂 Python、文档整理、代码重构
```

### 复杂任务

建议以后用：

```text
NVIDIA NIM / Codex CLI / 更强云端模型
```

本地 7B 虽然能用，但长上下文和复杂推理还是有限。

---

## 16. 常见错误处理

### 错误 1：`externally-managed-environment`

原因：Ubuntu / Debian 不允许直接用 pip 往系统 Python 里装包。

解决：用 pipx。

```bash
sudo apt install pipx -y
pipx ensurepath
pipx install aider-chat
```

---

### 错误 2：`aider: command not found`

执行：

```bash
pipx ensurepath
```

然后关闭 VSCode 当前终端，重新打开一个终端。

再试：

```bash
aider --version
```

---

### 错误 3：Aider 连不上 Ollama

检查 Ollama：

```bash
ollama list
```

设置 API：

```bash
export OLLAMA_API_BASE=http://127.0.0.1:11434
```

再启动：

```bash
aider --model ollama_chat/qwen2.5-coder:3b
```

---

### 错误 4：7B 太慢

换 3B：

```bash
aider --model ollama_chat/qwen2.5-coder:3b
```

或者减少加入上下文的文件数量。

不要一开始就 `/add` 整个项目。

---

### 错误 5：模型乱改代码

建议：

1. 一次只添加 1～3 个相关文件；
2. 指令写清楚；
3. 先让它解释，再让它修改；
4. 开启 `show-diffs: true`；
5. 修改前先 `git status`。

---

## 17. VSCode 中推荐使用方式

在 VSCode WSL 中：

1. 左边打开项目目录；
2. 下方打开终端；
3. 进入项目目录；
4. 运行 Aider；
5. 让 Aider 修改文件；
6. 在 VSCode 编辑器里查看 diff 和文件变化。

推荐命令：

```bash
cd ~/workspace/vscode_study/ai-lab/hello-agents-main
aider --model ollama_chat/qwen2.5-coder:7b
```

---

## 18. 最推荐你的最终配置

如果你的电脑跑 7B 可以接受，推荐 `.aider.conf.yml`：

```yaml
model: ollama_chat/qwen2.5-coder:7b
auto-commits: false
show-diffs: true
```

如果想更快，推荐：

```yaml
model: ollama_chat/qwen2.5-coder:3b
auto-commits: false
show-diffs: true
```

---

## 19. 最后建议

你现在不要把时间都花在比较工具上。

最有效的学习路线是：

```text
Aider + Qwen3B/7B
    ↓
练文件修改
    ↓
练 Tool Calling
    ↓
练 LangChain
    ↓
练 LangGraph
    ↓
再接 NVIDIA NIM 做复杂 Agent
```

本地模型最适合高频练习：不花钱、不消耗 ChatGPT Plus / Codex 额度、不怕试错。

---

## 参考资料

- Aider 安装文档：https://aider.chat/docs/install.html
- Aider Ollama 文档：https://aider.chat/docs/llms/ollama.html
- Ollama Qwen2.5-Coder：https://ollama.com/library/qwen2.5-coder
- Ollama Qwen2.5-Coder 7B：https://ollama.com/library/qwen2.5-coder:7b
