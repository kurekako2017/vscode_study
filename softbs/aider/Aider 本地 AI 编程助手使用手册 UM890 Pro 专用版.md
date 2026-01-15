Aider 本地安装使用指南

UM890 Pro (Windows 11 Pro + 32GB 内存) 专用版

概述
=====
本指南面向 UM890 Pro（Ryzen 9 8945HS、32GB 内存）用户，介绍如何在本机使用 Ollama + Aider 进行本地代码生成、重构与审查。包含环境准备、模型下载、Aider 安装与配置、使用示例、性能优化与故障排查。

目录
----
1. 系统与硬件建议
2. 安装前准备
3. 安装与验证 Ollama
4. 下载与测试模型
5. 安装与配置 Aider
6. 实战示例
7. 性能优化与建议
8. 常用命令速查
9. 故障排查

1. 系统与硬件建议
-----------------
推荐机器规格（UM890 Pro 已满足）：

```
主机: UM890 Pro（Ryzen 9 8945HS）
内存: 32 GB
系统: Windows 11 Pro
```

内存对模型加载影响最大。32GB 建议使用 Q4 量化版本（Q4_K_M），以便在加载 14B/16B 模型时保持系统响应。


```powershell

Aider 本地 AI 编程助手使用手册
================================
UM890 Pro · Windows 11 Pro · 32GB 内存 · 本地模型专用版

写在前面
--------
本手册面向 UM890 Pro（Ryzen 9 8945HS，32GB 内存）用户，帮助在本机利用 Ollama + Aider 进行本地代码生成、重构与审查。全部流程基于本地模型，强调可复制的 PowerShell 命令与实战范式。

目录
----
1. 环境概览与模型选择
2. 安装前检查
3. 安装与验证 Ollama
4. 拉取与测试模型（本地推理）
5. 安装与配置 Aider
6. 典型使用场景（实战流程）
7. 性能优化（32GB 场景）
8. 常用命令速查
9. 故障排查
10. 快速脚本与建议

1. 环境概览与模型选择
----------------------
- 硬件：UM890 Pro（Ryzen 9 8945HS，32GB 内存）
- 系统：Windows 11 Pro
- 推荐模型（本地部署优先 Q4 量化，兼顾性能与内存）：
  - Qwen2.5-Coder 14B Q4_K_M（约 9GB，日常开发、快速迭代）
  - DeepSeek-Coder V2 Lite 16B Q4_K_M（约 10GB，复杂重构、架构设计）

2. 安装前检查
--------------
```powershell
python --version      # 需 3.10+
| DeepSeek-Coder V2 Lite 16B | Q4_K_M | ~10GB | 中等 | 复杂代码生成、重构 |
git --version
# 如需运行脚本（管理员执行一次）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. 安装与验证 Ollama
--------------------
```powershell
# 下载并安装（或从官网下载安装包）
Invoke-WebRequest -Uri https://ollama.com/download/OllamaSetup.exe -OutFile OllamaSetup.exe
.\n+OllamaSetup.exe

# 验证安装
ollama --version
ollama list

# 服务检查（Windows 下为后台服务）
ollama ps
```

4. 拉取与测试模型（本地推理）
----------------------------
优先 Q4 量化，兼顾性能与内存占用：

```powershell
# Qwen2.5-Coder 14B Q4（快，约 9GB）
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# DeepSeek-Coder V2 Lite 16B Q4（强，约 10GB）
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M

ollama list
```

快速测试：
```powershell
ollama run qwen2.5-coder:14b-instruct-q4_K_M "解释什么是闭包"
ollama run deepseek-coder-v2:16b-lite-instruct-q4_K_M "写一个 Python 快速排序函数"
```

5. 安装与配置 Aider
------------------
推荐 pipx 隔离安装：

```powershell
pip install --user pipx
python -m pipx ensurepath
# 重新打开 PowerShell 后
pipx install aider-chat

# 验证
| DeepSeek-Coder V2 Lite 16B | Q5_K_M | ~12GB | 较慢 | 高质量代码生成 |
```

若需使用 pip：
```powershell
pip install aider-chat
```

