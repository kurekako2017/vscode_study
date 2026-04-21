# Win11 + WSL + VS Code 当前仓库实战教程

> 目标：基于你现在这个仓库 `vscode_study`，手把手说明如何在 WSL 里打开项目、运行 Java 项目、运行 Python 项目。

---

## 1. 这篇文档解决什么问题

前一篇快速指南讲的是通用方法，这一篇只做一件事：

`把你当前这个仓库，在 Win11 + WSL + VS Code 里真正跑起来。`

适合你现在这种情况：

- Windows 11 已安装 WSL
- 想用 VS Code 连 WSL 开发
- 想跑这个仓库里的 Java 和 Python 项目

---

## 2. 先确认你当前仓库在哪

你现在 Windows 侧的仓库路径是：

```text
d:\dev\source_code\vscode_study
```

在 WSL Ubuntu 里，它通常对应：

```bash
/mnt/d/dev/source_code/vscode_study
```

也就是说：

- Windows 路径：`d:\dev\source_code\vscode_study`
- WSL 路径：`/mnt/d/dev/source_code/vscode_study`

### 2.1 你这台机器的目录地图（已实测）

- WSL 发行版：`Ubuntu (WSL2)`
- WSL 用户：`victorkure`
- WSL Home：`/home/victorkure`
- Windows 里访问 WSL Home：`\\wsl$\Ubuntu\home\victorkure`

常用“目录场所”建议：

1. 只想快速复用当前仓库：继续用 `/mnt/d/dev/source_code/vscode_study`
2. 长期开发（推荐）：放到 `/home/victorkure/workspace/vscode_study`

### 2.2 如何打开这些目录

在 WSL 终端里打开 Windows 资源管理器：

```bash
# 打开当前目录
explorer.exe .

# 打开 WSL Home
explorer.exe \\\\wsl$\\Ubuntu\\home\\victorkure
```

在 Windows 资源管理器地址栏直接输入：

```text
\\wsl$\Ubuntu\home\victorkure
```

---

## 3. Terminal 怎么启动（Windows Terminal / cmd / PowerShell）

你可以任选一种入口，最终目标都是进入 Ubuntu：

### 3.1 从 Windows Terminal 启动 Ubuntu（推荐）

1. 打开 Windows Terminal
2. 点击 `+` 旁边下拉，选择 `Ubuntu`
3. 或将默认配置文件设置为 `Ubuntu` 后，新建标签页即自动进入

命令行方式（Windows 里执行）：

```powershell
wt -p Ubuntu
```

### 3.2 从 cmd / PowerShell 启动 Ubuntu

```powershell
wsl -d Ubuntu
```

直接进入 Home：

```powershell
wsl -d Ubuntu --cd ~
```

直接进入当前仓库：

```powershell
wsl -d Ubuntu --cd /mnt/d/dev/source_code/vscode_study
```

### 3.3 为什么打开后还是“命令提示符”

这是因为你打开的是 `cmd` 标签页，不是 Ubuntu 标签页。处理方法：

1. 关闭当前 `命令提示符` 标签页
2. 新建标签页时手工选择 `Ubuntu`
3. 或在设置里把默认 Profile 固定成 `Ubuntu`

快速自检当前是否在 WSL：

```bash
echo $WSL_DISTRO_NAME
uname -a
pwd
```

如果看到 Linux 内核信息、路径是 `/home/...` 或 `/mnt/...`，说明你已在 WSL。

---

## 4. 先用最简单方式在 WSL 里打开当前仓库

### 3.1 进入 Ubuntu

在 Windows PowerShell：

```powershell
wsl -d Ubuntu
```

### 3.2 进入当前仓库

在 Ubuntu 终端：

```bash
cd /mnt/d/dev/source_code/vscode_study
pwd
```

如果输出是：

```text
/mnt/d/dev/source_code/vscode_study
```

说明你已经成功进到这个仓库了。

### 3.3 用 VS Code 以 WSL 模式打开

继续执行：

```bash
code .
```

打开后确认左下角显示：

```text
WSL: Ubuntu
```

如果是这样，说明你现在不是在 Windows 本地开发，而是在 WSL 环境里开发。

---

## 5. 更推荐的长期方案：把仓库复制到 WSL 内

虽然你可以直接用 `/mnt/d/...` 开发，但长期更推荐复制到：

```bash
~/workspace/vscode_study
```

### 5.1 一键初始化 WSL 本地仓库

如果你想把当前仓库直接复制到 WSL 本地，可以先运行：

```bash
bash ./scripts/wsl/init-wsl-local-repo.sh
```

默认会把：

- 源仓库：`/mnt/d/dev/source_code/vscode_study`
- 目标仓库：`~/workspace/vscode_study`

复制完成后，再切换到本地模式启动：

```bash
scripts\wsl\start-wsl-vscode-dev.bat local
```

