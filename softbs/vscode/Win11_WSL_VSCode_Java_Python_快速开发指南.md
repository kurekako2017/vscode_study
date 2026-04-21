# Win11 + WSL + VS Code + Java/Python 快速开发指南

> 适用场景：你已经在 Windows 11 上安装好了 WSL，但还不清楚日常应该怎么用它来开发 Java、Python 项目。

---

## 1. 先建立一个正确认知

推荐你的日常开发方式是：

- Windows 负责桌面、VS Code、浏览器
- WSL Ubuntu 负责终端、Git、Java、Python、运行项目
- VS Code 通过 `Remote - WSL` 连接到 Ubuntu 环境

一句话理解：

`你是在 Windows 上打开 VS Code，但真正的开发环境是在 WSL 里的 Linux。`

---

## 2. 你每天最常用的几个命令

在 Windows PowerShell 里：

```powershell
wsl -l -v
wsl -d Ubuntu
wsl --shutdown
```

作用：

- `wsl -l -v`：查看 WSL 发行版和版本
- `wsl -d Ubuntu`：进入 Ubuntu
- `wsl --shutdown`：关闭全部 WSL 实例

如果你已经装好了 Ubuntu，平时最常用的其实就是：

```powershell
wsl -d Ubuntu
```

---

## 3. 第一次进入 Ubuntu 后先做什么

进入 Ubuntu：

```powershell
wsl -d Ubuntu
```

先更新系统：

```bash
sudo apt update
sudo apt upgrade -y
```

说明：

- `sudo` 会要求你输入你安装 Ubuntu 时设置的 Linux 密码
- 输入密码时屏幕上不会显示字符，这是正常现象

---

## 4. WSL 里“登录”到底是什么意思

很多初学者会把“登录”搞混，这里拆开说：

### 4.1 登录 Ubuntu

你执行：

```powershell
wsl -d Ubuntu
```

就是进入 Ubuntu 开发环境。

### 4.2 登录 root 或管理员权限

普通情况下不需要真的切换到 root。

安装软件时直接用：

```bash
sudo <命令>
```

例如：

```bash
sudo apt install -y git
```

### 4.3 登录 GitHub

如果你要拉代码、推代码，需要配置 Git：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

如果你以后要推送到 GitHub，建议再配 SSH key。

先检查：

```bash
ls -la ~/.ssh
```

没有的话可以生成：

```bash
ssh-keygen -t ed25519 -C "你的邮箱"
```

查看公钥：

```bash
cat ~/.ssh/id_ed25519.pub
```

复制内容到 GitHub 的 SSH keys 页面即可。

---

## 5. VS Code 怎么连接 WSL

### 5.1 Windows 侧需要安装什么

先安装：

- VS Code
- 扩展 `Remote - WSL`
- Java 开发时建议装 `Extension Pack for Java`
- Python 开发时建议装 `Python`

### 5.2 最推荐的打开方式

先进入 Ubuntu：

```powershell
wsl -d Ubuntu
```

再在 Ubuntu 里执行：

```bash
code .
```

或者先进入你的项目目录再执行：

```bash
cd ~/workspace
code .
```

如果左下角显示：

```text
WSL: Ubuntu
```

就说明你已经是在 WSL 里开发了。

---

## 6. 代码应该放哪里

强烈建议把项目放在 WSL 的 Linux 文件系统里，而不是放在 `/mnt/c/...`。

推荐目录：

```bash
mkdir -p ~/workspace
cd ~/workspace
```

例如：

```bash
~/workspace/java-demo
~/workspace/python-demo
~/workspace/vscode_study
```

不太推荐长期把开发仓库放在：

```bash
/mnt/c/Users/...
```

原因：

- Linux 文件权限体验差一些
- 某些依赖、软链接、监听会有兼容问题
- 大型项目性能通常更差

---

## 7. Java 开发环境怎么配

### 7.1 安装 Java 和 Maven

在 Ubuntu 里执行：

```bash
sudo apt install -y openjdk-17-jdk maven
```

检查版本：

```bash
java -version
javac -version
mvn -version
```

如果你的项目明确要求 Java 11，也可以装：

```bash
sudo apt install -y openjdk-11-jdk
```

### 7.2 新建一个最小 Java 项目试运行

```bash
mkdir -p ~/workspace/java-demo/src
cd ~/workspace/java-demo/src
```

