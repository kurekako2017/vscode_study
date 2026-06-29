# Windows Git Bash 开发实战教程（Java / Python / LLM）

适用场景：你在 Windows 主机上，准备用 Git Bash 作为日常开发终端，覆盖 Java、Python、大模型应用开发。

## 1. 你会得到什么

这份教程会帮你建立一套可长期复用的开发习惯：

- 用 Git Bash 统一常用命令和脚本入口
- 用一套 Git 配置支持多项目开发
- 在同一终端完成 Java、Python、LLM 项目日常工作
- 避开 Windows 常见坑（换行符、路径、权限、编码）

## 2. 安装与基础设置

## 2.1 安装 Git for Windows

1. 下载并安装 Git for Windows。
2. 安装时建议保持默认组件。
3. 打开 Git Bash，执行：

```bash
git --version
bash --version
```

## 2.2 配置 Git 身份

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
git config --global init.defaultBranch main
git config --global core.autocrlf input
git config --global core.editor "code --wait"
```

说明：

- `core.autocrlf=input`：提交时将 CRLF 转 LF，减少跨平台换行问题。
- `core.editor=code --wait`：让 Git 提交信息可直接在 VS Code 编辑。
## 2.3 建议生成 SSH Key（连接 GitHub）

```bash
ssh-keygen -t ed25519 -C "你的邮箱"
cat ~/.ssh/id_ed25519.pub
```

把公钥内容添加到 GitHub 后测试：

```bash
ssh -T git@github.com
```

## 3. 路径与文件系统认知

Git Bash 下常见路径映射：

- `C:\Users\你的用户名` 对应 `/c/Users/你的用户名`
- 当前工作区示例：`d:\dev\source_code\vscode_study` 对应 `/d/dev/source_code/vscode_study`

常用命令：

```bash
pwd
ls -la
cd /d/dev/source_code/vscode_study
```

## 4. 每日高频 Git Bash 命令

```bash
# Git
git status
git add .
git commit -m "feat: ..."
git pull --rebase
git push

# 文件与搜索
ls -la
find . -name "*.md"
grep -R "关键词" .

# 压缩与校验
zip -r backup.zip ./某目录
sha256sum 文件名
```

如果你安装了 ripgrep，建议优先用：

```bash
rg "关键词"
rg --files
```

## 5. Java 开发（Maven / Spring Boot）

## 5.1 推荐做法

- 优先使用项目自带 Maven Wrapper：`./mvnw`
- JDK 用 Windows 系统安装（如 `winget`），Git Bash 直接复用
- 尽量在项目根目录执行构建命令

## 5.2 检查 Java 环境

```bash
java -version
javac -version
./mvnw -v
```

如果项目没有 `mvnw`，可使用：

```bash
mvn -v
```

## 5.3 常用构建命令

```bash
# 编译 + 测试
./mvnw clean test

# 打包
./mvnw clean package

