Markdown# Windows 本地安装 Aider + DeepSeek-Coder-V2-Lite-16B + Qwen2.5-Coder-14B（量化版）

**适用设备**：UM890 Pro（Ryzen 9 8945HS + Radeon 780M + 32GB RAM + Win11 Pro）  
**当前日期参考**：2026年1月  
**目标模型**（推荐 Q4_K_M 量化，平衡速度/精度/显存）：
- DeepSeek-Coder-V2-Lite:16b-instruct-q4_K_M
- qwen2.5-coder:14b-instruct-q4_K_M

## 重要注意事项

- **安装路径**：模型文件较大（每个约 9–11GB），**强烈建议**放 D 盘，避免 C 盘空间不足
  - Ollama 数据目录建议：`D:\Ollama`
  - Aider 虚拟环境建议：`D:\aider_env`
- **显卡支持**：Radeon 780M 在 Windows 上 Ollama 的 AMD GPU 加速为实验性功能
  - 先更新最新 AMD Adrenalin 驱动
  - 如出现问题/速度慢，可临时禁用 GPU：`set OLLAMA_NO_GPU=1`
- **内存占用**（加载后估算）：
  - 16B Q4 ≈ 9.5–11GB
  - 14B Q4 ≈ 8.5–10GB
  - 32GB 内存基本够用，建议只同时跑一个模型
- **量化建议**：优先 Q4_K_M（速度快、省内存），Q5_K_M 精度稍高但多占 1–2GB 显存

## 详细安装步骤

### 1. 安装 Python（推荐 3.12.x）

1. 访问 https://www.python.org/downloads/
2. 下载最新 Windows installer (64-bit)
3. 安装时**务必勾选**：Add python.exe to PATH
4. 建议自定义安装到默认路径或 C:\Python312
5. 安装完成 CMD 验证：
python --version
pip --version
text### 2. 安装 Git（Aider 必须依赖）

1. 访问 https://git-scm.com/download/win
2. 下载 64-bit 版本
3. 安装保持默认选项（Use Git from the Windows Command Prompt）
4. CMD 验证：
git --version
text### 3. 安装 Ollama（本地模型运行核心）

1. 访问 https://ollama.com/download 下载 Windows 安装包 OllamaSetup.exe
2. 双击安装（默认装在用户目录，无需管理员权限）
3. **推荐移动到 D 盘**（节省 C 盘空间）：
- 安装完先退出 Ollama（任务栏右键退出）
- 将 `C:\Users\你的用户名\AppData\Local\Ollama` 剪切到 `D:\Ollama`
- 以管理员身份打开 CMD，执行创建符号链接：
mklink /J "%USERPROFILE%\AppData\Local\Ollama" "D:\Ollama"
text4. CMD 验证：
ollama --version
text### 4. 拉取模型（Q4_K_M 量化版）

在 CMD 或 PowerShell 中依次执行（建议管理员权限）：

```bash
# DeepSeek-Coder-V2-Lite 16B Instruct Q4
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M

# Qwen2.5-Coder 14B Instruct Q4
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

如想尝试 Q5_K_M，把 q4_K_M 改为 q5_K_M（若 Ollama 库有该 tag）
查看已下载模型：textollama list
首次下载较慢，耐心等待（每个模型约 9–11GB）

5. 创建 Aider 虚拟环境（强烈推荐隔离）
Bash# 创建虚拟环境到 D 盘
python -m venv D:\aider_env

# 激活（以后每次使用前都要执行）
D:\aider_env\Scripts\activate
激活后提示符变为 (aider_env)
6. 安装 Aider
在激活的环境中执行：
Bashpip install -U pip
pip install -U aider-chat
验证版本：
textaider --version
7. 启动 Aider 并使用本地模型
推荐启动方式（直接指定模型）：
Bash# DeepSeek 版（代码能力强，推荐主用）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# Qwen2.5-Coder 版（中文/中英混合更友好）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M
设置永久默认模型（可选）：
在 C:\Users\你的用户名\.aider.conf.yml 中写入（没有就新建）：
YAMLmodel: ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M
# 或换成 qwen2.5-coder:14b-instruct-q4_K_M
之后直接输入 aider 即可启动。
常用实用参数（可加在命令后）
Bashaider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M \
      --yes                 # 自动同意大部分操作
      --auto-commits        # 自动 git commit（谨慎）
      --4                     # 更简洁的回复风格
常见问题快速处理

Ollama 不启动/卡住 → 重启电脑，或检查杀毒软件拦截
模型加载很慢/卡死 → 第一次正常，后续会缓存加速
GPU 不工作/响应极慢 → 管理员 CMD 执行 set OLLAMA_NO_GPU=1 后再启动
内存/显存不足 → 关闭其他程序，或换更低量化（如 q3_K_M，如果存在）

祝你本地纯净编码愉快！
有问题可随时补充日志排查。