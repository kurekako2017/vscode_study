# GitHub 网站工具与热门项目学习地图

> 合并整理自 `github网站工具推荐.md` 与 `GitHub_AI_Tools_Comprehensive_Material.md`，目标是把零散收藏整理成一份可直接检索、可直接学习、可直接复用的 GitHub 工具地图。
>
> 使用建议：
> - 先看“快速选型表”，按目标找工具。
> - 再看对应分类，了解它解决什么问题。
> - 最后结合项目 README、目录结构和启动方式做二次筛选。

## 1. 快速选型表

| 学习目标 | 优先查看 | 重点理解 |
| --- | --- | --- |
| AI Agent 入门 | AutoGPT、browser-use、UI-TARS、Hermes Agent、DeerFlow 2.0 | 任务规划、工具调用、浏览器控制、多智能体协作 |
| AI 编程助手 | Claude Code 文档、AI-Coding-Guide-Zh、gpt-codex、OpenCode、Cursor | Prompt、上下文管理、代码修改流程、验证流程 |
| 语音/视频/字幕处理 | Voice-Pro、Clypra、Toonflow、AI Video Translator、NeMo、Riva | ASR、翻译、TTS、字幕生成、模型推理 |
| 网页抓取与自动化 | Scrapling、browser-use、Public APIs | 爬虫、浏览器自动化、数据源整理 |
| 开源 UI 组件与界面灵感 | Galaxy、Figma、GitHub Pages、Vercel、Netlify | 组件复用、页面布局、设计系统、作品集展示 |
| 模型部署 | Triton Inference Server、NGC、NeMo | 模型服务、GPU 推理、容器化部署 |
| 前端和作品集 | GitHub Pages、Vercel、Netlify、Figma | 静态站点、Next.js 部署、UI 原型 |
| DevOps | GitHub Actions、Docker、Kubernetes 示例项目 | CI/CD、镜像构建、部署、日志监控 |
| 资源检索 | awesome、Awesome-AI、awesome-chinese-ai-agents | 用索引型仓库找到更多项目 |

## 2. AI 编程助手与智能体开发框架

这一类工具专注于自动化代码编写、全库重构、多 Agent 协同、桌面/浏览器控制，是当前 AI 应用最核心的能力层。

### 工具清单

| 工具 / 项目 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Claude Code | https://github.com/anthropics/claude-code | Anthropic 官方终端 AI 编程助手 | 上下文管理、代码修改、测试验证、Git 工作流 |
| Cursor | https://github.com/getcursor/cursor | AI 集成开发环境 | 代码补全、智能聊天、行内生成、全库索引 |
| OpenCode | https://github.com/opencode-ai/opencode | 开源私有化 Coding Agent | 本地私有化部署、代码隐私、替代型编程助手 |
| OpenClaw | https://github.com/openclaw/openclaw | 通用 AI Agent 开源框架 | 高自主权 Agent、多工具调用、本地或自托管 |
| Molili (茉莉) | https://github.com/molili-ai/molili | OpenClaw 本土化替代版本 | 中文交互、一键安装、国内模型适配 |
| DeerFlow 2.0 | https://github.com/bytedance/deerflow | 字节跳动开源超级 AI 员工框架 | sub-agents、skills、跨模态任务编排 |
| OpenHarness | https://github.com/tjb-tech/openharness | 全能型 AI 编程与运行时助手框架 | Memory Runtime、行为编排、扩展式交互 |
| Odysseus | https://github.com/pewdiepie/odysseus | 极简本地 AI Agent | 轻量套壳、本地化自动化、极简交互 |
| AutoGPT | https://github.com/significant-gravitas/autogpt | 经典自治式 Agent 项目 | 目标驱动、任务拆解、工具调用、记忆机制 |
| browser-use | https://github.com/browser-use/browser-use | AI 控制浏览器的自动化项目 | 浏览器动作、页面观察、Web 自动化 |
| UI-TARS Desktop | https://github.com/bytedance/UI-TARS-desktop | 桌面 GUI Agent 工具 | 多模态 Agent、桌面操作、视觉理解 |
| Hermes Agent | https://github.com/NousResearch/hermes-agent | Agent 研究与实现项目 | Agent 框架、工具编排、模型调用 |
| agency-agents | https://github.com/msitarzewski/agency-agents | 多智能体协作示例 | 角色分工、Agent 间通信、任务协作 |
| Zeroclaw | https://github.com/zeroclaw-labs/zeroclaw | 本地 AI 助手基础设施 | 本地助手、工具接入、跨平台运行 |
| Agentic Design Patterns 中文翻译 | https://github.com/xindoo/Agentic-Design-Patterns-CN | 智能体设计模式中文百科指南 | 路由、规划、协作、记忆管理、知识检索 |
| oh-my-pi | https://github.com/can1357/oh-my-pi | 面向终端的 AI 编码与跨语言补全工具 | LSP 集成、深度浏览、子代理控制 |

