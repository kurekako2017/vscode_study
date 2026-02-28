# UM890 Pro（Win11）安装 WSL2 Ubuntu + Docker Desktop：模拟 macOS 的 Java/Python 开发与本地模型辅助开发教程

> 目标：在 **Windows 11（UM890 Pro）** 上搭建一套“日常开发尽量在 Linux 里完成”的环境，做到接近 macOS 终端开发体验。  
> 适用：Java / Python 项目开发、容器化测试、本地大模型辅助编码（Aider / VS Code Copilot Chat + 本地模型）。

---

## 1. 你将得到什么

完成后你将具备：

- `Windows + WSL2(Ubuntu) + Docker Desktop` 的稳定开发底座
- 在 WSL Ubuntu 内开发 Java 与 Python（命令、路径、工具链都接近 macOS/Linux）
- VS Code 通过 Remote - WSL 直接编辑 Linux 文件系统
- 本地模型（Ollama）+ Aider，离线辅助代码开发

---

## 2. 架构说明（为什么这套方案“像 macOS”）

推荐开发流：

1. Windows 只负责系统与图形界面（VS Code / Docker Desktop）
2. 代码仓库放在 WSL Ubuntu 的 Linux 文件系统内（如 `~/workspace`）
3. 终端命令、依赖安装、Git 操作都在 Ubuntu 中进行
4. Docker Desktop 启用 WSL2 引擎后，容器体验与 Linux/macOS 非常接近

这样你平时使用的是 **Unix 风格工具链**，而不是 Windows 路径和 shell 习惯。

---

## 3. 前置检查（Win11）

以管理员 PowerShell 运行：

```powershell
wsl --status
systeminfo | findstr /i "Hyper-V"
```

检查要点：

- Windows 版本建议 `22H2` 或更新
- BIOS 开启虚拟化（SVM/VT-x）
- 若 `wsl` 命令不可用，先执行：

```powershell
wsl --install
```

然后重启。

---

## 4. 安装 WSL2 + Ubuntu

### 4.1 安装 Ubuntu 发行版

```powershell
wsl --install -d Ubuntu
```

安装后首次进入 Ubuntu，设置 Linux 用户名与密码。

### 4.2 设置默认 WSL 版本为 2

```powershell
wsl --set-default-version 2
wsl -l -v
```

若某发行版不是 2：

```powershell
wsl --set-version Ubuntu 2
```

### 4.3 推荐的 WSL 配置（提升稳定性）

在 Windows 用户目录创建或编辑 `%UserProfile%\.wslconfig`：

```ini
[wsl2]
memory=16GB
processors=8
swap=8GB
localhostForwarding=true
```

> 32GB 内存机器（UM890 Pro）可按工作负载调整，Java + Docker 同时运行时建议保留较大内存。

修改后执行：

```powershell
wsl --shutdown
```

再重新打开 Ubuntu。

---

## 5. 安装 Docker Desktop（并接入 WSL2）

### 5.1 安装

- 下载并安装 Docker Desktop（Windows 版本）
- 首次启动勾选 `Use the WSL 2 based engine`

### 5.2 开启 WSL 集成

Docker Desktop -> `Settings` -> `Resources` -> `WSL Integration`：

- 打开 `Enable integration with my default WSL distro`
- 打开 `Ubuntu` 对应开关

### 5.3 验证（在 Ubuntu 终端）

```bash
docker version
docker run --rm hello-world
```

若成功，说明 Ubuntu 内可直接用 Docker CLI。

---

## 6. 把开发目录放到 WSL（关键）

在 Ubuntu 中：

```bash
mkdir -p ~/workspace
cd ~/workspace
```

建议把 Git 项目都克隆到这里，而不是 `/mnt/c/...`。

原因：

- 文件 IO 更快
- 权限与软链接行为更接近 Linux/macOS
- 避免 Windows/WSL 跨文件系统导致的性能与兼容问题

---

## 7. VS Code 接入 WSL 开发

### 7.1 安装扩展

- `Remote - WSL`
- `Docker`
- `Extension Pack for Java`（按需）
- `Python`（按需）

### 7.2 从 WSL 打开项目

