# 运行 LocalStack Java 示例程序

Write-Host "`n========================================"
Write-Host "  运行 LocalStack Java 示例程序"
Write-Host "========================================`n"

# 检查 LocalStack
Write-Host "[1/4] 检查 LocalStack 状态..." -ForegroundColor Yellow
$running = docker ps --format "{{.Names}}" | Select-String "localstack"
if (-not $running) {
    Write-Host "  ! LocalStack 未运行，正在启动..." -ForegroundColor Yellow
    docker start localstack | Out-Null
    Start-Sleep -Seconds 5
    Write-Host "  ✓ LocalStack 已启动" -ForegroundColor Green
} else {
    Write-Host "  ✓ LocalStack 正在运行" -ForegroundColor Green
}

# 检查 Java
Write-Host "`n[2/4] 检查 Java 环境..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    Write-Host "  ✓ $javaVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Java 未安装或未配置" -ForegroundColor Red
    exit 1
}

# 检查 Maven
Write-Host "`n[3/4] 检查 Maven 环境..." -ForegroundColor Yellow
try {
    $mvnVersion = mvn -version 2>&1 | Select-Object -First 1
    Write-Host "  ✓ $mvnVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Maven 未安装或未配置" -ForegroundColor Red
    exit 1
}

# 进入项目目录
Set-Location "D:\dev\study\localstack-lab\projects\hello-localstack-java"

# 运行程序
Write-Host "`n[4/4] 运行程序..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Cyan

# 设置环境变量（使用 localhost 而不是域名）
$env:LOCALSTACK_ENDPOINT_URL = "http://localhost:4566"

# 编译并运行
mvn clean compile exec:java -Dexec.mainClass="com.example.localstack.App" -q

Write-Host "----------------------------------------" -ForegroundColor Cyan

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  程序执行完成" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "提示:" -ForegroundColor Yellow
Write-Host "  - 查看 LocalStack 日志: docker logs localstack --tail 20"
Write-Host "  - 停止 LocalStack: docker stop localstack"
Write-Host "  - 再次运行: .\run.ps1`n"

