# VSCode + Aider + Ollama + Qwen 本地 AI 编程完整教程

> **零费用、零数据泄露、离线可用。** 本教程教你在本机搭建一套完全私有的 AI 辅助编程环境：Ollama 负责运行本地大模型，Aider 负责与模型协作修改代码，VSCode 作为开发主界面。

---

## 目录

1. [方案架构与优势](#1-方案架构与优势)
2. [硬件要求 & 模型选型](#2-硬件要求--模型选型)
3. [安装 Ollama](#3-安装-ollama)
4. [下载 Qwen 模型](#4-下载-qwen-模型)
5. [安装 Aider](#5-安装-aider)
6. [连接 Aider 与 Ollama](#6-连接-aider-与-ollama)
7. [在 VSCode 中启动并使用](#7-在-vscode-中启动并使用)
8. [常用 Aider 命令速查](#8-常用-aider-命令速查)
9. [推荐工作流实战](#9-推荐工作流实战)
10. [配置文件（一劳永逸）](#10-配置文件一劳永逸)
11. [性能调优](#11-性能调优)
12. [常见问题排查](#12-常见问题排查)

---

## 1. 方案架构与优势

```
┌─────────────────────────────────────────────┐
│                  VSCode                      │
│  ┌────────────────┐   ┌──────────────────┐  │
│  │  编辑器 / 文件  │   │   集成终端        │  │
│  │  实时查看变更   │   │  运行 Aider CLI   │  │
│  └────────────────┘   └────────┬─────────┘  │
└───────────────────────────────┼─────────────┘
                                │ 对话 + 代码修改
                                ▼
                    ┌─────────────────────┐
                    │       Aider         │
                    │  AI 编程助手 CLI     │
                    │  自动读写文件        │
                    │  自动 Git 提交       │
                    └──────────┬──────────┘
                               │ OpenAI 兼容 API
                               ▼
                    ┌─────────────────────┐
                    │       Ollama        │
                    │  本地模型运行时      │
                    │  http://localhost   │
                    │       :11434        │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │    Qwen 本地模型     │
                    │  qwen2.5-coder:7b   │
                    │  qwen3:8b  等       │
                    └─────────────────────┘
```

**核心优势：**

- 🆓 **完全免费**：无 API 费用，下载一次永久使用
- 🔒 **数据安全**：代码不离开本机，适合涉密项目
- 🌐 **无需翻墙**：不依赖任何境外服务
- ✈️ **离线可用**：模型下载后断网仍可工作

---

## 2. 硬件要求 & 模型选型

### 内存 / 显存对照表

| 你的设备 | 推荐模型 | 下载大小 | 编程能力 |
|---------|---------|---------|---------|
| 8GB RAM（无独显） | `qwen2.5-coder:7b` | ~4.7 GB | 基础够用 |
| 16GB RAM 或 8GB VRAM | `qwen2.5-coder:14b` | ~9 GB | 较强 |
| 16GB VRAM / Apple M系列 | `qwen3:8b` | ~5.2 GB | 推理+编程 |
| 32GB RAM 或 24GB VRAM | `qwen2.5-coder:32b` | ~20 GB | 强 |
| 大内存服务器（250GB+） | `qwen3-coder` | ~480 GB | 旗舰级 |

### 模型选择建议

**新手 / 低配机器 → `qwen2.5-coder:7b`**
代码专用模型，7B 参数在 8GB 内存上流畅运行，CPU 推理速度约 3-10 token/s。

**日常开发首选 → `qwen2.5-coder:14b`**
性价比最高，16GB 内存可顺畅运行，编程能力较强。

**Apple Silicon Mac → `qwen3:8b`**
Ollama 在 M 系列芯片上自动使用 Metal 加速，统一内存架构效率高，速度优于同配置 PC。

**追求最强本地模型 → `qwen3-coder:30b`（MoE）**
30B 总参数但只激活约 3.3B，效率较高，需 32GB+ 内存。

---

## 3. 安装 Ollama

### macOS

```bash
# 方式一：官网下载（推荐）
# 前往 https://ollama.com 下载 .dmg 安装包

# 方式二：Homebrew
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

前往 https://ollama.com 下载 .exe 安装包，双击安装。

> Windows 用户也可以通过 WSL2 安装 Linux 版本，GPU 加速更好。

### 验证安装

```bash
ollama --version
# 输出：ollama version is 0.x.x

# 确认服务正在运行
curl http://localhost:11434
# 输出：Ollama is running
```

Ollama 安装后会在后台自动运行。如果没有，手动启动：

```bash
ollama serve
```

---

## 4. 下载 Qwen 模型

根据你的硬件，选择对应命令（可下载多个）：

```bash
# 【推荐入门】8GB 内存可用，代码专用
ollama pull qwen2.5-coder:7b

# 【日常主力】16GB 内存，更强编程能力
ollama pull qwen2.5-coder:14b

# 【推理增强】支持思维模式，适合复杂逻辑
ollama pull qwen3:8b

# 【旗舰本地】需 32GB+ 内存
ollama pull qwen2.5-coder:32b
```

下载进度示例：

```
pulling manifest
pulling 1234abcd...  ████████████████  4.7 GB  25 MB/s  3m14s
verifying sha256 digest
writing manifest
success
```

> 国内下载较慢属正常现象（模型文件大），建议夜间下载或使用有线网络。

### 查看已下载的模型

```bash
ollama list
```

输出示例：

```
NAME                         ID              SIZE    MODIFIED
qwen2.5-coder:7b             abc123def456    4.7 GB  2 minutes ago
qwen2.5-coder:14b            xyz789abc012    9.0 GB  1 hour ago
```

### 测试模型是否正常工作

```bash
ollama run qwen2.5-coder:7b
# 进入交互模式
>>> 用 Python 写一个冒泡排序函数
# 看到代码输出即代表工作正常
>>> /bye
```

---

## 5. 安装 Aider

### 方式一：pip 安装

```bash
pip install aider-chat
```

### 方式二：pipx 安装（推荐，环境隔离）

```bash
pip install pipx
pipx ensurepath
pipx install aider-chat
```

### 方式三：uv 安装（最快）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install aider-chat
```

### 验证

```bash
aider --version
# 输出：aider 0.xx.x
```

---

## 6. 连接 Aider 与 Ollama

Aider 通过 OpenAI 兼容 API 接入 Ollama，只需设置一个环境变量。

### macOS / Linux

```bash
export OLLAMA_API_BASE=http://127.0.0.1:11434
```

写入配置文件永久生效：

```bash
echo 'export OLLAMA_API_BASE=http://127.0.0.1:11434' >> ~/.zshrc
source ~/.zshrc
# 或 bash 用户
echo 'export OLLAMA_API_BASE=http://127.0.0.1:11434' >> ~/.bashrc
source ~/.bashrc
```

### Windows PowerShell

```powershell
$env:OLLAMA_API_BASE = "http://127.0.0.1:11434"
```

永久生效（写入系统环境变量，需重开终端）：

```powershell
setx OLLAMA_API_BASE "http://127.0.0.1:11434"
```

### Windows CMD

```cmd
set OLLAMA_API_BASE=http://127.0.0.1:11434
```

### 验证连接

```bash
curl http://127.0.0.1:11434/api/tags
# 返回已下载模型列表的 JSON
```

---

## 7. 在 VSCode 中启动并使用

### 第一步：打开终端

按 Ctrl+`（Windows/Linux）或 Cmd+`（macOS）打开 VSCode 集成终端。

### 第二步：进入项目目录（必须是 Git 仓库）

```bash
cd /path/to/your/project

# 如果还没有初始化 Git
git init
git add .
git commit -m "init"
```

### 第三步：启动 Aider

```bash
# 使用 qwen2.5-coder:7b（注意模型前缀是 ollama_chat/）
aider --model ollama_chat/qwen2.5-coder:7b

# 使用 14b 版本
aider --model ollama_chat/qwen2.5-coder:14b

# 使用 qwen3
aider --model ollama_chat/qwen3:8b

# 启动时直接加载文件
aider --model ollama_chat/qwen2.5-coder:7b src/main.py src/utils.py
```

> 注意：接入 Ollama 的模型名前缀必须是 `ollama_chat/`，不是 `ollama/`。

### 第四步：开始使用

启动成功后会看到：

```
─────────────────────────────────────────────
Aider v0.xx.x
Model: ollama_chat/qwen2.5-coder:7b with ollama_chat edit format
Git repo: /your/project/.git
Repo-map: using 1024 tokens
─────────────────────────────────────────────
>
```

### 基本操作流程

```
# 1. 添加要编辑的文件
> /add src/main.py

# 2. 用中文描述你的需求
> 在 main.py 里添加一个函数，读取 CSV 文件并返回 DataFrame，要处理编码问题

# 3. Aider 生成代码后会问你是否应用
Apply this change? (y/n/d/e/a)
# 输入 y 确认，n 拒绝，d 查看详细 diff

# 4. 满意后代码自动写入文件并 Git 提交
```

---

## 8. 常用 Aider 命令速查

| 命令 | 说明 |
|------|------|
| `/add <文件>` | 添加文件到可编辑上下文 |
| `/drop <文件>` | 从上下文中移除文件 |
| `/read-only <文件>` | 添加只读参考文件（AI 可读但不改） |
| `/ls` | 列出当前上下文中的文件 |
| `/diff` | 查看本次所有变更 |
| `/undo` | 撤销上一次 AI 提交 |
| `/clear` | 清空对话历史（保留文件） |
| `/reset` | 完全重置 |
| `/run <命令>` | 执行 shell 命令并把输出给 AI 参考 |
| `/ask <问题>` | 只问问题，不修改代码 |
| `/model <模型名>` | 切换模型（无需重启） |
| `/help` | 查看帮助 |
| `/exit` | 退出 |

---

## 9. 推荐工作流实战

### 工作流一：修复 Bug

```
# 启动
aider --model ollama_chat/qwen2.5-coder:7b

# 添加相关文件
> /add src/api.py tests/test_api.py

# 描述问题（可直接粘贴错误信息）
> 运行 pytest 时出现以下错误，帮我定位并修复：
  FAILED tests/test_api.py::test_get_user - AssertionError: 404 != 200

# 让 AI 运行测试验证修复结果
> /run pytest tests/test_api.py -v
```

### 工作流二：添加新功能

```
# 添加文件
> /add src/models.py src/routes.py

# 参考文档（只读）
> /read-only docs/api-design.md

# 描述功能
> 参考 docs/api-design.md 中的接口规范，
  在 routes.py 里添加 POST /users/{id}/avatar 接口，
  支持上传图片，限制 2MB 以内，保存到 uploads/ 目录
```

### 工作流三：代码重构

```
# 先只读理解旧代码
> /read-only src/legacy/data_processor.py

# 添加要写入的新文件
> /add src/core/processor.py

# 描述重构目标
> 参考 legacy/data_processor.py 中的 process() 函数逻辑，
  在 core/processor.py 中用现代 Python 重写：
  - 使用 dataclass 替代 dict
  - 添加完整类型注解
  - 添加错误处理
  - 附带 docstring
```

### 工作流四：只问问题，不改代码

```
> /ask 解释一下 main.py 中 connection_pool 的实现原理，
       有没有潜在的线程安全问题？

> /ask 这段代码的时间复杂度是多少，有没有优化空间？
```

### 工作流五：生成单元测试

```
> /read-only src/utils.py
> /add tests/test_utils.py

> 为 utils.py 中的每个公开函数编写单元测试，
  使用 pytest 风格，覆盖正常情况和边界情况
```

---

## 10. 配置文件（一劳永逸）

在项目根目录创建 `.aider.conf.yml`：

```yaml
# .aider.conf.yml

# 默认模型（改成你常用的）
model: ollama_chat/qwen2.5-coder:7b

# 深色主题
dark-mode: true

# 自动提交（保持 true，方便 /undo 回滚）
auto-commits: true

# 不发送匿名使用数据
analytics: false
```

创建后，直接运行 `aider` 即可，无需额外参数。

### 让 AI 默认用中文回复

在项目根目录创建 `.aider.system.md`：

```markdown
请始终用中文与用户交流，包括解释代码修改原因、提问确认、报错分析等。
代码本身（变量名、注释等）保持原有语言风格，不要强行改成中文。
```

### VSCode 任务快捷启动

在 `.vscode/tasks.json` 中添加：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "启动 Aider qwen2.5-coder 7b",
      "type": "shell",
      "command": "aider --model ollama_chat/qwen2.5-coder:7b",
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "presentation": {
        "reveal": "always",
        "panel": "new",
        "focus": true
      }
    },
    {
      "label": "启动 Aider qwen2.5-coder 14b",
      "type": "shell",
      "command": "aider --model ollama_chat/qwen2.5-coder:14b",
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "presentation": {
        "reveal": "always",
        "panel": "new",
        "focus": true
      }
    }
  ]
}
```

之后通过 Ctrl+Shift+P → Tasks: Run Task 一键启动。

---

## 11. 性能调优

### 检查 GPU 是否被使用

```bash
# NVIDIA 显卡
nvidia-smi
# 运行 Aider 时观察 GPU 利用率是否上升

# Apple Silicon（自动使用 Metal，无需额外配置）
```

### 增大上下文窗口

默认上下文较小，可通过自定义 Modelfile 扩大：

```bash
cat > Modelfile << 'EOF'
FROM qwen2.5-coder:7b
PARAMETER num_ctx 8192
EOF

ollama create qwen2.5-coder-ctx8k -f Modelfile

aider --model ollama_chat/qwen2.5-coder-ctx8k
```

### 保持模型常驻内存

Ollama 空闲一段时间会自动卸载模型，下次请求需重新加载（约 5-30 秒）。

```bash
export OLLAMA_KEEP_ALIVE=-1
```

或运行时直接指定：

```bash
ollama run qwen2.5-coder:7b --keepalive -1
```

---

## 12. 常见问题排查

### Q: 启动 Aider 时提示 Connection refused？

Ollama 服务未启动：

```bash
ollama serve
```

确认服务状态：

```bash
curl http://localhost:11434
# 应返回 "Ollama is running"
```

### Q: Aider 找不到模型？

确认模型名称完全一致：

```bash
ollama list
# 使用与列表中完全一致的名称
aider --model ollama_chat/qwen2.5-coder:7b
```

### Q: 提示 not a git repository？

```bash
git init
git add .
git commit -m "init"
```

### Q: 响应很慢（CPU 推理）？

CPU 推理速度约 3-10 token/s 属正常现象。可以换用更小模型，或在有独立显卡的设备上运行。

### Q: 想撤销 AI 的修改？

```
/undo
```

可连续执行撤销多次提交。

### Q: AI 把不该改的文件也改了？

先 `/undo` 撤销，下次改用 `/read-only` 而非 `/add` 引用那些文件。

### Q: 对话太长导致 AI 失忆？

```
/clear
```

或完全重置：

```
/reset
/add src/main.py
```

### Q: 模型回复质量差？

切换到更大的模型：

```
/model ollama_chat/qwen2.5-coder:14b
```

并在提示词中更明确地说明语言、框架版本和输入输出预期。

---

## 附录：完整启动脚本

保存为 `start-aider.sh`（macOS / Linux）：

```bash
#!/bin/bash

if ! curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "启动 Ollama..."
    ollama serve &
    sleep 3
fi

export OLLAMA_API_BASE=http://127.0.0.1:11434

MODEL=${1:-"qwen2.5-coder:7b"}

echo "启动 Aider，模型：$MODEL"
aider --model "ollama_chat/$MODEL" --dark-mode
```

```bash
chmod +x start-aider.sh

./start-aider.sh                      # 使用默认 7b 模型
./start-aider.sh qwen2.5-coder:14b   # 使用 14b 模型
./start-aider.sh qwen3:8b            # 使用 qwen3
```

---

## 模型对比速查

| 模型 | 参数量 | 内存需求 | CPU 速度 | 编程能力 | 推荐场景 |
|------|--------|---------|---------|---------|---------|
| qwen2.5-coder:7b | 7B | 8GB | 中等 | 入门够用 | 入门、低配机 |
| qwen2.5-coder:14b | 14B | 16GB | 较慢 | 较强 | 日常主力 |
| qwen3:8b | 8B | 10GB | 中等 | 推理增强 | 需要思维链 |
| qwen2.5-coder:32b | 32B | 32GB | 慢 | 很强 | 高配机 / 有 GPU |
| qwen3-coder:30b | 30B MoE | 32GB | 较慢 | 最强本地编程 | 旗舰本地方案 |

---

文档版本：2026年6月 | 基于 Ollama 0.5.x、Aider 最新版、Qwen 系列模型整理
