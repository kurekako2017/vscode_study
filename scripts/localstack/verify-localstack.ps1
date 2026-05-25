# 脚本: verify-localstack.ps1
# 说明: 验证 LocalStack 容器健康状态、API 接口与最近日志。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\localstack\verify-localstack.ps1

Write-Host "===== LocalStack 运行状态验证 =====" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 Docker 状态
Write-Host "1. 检查 Docker 状态..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "   ✓ Docker 已安装: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Docker 未安装或未运行" -ForegroundColor Red
    exit 1
}

# 2. 检查 LocalStack 容器
Write-Host ""
Write-Host "2. 检查 LocalStack 容器..." -ForegroundColor Yellow
$containers = docker ps --format "{{.Names}}`t{{.Status}}`t{{.Ports}}" | Select-String "localstack"
if ($containers) {
    Write-Host "   ✓ LocalStack 容器正在运行:" -ForegroundColor Green
    $containers | ForEach-Object { Write-Host "     $_" -ForegroundColor White }
} else {
    Write-Host "   ✗ LocalStack 容器未运行" -ForegroundColor Red
    Write-Host "   尝试启动 LocalStack..." -ForegroundColor Yellow
    docker start localstack
    Start-Sleep -Seconds 5
}

# 3. 检查容器健康状态
Write-Host ""
Write-Host "3. 检查容器健康状态..." -ForegroundColor Yellow
$health = docker inspect --format='{{.State.Health.Status}}' localstack 2>$null
if ($health -eq "healthy") {
    Write-Host "   ✓ LocalStack 健康状态: $health" -ForegroundColor Green
} else {
    Write-Host "   ! LocalStack 健康状态: $health" -ForegroundColor Yellow
}

# 4. 测试 LocalStack API
Write-Host ""
Write-Host "4. 测试 LocalStack API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4566/_localstack/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "   ✓ LocalStack API 可访问 (HTTP $($response.StatusCode))" -ForegroundColor Green

    # 解析并显示服务状态
    $health = $response.Content | ConvertFrom-Json
    Write-Host ""
    Write-Host "   可用服务:" -ForegroundColor Cyan
    $health.services.PSObject.Properties | ForEach-Object {
        $status = if ($_.Value -eq "available" -or $_.Value -eq "running") { "✓" } else { "✗" }
        $color = if ($_.Value -eq "available" -or $_.Value -eq "running") { "Green" } else { "Yellow" }
        Write-Host "     $status $($_.Name): $($_.Value)" -ForegroundColor $color
    }
} catch {
    Write-Host "   ✗ 无法连接到 LocalStack API: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. 显示 LocalStack 日志（最后 10 行）
Write-Host ""
Write-Host "5. LocalStack 最新日志:" -ForegroundColor Yellow
docker logs localstack --tail 10 2>&1 | ForEach-Object {
    if ($_ -match "Ready\.") {
        Write-Host "   $_" -ForegroundColor Green
    } elseif ($_ -match "ERROR|Error|error") {
        Write-Host "   $_" -ForegroundColor Red
    } else {
        Write-Host "   $_" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "===== 验证完成 =====" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示:" -ForegroundColor Yellow
Write-Host "  - LocalStack Web UI: https://app.localstack.cloud" -ForegroundColor White
Write-Host "  - API Endpoint: http://localhost:4566" -ForegroundColor White
Write-Host "  - 查看实时日志: docker logs -f localstack" -ForegroundColor White
Write-Host ""

