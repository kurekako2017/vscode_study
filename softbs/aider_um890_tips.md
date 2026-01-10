# UM890 Pro 专用配置与建议 ✅

适用于：UM890 Pro（Ryzen 9 8945HS / 32GB / Radeon 780M）在 Windows 11 上运行本地 Ollama + Aider。

要点一览：
- 内存：32GB 可运行单个 14B 或 16B 的 Q4 量化模型；推荐一次只运行一个大型模型。✅
- BIOS：将 iGPU 的 UMA Frame Buffer Size 调整到 8G 或更高（16G 更稳妥）。
- 模型路径：优先放到非系统盘（例如 `D:\OllamaModels`），并通过环境变量 `OLLAMA_MODELS` 指向该目录。

调优建议：
- 页面文件（pagefile）：将最小/最大设置为 1.5–2 倍内存（例如 48–64GB），以在 RAM 不足时减少失败。
- 模型优先顺序：先把 `Qwen2.5-Coder 14B (Q4)` 设为默认，平衡推理质量与资源占用；需要高质量/大上下文时再切 DeepSeek 16B（Q4/Q5）。

故障排查要点：
- 模型拉取卡住：检查网络、代理；或直接下载 GGUF 到 `D:\OllamaModels` 再用 Modelfile 创建。
- 运行时报内存不足：尝试 Q4/Q5 版本、减少并发模型、关闭占用大量内存的其他程序。
- 服务无法访问：确认 `ollama serve` 已启动，并访问 `http://localhost:11434/api/` 做健康检查。

如果你愿意，我可以：
- 把常用命令写到一个 PowerShell 脚本（用于拉模型、启动服务、测试），并在你的机器上运行一次完整的“拉取→启动→测试”。
