#!/usr/bin/env bash

# AI 学习项目启动脚本

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "================================"
echo "AI 学习项目 - 环境设置"
echo "================================"
echo ""

if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "✓ 虚拟环境已存在: $VENV_DIR"
else
    if [ -d "$VENV_DIR" ]; then
        echo "⚠️ 检测到不完整的虚拟环境，正在重建..."
        rm -rf "$VENV_DIR"
    fi
    echo "📦 创建虚拟环境..."
    if ! python3 -m venv "$VENV_DIR"; then
        echo ""
        echo "❌ 无法创建虚拟环境。当前系统缺少 python3-venv。"
        echo ""
        echo "请先安装："
        echo "  sudo apt install python3.12-venv"
        echo "或："
        echo "  sudo apt install python3-venv"
        echo ""
        echo "安装后重新运行："
        echo "  bash setup.sh"
        exit 1
    fi
    echo "✓ 虚拟环境创建成功"
fi

echo ""
echo "🔌 激活虚拟环境..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo ""
echo "📦 升级 pip..."
pip install --upgrade pip setuptools wheel >/dev/null 2>&1
echo "✓ pip 已升级"

echo ""
echo "📦 安装依赖..."
pip install -r "$PROJECT_DIR/requirements.txt" >/dev/null 2>&1
echo "✓ 依赖安装成功"

echo ""
echo "================================"
echo "✅ 环境设置完成！"
echo "================================"
echo ""
echo "接下来的步骤："
echo ""
echo "1. 激活虚拟环境（如果还没有激活）："
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "2. 运行第一个示例："
echo "   python3 $PROJECT_DIR/01_python_basics.py"
echo ""
echo "3. 运行第二个示例："
echo "   python3 $PROJECT_DIR/02_numpy_intro.py"
echo ""
echo "4. 启动 Jupyter Notebook（推荐用于交互式学习）："
echo "   jupyter notebook $PROJECT_DIR"
echo ""
echo "5. 查看学习指南："
echo "   cat $PROJECT_DIR/LEARNING_GUIDE.md"
echo ""