# AI Agent 学习资源清单（含 GitHub 练习项目）

> 整理时间：2026年6月。按"入门课程 → 框架实战 → 评测练习 → 持续追新"的顺序排列，方便循序渐进地学习并动手练习。

---

## 一、系统课程类（适合入门，边学边敲代码）

### 1. Hugging Face AI Agents Course

- **GitHub 链接**：https://github.com/huggingface/agents-course
- **课程主页**：https://hf.co/learn/agents-course
- **简介**：目前公认最适合入门的智能体课程，从基础概念讲到部署自主智能体，分为 4 个单元，覆盖 smolagents、LlamaIndex、LangGraph 三大主流框架的实际操作。
- **练习内容**：
  - Unit 1：用 smolagents 搭建你的第一个智能体（基础工具调用、ReAct 模式）
  - Unit 2：分别用 smolagents / LlamaIndex / LangGraph 实现同一个任务，对比三种框架的设计思路
  - 最终项目：在 GAIA 基准上构建并评估自己的智能体，完成后可获得官方课程证书
  - 课程提供预配置的 Hugging Face Spaces 环境，免去环境搭建的麻烦
- **适合人群**：完全没接触过 agent 开发的人，免费且互动性强

### 2. Microsoft AI Agents for Beginners

- **GitHub 链接**：https://github.com/microsoft/ai-agents-for-beginners
- **简介**：对新手友好但内容全面的开源课程，共 11 节课，涵盖工具集成、RAG、智能体设计模式、多智能体系统、生产环境部署。
- **练习内容**：
  - 每节课配有 `code_samples` 文件夹，可直接 fork 仓库跑代码练习
  - 涉及 Azure AI Foundry 和 GitHub Model Catalog 的模型调用练习
  - 多智能体协作场景的实战示例
- **亮点**：支持简体中文、繁体中文等多语言翻译，中文资料阅读无障碍
- **适合人群**：希望用中文资料系统学习的人

---

## 二、框架实战类（用真实工具搭智能体）

### 3. Langflow（可视化拖拽搭建）

- **GitHub 链接**：https://github.com/langflow-ai/langflow
- **简介**：目前 Star 数最高的智能体相关项目之一（约 14.6 万星），通过拖拽方式设计 LLM 应用和智能体流程，不需要写太多代码。
- **练习内容**：跟着官方模板搭建一个简单的对话助手，再尝试接入外部 API 做数据查询类智能体
- **适合人群**：想先建立直观理解，不想一开始就写大量代码的人

### 4. Dify（一体化 LLM 应用开发平台）

- **GitHub 链接**：https://github.com/langgenius/dify
- **简介**：约 13.6 万星，自带可视化编排、RAG、Agent 工作流、模型管理等功能，支持自部署。
- **练习内容**：搭建一个客服类智能体，练习知识库挂载（RAG）+ 多轮对话记忆

### 5. CrewAI（多智能体协作框架）

- **GitHub 链接**：https://github.com/crewAIInc/crewAI
- **简介**：专注于让多个智能体分工协作完成复杂任务，强调"角色化"设计（比如设定一个智能体是"研究员"、另一个是"撰写者"）。
- **练习内容**：用官方示例搭建一个"调研 + 写报告"的两智能体团队，练习 task 拆分和智能体间的信息传递

### 6. AutoGen（微软出品，多智能体对话框架）

- **GitHub 链接**：https://github.com/microsoft/autogen
- **简介**：通过智能体之间互相对话的方式完成任务，支持人类介入（human-in-the-loop）。
- **练习内容**：实现一个"代码生成智能体 + 代码审查智能体"的对话循环，体会智能体互相纠错的过程

### 7. Browser-use（网页自动化智能体）

- **GitHub 链接**：https://github.com/browser-use/browser-use
- **简介**：约 8.6 万星，让 AI 智能体像人一样浏览网页——点击、输入、导航、填表。
- **练习内容**：做一个能自动完成"搜索某商品并比价"或"自动填写表单"的智能体，直观又有成就感

---

## 三、评测/练习题型仓库（验证学习成果）

### 8. SWE-bench（真实代码任务评测）

- **GitHub 链接**：https://github.com/SWE-bench/SWE-bench
- **简介**：包含两千多个来自真实 Python 项目的 GitHub issue，要求智能体生成补丁并通过测试，全程在 Docker 环境中运行，完全可复现。
- **练习内容**：挑选 SWE-bench Lite（难度较低的子集）尝试让自己搭建的 coding agent 解决其中几个 issue，对比官方榜单上各模型的通过率

### 9. WebArena（真实网页任务评测）

- **GitHub 链接**：https://github.com/web-arena-x/webarena
- **简介**：自托管的真实网页应用评测环境，包含电商、论坛、内容管理系统（CMS）、代码托管 4 类网站，800 多个长链条任务。
- **练习内容**：部署本地环境后，让你的网页智能体完成"在论坛里发帖并回复指定用户"之类的多步骤任务

---

## 四、汇总型仓库（持续追新案例）

### 10. awesome-agent-learning

- **GitHub 链接**：https://github.com/artnitolog/awesome-agent-learning
- **简介**：持续更新的智能体学习资源导航，整理了课程、阅读清单和各类评测基准，适合学完基础后按需查找新案例。

---

## 建议学习路线

1. **第一周**：跟着 Hugging Face AI Agents Course 的 Unit 1-2，搭建第一个智能体，理解 ReAct 模式
2. **第二周**：用 Langflow 或 Dify 快速搭一个可视化的小项目，建立整体直觉；同时用 CrewAI 或 AutoGen 写一个多智能体协作的代码项目
3. **进阶**：尝试 Browser-use 做一个网页自动化智能体，再用 SWE-bench Lite 检验自己搭建的 coding agent 的实际能力
4. **持续学习**：定期查看 awesome-agent-learning 仓库，跟进新出现的工具和案例

---

*提示：以上 GitHub 链接均为各项目的官方/主仓库地址，建议在使用前先查看仓库的 README 确认最新的安装方式和依赖版本，因为 AI Agent 相关项目迭代很快。*