创建配置（用户级）：
```powershell
$config = @"
model: ollama/qwen2.5-coder:14b-instruct-q4_K_M
edit-format: diff
auto-commits: false
dark-mode: true
pretty: true
stream: true
"@

$config | Out-File -FilePath "$env:USERPROFILE\.aider.conf.yml" -Encoding UTF8
```

6. 典型使用场景（实战流程）
-------------------------
场景 A：新项目快速起步（FastAPI 示例）
```powershell
mkdir my_project
cd my_project
git init
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M
# 在会话中提出需求，查看 /ls /diff，满意后 /commit，/exit
```

场景 B：复杂重构（用 DeepSeek）
```powershell
cd existing_project
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M main.py utils.py
# 描述重构目标，/diff 审查，/commit 确认
```

场景 C：代码审查与性能优化
```powershell
| Qwen2.5-Coder 14B | Q4_K_M | ~9GB | 快速 | 日常编码、快速迭代 |
# 请求性能审查或安全审查，/diff 查看，/commit 应用
```

场景 D：模型快速切换
```powershell
/model ollama/qwen2.5-coder:14b-instruct-q4_K_M
/model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M
```
7. 性能优化（32GB 场景）
----------------------
- 模型策略：优先 Q4 量化；只有需要更高质量时再切 Q5。
- Ollama 环境变量（降低并发、限制同时加载模型数）：

```powershell
[System.Environment]::SetEnvironmentVariable('OLLAMA_NUM_PARALLEL','2','User')
[System.Environment]::SetEnvironmentVariable('OLLAMA_MAX_LOADED_MODELS','2','User')
[System.Environment]::SetEnvironmentVariable('OLLAMA_FLASH_ATTENTION','1','User')
```

- Aider 启动参数（稳健、流式、少提交）：
- Windows 设置：启用高性能电源计划，适当设置虚拟内存。

8. 常用命令速查
--------------
# Ollama
ollama list
ollama run qwen2.5-coder:14b-instruct-q4_K_M
ollama ps

# Aider 启动
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 会话内常用
```

9. 故障排查
----------
- 无法连接 Ollama：检查进程或重启。
- 模型加载失败/内存不足：先用 Q4 量化，或卸载不必要模型。
- 找不到模型：模型名需带 `ollama/` 前缀和标签。

诊断命令：
```powershell
Get-Process ollama -ErrorAction SilentlyContinue
ollama list
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
```
10. 快速脚本与建议
------------------
`start-aider-qwen.ps1`
```powershell
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M --stream --pretty
```

`start-aider-deepseek.ps1`
```powershell

```

结语
----
本手册聚焦 UM890 Pro 的本地模型场景，提供可直接复制的命令与实践流程。如需增补截图、制作速查卡或添加 Mac/Linux 变体，请告知。
**32GB 内存推荐**: 使用 Q4_K_M 版本以获得最佳性能，或在需要高质量时使用 Q5_K_M。


## 安装前准备

### 1. 安装 Python

访问 [Python 官网](https://www.python.org/downloads/) 下载 Python 3.10 或更高版本

```powershell
# 验证 Python 安装
python --version
# 应该显示: Python 3.10.x 或更高

# 验证 pip
pip --version
```

### 2. 安装 Git

访问 [Git 官网](https://git-scm.com/download/win) 下载并安装

```powershell
# 验证 Git 安装
git --version
```

### 3. 配置 PowerShell 执行策略（如需要）

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

---

## 安装 Ollama

### 1. 下载并安装 Ollama

访问 [Ollama 官网](https://ollama.com/download/windows) 下载 Windows 安装程序

或使用命令行下载：
```powershell
# 下载 Ollama 安装程序
Invoke-WebRequest -Uri https://ollama.com/download/OllamaSetup.exe -OutFile OllamaSetup.exe

# 运行安装程序
.\OllamaSetup.exe
```

### 2. 验证 Ollama 安装

```powershell
# 打开新的 PowerShell 窗口
ollama --version

# 应该显示版本号，如: ollama version is 0.x.x
```

### 3. 启动 Ollama 服务

# Ollama 会在系统托盘中显示图标
# 确保服务正在运行
ollama list
```


## 下载和配置模型


```powershell
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M

# Q5 量化版本（质量更高，内存占用约 12GB）
ollama pull deepseek-coder-v2:16b-lite-instruct-q5_K_M

# 查看已下载的模型
ollama list
```

