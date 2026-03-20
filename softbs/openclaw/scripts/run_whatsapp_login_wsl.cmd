@echo off
title OpenClaw WhatsApp Login (WSL)
echo Running WSL OpenClaw WhatsApp login...
wsl.exe bash -lc "cd ~ && openclaw channels login --channel whatsapp"
echo.
echo Command finished. Press any key to close.
pause >nul
