#!/bin/bash
# 快速启动脚本 - JtSpringProject

set -e

PROJECT_DIR="/workspaces/study/java-projects/JtProject"
cd "$PROJECT_DIR"

echo "🚀 JtSpringProject 启动脚本"
echo "================================"
echo ""

# 显示可用的profile
echo "📋 可用的环境配置:"
echo "  1. 默认 (H2持久化) - 推荐"
echo "  2. local (H2持久化)"
echo "  3. remote (MySQL 192.168.10.2)"
echo "  4. mysql (本地MySQL)"
echo ""

# 读取用户选择
read -p "请选择环境 [1-4，默认1]: " choice
choice=${choice:-1}

PROFILE=""
case $choice in
    1)
        echo "✅ 使用默认H2配置"
        PROFILE=""
        ;;
    2)
        echo "✅ 使用local profile (H2)"
        PROFILE="-Dspring-boot.run.profiles=local"
        ;;
    3)
        echo "✅ 使用remote profile (MySQL 192.168.10.2)"
        PROFILE="-Dspring-boot.run.profiles=remote"
        ;;
    4)
        echo "✅ 使用mysql profile (本地MySQL)"
        PROFILE="-Dspring-boot.run.profiles=mysql"
        ;;
    *)
        echo "❌ 无效选择，使用默认配置"
        PROFILE=""
        ;;
esac

echo ""
echo "🔨 编译项目..."
mvn clean compile -q

echo ""
echo "🚀 启动应用..."
echo "   访问地址: http://localhost:8080"
echo "   H2控制台: http://localhost:8080/h2-console"
echo "   按 Ctrl+C 停止应用"
echo ""
echo "================================"
echo ""

if [ -z "$PROFILE" ]; then
    mvn spring-boot:run
else
    mvn spring-boot:run $PROFILE
fi