### 2. 下载 Qwen2.5-Coder 14B

```powershell
# Q4 量化版本（推荐，速度最快，内存占用约 9GB）
ollama pull qwen2.5-coder:14b-instruct-q4_K_M
# 查看所有模型
ollama list
```

### 3. 测试模型

```powershell
# 测试 DeepSeek-Coder（Q4 版本）
ollama run deepseek-coder-v2:16b-lite-instruct-q4_K_M "写一个 Python 快速排序函数"
# 测试 Qwen2.5-Coder（Q4 版本）
ollama run qwen2.5-coder:14b-instruct-q4_K_M "解释什么是闭包"

# 退出测试
/bye
```

---

## 安装 Aider


```powershell
# 安装 aider-chat
pip install aider-chat

# 验证安装
aider --version
```

### 2. 使用 pipx 安装（推荐，隔离环境）

```powershell
# 先安装 pipx
pip install pipx
pipx ensurepath

# 重启 PowerShell 后安装 aider
pipx install aider-chat

# 验证安装
aider --version
```

### 3. 配置 Aider

创建配置文件 `%USERPROFILE%\.aider.conf.yml`：

```yaml
# Aider 配置文件
model: ollama/qwen2.5-coder:14b-instruct-q4_K_M
edit-format: diff
auto-commits: false
dark-mode: true
pretty: true
stream: true
```

在 PowerShell 中创建：
```powershell
# 创建配置文件
$configContent = @"
model: ollama/qwen2.5-coder:14b-instruct-q4_K_M
edit-format: diff
auto-commits: false
dark-mode: true
pretty: true
stream: true
"@

$configContent | Out-File -FilePath "$env:USERPROFILE\.aider.conf.yml" -Encoding UTF8
```

---

## 实战使用教程

### 场景 1: 创建新 Python 项目

```powershell
# 1. 创建项目目录
mkdir my_project
cd my_project

# 2. 初始化 Git
git init

# 3. 启动 Aider（使用 Qwen2.5-Coder Q4，速度快）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 4. 在 Aider 中请求创建代码
# > 创建一个 FastAPI 应用，包含用户注册和登录接口，使用 SQLite 数据库

# 5. Aider 会自动生成文件，查看生成的文件
# > /ls

# 6. 提交更改
# > /commit

# 7. 退出
# > /exit
```

### 场景 2: 修改现有代码

```powershell
# 1. 进入项目目录
cd existing_project

# 2. 使用 DeepSeek-Coder V2（Q4 版本，适合复杂重构）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M main.py utils.py

# 3. 在 Aider 中请求修改
# > 重构 main.py 中的数据库连接代码，使用连接池，添加错误重试机制

# 4. 查看更改
# > /diff

# 5. 如果满意，提交
# > /commit

# 6. 继续其他修改或退出
# > /exit
```

### 场景 3: 代码审查和优化

```powershell
# 启动 Aider 并添加只读文件以提供上下文
aider --read README.md --read requirements.txt --file src/main.py

# 在 Aider 中请求优化
# > 分析 main.py 的性能瓶颈，优化数据库查询，添加缓存机制

# 查看建议的更改
# > /diff

# 应用更改
# > /commit
```

### 场景 4: 快速切换模型

```powershell
# 方法 1: 命令行指定模型
# 使用 Qwen2.5（日常快速开发）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 使用 DeepSeek-Coder V2（复杂任务）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 方法 2: 在 Aider 会话中切换模型
# > /model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M
```

### 场景 5: 批量处理多个文件

```powershell
# 添加多个文件
aider src/main.py src/utils.py src/models.py

# 在 Aider 中请求全局修改
# > 在所有文件中添加类型注解，使用 typing 模块

# 查看所有更改
# > /diff

# 提交
# > /commit
```

---

## 性能优化建议

### 1. 模型选择策略（基于 32GB 内存）

```powershell
# 日常开发、快速迭代 -> Qwen2.5-Coder Q4
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 复杂重构、架构设计 -> DeepSeek-Coder V2 Q4
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 需要最高质量输出 -> 任意模型的 Q5 版本
aider --model ollama/qwen2.5-coder:14b-instruct-q5_K_M
```

