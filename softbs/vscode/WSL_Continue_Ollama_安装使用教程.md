# UM890 Pro：VS Code + WSL + Continue + Ollama 本地 AI 编程教程

> **推荐方案**：VS Code + WSL + **Continue** + Ollama  
> **机器**：Minisforum UM890 Pro（Ryzen 9 8945HS / 32GB / 核显）  
> **默认模型**：`qwen2.5-coder:3b`  
> **特点**：免费、稳定、数据不出本机，不依赖 GitHub Copilot 订阅  

---

## 快速跳转

- [1. 方案说明](#sec-1)
- [2. UM890 Pro 环境前提](#sec-2)
- [3. WSL 内安装 Ollama](#sec-3)
- [4. 拉取并测试 qwen2.5-coder:3b](#sec-4)
- [5. 安装 Continue 扩展](#sec-5)
- [6. Continue 配置 config.yaml](#sec-6)
- [7. 日常使用](#sec-7)
- [8. 模型选择建议](#sec-8)
- [9. 常见问题排查](#sec-9)
- [10. 与 Aider 配合（可选）](#sec-10)
- [11. 相关文档](#sec-11)

---

<a id="sec-1"></a>

## 1. 方案说明

### 1.1 为什么用 Continue，而不是 Copilot Chat

| 对比项 | VS Code + WSL + Continue + Ollama | GitHub Copilot + Ollama |
| --- | --- | --- |
| 费用 | **完全免费** | 需登录 GitHub；部分能力要订阅 |
| 本地模型 | 原生支持 Ollama | 需 Language Models 配置，限制较多 |
| 配置 | `~/.continue/config.yaml`，可控 | 依赖 Copilot 版本与 Local 开关 |
| 适合 UM890 | **3B 模型即可稳定聊天改码** | Agent 对 3B 支持较弱 |

一句话：

`Ollama 提供本地模型 API，Continue 是 VS Code 里的免费 AI 助手，通过 config.yaml 直连 Ollama。`

### 1.2 整体架构

```text
Windows 11
  └── VS Code（Remote - WSL）
        └── Continue 扩展
              └── ~/.continue/config.yaml
                    └── provider: ollama
                          └── http://localhost:11434
                                └── WSL Ubuntu 内的 Ollama
                                      └── qwen2.5-coder:3b
```

### 1.3 本教程固定组合

- **Ollama 装在 WSL Ubuntu 内**（与 Java / Python / Git 同环境）
- **Continue 扩展装在 WSL: Ubuntu 侧**
- **配置文件路径**：`~/.continue/config.yaml`（WSL 内即 `/home/你的用户名/.continue/config.yaml`）

---

<a id="sec-2"></a>

## 2. UM890 Pro 环境前提

### 2.1 硬件

| 项目 | 规格 | 说明 |
| --- | --- | --- |
| CPU | Ryzen 9 8945HS | Ollama 主要靠 CPU 推理 |
| 内存 | 32GB | 开发 + 3B 模型可并行，需控制 WSL 配额 |
| 显卡 | Radeon 780M 核显 | 无 NVIDIA；不要装 CUDA 驱动教程 |

### 2.2 为什么默认 `qwen2.5-coder:3b`

- 加载约 **2～3GB**，边写 Java/Python 边聊天不易卡死
- Continue 的 **Chat / Edit** 足够应付解释代码、小改片段
- UM890 上 **Tab 自动补全**若也用 3B 会偏慢，本教程默认先关自动补全（见第 6 节）

### 2.3 WSL 内存配置（32GB 机器）

编辑 Windows `%UserProfile%\.wslconfig`：

```ini
[wsl2]
memory=20GB
processors=8
swap=8GB
sparseVhd=true
```

保存后 PowerShell 执行：

```powershell
wsl --shutdown
wsl -d Ubuntu
```

### 2.4 确认 VS Code 已连 WSL

1. `Ctrl+Shift+P` → `Remote-WSL: New Window`
2. 打开 `~/workspace/vscode_study`
3. 左下角显示 **`WSL: Ubuntu`**

更多 WSL 入门见 [Win11_WSL_VSCode_Java_Python_快速开发指南.md](Win11_WSL_VSCode_Java_Python_快速开发指南.md)。

---

<a id="sec-3"></a>

## 3. WSL 内安装 Ollama

### 3.1 启用 systemd（推荐）

```bash
sudo nano /etc/wsl.conf
```

写入：

```ini
[boot]
systemd=true
```

Windows PowerShell 执行 `wsl --shutdown` 后重新进入 WSL。

验证：

```bash
systemctl --version
```

### 3.2 安装 Ollama

```bash
sudo apt update
sudo apt install -y curl zstd
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

### 3.3 启动 Ollama 服务

**方式 A：systemd 后台服务（日常推荐）**

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

**方式 B：前台手动启动（调试用）**

```bash
ollama serve
```

保持该终端不关。Continue 连接前必须保证 `11434` 端口可用。

### 3.4 验证 API

```bash
curl http://127.0.0.1:11434
curl http://127.0.0.1:11434/api/tags
```

第一条应返回 `Ollama is running` 类文本；第二条返回 JSON（初次可能 `models: []`）。

---

<a id="sec-4"></a>

## 4. 拉取并测试 qwen2.5-coder:3b

### 4.1 下载模型

```bash
ollama pull qwen2.5-coder:3b
ollama list
```

### 4.2 命令行试跑

```bash
ollama run qwen2.5-coder:3b
```

测试提示：

```text
用 Java 写一个简单的 Spring Boot REST Controller，GET /hello 返回 hello。只给代码。
```

UM890 CPU 推理下 **30 秒～2 分钟** 开始输出属正常。输入 `/bye` 退出。

### 4.3 确认模型在内存中（可选）

另开终端：

```bash
ollama ps
free -h
```

---

<a id="sec-5"></a>

## 5. 安装 Continue 扩展

### 5.1 在 WSL 侧安装

1. 确认 VS Code 左下角为 **`WSL: Ubuntu`**
2. `Ctrl+Shift+X` 打开扩展
3. 搜索 **`Continue`**
4. 作者：**Continue.dev**
5. 扩展 ID：`Continue.continue`
6. 点击 **Install in WSL: Ubuntu**（确保装在 WSL，不是仅 Windows 本地）

同时建议已安装：

| 扩展 | ID |
| --- | --- |
| Remote - WSL | `ms-vscode-remote.remote-wsl` |

### 5.2 首次打开 Continue

安装后左侧活动栏会出现 **Continue 图标**，或：

- 快捷键 **`Ctrl+L`**（聚焦 Continue 输入框，以你本机键位为准）
- `Ctrl+Shift+P` → **`Continue: Focus on Continue Input`**

首次使用可能提示创建配置，选 **Local / Ollama** 或 **Open config.yaml** 即可。

---

<a id="sec-6"></a>

## 6. Continue 配置 config.yaml

### 6.1 打开配置文件

在 VS Code（WSL 窗口）中：

```text
Ctrl+Shift+P → Continue: Open Config
```

文件路径：

```text
~/.continue/config.yaml
```

即 WSL 内：

```text
/home/你的用户名/.continue/config.yaml
```

### 6.2 UM890 Pro 推荐配置（单模型 3B）

将下面内容 **完整替换** 为 `config.yaml`（可按需改 `name`）：

```yaml
name: UM890 Continue + Ollama
version: 0.0.1
schema: v1

models:
  # 聊天、解释代码、Edit 改码
  - name: Qwen2.5-Coder 3B
    provider: ollama
    model: qwen2.5-coder:3b
    apiBase: http://localhost:11434
    roles:
      - chat
      - edit
      - apply
    defaultCompletionOptions:
      contextLength: 8192
      temperature: 0.1
      maxTokens: 2048
    keepAlive: 1800

# 上下文：让 Continue 能引用当前文件、目录、终端等
context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: folder
  - provider: codebase

# UM890 + 3B：自动补全默认关闭（3B 做 Tab 补全太慢）
# 若以后拉了 1.5b，可取消下面注释并 pull qwen2.5-coder:1.5b
#
# models 中追加：
#   - name: Qwen2.5-Coder 1.5B Autocomplete
#     provider: ollama
#     model: qwen2.5-coder:1.5b
#     apiBase: http://localhost:11434
#     roles:
#       - autocomplete
#     autocompleteOptions:
#       disable: false
#       debounceDelay: 400
#       maxPromptTokens: 1024
#       onlyMyCode: true
```

保存后执行 **`Developer: Reload Window`** 重载 VS Code。

### 6.3 配置要点说明

| 字段 | 值 | 说明 |
| --- | --- | --- |
| `provider` | `ollama` | 固定 |
| `model` | `qwen2.5-coder:3b` | 必须与 `ollama list` 显示一致 |
| `apiBase` | `http://localhost:11434` | Ollama 与 VS Code 同在 WSL 时用此地址 |
| `roles` | `chat` / `edit` / `apply` | 聊天与选中改码 |
| `temperature` | `0.1` | 编码任务偏低更稳 |

### 6.4 验证 Continue 已连上 Ollama

1. 确认 Ollama 在跑：`curl http://127.0.0.1:11434`
2. 打开任意 `.java` 或 `.py` 文件
3. `Ctrl+L` 打开 Continue，确认模型下拉为 **Qwen2.5-Coder 3B**
4. 输入：

```text
用一句话解释当前打开文件的作用。
```

5. 另开 WSL 终端观察：

```bash
ollama ps
```

有 `qwen2.5-coder:3b` 且 CPU 占用上升，说明请求已打到本地 Ollama。

---

<a id="sec-7"></a>

## 7. 日常使用

### 7.1 界面与快捷键

| 操作 | 方式 |
| --- | --- |
| 打开 Continue 聊天 | 左侧 Continue 图标，或 `Ctrl+L` |
| 带当前文件提问 | 打开文件后在 Continue 输入问题 |
| 引用文件 | 输入 `@` → 选 `Files` / 文件名 |
| 引用代码块 | 选中代码 → `Ctrl+L` → 提问 |
| 改选中代码 | 选中 → Continue 里用 **Edit** 或描述「请修改选中部分」 |

### 7.2 解释终端报错

```text
我在 WSL 执行 mvn spring-boot:run 报错如下。
请用中文说明根因，并给出可直接复制执行的修复命令。

（粘贴完整报错）
```

### 7.3 小范围改码

选中一个方法，在 Continue 输入：

```text
在不改变方法签名的前提下，增加空值检查和日志。
只输出修改后的方法代码。
```

### 7.4 生成测试骨架

```text
根据当前打开的 Service 类，生成 JUnit 5 测试类骨架。
使用 Mockito，包含一个正常路径测试。
```

### 7.5 UM890 + 3B 使用技巧

- **一次只问一件事**，不要一次塞整份设计书  
- 问题里写清技术栈：`Java 17 + Spring Boot 3`  
- 限定输出：`只改当前文件`、`不超过 40 行`  
- 生成时避免同时跑 `mvn clean install`、Docker 大批量构建  
- Continue 与 Aider **不要同时**对大项目下重 prompt  

### 7.6 Agent / 多文件改动

`qwen2.5-coder:3b` 在 UM890 上 **不适合** 复杂 Agent 式多文件自主改动。  
多文件批量修改请用第 10 节的 **Aider**。

---

<a id="sec-8"></a>

## 8. 模型选择建议

| 模型 | 内存约 | UM890 用途 |
| --- | --- | --- |
| **`qwen2.5-coder:3b`** | 2～3GB | **默认**：Continue Chat / Edit |
| `qwen2.5-coder:1.5b` | 1～2GB | 可选：仅 Tab 自动补全 |
| `qwen2.5-coder:7b` | 5～8GB | 轻负载时可试；CPU 明显变慢 |

```bash
# 默认
ollama pull qwen2.5-coder:3b

# 可选：给 Continue 自动补全专用
ollama pull qwen2.5-coder:1.5b
```

升级到 7B 时，只需改 `config.yaml` 里 `model: qwen2.5-coder:7b`，并 `ollama pull qwen2.5-coder:7b`。

---

<a id="sec-9"></a>

## 9. 常见问题排查

### 9.1 Continue 提示无法连接 Ollama

```bash
# 1. Ollama 是否在跑
curl http://127.0.0.1:11434
sudo systemctl status ollama

# 2. 若用前台方式，先启动
ollama serve

# 3. 模型是否已拉取
ollama list
```

确认 `config.yaml` 中 `apiBase` 为 `http://localhost:11434`，`model` 与 `ollama list` 完全一致。

### 9.2 有响应但极慢

1. 确认用的是 **3b**，不是 7b/14b  
2. `ollama stop` 释放后重试  
3. 关闭 Docker 无用容器  
4. `free -h` 看 WSL 是否内存告急  
5. 缩短问题、减少 `@codebase` 大范围检索  

### 9.3 Continue 装在 Windows 本地，Ollama 在 WSL

**不要这样混用。** 请：

1. 卸载 Windows 本地的 Continue（或忽略）  
2. 在 **WSL: Ubuntu** 再装一份 Continue  
3. Ollama 与 `config.yaml` 都在 WSL 内  

### 9.4 `config.yaml` 改完不生效

1. `Developer: Reload Window`  
2. `Continue: Open Config` 确认改的是 `~/.continue/config.yaml`  
3. 看 Continue 输出面板是否有 YAML 语法报错  

### 9.5 端口 11434 冲突

Windows 与 WSL **只保留一处 Ollama**。检查：

```bash
ss -lntp | grep 11434
```

### 9.6 Tab 自动补全不出现

UM890 上 3B 做自动补全偏慢，本教程 **默认关闭**。若已按第 6.2 节启用 1.5b 自动补全：

- 确认 `ollama pull qwen2.5-coder:1.5b`  
- VS Code 设置中搜索 `continue`，确认未禁用 autocomplete  
- `debounceDelay` 调到 `400` 以上减轻 CPU 压力  

---

<a id="sec-10"></a>

## 10. 与 Aider 配合（可选）

| 工具 | 适合做什么 |
| --- | --- |
| **Continue** | 编辑器内问答、解释、选中改码 |
| **Aider** | 终端多文件批量修改 |

共用同一 Ollama，不要同时跑大任务。

```bash
python3 -m venv ~/.venv/aider
source ~/.venv/aider/bin/activate
pip install "aider-chat[all]"

cd ~/workspace/vscode_study
aider --model ollama/qwen2.5-coder:3b --no-stream
```

参考：`softbs/aider/04_VS Code + Aider + Ollama 完整开发流.md`

---

<a id="sec-11"></a>

## 11. 相关文档

| 文档 | 说明 |
| --- | --- |
| [Win11_WSL_VSCode_Java_Python_快速开发指南.md](Win11_WSL_VSCode_Java_Python_快速开发指南.md) | WSL + VS Code 入门 |
| [UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md) | 完整本地开发环境 |
| [Continue Ollama 官方指南](https://docs.continue.dev/guides/ollama-guide) | config.yaml 参考 |
| [Continue config 参考](https://docs.continue.dev/reference) | 字段说明 |

---

## UM890 Pro 最短路径 checklist

1. `.wslconfig` 设 `memory=20GB`，`wsl --shutdown` 后重进  
2. WSL：`curl -fsSL https://ollama.com/install.sh | sh`  
3. `sudo systemctl enable ollama && sudo systemctl start ollama`  
4. `ollama pull qwen2.5-coder:3b`  
5. `ollama run qwen2.5-coder:3b` 试跑一句  
6. VS Code **Remote - WSL** 打开 `~/workspace/vscode_study`  
7. 扩展市场安装 **Continue**（WSL 侧）  
8. `Ctrl+Shift+P` → **Continue: Open Config**，粘贴第 6.2 节 `config.yaml`  
9. 重载窗口，`Ctrl+L` 选 **Qwen2.5-Coder 3B**，开始提问  

完成以上步骤后，即可在 UM890 Pro 上用 **VS Code + WSL + Continue + Ollama** 免费本地辅助编程。
