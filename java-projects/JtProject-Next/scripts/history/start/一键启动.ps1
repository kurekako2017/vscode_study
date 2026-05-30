# JT电商系统 - 一键启动脚本
# 此脚本会自动处理端口冲突并启动应用

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   JT电商系统 - 智能启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查项目目录
$projectDir = "D:\dev\source_code\vscode_study\java-projects\JtProject"
if (-not (Test-Path $projectDir)) {
    Write-Host "错误: 找不到项目目录" -ForegroundColor Red
    Write-Host "路径: $projectDir" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "[1/5] 切换到项目目录..." -ForegroundColor Yellow
Set-Location $projectDir
Write-Host "      当前目录: $projectDir" -ForegroundColor Green
Write-Host ""

# 2. 检查JAR文件
$jarFile = ".\target\JtSpringProject-0.0.1-SNAPSHOT.jar"
if (-not (Test-Path $jarFile)) {
    Write-Host "错误: 找不到JAR文件" -ForegroundColor Red
    Write-Host "路径: $jarFile" -ForegroundColor Red
    Write-Host "请先运行: mvn clean package" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[2/5] JAR文件检查完成" -ForegroundColor Green
Write-Host ""

# 3. 停止所有Java进程
Write-Host "[3/5] 检查并停止旧的Java进程..." -ForegroundColor Yellow
$javaProcesses = Get-Process -Name java -ErrorAction SilentlyContinue
if ($javaProcesses) {
    Write-Host "      发现 $($javaProcesses.Count) 个Java进程" -ForegroundColor Cyan
    foreach ($proc in $javaProcesses) {
        Write-Host "      停止进程 PID: $($proc.Id)" -ForegroundColor Red
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "      等待5秒让端口释放..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
} else {
    Write-Host "      没有发现运行中的Java进程" -ForegroundColor Green
}
Write-Host ""

# 4. 检查8080端口
Write-Host "[4/5] 检查8080端口..." -ForegroundColor Yellow
$port8080 = netstat -ano | findstr ":8080.*LISTENING"
if ($port8080) {
    Write-Host "      警告: 端口8080仍被占用!" -ForegroundColor Red
    Write-Host "      $port8080" -ForegroundColor Cyan

    # 提取PID并停止
    $lines = $port8080 -split "`n"
    foreach ($line in $lines) {
        if ($line -match "\s+(\d+)\s*$") {
            $pid = $Matches[1]
            Write-Host "      强制停止进程 PID: $pid" -ForegroundColor Red
            taskkill /F /PID $pid 2>$null
        }
    }
    Write-Host "      再次等待5秒..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

$port8080Check = netstat -ano | findstr ":8080.*LISTENING"
if ($port8080Check) {
    Write-Host "      错误: 无法释放8080端口!" -ForegroundColor Red
    Write-Host "      建议: 1) 重启电脑  2) 使用其他端口" -ForegroundColor Yellow
    Write-Host ""
    $useOtherPort = Read-Host "是否使用8081端口启动? (Y/N)"
    if ($useOtherPort -eq "Y" -or $useOtherPort -eq "y") {
        $port = 8081
    } else {
        Write-Host "启动已取消" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} else {
    Write-Host "      端口8080可用" -ForegroundColor Green
    $port = 8080
}
Write-Host ""

# 5. 启动应用
Write-Host "[5/5] 正在启动JT电商系统..." -ForegroundColor Yellow
Write-Host "      端口: $port" -ForegroundColor Cyan
Write-Host "      日志将显示在下方..." -ForegroundColor Cyan
Write-Host "      按 Ctrl+C 可停止应用" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Java路径
$javaPath = "C:\Program Files\jdk-21.0.2\bin\java.exe"
if (-not (Test-Path $javaPath)) {
    # 尝试其他路径
    $javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot\bin\java.exe"
    if (-not (Test-Path $javaPath)) {
        Write-Host "错误: 找不到Java可执行文件" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
}

# 启动应用
if ($port -eq 8080) {
    & $javaPath -jar $jarFile
} else {
    & $javaPath -jar $jarFile --server.port=$port
}

# 如果到这里说明应用已停止
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "应用已停止" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "按回车键退出"

