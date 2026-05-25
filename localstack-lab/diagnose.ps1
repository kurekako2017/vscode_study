# LocalStack Diagnostic Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  LocalStack Environment Diagnostic" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$issues = @()
$allOk = $true

# 1. Check Docker Desktop
Write-Host "[1/7] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Docker installed: $dockerVersion" -ForegroundColor Green

        # Check if Docker is running
        $dockerInfo = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK Docker service is running" -ForegroundColor Green
        } else {
            Write-Host "  ERROR Docker service not running" -ForegroundColor Red
            $issues += "Docker Desktop is not started - Please open Docker Desktop"
            $allOk = $false
        }
    } else {
        Write-Host "  ERROR Docker not installed or not in PATH" -ForegroundColor Red
        $issues += "Docker not installed or not configured in environment variables"
        $allOk = $false
    }
} catch {
    Write-Host "  ERROR Cannot access Docker: $($_.Exception.Message)" -ForegroundColor Red
    $issues += "Docker access failed - May not be started"
    $allOk = $false
}

# 2. Check LocalStack container
Write-Host "`n[2/7] Checking LocalStack container..." -ForegroundColor Yellow
try {
    $containers = docker ps -a --format "{{.Names}},{{.Status}},{{.Ports}}" 2>&1 | Select-String "localstack"
    if ($containers) {
        Write-Host "  OK LocalStack container found" -ForegroundColor Green
        $containers | ForEach-Object {
            $parts = $_.ToString().Split(',')
            $name = $parts[0]
            $status = $parts[1]
            $ports = if ($parts.Length -gt 2) { $parts[2] } else { "none" }

            Write-Host "    Container: $name" -ForegroundColor White
            Write-Host "    Status: $status" -ForegroundColor White
            Write-Host "    Ports: $ports" -ForegroundColor White

            if ($status -notmatch "Up") {
                $issues += "LocalStack container is stopped - Need to start"
                $allOk = $false
            }
        }
    } else {
        Write-Host "  ERROR LocalStack container not found" -ForegroundColor Red
        $issues += "LocalStack container does not exist - Need to create"
        $allOk = $false
    }
} catch {
    Write-Host "  ERROR Cannot check containers: $($_.Exception.Message)" -ForegroundColor Red
    $issues += "Cannot access Docker container list"
    $allOk = $false
}

# 3. Check port 4566
Write-Host "`n[3/7] Checking port 4566..." -ForegroundColor Yellow
try {
    $portCheck = Test-NetConnection -ComputerName localhost -Port 4566 -WarningAction SilentlyContinue 2>&1
    if ($portCheck.TcpTestSucceeded) {
        Write-Host "  OK Port 4566 is accessible" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Port 4566 is not accessible" -ForegroundColor Red
        $issues += "Port 4566 not accessible - LocalStack may not be started"
        $allOk = $false
    }
} catch {
    Write-Host "  WARNING Cannot test port connection" -ForegroundColor Yellow
}

# 4. Check Java
Write-Host "`n[4/7] Checking Java environment..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Java installed: $javaVersion" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Java not installed or not configured" -ForegroundColor Red
        $issues += "Java environment issue"
        $allOk = $false
    }
} catch {
    Write-Host "  ERROR Java not found" -ForegroundColor Red
    $issues += "Java not installed"
    $allOk = $false
}

# 5. Check Maven
Write-Host "`n[5/7] Checking Maven environment..." -ForegroundColor Yellow
try {
    $mvnVersion = mvn -version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Maven installed: $mvnVersion" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Maven not installed or not configured" -ForegroundColor Red
        $issues += "Maven environment issue"
        $allOk = $false
    }
} catch {
    Write-Host "  ERROR Maven not found" -ForegroundColor Red
    $issues += "Maven not installed"
    $allOk = $false
}

