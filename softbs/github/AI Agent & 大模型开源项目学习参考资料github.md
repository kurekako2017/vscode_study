# AI Agent & 大模型开源项目学习参考资料

> 这是一份偏“学习路线 + 训练手册”的资料，适合和 [GitHub 网站工具与热门项目学习地图](github网站工具推荐.md) 配套使用。
>
> 本资料基于多份前沿 AI Agent 学习路线图、GitHub 热门开源项目榜单以及 Codex 必装技能指南整理而成，目标是给后续的深入学习与项目实战提供一份更顺手的参考。

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
