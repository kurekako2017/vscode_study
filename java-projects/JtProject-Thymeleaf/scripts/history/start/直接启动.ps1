# JT Spring Project - Direct Start Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JT Spring Project - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectDir = "D:\dev\source_code\vscode_study\java-projects\JtProject"
Set-Location $projectDir

$javaPath = "C:\Program Files\jdk-21.0.2\bin\java.exe"
$jarFile = "target\JtSpringProject-0.0.1-SNAPSHOT.jar"

if (-not (Test-Path $javaPath)) {
    Write-Host "ERROR: Java not found at $javaPath" -ForegroundColor Red
    Write-Host "Please check Java installation" -ForegroundColor Yellow
    pause
    exit 1
}

if (-not (Test-Path $jarFile)) {
    Write-Host "ERROR: JAR file not found" -ForegroundColor Red
    Write-Host "Location: $jarFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please compile first using one of:" -ForegroundColor Yellow
    Write-Host "  1. mvn clean package" -ForegroundColor White
    Write-Host "  2. In IDEA: Maven -> Lifecycle -> package" -ForegroundColor White
    pause
    exit 1
}

Write-Host "Starting application..." -ForegroundColor Green
Write-Host "Access URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& $javaPath -jar $jarFile

