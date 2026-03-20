# JT电商系统启动脚本
# 用途：快速启动Spring Boot应用

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JT电商系统 - 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 设置Java环境
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"
$javaExe = "$env:JAVA_HOME\bin\java.exe"

# 检查Java是否存在
if (-not (Test-Path $javaExe)) {
    Write-Host "错误: 找不到Java可执行文件" -ForegroundColor Red
    Write-Host "路径: $javaExe" -ForegroundColor Red
    exit 1
}

# 检查JAR文件是否存在
$jarFile = ".\target\JtSpringProject-0.0.1-SNAPSHOT.jar"
if (-not (Test-Path $jarFile)) {
    Write-Host "警告: 找不到JAR文件，正在编译..." -ForegroundColor Yellow
    Write-Host ""
    & mvn clean package "-Dmaven.test.skip=true"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "错误: Maven编译失败" -ForegroundColor Red
        exit 1
    }
}

# 检查端口是否被占用
$port8080 = netstat -ano | findstr ":8080"
if ($port8080) {
    Write-Host "警告: 端口8080已被占用" -ForegroundColor Yellow
    Write-Host $port8080
    $response = Read-Host "是否要停止现有进程并重新启动？(Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        $pid = ($port8080 -split "\s+")[-1]
        Write-Host "正在停止进程 $pid..." -ForegroundColor Yellow
        Stop-Process -Id $pid -Force
        Start-Sleep -Seconds 2
    } else {
        Write-Host "取消启动" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "正在启动应用..." -ForegroundColor Green
Write-Host "Java版本: " -NoNewline
& $javaExe -version 2>&1 | Select-Object -First 1
Write-Host ""

# 启动应用
Write-Host "访问地址: http://localhost:8080" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止应用" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& $javaExe -jar $jarFile

