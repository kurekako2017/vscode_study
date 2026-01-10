# 本地 Aider（与本地模型）使用指南 ✅

说明：本指南以**本地模型（例如 Ollama）+ 本地 Aider/编辑器集成**为目标，覆盖模型下载、启动、调试与常见命令。若你使用的是商业 SaaS 产品（如 Aider.ai），请告诉我，我会给出相应说明。💡

---

## 一、前提条件 🔧
- Windows/Linux/macOS：已安装 Ollama（若用其他后端请替换相应命令）。
- 已准备好磁盘空间（大模型通常需要数 GB 到数十 GB）。
- 建议：将模型放在 D 盘或非系统盘（Windows）以避免磁盘空间问题，或设置环境变量 `OLLAMA_MODELS` 指向模型目录。

常用安装命令（Windows 下载页面或 Linux 一行安装）：

```powershell
# Windows：下载并运行 OllamaSetup.exe（官网）
# Linux：
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 二、模型管理（Ollama CLI）📥
- 拉取/更新模型：

```bash
ollama pull <model>           # e.g. ollama pull qwen2.5-coder:14b
```

- 查看本地模型：

```bash
ollama list
```

- 查看模型详情：

```bash
ollama show <model>
```

- 移除模型：

```bash
ollama rm <model>
```

- 从本地 GGUF 导入（示例）：

1. 新建 `Modelfile`：
```
FROM ./vicuna-33b.Q4_0.gguf
```
2. 创建并运行：
```
ollama create mymodel -f Modelfile
ollama run mymodel
```

备注：拉取完成后，`ollama run <model>` 可以直接交互式对话。

---

## 三、运行与服务模式 ⚙️
- 即时对话（命令行）：

```bash
ollama run gemma3
# 或直接传入 prompt
ollama run gemma3 "请给出一个 3 行的工作总结示例"
```

- 以服务模式启动（适合集成）：

```bash
ollama serve    # 在后台启动 REST API，默认端口 11434
```

- 停止/查看运行中的模型：

```bash
ollama ps       # 列出正在运行的进程/模型
ollama stop <model>
```

---

## 四、用 REST API 调用模型（对接 Aider 或其它工具）🔗
- 生成（POST /api/generate）：

```bash
curl http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model":"llama3.2","prompt":"为什么天空是蓝色？"}'
```

- 聊天（POST /api/chat）：

```bash
curl http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{"model":"llama3.2","messages":[{"role":"user","content":"帮我写一个 PR 描述"}]}'
```

说明：如果你使用的是 Aider 的编辑器插件，通常能配置“Local LLM / Ollama REST endpoint”为 `http://localhost:11434`，使 Aider 的请求走本地模型。

---

## 五、在 VS Code 中使用（快速集成示例）🧩
- 方法 A：使用支持 Ollama 的 VS Code 扩展（例如 AI Toolkit for VS Code 或 Ollama 相关扩展），在扩展设置中将 endpoint 设为 `http://localhost:11434`。
- 方法 B：若你使用的是开源 Aider（CLI/插件），在插件配置中设置本地 endpoint 或把 `ollama run` 作为后端命令（具体取决于插件实现）。

推荐：在 VS Code 设置中打开开发者工具（Help → Toggle Developer Tools）观察插件请求和错误，便于排错。

---

## 六、常用交互示例（PowerShell / Bash）🧪
- 快速测试模型回显：

```bash
# 直接运行并交互
ollama run qwen2.5-coder:14b
```

- 管道方式（嵌入、脚本化）：

```bash
echo "生成 3 条代码注释示例" | ollama run gemma3
```

- 生成 embeddings（示例）：

```bash
echo "待嵌入文本" | ollama run embeddingmodel
```

---

## 七、故障排查 & 性能建议 ⚠️
- 图片/资源不显示：确认 Markdown 中图片路径是否使用相对路径 `./image.png` 且文件存在（你之前遇到过）。
- 模型拉取很慢或失败：检查网络、代理和磁盘空间。
- 运行时报显存/内存不足：换小一版模型（例如 1B/4B/7B），或调整系统 GPU/显存分配（BIOS UMA Frame Buffer Size），或使用 CPU 模式。
- `ollama serve` 无响应：确认服务是否在 11434 端口监听（`netstat -ano` 或 `ss`），并查看 `ollama ps`。
- REST API 返回错误：查看 `ollama` 的日志和系统日志，或者在浏览器访问 `http://localhost:11434` 看是否有服务响应。

---

## 八、安全与隐私小贴士 🔒
- 本地模型减少云发送风险，但依然要注意文件中不向模型泄露敏感凭证（API keys、私有数据等）。
- 若对外暴露 REST API，请务必通过反向代理或防火墙控制访问范围并使用 TLS/认证。

---

## 九、速查表（常用命令）📋
- 拉取模型：`ollama pull <model>`
- 列表模型：`ollama list`
- 运行模型：`ollama run <model>`
- 启动服务：`ollama serve`
- 停止模型：`ollama stop <model>`
- 列出运行模型：`ollama ps`
- REST 生成：`POST /api/generate`

---

## 十、后续建议 & 我可以帮你做的事 ✅
- 我可以把这份教程合并到你的仓库（例如 `aider_local_usage.md`），并根据你的实际环境（是否有 GPU、是否使用 VS Code Aider 插件）补全配置示例。是否需要我把本文件加入到当前工作区？

---

如果你需要，我可以：
- 把教程保存为仓库文件（我可以现在执行）。
- 为你的机器写一份一步步安装脚本（PowerShell/Batch）。
- 增加针对 Aider 插件或具体编辑器的配置示例。

告诉我你的优先项。