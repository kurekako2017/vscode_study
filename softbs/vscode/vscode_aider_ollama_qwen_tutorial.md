# VSCode 中使用 Aider + Ollama + Qwen 本地模型完整教程

## 适用环境

- Windows 11
- VSCode
- WSL Ubuntu
- Ollama
- Qwen2.5-Coder
- Aider CLI

---

## 一、安装 Ollama

官网：https://ollama.com

测试：

```bash
ollama list
```

---

## 二、下载模型

### 3B

```bash
ollama pull qwen2.5-coder:3b
```

### 7B

```bash
ollama pull qwen2.5-coder:7b
```

---

## 三、安装 Aider

Ubuntu 24 推荐：

```bash
sudo apt update
sudo apt install pipx -y
pipx ensurepath
```

重新打开终端后：

```bash
pipx install aider-chat
```

测试：

```bash
aider --version
```

---

## 四、配置 Ollama API

如果连接失败：

```bash
export OLLAMA_API_BASE=http://127.0.0.1:11434
```

---

## 五、VSCode 推荐插件

- Python
- Pylance
- Continue.dev
- GitLens
- Remote WSL

---

## 六、最重要：不要在大仓库启动 Aider

错误示例：

```bash
cd ~/workspace/vscode_study
aider ...
```

会导致：

- 扫描 10000+ 文件
- Repo-map 非常慢
- 本地模型卡顿

---

## 七、正确使用方式

创建小项目：

```bash
mkdir -p ~/agent-demo
cd ~/agent-demo
git init
touch main.py
```

---

## 八、推荐启动命令

### 3B

```bash
aider --map-tokens 0 --no-auto-commits --model ollama_chat/qwen2.5-coder:3b
```

### 7B

```bash
aider --map-tokens 0 --no-auto-commits --model ollama_chat/qwen2.5-coder:7b
```

---

## 九、推荐 alias

编辑：

```bash
nano ~/.bashrc
```

加入：

```bash
alias aider3='aider --map-tokens 0 --no-auto-commits --model ollama_chat/qwen2.5-coder:3b'

alias aider7='aider --map-tokens 0 --no-auto-commits --model ollama_chat/qwen2.5-coder:7b'
```

生效：

```bash
source ~/.bashrc
```

---

## 十、基础命令

添加文件：

```text
/add main.py
```

查看 diff：

```text
/diff
```

提交：

```text
/commit
```

---

## 十一、推荐学习路线

1. Calculator Agent
2. 文件 Agent
3. LangChain
4. LangGraph
5. RAG

---

## 十二、Aider vs Continue

### Continue

适合：

- 问问题
- Prompt
- 小代码

### Aider

适合：

- 多文件修改
- workflow
- coding agent
- refactor