# 6. Check project files
Write-Host "`n[6/7] Checking project files..." -ForegroundColor Yellow
$projectPath = "D:\dev\study\localstack-lab\projects\hello-localstack-java"
if (Test-Path $projectPath) {
    Write-Host "  OK Project directory exists" -ForegroundColor Green

    $pomPath = Join-Path $projectPath "pom.xml"
    if (Test-Path $pomPath) {
        Write-Host "  OK pom.xml exists" -ForegroundColor Green
    } else {
        Write-Host "  ERROR pom.xml does not exist" -ForegroundColor Red
        $issues += "Project configuration file missing"
        $allOk = $false
    }

    $scriptPath = Join-Path $projectPath "test-localstack.ps1"
    if (Test-Path $scriptPath) {
        Write-Host "  OK Test script exists" -ForegroundColor Green
    } else {
        Write-Host "  WARNING Test script does not exist (optional)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ERROR Project directory does not exist" -ForegroundColor Red
    $issues += "Project directory not found"
    $allOk = $false
}

# 7. Test LocalStack connection
Write-Host "`n[7/7] Testing LocalStack API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4566/_localstack/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  OK LocalStack API accessible (HTTP $($response.StatusCode))" -ForegroundColor Green

    $health = $response.Content | ConvertFrom-Json
    Write-Host "    Available services:" -ForegroundColor Cyan
    $health.services.PSObject.Properties | Select-Object -First 5 | ForEach-Object {
        $status = if ($_.Value -eq "available" -or $_.Value -eq "running") { "OK" } else { "X" }
        $color = if ($_.Value -eq "available" -or $_.Value -eq "running") { "Green" } else { "Yellow" }
        Write-Host "      $status $($_.Name): $($_.Value)" -ForegroundColor $color
    }
} catch {
    Write-Host "  ERROR Cannot connect to LocalStack API" -ForegroundColor Red
    $issues += "LocalStack API not accessible - Container may not be running"
    $allOk = $false
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Diagnostic Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($allOk) {
    Write-Host "SUCCESS All checks passed! Environment is ready" -ForegroundColor Green
    Write-Host "`nYou can run the test:" -ForegroundColor Yellow
    Write-Host "  cd $projectPath" -ForegroundColor White
    Write-Host "  .\test-localstack.ps1" -ForegroundColor White
} else {
    Write-Host "PROBLEMS FOUND: $($issues.Count) issue(s):" -ForegroundColor Red
    Write-Host ""
    $issues | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor Yellow
    }

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  Solutions" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Provide specific solutions
    if ($issues -match "Docker.*not started") {
        Write-Host "[Solution 1] Start Docker Desktop" -ForegroundColor Yellow
        Write-Host "  1. Search for 'Docker Desktop' in Start Menu" -ForegroundColor White
        Write-Host "  2. Launch Docker Desktop" -ForegroundColor White
        Write-Host "  3. Wait for Docker engine to start (tray icon shows running)" -ForegroundColor White
        Write-Host "  4. Re-run this diagnostic script" -ForegroundColor White
        Write-Host ""
    }

    if ($issues -match "LocalStack.*stopped") {
        Write-Host "[Solution 2] Start LocalStack container" -ForegroundColor Yellow
        Write-Host "  Run command:" -ForegroundColor White
        Write-Host "    docker start localstack" -ForegroundColor Cyan
        Write-Host ""
    }

    if ($issues -match "container does not exist") {
        Write-Host "[Solution 3] Create LocalStack container" -ForegroundColor Yellow
        Write-Host "  Run command:" -ForegroundColor White
        Write-Host "    docker run -d --name localstack -p 4566:4566 localstack/localstack" -ForegroundColor Cyan
        Write-Host ""
    }

    if ($issues -match "Port.*not accessible") {
        Write-Host "[Solution 4] Check port usage" -ForegroundColor Yellow
        Write-Host "  Check what is using port 4566:" -ForegroundColor White
        Write-Host "    netstat -ano | findstr 4566" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host "`nQuick action commands:" -ForegroundColor Cyan
Write-Host "  - Start Docker Desktop: Launch from Start Menu" -ForegroundColor White
Write-Host "  - Start LocalStack: docker start localstack" -ForegroundColor White
Write-Host "  - View container logs: docker logs localstack --tail 20" -ForegroundColor White
Write-Host "  - Restart LocalStack: docker restart localstack" -ForegroundColor White
Write-Host "  - Run test: cd $projectPath; .\test-localstack.ps1" -ForegroundColor White
Write-Host ""

# Auto-fix option
if (-not $allOk) {
    Write-Host "Attempt auto-fix? (Y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host

    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host "`nAttempting auto-fix..." -ForegroundColor Cyan

        # Try to start LocalStack
        try {
            Write-Host "  Trying to start LocalStack container..." -ForegroundColor Yellow
            docker start localstack 2>&1 | Out-Null
            Start-Sleep -Seconds 5

            $status = docker ps --format "{{.Names}}: {{.Status}}" | Select-String "localstack"
            if ($status) {
                Write-Host "  OK LocalStack started" -ForegroundColor Green
            } else {
                Write-Host "  ERROR LocalStack start failed" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ERROR Auto-fix failed: $($_.Exception.Message)" -ForegroundColor Red
        }

        Write-Host "`nPlease re-run this script to verify the fix" -ForegroundColor Yellow
    }
}

Write-Host ""

