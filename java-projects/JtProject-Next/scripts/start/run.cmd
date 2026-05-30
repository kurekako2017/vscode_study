@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - Start
echo ========================================
echo.
echo Starting Spring Boot with Maven Wrapper...
echo Default URL: http://localhost:8082/
echo Press Ctrl+C to stop
echo.

call mvnw.cmd spring-boot:run
