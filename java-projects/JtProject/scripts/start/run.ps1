$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
Set-Location $projectRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JtSpringProject - Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project: $projectRoot" -ForegroundColor DarkGray
Write-Host ""

$wrapper = Join-Path $projectRoot "mvnw.cmd"
if (-not (Test-Path $wrapper)) {
    Write-Host "ERROR: mvnw.cmd not found" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Spring Boot with Maven Wrapper..." -ForegroundColor Green
Write-Host "Default URL: http://localhost:8082/" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

& $wrapper spring-boot:run
