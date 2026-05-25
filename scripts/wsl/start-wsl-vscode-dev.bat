@echo off
setlocal

:: 脚本: start-wsl-vscode-dev.bat
:: 说明: 一键启动 WSL Ubuntu + 仓库目录 + VS Code。
:: 用法:
::   scripts\wsl\start-wsl-vscode-dev.bat         (mapped D: path mode)
::   scripts\wsl\start-wsl-vscode-dev.bat local   (WSL local repo mode)

set "WSL_DISTRO=Ubuntu"
set "WSL_ROOT_MNT=/mnt/d/dev/source_code"
set "WSL_REPO_MNT=/mnt/d/dev/source_code/vscode_study"
set "WSL_ROOT_LOCAL=/home/victorkure/workspace"
set "WSL_REPO_LOCAL=/home/victorkure/workspace/vscode_study"
set "WIN_REPO=D:\dev\source_code\vscode_study"
set "MODE=%~1"

if "%MODE%"=="" set "MODE=mnt"

if /I "%MODE%"=="mnt" (
  set "WSL_ROOT=%WSL_ROOT_MNT%"
  set "WSL_REPO=%WSL_REPO_MNT%"
) else if /I "%MODE%"=="local" (
  set "WSL_ROOT=%WSL_ROOT_LOCAL%"
  set "WSL_REPO=%WSL_REPO_LOCAL%"
) else (
  echo [ERROR] Invalid mode: %MODE%
  echo [INFO] Usage: scripts\wsl\start-wsl-vscode-dev.bat [mnt^|local]
  exit /b 1
)

echo [INFO] Starting WSL distro: %WSL_DISTRO% ^(mode=%MODE%^)

wsl -d %WSL_DISTRO% -- bash -lc "test -d '%WSL_REPO%/.git'"
if errorlevel 1 (
  if /I "%MODE%"=="local" (
    echo [WARN] Local WSL repo not found: %WSL_REPO%
    echo [INFO] Initialize it first with: bash ./scripts/wsl/init-wsl-local-repo.sh
    echo [INFO] Fallback to mapped Windows repo: %WSL_REPO_MNT%
    set "MODE=mnt"
    set "WSL_ROOT=%WSL_ROOT_MNT%"
    set "WSL_REPO=%WSL_REPO_MNT%"
  ) else (
    echo [ERROR] Repo not found in mapped path: %WSL_REPO%
    echo [INFO] Confirm D:\dev\source_code\vscode_study exists and is accessible in WSL.
    exit /b 1
  )
)

set "WT_FOUND=0"
where wt >nul 2>nul && set "WT_FOUND=1"

if "%WT_FOUND%"=="1" (
  start "" wt new-tab --title "Ubuntu Dev %MODE%" wsl.exe -d %WSL_DISTRO% --cd %WSL_ROOT%
) else (
  echo [WARN] Windows Terminal ^(wt^) not found. Continuing without opening a new terminal tab.
)

echo [INFO] Opening VS Code in WSL repo: %WSL_REPO%
wsl -d %WSL_DISTRO% --cd %WSL_REPO% -- bash -lc "code ."
if errorlevel 1 (
  echo [WARN] Failed to launch VS Code from WSL. Trying Windows Code fallback.
  start "" code "%WIN_REPO%"
)

echo [INFO] Done.
exit /b 0
