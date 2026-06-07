# Windows 环境下 Codex (AI 编程助手) 深度使用与进阶指南

本手册旨在指导 Windows 用户如何高效配置和使用基于 Codex/LLM 的编程助手（如 GitHub Copilot, Gemini Code Assist 等），并整合了工业级的 Skills 扩展，以提升工程化能力。

## 1. 环境准备与基础配置

### 1.1 推荐工具链
- **IDE**: Visual Studio Code (VS Code) —— 目前插件生态最完善。
- **核心插件**: 
    - GitHub Copilot / Gemini Code Assist
    - **Copilot Chat**: 开启对话式编程。
- **Windows 增强**: 安装 [PowerToys](https://github.com/microsoft/PowerToys)，利用其“文本提取器”和“粘贴为纯文本”功能配合 AI 输入。

### 1.2 基础使用技巧
- **行内补全 (Inline Suggestion)**: 输入代码或注释，按下 `Tab` 采纳，`Alt + ]` 切换下一个建议。
- **自然语言转代码**: 在注释中描述逻辑（例如：`// 使用 C# 写一个读取桌面文件并上传到服务器的函数`），AI 会自动生成。
- **快捷命令 (Slash Commands)**: 在 Chat 面板中使用 `/fix` (修复代码), `/tests` (生成测试), `/explain` (解释代码)。

---

## 1.5 如何“安装”下文提到的 Skills？

这些 Skills 并非全部是 VS Code 插件，请根据下表方式启用：

| Skill 类型 | 安装/启用方法 | 适用场景 |
| :--- | :--- | :--- |
| **自定义指令** | 进入 VS Code 设置 -> 搜索 `Custom Instructions` -> 粘贴对应的 Skill 提示词 | 全局行为改变（如 Superpowers） |
| **项目规则文件** | 在项目根目录创建 `.cursorrules` 或 `.github/copilot-instructions.md` | 特定项目的代码风格约束（如 Antfu Skills） |
| **工作流文件** | 手动创建 `PLAN.md` 或 `TODO.md` 并在对话时用 `@` 引用 | 复杂逻辑的长时记忆（如 Planning with Files） |
| **开源框架** | 通过 Python/Node.js 环境 `pip install` 或 `npm install` | 需要调用外部 API 或工具（如 Composio） |

---

## 2. 核心进阶：Codex 必装十大 Skills 指南

为了让 Codex 从一个“代码补全器”变成“资深架构师”，建议在你的工作流中引入以下 Skills：

### 2.1 工程质量与流程控制类
1. **Superpowers (TDD 强化)**:
   - **用法**: 强制要求 AI 先写单元测试再写业务代码。
   - **启用**: 在自定义指令中加入：“You are an expert developer. You MUST always follow TDD: write a failing test first, then the minimal code to pass it.”
2. **SuperClaude Framework (斜杠命令集)**:
   - **描述**: 预设 30+ 条高频命令（如 `/optimize`, `/refactor`）。
   - **启用**: 复制开源社区提供的 Prompts 模板，存入 VS Code 的 `User Snippets` 或 Chat 预设指令中。
3. **Vercel Agent Skills (前端性能准则)**:
   - **启用**: 在项目根目录创建 `.cursorrules`，写入 Vercel 官方的 React 最佳实践文档链接或内容。

### 2.2 上下文与记忆管理类
4. **Planning with Files (长期记忆库)**:
   - **方法**: 在项目根目录建立一个 `TODO.md` 或 `PLAN.md`。
   - **技巧**: 每次开始新功能前，让 Codex 先读取该文件：“根据 @PLAN.md 的进度，执行下一步任务”。
5. **Context Engineering Skills (上下文压缩)**:
   - **核心**: 避免 Token 溢出。在长对话中，使用“总结当前进度并开启新会话”的方式保持 AI 清醒。
6. **Antfu Skills (风格化规则)**:
   - **启用**: 访问 `github.com/antfu/dotfiles` 复制其规则内容至你的项目配置文件中。

### 2.3 自动化与外部联动类
7. **Composio Skills (SaaS 插件化)**:
   - **功能**: 让 AI 具备调用外部工具（GitHub API, Slack, 本地 Shell）的能力。
   - **安装**: 这是一个真实的库，需执行 `pip install composio_core` 并按照官网文档连接你的 GitHub 账号。
8. **MiniMax Skills (全栈模版包)**:
   - **价值**: 提供现成的工业级前端/移动端代码块，减少重复起步工作。
9. **Anthropic/Official Skills (官方示范)**:
   - **学习**: 参考官方的 `skill-creator` 文档，学习如何定义自己的函数调用（Tool Use）。
10. **Awesome Agent Skills (索引百科)**:
    - **作用**: 遇到复杂垂直领域需求时，去该索引寻找特定领域的 Skill 配置。

---

## 3. Windows 专属自动化场景

### 3.1 PowerShell 脚本助手
Codex 对 PowerShell 的支持极佳。
- **需求**: “写一个 PowerShell 脚本，递归扫描 D 盘下超过 100MB 的临时文件并输出列表”。
- **提示**: 在 Windows Terminal 中使用终端 AI 扩展，可以直接将生成的命令填入命令行。

### 3.2 自定义 Windows 自动化 (AutoHotkey + Codex)
- **场景**: 利用 Codex 编写 AutoHotkey (AHK) 脚本，实现“按下 F8 自动将剪贴板内容重构为 Markdown 表格”。
- **代码示例**:
  ```autohotkey
  ; 向 Codex 提问：写一个 AHK 脚本，调用 API 润色选中的文字
  ```

---

## 4. 最佳实践建议

1. **明确上下文 (Context is King)**: 始终保持相关文件处于打开状态，或使用 `@file` 明确引用，这是 Windows 开发环境下避免 AI 幻觉的最有效手段。
2. **小步快跑**: 不要让 AI 一次写 500 行代码。拆解为“定义接口 -> 实现逻辑 -> 编写测试”三步走。
3. **定期清理上下文**: 发现 AI 开始胡言乱语时，点击“New Chat”并提供当前最新的代码片段作为起点。

---
*更多关于 AI 实战的路线图，请参考本目录下的 AI Agent & 大模型开源项目学习参考资料github.md*