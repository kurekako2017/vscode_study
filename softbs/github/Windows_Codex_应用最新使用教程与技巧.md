# Windows 下 Codex 应用最新使用教程与使用技巧

> 适用对象：Windows 11 / Windows 10 用户，主要用于 VS Code / WSL / GitHub / Python / 前后端项目开发，也包含文档、数据分析、自动化任务的用法。
>
> 更新时间：2026-06-07

---

## 1. Codex 现在到底有几种用法？

在 Windows 上，Codex 主要有 3 种入口：

| 入口 | 适合场景 | 推荐程度 |
|---|---|---|
| **Codex Windows 应用** | 多项目管理、并行 agent、review 代码、使用插件/skills、自动化 | ⭐⭐⭐⭐⭐ |
| **Codex CLI** | 在终端里直接让 Codex 改代码、跑测试、查问题 | ⭐⭐⭐⭐ |
| **Codex IDE 插件** | 在 VS Code / Cursor / JetBrains 里边看代码边让 Codex 修改 | ⭐⭐⭐⭐⭐ |

我的建议：

- **主力用 Codex Windows 应用 + VS Code 插件**。
- 如果项目在 WSL 里，比如 Ubuntu 的 `/home/xxx/project`，优先配合 **WSL2 + VS Code Remote WSL**。
- 如果只是快速改一个目录里的文件，用 **Codex CLI** 也很方便。

---

## 2. Windows 环境准备

### 2.1 推荐系统

优先使用：

- Windows 11：推荐。
- Windows 10：可以用，但需要较新的版本，稳定性不如 Windows 11。
- 老版本 Windows 10：不推荐，容易出现 sandbox、终端、权限问题。

### 2.2 必装基础工具

建议先安装这些：

| 工具 | 用途 | 是否必装 |
|---|---|---|
| **Git for Windows** | 版本管理、让 Codex 能看 diff / commit / branch | 必装 |
| **VS Code** | 主力编辑器 | 必装 |
| **Windows Terminal** | 比默认 cmd 好用很多 | 推荐 |
| **WSL2 + Ubuntu** | Linux 开发环境，适合 Node/Python/后端项目 | 强烈推荐 |
| **Node.js LTS** | 前端 / TypeScript / npm 工具链 | 看项目 |
| **Python 3.11+ / 3.12+** | Python 项目、脚本自动化、数据分析 | 看项目 |
| **Docker Desktop** | 容器、数据库、本地服务 | 看项目 |
| **GitHub CLI (`gh`)** | PR、Issue、repo 操作自动化 | 推荐 |

---

## 3. 安装 Codex Windows 应用

### 方法 1：Microsoft Store 安装

1. 打开 Microsoft Store。
2. 搜索 **Codex**。
3. 发行方确认是 **OpenAI**。
4. 点击安装。
5. 打开后用 ChatGPT 账号登录。

### 方法 2：命令行安装

在 PowerShell 中运行：

```powershell
winget install Codex -s msstore
```

如果 `winget` 不存在，需要先更新 Windows 或安装 Windows Package Manager。

---

## 4. 安装 Codex CLI

### 4.1 Windows 原生命令安装

在 PowerShell 中运行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

安装完成后：

```powershell
codex
```

第一次运行会要求登录 ChatGPT 账号或使用 OpenAI API Key。

### 4.2 npm 安装方式

如果你已经有 Node.js：

```powershell
npm install -g @openai/codex
codex
```

### 4.3 WSL2 内安装

如果你的项目主要在 WSL 里，推荐在 WSL 里面也安装一份 Codex CLI。

先在 PowerShell 管理员模式安装 WSL：

```powershell
wsl --install
```

进入 WSL：

```powershell
wsl
```

