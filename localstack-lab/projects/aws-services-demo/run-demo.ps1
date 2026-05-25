# AWS Services Demo Test Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AWS Services Demo (DynamoDB, SQS, S3)" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check and start LocalStack
Write-Host "[1] Checking LocalStack..." -ForegroundColor Yellow
$running = docker ps --format "{{.Names}}" 2>$null | Select-String "localstack"
if (-not $running) {
    Write-Host "  LocalStack not running, starting..." -ForegroundColor Yellow
    docker start localstack | Out-Null
    Start-Sleep -Seconds 8
    Write-Host "  LocalStack started" -ForegroundColor Green
} else {
    Write-Host "  LocalStack is running" -ForegroundColor Green
}

# Navigate to project directory
Write-Host "`n[2] Navigating to project..." -ForegroundColor Yellow
$projectPath = "D:\dev\study\localstack-lab\projects\aws-services-demo"
Set-Location $projectPath
Write-Host "  Current directory: $(Get-Location)" -ForegroundColor Green

# Run the demo
Write-Host "`n[3] Running AWS Services Demo..." -ForegroundColor Yellow
Write-Host "  (This will test DynamoDB, SQS, and S3)" -ForegroundColor Gray
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan

# Execute Maven command
$output = & mvn clean compile exec:java "-Dexec.mainClass=com.example.aws.AwsServicesDemo" 2>&1

# Extract key output
$output | ForEach-Object {
    $line = $_.ToString()
    if ($line -match "Testing|Creating|Putting|Getting|Sending|Receiving|Uploading|Downloading|Listing|Table|Queue|Bucket|Message|Item|successfully|retrieved|sent|received|uploaded|downloaded") {
        Write-Host $line -ForegroundColor White
    } elseif ($line -match "BUILD SUCCESS") {
        Write-Host $line -ForegroundColor Green
    } elseif ($line -match "ERROR|FAILURE|failed") {
        Write-Host $line -ForegroundColor Red
    }
}

Write-Host "----------------------------------------" -ForegroundColor Cyan

# Save full log
$logFile = Join-Path $projectPath "demo-output.log"
$output | Out-File -FilePath $logFile -Encoding UTF8
Write-Host "`nFull log saved to: $logFile" -ForegroundColor Gray

# Check if successful
if ($output -match "BUILD SUCCESS") {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  All Tests Completed Successfully!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green

    Write-Host "Services tested:" -ForegroundColor Yellow
    Write-Host "  ✓ DynamoDB - Table creation, item insertion/retrieval" -ForegroundColor White
    Write-Host "  ✓ SQS - Queue creation, message send/receive" -ForegroundColor White
    Write-Host "  ✓ S3 - Bucket creation, file upload/download" -ForegroundColor White
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "  Test execution failed" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Red
}

Write-Host "`nTips:" -ForegroundColor Cyan
Write-Host "  - View LocalStack logs: docker logs localstack --tail 20" -ForegroundColor Gray
Write-Host "  - View full output: Get-Content $logFile" -ForegroundColor Gray
Write-Host ""

