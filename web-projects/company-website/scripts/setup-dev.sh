#!/bin/bash
# 开发环境快速设置脚本

set -e

echo "🚀 开始设置开发环境..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未安装 Node.js"
    echo "请访问 https://nodejs.org/ 下载安装"
    exit 1
fi

echo "✅ Node.js 版本: $(node -v)"

# 检查 pnpm
if ! command -v pnpm &> /dev/null; then
    echo "📦 安装 pnpm..."
    npm install -g pnpm
fi

echo "✅ pnpm 版本: $(pnpm -v)"

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
pnpm install

# 创建环境变量文件
if [ ! -f .env.local ]; then
    echo "📝 创建 .env.local..."
    cp .env.example .env.local
    echo "⚠️  请编辑 .env.local 填入你的配置"
fi

echo ""
echo "✅ 设置完成！"
echo ""
echo "📚 下一步操作："
echo "1. 编辑 frontend/.env.local 填入你的 Supabase 配置"
echo "2. 运行 'cd frontend && pnpm dev' 启动开发服务器"
echo "3. 访问 http://localhost:3000"
echo ""
echo "📖 完整文档请查看: docs/GETTING_STARTED.md"
