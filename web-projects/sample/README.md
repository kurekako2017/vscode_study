# Sample 项目索引

`web-projects/sample` 用来放更接近“实战样板”的项目。它和 `web-projects/examples` 的区别是：

- `examples`：偏框架最小 hello，用来学习单个技术的启动方式。
- `sample`：偏组合项目或业务样板，用来学习前后端联调、企业站、部署、Dev Container、项目组织方式。

## 项目总览

| 项目 | 类型 | 技术栈 | 用途 / 作用 | 适合学习 |
| --- | --- | --- | --- | --- |
| [`react-node-demo`](react-node-demo/README.md) | 全栈入门 demo | React + Vite + Express | 最小前后端分离示例，前端请求后端 `/api/hello` 并显示结果 | React 请求 API、Express 路由、前后端联调 |
| [`react-node-template`](react-node-template/README.md) | 本地开发模板 | React + Vite + Express + VS Code Tasks | 面向本地 VS Code 的可复用模板，带 Vite 代理、调试任务和前后端启动配置 | 本地全栈开发、Vite proxy、VS Code 调试 |
| [`codespaces-react-node-template`](codespaces-react-node-template/README.md) | Codespaces / Dev Container 模板 | React + Vite + Express + Dev Container | 面向 GitHub Codespaces 或 VS Code Dev Containers 的云端开发模板 | Dev Container、Codespaces、远程开发环境 |
| [`company-website`](company-website/README.md) | 企业官网全栈样板 | Next.js + TypeScript + Tailwind CSS + Supabase | 低成本企业官网方案，包含前台页面、新闻数据、联系表单、Supabase schema、部署文档 | 企业站架构、Next.js App Router、Supabase、部署 |
| [`web-learning-site`](web-learning-site/README.md) | Web 学习实战项目 | HTML + CSS + JavaScript + 文档化后端规划 | 企业官网学习路线项目，当前有静态前端和系统化学习文档 | 静态页面、新闻数据、后端演进规划、完整学习路线 |

## 项目定位

### `react-node-demo`

最简单的 React + Node 全栈入门项目。

作用：

- 快速看懂“前端页面如何调用后端 API”。
- 后端只提供一个 `GET /api/hello`，方便先学习请求链路。
- 适合第一次练习 React、fetch、Express、JSON 返回。

运行方式：

```bash
cd web-projects/sample/react-node-demo/server
npm install
npm start
```

```bash
cd web-projects/sample/react-node-demo/client
npm install
npm run dev
```

### `react-node-template`

本地 VS Code 使用的 React + Node 模板。

作用：

- 在 `react-node-demo` 基础上更偏“开发模板”。
- `client/vite.config.js` 配置了 `/api` 代理到后端，减少 CORS 干扰。
- `.vscode/tasks.json` 和 `.vscode/launch.json` 可用于 VS Code 一键运行或调试。

运行方式：

```bash
cd web-projects/sample/react-node-template/server
npm install
npm run dev
```

```bash
cd web-projects/sample/react-node-template/client
npm install
npm run dev
```

### `codespaces-react-node-template`

面向 GitHub Codespaces / VS Code Dev Containers 的 React + Node 模板。

作用：

- 和 `react-node-template` 类似，也是 React 前端 + Express 后端。
- 额外包含 `.devcontainer/devcontainer.json`，用于自动配置远程开发容器。
- 适合学习如何让项目在云端 Codespaces 或容器环境中开箱即用。

运行方式：

```bash
cd web-projects/sample/codespaces-react-node-template/server
npm install
npm run dev
```

```bash
cd web-projects/sample/codespaces-react-node-template/client
npm install
npm run dev
```

### `company-website`

企业官网全栈样板项目。

作用：

- 面向真实企业网站：主页、关于、服务、新闻、联系、后台管理等。
- 前端在 `frontend/`，使用 Next.js App Router、TypeScript、Tailwind CSS。
- 后端数据方案以 Supabase 为主，`backend/supabase/schema.sql` 存放数据库 schema。
- `docs/` 里有部署和入门文档，`scripts/` 里有初始化、部署、备份、新闻迁移脚本。

运行方式：

```bash
cd web-projects/sample/company-website/frontend
npm install
npm run dev
```

注意：

- 运行前参考 `frontend/.env.example` 创建 `.env.local`。
- Supabase 相关配置需要真实项目 URL 和 Key。

### `web-learning-site`

企业官网学习路线项目。

作用：

- 偏“学习计划 + 静态原型 + 后端演进说明”。
- `frontend/` 是静态 HTML/CSS/JS 页面，并使用 `news.json` 保存新闻数据。
- `docs/backend-implementation-guide.md` 说明后端如何从静态数据演进为 API、数据库和管理后台。
- 适合按阶段学习企业站从静态页面到全栈系统的完整路径。

运行方式：

```bash
cd web-projects/sample/web-learning-site/frontend
```

然后直接用浏览器打开 `index.html`，或使用本地静态服务器预览。

## 如何选择

| 目标 | 推荐项目 |
| --- | --- |
| 只想快速理解前后端联调 | `react-node-demo` |
| 想要一个本地 VS Code 全栈模板 | `react-node-template` |
| 想学习 Codespaces / Dev Container | `codespaces-react-node-template` |
| 想做可部署的企业官网 | `company-website` |
| 想按学习路线逐步从静态站做到全栈站 | `web-learning-site` |

## 目录关系说明

```text
web-projects/
  examples/   # 框架最小 hello：React、Vue、Angular、Next、TypeScript
  sample/     # 更接近实战的组合项目和项目模板
  docs/       # 通用 Web 知识文档
  plugins/    # 与插件或平台扩展相关的代码
```

一句话理解：

```text
examples 学单点技术，sample 学项目组合和真实工程组织。
```
