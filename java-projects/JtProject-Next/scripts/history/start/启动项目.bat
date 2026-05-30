@echo off
echo ========================================
echo JT Spring Project - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Java...
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Java not found in PATH
    echo Please install JDK 11 or later
    pause
    exit /b 1
)

echo [2/3] Checking JAR file...
if not exist "target\JtSpringProject-0.0.1-SNAPSHOT.jar" (
    echo ERROR: JAR file not found
    echo Please compile the project first using: mvn clean package
    pause
    exit /b 1
)

echo [3/3] Starting application...
echo.
echo Application URL: http://localhost:8080
echo Press Ctrl+C to stop
echo ========================================
echo.

java -jar target\JtSpringProject-0.0.1-SNAPSHOT.jar

pause