在 Ubuntu 中进入项目目录：

```bash
cd ~/workspace/your-project
code .
```

左下角出现 `WSL: Ubuntu` 即表示你在 Linux 环境内开发。

---

## 8. Ubuntu 内安装 Java 开发环境

### 8.1 安装 JDK 与 Maven

```bash
sudo apt update
sudo apt install -y openjdk-21-jdk maven
java -version
mvn -version
```

> 如项目要求 JDK17，可改为 `openjdk-17-jdk`。

### 8.2 Git 与常用工具

```bash
sudo apt install -y git curl unzip zip build-essential
```

---

## 9. Ubuntu 内安装 Python 开发环境

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
```

创建项目虚拟环境（示例）：

```bash
cd ~/workspace/your-python-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

---

## 10. 用 Docker 模拟“跨环境一致”开发

### 10.1 Java 示例（Maven）

```bash
docker run --rm -it -v "$PWD":/app -w /app maven:3.9-eclipse-temurin-21 mvn -v
```

### 10.2 Python 示例

```bash
docker run --rm -it -v "$PWD":/app -w /app python:3.11 python --version
```

这样可以快速验证项目在标准容器中的可运行性，减少“只在我机器能跑”的问题。

---

## 11. 本地模型辅助开发（Ollama + Aider）

> 你仓库里已有参考文档：`softbs/UM890_Aider_Local_LLM_Install.md`。本节给出与 WSL 开发流结合的最短路径。

### 11.1 在 Windows 安装 Ollama

- 下载安装：<https://ollama.com/download/windows>
- 在 Windows PowerShell 验证：

```powershell
ollama --version
ollama pull qwen2.5-coder:14b
```

> 说明：Ollama 服务通常运行在 Windows 侧，WSL 内通过 `http://localhost:11434` 访问。

### 11.2 在 WSL Ubuntu 安装 Aider

```bash
python3 -m venv ~/.venv/aider
source ~/.venv/aider/bin/activate
pip install --upgrade pip
pip install "aider-chat[all]"
```

### 11.3 在项目里启动 Aider（连接本地 Ollama）

```bash
cd ~/workspace/your-project
source ~/.venv/aider/bin/activate
aider --model ollama/qwen2.5-coder:14b --no-stream
```

如果想默认使用模型，可在项目目录创建 `.aider.conf.yml`：

```yaml
model: ollama/qwen2.5-coder:14b
no-stream: true
```

### 11.4 配置 CoPaw（OpenClaw）方案（可选）

> 说明：若你说的 `CoPaw` 指的是你仓库中的 `OpenClaw`，可按以下方式接入本地模型。参考文档：`softbs/Win11_OpenClaw_微信命令配置_qwen2.5-coder_1.5b.md`。

推荐职责分离：

- Windows 侧：运行 `Ollama` 与 `OpenClaw`
- WSL 侧：运行 Java/Python 开发命令与测试

步骤：

1. 在 Windows PowerShell 验证 Ollama：

```powershell
ollama --version
ollama pull qwen2.5-coder:14b
ollama run qwen2.5-coder:14b
```

2. 进入 OpenClaw 目录，执行配置：

```powershell
cd D:\tools\openclaw
openclaw configure
```

3. 在 OpenClaw 配置中设置：

- Provider：`ollama`
- Base URL：`http://localhost:11434`
- Model：`qwen2.5-coder:14b`（或你的其他本地代码模型）

4. 启动 OpenClaw：

```powershell
openclaw start
```

如果没有该命令，按实际安装方式使用 `openclaw run` 或 `python -m openclaw`。

5. 联调验证：

- 在 Windows 先确认 OpenClaw 能调用模型
- 在 WSL 项目目录中继续使用 `aider` 或 VS Code Chat 完成代码修改
- 形成“OpenClaw（外部命令/自动化）+ Aider（项目内改码）”组合

---

## 12. 推荐工作流（每天这样用）

1. 打开 Docker Desktop（确保已启动）
2. 打开 Ubuntu（WSL）终端
3. `cd ~/workspace/项目`，再 `code .`
4. Java/Python 依赖都在 Ubuntu 内安装
5. 需要容器测试时直接在 Ubuntu 里跑 `docker ...`
6. 需要 AI 辅助时启动 Aider，或在 VS Code 中使用本地模型插件

