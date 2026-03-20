# Softbs

`softbs/` 已整理为按主题分类的学习资料库，而不是把所有 Markdown 散放在根目录。

## 目录导航

- `tools/`: 脚本与调用示例
- `aider/`: Aider、本地模型、AI 编程辅助相关资料
- `openclaw/`: OpenClaw 安装、使用、微信命令、历史说明
- `github/`: GitHub、Codespaces、Pages、学生版 DevOps 相关资料
- `vscode/`: VS Code 操作指南
- `notes/`: 临时笔记与零散记录
- `history/`: 历史环境说明

## 推荐阅读

- [UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](D:/dev/source_code/vscode_study/softbs/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md)
- [OpenClaw_实用使用教程.md](D:/dev/source_code/vscode_study/softbs/openclaw/OpenClaw_实用使用教程.md)
- [GitHub学生版学习与DevOps实践教程.md](D:/dev/source_code/vscode_study/softbs/github/GitHub学生版学习与DevOps实践教程.md)
- [VSCode操作指南.md](D:/dev/source_code/vscode_study/softbs/vscode/VSCode操作指南.md)

## 原有脚本说明

- `tools/ai-run.ps1`：PowerShell 示例脚本，支持 `-Provider`、`-Prompt`、`-DryRun`
- `tools/openai.http`：REST Client 示例请求文件
- `.vscode/tasks.json`：VS Code 任务配置

## 说明

- 根目录尽量只保留总入口和少量核心教程
- 其余文档按主题归类到子目录
- 历史或重复说明优先放到 `history/` 或对应主题目录下的归档位置

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
