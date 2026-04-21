# 脚本: install-docker-quick.ps1
# 说明: 快速下载并启动 Docker Desktop 安装程序。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\docker\install-docker-quick.ps1
$ErrorActionPreference = 'Continue'

Write-Host "`n=== Docker Desktop 安装程序 ===" -ForegroundColor Cyan

$url = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$output = "$env:USERPROFILE\Downloads\DockerDesktopInstaller.exe"

# 检查是否已安装
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "`n✓ Docker 已安装！" -ForegroundColor Green
    docker --version
    exit 0
}

# 检查文件是否已存在
if (Test-Path $output) {
    $size = (Get-Item $output).Length / 1MB
    if ($size -gt 100) {
        Write-Host "`n✓ 安装文件已存在 ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
        Write-Host "`n正在启动安装..." -ForegroundColor Yellow
        Start-Process -FilePath $output -ArgumentList "install", "--quiet", "--accept-license" -Verb RunAs
        Write-Host "`n安装程序已启动！请按照屏幕提示完成安装。" -ForegroundColor Green
        exit 0
    }
}

# 下载安装文件
Write-Host "`n[1/2] 下载 Docker Desktop (约 600 MB)..." -ForegroundColor Yellow
Write-Host "保存位置: $output" -ForegroundColor Gray

try {
    Import-Module BitsTransfer
    Start-BitsTransfer -Source $url -Destination $output -Description "下载 Docker Desktop" -DisplayName "Docker Desktop"
    Write-Host "✓ 下载完成！" -ForegroundColor Green
} catch {
    Write-Host "BITS 传输失败，尝试使用 WebClient..." -ForegroundColor Yellow
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile($url, $output)
    Write-Host "✓ 下载完成！" -ForegroundColor Green
}

# 启动安装
Write-Host "`n[2/2] 启动安装程序..." -ForegroundColor Yellow
Start-Process -FilePath $output -ArgumentList "install", "--quiet", "--accept-license" -Verb RunAs

Write-Host @"

╔══════════════════════════════════════════════════════╗
║           安装程序已启动                              ║
╚══════════════════════════════════════════════════════╝

后续步骤：
  1. 等待安装完成（可能需要 5-10 分钟）
  2. 重启计算机（如果提示）
  3. 启动 Docker Desktop 应用
  4. 验证安装: docker --version

"@ -ForegroundColor Green

