# Codespaces React + Node 模板

这是一个用于教学与 Codespaces 的最小示例工程，包含：

- `client`：基于 Vite + React 的前端（在 3000 端口）
- `server`：基于 Express 的简单 API（在 4000 端口）
- `.devcontainer`：用于 GitHub Codespaces / VS Code Dev Containers 的配置

快速开始（在 Codespaces 中）

1. 在 GitHub 仓库中打开：`Code -> Open with Codespaces`，或在本地 VS Code 使用 Remote-Containers 打开。
2. Codespace 启动后，devcontainer 会自动安装依赖。
3. 在 Codespace 终端运行：

```bash
# 在第一个终端启动后端
cd server
npm run dev

# 在第二个终端启动前端
cd client
npm run dev
```

前端地址：http://localhost:3000
后端 API：http://localhost:4000/api/hello

在本地运行（无 Codespaces）

```bash
# 安装依赖
cd web-projects/sample/codespaces-react-node-template/server
npm install
cd ../client
npm install

# 启动后端
cd ../server
npm run dev

# 启动前端
cd ../client
npm run dev
```

如需将前端打包并由后端提供静态文件，请运行前端 `npm run build`，然后在 `server` 中启用静态托管（示例已包含注释）。
