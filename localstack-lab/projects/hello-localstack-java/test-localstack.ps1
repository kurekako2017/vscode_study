# LocalStack Test Script

Write-Host "`n===== LocalStack Test Started =====" -ForegroundColor Cyan
Write-Host ""

# 1. Check LocalStack
Write-Host "[1] Checking LocalStack status..." -ForegroundColor Yellow
$running = docker ps --format "{{.Names}}" 2>$null | Select-String "localstack"
if (-not $running) {
    Write-Host "  LocalStack not running, starting..." -ForegroundColor Yellow
    docker start localstack | Out-Null
    Write-Host "  Waiting for LocalStack to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 8
    Write-Host "  LocalStack started" -ForegroundColor Green
} else {
    Write-Host "  LocalStack is running" -ForegroundColor Green
}

# 2. Enter project directory
Write-Host "`n[2] Entering project directory..." -ForegroundColor Yellow
Set-Location "D:\dev\study\localstack-lab\projects\hello-localstack-java"
Write-Host "  Current directory: $(Get-Location)" -ForegroundColor Green

# 3. Run test
Write-Host "`n[3] Running LocalStack Java test..." -ForegroundColor Yellow
Write-Host "  (This will take about 20-30 seconds)" -ForegroundColor Gray
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan

# Execute Maven command
$output = & mvn exec:java "-Dexec.mainClass=com.example.localstack.App" 2>&1

# 提取关键输出
$output | ForEach-Object {
    $line = $_.ToString()
    if ($line -match "Endpoint:|Bucket:|Key:|Content:|Hello LocalStack") {
        Write-Host $line -ForegroundColor White
    } elseif ($line -match "BUILD SUCCESS") {
        Write-Host $line -ForegroundColor Green
    } elseif ($line -match "ERROR|FAILURE") {
        Write-Host $line -ForegroundColor Red
    }
}

Write-Host "----------------------------------------" -ForegroundColor Cyan

# 4. Show full log location
Write-Host "`n[4] Full log..." -ForegroundColor Yellow
$logFile = "D:\dev\study\localstack-lab\projects\hello-localstack-java\test-output.log"
$output | Out-File -FilePath $logFile -Encoding UTF8
Write-Host "  Full log saved to: $logFile" -ForegroundColor Green

Write-Host "`n===== Test Completed =====" -ForegroundColor Cyan
Write-Host ""

# Check if successful
if ($output -match "BUILD SUCCESS") {
    Write-Host "Test executed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Test operations:" -ForegroundColor Yellow
    Write-Host "  - Connected to LocalStack (port 4566)" -ForegroundColor White
    Write-Host "  - Created S3 bucket: hello-localstack-java" -ForegroundColor White
    Write-Host "  - Uploaded file: hello.txt" -ForegroundColor White
    Write-Host "  - Downloaded and read file content" -ForegroundColor White
} else {
    Write-Host "Test execution failed, check log file" -ForegroundColor Red
}

Write-Host ""
Write-Host "Tips:" -ForegroundColor Yellow
Write-Host "  - View LocalStack logs: docker logs localstack --tail 20" -ForegroundColor Gray
Write-Host "  - View full output: Get-Content $logFile" -ForegroundColor Gray
Write-Host ""

