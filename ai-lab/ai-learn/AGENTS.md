# ai-learn AGENTS.md 追加规则

# 模型调用优先级

ai-learn 目录下所有示例、项目、教程统一遵循以下模型调用优先级：

## 第一优先级

OpenRouter

统一从环境变量读取：

OPENROUTER_API_KEY

## 第二优先级

NVIDIA NIM

统一从环境变量读取：

NVIDIA_API_KEY

## 第三优先级

本地模型（Ollama）

默认模型：

qwen2.5-coder:1.5b

连接地址：

http://localhost:11434

禁止默认使用7B及以上模型。

## 第四优先级（最终兜底）

Mock模式

仅用于：

- API Key不存在
- 网络不可用
- OpenRouter失败
- NVIDIA失败
- Ollama未启动

禁止直接默认使用Mock。

必须优先尝试真实模型。

# 示例开发规范

# 环境变量规范

优先读取：

OPENROUTER_API_KEY

其次读取：

NVIDIA_API_KEY

最后检测：

OLLAMA_HOST

默认：

OLLAMA_HOST=http://localhost:11434

# README统一规范

每个例子的README必须包含：

## 项目目标

## 项目结构

## 运行方式

## Real Mode运行

## Mock Mode运行

## 测试清单

## 学习重点

## 常见问题

# 命令规范

所有命令必须从 ai-learn 根目录执行。

禁止：

cd example目录后执行

必须：

python agent-lab/projects/xxx/main.py

# 测试清单规范

每个README必须同时提供：

## 真实模型测试

### OpenRouter

python agent-lab/projects/xxx/main.py --provider openrouter

### NVIDIA

python agent-lab/projects/xxx/main.py --provider nvidia

### Ollama

python agent-lab/projects/xxx/main.py --provider ollama

## Mock测试

python agent-lab/projects/xxx/main.py --mock

# Agent教学规范

所有Agent示例必须解释：

- Prompt
- Model
- Tool
- Memory
- State
- Workflow

必须说明：

输入 -> Agent -> Tool -> LLM -> 输出

完整执行链路。

# LangGraph教学规范

必须说明：

- State是什么
- Node是什么
- Edge是什么
- Conditional Edge是什么
- Graph执行顺序是什么

# RAG教学规范

必须说明：

- Loader
- Chunk
- Embedding
- Vector Store
- Retriever
- Generation

完整数据流向。

# 文档优先原则

代码不是重点。

必须保证：

README能让人看懂。

即使不看代码，仅阅读README也能理解整个例子。
