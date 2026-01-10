# Aider 本地快速上手（UM890 Pro 推荐）⚡️

适用：Windows 11 Pro + UM890 Pro（Ryzen 9 8945HS / 32GB / Radeon 780M）

## 目标
- 在本地用 Ollama 运行模型并供 Aider 或编辑器调用。\
- 重点支持：DeepSeek-Coder V2 Lite 16B（Q4/Q5）和 Qwen2.5-Coder 14B（Q4/Q5）。

---

## 一步到位快速命令（按顺序执行）
1. 创建模型目录（建议放在 D 盘）并设置环境变量：

```powershell
# 创建目录
New-Item -ItemType Directory -Path D:\OllamaModels -Force
# 永久设置用户环境变量（重新登录或重启后生效）
setx OLLAMA_MODELS "D:\\OllamaModels"
```

2. 安装或确认安装 Ollama（官网下载安装或 Linux 一键）：

```powershell
# Windows: 下载并运行 OllamaSetup.exe（在浏览器打开 https://ollama.com/download）
# 检查 ollama 是否可用
ollama --version
```

3. 拉取（或创建）模型（优先使用 Ollama 官方库版本）：

```powershell
# 官方库（若存在）
ollama pull qwen2.5-coder:14b
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M
```

如果你手里有 Q4/Q5 的 GGUF 文件（例如 `deepseek-v2-16b.q4_0.gguf` 或 `qwen2.5-coder-14b.q4_0.gguf`），请用 Modelfile 导入：

```text
# Modelfile
FROM ./deepseek-v2-16b.q4_0.gguf
```

```powershell
ollama create deepseek-local -f Modelfile
ollama run deepseek-local
```

4. 启动 Ollama 服务（供 Aider/编辑器调用）：

```powershell
# 在一个终端里启动服务
ollama serve
# 推荐开启后在另一个终端运行检测
curl http://localhost:11434/
```

5. 快速测试（命令行）：

```powershell
# 测试 Qwen2.5-Coder
ollama run qwen2.5-coder:14b "用 2 行说明这段代码在做什么：\nprint(\"Hello\")"

# 测试 DeepSeek（逻辑分析）
ollama run deepseek-coder-v2:16b-lite-instruct-q4_K_M "阅读下面函数并指出潜在 bug：<your code>"
```

---

## 性能建议 & 常见限制
- 你有 32GB RAM：运行一个 Q4/Q5 量化的 14B 或 16B 模型通常可行，但同时运行多个大模型会吃满内存。建议一次只运行一个大型模型。
- 若遇到内存不足：
  - 使用 Q4/Q5 量化文件（大幅降低显存/内存占用）。
  - 增加 Windows 页面文件（Pagefile）或使用更小模型（如 7B/4B）。
  - 将模型用磁盘（D 盘）存放，确保有足够空间。
- 如果想频繁切换模型，使用 `ollama list` / `ollama rm` 管理本地模型。

---

## 集成到 Aider / 编辑器（概述）
- 启动 `ollama serve`（默认监听 11434）；将 Aider 或编辑器插件的“Local LLM endpoint”配置为 `http://localhost:11434`。
- 如果插件支持直接 Ollama CLI，也可使用 `ollama run` 管道方式。

---

需要我为你把这些快速命令打包成一个 PowerShell 脚本并帮你运行测试吗？
