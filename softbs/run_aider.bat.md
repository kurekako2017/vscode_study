@echo off
:: 1. 屏蔽 OpenAI 报错
set OPENAI_API_KEY=na
set OLLAMA_API_BASE=http://127.0.0.1:11434

:: 2. 切换到你的项目目录 (根据你提供的最新路径)
cd /d D:\dev\source_code\vscode_study\web-projects\company-website

:: 3. 启动 Aider
:: 使用 python -m 启动是最稳妥的，--chat-language zh 确保它说中文
python -m aider ^
  --model ollama/qwen2.5-coder:7b ^
  --edit-format diff ^
  --no-auto-commits ^
  --chat-language zh

pause