然后在 Ubuntu 里运行：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex
```

---

## 5. Windows 原生模式 vs WSL2 模式怎么选？

| 场景 | 推荐模式 |
|---|---|
| 项目在 `C:\Users\xxx\project` | Windows 原生 Codex |
| 项目在 `\\wsl$\Ubuntu\home\xxx\project` | WSL2 模式 |
| Node/Python/Linux 后端项目 | WSL2 更舒服 |
| C# / .NET / Windows 桌面项目 | Windows 原生更合适 |
| 需要 Docker/Linux 命令 | WSL2 更合适 |
| 只是修改文档、脚本、小工具 | Windows 原生即可 |

### 重要建议

不要把 WSL 项目放在 `C:\` 下面反复访问。更推荐：

```bash
/home/你的用户名/code/项目名
```

然后在 WSL 终端里：

```bash
cd ~/code/your-project
code .
```

这样 VS Code 会以 WSL Remote 模式打开，终端、依赖、路径都更稳定。

---

## 6. Codex Windows 应用基本用法

### 6.1 添加项目

1. 打开 Codex 应用。
2. 点击 **Add project** 或类似入口。
3. 选择项目目录。
4. 如果项目在 WSL 中，可以在文件选择器输入：

```text
\\wsl$\
```

然后进入你的 Ubuntu 目录。

### 6.2 第一次让 Codex 看项目

推荐先不要直接让它大改代码，先让它理解项目：

```text
请先阅读这个项目，不要修改任何文件。
请说明：
1. 项目技术栈
2. 主要目录结构
3. 启动命令
4. 测试命令
5. 当前最适合让你处理的任务类型
```

### 6.3 开始修改代码

好的任务写法：

```text
请修复登录页面手机号校验的问题。
要求：
1. 只修改与登录表单相关的文件
2. 不要改 UI 风格
3. 增加或更新相关测试
4. 修改完成后运行测试
5. 最后给我总结改了哪些文件、为什么这样改
```

不好的写法：

```text
帮我优化一下项目
```

这个太大，Codex 容易乱跑、耗额度、改太多。

---

## 7. Sandbox 和权限怎么理解？

Codex 在 Windows 原生模式下可以用 Windows sandbox。作用是限制 Codex：

- 默认只能在项目目录里读写。
- 访问项目外目录时需要权限。
- 需要联网、安装依赖、执行危险命令时应先询问你。

### 推荐设置

新手建议：

- 使用默认 sandbox 权限。
- 不要随便开 Full access。
- 让 Codex 每次执行删除、安装、联网、数据库操作前先说明。

可以对 Codex 说：

```text
除非我明确允许，否则不要执行 rm、删除文件、重置 git、安装全局依赖、修改系统配置、访问项目外目录。
```

如果 Codex 需要读取项目外目录，可以使用：

```text
/sandbox-add-read-dir C:\absolute\directory\path
```

---

## 8. VS Code 中如何配合 Codex

### 8.1 推荐插件

| 插件 | 用途 |
|---|---|
| **Codex IDE extension** | 在 VS Code 侧边栏直接使用 Codex |
| **WSL** | 打开 WSL 项目 |
| **GitLens** | 更好地看 Git 历史和 blame |
| **Error Lens** | 直接在代码行显示错误 |
| **ESLint** | JS/TS 项目检查 |
| **Prettier** | 格式化前端代码 |
| **Python** | Python 支持 |
| **Pylance** | Python 类型提示 |
| **Docker** | 管理容器和 Compose |
| **Markdown All in One** | 写文档更方便 |
| **REST Client** | 直接测试 API |

### 8.2 VS Code + Codex 的好用流程

1. 先用 VS Code 打开项目。
2. 确认终端能正常运行项目。
3. 让 Codex 先读项目，不修改。
4. 选一个小任务。
5. 让 Codex 修改。
6. 看 diff。
7. 运行测试。
8. 再让 Codex 自查一遍。

示例：

```text
请根据当前 git diff 做一次 code review。
重点检查：
1. 是否有明显 bug
2. 是否破坏既有逻辑
3. 是否缺少测试
4. 是否有不必要的大范围修改
只给建议，不要直接修改文件。
```

---

## 9. 必写的 AGENTS.md

`AGENTS.md` 是给 Codex 的项目说明书。Codex 在开始工作前会自动读取它。

建议每个项目根目录都放一个：

```markdown
# AGENTS.md

## 项目说明
这是一个 TypeScript 全栈项目，前端使用 React + Vite，后端使用 Node.js + Express。

## 常用命令
- 安装依赖：npm install
- 启动前端：npm run dev
- 启动后端：npm run server
- 运行测试：npm test
- 代码检查：npm run lint

## 工作规则
- 修改前先说明计划。
- 优先做小范围、高确定性的修改。
- 不要无理由重构大文件。
- 不要修改锁文件，除非确实安装了依赖。
- 修改后必须说明改了哪些文件。
- 如果需要新增依赖，必须先询问。

