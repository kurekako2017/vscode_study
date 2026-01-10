# UM890 Pro 本地 Aider + 大模型安装指南

## 一、系统环境准备

### 1. 硬件配置确认
- **CPU**: UM890 Pro（AMD Ryzen 9 8945HS）
- **内存**: 32GB（足够运行Q4/Q5量化模型）
- **显卡**: 集成AMD Radeon 780M（2GB显存）
- **硬盘**: 建议至少预留50GB空间

### 2. 磁盘分区建议
```
推荐安装方案：
- C盘：Python环境 + Aider（约5GB）
- D盘：大模型文件（约30-40GB）
```

**原因**：
- 系统盘保持轻量，便于维护
- 模型文件体积大，放D盘便于管理和迁移
- Python环境装C盘可避免权限问题

---

## 二、基础环境安装

### 1. 安装 Python 3.10/3.11

**下载地址**: https://www.python.org/downloads/

```powershell
# 安装时务必勾选：
☑ Add Python to PATH
☑ Install for all users

# 验证安装
python --version
pip --version
```

### 2. 安装 Git
**下载地址**: https://git-scm.com/download/win

```powershell
# 验证安装
git --version
```

### 3. 安装 Ollama（本地模型运行环境）

**下载地址**: https://ollama.com/download

```powershell
# 默认安装到C盘即可
# 但需要修改模型存储位置到D盘

# 创建D盘模型目录
mkdir D:\ollama-models

# 设置环境变量（重要！）
# Win+R 输入 sysdm.cpl → 高级 → 环境变量 → 系统变量 → 新建
变量名: OLLAMA_MODELS
变量值: D:\ollama-models
```

**验证安装**：
```powershell
ollama --version
```

---

## 三、下载并配置大模型

### 1. DeepSeek-Coder V2 Lite 16B

```powershell
# Q4量化版本（约9GB，推荐）
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M

# Q5量化版本（约11GB，更高精度）
ollama pull deepseek-coder-v2:16b-lite-instruct-q5_K_M
```

### 2. Qwen2.5-Coder 14B

```powershell
# Q4量化版本（约8GB，推荐）
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# Q5量化版本（约10GB）
ollama pull qwen2.5-coder:14b-instruct-q5_K_M
```

**下载时间**: 根据网速，每个模型约10-30分钟

**验证模型**：
```powershell
ollama list
```

---

## 四、安装 Aider

### 1. 创建虚拟环境（推荐）

```powershell
# 在C盘创建项目目录
mkdir C:\aider-workspace
cd C:\aider-workspace

# 创建虚拟环境
python -m venv aider-env

# 激活虚拟环境
.\aider-env\Scripts\activate
```

### 2. 安装 Aider

```powershell
# 安装最新版本
pip install aider-chat

# 验证安装
aider --version
```

---

## 五、显卡设置（关键步骤）

### AMD Radeon 780M 集成显卡配置

由于UM890 Pro使用集成显卡，需要特别配置：

#### 1. 设置显存分配
```
BIOS设置（开机按Del/F2进入）：
- 找到 UMA Frame Buffer Size
- 建议设置为 4GB 或 Auto
```

#### 2. 配置 Ollama 使用GPU

```powershell
# 检查AMD GPU支持
ollama run deepseek-coder-v2:16b-lite-instruct-q4_K_M "test"

# 如果无法使用GPU，设置环境变量强制CPU模式
# 环境变量添加：
变量名: OLLAMA_NUM_GPU
变量值: 0  # 0表示使用CPU，1表示尝试使用GPU
```

**注意**: 集成显卡性能有限，推荐使用CPU运行，体验更稳定。

#### 3. Windows 图形设置优化

```
设置 → 系统 → 显示 → 图形设置
将 ollama.exe 添加到列表，选择"高性能"
```

---

## 六、配置 Aider 使用本地模型

### 1. 创建配置文件

在用户目录创建 `.aider.conf.yml`：

```powershell
# 位置: C:\Users\你的用户名\.aider.conf.yml
notepad C:\Users\%USERNAME%\.aider.conf.yml
```

### 2. 配置文件内容

```yaml
# Aider 配置文件
model: ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M
# 或使用 qwen2.5-coder:14b-instruct-q4_K_M

# Ollama 服务地址
ollama-api-base: http://localhost:11434

# 其他推荐设置
edit-format: whole
auto-commits: false
pretty: true
stream: true
```

### 3. 启动 Aider

```powershell
# 激活虚拟环境
cd C:\aider-workspace
.\aider-env\Scripts\activate

# 启动Aider（指定模型）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 或使用Qwen模型
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M
```

---

## 七、性能优化建议

### 1. 内存设置

```powershell
# 限制Ollama内存使用（防止卡顿）
# 环境变量设置：
变量名: OLLAMA_MAX_LOADED_MODELS
变量值: 1  # 同时只加载1个模型
```

### 2. 推荐使用Q4版本

- **Q4优势**: 速度快，内存占用小（9GB左右）
- **Q5优势**: 精度略高，但速度慢20-30%
- **32GB内存建议**: 优先Q4，流畅度更好

### 3. 性能参考

```
UM890 Pro + Q4模型：
- 生成速度：约8-12 tokens/秒
- 首次加载：15-30秒
- 内存占用：12-15GB
```

---

## 八、常见问题排查

### 1. Ollama服务未启动

```powershell
# 检查服务
ollama serve

# 另开终端测试
ollama list
```

### 2. 模型下载失败

```powershell
# 使用国内镜像（如需要）
# 或手动下载模型文件到 D:\ollama-models
```

### 3. Aider连接失败

```powershell
# 验证Ollama API
curl http://localhost:11434/api/tags
```

### 4. 内存不足

```powershell
# 关闭其他应用
# 只运行一个模型
# 考虑使用更小的量化版本
```

---

## 九、日常使用流程

```powershell
# 1. 启动Ollama（首次开机）
ollama serve

# 2. 打开新终端，激活环境
cd C:\aider-workspace
.\aider-env\Scripts\activate

# 3. 启动Aider
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 4. 开始编码
# Aider会自动管理代码文件，支持对话式编程
```

---

## 十、注意事项总结

✅ **推荐配置**：
- Python装C盘，模型存D盘
- 优先使用Q4量化版本
- 显存分配设置为4GB
- 同时只加载1个模型

⚠️ **重要提示**：
- 首次运行会较慢（模型加载）
- 保持良好散热（CPU高负载）
- 定期清理临时文件
- 建议关闭不必要的后台程序

🎯 **性能预期**：
- 代码生成：中等速度
- 适合日常开发辅助
- 不适合大规模并发任务

---

## 附录：快速命令参考

### 环境变量配置汇总
```
OLLAMA_MODELS = D:\ollama-models
OLLAMA_MAX_LOADED_MODELS = 1
OLLAMA_NUM_GPU = 0
```

### 常用命令
```powershell
# Ollama相关
ollama list                    # 查看已下载模型
ollama rm <model-name>         # 删除模型
ollama serve                   # 启动Ollama服务

# Aider相关
aider --help                   # 查看帮助
aider --model ollama/<model>   # 指定模型启动
aider --list-models            # 列出可用模型

# Python环境
.\aider-env\Scripts\activate   # 激活虚拟环境
deactivate                     # 退出虚拟环境
```

---

**文档版本**: v1.0  
**更新日期**: 2026-01-08  
**适用系统**: Windows 11 Pro

如有问题，欢迎反馈！