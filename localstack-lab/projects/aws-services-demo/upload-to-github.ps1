# Git 上传脚本 - AWS Services Demo 项目

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  上传 AWS Services Demo 项目到 GitHub" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 切换到 study 目录
$studyPath = "D:\dev\study"
Set-Location $studyPath

# 检查是否是 Git 仓库
if (-not (Test-Path ".git")) {
    Write-Host "错误: 当前目录不是 Git 仓库" -ForegroundColor Red
    Write-Host "请先初始化 Git 仓库:" -ForegroundColor Yellow
    Write-Host "  git init" -ForegroundColor White
    Write-Host "  git remote add origin https://github.com/kurekako2017/study.git" -ForegroundColor White
    exit 1
}

# 1. 查看当前状态
Write-Host "[1] 查看 Git 状态..." -ForegroundColor Yellow
git status

# 2. 添加 aws-services-demo 项目
Write-Host "`n[2] 添加 aws-services-demo 项目..." -ForegroundColor Yellow
git add localstack-lab/projects/aws-services-demo/

# 3. 查看将要提交的文件
Write-Host "`n[3] 将要提交的文件:" -ForegroundColor Yellow
git diff --cached --name-only | Select-Object -First 50

# 4. 提交更改
Write-Host "`n[4] 提交更改..." -ForegroundColor Yellow
$commitMessage = "Add AWS Services Demo project for LocalStack testing

Complete Java application with DynamoDB, SQS, and S3 tests
Detailed JavaDoc comments and comprehensive documentation
Automatic log file generation for test results
Maven project with AWS SDK v2 dependencies"

git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n! 没有需要提交的更改，或者提交失败" -ForegroundColor Yellow
    Write-Host "  可能文件已经提交过了" -ForegroundColor Gray
}

# 5. 推送到 GitHub
Write-Host "`n[5] 推送到 GitHub..." -ForegroundColor Yellow
Write-Host "  目标仓库: https://github.com/kurekako2017/study.git" -ForegroundColor Gray

git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  ✓ 上传成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`n项目已上传到 GitHub:" -ForegroundColor Yellow
    Write-Host "  https://github.com/kurekako2017/study/tree/main/localstack-lab/projects/aws-services-demo" -ForegroundColor Cyan
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "  ✗ 上传失败" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "`n可能的原因:" -ForegroundColor Yellow
    Write-Host "  1. 远程仓库未配置" -ForegroundColor White
    Write-Host "  2. 需要身份验证" -ForegroundColor White
    Write-Host "  3. 网络连接问题" -ForegroundColor White
    Write-Host "`n请手动执行:" -ForegroundColor Yellow
    Write-Host "  cd D:\dev\study" -ForegroundColor White
    Write-Host "  git push origin main" -ForegroundColor White
}

Write-Host ""

