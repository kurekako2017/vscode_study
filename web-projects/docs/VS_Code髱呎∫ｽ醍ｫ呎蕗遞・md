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