---

## 13. 常见问题排查

### 13.1 `docker: command not found`（在 WSL）

- 确认 Docker Desktop 已启动
- 确认开启了 Ubuntu 的 WSL Integration
- 重启 WSL：

```powershell
wsl --shutdown
```

### 13.2 WSL 中网络访问慢/代理问题

- 检查公司代理/杀毒软件拦截
- 尝试在 WSL 设置镜像源（apt/pip）

### 13.3 Aider 连接不到 Ollama

在 WSL 中检查：

```bash
curl http://localhost:11434/api/tags
```

若失败：

- 确认 Windows 侧 Ollama 正在运行
- 先在 Windows 中 `ollama run qwen2.5-coder:14b` 做一次冷启动

### 13.4 Java 项目内存不足或构建慢

- 调整 `%UserProfile%\.wslconfig` 的 `memory` / `processors`
- 在 Maven/Gradle 配置里合理设置 JVM 堆内存

---

## 14. 如何尽量“真模拟 macOS 开发”（具体实现）

以下配置可以把日常体验进一步拉近 macOS（终端 + 工具链）：

### 14.1 统一 Shell 体验（zsh）

在 Ubuntu 中：

```bash
sudo apt update
sudo apt install -y zsh git curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

可选插件（自动补全/高亮）：

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

在 `~/.zshrc` 启用：

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

### 14.2 统一包管理习惯（Homebrew on Linux，可选）

如果你希望与 macOS 的 `brew` 命令保持一致，可安装 Linuxbrew：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

然后按安装提示把 `brew shellenv` 写入 `~/.zprofile`。

### 14.3 统一语言版本管理（更接近 macOS 团队协作）

- Java：用 `sdkman` 管理多 JDK
- Python：用 `pyenv` 或项目内 `.venv`

建议每个项目固定版本文件（如 `.python-version`、`.sdkmanrc`），减少环境漂移。

### 14.4 统一目录与 Git 规范

- 所有项目固定在 `~/workspace/*`
- 全局 Git 换行策略建议：

```bash
git config --global core.autocrlf input
git config --global core.eol lf
```

- 项目内使用 `.gitattributes` 固定文本文件为 LF

### 14.5 统一容器/运行时（最关键）

尽量在容器中执行构建与测试（Java/Python 都一样），让本机差异最小化。  
如果项目已有 `devcontainer`，优先使用 VS Code `Reopen in Container`，这一步最接近“团队统一开发机”。

---

## 15. 与“真 macOS 开发”的差异

能做到高度一致的部分：

- shell 命令、目录结构、包管理、Docker 使用方式
- Java/Python 工具链与 CI 环境一致性

仍有差异的部分：

- 底层内核与文件系统实现并非 macOS
- GUI 工具生态仍是 Windows 为主
- 某些依赖原生 Darwin 行为的工具需单独适配

对大多数后端/AI/容器化开发，这套方案已足够接近 macOS/Linux 体验。

---

## 16. 一键自检命令清单

在 Ubuntu 里执行：

```bash
uname -a
lsb_release -a
java -version
mvn -version
python3 --version
pip --version
docker version
docker run --rm hello-world
curl http://localhost:11434/api/tags
```

全部通过即可开始稳定开发。

---

## 17. 可选增强（按需）

- 安装 `zsh + oh-my-zsh`，获得更接近 macOS 终端体验
- 使用 `pyenv` / `sdkman` 管理多版本 Python/JDK
- 给 Docker Desktop 限制资源，避免挤占开发机性能
- 将常用命令写成 `Makefile` 或 `justfile` 统一团队开发入口

---

## 18. 结论

在 UM890 Pro + Win11 上，采用 **WSL2 Ubuntu + Docker Desktop + VS Code Remote**，可以把日常开发过程迁移到 Linux 语境中，形成接近 macOS 的 Java/Python 开发体验；再叠加 **Ollama + Aider**，即可实现本地大模型辅助编程，兼顾效率、隐私与成本。
