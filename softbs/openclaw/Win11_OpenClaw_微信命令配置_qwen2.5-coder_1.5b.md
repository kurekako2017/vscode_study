# Win11 配置 OpenClaw（微信发命令）+ qwen2.5-coder:1.5b 教程

> 目标：在 Win11 上安装并配置 OpenClaw，使用微信发送命令驱动本机执行，并把模型设置为 `qwen2.5-coder:1.5b`。

---

## 0. 准备清单

- Windows 11（已联网）
- 已安装 **Ollama**（用于本地模型）
- 可用的微信（个人号或企业微信均可）
- 一个空闲目录用于 OpenClaw 工作目录（建议：`D:\tools\openclaw`）

---

## 1. 安装 Ollama 并拉取模型

1. 安装 Ollama（已安装可跳过）：
   - 访问 Ollama 官网下载安装包并安装完成。
2. 打开 PowerShell，拉取模型：

```powershell
ollama pull qwen2.5-coder:1.5b
```

3. 验证模型可用：

```powershell
ollama run qwen2.5-coder:1.5b
```

输入一段简单提示，例如：

```
写一个 Python 的 hello world
```

如果正常输出说明模型可用。

---

## 2. 安装 OpenClaw

> 如果你已经有 OpenClaw，请从第 3 节开始。

1. 选择一个目录，例如：

```
D:\tools\openclaw
```

2. 打开 PowerShell，进入目录并安装（示例方式，实际以你的 OpenClaw 安装说明为准）：

```powershell
cd D:\tools
# 示例：git clone 方式
# git clone <OpenClaw 仓库地址> openclaw
```

3. 进入 OpenClaw 目录。

---

## 3. 配置 OpenClaw 通道（WeChat）

1. 打开 PowerShell，在 OpenClaw 目录执行：

```powershell
openclaw configure
```

2. 进入 **Channels** 菜单。
3. 选择 **wechat** 或 **wecom** 通道（按方向键选择并回车）。
4. 根据提示填写：
   - **企业微信**：通常需要企业 ID、Secret、应用 AgentId 等。
   - **个人微信**：通常需要扫码绑定。

> 说明：如果你是个人微信，按照命令提示扫码即可。

---

## 4. 开启“自动执行”技能（核心步骤）

> 只有开启 Skills 才能让微信命令执行本地任务。

1. 在 `openclaw configure` 界面进入 **Skills**。
2. 勾选以下能力：
   - **filesystem**：允许读写文件
   - **shell**：允许执行命令
3. 保存并退出。

---

## 5. 配置模型为 qwen2.5-coder:1.5b

在 OpenClaw 的配置文件中把默认模型设置为：

```
qwen2.5-coder:1.5b
```

具体位置以你当前 OpenClaw 的配置为准（常见位置：`config.yaml` / `settings.json` / `profiles/*.yaml`）。

示例（YAML）：

```yaml
model: qwen2.5-coder:1.5b
provider: ollama
```

> 如果 OpenClaw 支持多配置/多 Profile，请确保当前激活的 Profile 指向该模型。

---

## 6. 启动 OpenClaw

在 PowerShell 中运行（按你的安装方式）：

```powershell
openclaw start
```

如果没有 `openclaw start` 命令，就按你的 OpenClaw 文档启动服务（例如 `openclaw run` 或 `python -m openclaw`）。

---

## 7. 微信发命令测试

### 7.1 测试 Shell

在微信中发：

```
/run echo hello openclaw
```

预期：返回 `hello openclaw`。

### 7.2 测试文件写入

```
/write D:/temp/openclaw_test.txt
内容：openclaw OK
```

### 7.3 测试编码能力

```
写一个 Python 函数：输入数组，返回去重后的数组
```

如果回复正常，说明模型配置成功。

---

## 8. 常见问题

### 8.1 模型无法调用

- 确认 Ollama 运行中（后台进程正常）
- 运行 `ollama list` 确认模型存在
- 检查 OpenClaw 的 provider 是否指向 Ollama

### 8.2 微信上无响应

- 检查 OpenClaw 是否已启动
- 确认通道配置（WeChat/WeCom）无误
- 确认 Skills 中 `shell` 和 `filesystem` 已开启

### 8.3 提示权限不足

- 确认 OpenClaw 服务是否以管理员权限运行
- 目标目录是否允许写入

---

## 9. 推荐微信命令模板

```
/run <命令>
/write <文件路径>
/read <文件路径>
```

示例：

```
/run dir D:\
```

---

## 10. 完成

至此已完成 Win11 + OpenClaw + WeChat 命令控制 + `qwen2.5-coder:1.5b` 配置。

如果需要，我可以继续补充：
- OpenClaw 的多 Profile 配置
- 更安全的权限与白名单策略
- 使用企业微信机器人的完整配置示例