### 5.2 创建工作目录

```bash
mkdir -p ~/workspace
cd ~/workspace
```

### 5.3 复制当前仓库

```bash
cp -r /mnt/d/dev/source_code/vscode_study ~/workspace/
```

复制完成后进入：

```bash
cd ~/workspace/vscode_study
code .
```

### 5.4 为什么更推荐这样

- 依赖安装更稳定
- 文件监听通常更正常
- Git、软链接、脚本权限更像真实 Linux 环境
- 大项目性能一般更好

如果你只是先试一下，可以先直接用 `/mnt/d/...`。  
如果你后面准备长期开发，建议切到 `~/workspace/vscode_study`。

---

## 6. VS Code 里建议先装的扩展

在 `WSL: Ubuntu` 窗口里安装：

- `Remote - WSL`
- `Extension Pack for Java`
- `Python`

可选：

- `Pylance`
- `REST Client`
- `Markdown All in One`
- `GitLens`

注意：

`扩展最好安装到 WSL 环境里，不只是安装到 Windows 本地。`

---

## 7. 先配置 Java 运行环境

### 6.1 在 Ubuntu 安装 Java 和 Maven

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk maven
```

检查：

```bash
java -version
javac -version
mvn -version
```

如果某些项目要求 Java 11，也可以再装：

```bash
sudo apt install -y openjdk-11-jdk
```

---

## 8. 在 WSL 里跑 JtProject

### 7.1 进入项目目录

如果你直接使用 Windows 仓库映射：

```bash
cd /mnt/d/dev/source_code/vscode_study/java-projects/JtProject
```

如果你已经复制到 WSL：

```bash
cd ~/workspace/vscode_study/java-projects/JtProject
```

### 7.2 启动项目

Linux / WSL 下运行：

```bash
./mvnw spring-boot:run
```

或者如果 wrapper 不方便，也可以：

```bash
mvn spring-boot:run
```

### 7.3 打开页面

启动成功后访问：

```text
http://localhost:8082/
```

管理员登录页：

```text
http://localhost:8082/admin/login
```

### 7.4 默认账号

- 管理员：`admin / 123`
- 普通用户：`lisa / 765`

### 7.5 你要知道的一个现实情况

这个原始 `JtProject` 默认使用远程 MySQL：

```text
192.168.10.2:3306/ecommjava
```

所以如果你在 WSL 里运行时连不上数据库，不一定是 WSL 坏了，而是：

- 远程数据库没有开
- WSL 当前网络访问不到这个 IP
- 数据库账号密码或配置不通

这时你可以先：

1. 优先学习跑 `JtProject-Thymeleaf`
2. 或跑 `JtProject-React`
3. 或跑 `JtProject-Vue`

因为这些变体版更偏学习用途，环境通常更容易本地化。

---

## 9. 在 WSL 里跑 JtProject-Thymeleaf

### 8.1 进入目录

```bash
cd ~/workspace/vscode_study/java-projects/JtProject-Thymeleaf
```

如果你还没复制仓库，也可以先用：

```bash
cd /mnt/d/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf
```

### 8.2 启动

```bash
./mvnw spring-boot:run
```

### 8.3 访问

```text
http://localhost:8085/
```

这个项目更适合学习：

- JSP 和 Thymeleaf 对照
- 服务端模板渲染
- Controller -> Service -> DAO -> 模板 页面链路

---

## 10. 在 WSL 里跑 Python 项目

这份仓库里可以先拿：

```text
python-projects/ai-lab
```

做练手。

### 9.1 进入目录

```bash
cd ~/workspace/vscode_study/python-projects/ai-lab
```

或者：

```bash
cd /mnt/d/dev/source_code/vscode_study/python-projects/ai-lab
```

### 9.2 安装 Python 基础环境

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 9.3 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

激活后再安装依赖：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 9.4 运行示例

```bash
python 01_python_basics.py
python 02_numpy_intro.py
python 06_ml_intro.py
```

### 9.5 在 VS Code 里运行 Python

在 `WSL: Ubuntu` 窗口中：

1. 打开命令面板
2. 选择 `Python: Select Interpreter`
3. 选择这个项目里的 `.venv/bin/python`
4. 打开任意 `.py` 文件
5. 点击运行或按 `F5`

---

## 11. 你每天可以照抄的实际工作流

### 10.1 开 Java 项目

```powershell
wsl -d Ubuntu
```

```bash
cd ~/workspace/vscode_study
code .
```

VS Code 打开后，终端中执行：

```bash
cd java-projects/JtProject-Thymeleaf
./mvnw spring-boot:run
```

### 10.2 开 Python 项目

```powershell
wsl -d Ubuntu
```

```bash
cd ~/workspace/vscode_study
code .
```

VS Code 打开后，终端中执行：

```bash
cd python-projects/ai-lab
source .venv/bin/activate
python 01_python_basics.py
```

---

## 12. 怎么判断自己有没有“用对”

如果下面这些都成立，说明你用法基本是对的：

- VS Code 左下角显示 `WSL: Ubuntu`
- 项目路径是 Linux 路径或 `/mnt/d/...` 路径
- 终端里 `uname -a` 显示 Linux
- Java 用 Ubuntu 里的 JDK
- Python 用 Ubuntu 里的 `.venv`
- 运行命令都在 WSL 终端里执行

---

## 13. 常见问题

### 12.1 `./mvnw: Permission denied`

执行：

```bash
chmod +x mvnw
./mvnw spring-boot:run
```

### 12.2 `JAVA_HOME` 相关报错

先看 Java 安装位置：

```bash
readlink -f /usr/bin/java
```

通常不需要手动配，但如果要配置，可以放到 `~/.bashrc`：

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

然后执行：

```bash
source ~/.bashrc
```

### 12.3 `pip install` 很慢

先不要怀疑 VS Code，通常是网络或镜像源问题。

你可以先正常重试，或者后面再单独配置 `pip` 镜像。

### 12.4 浏览器打不开 `localhost`

如果 Spring Boot 在 WSL 里监听成功，Windows 浏览器通常能直接访问 `http://localhost:端口`。

