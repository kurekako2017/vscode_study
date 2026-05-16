# doc_qa_agent 演示运行脚本（PowerShell）
# 用法: .\run_demo.ps1 [-docDir "path/to/docs"]

param(
    [string]$docDir = "./docs"
)

# 检查 OPENAI_API_KEY
if (-not $env:OPENAI_API_KEY) {
    Write-Host "ERROR: OPENAI_API_KEY is not set." -ForegroundColor Red
    Write-Host "Please set: `$env:OPENAI_API_KEY = 'your-api-key'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Setting up doc_qa_agent demo..." -ForegroundColor Green

# 检查文档目录
if (-not (Test-Path $docDir)) {
    Write-Host "WARNING: Document directory '$docDir' not found." -ForegroundColor Yellow
    Write-Host "Creating sample documents..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $docDir -Force | Out-Null
    @"
# Sample Document

This is a sample document for the Q&A agent demo.
It demonstrates how the agent searches documents and answers questions.
"@ | Out-File "$docDir/sample.md"
}

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
Write-Host "`nRunning demo: Document Q&A Agent" -ForegroundColor Green
Write-Host "Document directory: $docDir" -ForegroundColor Yellow
Write-Host "Type 'quit' to exit.`n" -ForegroundColor Yellow

python main.py --docdir $docDir

# 清理
Write-Host "`nDemo completed." -ForegroundColor Green
