# Examples 目录总览

本目录包含若干前端最小示例工程，每个子目录内含可直接运行的示例代码与各自的 `README.md`。可作为学习模板或快速启动样板。

包含项目：

- `vue_hello`：Vue 3 + Vite 最小示例（开发服务器、构建、预览）。详见 [web-projects/examples/vue_hello/README.md](web-projects/examples/vue_hello/README.md)
- `react_hello`：React 18 + Vite 最小示例。详见 [web-projects/examples/react_hello/README.md](web-projects/examples/react_hello/README.md)
- `next_hello`：Next.js（Pages Router）最小示例。详见 [web-projects/examples/next_hello/README.md](web-projects/examples/next_hello/README.md)
- `angular_hello`：Angular 最小示例（standalone component）。详见 [web-projects/examples/angular_hello/README.md](web-projects/examples/angular_hello/README.md)

快速开始（通用步骤）

1. 进入任一子项目目录，例如 `cd web-projects/examples/vue_hello`。
2. 安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

4. 常用默认地址：

- Vite（`vue_hello`、`react_hello`）：`http://localhost:5173`
- Next.js（`next_hello`）：`http://localhost:3000`
- Angular（`angular_hello`）：`http://localhost:4200`

说明与故障排查

- 推荐 Node.js 版本：Node 16 及以上。
- 若端口被占用，Vite/Next/Angular 会提示并可选择其它端口，或通过设置 `PORT` 环境变量固定端口。
- 若遇到依赖安装或构建错误，先删除 `node_modules` 并重新运行 `npm install`，必要时清空 npm 缓存。

如需更详细的步骤，请打开各示例目录下的 README 查看专属说明与示例代码。欢迎在仓库中贡献更多示例！