## 验收标准
- 测试通过。
- lint 通过。
- 关键页面或 API 可以启动验证。
- 最后输出修改总结和后续建议。
```

个人全局规则可以放在：

```text
~/.codex/AGENTS.md
```

Windows PowerShell 下大概对应：

```powershell
mkdir $HOME\.codex
notepad $HOME\.codex\AGENTS.md
```

---

## 10. Codex 必装插件 / 工具建议

Codex 的插件可以把 skills、应用集成、MCP server 打包成可复用工作流。Windows 应用里可以打开 **Plugins** 页面浏览和安装。

### 10.1 Codex 插件类

| 插件 / Skill | 适合做什么 | 推荐指数 |
|---|---|---|
| **Codex Security plugin** | 扫描代码中的可疑漏洞，辅助安全 review | ⭐⭐⭐⭐ |
| **Google Drive plugin** | 读取/整理 Docs、Sheets、Slides | ⭐⭐⭐⭐ |
| **Gmail plugin** | 总结邮件、草拟回复、整理邮件任务 | ⭐⭐⭐ |
| **Slack plugin** | 总结频道、草拟回复、提取任务 | ⭐⭐⭐ |
| **Sites** | 创建和部署网页、小游戏、Web app | ⭐⭐⭐⭐ |
| **Playwright skill** | 前端 UI 自动打开浏览器检查、截图、回归验证 | ⭐⭐⭐⭐⭐ |
| **Skill Creator** | 把你常用流程做成可复用 skill | ⭐⭐⭐⭐⭐ |

### 10.2 编程工具类

| 工具 | 为什么推荐 |
|---|---|
| **GitHub CLI (`gh`)** | Codex 可以帮你查 issue、创建 PR、看 CI 状态 |
| **Playwright** | 前端项目让 Codex 真实打开页面检查 UI |
| **pytest / vitest / jest** | 让 Codex 修改后可以自动验证 |
| **ruff / eslint / prettier** | 让 Codex 自动修格式和简单问题 |
| **Docker Compose** | 本地数据库、Redis、服务依赖更稳定 |
| **Makefile / package.json scripts** | 把复杂命令包装成简单命令，Codex 更不容易跑错 |

---

## 11. 最实用的 Codex 提示词模板

### 11.1 让 Codex 先理解项目

```text
请先阅读项目，不要修改文件。
请输出：
1. 技术栈
2. 目录结构
3. 启动命令
4. 测试命令
5. 主要业务模块
6. 你建议我优先补充到 AGENTS.md 的规则
```

### 11.2 修 bug

```text
请修复这个 bug：[描述 bug]

限制：
- 只修改必要文件
- 不要大范围重构
- 不要新增依赖，除非先询问
- 修改后运行相关测试

最后输出：
1. 问题原因
2. 修改内容
3. 验证方式
4. 还有什么风险
```

### 11.3 写新功能

```text
请实现功能：[功能描述]

要求：
1. 先给实现计划，不要马上修改
2. 确认影响文件范围
3. 按现有代码风格实现
4. 补充测试
5. 运行测试和 lint
6. 最后总结 diff
```

### 11.4 代码 review

```text
请 review 当前 git diff，不要修改文件。
重点检查：
1. bug 风险
2. 边界条件
3. 类型问题
4. 安全问题
5. 测试覆盖
6. 是否有不必要的修改

请按严重程度排序。
```

### 11.5 让 Codex 写文档

```text
请根据当前项目生成一份 README.md 草稿。
要求：
1. 项目简介
2. 技术栈
3. 本地启动步骤
4. 环境变量说明
5. 常用命令
6. 测试方法
7. 部署注意事项

先不要覆盖现有 README，生成 README_DRAFT.md。
```

### 11.6 自动化脚本

```text
请帮我写一个 PowerShell 脚本，用于自动完成：
1. 检查 Node / npm / git 是否安装
2. 安装依赖
3. 运行 lint
4. 运行测试
5. 输出结果日志