### 学习时重点看这些层

- 入口层：CLI、Web UI、API 路由，负责接收用户任务。
- Planner 层：把目标拆成步骤。
- Tool 层：浏览器、文件、Shell、API 等外部能力。
- Memory / State 层：保存上下文、执行结果、历史信息。
- Executor 层：实际执行动作并处理失败重试。

## 3. 办公协同与特定软件生态 AI 智能体

此类智能体深度融入国内企业既有的办公、社交与操作系统生态，主打免开发、开箱即用或低代码快速集成。

| 产品名称 | 核心定位 | 功能特征描述 |
| :--- | :--- | :--- |
| WorkBuddy | 企业微信 AI Agent | 企业级数据安全保障、企微生态深度集成、支持全链路合规审计。 |
| QClaw | 微信生态个人 AI 助手 | 微信直连交互、支持远程控制电脑、数据完全保存在本地、拥有高免费额度。 |
| JVSClaw | 云端托管 AI 智能体 | 支持云端全托管运行与手机 App 接入，主打“零代码”快速上手。 |
| ArkClaw | 飞书生态 AI Agent | 与飞书办公流和多维表格深度集成，工作流处理能力强，长于团队内容分发。 |
| KimiClaw | 长文档分析 AI Agent | 专门针对超长文本处理进行优化，支持 200 万字级别上下文分析，多用于云端托管。 |
| MaxClaw | 多模态长文本 AI Agent | 具备超长记忆力，完美融合“图-文-音”多模态输入，专为自媒体创作者设计。 |
| CoPaw | 钉钉生态开发型 AI Agent | 具备强大的自动化和代码扩展能力，与钉钉深度集成且完全开源免费。 |
| AutoClaw | 零门槛本地部署 AI Agent | 国内自主可控，专注于本地长文本敏感数据分析与本地私有化大模型推理。 |
| 小艺Claw (LiteClaw) | 鸿蒙端侧 AI Agent | 运行于 HarmonyOS 移动端侧，支持多端协同与极致的端侧隐私保护。 |

## 4. AI 编程与代码学习工具

| 工具 / 文档 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Claude Code 最佳实践 | https://code.claude.com/docs/zh-CN/best-practices | AI 编码协作官方实践文档 | 上下文管理、验证、权限、hooks、skills、subagents |
| AI-Coding-Guide-Zh | https://github.com/KimYx0207/AI-Coding-Guide-Zh | 中文 AI Coding 指南集合 | Prompt、工具对比、编码工作流 |
| gpt-codex | https://github.com/xianyu110/gpt-codex | AI 编码辅助相关仓库 | 代码生成、编辑流程、自动化脚本 |
| Claude-CLI 非官方工具 | https://github.com/kiliczsh/claude-cmd | 在终端中调用 Claude 的命令行工具 | CLI 工具设计、终端交互、模型调用 |
| Open-Lovable | https://github.com/firecrawl/open-lovable | AI 应用生成和辅助开发相关项目 | 从需求到界面的 AI 开发流程 |
| Awesome LLM Apps | https://github.com/theunwindai/awesome-llm-apps | AI 应用落地实战案例与教程合集 | LLM、RAG、AI Agents、Voice Agents 实战 |
| ai-engineering-from-scratch | https://github.com/rohitg00/ai-engineering-from-scratch | 从零构建 AI 工程项目的实战指南 | 从底层原理到企业级 AI 应用交付 |

### 代码学习心得

- Prompt 不是简单提问，而是把目标、上下文、约束、验证方式交给模型。
- AI 编程工具的核心不是替你写完代码，而是帮助你更快完成“理解、修改、运行、验证、总结”。
- 真正适合项目现场的 AI 编码流程，一定要包含测试、代码审查、日志和回滚意识。

## 5. 多媒体、语音、视频与字幕 AI

这一类工具适合学习 ASR、翻译、TTS、字幕生成、视频处理和多模型流水线。

