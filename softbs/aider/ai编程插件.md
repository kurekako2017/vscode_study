## VS Code 最佳免费 AI 编程插件推荐（2026）

### 1. 免费云端 AI 编程插件

- **Codeium**
   - 功能：自动补全、代码生成、注释解释，体验接近 Copilot。
   - 优点：完全免费，支持多语言，响应速度快。
   - 安装：VS Code 插件市场搜索“Codeium”。

- **TabNine**（基础免费）
   - 功能：AI 代码补全，支持多语言。
   - 优点：本地和云端混合，免费版有基本补全。
   - 安装：VS Code 插件市场搜索“TabNine”。

### 2. 本地大模型 AI 编程插件

- **Continue**
   - 功能：支持本地 LLM（如 Ollama、LM Studio、OpenAI API），可自定义模型，支持代码补全、对话、代码解释。
   - 优点：隐私安全，支持多种本地模型（如 Llama 2/3、Qwen、Deepseek 等），界面友好。
   - 安装：VS Code 插件市场搜索“Continue”。
   - 配置：配合 Ollama（推荐 Windows/Mac 本地部署）、LM Studio 或自建 API。

- **Aider**（配合 VS Code Terminal 使用）
   - 功能：本地 LLM 代码助手，支持多轮对话、代码修改、自动补全。
   - 优点：支持 Ollama、LM Studio，适合本地私有化开发。
   - 用法：在终端运行 aider，结合 VS Code 编辑器。

### 3. 其他本地模型插件

- **ChatGPT - Genie AI**
   - 功能：支持自定义 API、本地模型，代码补全、对话。
   - 安装：VS Code 插件市场搜索“Genie AI”。

---

#### 推荐组合
- 云端免费体验：**Codeium**
- 本地模型体验：**Continue + Ollama/LM Studio**
- 进阶本地工作流：**Aider + Ollama**（需命令行操作）

#### 参考配置
1. 安装 Continue 插件，配置 Ollama（如 Llama 3、Qwen、Deepseek 等模型）。
2. VS Code 插件市场安装 Codeium 体验云端补全。
3. 需要更强本地控制可用 Aider（详见 softbs/01_Aider + Ollama Windows 标准启动方案.md）。

---
**注意：** 本地大模型需较大内存（16GB+），推荐 GPU 环境体验更佳。
# VS Code 替代方案推荐
## 前言
本文将介绍几款优秀的 VS Code 替代方案，特别适合追求 AI 深度集成的开发者。这些方案不仅能提供更好的智能编程体验，还能为你的开发工作带来更多便利。

## 方案对比

| 方案 | 特点 | 推荐理由 |
|------|------|----------|
| **Cursor (免费版)** | AI 原生编辑器 | 目前公认最强的 AI 编辑器。虽然 Pro 收费，但免费版提供的 Claude 3.5/GPT-4o 额度配合其 "Composer"（多文件同时修改）功能，体验远超 VS Code 插件。 |
| **Windsurf (Codeium)** | 自主 Agent 模式 | Codeium 出品的编辑器。它的 "Flow" 模式可以让 AI 自动在终端跑命令、搜文件、改代码，完全不需要你手动操作，目前免费额度很大。 |
| **Cline (VS Code 插件)** | 全能开源 Agent | 这是一个插件（原名 Claude Dev）。你可以把你的 OpenRouter Key 填进去，它能像一个真实的程序员一样帮你读文档、写代码并运行测试，比 Continue 更具“侵略性”。 |

## 使用建议
1. **初学者**：建议从 Cursor 开始，它的用户界面最为友好
2. **中级开发者**：Windsurf 的自动化功能值得尝试
3. **高级用户**：Cline 提供了最大程度的自定义空间

3. IDEA 中的最佳配置
在 IDEA 这种重型 IDE 里，Continue 的适配可能不如 VS Code 丝滑。

Amazon Q Developer：在 IDEA 里非常好用，它对 AWS 相关和 Java 生态有深度优化，且有很慷慨的免费个人层级。

Fitten Code：国产的一个非常快速的补全插件，支持 IDEA。它的优势是完全免费且在国内访问速度极快。

CodeGeeX：由清华系团队开发，在 IDEA 插件市场里排名很高，支持自动写注释、生成单元测试，对中文注释理解极好。

# 主流 IDE 的 AI 编程插件推荐

## VS Code 插件推荐

### 核心方案对比

| 插件 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| **Cursor** | AI 原生编辑器 | - 行业标杆级 AI 编辑器<br>- 免费版提供 Claude/GPT 额度<br>- 革命性的多文件编辑功能 | 追求极致效率的开发者 |
| **Windsurf** | 自主 Agent | - Codeium 的自动化工作流<br>- 终端/文件系统全自动操作 | 需要自动化辅助的工程 |
| **Cline** | 开源 Agent | - 支持 OpenRouter 多种模型<br>- 类人类开发行为模式 | 需要高度定制化的场景 |

