@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  运行 LocalStack Java 示例程序
echo ========================================
echo.

echo [1/3] 检查 LocalStack 是否运行...
docker ps | findstr localstack >nul 2>&1
if %errorlevel% neq 0 (
    echo ! LocalStack 未运行，正在启动...
    docker start localstack
    timeout /t 5 /nobreak >nul
    echo ✓ LocalStack 已启动
) else (
    echo ✓ LocalStack 正在运行
)
echo.

echo [2/3] 编译项目...
call mvn clean compile
if %errorlevel% neq 0 (
    echo ✗ 编译失败
    pause
    exit /b 1
)
echo.

echo [3/3] 运行程序...
echo ----------------------------------------
call mvn exec:java -Dexec.mainClass="com.example.localstack.App"
echo ----------------------------------------
echo.

echo ========================================
echo  程序执行完成
echo ========================================
echo.

echo 提示: 查看 LocalStack 日志
echo   docker logs localstack --tail 20
echo.
pause

