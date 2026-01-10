# Aider 本地 AI 编程助手使用手册（UM890 Pro 专用版）

> 适用于在 UM890 Pro 等高性能本地电脑上运行 Aider + 本地/云端大模型的完整指南

---

## 一、Aider 是什么？

Aider 是一个开源的**终端式 AI 结对编程助手**，可以让你直接在本地代码仓库中，用自然语言驱动大语言模型完成代码修改、重构、测试和文档编写。

**核心特点：**
- 直接修改真实代码文件（不是只给建议）
- 深度理解整个 Git 项目
- 自动生成 Git 提交
- 支持云端模型 & 本地大模型（Local LLM）
- 非常适合 UM890 Pro 这类高性能本地设备

---

## 二、运行环境要求（UM890 Pro 推荐）

- 操作系统：Windows 11 / Linux / macOS
- Python：3.9+
- Git：2.x
- 网络：本地模型可离线，云模型需联网
- 硬件建议（UM890 Pro）：
  - 内存 ≥ 32GB
  - NVMe SSD ≥ 1TB
  - 若使用本地 LLM，建议搭配 eGPU / 高性能 iGPU

---

## 三、安装 Aider

### 1. 安装 Python 依赖

```bash
pip install --upgrade pip
pip install aider-chat
```

验证安装：

```bash
aider --version
```

---

### 2. （可选）配置 API Key（云模型）

```bash
export OPENAI_API_KEY=你的key
# Windows PowerShell
setx OPENAI_API_KEY "你的key"
```

---

## 四、快速开始

### 1. 进入你的项目目录

```bash
cd your_project
```

### 2. 启动 Aider

```bash
aider
```

进入交互界面后，直接用中文或英文描述你的需求即可。

示例：
> 请为 utils.py 增加异常处理并补充注释

---

## 五、常用操作示例

### 1. 生成代码

> 写一个 Python 函数，用于并发下载多个文件

### 2. 修复 Bug

> 修复 main.py 中可能出现的空指针异常

### 3. 重构代码

> 将这个函数拆分成更清晰的多个函数

### 4. 添加测试

> 为 auth.py 生成 pytest 单元测试

### 5. 生成文档

> 为当前项目生成 README.md

---

## 六、Aider + Git 工作流

Aider 会自动：
- 修改代码文件
- 生成 git diff
- 创建高质量 git commit

常用命令：

```bash
git status
git diff
git log
```

---

## 七、指定模型运行

### 1. 使用云模型

```bash
aider --model gpt-4o
```

### 2. 使用本地模型（示例）

```bash
aider --model llama3
```

> 本地模型通常通过 Ollama / LM Studio / vLLM 提供接口

---

## 八、多文件上下文

让 Aider 同时理解多个文件：

```bash
aider --add main.py utils.py config.py
```

---

## 九、进阶技巧（UM890 Pro 强烈推荐）

### 1. 大项目重构

> 对整个项目进行模块化重构，并保持 API 不变

### 2. 性能优化

> 分析该模块性能瓶颈并给出优化方案

### 3. 自动生成测试覆盖率

> 为所有 public 方法补充测试用例

---

## 十、常见问题

### Q1：Aider 卡住不动？
- 检查模型是否可用
- 项目是否过大（可分批 add 文件）
- 终端编码是否为 UTF-8

### Q2：本地模型响应慢？
- 减少上下文文件数量
- 使用量化模型（Q4 / Q5）
- 确保 UM890 Pro 未降频

---

## 十一、推荐组合（UM890 Pro）

- Aider + Ollama + LLaMA 3
- Aider + LM Studio
- Aider + GPT-4o（联网）

---

## 十二、参考资料

- 官方文档：https://aider.chat/docs/
- GitHub：https://github.com/Aider-AI/aider
- 中文文档：https://aider.doczh.com/

---

**文档版本**：UM890 Pro 本地版  
**生成时间**：2026  
