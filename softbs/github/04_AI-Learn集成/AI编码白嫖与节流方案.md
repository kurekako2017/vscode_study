# AI 编码白嫖与节流方案（整理版）

> 整理自：社区开源桥接方案、[GitHub 网站工具与热门项目学习地图](../02_工具知识库/github网站工具推荐_优化完整版.md)、[GitHub AI 工具学习体系](../02_工具知识库/GitHub_AI_工具学习体系.md)，并结合本仓库已有 WSL / Ollama 实战文档。
> **目标**：不花钱或尽量少花钱，也能练习 **大模型上下文管理、Prompt 工程、Agent 式改码流程**。

---

## 快速跳转

- [1. 先选路线：30 秒决策](#sec-1)
- [2. 方案总览对比表](#sec-2)
- [3. 方案一：本地全免费（最推荐练手）](#sec-3)
- [4. 方案二：开源桥接免费云端模型](#sec-4)
- [5. 方案三：免费额度型云端插件](#sec-5)
- [5.2 NVIDIA NIM / Build 免费端点](#sec-5-2)
- [6. 方案四：Token 聚合与路由节流](#sec-6)
- [7. 按阶段怎么选](#sec-7)
- [8. UM890 Pro 推荐组合](#sec-8)
- [9. 配套开源项目与学习资源](#sec-9)
- [10. 风险与注意事项](#sec-10)
- [11. 本仓库相关文档](#sec-11)

---

<a id="sec-1"></a>

## 1. 先选路线：30 秒决策

```text
有 Claude Pro（$20/月）？
  └─ 是 → 直接用 Claude Code / Cursor Pro，不必折腾桥接
  └─ 否 → 继续往下看

主要在本机 UM890 / WSL 开发？
  └─ 是 → 优先「VS Code + WSL + Continue + Ollama」（完全免费、最稳）
  └─ 否 → 看方案二 OpenRouter 桥接

想要终端 Agent、多文件自主改码？
  └─ 本地 → Aider + Ollama
  └─ 云端免费 → Claude Code + OpenRouter，或 Cline + OpenRouter

只要 Tab 补全、偶尔问答？
  └─ Codeium / GitHub Copilot Free
```

---

<a id="sec-2"></a>

## 2. 方案总览对比表

| 方案 | 费用 | 隐私 | Agent 能力 | 上手难度 | 适合谁 |
| --- | --- | --- | --- | --- | --- |
| **Continue + Ollama（本地）** | 0 元 | 最高 | 中（Ask/Edit 稳，Agent 看模型） | 低 | **本仓库默认推荐** |
| **Roo Code + Ollama（本地）** | 0 元 | 最高 | 中高 | 中 | 想要更强 Agent 感的 VS Code 用户 |
| **Aider + Ollama（终端）** | 0 元 | 最高 | 高（多文件改码） | 中 | 命令行熟练、批量改库 |
| **Claude Code + OpenRouter** | 0 元（免费模型） | 数据出网 | 高 | 中 | 想练官方 Agent 流程、无本地算力 |
| **Cline + OpenRouter** | 0 元（免费模型） | 数据出网 | 高 | 中 | VS Code 内自主跑终端的 Agent |
| **OpenCode（开源）** | 0 元 | 可自建 | 高 | 中高 | 要私有化 Coding Agent |
| **Codeium / Copilot Free** | 0 元（有限额） | 云端 | 低～中 | 最低 | 补全为主、轻量问答 |
| **FreeLLMAPI 等聚合** | 0 元（视节点） | 视节点 | 中 | 高 | 自建 API 路由、开发测试 |

---

<a id="sec-3"></a>

## 3. 方案一：本地全免费（最推荐练手）

核心思路：**模型跑在本机，编辑器插件直连 `localhost:11434`，不产生 API 账单。**

### 3.1 VS Code + WSL + Continue + Ollama（本仓库主方案）

| 项目 | 说明 |
| --- | --- |
| 组件 | Ollama（WSL）+ Continue 扩展（WSL 侧）+ VS Code Remote - WSL |
| 默认模型 | `qwen2.5-coder:3b`（UM890 Pro 省内存） |
| 费用 | **0 元** |
| 能力 | Chat、选中改码（`Ctrl+L`）、行内改码（`Ctrl+I`） |

**操作要点：**

```bash
# WSL 内
ollama pull qwen2.5-coder:3b
# systemd 或 ollama serve 保持 11434 可用
```

Continue 配置 `~/.continue/config.yaml` 指向 `http://localhost:11434`。

**详细教程**（含 Prompt 模板、快捷键）：

- [../../vscode/WSL_Continue_Ollama_安装使用教程.md](../../vscode/WSL_Continue_Ollama_安装使用教程.md)

**优点**：最稳定、最省钱、最适合本地模型、数据不出机器。  
**缺点**：3B 模型能力有限；CPU 推理比云端慢；复杂 Agent 不如大模型。

---

### 3.2 Roo Code + 本地 Ollama（省钱 Agent 向）

| 项目 | 说明 |
| --- | --- |
| 是什么 | VS Code 扩展，偏 **自主 Agent**（读文件、跑命令、多步改码） |
| 安装 | 扩展市场搜 **Roo Code**（原 Roo Cline 系） |
| 连接 | 设置里选 Ollama Provider，`http://localhost:11434` |
| 模型 | 本地 `qwen2.5-coder:3b` 或 `7b`；UM890 建议先 3B |

与 Continue 的分工：

| 工具 | 更适合 |
| --- | --- |
| Continue | 选中代码问答、小改、Prompt 练手 |
| Roo Code | 多文件任务、带终端执行的 Agent 流程 |

**UM890 注意**：3B 跑 Agent 易慢或失败，宜 **小仓库、小任务**；大改动用 Aider 或云端桥接。

---

### 3.3 Aider + Ollama（终端多文件改码）

| 项目 | 说明 |
| --- | --- |
| 是什么 | 终端 AI 结对编程，自动改多个文件、走 Git diff |
| 安装 | `pip install aider-chat`（WSL venv 推荐） |
| 启动 | `aider --model ollama/qwen2.5-coder:3b --no-stream` |
| 费用 | **0 元** |

本仓库文档：

- `softbs/aider/01_Aider + Ollama Windows 标准启动方案.md`
- `softbs/aider/04_VS Code + Aider + Ollama 完整开发流.md`
- `softbs/aider/02_Aider 参数调优（UM890 Pro  32GB 内存专用）.md`

**优点**：多文件改动强、可审计 diff。  
**缺点**：命令行为主，不如 Continue 图形化顺手。

---

### 3.4 OpenCode（开源私有化 Coding Agent）

| 项目 | 说明 |
| --- | --- |
| 链接 | https://github.com/opencode-ai/opencode |
| 定位 | 开源、可自托管的 Coding Agent，替代型编程助手 |
| 费用 | 软件 0 元；自托管则只花机器成本 |
| 适合 | 想理解 Agent 架构、私有化部署 |

见 [GitHub 网站工具与热门项目学习地图](../02_工具知识库/github网站工具推荐_优化完整版.md)第 2 节。

---

### 3.5 本地方案推荐组合（0 元）

```text
日常问答 / 小改码  → Continue + Ollama（Ctrl+L）
多文件批量修改    → Aider + Ollama（同一 Ollama 服务）
想试 Agent 自动化 → Roo Code + Ollama（小任务）
```

三者 **共用一个 Ollama**，不要同时对大项目下重 prompt。

---

<a id="sec-4"></a>

## 4. 方案二：开源桥接免费云端模型

核心思路：**前端用成熟 Agent 产品（Claude Code、Cline），后端 HTTP 指到 OpenRouter 等平台的免费模型。**

### 4.1 Claude Code + OpenRouter（终端 Agent，0 元练流程）

适合：**没有付费 Claude 账号**，但想体验 **Claude Code 终端 Agent 命令流**。

#### 步骤 1：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

（在 WSL 或本机 Node 环境均可，与日常开发环境统一即可。）

#### 步骤 2：注册 OpenRouter 并拿 API Key

1. 打开 https://openrouter.ai/
2. 注册账号，创建 API Key  
3. 在模型列表中筛选 **`:free`** 免费模型（额度与可用模型以官网为准）

#### 步骤 3：改本地配置

编辑 `~/.claude/settings.json`（路径以 Claude Code 文档为准）：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "你的_OpenRouter_API_Key",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_MODEL": "qwen/qwen-2.5-coder-32b-instruct:free"
  }
}
```

说明：

- `ANTHROPIC_BASE_URL` 把请求 **桥接** 到 OpenRouter，而非 Anthropic 官方  
- `ANTHROPIC_MODEL` 换成 OpenRouter 上当前可用的 **免费** 模型 ID  
- 免费模型名会变，部署前到 OpenRouter 模型页核对

#### 步骤 4：验证

```bash
claude
```

在终端下发小任务（如「列出当前目录并解释 README」），观察是否正常响应。

**优点**：Agent 体验接近官方 Claude Code；可用 **32B 级免费云端模型**（本机跑不动时）。  
**缺点**：数据经第三方；免费模型有速率/额度限制；配置错误时排查成本高。

**相关学习**：[Claude Code 最佳实践](https://code.claude.com/docs/zh-CN/best-practices)（上下文、验证、权限）。

---

### 4.2 Cline + OpenRouter（VS Code 内 Agent）

| 项目 | 说明 |
| --- | --- |
| 扩展 | VS Code 搜 **Cline**（原 Claude Dev） |
| 配置 | API Provider 选 OpenRouter，填入 Key 与免费模型 |
| 能力 | 读文档、改代码、**自动跑终端命令**（比 Continue 更「侵略性」） |
| 费用 | 0 元（用免费模型时） |

见 `softbs/aider/ai编程插件.md` 中 Cline 对比说明。

**与 Continue 选型**：

| 需求 | 选 |
| --- | --- |
| 稳定、轻量、本地优先 | Continue + Ollama |
| 云端免费 + 强 Agent | Cline + OpenRouter |
| 终端 + 官方 Agent 手感 | Claude Code + OpenRouter |

---

### 4.3 其他桥接思路（了解即可）

| 工具 | 说明 |
| --- | --- |
| **OpenClaw / Molili** | 通用 Agent 框架，可接本地或国内模型，见 [GitHub 工具学习地图](../02_工具知识库/github网站工具推荐_优化完整版.md) |
| **Claude-CLI 非官方** | https://github.com/kiliczsh/claude-cmd ，终端调用 Claude 的第三方工具 |
| **gpt-codex** | https://github.com/xianyu110/gpt-codex ，编码辅助与脚本自动化参考 |

---

<a id="sec-5"></a>

## 5. 方案三：免费额度型云端插件

不折腾桥接、不跑本地模型时，用 **官方免费层** 做补全和轻量问答。

| 工具 | 费用 | 特点 | 安装 |
| --- | --- | --- | --- |
| **Codeium** | 免费 | 补全接近 Copilot，多语言 | VS Code 搜 Codeium |
| **GitHub Copilot Free** | 免费有限额 | 补全 + Chat；自定义本地模型需另配 | Copilot + Copilot Chat |
| **TabNine** | 基础免费 | 补全为主 | VS Code 搜 TabNine |
| **Amazon Q Developer** | 个人层免费 | IDEA 里 Java/AWS 生态友好 | JetBrains 插件市场 |
| **CodeGeeX** | 免费 | 中文注释、单测生成 | VS Code / IDEA |
| **Fitten Code** | 免费 | 国内访问快 | IDEA 等 |

详见 `softbs/aider/ai编程插件.md`。

**节流建议**：

- 补全用 **Codeium** 或 **Copilot Free**  
- 深度改码、长上下文用 **本地 Continue** 或 **OpenRouter 桥接**  
- 避免 **Cursor Pro / Claude Pro** 与免费方案 **重复付费**

<a id="sec-5-2"></a>

### 5.2 NVIDIA NIM / Build 免费端点（官方免费模型）

如果你想要的是“**官方可用的免费模型端点**”，NVIDIA 的 [`build.nvidia.com`](https://build.nvidia.com/) 是一个值得补进方案里的选项。官方页面会把部分模型标成 **Free Endpoint** 或 **Downloadable Free Endpoint**，并提供 `NVIDIA_API_KEY` 的接入方式。  
适合场景：**在线试用、Prompt 练习、Agent 走通路、需要 OpenAI 风格接口的开发测试**。

| 项目 | 说明 |
| --- | --- |
| 平台 | [build.nvidia.com](https://build.nvidia.com/) / NVIDIA NIM APIs |
| 费用 | 官方标注为 Free Endpoint 的模型可免费试用，具体额度与条款以官网为准 |
| 接入方式 | 使用 `NVIDIA_API_KEY`，并通过 `https://integrate.api.nvidia.com/v1` 这类 OpenAI 兼容入口调用 |
| 适合 | 聊天、代码辅助、规划、推理、多模态问答、RAG 试验 |
| 注意 | 免费端点、模型名称、额度会调整，使用前先核对官方模型页 |

**可优先看的模型类型：**

- `nemotron` 系列：偏推理、规划、工具调用，适合 Agent / 编码辅助
- `llama-3.3-nemotron-*`：适合聊天、代码理解、规划类任务
- `llama-3.1-nemotron-*`：适合轻量级推理和多模态场景
- `cosmos*`、`paligemma` 等：更偏多模态、视觉理解，不一定是编码主力，但可作为补充方案

**简化接入步骤：**

```bash
# 1) 到 build.nvidia.com 申请 NVIDIA API Key
# 2) 在支持 OpenAI 兼容接口的工具里配置：
#    base_url = https://integrate.api.nvidia.com/v1
#    api_key  = 你的 NVIDIA_API_KEY
# 3) 选择官网当前可用的 Free Endpoint 模型
```

**适合放进本方案的原因：**

- 你可以把它当成“**官方免费云端模型**”补进白嫖梯队
- 和 OpenRouter 免费模型相比，NVIDIA 这条线更像“官方平台的免费入口”
- 对写代码的人来说，`OpenAI-compatible` 接法比较容易接到 Continue / Cline / 自己的 FastAPI 里

**官方入口：**

- [NVIDIA Build / NIM APIs](https://build.nvidia.com/)
- [OpenAI Compatible Services - NVIDIA Docs](https://docs.nvidia.com/nemo/curator/latest/curate-text/generate-data/connect-service/openai.html)

---

<a id="sec-6"></a>

## 6. 方案四：Token 聚合与路由节流

适合已有一定工程能力、想 **统一 API 入口、故障转移、省 Key 管理成本** 的场景。

| 项目 | 链接 | 作用 |
| --- | --- | --- |
| **FreeLLMAPI** | https://github.com/tashfeenahmed/freellmapi | 免费大模型 Token 聚合，OpenAI 兼容接口 |
| **OpenRouter** | https://openrouter.ai/ | 多模型路由，含 `:free` 模型 |
| **headroom** | https://github.com/headroom-project/headroom | 长上下文压缩，省 Token |
| **ECC** | https://github.com/affaan-m/ECC | Agent 性能优化（Claude Code / Codex / Cursor 等） |

来自 [GitHub 工具学习地图](../02_工具知识库/github网站工具推荐_优化完整版.md)第 11 节、[GitHub AI 工具学习体系](../02_工具知识库/GitHub_AI_工具学习体系.md)第 3 节。

**节流用法**：

- 开发测试走 **免费模型 / FreeLLMAPI**  
- 生产或重要任务再切付费模型  
- 长对话配合 **headroom** 或自建摘要，减少重复塞上下文  

---

<a id="sec-7"></a>

## 7. 按阶段怎么选

### 7.1 当前阶段实践建议（来自社区总结）

| 你的情况 | 推荐 |
| --- | --- |
| **已有 Claude Pro** | 直接 Claude Code，不必桥接 |
| **无付费账号，要练 Agent** | Claude Code + OpenRouter **或** Roo Code / Cline + 本地 Ollama |
| **无付费账号，要稳、要隐私** | **Continue + Ollama**（本仓库已写教程） |
| **主要学 Prompt / 上下文** | 以上任选其一，刻意练「选中代码 → 明确约束 → 验证」 |
| **主要学多文件协作** | Aider + Ollama，或 Cline Agent |

三种路径的 **工作流相似度** 都很高：都是「给上下文 → 模型规划 → 改文件 / 跑命令 → 人审核」。差别在 **模型强弱、是否出网、是否花钱**。

### 7.2 与 90 天 Agent 学习路线配合

见 [GitHub AI 工具学习体系](../02_工具知识库/GitHub_AI_工具学习体系.md)：

- **DAY 7 Prompt** → 用 Continue 练固定 Prompt 模板（见 WSL Continue 教程 7.9 节）  
- **DAY 24 Agent 架构** → 用 Roo Code / Cline / Claude Code 观察 Planner + Tool  
- **DAY 40 私有化部署** → Ollama + WSL 即最小私有化  
- **Codex Skills** → 给 Agent 加 TDD、审查流程（Superpowers 等）

---

<a id="sec-8"></a>

## 8. UM890 Pro 推荐组合

机器：Ryzen 9 8945HS / 32GB / 核显，**无独显大模型加速**。

### 8.1 默认 0 元方案（日常开发）

```text
VS Code Remote - WSL
  ├── Continue + Ollama（qwen2.5-coder:3b）  ← 主用
  └── Aider + Ollama（同模型）               ← 多文件时
```

WSL `.wslconfig` 建议 `memory=20GB`。教程：

- [../../vscode/WSL_Continue_Ollama_安装使用教程.md](../../vscode/WSL_Continue_Ollama_安装使用教程.md)

### 8.2 需要更强模型时（仍尽量不花钱）

| 场景 | 做法 |
| --- | --- |
| 本机只轻量开发 | 试 `ollama pull qwen2.5-coder:7b`，关闭 Docker 再用 |
| 本机跑不动 32B | **Claude Code + OpenRouter 免费 32B 模型** |
| 要 Agent 自动跑命令 | Roo Code + 本地 3B（小任务）或 Cline + OpenRouter |

### 8.3 不建议在 UM890 上日常做的

- 本地 `14b` / `32b` 常驻（内存与 CPU 扛不住）  
- Continue + Aider + Roo Code **同时**对大仓库下任务  
- 未读 diff 就接受 Agent 批量改码  

---

<a id="sec-9"></a>

## 9. 配套开源项目与学习资源

### 9.1 AI 编程与 Agent 框架（扩展阅读）

| 项目 | 链接 | 与白嫖方案关系 |
| --- | --- | --- |
| Claude Code | https://github.com/anthropics/claude-code | 可桥接 OpenRouter |
| OpenCode | https://github.com/opencode-ai/opencode | 开源自托管 Agent |
| AutoGPT | https://github.com/significant-gravitas/autogpt | 学 Agent 拆解与工具调用 |
| AI-Coding-Guide-Zh | https://github.com/KimYx0207/AI-Coding-Guide-Zh | 中文编码工作流 |
| Hello-Agents | https://github.com/datawhalechina/hello-agents | 系统学 Agent |

完整清单见 [GitHub 工具学习地图](../02_工具知识库/github网站工具推荐_优化完整版.md)第 2、4 节。

### 9.2 学生 / GitHub 相关节流

| 资源 | 说明 |
| --- | --- |
| **GitHub 学生版** | 含 Copilot、Codespaces 等权益，见 `GitHub学生版学习与DevOps实践教程.md` |
| **GitHub Codespaces** | 免费时长有限，适合短期练环境，见 `Codespaces学习要点.md` |
| **FMHY** | https://fmhy.net/ 免费资源导航，**注意来源质量与合规** |

### 9.3 Prompt 与工程化增效（不花钱提质量）

| 项目 | 作用 |
| --- | --- |
| taste-skill | 减少 AI 机械腔 |
| stop-slop | 输出更自然 |
| Planning with Files | 用 Markdown 当 Agent 长期记忆 |
| Context Engineering Skills | 控制 Token、防失忆 |

见 [GitHub AI 工具学习体系](../02_工具知识库/GitHub_AI_工具学习体系.md)及工具学习地图中的 Codex Skills 章节。

---

<a id="sec-10"></a>

## 10. 风险与注意事项

| 风险 | 说明 |
| --- | --- |
| **免费模型变动** | OpenRouter `:free` 模型 ID、额度常调整，需定期核对 |
| **数据出网** | 桥接方案代码会发到第三方，**公司 / 客户代码勿用** |
| **API Key 泄露** | `settings.json`、`.env` 勿提交 Git；用环境变量或本地私密配置 |
| **Agent 误操作** | 自动跑终端可能 `rm`、改配置，**必须人工 review diff** |
| **合规** | FMHY、非官方桥接等自行承担风险；生产环境用正规授权 |
| **幻觉** | 小模型 + 大上下文更易胡说；用测试、编译、lint 验证 |

---

<a id="sec-11"></a>

## 11. 本仓库相关文档

| 文档 | 路径 |
| --- | --- |
| **Continue + Ollama 实操（UM890）** | [../../vscode/WSL_Continue_Ollama_安装使用教程.md](../../vscode/WSL_Continue_Ollama_安装使用教程.md) |
| Aider + Ollama | `softbs/aider/` 目录 |
| AI 编程插件对比 | `softbs/aider/ai编程插件.md` |
| GitHub 工具地图 | [github网站工具推荐_优化完整版.md](../02_工具知识库/github网站工具推荐_优化完整版.md) |
| Agent 学习路线 | [GitHub_AI_工具学习体系.md](../02_工具知识库/GitHub_AI_工具学习体系.md) |
| WSL 开发入门 | [../../vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md](../../vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md) |

---

## 最短路径：今天就开始 0 元编码

**路径 A（本地，推荐）：**

1. WSL 安装 Ollama → `ollama pull qwen2.5-coder:3b`  
2. VS Code WSL 安装 **Continue**  
3. 配置 `~/.continue/config.yaml` → 按 [WSL Continue 教程](../../vscode/WSL_Continue_Ollama_安装使用教程.md)  
4. 选中代码 → `Ctrl+L` → 用「只返回最终代码」Prompt 模板  

**路径 B（云端免费 Agent）：**

1. 注册 OpenRouter → 拿 API Key  
2. `npm i -g @anthropic-ai/claude-code`  
3. 配置 `~/.claude/settings.json` 桥接到 OpenRouter 免费模型  
4. 终端 `claude` 练小任务  

**路径 C（补全为主）：**

1. VS Code 安装 **Codeium**  
2. 深度任务仍走路径 A 或 B  

---

> 总结：**练手与日常节流** 优先 **Continue + Ollama**；**练 Agent 流程** 用 **Claude Code / Cline + OpenRouter** 或 **Roo Code + 本地 Ollama**；**只补全** 用 **Codeium**。三者可并存，按任务切换，避免重复付费。