### 2. Ollama 性能优化

创建或编辑环境变量：

```powershell
# 设置用户环境变量（永久生效）
[System.Environment]::SetEnvironmentVariable('OLLAMA_NUM_PARALLEL', '2', 'User')
[System.Environment]::SetEnvironmentVariable('OLLAMA_MAX_LOADED_MODELS', '2', 'User')
[System.Environment]::SetEnvironmentVariable('OLLAMA_FLASH_ATTENTION', '1', 'User')

# 重启 PowerShell 使环境变量生效
```

或手动设置：
1. 右键"此电脑" → "属性" → "高级系统设置"
2. "环境变量" → "用户变量" → "新建"
3. 添加以下变量：
   - `OLLAMA_NUM_PARALLEL` = `2`
   - `OLLAMA_MAX_LOADED_MODELS` = `2`
   - `OLLAMA_FLASH_ATTENTION` = `1`

### 3. Aider 优化参数

```powershell
# 使用优化参数启动
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M \
      --model-temperature 0.2 \
      --stream \
      --no-auto-commits

# 或在配置文件中设置（推荐）
# 编辑 ~/.aider.conf.yml
```

### 4. Windows 性能优化

```powershell
# 设置 Windows 电源计划为高性能
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# 确保虚拟内存足够（推荐 16-32GB）
# 控制面板 → 系统 → 高级系统设置 → 性能设置 → 高级 → 虚拟内存
```

---

## 常用命令速查

### Aider 启动命令

```powershell
# 基础启动（使用默认配置）
aider

# 指定模型启动（Qwen2.5-Coder Q4）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 指定模型启动（DeepSeek-Coder V2 Q4）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 添加文件启动
aider main.py utils.py

# 添加只读文件（作为上下文）
aider --read README.md --file main.py

# 架构师模式（只规划不修改）
aider --architect

# 自动提交模式
aider --auto-commits

# 禁用流式输出（适合慢速终端）
aider --no-stream
```

### Aider 会话内命令

```
/add <file>              添加文件到编辑列表
/drop <file>             从编辑列表移除文件
/read <file>             添加只读文件（仅作为上下文）
/ls                      列出所有文件
/diff                    显示未提交的更改
/undo                    撤销最后一次更改
/commit [message]        提交更改到 Git
/clear                   清除聊天历史
/tokens                  显示 token 使用情况
/model <model_name>      切换模型
/help                    显示帮助
/exit 或 /quit           退出 Aider
```

### Ollama 常用命令

```powershell
# 列出已安装的模型
ollama list

# 运行模型（交互模式）
ollama run qwen2.5-coder:14b-instruct-q4_K_M

# 删除模型
ollama rm deepseek-coder-v2:16b-lite-instruct-q5_K_M

# 查看模型信息
ollama show qwen2.5-coder:14b-instruct-q4_K_M

# 查看正在运行的模型
ollama ps

# 停止所有模型
ollama stop -a
```

---

## 故障排查

### 问题 1: Ollama 服务未启动

**症状**: `Error: could not connect to ollama`

**解决方法**:
```powershell
# 检查 Ollama 服务状态
Get-Process ollama -ErrorAction SilentlyContinue

# 如果没有运行，从开始菜单启动 Ollama
# 或重新启动计算机
```

### 问题 2: 模型加载失败或内存不足

**症状**: `Error: model failed to load` 或系统变慢

**解决方法**:
```powershell
# 1. 检查可用内存
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory

# 2. 关闭其他应用程序释放内存

# 3. 使用更小的量化版本（Q4 而非 Q5）
ollama pull qwen2.5-coder:14b-instruct-q4_K_M

# 4. 卸载不需要的模型
ollama rm <model_name>
```

### 问题 3: Aider 找不到 Ollama 模型

**症状**: `Model not found`

**解决方法**:
```powershell
# 1. 确认模型已下载
ollama list

# 2. 使用正确的模型名称
# 正确: ollama/qwen2.5-coder:14b-instruct-q4_K_M
# 错误: qwen2.5-coder (缺少 ollama/ 前缀和版本标签)

# 3. 测试模型是否可用
ollama run qwen2.5-coder:14b-instruct-q4_K_M "hello"
```

