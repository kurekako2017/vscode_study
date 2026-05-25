@echo off
echo ===== LocalStack 测试开始 =====
echo.

echo [1] 检查 LocalStack 状态...
docker ps | findstr localstack
if errorlevel 1 (
    echo LocalStack 未运行，正在启动...
    docker start localstack
    timeout /t 8 /nobreak
) else (
    echo LocalStack 已运行
)

echo.
echo [2] 进入项目目录...
cd /d D:\dev\study\localstack-lab\projects\hello-localstack-java

echo.
echo [3] 运行测试程序...
echo 这将需要约 20-30 秒时间...
echo.

call mvn exec:java -Dexec.mainClass="com.example.localstack.App"

echo.
echo ===== 测试完成 =====
pause

