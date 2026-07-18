# AI Website Cloner Template 使用教程

> 用 AI 编码 Agent 将任意网页反向工程为 Next.js 代码库的模板项目
> 项目地址：https://github.com/JCodesMore/ai-website-cloner-template

## 一、这个工具是做什么的

这是一个 **模板仓库 (Template Repo)**，核心能力是：给它一个网站 URL，运行一条命令 `/clone-website`，AI 编码 Agent 就会自动完成：

1. **侦察（Reconnaissance）**：截图、提取设计 Token（颜色、字体等）、模拟滚动/点击/悬停等交互，采集响应式断点信息
2. **地基搭建（Foundation）**：更新字体、颜色、全局样式，下载所有素材（图片、视频、图标）
3. **组件规格说明（Component Specs）**：为每个组件写详细的规格文件，记录精确的 CSS 计算值、状态、行为和文案内容
4. **并行构建（Parallel Build）**：在 Git worktree 中派发多个"建造者"子 Agent，一个组件/区块一个 Agent，并行开发
5. **组装与质检（Assembly & QA）**：合并所有 worktree，拼装页面，并与原网站做视觉差异比对

最终产出是一个结构清晰、可维护的 **Next.js 16 + shadcn/ui + Tailwind CSS v4** 项目，而不是一堆爬虫抓下来的静态 HTML。

### 适用场景
- **平台迁移**：把 WordPress / Webflow / Squarespace 上的网站迁移为现代化 Next.js 代码库
- **代码丢失找回**：网站还在线上跑，但源码仓库丢了、原开发者离职了、或技术栈太老
- **学习研究**：拆解生产环境网站是如何实现某些布局、动效和响应式效果的

### 明确不适用的场景（请勿用于）
- 钓鱼或仿冒网站等欺骗性用途
- 把别人的 Logo、品牌素材、原创文案占为己有
- 违反目标网站服务条款（部分网站明确禁止抓取或复制，使用前请自行确认）

---

## 二、前置条件

| 项目 | 要求 |
|---|---|
| Node.js | 24 及以上版本 |
| AI 编码 Agent | 见下方支持列表，官方推荐 **Claude Code**（模型用 Opus） |
| Git / GitHub 账号 | 用于创建你自己的仓库副本 |

### 支持的 AI 编码 Agent

| Agent | 状态 |
|---|---|
| Claude Code | **官方推荐** |
| Codex CLI | 支持 |
| OpenCode | 支持 |
| GitHub Copilot | 支持 |
| Cursor | 支持 |
| Windsurf | 支持 |
| Gemini CLI | 支持 |
| Cline | 支持 |
| Roo Code | 支持 |
| Continue | 支持 |
| Amazon Q | 支持 |
| Augment Code | 支持 |
| Aider | 支持 |

---

## 三、快速上手步骤

> ⚠️ **重要**：一定要先点 **Use this template** 创建你自己的仓库副本，**不要**直接 clone 这个模板仓库来做你的网站项目，也不要把生成的网站代码提 PR 回原仓库。

### 步骤 1：基于模板创建你自己的仓库

1. 打开项目主页：https://github.com/JCodesMore/ai-website-cloner-template
2. 点击右上角 **Use this template** 按钮
3. 选择 **Create a new repository**
4. 给新仓库起名字，选择公开或私有，点击 **Create repository**
5. 如果出现 "Include all branches" 选项，可以不勾选

这样你就有了一个完全独立于原模板的项目，后续所有修改都只会保存在你自己的账号下。

### 步骤 2：把新仓库拉到本地

点击你新仓库页面的 **Code** 按钮，用你习惯的方式打开/克隆，命令行方式如下：

```bash
git clone https://github.com/你的用户名/你的新仓库名.git
cd 你的新仓库名
```

### 步骤 3：安装依赖

```bash
npm install
```

### 步骤 4：启动 AI Agent

以 Claude Code 为例（官方推荐），加上 `--chrome` 参数以便 Agent 能通过浏览器实际访问目标网站：

```bash
claude --chrome
```

如果你用的是其他 Agent（Cursor、Cline、Gemini CLI 等），打开 `AGENTS.md` 文件查看项目说明——大多数 Agent 会自动读取这份文件。

### 步骤 5：运行克隆命令

在 Agent 的交互界面中输入：

```bash
/clone-website <目标网址1> [<目标网址2> ...]
```

支持一次传入多个 URL，工具会并行处理、各自隔离产出结果。

### 步骤 6：按需自定义

基础克隆完成后，你可以像修改任何普通 Next.js 项目一样继续调整代码、替换文案、微调样式。

---

## 四、生成后的项目结构

```
src/
  app/                  # Next.js 路由
  components/           # React 组件
    ui/                 # shadcn/ui 基础组件
    icons.tsx           # 提取出的 SVG 图标
  lib/utils.ts           # cn() 工具函数
  types/                 # TypeScript 类型定义
  hooks/                 # 自定义 React Hooks
public/
  images/                # 从目标网站下载的图片
  videos/                # 从目标网站下载的视频
  seo/                   # favicon、OG 图等
docs/
  research/              # 提取结果与组件规格说明
  design-references/     # 截图参考
scripts/
  sync-agent-rules.sh    # 重新生成各 Agent 的说明文件
  sync-skills.mjs        # 重新生成各平台的 /clone-website 命令
AGENTS.md                # Agent 说明文件（唯一信息源）
CLAUDE.md                # Claude Code 专用配置（引用 AGENTS.md）
GEMINI.md                # Gemini CLI 专用配置（引用 AGENTS.md）
```

---

## 五、常用命令

```bash
npm run dev        # 启动开发服务器
npm run build      # 生产环境构建
npm run lint       # ESLint 代码检查
npm run typecheck  # TypeScript 类型检查
npm run check      # 依次执行 lint + typecheck + build
```

### 如果使用 Docker

```bash
docker compose up app --build   # 构建并运行正式版应用
docker compose up dev --build   # 以开发模式运行，端口 3001
```

---

## 六、技术栈说明

- **Next.js 16** —— App Router、React 19、TypeScript 严格模式
- **shadcn/ui** —— 基于 Radix 的无样式组件库
- **Tailwind CSS v4** —— 使用 oklch 色彩空间的设计 Token
- **Lucide React** —— 默认图标库（克隆过程中会被提取出的原网站 SVG 图标替换/补充）

---

## 七、进阶：适配其他 Agent 平台

项目用两个"唯一信息源"文件驱动所有平台的支持，改完源文件后跑对应脚本同步即可：

| 内容 | 源文件 | 同步命令 |
|---|---|---|
| 项目整体说明 | `AGENTS.md` | `bash scripts/sync-agent-rules.sh` |
| `/clone-website` 技能定义 | `.claude/skills/clone-website/SKILL.md` | `node scripts/sync-skills.mjs` |

原生支持读取源文件的 Agent 不需要额外同步。

---

## 八、小贴士

- 效果好坏很大程度取决于目标网站的复杂度：动效多、交互复杂的网站生成结果可能需要更多手工微调
- 建议先在小型、结构简单的网站上试跑一遍，熟悉整个流程后再处理复杂项目
- 生成后的组件规格文件（`docs/research/components/`）值得读一读，能帮你理解 Agent 是如何"看懂"原网站的