| 工具 / 项目 | 链接 | 是什么 | 核心作用 | 适合学习 |
| --- | --- | --- | --- | --- |
| Voice-Pro | https://github.com/abus-aikorea/voice-pro | 本地运行的 Gradio WebUI 多媒体处理工具 | 视频下载、语音识别、翻译、字幕、TTS、语音克隆等流程整合 | Whisper、Faster-Whisper、字幕处理、Gradio Web 应用、多媒体流水线 |
| Clypra | https://github.com/clypra/clypra | 基于 Tauri + React + TypeScript 的现代化视频编辑器 | 替代 CapCut / 剪映 Pro 的本地视频剪辑能力 | 多轨时间线、帧级编辑、FFmpeg、桌面应用结构 |
| MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | 基于大模型的自动化高清短视频生成工具 | 自动脚本、素材搜集、配音、字幕、成片输出 | 自媒体视频流水线、内容自动生成 |
| Toonflow | https://github.com/tooflow-ai/toonflow | AI 漫剧与短剧自动化制作工具 | 分镜、渲染、合成一体化 | Node.js、Electron、Docker、自动化短剧制作 |
| html-video | https://github.com/nesa-io/html-video | 基于 HTML 渲染的视频生成引擎 | 让 HTML 变成视频，支持模板和多 Agent 后端 | 模板化视频、渲染引擎、自动化生成 |
| AI Video Translator | https://github.com/video-parallel-translator/video-translator | 智能视频搬运翻译工具 | 下载、转写、翻译、声音克隆、音轨替换 | 视频出海、跨语种处理、音视频链路 |
| NVIDIA NeMo | https://github.com/NVIDIA/NeMo | NVIDIA AI 模型训练与推理工具包 | 语音、NLP、LLM 相关模型训练和推理 | ASR、TTS、模型微调、深度学习工程结构 |
| NVIDIA Riva | https://developer.nvidia.com/riva | NVIDIA 语音和语言 AI 服务平台 | 把 ASR、TTS、NLP 部署成实时服务 | 语音服务化、GPU 推理、生产级部署 |

### Voice-Pro 学习定位

- 前端层：Gradio 页面，负责上传文件、选择功能、展示结果。
- 处理层：调用语音识别、翻译、TTS、字幕等模块。
- 模型层：底层依赖 Whisper / Faster-Whisper / TTS / 翻译模型等能力。
- 文件层：输入视频或音频，输出字幕、音频、翻译文本或处理后的视频。

### 阅读 Voice-Pro 时重点看

- README 的安装方式和功能说明。
- Gradio app 的入口文件。
- 语音识别、翻译、TTS、字幕处理相关模块。
- 模型下载目录、配置项、输出目录。

## 6. 抓取、数据与 API

| 工具 / 项目 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Scrapling | https://github.com/D4Vinci/Scrapling | 自适应 Web 抓取框架 | 爬虫、反爬适配、HTML 解析、批量采集 |
| browser-use | https://github.com/browser-use/browser-use | AI 浏览器自动化工具 | 自动访问网页、点击、读取页面、执行任务 |
| Public APIs | https://github.com/public-apis/public-apis | 公共 API 目录 | 找数据源、练习 API 调用、做 Demo 项目 |

### 学习重点

- Requests / HTTP 层：怎么请求网页或 API。
- Parser 层：怎么从 HTML / JSON 中抽取数据。
- Scheduler 层：怎么批量处理多个 URL 或任务。
- Storage 层：怎么保存 CSV、JSON、数据库数据。
- Browser 层：动态网页需要浏览器自动化工具参与。

## 7. 模型部署、GPU 与平台工具

| 工具 / 平台 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Triton Inference Server | https://github.com/triton-inference-server/server | NVIDIA 高性能模型推理服务器 | 模型服务、HTTP/gRPC 推理、多模型部署、GPU 批处理 |
| NGC Catalog | https://catalog.ngc.nvidia.com/ | NVIDIA 模型、容器、镜像目录 | 查找官方优化容器和预训练模型 |
| NeMo | https://github.com/NVIDIA/NeMo | 模型训练与推理工具包 | 从训练、微调到部署的工程流程 |

### 学习重点

- Model Repository：模型文件和配置如何组织。
- Inference API：客户端如何通过 HTTP / gRPC 调用模型。
- Batch / Queue：服务端如何提高吞吐量。
- Container：为什么生产环境常用 Docker 镜像部署模型。
- Monitoring：如何观察延迟、吞吐量、GPU 使用率和错误日志。