如果不行，先检查：

```bash
ss -ltnp | grep 8082
ss -ltnp | grep 8085
```

---

## 14. 给你的实际建议

如果你是为了尽快上手，不要一开始就追求“所有项目都一次跑通”。

最推荐顺序：

1. 先让 `WSL + VS Code` 打开当前仓库成功
2. 再让 Python 项目 `ai-lab` 跑通
3. 再让 `JtProject-Thymeleaf` 跑通
4. 最后再挑战原始 `JtProject`

这样成功率最高，也最不容易被数据库和旧项目环境卡住。

---

## 15. 最后给你一个最小成功清单

今天你至少做到这 4 步，就算已经入门成功：

1. `wsl -d Ubuntu`
2. `cd ~/workspace/vscode_study`
3. `code .`
4. 在 WSL 终端里跑通一个 Java 或 Python 项目

如果你能完成这一步，你之后学 Java、Python、Docker、Git，都会顺很多。

---

## 16. 开机后 30 秒进入开发状态（推荐固定流程）

这一节的目标是：你每次开机后，几乎不用思考就能进入可开发状态。

### 16.1 一次性设置（只做一次）

1. Windows Terminal 默认 Profile 设为 `Ubuntu`
2. VS Code 默认终端 Profile 设为 `Ubuntu (WSL)`
3. 把仓库固定在以下二选一路径：

- 方案 A（快速）：`/mnt/d/dev/source_code/vscode_study`
- 方案 B（长期推荐）：`/home/victorkure/workspace/vscode_study`

### 16.2 每天启动（30 秒版）

步骤 1：打开 Windows Terminal（应直接进入 Ubuntu）

如果没有直接进 Ubuntu，手工执行：

```powershell
wsl -d Ubuntu --cd /mnt/d/dev/source_code/vscode_study
```

步骤 2：在 WSL 里打开 VS Code

```bash
code .
```

步骤 3：VS Code 终端确认是 WSL

```bash
echo $WSL_DISTRO_NAME
uname -a
pwd
```

如果输出显示 Linux 且路径是 `/home/...` 或 `/mnt/...`，说明环境正确。

### 16.3 首次自检（每天可选，30 秒）

```bash
cd /mnt/d/dev/source_code/vscode_study
bash ./scripts/wsl/dev-check-gitbash.sh
```

说明：这个脚本主要检查开发工具可用性（Git/Java/Python/LLM 变量等）。

### 16.4 进入具体项目（按需）

Java 示例：

```bash
cd /mnt/d/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf
./mvnw spring-boot:run
```

Python 示例：

```bash
cd /mnt/d/dev/source_code/vscode_study/python-projects/ai-lab
source .venv/bin/activate
python 01_python_basics.py
```

### 16.5 两个常用兜底命令

如果你怀疑当前不在 Ubuntu：

```powershell
wsl -d Ubuntu
```

如果你想直接打开 WSL 家目录：

```text
\\wsl$\Ubuntu\home\victorkure
```

---

## 17. 用 D:\dev\source_code 在 WSL 继续开发（映射实战）

你的 Windows 开发根目录是：

```text
D:\dev\source_code
```

在 WSL 里默认映射为：

```bash
/mnt/d/dev/source_code
```

### 17.1 先确认映射是否存在

```bash
ls -la /mnt/d/dev/source_code
```

如果能看到目录内容，说明映射正常。

### 17.2 直接在映射目录开发（最快）

```bash
cd /mnt/d/dev/source_code/vscode_study
code .
```

适合场景：

