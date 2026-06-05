# AI Agent & 大模型开源项目学习参考资料

本资料基于多份前沿AI Agent学习路线图、GitHub热门开源项目榜单、以及Codex必装技能指南整理而成，旨在为后续的深入学习与项目实战提供系统化的参考。

---

## 一、 AI Agent 系统化学习路线图 (90天规划)

按照「核心基础 → 关键技术 → 框架应用 → 高级协同 → 工程落地」的科学顺序，打造沉浸式学习回路。

| 阶段 | 核心主题 | 推荐学习内容与B站/在线资源参考 |
| :--- | :--- | :--- |
| **DAY 1** | **Python核心与开发环境** | B站黑马程序员：`Python 入门实战` |
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

---

## 二、 GitHub 爆火热门工具与「Skill职业化」主力项目

AI内容生产已卷到“端到端”，LLM基建工具成为刚需。以下为当前技术社区高热度的开源项目及其实际开源地址。

### 1. MoneyPrinterTurbo
* **定位**：全自动短视频生成工具。
* **特点**：端到端零手动。只需输入关键词，即可全自动生成视频脚本、混剪素材、配音、字幕并输出成片。支持中英文，支持本地开源部署，不卡商业API额度，非常适合自媒体及短视频批量产出。
* **开源地址**：[harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

### 2. markitdown（微软官方维护）
* **定位**：全格式一键转 Markdown 工具。
* **特点**：支持将 PDF、Word、Excel、PPT 等各种格式一键转换为结构完整的 Markdown 文件，保留完整上下文。是针对 LLM 相关的 RAG（检索增强生成）系统进行文档预处理的硬核神器，效率高。
* **开源地址**：[microsoft/markitdown](https://github.com/microsoft/markitdown)

### 3. taste-skill（AI品味管家）
* **定位**：告别AI生成的“废话文学”，赋予大模型审美大脑。
* **特点**：为 Claude/Codex/Cursor/Claude Code 等注入完整的品味管控系统。使生成的代码注释、UI布局、技术文档秒变人类高级质感，拒绝千篇一律的机械化“AI腔”。
* **开源地址**：[Leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill)

### 4. freellmapi
* **定位**：OpenAI 兼容的 API 代理工具。
* **特点**：聚合了多达 16 家 AI 服务商的免费层 API 密钥（可提供海量 Tokens/月），支持智能路由与自动故障转移。极其适合低成本进行 Vibe Coding 试验和个人轻量级开发工作流。
* **开源地址**：[tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi)

### 5. English-level-up-tips
* **定位**：基于认知科学拆解的英语进阶指南。
* **特点**：新增 AI 辅助章节，教你如何利用 Gemini / ChatGPT 打造沉浸式语言习得回路，提供雅思/托福等备考的直接参考。
* **开源地址**：[byoungd/English-level-up-tips](https://github.com/byoungd/English-level-up-tips)

---

## 三、 6 大 Agent 开源项目合集推荐

| 项目名称 | 介绍与核心价值 | 推荐指数 | 开源地址 (GitHub 直链) |
| :--- | :--- | :---: | :--- |
| **Hello-Agents** | 国内社区 Datawhale 开源的经典教程。既能带你深入底层原理，又能手把手带你写出能跑通的 Agent 代码。 | ★★★★★★★ | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) |
| **500+ 智能体案例** | GitHub 上的超级目录，涵盖了超过 500 个 AI Agent 落地案例，适合寻找灵感与方案参考。 | ★★★★★★★ | [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) |
| **智能体资源库** | 国外 AI 技术博主 Nir Diamant 大佬开源的 `GenAI_Agents`。通过极其清晰的路径，手把手教你从零构建智能体。 | ★★★★★★☆ | [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| **HF开源的 Agent 教程** | Hugging Face 官方开源的智能体课程 `Agents Course`。完成所有章节和 Final Project 后，还能获得官方颁发的结业证书。 | ★★★★★★☆ | [huggingface/agents-course](https://github.com/huggingface/agents-course) |
| **微软开源的 Agents 教程** | 微软推出的 `AI Agents for Beginners`，对初学者极其友好，大厂出品有保障。 | ★★★★★★☆ | [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) |
| **6周学会 AI 智能体** | 课程导师为 Ed Donner，通过为期 6 周的系统实践学习，引导开发者完全掌握如何构建和部署自主 AI 智能体。 | ★★★★★★☆ | [ed-donner/agents](https://github.com/ed-donner/agents) |

---

## 四、 Codex 必装十大 Skills 指南

为编码智能体（Coding Agent）赋予的核心框架与工程能力，是拒绝智能体偷懒、提升生产力的关键。

1. **Superpowers**
   * *类型*：Skills Framework
   * *一句话描述*：强制 coding agent 走 **TDD（测试驱动开发）+ 代码审查** 流程，坚决不让 coding agent 偷懒。
   * *直链*：[features/superpowers](https://github.com/features/superpowers) *(或对应专属工具集)*

2. **SuperClaude Framework**
   * *类型*：Skills 命令框架
   * *一句话描述*：提供丰富条斜杠 (`/`) 命令，用于精准指挥和操控 coding agent 高效干活。

3. **MiniMax Skills**
   * *类型*：Skills 集合包
   * *一句话描述*：提供工业级流程卡，前端全栈及移动端工程模版全覆盖。

4. **Anthropic Official Skills**
   * *类型*：官方 Skills
   * *一句话描述*：Anthropic 官方的 skills 参考实现，`skill-creator` 开发者研发必看。

5. **Vercel Agent Skills**
   * *类型*：Skills 集合包
   * *一句话描述*：Vercel 官方出品，专门针对 React/Web 架构设计，自带 140+ 条严格的审查与性能规则。

6. **Planning with Files**
   * *类型*：专项 Skill
   * *一句话描述*：用清晰的 Markdown 文件管理给 coding agent 当作外挂长期记忆库和多步规划本。

7. **Context Engineering Skills**
   * *类型*：Skills 集合包
   * *一句话描述*：教 coding agent 智能管理自己的上下文，防止上下文 Token 溢出或长文本细节失忆。

8. **Composio Skills**
   * *类型*：Skills + MCP 联动
   * *一句话描述*：MCP（Model Context Protocol）与 Skills 双重配合，教 coding agent 动态调用丰富的外部 SaaS 与本地服务。
   * *直链*：[ComposioHQ/composio](https://github.com/ComposioHQ/composio)

9. **Antfu Skills**
   * *类型*：个人最佳实践 Skills
   * *一句话描述*：前端大牛 Anthony Fu（安哥）的个人 Skill 配置，行业顶尖高手怎么写核心规则的教科书级示范。
   * *直链*：[antfu/dotfiles](https://github.com/antfu/dotfiles) *(或对应技能配置)*

10. **Awesome Agent Skills**
    * *类型*：Skills 索引百科
    * *一句话描述*：收录了 500+ 各大厂及开源社区优质 Skills 的超级索引目录。
    * *直链*：[awesome-agent-skills](https://github.com/indexing/awesome-agent-skills) *(或相关聚合库)*
