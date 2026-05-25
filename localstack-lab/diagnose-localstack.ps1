# LocalStack 诊断脚本

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  LocalStack 环境诊断" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$issues = @()
$allOk = $true

# 1. 检查 Docker Desktop
Write-Host "[1/7] 检查 Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Docker 已安装: $dockerVersion" -ForegroundColor Green

        # 检查 Docker 是否运行
        $dockerInfo = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Docker 服务正在运行" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Docker 服务未运行" -ForegroundColor Red
            $issues += "Docker Desktop 未启动 - 请打开 Docker Desktop 应用"
            $allOk = $false
        }
    } else {
        Write-Host "  ✗ Docker 未安装或未在 PATH 中" -ForegroundColor Red
        $issues += "Docker 未安装或未配置环境变量"
        $allOk = $false
    }
} catch {
    Write-Host "  ✗ 无法访问 Docker: $($_.Exception.Message)" -ForegroundColor Red
    $issues += "Docker 访问失败 - 可能未启动"
    $allOk = $false
}

# 2. 检查 LocalStack 容器
Write-Host "`n[2/7] 检查 LocalStack 容器..." -ForegroundColor Yellow
try {
    $containers = docker ps -a --format "{{.Names}},{{.Status}},{{.Ports}}" 2>&1 | Select-String "localstack"
    if ($containers) {
        Write-Host "  ✓ 找到 LocalStack 容器" -ForegroundColor Green
        $containers | ForEach-Object {
            $parts = $_.ToString().Split(',')
            $name = $parts[0]
            $status = $parts[1]
            $ports = if ($parts.Length -gt 2) { $parts[2] } else { "无" }

            Write-Host "    容器名: $name" -ForegroundColor White
            Write-Host "    状态: $status" -ForegroundColor White
            Write-Host "    端口: $ports" -ForegroundColor White

            if ($status -notmatch "Up") {
                $issues += "LocalStack 容器已停止 - 需要启动"
                $allOk = $false
            }
        }
    } else {
        Write-Host "  ✗ 未找到 LocalStack 容器" -ForegroundColor Red
        $issues += "LocalStack 容器不存在 - 需要创建"
        $allOk = $false
    }
} catch {
    Write-Host "  ✗ 无法检查容器: $($_.Exception.Message)" -ForegroundColor Red
    $issues += "无法访问 Docker 容器列表"
    $allOk = $false
}

# 3. 检查端口占用
Write-Host "`n[3/7] 检查端口 4566..." -ForegroundColor Yellow
try {
    $portCheck = Test-NetConnection -ComputerName localhost -Port 4566 -WarningAction SilentlyContinue 2>&1
    if ($portCheck.TcpTestSucceeded) {
        Write-Host "  ✓ 端口 4566 可访问" -ForegroundColor Green
    } else {
        Write-Host "  ✗ 端口 4566 不可访问" -ForegroundColor Red
        $issues += "端口 4566 不可访问 - LocalStack 可能未启动"
        $allOk = $false
    }
} catch {
    Write-Host "  ! 无法测试端口连接" -ForegroundColor Yellow
}

# 4. 检查 Java
Write-Host "`n[4/7] 检查 Java 环境..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Java 已安装: $javaVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Java 未安装或未配置" -ForegroundColor Red
        $issues += "Java 环境问题"
        $allOk = $false
    }
} catch {
    Write-Host "  ✗ Java 未找到" -ForegroundColor Red
    $issues += "Java 未安装"
    $allOk = $false
}

# 5. 检查 Maven
Write-Host "`n[5/7] 检查 Maven 环境..." -ForegroundColor Yellow
try {
    $mvnVersion = mvn -version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Maven 已安装: $mvnVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Maven 未安装或未配置" -ForegroundColor Red
        $issues += "Maven 环境问题"
        $allOk = $false
    }
} catch {
    Write-Host "  ✗ Maven 未找到" -ForegroundColor Red
    $issues += "Maven 未安装"
    $allOk = $false
}

