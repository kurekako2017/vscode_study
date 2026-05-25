@echo off
cd /d D:\dev\study\localstack-lab\projects\hello-localstack-java
echo Running LocalStack Java Example...
echo.

REM Start LocalStack if not running
docker ps | findstr localstack >nul 2>&1
if errorlevel 1 (
    echo Starting LocalStack...
    docker start localstack
    timeout /t 5 /nobreak >nul
)

REM Run the application
echo Compiling and running...
call mvn clean compile exec:java -Dexec.mainClass="com.example.localstack.App" > execution-result.txt 2>&1

echo.
echo Execution completed. Results saved to execution-result.txt
echo Opening results file...
notepad execution-result.txt