创建 `Hello.java`：

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello from WSL Java");
    }
}
```

运行：

```bash
javac Hello.java
java Hello
```

### 7.3 在 VS Code 里怎么运行 Java

如果你已经在 `WSL: Ubuntu` 环境里打开项目：

- 安装 Java 扩展
- 打开 `.java` 文件
- 点击右上角 `Run`
- 或按 `F5`

也可以直接在 VS Code 终端里执行：

```bash
mvn spring-boot:run
```

### 7.4 运行 Spring Boot 项目

例如你的仓库项目：

```bash
cd ~/workspace/vscode_study/java-projects/JtProject
./mvnw spring-boot:run
```

如果是 Windows 仓库当前在 `D:` 盘，你可以先在 Ubuntu 中进入：

```bash
cd /mnt/d/dev/source_code/vscode_study
```

但从长期看，更推荐把仓库复制到：

```bash
~/workspace/vscode_study
```

---

## 8. Python 开发环境怎么配

### 8.1 安装 Python 和常用工具

```bash
sudo apt install -y python3 python3-pip python3-venv
```

检查：

```bash
python3 --version
pip3 --version
```

### 8.2 创建虚拟环境

进入项目目录：

```bash
mkdir -p ~/workspace/python-demo
cd ~/workspace/python-demo
```

创建虚拟环境：

```bash
python3 -m venv .venv
```

激活：

```bash
source .venv/bin/activate
```

激活后你会看到命令行前面出现：

```text
(.venv)
```

安装测试包：

```bash
pip install requests
```

### 8.3 运行一个 Python 文件

创建 `app.py`：

```python
print("Hello from WSL Python")
```

运行：

```bash
python app.py
```

### 8.4 在 VS Code 里怎么运行 Python

如果你是在 `WSL: Ubuntu` 里打开项目：

1. 打开命令面板
2. 选择 `Python: Select Interpreter`
3. 选择 WSL 里的 `.venv/bin/python`
4. 按 `F5` 或点运行

---

## 9. 平时怎么打开和运行项目

推荐日常流程：

### 9.1 打开 WSL

```powershell
wsl -d Ubuntu
```

### 9.2 进入项目目录

```bash
cd ~/workspace/vscode_study
```

### 9.3 用 VS Code 打开

```bash
code .
```

### 9.4 在 VS Code 终端运行项目

Java 项目例子：

```bash
cd java-projects/JtProject
./mvnw spring-boot:run
```

Python 项目例子：

```bash
cd python-projects/ai-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 10. Windows 和 WSL 怎么互相配合

### 10.1 在 WSL 里打开当前目录到资源管理器

```bash
explorer.exe .
```

### 10.2 从 Windows 访问 WSL 文件

资源管理器地址栏输入：

```text
\\wsl$\Ubuntu\home\你的用户名
```

### 10.3 在 Windows 里直接执行 WSL 命令

```powershell
wsl -d Ubuntu -- bash -lc "cd ~/workspace && ls"
```

---

## 11. 最常见问题

### 11.1 `code: command not found`

说明 VS Code 还没有正确接入 WSL。

先确认：

- 已安装 `Remote - WSL`
- 已在 Windows 正常安装 VS Code

然后在 Windows 里先打开 VS Code，再使用命令面板执行：

```text
Remote-WSL: New WSL Window
```

### 11.2 `sudo` 密码输不进去

其实是输入了但不显示。

直接输入密码后按回车即可。

### 11.3 不知道现在是不是在 WSL 里

执行：

```bash
pwd
uname -a
```

如果看到 Linux 路径、Linux 内核信息，就说明你在 WSL 里。

### 11.4 Java 或 Python 明明装了，VS Code 识别不到

大概率是因为你在 Windows 窗口打开了项目，而不是在 `WSL: Ubuntu` 窗口打开。

记住：

`开发语言环境装在 WSL，就要用 WSL 窗口打开项目。`

---

## 12. 适合你的最短上手路径

如果你现在就要开始：

1. Windows 里执行 `wsl -d Ubuntu`
2. Ubuntu 里执行 `mkdir -p ~/workspace`
3. Ubuntu 里执行 `cd ~/workspace`
4. Ubuntu 里执行 `code .`
5. 在 VS Code 安装 `Remote - WSL`、Java、Python 扩展
6. Java 用 `openjdk + maven`
7. Python 用 `python3 + venv + pip`
8. 以后所有构建、运行、调试，尽量都在 WSL 终端里做

---

## 13. 你接下来最推荐看的现有文档

如果你想继续深入，建议再看：

- `softbs/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md`
- `softbs/vscode/VSCode操作指南.md`

这篇文档负责“快速开始”，上面两篇更适合后续扩展。
