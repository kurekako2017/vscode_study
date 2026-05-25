# VS Code 本地 React + Node 示例工程

这是一个面向本地开发与教学的最小示例工程（适合在本地 VS Code 中打开）。项目包含：

- `client`：基于 Vite + React 的前端（默认端口 3000）
- `server`：基于 Express 的简单 API（默认端口 4000）

本仓库旨在作为一个轻量的本地开发示例：演示前后端分离、Vite 代理到后端 API、以及如何在 VS Code 中配置任务与调试。

项目功能（当前实现）

- 简单的 React 单页应用：`client/src/App.jsx`，展示从后端读取的消息。
- 后端示例 API：`GET /api/hello` 返回 JSON 消息。
- Vite 开发代理：`client/vite.config.js` 已配置将 `/api` 代理到 `http://localhost:4000`（避免 CORS）。
- VS Code 运行/调试：已提供 `launch.json` 与 `tasks.json`，可一键启动后端和在浏览器中打开前端。

快速开始（本地）

1. 安装依赖

```bash
cd web-projects/sample/react-node-template/server
npm install
cd ../client
npm install
```

2. 启动后端（终端 A）

```bash
cd web-projects/sample/react-node-template/server
npm run dev
```

3. 启动前端（终端 B）

```bash
cd web-projects/sample/react-node-template/client
npm run dev
```

打开浏览器访问 http://localhost:3000，页面会向 `/api/hello` 请求并显示后端消息。

在 VS Code 中运行（推荐）

1. 在 VS Code 中打开仓库根目录。
2. 打开「运行和调试」侧栏，选择 `Run Fullstack`，点击运行 — 这会同时启动后端并在浏览器中打开前端。也可通过命令面板运行单独任务：`Tasks: Run Task` → `Start Server` / `Start Client`。

部署与静态托管

如需将前端打包并由后端提供静态文件：

```bash
# 在 client 下构建
cd web-projects/sample/react-node-template/client
npm run build

# 在 server 中启用静态目录（已在 server/index.js 中有说明），将 dist 目录复制到 server 并取消注释静态托管代码
```

扩展建议

- 可以添加更多前端页面（关于、服务、新闻、联系表单）以示范路由与组件结构。
- 可在 `server` 中添加更多 API 路由（例如 `GET /api/news`、`POST /api/contact`），并演示如何将前端表单提交到后端。
- 建议安装 VS Code 常用扩展：ESLint、Prettier、Tailwind CSS IntelliSense（若使用 Tailwind）。

如果你希望我把项目名改为特定的名称（例如 `vscode-local-react-node-template`），或自动提交这些更改为一个 commit/PR，请告诉我。

