# 在 VSCode 中使用 Aider 完全教程

> Aider 是一款强大的 AI 辅助编程工具，可在终端中与 Claude、GPT-4 等大模型协作修改代码。本教程帮助你在 VSCode 环境中高效使用 Aider。

---

## 目录

1. [环境准备](#1-环境准备)
2. [安装 Aider](#2-安装-aider)
3. [配置 API Key](#3-配置-api-key)
4. [在 VSCode 终端中启动 Aider](#4-在-vscode-终端中启动-aider)
5. [基本使用方法](#5-基本使用方法)
6. [常用命令速查](#6-常用命令速查)
7. [推荐工作流](#7-推荐工作流)
8. [VSCode 集成技巧](#8-vscode-集成技巧)
9. [配置文件详解](#9-配置文件详解)
10. [常见问题](#10-常见问题)

---

## 1. 环境准备

### 系统要求

- Python 3.9 或更高版本
- Git（已初始化仓库）
- VSCode（建议最新版）

### 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

如果未安装 Python，前往 [python.org](https://www.python.org/downloads/) 下载安装。

### 确认 Git 已初始化

Aider 需要在 Git 仓库中运行，它会自动提交每次修改：

```bash
# 进入你的项目目录
cd your-project

# 初始化 Git（如果还没有）
git init
```

---

## 2. 安装 Aider

### 方式一：pip 安装（推荐）

```bash
pip install aider-chat
```

### 方式二：pipx 安装（隔离环境，更干净）

```bash
# 先安装 pipx
pip install pipx
pipx ensurepath

# 再安装 aider
pipx install aider-chat
```

### 方式三：uv 安装（速度最快）

```bash
# 先安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 aider
uv tool install aider-chat
```

### 验证安装

```bash
aider --version
```

---

## 3. 配置 API Key

Aider 支持多种模型，最常用的是 Claude 和 OpenAI。

### 使用 Claude（Anthropic）

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxx"

# Windows CMD
set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

获取 API Key：前往 [console.anthropic.com](https://console.anthropic.com/)

### 使用 OpenAI

```bash
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 永久保存 API Key

将环境变量写入 shell 配置文件（推荐）：

```bash
# ~/.bashrc 或 ~/.zshrc
echo 'export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx' >> ~/.zshrc
source ~/.zshrc
```

或者使用 `.env` 文件（在项目根目录）：

```
# .env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

> ⚠️ 注意：`.env` 文件不要提交到 Git，记得加入 `.gitignore`。

---

## 4. 在 VSCode 终端中启动 Aider

### 打开集成终端

按 `` Ctrl+` ``（Windows/Linux）或 `` Cmd+` ``（macOS）打开 VSCode 内置终端。

### 基本启动命令

```bash
# 使用 Claude Sonnet（推荐，性价比高）
aider --model claude-sonnet-4-5

# 使用 Claude Opus（最强，但更贵）
aider --model claude-opus-4-5

# 使用 GPT-4o
aider --model gpt-4o

# 启动时直接指定要编辑的文件
aider src/main.py src/utils.py
```

### 启动后的界面

```
─────────────────────────────────────────
Aider v0.xx.x
Model: claude-sonnet-4-5
Git repo: /your/project/.git
Repo-map: using 1024 tokens
─────────────────────────────────────────
> 
```

看到 `>` 提示符就说明 Aider 已就绪，可以开始输入指令了。

---

## 5. 基本使用方法

### 5.1 添加文件到上下文

Aider 需要知道你想修改哪些文件：

```
# 在 Aider 提示符中输入
/add src/main.py
/add src/utils.py src/config.py   # 一次添加多个
/add src/                          # 添加整个目录
```

### 5.2 直接描述需求

添加文件后，用自然语言描述你想做的事：

```
> 在 main.py 中添加一个函数，接收用户名列表，返回去重后按字母排序的结果

> 帮我给 utils.py 中的所有函数添加类型注解

> 把 config.py 中的硬编码字符串都改成从环境变量读取
```

Aider 会：
1. 分析你的需求
2. 生成修改方案
3. 显示 diff 供你确认
4. 自动写入文件并提交到 Git

### 5.3 确认或拒绝修改

Aider 显示修改内容后，会询问是否应用：

```
Apply this change? (y/n/d/e/a)
y - 应用修改
n - 拒绝修改
d - 查看详细 diff
e - 在编辑器中打开文件
a - 全部应用（多文件时）
```

### 5.4 只读模式查看文件

有些文件你只想让 AI 参考，不想让它修改：

```
/read-only docs/api-spec.md
/read-only README.md
```

### 5.5 查看当前上下文中的文件

```
/ls
```

---

## 6. 常用命令速查

| 命令 | 说明 |
|------|------|
| `/add <file>` | 添加文件到可编辑上下文 |
| `/drop <file>` | 从上下文中移除文件 |
| `/read-only <file>` | 添加只读参考文件 |
| `/ls` | 列出当前上下文中的所有文件 |
| `/diff` | 查看自上次提交以来的所有变更 |
| `/undo` | 撤销上一次 AI 提交 |
| `/commit` | 手动提交当前变更 |
| `/clear` | 清空对话历史 |
| `/reset` | 重置上下文和对话 |
| `/run <cmd>` | 在 shell 中运行命令并将输出给 AI 参考 |
| `/test` | 运行测试命令（需配置） |
| `/ask <question>` | 提问但不修改代码 |
| `/help` | 查看帮助 |
| `/exit` 或 `/quit` | 退出 Aider |

---

## 7. 推荐工作流

### 工作流一：修复 Bug

```bash
# 1. 启动 Aider
aider --model claude-sonnet-4-5

# 2. 添加相关文件
/add src/auth.py tests/test_auth.py

# 3. 描述问题
> 运行测试时 test_login_with_invalid_password 失败，
  错误信息是 AssertionError: 200 != 401，
  请帮我找到问题并修复

# 4. 让 AI 运行测试验证
/run pytest tests/test_auth.py -v
```

### 工作流二：添加新功能

```bash
# 1. 启动并指定文件
aider src/api.py src/models.py

# 2. 描述功能需求
> 参考现有的 /users 接口风格，
  在 api.py 中添加一个 /users/{id}/posts 接口，
  返回该用户的所有帖子（分页，默认每页20条）

# 3. 查看修改
/diff

# 4. 如果满意则提交
/commit "feat: add user posts endpoint with pagination"
```

### 工作流三：代码重构

```bash
# 1. 先只读理解代码
/read-only src/legacy_utils.py

# 2. 添加要修改的文件
/add src/new_module.py

# 3. 描述重构目标
> 参考 legacy_utils.py 中的 process_data 函数，
  在 new_module.py 中用更现代的 Python 风格重写，
  使用 dataclass、类型注解，并添加单元测试

# 4. 确认后撤销（如果不满意）
/undo
```

### 工作流四：代码审查模式

```bash
# 只提问，不修改代码
> /ask 解释一下 main.py 中 process_queue 函数的工作原理，
  有没有潜在的并发问题？
```

---

## 8. VSCode 集成技巧

### 技巧一：分屏使用

1. 在 VSCode 中打开你的代码文件
2. 按 `` Ctrl+` `` 打开终端
3. 在终端中启动 Aider
4. 左侧看代码，右侧（终端）与 AI 对话

### 技巧二：使用多个终端标签

VSCode 支持多个终端标签：
- 终端1：运行 Aider
- 终端2：运行服务器/测试
- 终端3：执行 git 命令

点击终端面板右上角的 `+` 新建终端标签。

### 技巧三：配置 VSCode 任务

在 `.vscode/tasks.json` 中添加快速启动任务：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Aider (Claude Sonnet)",
      "type": "shell",
      "command": "aider --model claude-sonnet-4-5",
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

通过 `Ctrl+Shift+P` → `Tasks: Run Task` → `Start Aider` 一键启动。

### 技巧四：使用 VSCode Git 面板配合

Aider 会自动 Git 提交，你可以在 VSCode 的源代码管理面板（`Ctrl+Shift+G`）中：
- 查看每次 AI 的修改记录
- 对比文件变更
- 一键撤销某次提交

### 技巧五：Aider 完成修改后立即在编辑器看效果

Aider 修改文件后，VSCode 会自动检测到文件变化并刷新，无需手动重新打开文件。

---

## 9. 配置文件详解

在项目根目录创建 `.aider.conf.yml` 文件，避免每次手动输入参数：

```yaml
# .aider.conf.yml

# 默认使用的模型
model: claude-sonnet-4-5

# 自动提交（默认开启，设为 false 可手动控制）
auto-commits: true

# 提交信息前缀
commit-prompt: "简洁描述这次修改做了什么（用中文）"

# 是否显示 diff 确认
auto-accept-architect: false

# 默认添加到上下文的文件（项目启动时自动加载）
# read-only-files:
#   - README.md
#   - docs/architecture.md

# 使用深色主题
dark-mode: true

# 代码修改后自动运行的测试命令
# test-cmd: pytest

# 语言提示（让 AI 用中文回复）
# system-prompt: "请用中文回复"
```

### 让 AI 默认用中文回复

创建 `.aider.system.md` 文件：

```markdown
请始终用中文回复用户，包括解释修改原因、提问等。
代码注释可以用英文，但对话内容请用中文。
```

---

## 10. 常见问题

### Q: Aider 说找不到 API Key？

确认环境变量已设置：

```bash
echo $ANTHROPIC_API_KEY   # macOS/Linux
echo $env:ANTHROPIC_API_KEY  # Windows PowerShell
```

如果为空，重新设置并重启终端。

### Q: 提示 "not a git repository"？

```bash
git init
git add .
git commit -m "initial commit"
```

然后重新启动 Aider。

### Q: 想撤销 AI 刚才做的修改？

```
/undo
```

这会撤销最近一次 Aider 的 Git 提交。

### Q: AI 修改了不该动的文件？

1. 使用 `/undo` 撤销
2. 下次用 `/read-only` 而不是 `/add` 来引用那些文件

### Q: 上下文窗口太长，AI 开始"忘事"？

```
/clear      # 清空对话历史（保留文件上下文）
/reset      # 完全重置（清空所有）
```

重新添加文件和核心需求。

### Q: 如何让 Aider 只解释代码，不修改？

```
/ask 解释一下这段代码的作用
```

或者在问题前加 "只解释，不要修改代码："

### Q: 网络问题导致请求失败？

配置代理：

```bash
export HTTPS_PROXY=http://127.0.0.1:7890
aider --model claude-sonnet-4-5
```

---

## 附录：实用启动脚本

在项目根目录创建 `start-aider.sh`（macOS/Linux）：

```bash
#!/bin/bash
echo "🚀 启动 Aider..."
export ANTHROPIC_API_KEY=$(cat ~/.anthropic_key 2>/dev/null || echo $ANTHROPIC_API_KEY)
aider \
  --model claude-sonnet-4-5 \
  --dark-mode \
  "$@"
```

```bash
chmod +x start-aider.sh
./start-aider.sh                    # 普通启动
./start-aider.sh src/main.py       # 启动时加载文件
```

---

*文档版本：2025年 | 基于 Aider 最新稳定版编写*
