@echo off
:: 脚本: show-localstack-logs.bat
:: 说明: 确保 LocalStack 正在运行并输出最近日志。
:: 用法: scripts\localstack\show-localstack-logs.bat

chcp 65001 >nul
echo.
echo ========================================
echo    LocalStack 日志查看演示
echo ========================================
echo.

echo [1/4] 检查 Docker 状态...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Docker 未运行，请先启动 Docker Desktop
    pause
    exit /b 1
)
echo ✓ Docker 正在运行
echo.

echo [2/4] 检查 LocalStack 容器...
docker inspect localstack >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ LocalStack 容器不存在
    pause
    exit /b 1
)

docker ps --filter "name=localstack" --filter "status=running" | findstr localstack >nul
if %errorlevel% neq 0 (
    echo ! LocalStack 容器已停止，正在启动...
    docker start localstack
    timeout /t 5 /nobreak >nul
)
echo ✓ LocalStack 容器正在运行
echo.

echo [3/4] 显示容器信息...
docker ps --filter "name=localstack" --format "容器名: {{.Names}} | 状态: {{.Status}} | 端口: {{.Ports}}"
echo.

echo [4/4] 显示最近 20 行日志...
echo ----------------------------------------
docker logs localstack --tail 20
echo ----------------------------------------
echo.

echo ========================================
echo 如何查看更多日志:
echo ----------------------------------------
echo 1. 实时日志:  docker logs -f localstack
echo 2. 最近日志:  docker logs localstack --tail 50
echo 3. 图形界面:  打开 Docker Desktop ^> Containers ^> localstack ^> Logs
echo ========================================
echo.
pause

