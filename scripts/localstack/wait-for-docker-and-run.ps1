# 脚本: wait-for-docker-and-run.ps1
# 说明: 等待 Docker 引擎就绪后，执行 LocalStack Java 示例流程。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\localstack\wait-for-docker-and-run.ps1

$ErrorActionPreference = 'Continue'

Write-Host @"

╔══════════════════════════════════════════════════════╗
║        等待 Docker 启动并运行 LocalStack 示例          ║
╚══════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# 步骤 1: 等待 Docker 引擎就绪
Write-Host "[1/3] 等待 Docker 引擎启动..." -ForegroundColor Yellow
Write-Host "      这可能需要 1-3 分钟，请耐心等待..." -ForegroundColor Gray
Write-Host ""

$maxWait = 180  # 最多等待 3 分钟
$waited = 0
$ready = $false

while ($waited -lt $maxWait) {
    try {
        $output = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Docker 引擎已就绪！" -ForegroundColor Green
            $ready = $true
            break
        }
    } catch {}

    Write-Host "." -NoNewline -ForegroundColor Gray
    Start-Sleep -Seconds 5
    $waited += 5
}

Write-Host ""

if (-not $ready) {
    Write-Host "`n  ✗ Docker 引擎启动超时" -ForegroundColor Red
    Write-Host "`n可能的原因：" -ForegroundColor Yellow
    Write-Host "  1. Docker Desktop 仍在初始化（首次启动需要更长时间）" -ForegroundColor White
    Write-Host "  2. WSL 2 需要配置" -ForegroundColor White
    Write-Host "  3. 系统资源不足" -ForegroundColor White
    Write-Host "`n建议操作：" -ForegroundColor Yellow
    Write-Host "  1. 查看 Docker Desktop 窗口中的状态" -ForegroundColor White
    Write-Host "  2. 等待几分钟后重试" -ForegroundColor White
    Write-Host "  3. 重启 Docker Desktop" -ForegroundColor White
    exit 1
}

# 显示 Docker 信息
Write-Host "`n  Docker 版本信息：" -ForegroundColor Gray
docker version --format "  Client: {{.Client.Version}}, Server: {{.Server.Version}}"
Write-Host ""

# 步骤 2: 测试 Docker
Write-Host "[2/3] 测试 Docker 运行..." -ForegroundColor Yellow

try {
    Write-Host "  运行测试容器..." -ForegroundColor Gray
    docker run --rm hello-world | Select-Object -First 10
    Write-Host "  ✓ Docker 运行正常！" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Docker 测试失败: $_" -ForegroundColor Yellow
}

# 步骤 3: 运行 LocalStack 示例
Write-Host "`n[3/3] 运行 LocalStack Java 示例..." -ForegroundColor Yellow

$projectPath = "D:\dev\study\localstack-lab\projects\hello-localstack-java"

if (-not (Test-Path $projectPath)) {
    Write-Host "  ✗ 项目路径不存在: $projectPath" -ForegroundColor Red
    exit 1
}

Write-Host "  切换到项目目录..." -ForegroundColor Gray
Set-Location $projectPath

Write-Host "  运行项目脚本..." -ForegroundColor Gray
Write-Host ""

# 运行项目
if (Test-Path ".\run.ps1") {
    .\run.ps1
} else {
    Write-Host "  run.ps1 不存在，手动启动 LocalStack 和 Java 项目..." -ForegroundColor Yellow

    # 检查 LocalStack CLI
    if (Get-Command localstack -ErrorAction SilentlyContinue) {
        Write-Host "  启动 LocalStack..." -ForegroundColor Gray
        localstack start -d

        Write-Host "  等待 LocalStack 就绪..." -ForegroundColor Gray
        Start-Sleep -Seconds 20

        Write-Host "  运行 Java 项目..." -ForegroundColor Gray
        mvn clean compile exec:java
    } else {
        Write-Host "  LocalStack CLI 未安装" -ForegroundColor Yellow
        Write-Host "  直接运行 Java 项目（需要 LocalStack 容器）..." -ForegroundColor Gray

        # 启动 LocalStack 容器
        docker run -d --rm -p 4566:4566 -p 4571:4571 --name localstack localstack/localstack

        Write-Host "  等待 LocalStack 容器就绪..." -ForegroundColor Gray
        Start-Sleep -Seconds 20

        Write-Host "  运行 Java 项目..." -ForegroundColor Gray
        mvn clean compile exec:java
    }
}

Write-Host "`n✓ 完成！" -ForegroundColor Green

