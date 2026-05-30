#!/bin/bash
# llm-lab/examples 运行脚本（Bash）
# 用法: bash run_example.sh [example_name]
# 示例: bash run_example.sh basics
# 示例: bash run_example.sh pydantic_example

EXAMPLE_NAME="${1:-basics}"
EXAMPLE_FILE="$EXAMPLE_NAME.py"

if [ ! -f "$EXAMPLE_FILE" ]; then
    echo "ERROR: Example file '$EXAMPLE_FILE' not found."
    echo "Available examples:"
    ls -1 *.py | sed 's/.py$//' | sed 's/^/  - /'
    exit 1
fi

# 提示 OPENAI_API_KEY（model_call_example 无 Key 时会自动 mock）
if [[ "$EXAMPLE_NAME" == "model_call_example" ]] || [[ "$EXAMPLE_NAME" == *"model"* ]]; then
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "INFO: OPENAI_API_KEY is not set; model_call_example will use mock mode."
        echo "For real API calls, set it first:"
        echo "export OPENAI_API_KEY='your-api-key'"
    fi
fi

echo "Setting up llm-lab/examples..."

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

# 运行示例
echo ""
echo "Running example: $EXAMPLE_NAME"
echo ""

python "$EXAMPLE_FILE"

echo ""
echo "Example completed."
