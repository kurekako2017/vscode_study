# AI Agent & 大模型开源项目学习参考资料

> 这是一份偏“学习路线 + 训练手册”的资料，适合和 [GitHub 网站工具与热门项目学习地图](github网站工具推荐.md) 配套使用。
>
> 本资料基于多份前沿 AI Agent 学习路线图、GitHub 热门开源项目榜单以及 Codex 必装技能指南整理而成，目标是给后续的深入学习与项目实战提供一份更顺手的参考。

## 章节连接

- [1. 先怎么用这份资料](#1-先怎么用这份资料)
- [2. AI Agent 系统化学习路线图](#2-ai-agent-系统化学习路线图)
- [3. GitHub 核心热榜 - Skill 职业化与基建](#3-github-核心热榜---skill-职业化与基建)
- [4. 6 大 Agent 开源项目合集推荐](#4-6-大-agent-开源项目合集推荐)
- [5. Codex 必装十大 Skills 指南](#5-codex-必装十大-skills-指南)
- [6. 推荐学习节奏](#6-推荐学习节奏)

## 快速路线

| 顺序 | 项目 | 作用 |
| :--- | :--- | :--- |
| 1 | [llm-cookbook](https://github.com/datawhalechina/llm-cookbook) | 先打 LLM / Prompt 基础 |
| 2 | [llm-universe](https://github.com/datawhalechina/llm-universe) | 再做一个能跑的 LLM 应用 |
| 3 | [All-in-RAG](https://github.com/datawhalechina/all-in-rag) | 学 RAG 全栈链路 |
| 4 | [Hello-Agents](https://github.com/datawhalechina/hello-agents) | 学 Agent 系统与协作 |
| 5 | [ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero) | 补全 Agent 全栈路线图 |

## 1. 先怎么用这份资料

- 如果你刚开始学，先看 90 天路线图，建立大方向。
- 如果你想找项目练手，先看 GitHub 热榜和 6 大 Agent 项目合集。
- 如果你已经在写代码，直接看 Codex Skills，补齐工程化流程。

## 2. AI Agent 系统化学习路线图

按照「核心基础 → 关键技术 → 框架应用 → 高级协同 → 工程落地」的顺序推进，可以形成比较稳定的沉浸式学习回路。

| 阶段 | 核心主题 | 推荐学习内容与 B 站 / 在线资源参考 |
| :--- | :--- | :--- |
| **DAY 1** | **Python 核心与开发环境** | B站黑马程序员：`Python 入门实战` |
| **DAY 3** | **大模型基础认知** | B站李沐：`《动手学大模型》入门篇` |
| **DAY 5** | **Transformer 核心原理** | B站王树森：`Transformer 深度解析` |
| **DAY 7** | **Prompt 工程进阶** | B站吴恩达：`《企业级 Prompt 实战》` |
| **DAY 9** | **RAG 技术体系精讲** | B站：`RAG 实战课` |
| **DAY 11** | **RAG 优化与效果评估** | B站：`RAG 优化专题课` |
| **DAY 13** | **LangChain 框架入门** | DeepLearning 专项课程 |
| **DAY 19** | **LangGraph 状态机与工作流** | B站：`LangGraph 教程` |
| **DAY 24** | **Agent 智能体架构核心** | B站李沐相关分享 |
| **DAY 30** | **单 Agent 开发实战** | 李沐：`AI 实战营` |
| **DAY 35** | **多 Agent 系统协作开发** | B站：`多智能体系统设计与实现教程` |
| **DAY 40** | **私有化部署方案** | B站：`VLLM 部署实战` |
| **DAY 43** | **模型轻量化与微调** | B站：`微调实战课` |
| **DAY 45** | **多模态 Agent 开发** | B站：`LLaVA 相关课程` |
| **DAY 48** | **Agent 工程化与监控** | B站：`《AI 应用工程化落地》` |
| **DAY 90** | **全流程项目实战带学** | 李沐：`AI 实战营` |

## 3. GitHub 核心热榜 - Skill 职业化与基建

结合“程序员 Raigor”与“星探 AI”两套热榜，AI 内容生产已经卷到“端到端”，LLM 基建和具象化 Skill 工具也逐渐成为硬需求。下面把原始热榜重新整理成更适合学习的版本。

### 3.1 10 大核心项目

1. **MoneyPrinterTurbo**
   - 排名与数据：Raigor 榜 TOP 1 / 星探榜 #1（周增 +18,553 Star，累计 7.8 万 Star）
   - 定位：全自动短视频端到端生成工具。
   - 特点：输入关键词即可全自动生成视频脚本、混剪素材、配音、字幕并直接输出成片，适合做自媒体批量产出。
   - 开源地址：[harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

2. **markitdown**
   - 排名与数据：Raigor 榜 TOP 2 / 星探榜 #4（累计 14.3 万 Star）
   - 定位：全格式一键转 Markdown 预处理工具。
   - 特点：把 PDF、Word、Excel、PPT 等内容转换成 Markdown，适合做 RAG 前处理。
   - 开源地址：[microsoft/markitdown](https://github.com/microsoft/markitdown)

3. **taste-skill**
   - 排名与数据：Raigor 榜 TOP 3 / 星探榜 #3（累计 3.2 万 Star）
   - 定位：消灭“AI 机械腔”的审美把关框架。
   - 特点：给 Claude、Codex 等开发助手装上“审美大脑”，让输出更自然。
   - 开源地址：[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)

4. **ECC (Enterprise Core Connect)**
   - 排名与数据：星探榜 #2（累计 20.6 万 Star）
   - 定位：面向复杂老旧系统的代码理解与业务抽象组件。
   - 特点：专注于大规模代码逻辑重构与多系统高并发数据对接。
   - 开源地址：原始资料仅给出占位链接，建议后续再核对具体仓库。

5. **headroom**
   - 排名与数据：星探榜 #5（累计 1.0 万 Star）
   - 定位：长文本上下文与 Token 压缩框架。
   - 特点：通过语义剪裁释放上下文空间，减少长对话失忆问题。
   - 开源地址：[headroom-project/headroom](https://github.com/headroom-project/headroom)

6. **freellmapi**
   - 排名与数据：社区热门推荐。
   - 定位：免费顶级大模型 Token 聚合代理工具。
   - 特点：支持 OpenAI 协议接口、自带路由和故障转移，适合个人开发者测试。
   - 开源地址：[tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi)

7. **English-level-up-tips**
   - 排名与数据：Raigor 榜 TOP 5（日均暴涨 1564 Star）
   - 定位：认知科学拆解的英语进阶指南。
   - 特点：新增 AI 辅助章节，可用于打造沉浸式语言习得环境。
   - 开源地址：[byoungd/English-level-up-tips](https://github.com/byoungd/English-level-up-tips)

8. **Awesome-Vibe-Coding-Tools**
   - 定位：AI 时代原生设计的全栈快速交付模板。
   - 特点：适合独立开发者通过一句提示词快速出成品。
   - 开源地址：原始资料未给出明确链接，后续建议补充核对。

9. **Prompt-Sanitizer**
   - 定位：大模型输入端的数据清洗与质量把控工具。
   - 特点：在 RAG 和 Agent 输入大模型前对杂乱数据进行重组与高密度提取。
   - 开源地址：原始资料未给出明确链接，后续建议补充核对。

10. **Agent-Monitor-SDK**
    - 定位：防止 Agent 线上运行跑偏的监控守卫。
    - 特点：用于拦截 Agent 的幻觉和劣质文本，提升生产环境稳定性。
    - 开源地址：原始资料未给出明确链接，后续建议补充核对。

### 3.2 这组项目怎么理解

- 一类偏“内容生产”，比如视频生成、文档转换、文案润色。
- 一类偏“基础设施”，比如上下文压缩、Token 聚合、质量监控。
- 一类偏“工程实践”，比如把 LLM 能力真正嵌进业务流里。

## 4. 6 大 Agent 开源项目合集推荐

| 项目名称 | 介绍与核心价值 | 推荐指数 | 开源地址 (GitHub 直链) |
| :--- | :--- | :---: | :--- |
| **Hello-Agents** | 国内社区 Datawhale 开源的经典教程，适合从底层原理到可运行代码的完整学习。 | ★★★★★★★ | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) |
| **500+ 智能体案例** | GitHub 上的超级目录，涵盖了超过 500 个 AI Agent 落地案例。 | ★★★★★★★ | [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) |
| **智能体资源库** | Nir Diamant 开源的 `GenAI_Agents`，适合手把手构建智能体。 | ★★★★★★☆ | [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| **HF 开源的 Agent 教程** | Hugging Face 官方智能体课程 `Agents Course`，完成后还有结业证书。 | ★★★★★★☆ | [huggingface/agents-course](https://github.com/huggingface/agents-course) |
| **微软开源的 Agents 教程** | `AI Agents for Beginners`，对初学者比较友好。 | ★★★★★★☆ | [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) |
| **6 周学会 AI 智能体** | Ed Donner 课程，通过 6 周系统实践学习构建并部署自主 AI 智能体。 | ★★★★★★☆ | [ed-donner/agents](https://github.com/ed-donner/agents) |

### 4.1 我建议你重点学的 2 个项目

如果你现在主要精力放在 `Hello-Agents` 和 `All-in-RAG`，我建议把它们当成两条主线来学，而不是混着啃。

#### 1）Hello-Agents

- 核心定位：**智能体入门到进阶的系统教程**
- 适合学习的内容：
  - 智能体到底是什么
  - Agent 的经典范式怎么做
  - 框架怎么搭
  - 记忆、协议、多 Agent 协作怎么串起来
  - 如何从“会用大模型”过渡到“会搭智能体系统”
- 这个项目的特点：
  - 更偏 **Agent 思维**
  - 更偏 **系统架构**
  - 更适合建立“智能体系统”的整体认知
  - 你会看到很多“为什么这么设计”的内容，而不只是代码片段
- 适合的学习方式：
  - 先读目录和总纲
  - 再按章节看理论
  - 最后挑一个最容易跑通的案例动手

#### 2）All-in-RAG

- 核心定位：**RAG 技术全栈教程**
- 适合学习的内容：
  - 文档怎么加载和清洗
  - 文本怎么切块
  - embedding 怎么做
  - 向量数据库怎么用
  - 检索怎么优化
  - 生成和评估怎么接起来
- 这个项目的特点：
  - 更偏 **RAG 工程**
  - 更偏 **检索链路**
  - 更适合打基础，理解知识库问答是怎么做出来的
  - 从“数据 -> 向量 -> 检索 -> 生成 -> 评估”这条链路非常完整
- 适合的学习方式：
  - 先看整体目录树
  - 再按章节顺序过一遍
  - 优先跑 `C1`、`C2`、`C3` 里的基础示例

### 4.2 推荐学习顺序

如果你现在是初学者，我建议按下面顺序学：

1. **先学 `All-in-RAG`**
   - 先把 RAG 的基础链路打通
   - 先弄懂“文档怎么进来、怎么切、怎么检索、怎么生成”
   - 这会给你一个很稳定的基础认知

2. **再学 `Hello-Agents`**
   - 在你理解检索和知识注入之后，再看智能体怎么规划、怎么调工具、怎么协作
   - 这时你会更容易理解为什么 Agent 里常常也会用到记忆和检索

3. **最后再看工程化扩展**
   - 比如多 Agent、监控、评估、协议、工作流编排
   - 这一步适合在你能跑通基础项目之后再补

### 4.3 你可以怎么安排时间

- 如果你每周能投入 5 到 8 小时：
  - 第 1 周：All-in-RAG 基础章节
  - 第 2 周：All-in-RAG 项目实战和评估章节
  - 第 3 周：Hello-Agents 前半部分
  - 第 4 周：Hello-Agents 的框架、协作和综合案例

- 如果你时间更紧：
  - 先只学 `All-in-RAG`
  - 把它跑通后，再转 `Hello-Agents`

### 4.4 一个更实用的学习目标

- 先让自己能说清楚：
  - RAG 是怎么工作的
  - Agent 是怎么工作的
  - 两者的关系是什么
- 再让自己能做出来：
  - 一个最小 RAG 问答 demo
  - 一个最小 Agent 工具调用 demo

### 4.5 再加一个 `ai-agents-from-zero` 怎么看

如果把 `ai-agents-from-zero` 也放进来对比，它和前面两个项目的关系会更像“总路线图”：

- 核心定位：**从零到企业级落地的 AI 智能体系统教程**
- 适合学习的内容：
  - 大模型基础
  - Agent / 多 Agent
  - LangChain / LangGraph
  - MCP / Tool Calling
  - RAG 与记忆
  - 部署、实战项目、面试题库
- 这个项目的特点：
  - 更偏 **大而全的学习地图**
  - 更偏 **工程落地和长期更新**
  - 覆盖面比 `Hello-Agents` 更宽，也比 `All-in-RAG` 更综合
  - 你会看到“教程 + 案例 + 面试题库 + 项目实战”一整套内容
- 适合的学习方式：
  - 先当成“总索引”看目录
  - 结合章节总索引挑你缺的部分补
  - 不建议一上来硬啃全部内容，容易信息量过大

### 4.6 三个项目怎么分工

你可以把这三个项目理解成三层：

1. **All-in-RAG**
   - 负责把 RAG 的基础链路打扎实
   - 适合先学，解决“检索增强生成怎么做”的问题

2. **Hello-Agents**
   - 负责把智能体的概念、范式和系统架构打通
   - 适合在理解 RAG 后继续学，解决“Agent 怎么搭”的问题

3. **ai-agents-from-zero**
   - 负责把前面的知识串成更完整的学习路线图
   - 适合当总纲和进阶路线，解决“怎么把 RAG、Agent、LangChain、LangGraph、MCP、项目实战连起来”的问题

### 4.7 推荐学习顺序（更新版）

如果你现在是初学者，我建议这样排：

1. **先学 `All-in-RAG`**
   - 先把 RAG 的底层流程学稳
   - 先知道知识如何进入系统、如何被检索出来

2. **再学 `Hello-Agents`**
   - 重点看 Agent 的思维方式、范式和协作
   - 把“会检索”升级成“会规划、会调用工具、会协作”

3. **最后系统看 `ai-agents-from-zero`**
   - 用它补全更大的全栈视角
   - 重点补 LangChain、LangGraph、MCP、实战项目和面试准备

### 4.8 适合你的实际学习策略

- 如果你的时间有限：
  - 先把 `All-in-RAG` 学通
  - 再挑 `Hello-Agents` 看核心章节
  - `ai-agents-from-zero` 当总参考，不用一次性全刷完

- 如果你想走“完整路线”：
  - `All-in-RAG` 打基础
  - `Hello-Agents` 学 Agent 核心
  - `ai-agents-from-zero` 当总路线图和项目库

- 如果你更偏工程实战：
  - 优先 `ai-agents-from-zero`
  - 但其中 RAG 基础还是建议回头补 `All-in-RAG`

### 4.9 中文教程学习顺序表

如果你想按“先基础、再应用、再系统路线图”的方式继续，推荐直接按下面这个顺序学。

| 顺序 | 项目 | 方向 | 适合先学的原因 | 当前热度 |
| :--- | :--- | :--- | :--- | :---: |
| 1 | [llm-cookbook](https://github.com/datawhalechina/llm-cookbook) | LLM 入门 / Prompt | 先把大模型调用、提示词和基础概念打稳 | 23.7k ⭐ |
| 2 | [llm-universe](https://github.com/datawhalechina/llm-universe) | LLM 应用开发入门 | 先做一个能跑的入门应用，建立整体感觉 | 13.2k ⭐ |
| 3 | [All-in-RAG](https://github.com/datawhalechina/all-in-rag) | RAG 全栈 | 把检索增强生成的整条链路学扎实 | 8.5k ⭐ |
| 4 | [Hello-Agents](https://github.com/datawhalechina/hello-agents) | Agent 系统教程 | 进入智能体思维、范式和系统架构 | 58.5k ⭐ |
| 5 | [ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero) | Agent 综合路线图 | 用更完整的工程视角补全全栈学习地图 | 1.9k ⭐ |

### 4.10 这几个项目怎么分工

- `llm-cookbook`：先学基础，适合把 Prompt、LLM 调用、基础思路打通。
- `llm-universe`：再学应用，适合把“怎么做一个大模型应用”跑明白。
- `All-in-RAG`：再学检索，适合把 RAG 的数据处理、切块、向量库、召回、评估学完整。
- `Hello-Agents`：再学智能体，适合把 Agent 的范式、工具调用、协作和工程架构学清楚。
- `ai-agents-from-zero`：最后补全路线图，适合把前面知识串成更大的系统化学习路径。

### 4.11 最实用的继续学习方式

1. 先看 `llm-cookbook`，把基础概念和 Prompt 习惯养起来。
2. 再看 `llm-universe`，做出第一个完整的 LLM 应用。
3. 接着看 `All-in-RAG`，把检索链路学稳。
4. 然后看 `Hello-Agents`，进入智能体系统设计。
5. 最后用 `ai-agents-from-zero` 做总复盘，补齐工程实战和路线图。

## 5. Codex 必装十大 Skills 指南

这部分是给编码智能体补上工程能力、流程能力和上下文管理能力的，适合做成自己的“技能包清单”。

1. **Superpowers**
   - 类型：Skills Framework
   - 一句话描述：强制 coding agent 走 TDD + 代码审查流程，避免偷懒。
   - 直链：[features/superpowers](https://github.com/features/superpowers)

2. **SuperClaude Framework**
   - 类型：Skills 命令框架
   - 一句话描述：提供 30 条斜杠命令，用于精准指挥 coding agent。

3. **MiniMax Skills**
   - 类型：Skills 集合包
   - 一句话描述：提供 10 个工业级流程卡，覆盖前端全栈及移动端模版。

4. **Anthropic Official Skills**
   - 类型：官方 Skills
   - 一句话描述：Anthropic 官方 skills 参考实现，`skill-creator` 开发者可重点看。

5. **Vercel Agent Skills**
   - 类型：Skills 集合包
   - 一句话描述：Vercel 官方出品，针对 React/Web 架构设计，带有严格审查与性能规则。

6. **Planning with Files**
   - 类型：专项 Skill
   - 一句话描述：用 Markdown 文件给 coding agent 当长期记忆库和多步规划本。

7. **Context Engineering Skills**
   - 类型：Skills 集合包
   - 一句话描述：教 coding agent 智能管理上下文，避免 Token 溢出和长文本失忆。

8. **Composio Skills**
   - 类型：Skills + MCP 联动
   - 一句话描述：让 coding agent 动态调用外部 SaaS 与本地服务。
   - 直链：[ComposioHQ/composio](https://github.com/ComposioHQ/composio)

9. **Antfu Skills**
   - 类型：个人最佳实践 Skills
   - 一句话描述：Anthony Fu 的个人 Skill 配置，属于前端高手的规则样本。
   - 直链：[antfu/dotfiles](https://github.com/antfu/dotfiles)

10. **Awesome Agent Skills**
    - 类型：Skills 索引百科
    - 一句话描述：收录 500+ 各大厂及开源社区优质 Skills 的超级索引目录。
    - 直链：[awesome-agent-skills](https://github.com/indexing/awesome-agent-skills)

## 6. 推荐学习节奏

- 第一轮：先过 90 天路线图，建立 Agent、RAG、Prompt、部署的整体认知。
- 第二轮：挑 1 个 Agent 框架和 1 个工具链项目跑起来。
- 第三轮：把 Codex Skills、Prompt 质量、上下文管理和测试验证流程融进自己的日常工作流。
- 第四轮：结合 [GitHub 网站工具与热门项目学习地图](github网站工具推荐.md)，把学习范围从 Agent 扩展到多媒体、量化、部署和工程化。
