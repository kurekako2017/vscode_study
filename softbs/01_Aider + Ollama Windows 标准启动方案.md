# Aider + Ollama Windows 启动指南（标准版）

## 环境前提
- Windows 11 Pro
- 已安装 Ollama
- 已安装 Aider
- 已拉取模型：
  - qwen2.5-coder:14b
  - deepseek-coder-v2-lite:16b

## 基础启动（推荐）

### Qwen2.5-Coder 14B
```powershell
cd D:\your_project
aider --model ollama/qwen2.5-coder:14b
```

### DeepSeek-Coder V2 Lite 16B
```powershell
cd D:\your_project
aider --model ollama/deepseek-coder-v2-lite:16b
```

## 常用检查命令
```powershell
ollama list
ollama ps
```

---