# Spring Boot 启动
./mvnw spring-boot:run
```

## 5.4 脚本可执行权限（Windows 常见）

某些脚本首次拉取后可能没有执行位：

```bash
chmod +x mvnw
chmod +x scripts/*.sh
```

## 6. Python 开发（venv / pip / uv）

## 6.1 建议做法

- 每个项目一个独立虚拟环境
- 不要把依赖安装到全局 Python
- 将 `.venv/` 加入 `.gitignore`

## 6.2 虚拟环境流程（标准）

```bash
# 在项目目录
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python your_script.py
```

退出环境：

```bash
deactivate
```

## 6.3 使用 uv（可选，更快）

```bash
# 安装 uv 后
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt
```

## 7. 大模型应用开发（API / 本地模型）

## 7.1 API Key 管理（推荐）

只在当前终端会话临时导出，不写死到代码仓库：

```bash
export OPENAI_API_KEY="你的key"
export ANTHROPIC_API_KEY="你的key"
export GEMINI_API_KEY="你的key"
```

查看是否生效：

```bash
env | grep -E "OPENAI|ANTHROPIC|GEMINI"
```

## 7.2 Python 调用模型（最小示例）

```bash
pip install openai
python - << 'PY'
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.responses.create(
    model="gpt-4.1-mini",
    input="请用一句话解释什么是向量数据库"
)
print(resp.output_text)
PY
```

## 7.3 本地模型（例如 Ollama）

如已安装 Ollama：

```bash
ollama list
ollama run qwen2.5:7b
```

## 8. 在 Windows Terminal / VS Code 里调用 Git Bash（推荐体验）

先澄清一个常见误区：Terminal 不等于 cmd。

- Terminal 是终端程序（窗口容器）
- cmd / PowerShell / Git Bash 是在终端里运行的 Shell（命令解释器）

启动差异（你问的“启动方式是否不同”）：

1. 启动 cmd：通常是直接打开“命令提示符”，默认进入 cmd Shell
2. 启动 Windows Terminal：先打开 Terminal 程序，再按 Profile 决定进入哪个 Shell（cmd、PowerShell、Git Bash、WSL）
3. 启动 VS Code 终端：先打开 VS Code，再按默认 Profile 启动指定 Shell

结论：启动入口可以不同，但关键是“最终进入哪个 Shell”，这决定命令语法和开发体验。

如果你希望开发时主要使用一个终端入口，推荐两种方式：

- 方式 A：Windows Terminal 里用 Git Bash（系统级主终端）
- 方式 B：VS Code 内置终端用 Git Bash（编辑器内无缝开发）

这两种方式可以同时存在，你只需要把 Git Bash 设为默认即可。

## 8.1 在 Windows Terminal 中使用 Git Bash

1. 安装好 Git for Windows 后打开 Windows Terminal。
2. 按 `Ctrl + Shift + ,` 打开设置。
3. 在“启动”里把默认配置文件切换到 Git Bash。
4. 新开一个标签页，确认提示符包含 `MINGW64`。

如果下拉列表里没有 Git Bash，可在 `settings.json` 手工添加 Profile（路径按你的安装位置调整）：

```json
{
    "profiles": {
        "list": [
            {
                "guid": "{b2cf50f5-8f87-4b03-a84f-4f2f9f7f7a90}",
                "name": "Git Bash",
                "commandline": "C:\\Program Files\\Git\\bin\\bash.exe -i -l",
                "icon": "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico",
                "startingDirectory": "%USERPROFILE%"
            }
        ]
    },
    "defaultProfile": "Git Bash"
}
```

建议体验优化：

- 字体选支持连字和中文的等宽字体（如 Cascadia Mono + 中文 fallback）
- 开启复制粘贴快捷键与右键粘贴
- 将 `startingDirectory` 设为常用开发目录（例如 `%USERPROFILE%` 或你的代码目录）

## 8.2 在 VS Code 内置终端中使用 Git Bash

在 VS Code 中打开命令面板，执行：

1. `Terminal: Select Default Profile`
2. 选择 `Git Bash`
3. 新建终端验证是否进入 Git Bash

你也可以在 `settings.json` 里显式写入（Windows）：

```json
{
    "terminal.integrated.defaultProfile.windows": "Git Bash",
    "terminal.integrated.profiles.windows": {
        "Git Bash": {
            "path": "C:\\Program Files\\Git\\bin\\bash.exe",
            "args": ["-i", "-l"]
        }
    }
}
```

常用联动方式：

```bash
cd /d/dev/source_code/vscode_study
code .
```

进入项目后直接在 VS Code 终端执行：

- Java：`./mvnw clean test`
- Python：`source .venv/Scripts/activate`
- LLM：`export OPENAI_API_KEY="你的key"`

## 8.3 推荐你采用的终端组合

- Windows Terminal：作为系统级总入口（多标签管理、分屏、跨项目切换）
- VS Code Terminal：作为项目内执行入口（写代码 + 跑命令同屏）

建议日常节奏：

1. 在 Windows Terminal 打开 Git Bash，进入仓库
2. 执行 `code .` 打开工程
3. 在 VS Code 内置 Git Bash 里完成构建、测试、运行

## 8.4 常见体验问题（Terminal / VS Code）

1. 找不到 Git Bash Profile

- 确认 Git 安装目录是否为 `C:\Program Files\Git`
- 手工指定 `bash.exe` 路径后重启 Terminal/VS Code

2. 中文显示或字符宽度不协调

- 切换终端字体并启用 UTF-8
- 使用支持中文的等宽字体组合

3. Ctrl+C 复制和中断冲突

- 终端中 `Ctrl+C` 默认是中断进程
- 复制建议用 `Ctrl+Shift+C`，粘贴用 `Ctrl+Shift+V`

4. 启动目录每次不对

- Windows Terminal 用 `startingDirectory`
- VS Code 可在工作区打开时自动定位到项目根目录

## 9. 常见问题与解决

## 9.1 换行符冲突（CRLF / LF）

症状：脚本报错、提交后大量无意义改动。

处理：

```bash
git config --global core.autocrlf input
git config --global core.eol lf
```

并在仓库内添加 `.gitattributes`（按需）：

```gitattributes
*.sh text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

## 9.2 路径带空格

命令中给路径加引号：

```bash
cd "/d/dev/source code/vscode_study"
```

## 9.3 编码乱码

优先使用 UTF-8 编码保存文件，VS Code 状态栏可切换编码。

## 9.4 权限与执行失败

脚本执行前确认：

```bash
chmod +x ./script.sh
./script.sh
```

## 10. 推荐你的落地流程（每天）

```bash
# 1) 进入仓库
cd /d/dev/source_code/vscode_study

# 2) 更新代码
git pull --rebase

# 3) 进入具体项目（示例）
cd python-projects/ai-lab

# 4) 激活环境并运行
source .venv/Scripts/activate
python 01_python_basics.py

# 5) 提交变更
cd /d/dev/source_code/vscode_study
git add .
git commit -m "chore: update learning notes"
git push
```

## 11. 最小检查清单

- Git 身份配置完成
- SSH Key 可连接 GitHub
- Java 和 Python 命令可在 Git Bash 正常执行
- 项目可以在 Git Bash 内完成构建/运行
- API Key 通过环境变量注入，无明文入库

完成以上五项后，你就可以把 Git Bash 作为 Windows 上的主力开发终端长期使用。

## 12. 一键环境检查脚本（Git Bash）

为了减少每次手工检查成本，你可以直接使用仓库内脚本：

`/d/dev/source_code/vscode_study/scripts/wsl/dev-check-gitbash.sh`

使用步骤：

```bash
cd /d/dev/source_code/vscode_study
chmod +x scripts/wsl/dev-check-gitbash.sh
./scripts/wsl/dev-check-gitbash.sh
```

输出说明：

- `[PASS]`：该项已就绪
- `[WARN]`：可选项未安装或当前目录未命中（例如不在某个具体项目目录）
- `[FAIL]`：关键项缺失（例如 Git 未安装）

如果脚本返回非 0，表示存在失败项。你可以先处理失败项，再继续开发。

建议在下面几个时机运行一次：

1. 新机器初始化后
2. 更新 Git/JDK/Python 后
3. 切换到新的 Java/Python/LLM 项目前

## 13. Windows Terminal 配套命令别名（提效）

仓库已提供 Git Bash 别名文件：

`/d/dev/source_code/vscode_study/scripts/wsl/gitbash_aliases.sh`

### 13.1 临时加载（当前会话生效）

```bash
source /d/dev/source_code/vscode_study/scripts/wsl/gitbash_aliases.sh
```

### 13.2 永久加载（每次打开 Git Bash 自动生效）

把下面一行追加到 `~/.bashrc`：

```bash
echo 'source /d/dev/source_code/vscode_study/scripts/wsl/gitbash_aliases.sh' >> ~/.bashrc
source ~/.bashrc
```

### 13.3 常用别名

- `gs`：`git status -sb`
- `gp`：`git push`
- `gpl`：`git pull --rebase`
- `gcm "msg"`：`git commit -m "msg"`
- `venvon`：自动激活 `.venv` 或 `venv`
- `venvoff`：退出虚拟环境
- `devcheck`：运行开发环境一键检查脚本

快速验证：

```bash
gs
venvon
devcheck
```
