@echo off
setlocal

:: 脚本: sync-from-wsl.bat
:: 说明: 一键从 WSL 主目录拉取最新内容到 Windows D 盘仓库。
:: 用法:
::   scripts\wsl\sync-from-wsl.bat
::   powershell -ExecutionPolicy Bypass -File .\scripts\wsl\sync-from-wsl.ps1

powershell -ExecutionPolicy Bypass -File "%~dp0sync-from-wsl.ps1" %*
if errorlevel 1 pause
exit /b %errorlevel%