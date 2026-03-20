# 📘 Windows 11 本地 Aider + 大模型部署指南（UM890 Pro | 32G | Win11 Pro）

> **适用设备**
- 机器：UM890 Pro  
- CPU：Ryzen 9 7940HS  
- GPU：Radeon 780M（集成显卡，共享内存）  
- 内存：32GB  
- 系统：Windows 11 Pro  

---

## 目录
1. 架构与方案选择  
2. 磁盘与目录规划  
3. 显卡 / 内存关键设置  
4. Python 环境安装  
5. Ollama 安装与配置  
6. 模型下载与测试  
7. Aider 安装  
8. Aider 使用方式  
9. 性能与稳定性调优  
10. 常见问题（FAQ）

---


## 1️⃣ 架构与方案选择

### 方案一：Ollama + Aider（推荐，适合 AMD/集显/新手）
- Windows 下最稳定，支持 AMD/集显
- 操作简单，自动管理模型
- 架构：Aider → Ollama → 本地模型

### 方案二：llama-cpp-python + Aider（适合 NVIDIA 独显/高阶用户）
- 支持 CUDA，推理速度快
- 可自定义模型参数
- 架构：Aider → llama-cpp-python → 本地 GGUF 模型

---


## 2️⃣ 磁盘与目录规划（强烈建议）

**不要把模型放在 C 盘。**

推荐：
```
D:\ollama\models         # Ollama 模型目录
D:\LLM\models            # llama-cpp-python/自定义模型目录
D:\ai\venv               # Python 虚拟环境
```

---


## 3️⃣ 显卡 / 内存设置

### 1. NVIDIA 独显用户（如 RTX 3060/4060/4090 等）
- 建议安装最新版 NVIDIA 驱动
- 安装 CUDA Toolkit（推荐 11.8 或 12.x）
- 安装 cuDNN（与 CUDA 版本匹配）
- 检查环境变量：`CUDA_HOME`、`Path` 包含 CUDA/bin

### 2. AMD/集显用户（如 780M）
- BIOS 设置 UMA Frame Buffer Size：8GB 或 Auto
- Windows 虚拟内存（必须）：
	- 位置：D 盘
	- 初始：32768 MB
	- 最大：65536 MB

---


## 4️⃣ 安装 Python

- 安装 Python 3.10/3.11（推荐用 Anaconda/Miniconda 管理环境）
- 勾选 Add to PATH

验证：
```
python --version
pip --version
```

---


## 5️⃣ 安装 Ollama（推荐新手/集显/AMD）

下载：https://ollama.com/download/windows

设置模型目录：
```
setx OLLAMA_MODELS D:\ollama\models
```
重启系统。

---


## 6️⃣ 下载模型

### DeepSeek-Coder V2 Lite 16B
Ollama 方案：
```
ollama pull deepseek-coder-v2:16b-lite-q4_0
```

llama-cpp-python 方案：
1. 访问 [HuggingFace DeepSeek-Coder V2 Lite 16B GGUF](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-16B-GGUF)
2. 下载 Q4_0 或 Q5_0 量化 `.gguf` 文件到 `D:\LLM\models\deepseek-coder-v2-lite-16b`

### Qwen2.5-Coder 14B
Ollama 方案：
```
ollama pull qwen2.5-coder:14b-q4_0
```

llama-cpp-python 方案：
1. 访问 [HuggingFace Qwen2.5-Coder 14B GGUF](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-GGUF)
2. 下载 Q4_0 或 Q5_0 量化 `.gguf` 文件到 `D:\LLM\models\qwen2.5-coder-14b`

测试（Ollama）：
```
ollama run deepseek-coder-v2:16b-lite-q4_0
```

---


## 7️⃣ 安装 Aider

推荐用虚拟环境：
```
python -m venv D:\ai\venv
D:\ai\venv\Scripts\activate
pip install --upgrade pip
pip install aider-chat[all]
```
如遇网络问题可用：
```
pip install aider-chat[all] -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---


## 8️⃣ 使用 Aider

### 方案一：Ollama 直连

DeepSeek：
```
aider --model ollama/deepseek-coder-v2:16b-lite-q4_0 --no-stream
```
Qwen：
```
aider --model ollama/qwen2.5-coder:14b-q4_0 --no-stream
```

### 方案二：llama-cpp-python 本地 API
1. 安装 llama-cpp-python：
	```
	pip install llama-cpp-python --upgrade
	```
2. 启动本地模型服务（以 DeepSeek 为例）：
	```
	python -m llama_cpp.server --model D:\LLM\models\deepseek-coder-v2-lite-16b\deepseek-coder-v2-lite-16b.Q4_0.gguf --n-gpu-layers 32 --n-ctx 4096
	```
	- `--n-gpu-layers` 视显存大小调整（12GB 显存建议 32-40）
	- `--n-ctx` 上下文长度，4096 或更高
3. 启动 Qwen2.5-Coder 同理，修改模型路径即可。
4. Aider 连接本地 API：
	```
	aider --llm http://localhost:8000/v1
	```
5. 或在 `.aider.conf` 文件中设置：
	```json
	{
	  "llm": "http://localhost:8000/v1"
	}
	```

---


## 9️⃣ 调优建议

- 优先使用 Q4 量化模型，显存压力小
- 不要同时运行多个大模型
- 保持虚拟内存开启，防止爆内存
- NVIDIA 用户优先用 llama-cpp-python，速度更快
- 模型/数据建议全部放 D 盘，避免 C 盘爆满

---


## 🔟 FAQ & 常见问题

**Q：780M 能跑 16B 吗？**  
可以，Q4 稳定，Q5 需更大显存。

**Q：NVIDIA 独显能用 Ollama 吗？**  
可以，但建议用 llama-cpp-python，速度更快。

**Q：模型下载慢？**  
可用 huggingface 镜像、aria2 等工具加速。

**Q：Aider 如何升级？**  
`pip install --upgrade aider-chat[all]`

**Q：llama-cpp-python CUDA 不生效？**  
检查 CUDA/cuDNN 安装和环境变量。

**Q：本地 API 端口冲突？**  
可用 `--port` 参数自定义端口。

---

## ✅ 推荐配置

- 模型：DeepSeek 16B Q4 / Qwen2.5 14B Q4
- 后端：Ollama（新手/集显）或 llama-cpp-python（NVIDIA）
- Aider：--no-stream

---

如有问题欢迎随时反馈！
