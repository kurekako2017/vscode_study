# Aider 本地 AI 编程助手使用手册 (UM890 Pro 专用版)

## 目录
1. [简介](#简介)
2. [系统要求](#系统要求)
3. [安装配置](#安装配置)
4. [基础使用](#基础使用)
5. [高级功能](#高级功能)
6. [最佳实践](#最佳实践)
7. [故障排查](#故障排查)
8. [性能优化](#性能优化)

---

## 简介

Aider 是一个基于 AI 的命令行编程助手,可以帮助您直接在终端中编辑代码文件。本手册专为在 UM890 Pro 上使用本地 AI 模型(如 Ollama)的用户编写。

### 主要特性
- 直接修改现有代码文件
- 支持多文件编辑
- Git 集成,自动提交更改
- 支持本地和云端 AI 模型
- 智能代码补全和重构

---

## 系统要求

### 硬件要求 (UM890 Pro)
- **CPU**: AMD Ryzen 9 8945HS (已满足)
- **内存**: 建议 32GB 以上(运行较大模型)
- **存储**: 至少 20GB 可用空间(用于模型存储)
- **GPU**: 集成显卡可用,独立显卡更佳

### 软件要求
- **操作系统**: Linux, macOS, 或 Windows
- **Python**: 3.8 或更高版本
- **Git**: 用于版本控制
- **Ollama**: 用于运行本地 LLM 模型

---

## 安装配置

### 1. 安装 Python 依赖

```bash
# 使用 pip 安装
pip install aider-chat

# 或使用 pipx (推荐,隔离环境)
pipx install aider-chat
```

### 2. 安装 Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# 从 https://ollama.com/download 下载安装程序
```

### 3. 下载推荐模型

UM890 Pro 推荐使用以下模型:

```bash
# 轻量级模型 (8GB 内存)
ollama pull codellama:7b

# 中等模型 (16GB 内存)
ollama pull deepseek-coder:6.7b

# 高性能模型 (32GB+ 内存)
ollama pull qwen2.5-coder:14b
```

### 4. 配置环境变量

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export OLLAMA_HOST=http://localhost:11434
```

---

## 基础使用

### 启动 Aider

```bash
# 使用默认模型
aider

# 指定 Ollama 模型
aider --model ollama/deepseek-coder:6.7b

# 添加文件到聊天
aider main.py utils.py

# 只读模式添加文件
aider --read README.md --file main.py
```

### 基本命令

在 Aider 会话中:

```
/add <file>        # 添加文件到编辑
/drop <file>       # 从编辑中移除文件
/ls                # 列出所有文件
/undo              # 撤销最后一次更改
/commit            # 提交更改到 git
/diff              # 查看未提交的更改
/help              # 显示帮助
/exit              # 退出 Aider
```

### 示例工作流

```bash
# 1. 启动 Aider 并添加文件
$ aider main.py

# 2. 请求修改代码
> 添加一个函数来计算列表的平均值

# 3. Aider 会自动修改文件并显示 diff

# 4. 确认更改
> /commit

# 5. 继续工作或退出
> /exit
```

---

## 高级功能

### 1. 多模型配置

创建配置文件 `~/.aider.conf.yml`:

```yaml
model: ollama/deepseek-coder:6.7b
edit-format: diff
auto-commits: true
dark-mode: true
```

### 2. 自定义提示词

```bash
# 使用自定义系统提示
aider --message "你是一个 Python 专家,专注于编写高性能代码"
```

### 3. 架构师模式

```bash
# 用于规划和设计(不直接修改代码)
aider --architect
```

### 4. 与 Git 集成

```bash
# 自动提交每次更改
aider --auto-commits

# 自定义提交消息前缀
aider --commit-prompt "feat: "
```

### 5. 使用 API 模式

如果您想使用云端模型作为备份:

```bash
# 使用 OpenAI
export OPENAI_API_KEY=your-key
aider --model gpt-4

# 使用 Anthropic Claude
export ANTHROPIC_API_KEY=your-key
aider --model claude-sonnet-4-5-20250929
```

---

## 最佳实践

### 1. 模型选择策略

| 任务类型 | 推荐模型 | 内存需求 |
|---------|---------|---------|
| 简单修改 | codellama:7b | 8GB |
| 中等复杂度 | deepseek-coder:6.7b | 16GB |
| 复杂重构 | qwen2.5-coder:14b | 32GB |

### 2. 提示词技巧

**好的提示**:
```
在 main.py 中添加错误处理,捕获 ValueError 和 TypeError,
并记录错误信息到日志文件
```

**不好的提示**:
```
修复代码
```

### 3. 文件管理

```bash
# 添加相关文件以提供上下文
aider --read requirements.txt --read README.md main.py

# 对于大型项目,只添加需要修改的文件
aider src/module.py
```

### 4. 增量开发

1. 从小改动开始
2. 每次只修改一个功能
3. 频繁提交
4. 使用 `/undo` 回退错误更改

---

## 故障排查

### 常见问题

**1. Ollama 连接失败**
```bash
# 检查 Ollama 是否运行
ollama list

# 启动 Ollama 服务
ollama serve
```

**2. 模型响应慢**
```bash
# 切换到更小的模型
aider --model ollama/codellama:7b

# 或调整温度参数
aider --model-temperature 0.2
```

**3. 内存不足**
```bash
# 监控内存使用
htop

# 使用更小的模型或增加交换空间
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**4. Git 冲突**
```bash
# Aider 会自动处理大多数 Git 操作
# 如果出现问题,可以手动解决
git status
git add .
git commit -m "manual fix"
```

---

## 性能优化

### 1. UM890 Pro 特定优化

```bash
# 启用 CPU 性能模式
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# 为 Ollama 分配更多资源
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

### 2. 模型量化

使用量化模型以减少内存占用:

```bash
# 下载 Q4 量化版本(更快,内存更少)
ollama pull deepseek-coder:6.7b-q4_0
```

### 3. 缓存优化

```bash
# 保持模型在内存中
ollama run deepseek-coder:6.7b ""  # 预加载模型
```

### 4. 监控性能

```bash
# 实时监控
watch -n 1 'ollama ps'

# 检查模型性能
ollama show deepseek-coder:6.7b
```

---

## 快速参考

### 常用命令速查

```bash
# 启动
aider --model ollama/deepseek-coder:6.7b main.py

# 会话中
/add file.py           # 添加文件
/drop file.py          # 移除文件
/undo                  # 撤销
/commit               # 提交
/diff                 # 查看差异
/tokens               # 查看 token 使用量
/exit                 # 退出
```

### 推荐工作流

1. **初始化项目**: `git init && aider`
2. **描述需求**: 用自然语言描述要实现的功能
3. **审查更改**: 检查 Aider 的修改
4. **测试代码**: 运行测试确保正确性
5. **提交更改**: `/commit` 或 `git commit`
6. **迭代改进**: 继续下一个功能

---

## 资源链接

- **Aider 官方文档**: https://aider.chat/docs/
- **Ollama 模型库**: https://ollama.com/library
- **GitHub 仓库**: https://github.com/paul-gauthier/aider
- **社区论坛**: https://discord.gg/Tv2uQnR5

---

## 许可证与支持

本手册基于 Aider 官方文档编写,专为 UM890 Pro 用户优化。如有问题,请访问官方 GitHub 仓库提交 issue。

**最后更新**: 2025年1月