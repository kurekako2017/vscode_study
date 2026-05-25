# llm-lab Python 示例集合

本目录包含面向 `llm-lab` 主线的最小 Python 示例，每个示例都带有丰富注释，便于快速上手与改造。

示例清单：

- `basics.py`：Python 基础语法与函数示例
- `dataclass_example.py`：`dataclasses` 使用示例
- `pydantic_example.py`：`pydantic` 数据验证示例
- `file_io_example.py`：JSON / CSV 读写示例
- `text_split_example.py`：文本分割（RAG 前处理）示例
- `model_call_example.py`：最小模型调用示例（使用 `openai` SDK，需配置 `OPENAI_API_KEY`）

## 🚀 快速运行

### 自动脚本（推荐）

**Windows (PowerShell):**
```powershell
.\run_example.ps1 basics
.\run_example.ps1 pydantic_example
.\run_example.ps1 model_call_example
```

**Linux / macOS (Bash):**
```bash
bash run_example.sh basics
bash run_example.sh pydantic_example
bash run_example.sh model_call_example
```

### 或手动运行

1. 进入示例目录：

```bash
cd llm-lab/examples
```

2. 安装依赖（可选）：

```bash
pip install -r requirements.txt
```

3. 运行示例：

```bash
python basics.py
python dataclass_example.py
python pydantic_example.py
python file_io_example.py
python text_split_example.py
python model_call_example.py "一句话解释什么是 agent"  # 需要 OPENAI_API_KEY
```

## 前置要求

- Python 3.10+
- 对 `model_call_example`：需设置环境变量 `OPENAI_API_KEY`

注意：所有示例都包含注释，便于理解每一行代码的意图。如需我把某个示例复制到 `llm-lab/projects` 下以便修改，请告知。
