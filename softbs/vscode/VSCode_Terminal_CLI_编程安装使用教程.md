# VSCode + Terminal CLI 编程安装使用教程

本文面向 Windows 11 + VS Code 用户，目标是把 VS Code 和终端 CLI 组合成日常开发环境。CLI 是 Command Line Interface，也就是命令行工具。学会 CLI 后，可以更高效地运行项目、管理 Git、安装依赖、执行测试和调用 AI 编程工具。

章节速览：

- [1. 推荐环境](#1-推荐环境)
- [2. 安装 VS Code](#2-安装-vs-code)
- [3. 安装常用 CLI 工具](#3-安装常用-cli-工具)
   - [3.1 Git](#31-git)
   - [3.2 Node.js 和 npm](#32-nodejs-和-npm)
   - [3.3 Python](#33-python)
   - [3.4 Java 和 Maven](#34-java-和-maven)
   - [3.5 OpenAI Codex CLI](#35-openai-codex-cli)
   - [3.6 Codex CLI 添加图片和截图](#36-codex-cli-添加图片和截图)
   - [3.7 GitHub Copilot CLI](#37-github-copilot-cli)
- [4. 在 VS Code 中使用终端](#4-在-vs-code-中使用终端)
- [5. 用 CLI 打开项目](#5-用-cli-打开项目)
- [6. CLI 编程基本工作流](#6-cli-编程基本工作流)
- [7. VS Code 插件建议](#7-vs-code-插件建议)
- [8. 常用 CLI 命令速查](#8-常用-cli-命令速查)
   - [文件和目录](#文件和目录)
   - [搜索](#搜索)
   - [端口检查](#端口检查)
- [9. 前端项目实战](#9-前端项目实战)
- [10. Java Spring Boot 项目实战](#10-java-spring-boot-项目实战)
- [11. Python CLI 脚本实战](#11-python-cli-脚本实战)
- [12. 常见问题](#12-常见问题)
   - [code 命令不可用](#code-命令不可用)
   - [npm 命令不可用](#npm-命令不可用)
   - [PowerShell 无法激活 Python 虚拟环境](#powershell-无法激活-python-虚拟环境)
   - [命令在 VS Code 终端和系统终端表现不同](#命令在-vs-code-终端和系统终端表现不同)
- [13. 学习顺序建议](#13-学习顺序建议)

## 1. 推荐环境

建议使用以下组合：

| 工具 | 用途 |
| --- | --- |
| VS Code | 代码编辑、终端集成、插件管理 |
| Git | 版本管理 |
| Node.js / npm | 前端项目和 CLI 工具 |
| Python | 脚本、自动化、AI 应用开发 |
| Java / Maven | Java 项目开发 |
| Codex CLI | 在终端中使用 OpenAI Codex 编程助手 |

如果只想先快速开始，至少安装：

1. VS Code
2. Git
4. Python
5. Windows Terminal

## 2. 安装 VS Code

1. 打开 VS Code 官网下载安装包。
2. 安装时建议勾选：
   - Add to PATH
   - Register Code as an editor
   - Add "Open with Code" action
3. 安装完成后打开 PowerShell，验证 `code` 命令：

```powershell
code --version
```

如果提示找不到 `code`，可以在 VS Code 中执行：

1. 按 `Ctrl + Shift + P`
2. 输入 `Shell Command`
3. 选择安装 `code` 命令到 PATH 的选项
4. 重新打开终端后再执行 `code --version`

## 3. 安装常用 CLI 工具

### 3.1 Git

安装 Git 后验证：

```powershell
git --version
```

设置用户名和邮箱：

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

常用命令：

```powershell
git status
git add .
git commit -m "update docs"
git pull
git push
```

### 3.2 Node.js 和 npm

安装 Node.js LTS 版本后验证：

```powershell
node -v
npm -v
```

常用命令：

```powershell
npm install
npm run dev
npm run build
npm test
```

### 3.3 Python

安装 Python 后验证：

```powershell
python --version
pip --version
```

如果你的环境使用 `py` 启动器，也可以执行：

```powershell
py --version
py -m pip --version
```

创建虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 3.4 Java 和 Maven

验证 Java：

```powershell
java -version
```

如果项目自带 Maven Wrapper，优先使用：

```powershell
.\mvnw.cmd -v
.\mvnw.cmd test
.\mvnw.cmd spring-boot:run
```

在 WSL 或 Linux 终端中：

```bash
### 3.5 OpenAI Codex CLI

Codex CLI 是 OpenAI 的终端编程助手，可以在 VS Code 终端里直接读取当前工作区，帮助你理解代码、修改文件、运行命令、做代码审查和排查错误。

本工作区已安装：

```bash
which codex
codex --version
```

注意：`code --version` 查看的是 VS Code 命令行工具版本，不是 Codex CLI 版本。Codex CLI 必须用 `codex --version` 查看。

```bash
code --version
# 显示 VS Code 版本，例如 1.122.1

codex --version
# 显示 Codex CLI 版本，例如 codex-cli 0.135.0
```

当前安装位置：

```text
/home/victorkure/.npm-global/bin/codex
```

当前版本：

```text
codex-cli 0.135.0
```

如果以后需要重新安装或升级，可以执行：

```bash
npm install -g @openai/codex
```

检查全局安装结果：

```bash
npm list -g --depth=0 @openai/codex
```

诊断本机 Codex 环境：

```bash
codex doctor
```

登录：

```bash
codex login
```

退出登录：

```bash
codex logout
```

在当前目录启动交互式 Codex：

```bash
codex
```

如果 VS Code 左下角或资源管理器标题显示 `WSL: Ubuntu`，并且终端提示符类似：

```bash
victorkure@um890pro:~/workspace/vscode_study$
```

说明当前窗口已经连接到 WSL，终端目录就是 Linux 路径：

```bash
/home/victorkure/workspace/vscode_study
```

这种情况下可以直接在终端输入：

```bash
codex

```bash
codex "请阅读当前工作区，告诉我这个仓库主要有哪些学习模块"
```

如果提示需要登录，先执行：

```bash
codex login
```

登录完成后再重新运行 `codex`。

直接带问题启动：

```bash
codex "帮我阅读这个项目，并说明启动方式"
```

在 Bash / WSL 终端里，中文任务只要包含空格，就必须用引号包起来。否则终端会把一句话拆成多个参数，Codex 可能报：

```text
error: unexpected argument '...' found
```

错误写法：

```bash
codex 检查这个项目的 mmd 文件，是怎么使用的？我怎么看看，需要吗 不需要的话删除
```

正确写法：

```bash
codex "检查这个项目的 mmd 文件，是怎么使用的？我怎么看看，需要吗，不需要的话删除"
```

如果任务里本身有英文双引号，可以改用单引号：

```bash
codex '检查这个项目的 Mermaid / mmd 文件，告诉我哪些还被 Markdown 引用，哪些可以删除'
```

在指定目录启动：

```bash
codex -C /home/victorkure/workspace/vscode_study
```

非交互式执行一次任务：

```bash
codex exec "检查这个项目的 README 是否有断链"
```

更多使用例子：

```bash
codex "帮我总结这个工作区的目录结构，重点说明 java-projects 和 softbs 目录"
```

```bash
cd ~/workspace/vscode_study/java-projects/JtProject-Next
codex "帮我检查这个项目怎么启动，前端和后端分别用什么命令"
```

```bash
codex exec "检查 softbs/vscode/VSCode_Terminal_CLI_编程安装使用教程.md 有没有明显错别字和命令错误"
```

做代码审查：

```bash
codex review
```

常用参数：

| 命令 | 用途 |
| --- | --- |
| `codex` | 打开交互式 TUI |
| `codex "任务"` | 带初始任务打开 Codex |
| `codex exec "任务"` | 非交互执行一次任务 |
| `codex review` | 对当前变更做代码审查 |
| `codex resume` | 恢复之前的会话 |
| `codex doctor` | 检查安装、配置、认证和网络 |
| `codex login` | 登录 OpenAI / ChatGPT |
| `codex update` | 更新 Codex CLI |

在 VS Code 工作区里使用时，推荐先进入仓库根目录：

```bash
cd /home/victorkure/workspace/vscode_study
codex
```

如果只想让 Codex 处理某个项目，可以进入对应目录：

```bash
cd /home/victorkure/workspace/vscode_study/java-projects/JtProject-Next
codex
```

Codex 修改文件前会根据当前审批策略请求确认。建议日常开发使用默认的安全模式，不要随意使用跳过审批和沙箱的危险参数。

### 3.6 Codex CLI 添加图片和截图

Codex CLI 支持把图片作为输入一起发给 Codex。常见用途：

- 粘贴或保存报错截图，让 Codex 帮你读错误信息。
- 发送浏览器页面截图，让 Codex 判断页面显示问题。
- 发送 VS Code 终端截图，让 Codex 分析命令报错。
- 发送设计图或 UI 截图，让 Codex 帮你改前端样式。

查看图片参数：

```bash
codex --help
```

可以看到类似参数：

```text
-i, --image <FILE>...
```

#### 方法 1：使用图片路径提问

先把图片放到工作区里，例如：

```bash
mkdir -p tmp/screenshots
```

假设图片路径是：

```text
tmp/screenshots/error.png
```

运行：

```bash
codex -i tmp/screenshots/error.png "请读取这张截图里的错误信息，告诉我原因和修复步骤"
```

也可以附加多张图片：

```bash
codex -i tmp/screenshots/error1.png -i tmp/screenshots/error2.png "比较这两张截图，说明错误有什么变化"
```

#### 方法 2：从 Windows 截图后保存到 WSL 可访问目录

如果你在 Windows 里截图，推荐保存到当前 WSL 工作区，例如：

```text
\\wsl.localhost\Ubuntu\home\victorkure\workspace\vscode_study\tmp\screenshots
```

然后在 WSL 终端中确认：

```bash
ls ~/workspace/vscode_study/tmp/screenshots
```

使用：

```bash
cd ~/workspace/vscode_study
codex -i tmp/screenshots/error.png "帮我分析截图中的报错"
```

#### 方法 3：从 Windows 下载或桌面目录读取图片

WSL 可以访问 Windows 的 C 盘，路径通常是：

```bash
/mnt/c/Users/你的Windows用户名/Desktop
/mnt/c/Users/你的Windows用户名/Downloads
```

例如图片在 Windows 下载目录：

```bash
ls /mnt/c/Users/你的Windows用户名/Downloads
```

复制到当前工作区：

```bash
mkdir -p tmp/screenshots
cp "/mnt/c/Users/你的Windows用户名/Downloads/error.png" tmp/screenshots/
```

再发给 Codex：

```bash
codex -i tmp/screenshots/error.png "这张截图里的错误是什么意思？请给我修复命令"
```

如果 Windows 用户名不确定，可以查看：

```bash
ls /mnt/c/Users
```

#### 方法 4：VS Code 里快速保存图片

在 VS Code 中可以这样做：

1. 在资源管理器中右键工作区目录，创建 `tmp/screenshots`。
2. 从 Windows 文件夹把图片拖进 VS Code 的 `tmp/screenshots` 目录。
3. 在终端执行：

```bash
codex -i tmp/screenshots/图片文件名.png "请分析这张截图"
```

#### 方法 5：粘贴图片错误信息的推荐流程

如果遇到错误截图，推荐这样问：

```bash
codex -i tmp/screenshots/error.png "这是我在 VS Code WSL 终端里运行命令时的报错截图。请先逐行读出关键错误，再告诉我为什么会报错，最后给出可以直接复制执行的修复命令。"
```

如果是浏览器页面显示问题：

```bash
codex -i tmp/screenshots/page.png "这是前端页面截图。请判断 UI 哪里显示不正确，并告诉我应该检查哪些文件。"
```

如果是 Markdown / Mermaid 图不显示：

```bash
codex -i tmp/screenshots/mermaid-error.png "这是 Markdown 预览里的 Mermaid 显示错误截图。请分析可能原因，并检查当前项目里的 Mermaid 文件和引用。"
```

#### 图片使用注意事项

- 图片路径建议不要有空格；如果有空格，要用引号包起来。
- 推荐把截图放到项目内的 `tmp/screenshots/`，路径短、好输入。
- 如果图片在 Windows 路径下，先复制到 WSL 工作区再使用，稳定性更好。
- 截图里如果包含账号、Token、API Key、邮箱验证码等敏感信息，先打码再发送。
- `codex -i` 后面仍然要写清楚你希望 Codex 做什么，不要只给图片。

带空格路径示例：

```bash
codex -i "tmp/screenshots/error screen.png" "请分析这张错误截图"
```

### 3.7 GitHub Copilot CLI

GitHub Copilot CLI 可以在 VS Code 终端里直接使用 Copilot 来解释命令、生成命令和和当前工作区对话。旧版 `gh copilot` 已经退役，新的推荐方式是直接使用 Copilot CLI。

安装方式可任选其一：

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

```bash
npm install -g @github/copilot
```

```powershell
winget install GitHub.Copilot
```

验证安装：

```bash
copilot --version
copilot --help
```

首次使用时直接启动：

```bash
cd /home/victorkure/workspace/vscode_study
copilot
```

常见用法：

```text
请帮我解释当前目录的结构，并告诉我应该先看哪些文件
```

如果提示未登录，就按界面提示完成 GitHub 登录流程即可。建议在 VS Code 的集成终端里运行，并先切到目标项目根目录，这样 Copilot 能读取更准确的上下文。

#### 常用命令

```bash
copilot --help
```

查看版本：

```bash
copilot --version
```

进入交互式界面：

```bash
copilot
```

在实验模式下启动：

```bash
copilot --experimental
```

如果你想让它直接围绕当前项目工作，先切到仓库根目录，再执行 `copilot`。如果你在 Windows / WSL 混合环境里工作，优先用 WSL 终端打开当前仓库，这样路径和工具链更一致。

#### 使用技巧

先说目标，再说约束，Copilot 通常会给出更稳定的建议。比如不要只问“怎么修”，而是补上当前目录、报错信息和期望结果。

更推荐的问法是：

```text
请检查当前工作区中的启动脚本，并告诉我如何在 VS Code 终端里启动这个项目
```

如果你想让它帮你分析命令，可以直接把整条命令贴进去：

```text
请解释这条命令的每一部分，并告诉我它会修改什么文件
```

使用时建议注意这些点：

- 在项目根目录启动，避免上下文太小。
- 把报错原文贴完整，尤其是第一行和最后一行。
- 如果涉及 PowerShell、Git Bash、WSL，不要混用命令语法。
- 涉及敏感信息时，先把 Token、密码、邮箱和内部地址打码。
- 如果 Copilot 给出的命令可能有破坏性，先人工确认再执行。

## 4. 在 VS Code 中使用终端

打开终端：

- 快捷键：`Ctrl + Shift + \``
- 菜单：`Terminal -> New Terminal`

切换默认终端：

1. 按 `Ctrl + Shift + P`
2. 输入 `Terminal: Select Default Profile`
3. 选择 PowerShell、Git Bash、Command Prompt 或 WSL

推荐选择：

| 场景 | 推荐终端 |
| --- | --- |
| Windows 普通操作 | PowerShell |
| Git 和简单 Linux 命令 | Git Bash |
| Java / Python / Docker / 服务器风格开发 | WSL Ubuntu |
| 前端 Next.js / React | PowerShell 或 WSL |

## 5. 用 CLI 打开项目

进入工作目录：

```powershell
cd D:\dev\source_code\vscode_study
code .
```

打开指定项目：

```powershell
code D:\dev\source_code\vscode_study\java-projects\JtProject-Next
```

在 WSL 中：

```bash
cd ~/workspace/vscode_study
code .
```

## 6. CLI 编程基本工作流

一个常见开发流程如下：

```text
打开项目
-> 查看状态
-> 安装依赖
-> 运行项目
-> 修改代码
-> 执行测试
-> 提交 Git
```

对应命令示例：

```powershell
git status
npm install
npm run dev
npm test
git add .
git commit -m "implement feature"
git push
```

Java 项目示例：

```powershell
git status
.\mvnw.cmd test
.\mvnw.cmd spring-boot:run
git add .
git commit -m "update java project"
```

Python 项目示例：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
pytest
```

## 7. VS Code 插件建议

建议安装：

| 插件 | 用途 |
| --- | --- |
| Chinese (Simplified) Language Pack | 中文界面 |
| GitLens | Git 历史查看 |
| ESLint | JavaScript / TypeScript 检查 |
| Prettier | 前端格式化 |
| Python | Python 开发 |
| Pylance | Python 类型提示 |
| Extension Pack for Java | Java 开发 |
| Markdown All in One | Markdown 写作 |
| Docker | Docker 文件与容器管理 |
| WSL | 从 Windows 连接 WSL |

## 8. 常用 CLI 命令速查

### 文件和目录

```powershell
pwd
ls
cd path\to\project
mkdir docs
```

PowerShell 中查看文件内容：

```powershell
Get-Content README.md
```

Git Bash / WSL 中查看文件内容：

```bash
cat README.md
sed -n '1,120p' README.md
```

### 搜索

推荐使用 `rg`：

```powershell
rg "keyword"
rg --files
rg -n "TODO" .
```

### 端口检查

PowerShell：

```powershell
netstat -ano | findstr :3000
```

WSL：

```bash
ss -ltnp | grep 3000
```

## 9. 前端项目实战

进入前端目录：

```powershell
cd D:\dev\source_code\vscode_study\java-projects\JtProject-Next\frontend
```

安装依赖：

```powershell
npm install
```

启动开发服务器：

```powershell
npm run dev
```

浏览器打开：

```text
http://localhost:3000
```

构建检查：

```powershell
npm run build
```

## 10. Java Spring Boot 项目实战

进入项目目录：

```powershell
cd D:\dev\source_code\vscode_study\java-projects\JtProject-Next
```

编译：

```powershell
.\mvnw.cmd -DskipTests compile
```

启动：

```powershell
.\mvnw.cmd spring-boot:run
```

如果项目使用指定端口，浏览器访问项目 README 中说明的地址。

## 11. Python CLI 脚本实战

新建脚本：

```powershell
mkdir cli-demo
cd cli-demo
code .
```

创建 `hello.py`：

```python
import argparse

parser = argparse.ArgumentParser(description="Simple CLI demo")
parser.add_argument("name", help="Your name")
args = parser.parse_args()

print(f"Hello, {args.name}!")
```

运行：

```powershell
python hello.py Victor
```

这就是最小 CLI 程序：从终端接收参数，执行逻辑，输出结果。

## 12. 常见问题

### code 命令不可用

重新安装 VS Code 时勾选 PATH，或在 VS Code 命令面板安装 `code` 命令。

### npm 命令不可用

确认 Node.js 已安装，并重新打开终端：

```powershell
node -v
npm -v
```

### PowerShell 无法激活 Python 虚拟环境

如果出现执行策略错误，可以使用：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然后重新执行：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 命令在 VS Code 终端和系统终端表现不同

通常是 PATH 或默认终端不同。检查：

```powershell
$env:Path
```

并在 VS Code 中重新选择默认终端 Profile。

## 13. 学习顺序建议

1. 会用 `cd`、`ls`、`pwd`、`code .`
2. 会用 `git status`、`git add`、`git commit`
3. 会启动一个前端项目：`npm install`、`npm run dev`
4. 会启动一个 Java 项目：`mvnw spring-boot:run`
5. 会创建一个 Python CLI 脚本
6. 会用 `codex` 在当前工作区询问、修改、审查代码
7. 会看报错、复制关键错误、搜索和定位文件

掌握这些之后，VS Code 就不只是编辑器，而是一个完整的 CLI 编程工作台。
