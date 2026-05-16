#!/bin/bash
# structured_output_demo 演示运行脚本（Bash）
# 用法: bash run_demo.sh

# 检查 OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: OPENAI_API_KEY is not set."
    echo "Please set: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

echo "Setting up structured_output_demo..."

# 创建虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "Activating virtual environment..."
source .venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -q -r requirements.txt

# 运行演示
echo ""
echo "Running demo: Structured output (Pydantic) with Responses API"
echo "Generating an agent plan using Responses.parse()..."
echo ""

python main.py

echo ""
echo "Demo completed."
