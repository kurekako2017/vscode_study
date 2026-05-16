#!/bin/bash
# tool_agent_demo 演示运行脚本（Bash）
# 用法: bash run_demo.sh [-p "Your task here"] [-w path]

PROMPT="List all files in the current directory and search for any markdown files"
WORKDIR="."

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--prompt)
            PROMPT="$2"
            shift 2
            ;;
        -w|--workdir)
            WORKDIR="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# 检查 OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: OPENAI_API_KEY is not set."
    echo "Please set: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

echo "Setting up tool_agent_demo..."

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
echo "Running demo: Tool-Calling Agent"
echo "Prompt: $PROMPT"
echo "Working directory: $WORKDIR"
echo ""

python main.py "$PROMPT" --workdir "$WORKDIR"

echo ""
echo "Demo completed."
