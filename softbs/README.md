# AI Agents Windows 示例（软体学习仓库）

本仓库包含在 Windows + VS Code 环境下，如何用命令行 / 脚本 调用常见 AI 服务（OpenAI / Claude / Gemini）的示例。

目录（新增文件）
- `tools/ai-run.ps1`：PowerShell 示例脚本，支持 `-Provider`、`-Prompt`、`-DryRun`。默认 DryRun 模式仅打印请求体，避免意外使用密钥。
- `tools/openai.http`：REST Client（VS Code 扩展）示例请求文件，使用 `{{OPENAI_API_KEY}}` 等变量。
- `.vscode/tasks.json`：可选的任务配置，用于在 VS Code 中一键运行脚本。

快速开始（在 VS Code 终端运行）：

1. 在 PowerShell 会话中设置环境变量（仅示例，不要把秘钥提交到仓库）：

```powershell
setx OPENAI_API_KEY "你的_openai_key"
setx CLAUDE_API_KEY "你的_claude_key"
setx GEMINI_API_KEY "你的_gemini_key"
```

2. 打开新的终端（使 `setx` 生效），然后运行脚本的 dry-run 验证：

```powershell
# 在仓库根目录下运行
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\ai-run.ps1 -Provider openai -Prompt "测试 DryRun" -DryRun
```

3. 若一切正常，移除 `-DryRun` 即可发起真实请求（注意：会使用你在系统中配置的 API Key）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\ai-run.ps1 -Provider openai -Prompt "请用中文写一个冒泡排序例子"
```

备注：示例脚本在没有检测到对应环境变量时会提示并退出。请按照厂商文档确认请求字段与模型名是否需要更新。
