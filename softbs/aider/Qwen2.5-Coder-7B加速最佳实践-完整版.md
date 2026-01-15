# Qwen2.5-Coder:7B 本地加速与 Agent 插件最佳实践

Qwen2.5-Coder 在本地推理时受限于显存（VRAM）、系统物理内存或集成显卡带宽（RAM），容易导致推理速度和响应性能下降。推荐如下高效组合与操作流程：

## 1. 推荐插件：Roo Code（Cline 的增强版）

### 插件模式与环境组合
- **核心插件**：
  - VS Code 插件：Aider（代码编辑/对话式交互）
  - API Provider（API管理）
  - Run Agent Project（批量指令/多模型自动切换）
- **辅助插件**：
  - Page Assistant Project（页面指令流自动化）
  - Agent Provider（多 Agent 协同）

### 典型模式说明
- Aider 插件用于对话模式（D），侧重代码编辑/交互。
- Run Agent Project 用于批量任务、自动化指令流。
- Page Assistant Project 可实现页面级批量指令。
- Agent Provider 支持多 Agent 协同。

---

## 2. 启动与高效执行流程

### 2.1 启动 Ollama（Qwen2.5-Coder:7B）
1. 只加载一个模型，环境变量：
   - `OLLAMA_MAX_LOADED_MODELS=1`
   - `OLLAMA_NUM_GPU=0`（集成显卡建议用 CPU）
2. 启动命令：
   ```powershell
   ollama serve
   ollama pull qwen2.5-coder:7b-instruct-q4_K_M
   ```

### 2.2 VS Code 插件统一管理 Agent 指令
- 推荐 Run Agent Project 插件，支持 Page/指令流自动批处理。
- 可用 Page Assistant Project 实现页面级批量指令。

### 2.3 具体命令与配置
1. 启动 Aider 插件
2. 启动 VS Code 插件统一管理 Agent
3. 启动 Ollama 服务
4. 拉取 Qwen2.5-Coder:7B Q4 量化模型
5. 配置 `.aider.conf.yml`：
   ```yaml
   model: ollama/qwen2.5-coder:7b-instruct-q4_K_M
   ollama-api-base: http://localhost:11434
   auto-commits: false
   stream: true
   edit-format: whole
   ```

---

## 3. 显卡与系统设置（关键步骤）

### 3.1 集成显卡优化
- BIOS 设置 UMA Frame Buffer Size 为 4GB 或 Auto。
- Windows 图形设置：
  - 设置 → 系统 → 显示 → 图形设置，将 ollama.exe 添加到列表，选择“高性能”。

### 3.2 强制 CPU 推理
- 环境变量 `OLLAMA_NUM_GPU=0`，如需用 GPU 则设为 1。

---

## 4. 性能优化建议
- 优先 Q4 量化，推理快、占用低。
- 只加载一个模型，关闭其他大模型。
- 关闭不必要的后台程序，释放内存。
- Ollama/插件均升级到最新版。
- Windows 图形设置中将 Ollama/LM Studio 设置为高性能。

---

## 5. 常见问题与排查

### 5.1 推理慢
- 检查是否为 Q4 量化、是否只加载一个模型、是否有后台程序占用内存。

### 5.2 Agent 执行卡顿
- 建议用 Run Agent Project 或 Aider 插件，保持 VS Code 只加载一个 Agent。

### 5.3 显卡占用高
- 强制用 CPU，或调整显存分配。

### 5.4 Ollama 服务未启动
- 命令：
  ```powershell
  ollama serve
  ollama list
  ```

### 5.5 模型下载失败
- 可用国内镜像或手动下载模型文件到本地模型目录。

### 5.6 Aider 连接失败
- 验证 Ollama API：
  ```powershell
  curl http://localhost:11434/api/tags
  ```

### 5.7 内存不足
- 关闭其他应用，只运行一个模型，考虑更小量化版本。

---

## 6. 日常使用流程（推荐）
1. 启动 Ollama 服务：
   ```powershell
   ollama serve
   ```
2. 启动 agent 工具（如 Open Interpreter）：
   ```powershell
   interpreter --model ollama/qwen2.5-coder:7b-instruct-q4_K_M
   ```
3. VS Code 中打开插件，开始 agent 交互。

---

## 7. 环境变量配置汇总
```
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_GPU=0
```

---

## 8. 参考命令
```powershell
# 拉取 Qwen2.5-Coder:7B Q4 量化
ollama pull qwen2.5-coder:7b-instruct-q4_K_M

# 查看已下载模型
ollama list

# 启动 Ollama 服务
ollama serve

# 启动 Open Interpreter agent
interpreter --model ollama/qwen2.5-coder:7b-instruct-q4_K_M
```

---

**文档版本**: v1.1（完整细节版）
**更新日期**: 2026-01-12
**适用系统**: Windows 11 Pro

如有问题，欢迎反馈！

---

# 附录：run_aider.bat 启动脚本优化与说明

## 优化建议

1. **环境变量设置**
  - 推荐在 Ollama 启动前设置：
    ```bat
    set OLLAMA_MAX_LOADED_MODELS=1
    set OLLAMA_NUM_GPU=0
    ```
  - 确保只加载一个模型，并强制用 CPU（适合集成显卡）。

2. **Ollama API 地址**
  - 保持 `set OLLAMA_API_BASE=http://127.0.0.1:11434`，如有端口变动需同步修改。

3. **Aider 参数优化**
  - 推荐用 Q4 量化模型：`--model ollama/qwen2.5-coder:7b-instruct-q4_K_M`，推理更快更省内存。
  - `--edit-format whole` 推荐全量编辑（如需 diff 可切换）。
  - `--no-auto-commits` 关闭自动提交，便于手动管理。
  - `--chat-language zh` 保持中文。
  - `--map-tokens 1024` 可根据显存适当调整（如 2048）。

4. **启动顺序建议**
  - 先启动 Ollama 服务（`ollama serve`），再运行 bat 脚本。
  - bat 脚本可加入 Ollama 服务检测逻辑（如 ping 或 curl 检查端口）。

5. **目录切换**
  - `cd` 命令建议用绝对路径，避免中文路径或空格导致问题。

---

## 推荐优化后的 run_aider.bat 示例

```bat
@echo off
REM Ollama 推荐环境变量
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_NUM_GPU=0

REM API KEY 可选
set OPENAI_API_KEY=na
set OLLAMA_API_BASE=http://127.0.0.1:11434

REM 切换到你的项目目录
cd /d D:\dev\source_code\vscode_study\web-projects\company-website

REM 检查 Ollama 服务是否启动（可选）
curl http://127.0.0.1:11434/api/tags >nul 2>nul
if errorlevel 1 (
  echo Ollama 服务未启动，请先运行 ollama serve
  pause
  exit /b
)

REM 启动 Aider，推荐 Q4 量化模型
aider ^
  --model ollama/qwen2.5-coder:7b-instruct-q4_K_M ^
  --edit-format whole ^
  --no-auto-commits ^
  --chat-language zh ^
  --map-tokens 1024

pause
```

---

## 说明与扩展

- Ollama 服务需提前启动（`ollama serve`）。
- bat 脚本可自动检测服务状态，避免未启动导致连接失败。
- 推荐用 Q4 量化模型，推理速度快、内存占用低。
- 只加载一个模型，关闭其他大模型。
- 目录切换建议用绝对路径，避免路径问题。
- 可根据实际显存调整 `--map-tokens` 参数。

如需批量 agent 管理，可结合 Run Agent Project 插件或 Page Assistant Project，详见本文件前述最佳实践。