- 你希望继续沿用 Windows 目录结构
- 你已经有大量项目都在 `D:\dev\source_code`

### 17.3 给映射目录做一个短链接（推荐）

```bash
ln -s /mnt/d/dev/source_code ~/devsrc
cd ~/devsrc/vscode_study
```

这样以后就不用每次敲很长路径。

### 17.4 何时迁移到 WSL 本地目录

如果你遇到以下问题，再迁移到 `/home/victorkure/workspace`：

- 文件监听不稳定
- Python/Node 大量小文件场景性能不理想
- 依赖安装速度明显慢

---

## 18. 一键启动脚本（双击后自动拉起 Ubuntu + 打开仓库 + 启动 VS Code）

已新增脚本：

`scripts/wsl/start-wsl-vscode-dev.bat`

脚本行为：

1. 拉起 Ubuntu（WSL）
2. 打开一个 Ubuntu 终端标签（若系统安装了 Windows Terminal）
3. 自动在 WSL 路径 `/mnt/d/dev/source_code/vscode_study` 执行 `code .`

脚本现支持两种模式：

1. `mnt`：使用映射目录 `/mnt/d/dev/source_code/vscode_study`（默认）
2. `local`：使用 WSL 本地目录 `/home/victorkure/workspace/vscode_study`

### 18.1 直接使用

在资源管理器双击：

```text
scripts\wsl\start-wsl-vscode-dev.bat
```

或在 PowerShell 运行：

```powershell
./scripts/wsl/start-wsl-vscode-dev.bat
```

使用 WSL 本地模式启动：

```powershell
./scripts/wsl/start-wsl-vscode-dev.bat local
```

如果 `local` 目录不存在，脚本会自动回退到 `mnt` 模式并给出提示。

### 18.2 可定制参数（脚本开头）

你可以按需修改这几个变量：

- `WSL_DISTRO=Ubuntu`
- `WSL_ROOT=/mnt/d/dev/source_code`
- `WSL_REPO=/mnt/d/dev/source_code/vscode_study`

新版变量名如下：

- `WSL_ROOT_MNT` / `WSL_REPO_MNT`
- `WSL_ROOT_LOCAL` / `WSL_REPO_LOCAL`

如果你以后换成 WSL 本地仓库，把 `WSL_REPO` 改成：

```text
/home/victorkure/workspace/vscode_study
```

---

## 19. GitHub 同步到 WSL 开发模式（适合你当前目录已同步）

你现在的前提是：`D:\dev\source_code` 下面的仓库已经和 GitHub 基本同步。

这时可以用两种模式：

### 19.1 模式 A：WSL 本地仓库为主（推荐长期）

思路：在 WSL 里重新 `clone` 一份，日常只在 WSL 这一份开发。

优点：

- Linux 工具链兼容性最好
- 大量小文件项目性能通常更稳定
- 避免 Windows/WSL 双边同时改动导致冲突

操作：

```bash
mkdir -p ~/workspace
cd ~/workspace
git clone <你的仓库SSH或HTTPS地址> vscode_study
cd vscode_study
code .
```

Windows 一键启动可直接改用：

```powershell
./scripts/wsl/start-wsl-vscode-dev.bat local
```

后续开发流程：

```bash
git pull --rebase
# 开发 + 提交
git push
```

### 19.2 模式 B：Windows 工作副本 + WSL 通过 GitHub 同步

思路：继续保留 `D:\dev\source_code\vscode_study` 为主要副本，WSL 里另外保留一份，通过 GitHub 做桥接同步。

建议规则：

1. 同一时间只在一侧改代码（Windows 或 WSL 二选一）
2. 切换开发侧前，先 `push` 当前侧，再到另一侧 `pull --rebase`
3. 不要在两侧同时改同一文件后再合并

Windows 侧（示例）：

```bash
git add .
git commit -m "feat: ..."
git push
```

WSL 侧切换前同步：

```bash
cd ~/workspace/vscode_study
git pull --rebase
```

WSL 开发完成后回推：

```bash
git add .
git commit -m "feat: ..."
git push
```

然后 Windows 侧再拉取：

```bash
cd /mnt/d/dev/source_code/vscode_study
git pull --rebase
```

Windows 一键启动继续用默认即可：

```powershell
./scripts/wsl/start-wsl-vscode-dev.bat
```

### 19.3 你该选哪种

- 如果你准备长期做 Java/Python/LLM：优先 `模式 A`
- 如果你现在必须沿用 Windows 工具链：先用 `模式 B` 过渡

### 19.4 搭配一键脚本的建议

如果你采用 `模式 A`，建议把一键脚本中的 `WSL_REPO` 改为：

```text
/home/victorkure/workspace/vscode_study
```

如果采用 `模式 B`，保持当前默认值即可：

```text
/mnt/d/dev/source_code/vscode_study
```
