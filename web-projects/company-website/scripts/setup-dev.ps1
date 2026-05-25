# Windows 开发环境快速设置脚本

Write-Host "🚀 开始设置开发环境..." -ForegroundColor Green

# 检查 Node.js
try {
    $nodeVersion = node -v
    Write-Host "✅ Node.js 版本: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未安装 Node.js" -ForegroundColor Red
    Write-Host "请访问 https://nodejs.org/ 下载安装" -ForegroundColor Yellow
    exit 1
}

# 检查 pnpm
try {
    $pnpmVersion = pnpm -v
    Write-Host "✅ pnpm 版本: $pnpmVersion" -ForegroundColor Green
} catch {
    Write-Host "📦 安装 pnpm..." -ForegroundColor Yellow
    npm install -g pnpm
}

# 安装前端依赖
Write-Host "📦 安装前端依赖..." -ForegroundColor Yellow
Set-Location frontend
pnpm install

# 创建环境变量文件
if (-not (Test-Path .env.local)) {
    Write-Host "📝 创建 .env.local..." -ForegroundColor Yellow
    Copy-Item .env.example .env.local
    Write-Host "⚠️  请编辑 .env.local 填入你的配置" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ 设置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📚 下一步操作：" -ForegroundColor Cyan
Write-Host "1. 编辑 frontend\.env.local 填入你的 Supabase 配置"
Write-Host "2. 运行 'cd frontend; pnpm dev' 启动开发服务器"
Write-Host "3. 访问 http://localhost:3000"
Write-Host ""
Write-Host "📖 完整文档请查看: docs\GETTING_STARTED.md" -ForegroundColor Cyan
