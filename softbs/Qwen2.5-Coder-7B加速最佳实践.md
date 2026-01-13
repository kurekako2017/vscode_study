# Qwen2.5-Coder:7B 本地加速与 Agent 插件最佳实践

Qwen2.5-Coder 在本地推理时受限于显存（VRAM）、系统物理内存或集成显卡带宽（RAM），容易导致推理速度和响应性能下降。推荐如下高效组合与操作流程：

## 1. 插件模式：VS Code + Ollama + Agent

### 核心插件
- VS Code 安装 Aider 插件（代码编辑/对话式交互）。
- 推荐安装 API Provider 插件（API管理）。
- 配合 Ollama 本地部署，支持多模型切换。

### 辅助插件
- 安装 Run Agent Project（批量指令/多模型自动切换）。

### 模式说明
- Aider 插件用于对话模式（D），侧重代码编辑/交互。
- Run Agent Project 用于批量任务、自动化指令流。

## 2. 快速执行步骤

1. 启动 Ollama（Qwen2.5-Coder:7B），建议只加载一个模型，环境变量设置：
   - `OLLAMA_MAX_LOADED_MODELS=1`
   - `OLLAMA_NUM_GPU=0`
2. VS Code 插件统一管理 Agent 指令，推荐 Run Agent 插件，支持 Page/指令流自动批处理。
3. 具体命令：
   - 启动 Aider 插件
   - 启动 VS Code 插件统一管理 Agent
   - 启动 Ollama 服务：`ollama serve`
   - 拉取 Qwen2.5-Coder:7B Q4 量化模型：`ollama pull qwen2.5-coder:7b-instruct-q4_K_M`
   - 配置 `.aider.conf.yml`：
     ```yaml
     model: ollama/qwen2.5-coder:7b-instruct-q4_K_M
     ollama-api-base: http://localhost:11434
     auto-commits: false
     stream: true
     edit-format: whole
     ```
4. 性能优化建议（Q4/X_M 版本）：
   - 优先 Q4 量化，推理快、占用低。
   - 集成显卡建议 Windows 平台用 CPU，避免显卡瓶颈。
   - 只加载一个模型，关闭其他大模型。

## 3. 环境变量与常见问题

### 环境变量配置
```
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_GPU=0
```

### 常见问题
1. 推理慢：优先 Q4 量化，关闭其他模型，释放内存。
2. Agent 执行卡顿：建议用 Run Agent Project 或 Aider 插件，保持 VS Code 只加载一个 Agent。
3. 显卡占用高：强制用 CPU，或调整显存分配。

---

如需保存为 md 文件，可直接复制以上内容。