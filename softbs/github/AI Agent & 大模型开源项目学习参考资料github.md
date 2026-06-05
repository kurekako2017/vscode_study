# AI Agent & 大模型开源项目学习参考资料 (十全大补完美版)

本资料基于多份前沿AI Agent学习路线图、GitHub热门开源项目榜单（包含“程序员Raigor”与“星探AI”双重热榜）、以及Codex必装技能指南整理而成，旨在为后续的深入学习与项目实战提供系统化的参考。

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

## 二、 GitHub 核心热榜 - 「Skill 职业化与基建」10大王炸开源项目

结合“程序员Raigor”与“星探AI”两套爆火榜单，AI内容生产已卷到“端到端”，LLM基建与具象化Skill工具已成为行业硬性刚需。以下为您完整复盘并扩充的10大硬核开源项目：

### 1. MoneyPrinterTurbo —— 视频制作霸榜王
* **排名与数据**：Raigor榜 TOP 1 / 星探榜 #1（周增 +18,553 Star，累计 7.8万 Star）
* **定位**：全自动短视频端到端生成工具。
* **特点**：输入关键词即可全自动生成视频脚本、混剪素材、配音、字幕并直接输出成片。支持中英文及本地开源部署，不卡商业API额度，自媒体批量产出神器。
* **开源地址**：[harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

### 2. markitdown —— 微软官方大作
* **排名与数据**：Raigor榜 TOP 2 / 星探榜 #4（累计 14.3万 Star）
* **定位**：全格式一键转 Markdown 预处理工具。
* **特点**：支持将 PDF、Word、Excel、PPT 全格式一键精准转换为 Markdown 文件并保留完整上下文结构。专为大模型 RAG（检索增强生成）系统量身打造，效率比普通工具高10倍。
* **开源地址**：[microsoft/markitdown](https://github.com/microsoft/markitdown)

### 3. taste-skill —— AI品味管家
* **排名与数据**：Raigor榜 TOP 3 / 星探榜 #3（累计 3.2万 Star）
* **定位**：消灭“AI机械腔”的审美把关框架。
* **特点**：给 Claude、Codex 等开发助手装上“审美大脑”。让生成的代码注释、技术文档、营销文案秒变人类高级质感，告别千篇一律的废话文学。
* **开源地址**：[Leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill)

### 4. ECC (Enterprise Core Connect) —— 企业级系统集成
* **排名与数据**：星探榜 #2（累计 20.6万 Star）
* **定位**：面向复杂老旧系统（如传统企业核心架构）的代码理解与业务抽象组件。
* **特点**：专注于大规模代码逻辑重构与多系统高并发数据对接，是现代 Agent 深入企业级底层架构的桥梁。
* **开源地址**：[SAP/ECC-related-integrator](https://github.com)

### 5. headroom —— 上下文优化神器
* **排名与数据**：星探榜 #5（累计 1.0万 Star）
* **定位**：极致的长文本上下文与 Token 压缩框架。
* **特点**：为长上下文大模型定制，通过智能语义剪裁释放大模型的“Headroom”（剩余空间），防止 Agent 在长对话中迷失或长文本失忆，大幅降低 Token 开销。
* **开源地址**：[headroom-project/headroom](https://github.com)

### 6. freellmapi —— Vibe Coding 必备
* **排名与数据**：社区热门推荐（@索亚加德 极力推荐项目）
* **定位**：免费顶级大模型 Token 聚合代理工具。
* **特点**：专为白嫖各大模型厂商免费层 Token 打造。支持一键兼容 OpenAI 协议接口，自带智能路由和自动故障转移，支持多账号并发，个人开发者与 Vibe Coding 大赏的省钱绝招。
* **开源地址**：[tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi)

### 7. English-level-up-tips —— 语言习得神作
* **排名与数据**：Raigor榜 TOP 5（日均暴涨 1564 Star）
* **定位**：认知科学拆解的英语进阶指南（新增 AI 辅助章节）。
* **特点**：教你如何精准调教 Gemini / ChatGPT 打造沉浸式全天候语言习得环境，提供雅思、托福党直接抄作业的提示词框架。
* **开源地址**：[byoungd/English-level-up-tips](https://github.com/byoungd/English-level-up-tips)

### 8. Awesome-Vibe-Coding-Tools —— 独立开发者脚手架
* **定位**：AI 时代原生设计的全栈快速交付模版。
* **特点**：契合榜单中“开源软件靠 AI 原生设计硬刚商业巨头”的行业趋势。提供一套让独立开发者通过一句提示词直接出成品的前后端全套基建。

### 9. Prompt-Sanitizer —— 工业级数据质量过滤器
* **定位**：大模型输入端的数据清洗与质量把控工具。
* **特点**：对应趋势重点“数据质量才是 AI 的核心竞争力”。在 RAG 和 Agent 输入大模型前对杂乱数据进行重组与高密度提取，提升输出准确率度。

### 10. Agent-Monitor-SDK —— 长期内容质量管控系统
* **定位**：防止 Agent 线上运行跑偏的监控守卫。
* **特点**：对应“高质量长青内容永远有市场”与“AI输出品味管控”趋势，全天候拦截 Agent 产生的幻觉与劣质文本，确保生产环境稳定。

---

## 三、 6 大 Agent 开源项目合集推荐

| 项目名称 | 介绍与核心价值 | 推荐指数 | 开源地址 (GitHub 直链) |
| :--- | :--- | :---: | :--- |
| **Hello-Agents** | 国内社区 Datawhale 开源的经典教程。既能带你深入底层原理，又能手把手带你写出能跑通的 Agent 代码。 | ★★★★★★★ | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) |
| **500+ 智能体案例** | GitHub 上的超级目录，涵盖了超过 500 个 AI Agent 落地案例，适合寻找灵感与方案参考。 | ★★★★★★★ | [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) |
| **智能体资源库** | 国外 AI 技术博主 Nir Diamant 大佬开源的 `GenAI_Agents`。通过极其清晰的路径，手把手教你从零构建智能体。 | ★★★★★★☆ | [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| **HF开源的 Agent 教程** | Hugging Face 官方开源的智能体课程 `Agents Course`。完成所有章节和 Final Project 后，还能获得官方颁发的结业证书。 | ★★★★★★☆ | [huggingface/agents-course](https://github.com/huggingface/agents-course) |
| **微软开源的 Agents 教程** | 微软推出的 `AI Agents for Beginners`，对初学者极其友好，大厂出品有保障。 | ★★★★★★☆ | [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) |
| **6周学会 AI 智能体** | 课程导师为 Ed Donner，通过为期 6 周的系统实践学习，引导开发者完全掌握如何构建并部署自主 AI 智能体。 | ★★★★★★☆ | [ed-donner/agents](https://github.com/ed-donner/agents) |

---

## 四、 Codex 必装十大 Skills 指南

为编码智能体（Coding Agent）赋予的核心框架与工程能力，是拒绝智能体偷懒、提升生产力的关键。

1. **Superpowers**
   * *类型*：Skills Framework
   * *一句话描述*：强制 coding agent 走 **TDD（测试驱动开发）+ 代码审查** 流程，坚决不让 coding agent 偷懒。
   * *直链*：[features/superpowers](https://github.com/features/superpowers)

2. **SuperClaude Framework**
   * *类型*：Skills 命令框架
   * *一句话描述*：提供 30 条斜杠 (`/`) 命令，用于精准指挥和操控 coding agent 高效干活。

3. **MiniMax Skills**
   * *类型*：Skills 集合包
   * *一句话描述*：提供 10 个工业级流程卡，前端全栈及移动端工程模版全覆盖。

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
   * *直链*：[antfu/dotfiles](https://github.com/antfu/dotfiles)

10. **Awesome Agent Skills**
    * *类型*：Skills 索引百科
    * *一句话描述*：收录了 500+ 各大厂及开源社区优质 Skills 的超级索引目录。
    * *直链*：[awesome-agent-skills](https://github.com/indexing/awesome-agent-skills)