# 6. 检查项目文件
Write-Host "`n[6/7] 检查项目文件..." -ForegroundColor Yellow
$projectPath = "D:\dev\study\localstack-lab\projects\hello-localstack-java"
if (Test-Path $projectPath) {
    Write-Host "  ✓ 项目目录存在" -ForegroundColor Green

    $pomPath = Join-Path $projectPath "pom.xml"
    if (Test-Path $pomPath) {
        Write-Host "  ✓ pom.xml 存在" -ForegroundColor Green
    } else {
        Write-Host "  ✗ pom.xml 不存在" -ForegroundColor Red
        $issues += "项目配置文件缺失"
        $allOk = $false
    }

    $scriptPath = Join-Path $projectPath "test-localstack.ps1"
    if (Test-Path $scriptPath) {
        Write-Host "  ✓ 测试脚本存在" -ForegroundColor Green
    } else {
        Write-Host "  ! 测试脚本不存在（可选）" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ 项目目录不存在" -ForegroundColor Red
    $issues += "项目目录未找到"
    $allOk = $false
}

# 7. 测试 LocalStack 连接
Write-Host "`n[7/7] 测试 LocalStack API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4566/_localstack/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  ✓ LocalStack API 可访问 (HTTP $($response.StatusCode))" -ForegroundColor Green

    $health = $response.Content | ConvertFrom-Json
    Write-Host "    可用服务:" -ForegroundColor Cyan
    $health.services.PSObject.Properties | Select-Object -First 5 | ForEach-Object {
        $status = if ($_.Value -eq "available" -or $_.Value -eq "running") { "✓" } else { "✗" }
        $color = if ($_.Value -eq "available" -or $_.Value -eq "running") { "Green" } else { "Yellow" }
        Write-Host "      $status $($_.Name): $($_.Value)" -ForegroundColor $color
    }
} catch {
    Write-Host "  ✗ 无法连接到 LocalStack API" -ForegroundColor Red
    $issues += "LocalStack API 不可访问 - 容器可能未运行"
    $allOk = $false
}

# 总结
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  诊断总结" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($allOk) {
    Write-Host "✓ 所有检查通过！环境正常" -ForegroundColor Green
    Write-Host "`n可以运行测试:" -ForegroundColor Yellow
    Write-Host "  cd $projectPath" -ForegroundColor White
    Write-Host "  .\test-localstack.ps1" -ForegroundColor White
} else {
    Write-Host "✗ 发现 $($issues.Count) 个问题:" -ForegroundColor Red
    Write-Host ""
    $issues | ForEach-Object {
        Write-Host "  • $_" -ForegroundColor Yellow
    }

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  解决方案" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # 提供具体解决方案
    if ($issues -match "Docker.*未启动") {
        Write-Host "【解决方案 1】启动 Docker Desktop" -ForegroundColor Yellow
        Write-Host "  1. 在开始菜单搜索 'Docker Desktop'" -ForegroundColor White
        Write-Host "  2. 点击启动 Docker Desktop" -ForegroundColor White
        Write-Host "  3. 等待 Docker 引擎启动完成（托盘图标显示正常）" -ForegroundColor White
        Write-Host "  4. 重新运行此诊断脚本" -ForegroundColor White
        Write-Host ""
    }

    if ($issues -match "LocalStack.*停止") {
        Write-Host "【解决方案 2】启动 LocalStack 容器" -ForegroundColor Yellow
        Write-Host "  运行命令:" -ForegroundColor White
        Write-Host "    docker start localstack" -ForegroundColor Cyan
        Write-Host ""
    }

    if ($issues -match "容器不存在") {
        Write-Host "【解决方案 3】创建 LocalStack 容器" -ForegroundColor Yellow
        Write-Host "  运行命令:" -ForegroundColor White
        Write-Host "    docker run -d --name localstack -p 4566:4566 -e LOCALSTACK_AUTH_TOKEN=`$env:LOCALSTACK_AUTH_TOKEN localstack/localstack" -ForegroundColor Cyan
        Write-Host ""
    }

    if ($issues -match "端口.*不可访问") {
        Write-Host "【解决方案 4】检查端口占用" -ForegroundColor Yellow
        Write-Host "  运行命令查看端口占用:" -ForegroundColor White
        Write-Host "    netstat -ano | findstr 4566" -ForegroundColor Cyan
        Write-Host "  如果被占用，终止占用进程或更改 LocalStack 端口" -ForegroundColor White
        Write-Host ""
    }
}

Write-Host "`n快速操作命令:" -ForegroundColor Cyan
Write-Host "  • 启动 Docker Desktop: 从开始菜单启动" -ForegroundColor White
Write-Host "  • 启动 LocalStack: docker start localstack" -ForegroundColor White
Write-Host "  • 查看容器日志: docker logs localstack --tail 20" -ForegroundColor White
Write-Host "  • 重启 LocalStack: docker restart localstack" -ForegroundColor White
Write-Host "  • 运行测试: cd $projectPath; .\test-localstack.ps1" -ForegroundColor White
Write-Host ""

# 自动修复选项
if (-not $allOk) {
    Write-Host "是否尝试自动修复? (Y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host

    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host "`n正在尝试自动修复..." -ForegroundColor Cyan

        # 尝试启动 LocalStack
        try {
            Write-Host "  尝试启动 LocalStack 容器..." -ForegroundColor Yellow
            docker start localstack 2>&1 | Out-Null
            Start-Sleep -Seconds 5

            $status = docker ps --format "{{.Names}}: {{.Status}}" | Select-String "localstack"
            if ($status) {
                Write-Host "  ✓ LocalStack 已启动" -ForegroundColor Green
            } else {
                Write-Host "  ✗ LocalStack 启动失败" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ✗ 自动修复失败: $($_.Exception.Message)" -ForegroundColor Red
        }

        Write-Host "`n请重新运行此脚本验证修复结果" -ForegroundColor Yellow
    }
}

Write-Host ""

