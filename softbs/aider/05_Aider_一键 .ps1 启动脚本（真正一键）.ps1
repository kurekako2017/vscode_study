# ================================
# Aider One-Click Startup Script
# ================================

param (
    [string]$ProjectPath = ".",
    [string]$Model = "ollama/qwen2.5-coder:14b"
)

Write-Host "Starting Aider with Ollama model..." -ForegroundColor Cyan
Write-Host "Project Path: $ProjectPath"
Write-Host "Model: $Model"

Set-Location $ProjectPath

aider `
  --model $Model `
  --edit-format diff `
  --auto-commits false `
  --stream

Pause