要求：
- 不要删除任何文件
- 出错时停止
- 每一步都有清楚输出
```

---

## 12. 如何节省 Codex 使用量

### 12.1 不要让 Codex 盲扫整个项目

差的问法：

```text
帮我看看这个项目有什么问题
```

好的问法：

```text
只检查 src/auth 和 src/api/login 相关代码，找出登录失败后错误提示不正确的原因。不要修改文件，先给分析。
```

### 12.2 任务越小越省

推荐拆成：

1. 先分析。
2. 再给计划。
3. 只改一个模块。
4. 最后 review diff。

### 12.3 先让 Codex “不要修改”

很多时候先分析就够了：

```text
先不要修改文件，只告诉我应该改哪里、为什么。
```

### 12.4 使用 AGENTS.md 减少重复说明

把固定规则写进去，不要每次都重复粘贴大段提示词。

### 12.5 善用 git diff

修改后让 Codex 只看 diff：

```text
只 review 当前 git diff，不要重新扫描整个项目。
```

---

## 13. 推荐工作流：从需求到提交

### Step 1：创建分支

```bash
git checkout -b feature/login-error-message
```

### Step 2：让 Codex 分析

```text
请分析登录错误提示这个功能相关代码。不要修改文件。
```

### Step 3：让 Codex 给计划

```text
请给出最小修改计划，列出预计修改文件。
```

### Step 4：执行修改

```text
按刚才计划修改。要求小范围修改，并补充测试。
```

### Step 5：运行验证

```text
请运行相关测试和 lint。如果失败，先解释失败原因，再修复。
```

### Step 6：Review diff

```text
请 review 当前 git diff，确认没有多余修改。
```

### Step 7：提交

```text
请根据当前 diff 生成一个合适的 git commit message。
```

---

## 14. Codex 可做的自动化任务

除了编程，Codex 也适合做这些：

| 任务 | 示例 |
|---|---|
| 文档整理 | 根据代码生成 README、API 文档、开发手顺 |
| 数据处理 | 读取 CSV/Excel，清洗数据，生成报告 |
| 测试补充 | 为已有函数补 pytest / jest / vitest |
| CI/CD 修复 | 分析 GitHub Actions 失败日志并修复 |
| 依赖升级 | 小版本升级、修复安全漏洞 |
| 前端 UI 调整 | 根据截图调整页面，配合 Playwright 验证 |
| 邮件/资料整理 | 配合 Gmail / Drive 插件总结资料 |
| 重复流程固化 | 用 Skill Creator 变成自己的 skill |

---

## 15. 常见问题

### Q1：Codex Windows 应用和 VS Code 插件冲突吗？

不冲突。它们是不同入口，可以共享同一项目。Windows 应用适合统一管理任务，VS Code 插件适合边看代码边操作。

### Q2：项目在 WSL，Codex 应该装 Windows 还是 WSL？

两个都可以装。项目主要在 WSL 的话，CLI 建议装在 WSL 里；Windows 应用可以通过 `\\wsl$\` 打开 WSL 项目。

### Q3：Codex 会不会乱删文件？

如果你开 Full access 或给了危险命令权限，就有风险。建议保持 sandbox，且在 AGENTS.md 里明确写：删除、重置、安装全局依赖前必须询问。

### Q4：为什么 Codex 运行命令失败？

常见原因：

- 当前目录不对。
- 项目依赖没安装。
- WSL / Windows 路径混用。
- sandbox 没有权限访问某目录。
- 没有安装 Node/Python/Docker/Git。

可以让 Codex 先诊断：

```text
请不要修改文件。请检查当前开发环境是否能运行这个项目，并列出缺失工具或错误配置。
```

### Q5：Codex 和 GitHub Copilot 怎么搭配？

- Copilot 更像代码补全和轻量聊天。
- Codex 更像能读项目、改文件、跑命令、做多步骤任务的 agent。
- 日常补全用 Copilot，复杂任务交给 Codex。

---

## 16. 我的推荐配置组合

### 轻量配置

适合只写小脚本、文档、简单项目：

- Codex Windows 应用
- VS Code
- Git for Windows
- Codex IDE extension

### 编程主力配置

适合 React / Node / Python / Java 项目：

- Codex Windows 应用
- Codex CLI
- VS Code + WSL 插件
- WSL2 Ubuntu
- Git + GitHub CLI
- Node.js LTS
- Python 3.12
- Docker Desktop
- Playwright

### 前端 UI 配置

- Codex Windows 应用
- VS Code
- Playwright skill
- Chrome / Edge
- ESLint + Prettier
- Storybook（如果项目有组件库）

---

## 17. 一句话总结

最稳的 Codex 用法不是“让它一次性帮我做完全部”，而是：

> 先让它读项目 → 给计划 → 小范围修改 → 自动测试 → review diff → 再提交。

把固定规则写进 `AGENTS.md`，把重复流程做成 skill，再配合 VS Code、WSL、GitHub CLI、Playwright，Codex 才会从“聊天工具”变成真正的开发助手。

---

## 参考资料

- OpenAI Codex app: https://developers.openai.com/codex/app
- OpenAI Codex Windows app: https://developers.openai.com/codex/app/windows
- OpenAI Codex Windows setup: https://developers.openai.com/codex/windows
- OpenAI Codex CLI: https://developers.openai.com/codex/cli
- OpenAI Codex IDE extension: https://developers.openai.com/codex/ide
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- OpenAI Codex plugins: https://developers.openai.com/codex/plugins
- OpenAI AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex best practices: https://developers.openai.com/codex/learn/best-practices
- OpenAI reusable Codex skills: https://developers.openai.com/codex/use-cases/reusable-codex-skills
- OpenAI frontend + Playwright use case: https://developers.openai.com/codex/use-cases/frontend-designs
