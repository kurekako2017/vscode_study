# 脚本: diagnostic.ps1
# 说明: 快速诊断 Docker、WSL、容器与关键本地端口。
# 用法: powershell -ExecutionPolicy Bypass -File .\scripts\localstack\diagnostic.ps1

Write-Host "`n=== System Diagnostic ===" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -ForegroundColor Gray

# 1. Docker Desktop Process
Write-Host "[1] Docker Desktop Process" -ForegroundColor Yellow
$dockerProc = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
if ($dockerProc) {
    Write-Host "    Status: RUNNING" -ForegroundColor Green
    Write-Host "    PID: $($dockerProc.Id)" -ForegroundColor Gray
    Write-Host "    Memory: $([Math]::Round($dockerProc.WorkingSet64/1MB, 0)) MB" -ForegroundColor Gray
} else {
    Write-Host "    Status: NOT RUNNING" -ForegroundColor Red
}

# 2. Docker CLI
Write-Host "`n[2] Docker CLI" -ForegroundColor Yellow
try {
    $version = docker --version 2>&1
    Write-Host "    Version: $version" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: Docker command not found" -ForegroundColor Red
}

# 3. Docker Engine
Write-Host "`n[3] Docker Engine" -ForegroundColor Yellow
try {
    $info = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    Status: READY" -ForegroundColor Green
        $info | Select-String "Server Version", "Context", "Containers" | ForEach-Object {
            Write-Host "    $_" -ForegroundColor Gray
        }
    } else {
        Write-Host "    Status: NOT READY" -ForegroundColor Red
        $info | Select-Object -First 2 | ForEach-Object {
            Write-Host "    $_" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "    ERROR: $_" -ForegroundColor Red
}

# 4. Running Containers
Write-Host "`n[4] Running Containers" -ForegroundColor Yellow
try {
    $containers = docker ps --format "{{.Names}}" 2>$null
    if ($containers) {
        $containers | ForEach-Object {
            Write-Host "    - $_" -ForegroundColor Green
        }
    } else {
        Write-Host "    None" -ForegroundColor Gray
    }
} catch {
    Write-Host "    Cannot check (Docker not ready)" -ForegroundColor Gray
}

# 5. Port Check
Write-Host "`n[5] Port Availability" -ForegroundColor Yellow
$ports = @(4566, 4571)
foreach ($port in $ports) {
    try {
        $listener = [System.Net.Sockets.TcpClient]::new()
        $listener.Connect("localhost", $port)
        $listener.Close()
        Write-Host "    Port $port : IN USE" -ForegroundColor Yellow
    } catch {
        Write-Host "    Port $port : AVAILABLE" -ForegroundColor Green
    }
}

# 6. WSL Status
Write-Host "`n[6] WSL Status" -ForegroundColor Yellow
try {
    $wsl = wsl --status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    Status: INSTALLED" -ForegroundColor Green
    } else {
        Write-Host "    Status: NOT INSTALLED or ERROR" -ForegroundColor Red
    }
} catch {
    Write-Host "    Cannot check WSL" -ForegroundColor Gray
}

Write-Host "`n=== End of Diagnostic ===" -ForegroundColor Cyan
Write-Host ""

