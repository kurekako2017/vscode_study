# WSL 中安装 Ollama + GitHub Copilot 使用本地模型教程

> 适用场景：Win11 + WSL2 Ubuntu + VS Code Remote - WSL，希望在 Copilot Chat 里使用本机 Ollama 模型辅助编程。
> 目标：数据不出本机、不额外消耗云端 API 额度，同时保留 VS Code 熟悉的 Chat / Agent 体验。

---

## 快速跳转

- [1. 整体架构与两种安装方式](#sec-1)
- [2. 环境前提](#sec-2)
- [3. 方案 A：在 WSL Ubuntu 内安装 Ollama（推荐）](#sec-3)
- [4. 方案 B：在 Windows 侧安装 Ollama（备选）](#sec-4)
- [5. 拉取与测试模型](#sec-5)
- [6. VS Code + GitHub Copilot 接入 Ollama](#sec-6)
- [7. 日常使用示例](#sec-7)
- [8. 模型推荐（按内存）](#sec-8)
- [9. 常见问题排查](#sec-9)
- [10. 与 Aider 的配合（可选）](#sec-10)
- [11. 相关文档](#sec-11)

---

<a id="sec-1"></a>

## 1. 整体架构与两种安装方式

### 1.1 推荐架构

```text
Windows 11
  └── VS Code（Remote - WSL）
        └── Copilot Chat
              └── Language Models → Ollama Provider
                    └── http://localhost:11434
                          └── WSL Ubuntu 内的 Ollama 服务
                                └── 本地 LLM（如 qwen2.5-coder:14b）
```

一句话理解：

`VS Code 在 Windows 打开，但 Ollama 跑在 WSL 里；Copilot Chat 通过 localhost:11434 调用本地模型。`

### 1.2 两种安装方式怎么选

| 方式               | 安装位置      | 适合谁                   | 说明                                          |
| ------------------ | ------------- | ------------------------ | --------------------------------------------- |
| **方案 A（推荐）** | WSL Ubuntu 内 | 日常用 Remote - WSL 开发 | 与 Java / Python / Git 工具链同环境，路径一致 |
| **方案 B（备选）** | Windows 侧    | 已在 Windows 装好 Ollama | WSL 通过 `localhost:11434` 访问 Windows 服务  |

> 不要同时在 Windows 和 WSL 各装一个 Ollama 并都监听 `11434`，容易端口冲突。选一种即可。

---

<a id="sec-2"></a>

## 2. 环境前提

### 2.1 硬件与系统

- Windows 11 + WSL2（Ubuntu 22.04 / 24.04）
- 建议内存 16GB 以上；跑 7B～14B 编码模型建议 32GB
- 有独显时：在 **Windows** 安装最新 NVIDIA 驱动即可，WSL 内 **不要** 再装 Linux 版显卡驱动

### 2.2 软件版本（Copilot 接 Ollama 的最低要求）

| 组件                     | 最低版本     |
| ------------------------ | ------------ |
| Ollama                   | 0.18.3+      |
| VS Code                  | 1.113+       |
| GitHub Copilot 扩展      | 已安装并登录 |
| GitHub Copilot Chat 扩展 | 0.41.0+      |

### 2.3 确认 WSL 正常

Windows PowerShell：

```powershell
wsl -l -v
wsl -d Ubuntu
```

WSL 内：

```bash
uname -a
pwd
```

若左下角显示 `WSL: Ubuntu`，说明 VS Code 已连上 WSL 开发环境。详见 [Win11_WSL_VSCode_Java_Python_快速开发指南.md](Win11_WSL_VSCode_Java_Python_快速开发指南.md)。

---

<a id="sec-3"></a>

## 3. 方案 A：在 WSL Ubuntu 内安装 Ollama（推荐）

### 3.1 启用 systemd（Ollama 后台服务需要）

较新的 Ubuntu on WSL 默认可能已启用。先检查：

```bash
systemctl --version
```

若提示 systemd 不可用，编辑 `/etc/wsl.conf`：

```bash
sudo nano /etc/wsl.conf
```

写入：

```ini
[boot]
systemd=true
```

保存后，在 **Windows PowerShell** 执行：

```powershell
wsl --shutdown
wsl -d Ubuntu
```

重新进入 WSL 后验证：

```bash
systemctl is-system-running
```

### 3.2 安装依赖并执行官方安装脚本

```bash
sudo apt update
sudo apt install -y curl zstd
curl -fsSL https://ollama.com/install.sh | sh
```

验证：

```bash
ollama --version
```

### 3.3 确认 Ollama 服务已启动

```bash
sudo systemctl status ollama
```

若未运行：

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### 3.4 验证 API 端口

```bash
curl http://127.0.0.1:11434
```

正常应返回 `Ollama is running` 一类文本。

```bash
curl http://127.0.0.1:11434/api/tags
```

应返回已安装模型的 JSON 列表（初次可能为空数组 `{"models":[]}`）。

### 3.5 （可选）确认 GPU 是否被识别

有独显时：

```bash
nvidia-smi
ollama ps
```

拉模型并运行后，`ollama ps` 里若显示 `GPU` 相关字段，说明加速生效。

### 3.6 （可选）给 WSL 分配足够内存

编辑 Windows 用户目录下的 `%UserProfile%\.wslconfig`：

```ini
[wsl2]
memory=24GB
processors=8
swap=8GB
```

修改后执行：

```powershell
wsl --shutdown
```

---

<a id="sec-4"></a>

## 4. 方案 B：在 Windows 侧安装 Ollama（备选）

若你已在 Windows 安装 Ollama，可跳过方案 A，按下面验证即可。

### 4.1 Windows 安装

1. 打开 <https://ollama.com/download/windows> 下载安装包
2. 安装完成后，在 PowerShell 验证：

```powershell
ollama --version
```

### 4.2 从 WSL 访问 Windows 上的 Ollama

WSL2 下 `localhost` 通常可直接转发到 Windows 主机服务：

```bash
curl http://localhost:11434
curl http://localhost:11434/api/tags
```

若失败，可在 Windows 确认 Ollama 托盘图标正在运行，或在 PowerShell 执行：

```powershell
ollama serve
```

> 说明：此方式下，模型文件存放在 Windows 用户目录，与 WSL 内 Linux 路径分离；Copilot Chat 在 WSL 窗口里使用时，只要 `localhost:11434` 通即可。

---

<a id="sec-5"></a>

## 5. 拉取与测试模型

### 5.1 拉取编码向模型（推荐起步）

在 **Ollama 所在环境**（WSL 或 Windows 终端）执行：

```bash
# 轻量，适合 16GB 内存试跑
ollama pull qwen2.5-coder:7b

# 质量更好，建议 32GB 内存 + 独显
ollama pull qwen2.5-coder:14b
```

查看已安装模型：

```bash
ollama list
```

### 5.2 命令行试跑

```bash
ollama run qwen2.5-coder:7b
```

输入一句测试：

```text
用 Java 写一个简单的 REST Controller 示例，只返回 hello。
```

能正常输出代码，说明模型与服务正常。输入 `/bye` 退出。

### 5.3 一键检测 VS Code 集成（官方快捷命令）

Ollama 0.18.3+ 支持：

```bash
ollama launch vscode
```

该命令会引导你完成 VS Code 侧配置，并提示推荐模型。也可指定模型：

```bash
ollama launch vscode --model qwen2.5-coder:7b
```

---

<a id="sec-6"></a>

## 6. VS Code + GitHub Copilot 接入 Ollama

### 6.1 安装扩展

在 **WSL: Ubuntu** 扩展区域安装（不要只装在 Windows 本地）：

| 扩展                | ID                            |
| ------------------- | ----------------------------- |
| GitHub Copilot      | `GitHub.copilot`              |
| GitHub Copilot Chat | `GitHub.copilot-chat`         |
| Remote - WSL        | `ms-vscode-remote.remote-wsl` |

### 6.2 登录 GitHub

1. 按 `Ctrl+Shift+P`，执行 `GitHub Copilot: Sign In`
2. 按浏览器提示完成授权

> 使用本地 Ollama 模型也需要登录 GitHub，但 **不要求付费 Copilot 订阅**；GitHub Copilot Free 即可在模型选择器中使用自定义本地模型。

### 6.3 方式一：快捷配置（推荐）

在 WSL 终端：

```bash
ollama launch vscode
```

然后在 VS Code 中：

1. 打开 Copilot Chat 侧栏（右上角聊天图标，或 `Ctrl+Alt+I`）
2. 面板底部将 **Session target** 设为 **`Local`**（使用本地模型时必须选 Local）
3. 在模型选择器里选择你的 Ollama 模型（如 `qwen2.5-coder:7b`）

### 6.4 方式二：手动配置 Language Models

1. 打开 Copilot Chat 侧栏
2. 点击设置齿轮，进入 **Language Models** 管理界面
3. 点击 **Add Models**
4. 选择 **Ollama**
5. 端点填写：

```text
http://localhost:11434
```

6. 确认后，VS Code 会自动发现 `ollama list` 中的模型
7. 若模型在管理界面可见但聊天框里看不到，点击模型选择器中的 **Unhide**，把 Ollama 模型显示出来

### 6.5 验证是否走本地模型

1. Copilot Chat 底部：**Local** + 选中 Ollama 模型名
2. 打开任意代码文件，选中一小段代码
3. 在 Chat 输入：

```text
请用中文解释这段代码在做什么，并指出一个可能的改进点。
```

4. 同时在终端观察 Ollama 日志：

```bash
# WSL 内安装的 Ollama
sudo journalctl -u ollama -f
```

若看到 `/v1/chat/completions` 或 `/api/chat` 请求，说明 Copilot 正在调用本地 Ollama。

### 6.6 Agent 模式与 Tool Calling 说明

在 **Agent 模式**下，模型需要支持 **tool calling（工具调用）**，才会出现在部分模型下拉列表中。

- 支持较好的：`qwen2.5-coder` 系列等较新编码模型
- 若模型在 Language Models 里已检测到，但 Chat 下拉框没有：
  - 先切换到 **Ask / Edit** 等非 Agent 模式试聊
  - 或换用支持 tools 的模型
  - 更新 VS Code、Copilot Chat、Ollama 到最新版

官方说明：<https://code.visualstudio.com/docs/copilot/customization/language-models>

---

<a id="sec-7"></a>

## 7. 日常使用示例

### 7.1 解释报错

把终端报错全文贴进 Chat：

```text
我在 WSL 终端执行 mvn spring-boot:run 时出现下面的错误。
请先说明根因，再给出可以直接复制执行的修复命令。
项目路径：~/workspace/vscode_study/java-projects/JtProject-Next

（这里粘贴完整报错）
```

### 7.2 改代码

1. 选中要修改的函数或文件片段
2. Chat 输入：

```text
在不改变对外接口的前提下，给这个方法加上空值检查和日志输出。
只改必要部分，并说明改了哪里。
```

### 7.3 生成单元测试骨架

```text
根据当前打开的 Service 类，生成 JUnit 5 测试类骨架。
使用 Mockito，先覆盖正常路径和一个异常路径。
```

### 7.4 使用技巧

- 在 **项目根目录** 打开 VS Code，上下文更准确
- 问题里写清：当前目录、技术栈、期望结果、完整报错
- 本地模型比云端慢时属正常，可先用 7B 试流程，满意后再换 14B
- 涉及删除文件、改生产配置、执行 `rm` / `git reset` 等命令时，**先人工确认**再执行

---

<a id="sec-8"></a>

## 8. 模型推荐（按内存）

| 模型                    | 大致内存需求 | 特点                        |
| ----------------------- | ------------ | --------------------------- |
| `qwen2.5-coder:7b`      | 8～12GB      | 入门首选，响应较快          |
| `qwen2.5-coder:14b`     | 16～20GB     | 代码质量更好，32GB 机器推荐 |
| `deepseek-coder-v2:16b` | 16～20GB     | 备选编码模型                |
| `phi4`                  | 较低         | CPU 友好，适合无独显试跑    |

拉取命令示例：

```bash
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:14b
```

本仓库另有 Aider 侧模型调优参考：`softbs/aider/02_Aider 参数调优（UM890 Pro  32GB 内存专用）.md`

---

<a id="sec-9"></a>

## 9. 常见问题排查

### 9.1 `curl http://localhost:11434` 失败

**WSL 内安装的 Ollama：**

```bash
sudo systemctl status ollama
sudo systemctl restart ollama
curl http://127.0.0.1:11434
```

**Windows 安装的 Ollama：**

- 确认托盘区 Ollama 正在运行
- PowerShell：`ollama serve`
- WSL 再测：`curl http://localhost:11434`

### 9.2 Copilot Chat 里看不到 Ollama 模型

按顺序检查：

1. 是否已登录 GitHub Copilot
2. Chat 面板底部是否选了 **Local**
3. Language Models 里 Ollama 端点是否为 `http://localhost:11434`
4. 模型选择器里是否点了 **Unhide**
5. `ollama list` 是否已有模型
6. 更新 VS Code、Copilot Chat、Ollama 后执行 `Developer: Reload Window`

### 9.3 模型能聊天，但 Agent 模式不可用

- 换支持 tool calling 的模型（如 `qwen2.5-coder` 系列）
- 先用 Ask / Edit 模式完成日常问答和改码

### 9.4 响应很慢或内存不足

- 换更小模型（7B 代替 14B）
- 调大 `.wslconfig` 的 `memory`
- 关闭其他占内存应用
- `ollama ps` 查看是否在用 GPU

### 9.5 端口 11434 被占用

```bash
ss -lntp | grep 11434
```

确认只有一个 Ollama 实例在监听。Windows 与 WSL 不要重复安装并同时启动。

### 9.6 VS Code 连的是 Windows 窗口，不是 WSL

左下角应显示 `WSL: Ubuntu`。若显示本地 Windows：

1. `Ctrl+Shift+P` → `Remote-WSL: New Window`
2. 打开文件夹：`/home/你的用户名/workspace/vscode_study`

---

<a id="sec-10"></a>

## 10. 与 Aider 的配合（可选）

Copilot Chat 适合在编辑器里问答、解释、小范围改码；**Aider** 适合在终端里批量改多文件。两者可共用同一个 Ollama 服务。

### 10.1 在 WSL 安装 Aider

```bash
python3 -m venv ~/.venv/aider
source ~/.venv/aider/bin/activate
pip install --upgrade pip
pip install "aider-chat[all]"
```

### 10.2 在项目里启动

```bash
cd ~/workspace/vscode_study
source ~/.venv/aider/bin/activate
aider --model ollama/qwen2.5-coder:7b
```

更多内容见：

- `softbs/aider/01_Aider + Ollama Windows 标准启动方案.md`
- `softbs/aider/04_VS Code + Aider + Ollama 完整开发流.md`

---

<a id="sec-11"></a>

## 11. 相关文档

| 文档                                                                                                                             | 说明                                 |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| [Win11_WSL_VSCode_Java_Python_快速开发指南.md](Win11_WSL_VSCode_Java_Python_快速开发指南.md)                                     | WSL + VS Code 日常开发入门           |
| [UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md) | 含 Ollama + Aider 的完整本地开发环境 |
| [VSCode_Terminal_CLI_编程安装使用教程.md](VSCode_Terminal_CLI_编程安装使用教程.md)                                               | 含 GitHub Copilot CLI 终端用法       |
| [Ollama 官方 VS Code 集成说明](https://docs.ollama.com/integrations/vscode)                                                      | 官方快速配置                         |
| [VS Code Language Models 文档](https://code.visualstudio.com/docs/copilot/customization/language-models)                         | 自定义模型与 Agent 要求              |

---

## 最短路径 checklist

1. `wsl -d Ubuntu` 进入 WSL
2. `curl -fsSL https://ollama.com/install.sh | sh` 安装 Ollama
3. `ollama pull qwen2.5-coder:7b` 拉模型
4. `ollama run qwen2.5-coder:7b` 试跑一句
5. VS Code 用 Remote - WSL 打开项目
6. 安装并登录 GitHub Copilot + Copilot Chat
7. `ollama launch vscode` 或手动 Add Models → Ollama
8. Copilot Chat 选 **Local** + Ollama 模型，开始提问

完成以上步骤后，即可在 VS Code WSL 环境中用 GitHub Copilot Chat 调用本机 Ollama 模型辅助开发。