## 8. 开发环境、作品集与设计工具

| 工具 / 平台 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Galaxy | https://github.com/uiverse-io/galaxy | 开源 UI 组件库和界面灵感站点 | 组件分类、页面片段复用、设计系统、前端审美 |
| GitHub Pages | https://pages.github.com/ | GitHub 静态网站托管 | 发布学习笔记、作品集、项目文档 |
| Vercel | https://vercel.com/ | 前端和 Next.js 部署平台 | Next.js 部署、预览环境、环境变量 |
| Netlify | https://www.netlify.com/ | 静态站点和前端部署平台 | React / Vue 静态部署、表单、预览 |
| Figma | https://www.figma.com/ | UI 设计和原型协作工具 | 页面设计、组件设计、作品集展示 |
| Warp | https://www.warp.dev/ | 现代终端工具 | 命令管理、终端工作流、AI 辅助命令 |
| GitNexus | https://github.com/abhigyanpatwari/GitNexus | 项目知识图谱工具 | 理解代码仓库结构、项目关系和知识管理 |
| CodeGraph | https://github.com/colbymchenry/codegraph | 本地预索引代码知识图谱工具 | 代码结构索引、符号关系、调用链分析、AI 编程工具集成 |

### 建议用法

- GitHub Pages：放静态学习文档和作品集。
- Vercel / Netlify：部署 Next.js、React、Vue 项目。
- Figma：先画页面流程，再实现前端。
- GitNexus：辅助理解复杂仓库结构，但要注意许可证和商用限制。

## 9. 资源索引与 Awesome 仓库

| 项目 | 链接 | 是什么 | 怎么用 |
| --- | --- | --- | --- |
| awesome | https://github.com/sindresorhus/awesome | Awesome 系列总入口 | 找各技术方向的优秀项目合集 |
| Awesome-AI | https://github.com/cssmagic/Awesome-AI | AI 资源集合 | 查 AI 工具、模型、文章、教程 |
| awesome-chinese-ai-agents | https://github.com/happydog-intj/awesome-chinese-ai-agents | 中文 AI Agent 资源索引 | 找中文社区 Agent 项目 |
| awesome-llvm | https://github.com/learn-llvm/awesome-llvm | LLVM 资源索引 | 学编译器、底层、LLVM 工具链 |
| Google AI Edge Gallery | https://github.com/google-ai-edge/gallery | Google 边缘 AI 示例集合 | 学移动端、边缘端 AI 示例 |

### 使用方法

- 先用 Awesome 仓库找方向。
- 再挑 1 到 2 个真实项目跑起来。
- 最后把项目结构、启动命令、核心流程写入自己的学习笔记。

## 10. 金融与量化工具

| 工具 / 项目 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| Kronos | https://github.com/tsinghua-quant/kronos | 全球首款 K 线金融大模型 | 金融蜡烛图、预训练、微调、多周期预测 |
| TradingAgents | https://github.com/rotquant/TradingAgents | 多 Agent 架构的 LLM 金融交易框架 | 宏观新闻分析、微观数据追踪、买卖决策模拟 |
| AI-Trader | https://github.com/quant-agent/AI-Trader | 100% 全自动 Agent 原生交易系统 | 自动交易链路、量化执行 |
| Vibe-Trading | https://github.com/vibe-quant/Vibe-Trading | 面向个人投资者的轻量交易 Agent 系统 | 场景化交易、个人投资者工具 |
| tensortrade | https://github.com/tensortrade-org/tensortrade | 基于深度强化学习的交易及资产评估框架 | 强化学习交易、回测、评估 |
| QuantDinger | https://github.com/quantdinger/QuantDinger | 多 Agent 量化分析平台 | 加密货币、股票、外汇分析 |
| OpenAlice | https://github.com/openalice/OpenAlice | 跨市场 AI 交易 Agent | 股票、期货、商品等多资产交易 |
| Polymarket agents | https://github.com/polymarket-share/polymarket-agents | Polymarket 预测市场交易智能体 | 对冲、套利、预测市场 |
| AutoHedge | https://github.com/autohedge/AutoHedge | 自主对冲基金系统 | 群体智能、自动化执行 |
| TradingGym | https://github.com/tradinggym/TradingGym | 交易 Agent 强化学习与回测沙盒 | RL 微调、仿真环境、策略验证 |

### 注意

- 金融类项目适合学习系统设计和数据处理，不建议直接用于真实投资。
- 重点看数据来源、指标计算、回测逻辑、风险控制，而不是只看模型输出。

