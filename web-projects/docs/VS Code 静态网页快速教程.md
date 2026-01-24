# VS Code 静态网页快速教程

## 目标

本教程面向想用 VS Code 快速搭建静态网站的开发者。内容涵盖所需插件、模板、示例项目、预览与部署的实用步骤。

## 准备工作

- 安装 VS Code。打开项目文件夹：`File → Open Folder`。
- 推荐创建项目文件夹并在 VS Code 中打开（本示例位于 `static-site-example`）。

## 推荐扩展

- **Live Server (必选)**：快速本地预览并热重载。
- **Prettier - Code formatter (必选)**：代码格式化，建议开启 `Format On Save`。
- **Path Intellisense**：文件路径自动补全。
- **Auto Close Tag / Auto Rename Tag**：自动关闭/重命名 HTML 标签。
- **Tailwind CSS IntelliSense**（当使用 Tailwind 时）

安装扩展：打开扩展视图或按 `Ctrl+P`，输入 `ext install <extension-id>`。

## 使用插件与模板快速创建静态网页

下面列出三种常用方法：内置工具（Emmet/代码片段）、模板扩展，以及脚手架/生成器。

方法一 — Emmet 与用户代码片段（无需额外扩展）
- 快速生成 HTML 骨架：在新文件输入 `!` 回车（或 Tab），Emmet 会生成基本的 `<!doctype html>` 模板。
- 自定义片段：按 `File → Preferences → User Snippets`，选择 `html.json`，添加例如：

```json
{
  "Static Site Boilerplate": {
    "prefix": "ssb",
    "body": [
      "<!doctype html>",
      "<html lang=\"zh-CN\">",
      "<head>",
      "  <meta charset=\"utf-8\">",
      "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
      "  <title>$1</title>",
      "  <link rel=\"stylesheet\" href=\"css/styles.css\">",
      "</head>",
      "<body>",
      "  $0",
      "  <script src=\"js/script.js\"></script>",
      "</body>",
      "</html>"
    ],
    "description": "静态站点基础模板"
  }
}
```

方法二 — 使用模板扩展（快速从模板/样板创建项目）
- 在扩展视图搜索关键词 `template`、`project templates` 或 `file templates`，安装评分高的扩展（例如常见的 `Project Templates`/`File Templates` 类扩展）。
- 使用方式通常是：打开命令面板（`Ctrl+Shift+P`）→ 选择扩展提供的命令（如“Create Project From Template”或“New File From Template”）→ 选择模板并填写项目名与路径。
- 许多模板扩展支持将 `.vscode`、依赖文件、README、基础目录结构一起创建，方便团队统一样板。

方法三 — 使用脚手架 / Yeoman / npm generator（适合复杂模板）
- 全局安装并使用脚手架：

```bash
npm install -g yo generator-webapp
yo webapp
```

- 这种方式适合需要一套构建流程（例如包含 PostCSS、Tailwind、构建脚本）的模板。

工作区模板建议
- 在工作区加入 `.vscode/extensions.json` 推荐扩展，以及 `.vscode/settings.json` 的常用设置（例如 `editor.formatOnSave`、`files.exclude`），能让团队打开仓库时快速统一开发环境。
- 示例 `extensions.json`（放于项目的 `.vscode` 目录）：

```json
{
  "recommendations": [
    "ritwickdey.LiveServer",
    "esbenp.prettier-vscode",
    "christian-kohler.path-intellisense"
  ]
}
```

小结：初学者优先用 Emmet 与自定义片段迅速起步；需要团队或多次复用时，使用模板扩展或脚手架能节省大量重复工作。


## 常见模板来源与快速方法（附件内容）

下面摘录并整理自附件笔记，包含常见下载来源、VS Code 插件模板、脚手架与 GitHub 下载方法，便于快速开始：

方法一：从模板网站下载（最常用）
- 常见站点：
 - HTML5 UP（响应式模板，免费高质量）：https://html5up.net/
 - Bootstrap 官方示例（组件与模板）：https://getbootstrap.com/docs/5.3/examples/
 - FreeCSS（免费模板集合）：https://www.free-css.com/
 - ThemeForest（付费优质模板市场）：https://themeforest.net/
- 使用流程：下载 ZIP → 解压到项目文件夹 → 在 VS Code 中打开 → 用 `Live Server` 或内置预览查看。

方法二：VS Code 插件直接快速创建模版（新手友好）
- 推荐扩展举例：
  - `Live Server`（实时预览）
  - `HTML Boilerplate` / `HTML Snippets`（快速插入常用 HTML 模板）
  - `Bootstrap 5 Snippets`（Bootstrap 组件片段）
- 使用流程：安装扩展 → 打开命令面板 `Ctrl+Shift+P` → 运行扩展提供的“New File From Template”或相似命令 → 填写名称与路径。

方法三：用前端脚手架（进阶一点）
- 适用于需要构建流程的项目（如 Vue、React、Vite 等）。
- 常用命令示例：

```bash
npm create vite@latest my-vue-app -- --template vue
npx create-react-app my-react-app
```

方法四：GitHub 直接下载现成网站模板（懒人方法）
- 在 GitHub 仓库点击 `Code → Download ZIP`，或使用 `git clone` 拉取。
- 下载后在 VS Code 中打开，按需修改、用 `Live Server` 预览。

新手快速组合建议：
- 先用 `HTML5 UP` 或 `Bootstrap` 模板配合 `Live Server` 快速预览与修改；
- 想做现代前端或组件化开发时，使用 `Vite`/`create-*` 脚手架开始，然后把模板或样式迁移进来。

## 最简单的项目结构

```
static-site-example/
  ├─ index.html
  ├─ css/
  │   └─ styles.css
  ├─ js/
  │   └─ script.js
  ├─ .vscode/
  │   └─ settings.json
  └─ README.md
```

## 使用方法（本示例）

1. 在 VS Code 中打开 `static-site-example`。  
2. 右键 `index.html` → `Open with Live Server` 查看实时效果。  
3. 编辑 `index.html`、`css/styles.css` 或 `js/script.js`，页面会自动刷新。

## 如果要使用 Tailwind（生产化推荐用 npm）

本示例使用 Tailwind CDN 便于快速试验；若用于生产应采用 `npm` + `tailwindcss` 构建流程，以便提取未使用样式并压缩输出。

快速命令（可选）:

```bash
npm init -y
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

然后在 `styles.css` 中引入 `@tailwind base; @tailwind components; @tailwind utilities;` 并用构建脚本输出最终 CSS。

## 部署

- 纯静态站点：可直接部署到 GitHub Pages、Netlify、Vercel。  
- 将仓库推到 GitHub，然后在 Netlify/Vercel 中连接仓库，配置构建命令（如果使用构建）与发布目录（如 `_site` 或 `dist`）。

## 常见问题

- Live Server 无刷新：检查端口、关闭浏览器缓存或重启扩展。  
- 样式不生效：确认 CSS 引入路径正确，或 Tailwind 是否使用了构建流程。

## 下一步建议

- 想要组件化：考虑使用 Astro、Next.js 或 Vite + React。  
- 需要多语言或博客功能：考虑 Eleventy 或 Hugo。

---

示例项目位于 `static-site-example` 目录，包含演示用的 `index.html`、`css/styles.css`、`js/script.js`，以及 `.vscode` 设置与 `README.md`。
