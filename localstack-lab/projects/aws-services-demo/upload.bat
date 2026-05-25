@echo off
chcp 65001 >nul
echo ========================================
echo   上传 AWS Services Demo 到 GitHub
echo ========================================
echo.

cd /d D:\dev\study

echo [1] 检查 Git 仓库...
if not exist .git (
    echo 错误: 不是 Git 仓库！
    echo 请先执行: git init
    pause
    exit /b 1
)

echo [2] 添加文件...
git add .

echo [3] 查看状态...
git status --short | findstr "aws-services-demo"

echo [4] 提交更改...
git commit -m "Add AWS Services Demo: Complete LocalStack testing project"

if errorlevel 1 (
    echo 注意: 可能没有新的更改需要提交
)

echo [5] 推送到 GitHub...
git push origin main

if errorlevel 0 (
    echo.
    echo ========================================
    echo   上传成功！
    echo ========================================
    echo.
    echo 查看项目: https://github.com/kurekako2017/study/tree/main/localstack-lab/projects/aws-services-demo
) else (
    echo.
    echo ========================================
    echo   上传失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 需要 Git 身份验证
    echo 2. 远程仓库未配置
    echo 3. 网络问题
)

echo.
pause

