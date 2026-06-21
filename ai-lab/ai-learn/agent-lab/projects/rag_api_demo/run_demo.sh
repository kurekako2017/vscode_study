#!/bin/bash
# rag_api_demo 演示运行脚本（Bash）
# 用法: bash run_demo.sh [-p port]

PORT=8000

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
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

echo "Setting up rag_api_demo..."

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
echo "Running demo: RAG API Server (FastAPI)"
echo "Server will start on http://127.0.0.1:$PORT"
echo "Press Ctrl+C to stop."
echo ""

uvicorn main:app --host 127.0.0.1 --port $PORT

echo ""
echo "Demo stopped."