### 使用技巧
1. 组合使用 Cursor + GitHub Copilot 效果更佳
2. 为不同项目创建专属的配置预设
3. 定期清理插件缓存保持性能

---

## IDEA 插件推荐

### 精选插件对比

| 插件 | 核心优势 | 技术栈适配 | 推荐指数 |
|------|----------|------------|----------|
| **Amazon Q** | - AWS 深度集成<br>- Java 生态专项优化 | AWS/Java | ⭐⭐⭐⭐⭐ |
| **Fitten Code** | - 国内零延迟响应<br>- 完全免费无限制 | 全栈开发 | ⭐⭐⭐⭐ |
| **CodeGeeX** | - 中文注释理解最佳<br>- 文档/测试全自动生成 | 中文项目 | ⭐⭐⭐⭐ |

### 配置要点
1. 调整 JVM 参数：`-Xmx4096m -XX:+UseG1GC`
2. 禁用冲突插件（如多个 AI 插件同时启用）
3. 为大型项目启用 "Power Save" 模式

## 通用建议
1. 优先选择官方认证插件
2. 定期备份插件配置
3. 关注各插件的额度限制变化

## 注意事项
- 各方案的免费额度可能随时间调整，建议定期查看官方说明
- 使用 AI 功能时请注意代码安全性和隐私保护
- 建议先在测试项目中体验，再应用到实际工作中

> 提示：选择适合自己的工具能够大幅提升开发效率和体验。根据你的需求和习惯，选择最合适的方案吧！

---

## Cursor 编辑器中的免费 AI 插件推荐

Cursor 虽然已经内置了强大的 AI 功能（Claude/GPT），但通过安装额外的插件可以进一步增强开发体验。以下是 Cursor 中值得推荐的免费 AI 编程插件：

### 推荐插件对比

| 插件 | 核心功能 | 免费额度 | 推荐指数 |
|------|----------|----------|----------|
| **Codeium** | - 代码补全和对话<br>- 支持多种编程语言<br>- 完全免费无限制 | 完全免费 | ⭐⭐⭐⭐⭐ |
| **GitHub Copilot** | - 代码自动补全<br>- 支持多种语言<br>- 智能注释生成 | 学生/开源项目免费 | ⭐⭐⭐⭐ |
| **Continue** | - 开源 AI 编程助手<br>- 支持本地模型<br>- 可自定义配置 | 完全免费 | ⭐⭐⭐⭐ |
| **Cline** | - 支持 OpenRouter 多模型<br>- Agent 模式自动操作<br>- 高度可定制 | 取决于 OpenRouter 模型 | ⭐⭐⭐⭐ |
| **Tabnine** | - 代码预测补全<br>- 私有代码训练<br>- 团队协作功能 | 基础功能免费 | ⭐⭐⭐ |
| **Fitten Code** | - 国产插件，速度快<br>- 中文支持优秀<br>- 零延迟响应 | 完全免费 | ⭐⭐⭐⭐ |

### 详细推荐及安装方法

#### 1. Codeium（最推荐）

**特点：**
- 完全免费，无使用限制
- 代码补全速度快，质量高
- 支持代码对话和解释
- 不依赖 GitHub 账户

**安装方法：**
1. 在 Cursor 中按 `Ctrl+Shift+X` 打开扩展市场
2. 搜索 "Codeium"
3. 点击 "Install" 安装
4. 安装后会自动提示登录（可使用 GitHub/Google 账户）
5. 登录后即可开始使用

**使用技巧：**
- 使用 `Ctrl+K` 触发代码生成
- 使用 `Ctrl+L` 打开对话面板
- 支持多语言代码补全

#### 2. GitHub Copilot

**特点：**
- 业界标杆级代码补全
- 支持学生和教育账户免费
- 开源项目可申请免费使用

**安装方法：**
1. 打开扩展市场（`Ctrl+Shift+X`）
2. 搜索 "GitHub Copilot"
3. 点击安装
4. 安装后会提示登录 GitHub 账户
5. 确认免费资格后即可使用

