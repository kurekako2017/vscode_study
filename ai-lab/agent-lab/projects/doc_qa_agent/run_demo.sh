#!/bin/bash
# doc_qa_agent 演示运行脚本（Bash）
# 用法: bash run_demo.sh [-d path/to/docs]

DOC_DIR="./docs"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--docdir)
            DOC_DIR="$2"
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

echo "Setting up doc_qa_agent demo..."

# 检查文档目录
if [ ! -d "$DOC_DIR" ]; then
    echo "WARNING: Document directory '$DOC_DIR' not found."
    echo "Creating sample documents..."
    mkdir -p "$DOC_DIR"
    cat > "$DOC_DIR/sample.md" << 'EOF'
# Sample Document

This is a sample document for the Q&A agent demo.
It demonstrates how the agent searches documents and answers questions.
EOF
fi

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
echo "Running demo: Document Q&A Agent"
echo "Document directory: $DOC_DIR"
echo "Type 'quit' to exit."
echo ""

python main.py --docdir "$DOC_DIR"

echo ""
echo "Demo completed."