## 11. 效率、安全、内容治理与提示词辅助

| 工具 / 项目 | 链接 | 是什么 | 适合学习 |
| --- | --- | --- | --- |
| FreeLLMAPI | https://github.com/tashfeenahmed/freellmapi | 免费顶级大模型 Token 聚合工具 | API 路由、免费额度整合、本地开发测试 |
| ECC | https://github.com/affaan-m/ECC | 面向 Claude Code、Codex、OpenCode、Cursor 的性能优化底座 | Agent 性能优化、运行时加速 |
| taste-skill | https://github.com/Leonxlnx/taste-skill | 提升 AI 审美、减少机械感的 Prompt 质量库 | 文案、代码注释、技术表达优化 |
| markitdown | https://github.com/microsoft/markitdown | 微软官方文档转 Markdown 工具 | Office 文档、PDF、图像到 Markdown |
| Anthropic-Cybersecurity-Skills | https://github.com/mukul975/Anthropic-Cybersecurity-Skills | 为 AI Agent 构建的结构化网络安全技能库 | 安全护栏、网络安全技能 |
| stop-slop | https://github.com/hardikpandya/stop-slop | 自动去除 AI 味的 NLP 净化插件 | 让输出更自然、更像真人 |
| headroom | https://github.com/headroom-project/headroom | 长文本上下文与 Token 压缩框架 | 长上下文剪裁、Token 控制 |
| Prompt-Sanitizer | 待补充 | 大模型输入端的数据清洗与质量把控工具 | RAG/Agent 输入净化、结构化提取 |
| Agent-Monitor-SDK | 待补充 | 防止 Agent 线上跑偏的监控守卫 | 幻觉拦截、输出质量监控 |
| Awesome-Vibe-Coding-Tools | 待补充 | AI 时代原生设计的全栈快速交付模版 | 一句话出成品、独立开发脚手架 |
| English-level-up-tips | https://github.com/byoungd/English-level-up-tips | 英语进阶指南（含 AI 辅助章节） | 语言习得、提示词框架 |

## 12. 其他工具与待确认条目

| 条目 | 链接 | 说明 |
| --- | --- | --- |
| FreeDomain | https://github.com/DigitalPlatDev/FreeDomain | 域名或免费资源相关项目，使用前需要确认具体规则和可用性 |
| FMHY | https://fmhy.net/ | 免费资源导航站，内容较杂，适合查资料但要注意来源质量 |
| MAIC Chat | https://open.maic.chat/ | AI 学习和大纲生成工具，可辅助整理学习路线 |
| OpenRelay | 待确认 | 目前可能对应多个不同项目或服务，不建议在工具目录中写死，确认仓库后再补充 |

## 13. 判断一个 GitHub 工具值不值得学

| 判断点 | 怎么看 |
| --- | --- |
| README | 是否说清楚“是什么、怎么安装、怎么运行、有什么示例” |
| 项目结构 | 是否能看出前端、后端、模型、配置、测试、部署目录 |
| 最近维护 | 是否仍有 commit、release、issue 回复 |
| License | 是否允许学习、修改、商用 |
| 最小运行成本 | 是否能在本机、WSL、Docker 或 Codespaces 中跑起来 |
| 学习价值 | 是否能帮助你理解某个框架、系统流程或真实项目结构 |

不要只按 star 数收藏项目。star 多只能说明关注度高，不代表适合当前学习阶段；对你来说，能跑起来、能读懂、能迁移到自己的项目里更重要。

## 14. 工具记录模板

以后追加新工具时，建议统一使用下面格式：

```md
### 工具名

- 链接：
- 是什么：
- 核心作用：
- 适合学习：
- 适合直接使用：
- 技术关键词：
- 项目入口文件或核心目录：
- 注意事项：
```

## 15. 一个实用的学习顺序

- 第一阶段：Git、GitHub、Markdown、README、Issue、PR。
- 第二阶段：React / Vue / Next.js + TypeScript，再结合 Scrapling、browser-use 学网页数据获取与自动化。
- 第三阶段：Voice-Pro、AutoGPT、browser-use、Claude Code 文档，建立 AI 应用与 AI 编程协作的基本链路。
- 第四阶段：GitHub Actions、Docker、DevOps 文档、Triton、NeMo、Riva，理解部署和工程化。
- 第五阶段：金融量化、代码知识图谱、编译器和底层工具，按兴趣做专题深入。
