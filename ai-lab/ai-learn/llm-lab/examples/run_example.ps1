# llm-lab/examples 运行脚本（PowerShell）
# 用法: .\run_example.ps1 [example_name]
# 示例: .\run_example.ps1 basics
# 示例: .\run_example.ps1 pydantic_example

param(
    [string]$exampleName = "basics"
)

$exampleFile = "$exampleName.py"

if (-not (Test-Path $exampleFile)) {
    Write-Host "ERROR: Example file '$exampleFile' not found." -ForegroundColor Red
    Write-Host "Available examples:" -ForegroundColor Yellow
    Get-ChildItem *.py | ForEach-Object { Write-Host "  - $($_.BaseName)" }
    exit 1
}

# 提示 OPENAI_API_KEY（model_call_example 无 Key 时会自动 mock）
if ($exampleName -eq "model_call_example" -or $exampleName -match "model") {
    if (-not $env:OPENAI_API_KEY) {
        Write-Host "INFO: OPENAI_API_KEY is not set; model_call_example will use mock mode." -ForegroundColor Yellow
        Write-Host "For real API calls, set it first:" -ForegroundColor Yellow
        Write-Host "`$env:OPENAI_API_KEY = 'your-api-key'" -ForegroundColor Yellow
    }
}

Write-Host "Setting up llm-lab/examples..." -ForegroundColor Green

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

# 运行示例
Write-Host "`nRunning example: $exampleName`n" -ForegroundColor Green

python $exampleFile

Write-Host "`nExample completed." -ForegroundColor Green
