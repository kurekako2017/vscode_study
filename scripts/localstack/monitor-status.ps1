# 脚本: monitor-status.ps1
# 说明: 每 5 秒持续监控 Docker 与 LocalStack 运行状态。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\localstack\monitor-status.ps1

while ($true) {
    Clear-Host
    Write-Host "=== 状态监控 $(Get-Date -Format 'HH:mm:ss') ===" -ForegroundColor Cyan
    Write-Host ""

    # Docker Desktop 进程
    Write-Host "[Docker Desktop 进程]" -ForegroundColor Yellow
    $dockerProc = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
    if ($dockerProc) {
        Write-Host "  ✓ 运行中 (PID: $($dockerProc.Id))" -ForegroundColor Green
    } else {
        Write-Host "  ✗ 未运行" -ForegroundColor Red
    }

    # Docker 引擎
    Write-Host "`n[Docker 引擎]" -ForegroundColor Yellow
    try {
        $null = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ 已就绪" -ForegroundColor Green
            docker version --format "  版本: {{.Server.Version}}"
        } else {
            Write-Host "  ⏳ 启动中..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ✗ 无法连接" -ForegroundColor Red
    }

    # LocalStack 容器
    Write-Host "`n[LocalStack 容器]" -ForegroundColor Yellow
    $containers = docker ps --filter "name=localstack" --format "{{.Names}}\t{{.Status}}" 2>$null
    if ($containers) {
        Write-Host "  ✓ $containers" -ForegroundColor Green
    } else {
        Write-Host "  ✗ 未运行" -ForegroundColor Red
    }

    Write-Host "`n按 Ctrl+C 退出监控" -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

