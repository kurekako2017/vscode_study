# Simple startup script for JT E-commerce System
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JT电商系统 - 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location D:\dev\source_code\vscode_study\java-projects\JtProject

# Start with Maven, skipping tests
Write-Host "正在启动应用..." -ForegroundColor Green
Write-Host "访问地址: http://localhost:8080" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止应用" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 使用生产模式启动，禁用devtools自动重启
& "C:\Program Files\jdk-21.0.2\bin\java.exe" "-Dspring.devtools.restart.enabled=false" -jar .\target\JtSpringProject-0.0.1-SNAPSHOT.jar