### 问题 4: Git 相关错误

**症状**: `fatal: not a git repository`

**解决方法**:
```powershell
# 在项目目录中初始化 Git
git init

# 配置 Git 用户信息（如果是首次使用）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 问题 5: 模型响应太慢

**解决方法**:
```powershell
# 1. 切换到 Q4 量化版本
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 2. 降低温度参数（更确定性，更快）
aider --model-temperature 0.1

# 3. 预加载模型到内存
ollama run qwen2.5-coder:14b-instruct-q4_K_M ""

# 4. 检查系统资源
# 打开任务管理器 (Ctrl+Shift+Esc) 查看 CPU/内存使用
```

### 问题 6: PowerShell 中文显示乱码

**解决方法**:
```powershell
# 设置 PowerShell 编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# 或在 PowerShell 配置文件中永久设置
# 编辑: notepad $PROFILE
# 添加: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 实用技巧

### 1. 创建快捷启动脚本

创建 `start-aider-qwen.ps1`:
```powershell
# Qwen2.5-Coder Q4（日常使用）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M --stream --pretty
```

创建 `start-aider-deepseek.ps1`:
```powershell
# DeepSeek-Coder V2 Q4（复杂任务）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M --stream --pretty
```

使用：
```powershell
.\start-aider-qwen.ps1
```

### 2. 批处理脚本（.bat 格式）

创建 `aider-qwen.bat`:
```batch
@echo off
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M --stream --pretty
```

双击运行即可。

### 3. 设置 Windows Terminal 配置

如果使用 Windows Terminal，可以添加专用配置：

```json
{
    "name": "Aider (Qwen)",
    "commandline": "powershell.exe -NoExit -Command \"aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M\"",
    "startingDirectory": "%USERPROFILE%\\Projects"
}
```

---

## 推荐工作流程

### 工作流 1: 新项目开发

```powershell
# 1. 创建项目
mkdir my_new_project
cd my_new_project
git init

# 2. 启动 Aider（使用 Qwen，速度快）
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M

# 3. 描述项目需求
> 创建一个 Flask Web 应用，包含用户认证系统（注册、登录、登出），
  使用 SQLAlchemy ORM，JWT 令牌认证，包含单元测试

# 4. 审查生成的代码
> /ls
> /diff

# 5. 测试运行
> /exit
python main.py

# 6. 如果需要修改
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M main.py
> 添加密码强度验证和邮箱格式检查
```

### 工作流 2: 代码重构

```powershell
# 1. 进入项目
cd existing_project

# 2. 使用 DeepSeek（适合复杂重构）
aider --model ollama/deepseek-coder-v2:16b-lite-instruct-q4_K_M \
      --read README.md \
      --file src/legacy_code.py

# 3. 请求重构
> 重构这个文件：
  1. 将单个大函数拆分成多个小函数
  2. 添加类型注解
  3. 改进错误处理
  4. 添加文档字符串
  5. 遵循 PEP 8 规范

# 4. 审查并提交
> /diff
> /commit
```

### 工作流 3: Bug 修复

```powershell
# 1. 启动 Aider，添加相关文件
aider --model ollama/qwen2.5-coder:14b-instruct-q4_K_M \
      buggy_file.py \
      --read test_file.py

# 2. 描述 Bug
> 修复以下 Bug：当输入为空列表时程序崩溃，
  应该返回默认值而不是抛出异常

# 3. 运行测试验证
> /exit
pytest test_file.py

# 4. 如果测试通过，提交
git add .
git commit -m "fix: handle empty list input"
```

---

## 总结

### 您的最佳配置

**硬件**: UM890 Pro + 32GB 内存 + Win11 Pro  
**推荐模型**: 
- **日常开发**: Qwen2.5-Coder 14B Q4_K_M（快速）
- **复杂任务**: DeepSeek-Coder V2 Lite 16B Q4_K_M（强大）

### 快速开始

```powershell
# 1. 安装 Ollama（官网下载安装）
# 2. 下载模型
ollama pull qwen2.5-coder:14b-instruct-q4_K_M
ollama pull deepseek-coder-v2:16b-lite-instruct-q4_K_M

# 3. 安装 Aider
pip install 