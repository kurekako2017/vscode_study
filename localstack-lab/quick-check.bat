@echo off
echo ========================================
echo   LocalStack Quick Check
echo ========================================
echo.

echo [Step 1] Checking Docker...
docker --version
if errorlevel 1 (
    echo ERROR: Docker not found
    goto :end
)
echo OK
echo.

echo [Step 2] Checking Docker service...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running
    echo SOLUTION: Start Docker Desktop from Start Menu
    goto :end
)
echo OK
echo.

echo [Step 3] Checking LocalStack container...
docker ps -a | findstr localstack
if errorlevel 1 (
    echo ERROR: LocalStack container not found
    echo SOLUTION: Run: docker run -d --name localstack -p 4566:4566 localstack/localstack
    goto :end
)
echo.

echo [Step 4] Checking if LocalStack is running...
docker ps | findstr localstack
if errorlevel 1 (
    echo WARNING: LocalStack is stopped
    echo Attempting to start...
    docker start localstack
    timeout /t 5 /nobreak >nul
    docker ps | findstr localstack
)
echo.

echo [Step 5] Testing LocalStack API...
curl -s http://localhost:4566/_localstack/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot connect to LocalStack API
    echo Container may still be starting...
) else (
    echo OK: LocalStack API is accessible
)
echo.

echo ========================================
echo   Diagnostic Complete
echo ========================================
echo.
echo Quick commands:
echo   Start LocalStack: docker start localstack
echo   View logs: docker logs localstack --tail 20
echo   Run test: cd projects\hello-localstack-java ^&^& test-localstack.ps1
echo.

:end
pause

