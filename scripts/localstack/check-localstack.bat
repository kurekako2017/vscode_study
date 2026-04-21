@echo off
:: 脚本: check-localstack.bat
:: 说明: 快速检查/启动 LocalStack 容器并测试健康接口。
:: 用法: scripts\localstack\check-localstack.bat

echo ===== LocalStack Status Check =====
echo.
echo Checking Docker...
docker --version
echo.
echo Checking LocalStack container...
docker ps -a --filter "name=localstack"
echo.
echo Starting LocalStack if not running...
docker start localstack
echo.
echo Waiting 5 seconds...
timeout /t 5 /nobreak >nul
echo.
echo Checking LocalStack status...
docker ps --filter "name=localstack"
echo.
echo Testing LocalStack health endpoint...
curl -s http://localhost:4566/_localstack/health
echo.
echo.
echo ===== Check Complete =====
pause

