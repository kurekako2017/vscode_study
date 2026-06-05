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
- [7. Continue 日常使用（喂代码 / 选文件 / 快捷键 / Prompt 模板）](#sec-7)
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

## 7. Continue 日常使用（喂代码 / 选文件 / 快捷键）

配置好 **VS Code + WSL + Continue + Ollama** 之后，日常效率主要取决于：**有没有把正确的上下文喂给模型**。  
UM890 上用 `qwen2.5-coder:3b` 时尤其如此——上下文越精准，回答越稳。

### 7.1 快捷键一览（建议背下来）

| 操作 | 快捷键 / 方式 |
| --- | --- |
| 打开 Continue 聊天 | `Ctrl+L` |
| 把选中代码加入对话 | 选中代码 → `Ctrl+L` |
| 行内直接改码（Inline Edit） | 选中代码 → `Ctrl+I` |
| 引用文件 / 上下文 | 在输入框输入 `@` |
| 发送消息 | `Enter` 或 `Ctrl+Enter`（以 Continue 设置为准） |

也可点击左侧活动栏的 **Continue 图标** 打开侧栏。

### 7.2 正确「喂」代码的 3 种方法

#### 方法 1：选中代码 + `Ctrl+L`（最推荐）

1. 在编辑器里 **拖选** 一段代码（一个方法、一个类、几行逻辑均可）  
2. 按 **`Ctrl+L`**  
3. 选中内容会出现在 **Continue 侧栏** 的上下文中  
4. 直接输入问题，例如：`帮我重构这段代码` / `解释这段在做什么`

这是 UM890 + 3B 下 **最稳** 的方式：上下文小、模型不容易跑偏。

#### 方法 2：右键菜单

1. 选中代码  
2. 右键 → **Continue** → **Add Highlighted Code to Context**（将高亮代码加入上下文）  
3. 在 Continue 侧栏输入问题  

效果与方法 1 相同，适合不习惯快捷键时使用。

#### 方法 3：用 `@codebase` 搜全项目（范围大，慎用）

在 Continue 输入框输入 **`@codebase`**，再写问题，例如：

```text
@codebase 项目里哪里处理了用户登录校验？
```

- 适合：不知道代码在哪、要在整个仓库里搜  
- **UM890 + 3B 注意**：全库检索慢、占上下文，容易答偏；优先用方法 1 圈定具体代码  

### 7.3 如何「选中文件」作为上下文

#### 方式 A：`@` + 文件名（推荐）

在 Continue 输入框输入 **`@`**，接着打文件名，例如：

```text
@UserService.java 这个类负责什么？
```

会出现自动补全，选中目标文件即可。

#### 方式 B：`@` + 当前活动文件

先 **在编辑器里打开** 目标文件，再在 Continue 输入：

```text
@Active File 总结这个文件的结构
```

或输入 `@` 后从列表里选 **Current File / Active File**（名称因 Continue 版本略有不同）。

#### 不推荐的习惯

只写 **`@Active File` + 笼统问题**（例如「帮我优化」），却不选中具体函数——  
模型看到的是整文件，3B 容易忽略重点。**更好的做法见 7.4 节。**

### 7.4 最推荐工作流（非常重要）

```text
选中具体函数或代码块 → Ctrl+L → 用中文说清楚要什么
```

示例：

1. 选中某个 `public void saveUser(...)` 方法  
2. `Ctrl+L`  
3. 输入：

```text
在不改方法签名的前提下，增加参数校验和日志。只改这个方法。
```

对比：

| 做法 | 效果 |
| --- | --- |
| `@Active File` + 「帮我重构」 | 上下文过大，3B 易泛泛而谈 |
| 选中一个方法 + `Ctrl+L` + 明确指令 | **精准、可改、可解释** |

日常改 bug、讲逻辑、写小函数，都按这个流程来。

### 7.5 有没有选中成功？看侧栏，别看编辑器

Continue **不像 Cursor** 那样在编辑器里做很明显的高亮标记。

判断是否选中成功：

1. 按 `Ctrl+L` 后看 **Continue 侧栏**  
2. 若出现 **代码片段 / 文件引用 / Context 区域** 有内容 → 已加入上下文  
3. 侧栏里没有代码、只有空输入框 → 重新选中代码再 `Ctrl+L`  

### 7.6 行内改码：`Ctrl+I`

适合「就改这一块、立刻看 diff」：

1. 选中要改的代码  
2. **`Ctrl+I`**  
3. 输入修改意图，例如：`把这里改成 stream 写法`  
4. 在编辑器内查看 Continue 给出的修改，接受或拒绝  

Chat（`Ctrl+L`）适合问答；**Inline Edit（`Ctrl+I`）** 适合就地改码。

### 7.7 解释终端报错

不必选中代码，直接在 Continue 粘贴报错：

```text
我在 WSL 执行 mvn spring-boot:run 报错如下。
请用中文说明根因，并给出可直接复制执行的修复命令。

（粘贴完整报错）
```

### 7.8 生成测试骨架

选中 Service 类中的一个方法或整个类 → `Ctrl+L`：

```text
为当前选中的类生成 JUnit 5 测试骨架，使用 Mockito，包含一个正常路径测试。
```

### 7.9 特别适合本地模型的 Prompt 模板（建议收藏）

本地 `qwen2.5-coder:3b` 容易 **话多、只给片段、夹带解释**。改代码时建议在问题末尾加上固定句式，**强迫只输出可直接用的完整代码**。

配合方式：**选中代码 → `Ctrl+L`（或 `Ctrl+I`）→ 粘贴下面模板再补你的具体要求**。

#### 模板 1：通用改码（最常用）

```text
请直接输出修改后的完整代码。
不要解释。
只返回最终代码。
```

适用：重构、改 bug、改写法、补全选中片段。

#### 模板 2：在指定位置加注释

```text
请直接输出修改后的完整代码。
在这行代码上方添加中文注释。
不要解释。
```

把「这行代码」换成更具体的描述，例如：`在 client 赋值那一行上方`。

#### 模板 3：Java / Spring 改码（本仓库常用）

```text
请直接输出修改后的完整方法代码。
技术栈：Java 17 + Spring Boot。
不要解释，不要 markdown 代码块标记。
只返回最终代码。
```

#### 模板 4：只要 diff 式说明时再用（例外）

需要理解逻辑、查报错时 **不要** 用上面模板，改用：

```text
请用中文分点说明原因，并给出修复步骤。先不要直接改代码。
```

#### 预期输出示例

提问（选中 Python 片段 + 模板 2）后，理想回复应接近：

```python
# 根据 mock 模式创建对应客户端
client = build_client(use_mock)
```

Java 场景理想回复应接近：

```java
// 根据配置决定使用 Mock 还是真实实现
Client client = buildClient(useMock);
```

而不是：

```text
好的，我来帮你修改。首先我们需要理解这段代码的作用……
（后面一大段说明，代码还不完整）
```

#### 使用技巧

| 场景 | 是否加「不要解释」 |
| --- | --- |
| `Ctrl+I` 行内改码 | **建议加** |
| `Ctrl+L` 问「这段干什么」 | **不要加**（需要解释） |
| `Ctrl+L` 改选中方法 | **建议加** |
| 粘贴终端报错 | **不要加**（需要根因分析） |

可把模板 1 存到 Continue 的 **自定义 prompt / 片段**（若版本支持），或单独记在笔记里复制使用。

### 7.10 UM890 + 3B 使用技巧

- **一次只问一件事**，不要一次塞整份设计书  
- 问题里写清技术栈：`Java 17 + Spring Boot 3`  
- 限定输出：`只改当前方法`、`不超过 40 行`  
- 大项目搜索少用 `@codebase`，多用 **选中 + `Ctrl+L`**  
- 生成时避免同时跑 `mvn clean install`、Docker 大批量构建  
- Continue 与 Aider **不要同时**对大项目下重 prompt  

### 7.11 Agent / 多文件改动

`qwen2.5-coder:3b` 在 UM890 上 **不适合** 复杂 Agent 式多文件自主改动。  
多文件批量修改请用第 10 节的 **Aider**。

### 7.12 方案串联小结

```text
VS Code（Remote - WSL）
  → Continue（Ctrl+L 喂上下文 / Ctrl+I 改代码）
    → Ollama localhost:11434
      → qwen2.5-coder:3b
```

连上之后，你就有一套 **免费、本地、可离线** 的 AI 编程助手；熟练 **选中 → Ctrl+L → 提问** 是用好它的关键。

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
