# 检查应用状态脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JT电商系统 - 状态检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查端口8080
Write-Host "检查端口8080..." -ForegroundColor Yellow
$port = netstat -ano | findstr ":8080" | findstr "LISTENING"
if ($port) {
    Write-Host "✓ 端口8080正在监听" -ForegroundColor Green
    Write-Host $port
    $pid = ($port -split "\s+")[-1]
    Write-Host "进程ID: $pid" -ForegroundColor Green
} else {
    Write-Host "✗ 端口8080未在监听" -ForegroundColor Red
}

Write-Host ""

# 检查Java进程
Write-Host "检查Java进程..." -ForegroundColor Yellow
$javaProcesses = Get-Process | Where-Object { $_.ProcessName -eq "java" }
if ($javaProcesses) {
    Write-Host "✓ 找到Java进程:" -ForegroundColor Green
    $javaProcesses | Format-Table Id, ProcessName, @{Name="Memory(MB)";Expression={[math]::Round($_.WorkingSet/1MB,2)}} -AutoSize
} else {
    Write-Host "✗ 未找到Java进程" -ForegroundColor Red
}

Write-Host ""

# 测试HTTP访问
Write-Host "测试HTTP访问..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -Method GET -TimeoutSec 5 -UseBasicParsing
    Write-Host "✓ 应用响应正常!" -ForegroundColor Green
    Write-Host "状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "内容长度: $($response.Content.Length) 字节" -ForegroundColor Green
} catch {
    Write-Host "✗ HTTP访问失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "访问地址: http://localhost:8080" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

