# Roo Code Agent 启动与配置实战指南

## 1. 启动 Roo Code 的 Agent（推荐批处理脚本）

推荐用批处理脚本（如 runRooCode_service.bat）实现自动启动和环境变量设置，便于快速切换和复用。

### 启动脚本示例

```bat
@echo off
setlocal enabledelayedexpansion
title Roo Code + Ollama Turbo Loader

REM --- 核心性能优化参数 ---
REM 强制模型在显存中保持活跃，避免每次请求都重新加载 (单位: 秒，-1 为永久)
set OLLAMA_KEEP_ALIVE=-1
REM 允许模型占用的最大显存比例 (0.9 代表 90%)
set OLLAMA_MAX_VRAM=0.9
REM 强制只启动一个模型实例，防止多个 Agent 同时调用导致崩溃
set OLLAMA_MAX_LOADED_MODELS=1
REM 确保系统优先使用 NVIDIA GPU (如果你是双显卡笔记本)
set CUDA_VISIBLE_DEVICES=0

echo ======================================================
echo           ROO CODE 专用本地模型加速启动器
echo ======================================================

:CHECK_SERVICE
echo [1/3] 正在检测 Ollama 服务...
curl -s http://127.0.0.1:11434/api/tags >nul 2>nul
if errorlevel 1 (
    echo [错误] 核心服务未启动！正在尝试后台拉起...
    start /min "" ollama serve
    timeout /t 5
    goto CHECK_SERVICE
)
echo [就绪] Ollama API 已在线。

:PRELOAD
echo [2/3] 正在预取模型到显存: qwen2.5-coder:7b...
REM 通过发送一个空请求强制显卡加载模型权重
curl -s -X POST http://localhost:11434/api/generate -d "{\"model\": \"qwen2.5-coder:7b\"}" >nul
echo [就绪] 模型已成功锁定在 GPU 显存中。

:VRAM_MONITOR
echo [3/3] 正在监控显存状态...
nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits 2>nul
if errorlevel 1 (
    echo [提示] 未检测到 NVIDIA 显卡或驱动，将使用系统内存运行。
) else (
    echo [状态] GPU 加速已激活。
)

echo ------------------------------------------------------
echo 现在你可以打开 VS Code 使用 Roo Code 插件了！
echo 提示: 请确保 Roo Code 设置中的 Context Window 为 8192。
echo ------------------------------------------------------
echo 保持此窗口开启以维持模型热度...
pause >nul
```

> 建议：提前启动 Ollama 服务。
> 启动 Roo Code Agent 前，建议先在 VS Code 或 Roo Code 插件中检查 Ollama 服务状态。
> Ollama 可用 `ollama serve` 启动，`ollama list` 查看模型。

---


## 2. Roo Code 插件详细配置

安装完 Roo Code 后，点击插件左侧的插件图标(Settings)进行如下设置：

| 配置项              | 设定值                        | 备注                                                         |
|---------------------|------------------------------|--------------------------------------------------------------|
| API Provider        | Ollama                       | 推荐选择本地高效的本体推理。                                 |
| Base URL            | http://localhost:11434       | 与本地 Ollama 服务端一致。                                   |
| Model ID            | qwen2.5-coder:7b             | 保持和模型下载/服务端一致。                                  |
| Context Window      | 8192                         | 支持长上下文，推荐8192及以上。                               |
| Use Compact Prompt  | 开启(On)                     | 光标变成紧凑模式，提升推理效率和多Agent协同能力。            |

---

## 3. 如何实现“快速切换多种”Agent模式

Roo Code 的核心优势之一在于它能像一个插件集群一样协同的项目。为了让代码执行权仅交叉权，建议以下方式操作：

1. 切换到 Architect Mode（架构模式）：
    - 在 Roo Code 侧栏上选择 Architect。
    - 用法：在这个模式下，只保留分析生成的方案，不直接写文件。这样让决策代码更聚集，分析式决策更高效。

2. 一键切入 Act Mode（执行模式）：
    - 进入方案后，点击“Apply”或切换为 Act 模式。
    - 用法：此模式自动调用模型的 GPU 资源，快速完成代码修改、创意类复杂任务。

3. 直指 Q4 量化模型：
    - 如需切换模型，推荐将插件 Model ID 设为你本地服务端模型的具体名称，例如 qwen2.5-coder:7b-instruct-q4_K_M，确保推理速度和兼容性最佳。

---

## 4. 总结性操作

1. 第一步：双击启动你的 start_ollama_service.bat。
2. 第二步：打开 VS Code 并启动 Roo Code 插件。
3. 第三步：推荐分析和推理模式切换，并准备一组简单 Java Lambda 例列。

---

> 本文档适用于 Windows 11/10，适配 Roo Code 插件。
> 更新日期：2026-01-13
