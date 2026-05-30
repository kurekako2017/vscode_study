# chat_cli 演示运行脚本（PowerShell）
# 用法: .\run_demo.ps1

# 检查 OPENAI_API_KEY
if (-not $env:OPENAI_API_KEY) {
    Write-Host "ERROR: OPENAI_API_KEY is not set." -ForegroundColor Red
    Write-Host "Please set: `$env:OPENAI_API_KEY = 'your-api-key'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Setting up chat_cli demo..." -ForegroundColor Green

# 创建虚拟环境（如果不存在）
$venv_path = "\.venv"
if (-not (Test-Path $venv_path)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv $venv_path
}

# 激活虚拟环境
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& $venv_path\Scripts\Activate.ps1

# 安装依赖
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt

# 运行演示
Write-Host "`nRunning demo: Interactive chat with OpenAI Responses API" -ForegroundColor Green
Write-Host "Type 'quit' to exit.`n" -ForegroundColor Yellow

python main.py

# 清理
Write-Host "`nDemo completed." -ForegroundColor Green