**免费资格获取：**
- 学生：访问 [GitHub Education](https://education.github.com/pack) 申请学生包
- 开源项目维护者：在 GitHub 上维护活跃的开源项目可申请免费

#### 3. Continue

**特点：**
- 完全开源免费
- 支持本地模型（如 Ollama）
- 可自定义模型和配置
- 支持多种 AI 服务 API

**安装方法：**
1. 打开扩展市场搜索 "Continue"
2. 点击安装
3. 安装后按 `Ctrl+Shift+P` 打开命令面板
4. 输入 "Continue: Setup" 进行配置
5. 可选择使用本地模型或 API 服务

**配置示例（使用 OpenRouter）：**
```json
{
  "models": [
    {
      "title": "GPT-4",
      "provider": "openrouter",
      "model": "openai/gpt-4",
      "apiKey": "your-api-key"
    }
  ]
}
```

#### 4. Cline

**特点：**
- 支持 OpenRouter 多种免费模型
- Agent 模式可自动执行操作
- 类似于 AI 编程助手

**安装方法：**
1. 搜索 "Cline" 或 "Claude Dev"
2. 点击安装
3. 配置 OpenRouter API Key（可在 [OpenRouter](https://openrouter.ai/) 免费注册）
4. 选择使用的模型（推荐免费模型如 `mistralai/mistral-7b-instruct`）

**配置步骤：**
- 获取 OpenRouter API Key
- 在插件设置中填入 API Key
- 选择适合的模型

#### 5. Fitten Code

**特点：**
- 国产插件，国内访问速度快
- 完全免费
- 对中文注释理解优秀
- 响应速度快

**安装方法：**
1. 搜索 "Fitten Code"
2. 点击安装
3. 安装后自动启用，无需额外配置
4. 首次使用可能需要登录（可选）

### Cursor 插件安装通用步骤

1. **打开扩展市场**
   - 快捷键：`Ctrl+Shift+X`（Windows/Linux）或 `Cmd+Shift+X`（Mac）
   - 或点击左侧活动栏的扩展图标

2. **搜索插件**
   - 在搜索框输入插件名称
   - 查看插件评分和下载量

3. **安装插件**
   - 点击 "Install" 按钮
   - 等待安装完成

4. **配置插件**
   - 部分插件安装后需要配置 API Key 或其他设置
   - 按 `Ctrl+,` 打开设置，搜索插件名称进行配置

5. **启用插件**
   - 安装后插件通常自动启用
   - 可在扩展列表中查看插件状态

### 使用建议

1. **组合使用**：Cursor 内置 AI + Codeium 是很好的免费组合
2. **避免冲突**：不要同时启用多个代码补全插件，可能导致冲突
3. **按需选择**：
   - 追求速度：Fitten Code 或 Codeium
   - 需要本地运行：Continue
   - 需要多模型支持：Cline
4. **定期更新**：保持插件为最新版本以获得最佳体验

### 注意事项

- Cursor 内置的 AI 功能已经很强，额外插件主要用于增强特定功能
- 多个 AI 插件同时启用可能会影响性能
- 某些插件可能需要网络访问，注意防火墙设置
- 免费额度可能随时间变化，建议关注插件更新说明

git add "ai编程插件.md"

---

## 调用 ACP/CLI 代理（Claude / Gemini / OpenAI）——Windows + VS Code 使用指南

下面给出在 Windows（PowerShell）下使用常见 AI 服务（OpenAI、Anthropic/Claude、Google Gemini）的快速上手方法，并比较 ACP 与 CLI 的适用场景与优缺点。示例中不包含任何真实密钥；请用你的环境变量替换相应占位符。切勿将 API Key 明文提交到代码仓库。

### 1) ACP vs CLI：该选哪个？
- CLI（命令行工具）优点：上手快、直接在终端或 VS Code 集成，便于交互式调试与自动化脚本（Windows 用户推荐从 CLI 开始）。
- ACP（Agent/协议层）优点：适合多 agent 协作、编排与长期运行的自动化流程；更适合构建复杂流水线或把多个模型联动的场景。
- 建议：初学者/日常编码用 CLI；需要跨服务或多 agent 协作时考虑 ACP 或相应 SDK/中间件。

### 2) Windows：设置环境变量（推荐）
- 临时在当前 PowerShell 会话中设置（仅本次会话有效）：

```powershell
$env:OPENAI_API_KEY = "你的_openai_key"
$env:CLAUDE_API_KEY = "你的_claude_key"
$env:GEMINI_API_KEY = "你的_gemini_key"
```

- 永久写入用户环境变量（需重启终端生效）：

```powershell
setx OPENAI_API_KEY "你的_openai_key"
setx CLAUDE_API_KEY "你的_claude_key"
setx GEMINI_API_KEY "你的_gemini_key"
```

注意：不要把密钥写入仓库或公开文件；若密钥已泄露，请立即在服务提供商控制台撤销并旋转。可考虑使用系统凭据管理器或云端 Secret Manager 存储密钥。

### 3) 快速示例：用 PowerShell 调用 REST API
以下示例使用 `Invoke-RestMethod`（PowerShell 原生），可在 VS Code 的终端中运行。

- OpenAI（REST 示例）：

```powershell
$body = @{ model = 'gpt-4o-mini'; messages = @(@{ role = 'user'; content = '用中文写一个排序算法示例' }) }
Invoke-RestMethod -Uri 'https://api.openai.com/v1/chat/completions' -Method Post -Headers @{ Authorization = "Bearer $env:OPENAI_API_KEY" } -ContentType 'application/json' -Body ($body | ConvertTo-Json -Depth 6)
```

- Anthropic / Claude（REST 示例，具体 endpoint/字段以官方文档为准）：

```powershell
$body = @{ model = 'claude-2.1'; prompt = '请用中文写一个排序算法示例'; max_tokens = 800 }
Invoke-RestMethod -Uri 'https://api.anthropic.com/v1/complete' -Method Post -Headers @{ 'x-api-key' = $env:CLAUDE_API_KEY; 'Content-Type' = 'application/json' } -Body ($body | ConvertTo-Json -Depth 6)
```

- Google Generative / Gemini（示例使用 API Key query 参数，具体以官方文档为准）：

```powershell
$gk = $env:GEMINI_API_KEY
$body = @{ prompt = @{ text = '请用中文写一个排序算法示例' }; temperature = 0.2 }
Invoke-RestMethod -Uri "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate?key=$gk" -Method Post -ContentType 'application/json' -Body ($body | ConvertTo-Json -Depth 6)
```

提示：上面请求格式可能随厂商 API 更新而变化，请以官方 API 文档为准（示例主要演示调用流程与在 PowerShell 中如何传递环境变量）。

### 4) 在 VS Code 中的实用集成方式
- 直接在 VS Code 终端中运行上面 PowerShell 命令（最简单）。
- 使用 VS Code `Tasks`（tasks.json）把常用命令做成快捷任务，按 `Ctrl+Shift+B` 或命令面板运行。
- 使用扩展 `REST Client` 或 `Thunder Client`：把示例 HTTP 请求保存为 `.http` 或在界面中配置变量，按需发送请求并方便保存历史。

示例：用 `REST Client` 的 `openai.http`（保存为文件后点击 Send Request）：

```http
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json

{
   "model": "gpt-4o-mini",
   "messages": [{ "role": "user", "content": "用中文写一个排序算法示例" }]
}
```

（在 REST Client 扩展中可以配置环境变量或手动替换 `{{OPENAI_API_KEY}}`）

### 5) 在 VS Code 中把 CLI 工具当作 Agent 使用
- 许多项目会提供本地 CLI（例如某些 Claude/Gemini/自研 agent 的 CLI）；在 VS Code 通过 Terminal / Tasks / 自定义扩展调用这些 CLI，就能把它们集成到工作流中。
- 若要把 agent 与项目自动化结合，可编写 PowerShell 脚本或 Node/Python 小工具：在脚本里读取环境变量、向模型发起请求并把结果写回文件或运行测试。

示例：简单 PowerShell 脚本 `ai-run.ps1`：

```powershell
param([string]$prompt = "写一个示例函数")
$body = @{ model = 'gpt-4o-mini'; messages = @(@{ role = 'user'; content = $prompt }) }
$resp = Invoke-RestMethod -Uri 'https://api.openai.com/v1/chat/completions' -Method Post -Headers @{ Authorization = "Bearer $env:OPENAI_API_KEY" } -ContentType 'application/json' -Body ($body | ConvertTo-Json -Depth 6)
$resp.choices
```

然后在 VS Code 任务中配置运行该脚本并传入参数，实现“一键询问 AI 并把结果显示在终端/输出面板”的体验。

### 6) 安全与运维建议
- 永远不要把 API Key 写入源码或提交到 Git。把密钥放到系统环境变量、Windows 凭据管理器、或云 Secret Manager（如 Azure Key Vault、AWS Secrets Manager、GCP Secret Manager）。
- 若怀疑密钥泄露，立即在供应商控制台撤销并生成新密钥。
- 为生产系统使用短期凭证或受限权限的服务账号，避免使用长期高权限密钥。

### 7) 常见故障与排查
- 401/403：检查 Key 是否正确、是否已被撤销或绑定了 IP 限制。
- 429/额度问题：检查厂商免费额度或速率限制，考虑限流或缓存常见请求。
- 请求格式错误：使用 `-Verbose` 或查看返回的错误 JSON，按厂商文档调整请求字段与模型名称。

---

如果你愿意，我可以：
- 把上面的示例脚本写成一个小仓库（含 `ai-run.ps1`、`openai.http`、以及一个 `README.md` 的使用说明）；
- 或者把示例直接补到本仓库的独立文件（例如 `docs/Windows_AI_Agents.md`）。

请告诉我你希望的下一步。