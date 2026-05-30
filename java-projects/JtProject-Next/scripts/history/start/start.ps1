Write-Host "Starting JT E-commerce System..." -ForegroundColor Green
Set-Location "D:\dev\source_code\vscode_study\java-projects\JtProject"

# Try to find Java
$javaPaths = @(
    "C:\Program Files\jdk-21.0.2\bin\java.exe",
    "C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot\bin\java.exe",
    "C:\Program Files\Java\jdk-11\bin\java.exe",
    "C:\Program Files\Java\jdk-17\bin\java.exe",
    "C:\Program Files\Java\jdk1.8.0_301\bin\java.exe"
)

$javaExe = $null
foreach ($path in $javaPaths) {
    if (Test-Path $path) {
        $javaExe = $path
        Write-Host "Found Java at: $javaExe" -ForegroundColor Cyan
        break
    }
}

if (-not $javaExe) {
    Write-Host "ERROR: Java not found!" -ForegroundColor Red
    Write-Host "Please install Java 11 or later" -ForegroundColor Yellow
    exit 1
}

# Check if JAR exists
$jarFile = ".\target\JtSpringProject-0.0.1-SNAPSHOT.jar"
if (-not (Test-Path $jarFile)) {
    Write-Host "ERROR: JAR file not found at $jarFile" -ForegroundColor Red
    Write-Host "Please run: mvn clean package" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting application..." -ForegroundColor Green
Write-Host "Access URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

Start-Process -FilePath $javaExe -ArgumentList "-jar", $jarFile -NoNewWindow -Wait

