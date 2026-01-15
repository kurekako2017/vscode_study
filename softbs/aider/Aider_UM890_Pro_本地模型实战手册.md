# Aider 本地 AI 编程助手使用手册  
## —— UM890 Pro · Windows 11 Pro · 32GB 内存 · 本地模型专用版

> **适用对象**  
> - 设备：UM890 Pro（32GB RAM）  
> - 系统：Windows 11 Pro  
> - 使用方式：Aider + 本地大模型（Ollama / LM Studio）  
> - 模型：  
>   - DeepSeek-Coder V2 Lite 16B（Q4 / Q5）  
>   - Qwen2.5-Coder 14B（Q4 / Q5）

---

## 一、整体推荐架构（稳定 & 高性价比）

```
┌──────────────┐
│   Aider CLI  │
└──────┬───────┘
       │ OpenAI Compatible API
┌──────▼───────┐
│ Ollama / LM  │
│   Studio     │
└──────┬───────┘
       │
┌──────▼────────────────────┐
│ DeepSeek / Qwen 本地模型   │
└───────────────────────────┘
```

**为什么这样配？**
- Aider 原生支持 OpenAI API 协议
- Ollama / LM Studio 都可直接提供兼容接口
- 14B–16B Q4/Q5 非常适合 32GB 内存的 UM890 Pro

---

## 二、基础环境准备（Windows 11）

### 1️⃣ 安装 Python（必需）

推荐 **Python 3.10 或 3.11**

```powershell
python --version
```

若未安装：  
👉 https://www.python.org/downloads/windows/

> 安装时务必勾选：**Add Python to PATH**

---

### 2️⃣ 安装 Git

```powershell
git --version
```

下载：https://git-scm.com/download/win

---

## 三、安装 Aider（本地版）

```powershell
pip install --upgrade pip
pip install aider-chat
```

验证：

```powershell
aider --version
```

---

## 四、本地模型部署（强烈推荐 Ollama）

### 方案 A：Ollama（最稳妥）

#### 1️⃣ 安装 Ollama

👉 https://ollama.com/download/windows

安装完成后：

```powershell
ollama --version
```

---

#### 2️⃣ 拉取模型（任选 Q4 / Q5）

**DeepSeek-Coder V2 Lite 16B**
```powershell
ollama pull deepseek-coder-v2:16b-lite-q4
# 或
ollama pull deepseek-coder-v2:16b-lite-q5
```

**Qwen2.5-Coder 14B**
```powershell
ollama pull qwen2.5-coder:14b-q4
# 或
ollama pull qwen2.5-coder:14b-q5
```

---

#### 3️⃣ 启动 Ollama（默认端口 11434）

```powershell
ollama serve
```

> **不要关闭这个窗口**

---

## 五、Aider 连接本地模型（关键）

### 1️⃣ 设置环境变量（PowerShell）

```powershell
$env:OPENAI_API_BASE="http://localhost:11434/v1"
$env:OPENAI_API_KEY="ollama"
```

（Ollama 不校验 key，随便填）

---

### 2️⃣ 推荐启动命令（重点）

#### ✅ 使用 DeepSeek-Coder（更偏工程 & 重构）

```powershell
aider ^
  --model deepseek-coder-v2:16b-lite-q4 ^
  --edit-format diff ^
  --no-auto-commits ^
  --map-tokens 4096
```

#### ✅ 使用 Qwen2.5-Coder（更强逻辑 & 中文）

```powershell
aider ^
  --model qwen2.5-coder:14b-q4 ^
  --edit-format diff ^
  --no-auto-commits ^
  --map-tokens 4096
```

---

## 六、UM890 Pro 专用参数解释（必看）

| 参数 | 说明 | 推荐原因 |
|----|----|----|
| `--edit-format diff` | 使用 diff 补丁 | 本地模型更稳 |
| `--no-auto-commits` | 不自动 git commit | 防止误提交 |
| `--map-tokens 4096` | 控制上下文规模 | 防止 OOM |
| Q4 / Q5 | 量化模型 | 内存占用合理 |

---

## 七、标准使用流程（实战）

### 1️⃣ 进入你的项目

```powershell
cd D:\projects\my_app
```

### 2️⃣ 首次启动（添加核心文件）

```powershell
aider --add main.py utils.py config.py
```

### 3️⃣ 典型指令示例（直接复制用）

**修 Bug**
> 修复 main.py 中潜在的空指针和边界问题

**重构**
> 重构 utils.py，使其职责更清晰并添加类型注解

**生成测试**
> 为 auth 模块生成 pytest 单元测试

**性能优化**
> 分析这个函数的性能瓶颈并给出优化后的代码

---

## 八、两个模型如何选？（结论版）

### 🔵 DeepSeek-Coder V2 Lite 16B
- ✅ 更像“高级工程师”
- ✅ 擅长：重构 / 多文件 / 架构
- ⛔ 中文表达略弱

**适合：**
> 中大型项目 / 老代码重构

---

### 🟢 Qwen2.5-Coder 14B
- ✅ 中文非常好
- ✅ 逻辑清晰、解释友好
- ⛔ 大型重构略逊

**适合：**
> 日常开发 / 学习 / 中文项目

---

## 九、常见问题（UM890 Pro 实测）

### Q1：卡死 / 无响应？
- 模型太大 → 换 Q4
- 上下文太多 → 减少 --add 文件
- 首次加载模型需 1~2 分钟（正常）

---

### Q2：生成代码不修改文件？
- 确保使用 `--edit-format diff`
- 使用明确指令：  
  > 请**直接修改代码文件**

---

## 十、推荐启动命令速查表（收藏）

```powershell
# DeepSeek（稳定重构）
aider --model deepseek-coder-v2:16b-lite-q4 --edit-format diff --no-auto-commits

# Qwen（中文开发）
aider --model qwen2.5-coder:14b-q4 --edit-format diff --no-auto-commits
```

---

## 十一、进阶建议

- 项目 > 50 个文件：分模块使用 Aider
- 经常 `git diff` 人工确认
- 大改动：一次只让模型做一件事

---

**文档版本**：UM890 Pro 本地模型专用版  
**适配模型**：DeepSeek / Qwen Coder  
**系统**：Windows 11 Pro  
