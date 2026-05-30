# Examples 目录总览

本目录包含若干前端示例工程，每个子目录内含可直接运行的示例代码与各自的 `README.md`。可作为学习模板或快速启动样板。

## 基础入门示例

- `vue_hello`：Vue 3 + Vite 最小示例（开发服务器、构建、预览）。详见 [vue_hello/README.md](vue_hello/README.md)
- `react_hello`：React 18 + Vite 最小示例。详见 [react_hello/README.md](react_hello/README.md)
- `next_hello`：Next.js（Pages Router）最小示例。详见 [next_hello/README.md](next_hello/README.md)
- `angular_hello`：Angular 最小示例（standalone component）。详见 [angular_hello/README.md](angular_hello/README.md)
- `typescript_hello`：Vanilla TypeScript + Vite 最小示例。详见 [typescript_hello/README.md](typescript_hello/README.md)

## 进阶场景示例

- `headless-nextjs`：Next.js + Headless CMS / WordPress API 的进阶示例。详见 [headless-nextjs/README.md](headless-nextjs/README.md)

暂时标记：`headless-nextjs` 当前仍放在 `examples/` 下，方便和 `next_hello` 对照学习。它不是基础 hello 项目，而是“Next.js 前端 + API/CMS 数据源”的进阶场景。等内容扩展到更完整的 CMS、GraphQL、认证、部署等主题后，可以再考虑移动到 `web-projects/headless-nextjs/` 或单独的实战目录。

## plugins 是什么

在这些前端项目里，`plugins` 通常指“框架或构建工具插件”，不是浏览器插件，也不是后端插件。

常见例子：

- Vite 插件：例如 Vue 项目里的 `@vitejs/plugin-vue`，负责让 Vite 识别和编译 `.vue` 单文件组件。
- Vue DevTools 插件：例如 `vite-plugin-vue-devtools`，在开发阶段增强调试能力。
- Next.js 插件：通常用于扩展 Next.js 的构建、图片、国际化、Bundle 分析等能力。
- Angular 插件/构建器：通常通过 Angular CLI、builder、schematics 或第三方包扩展项目能力。

一句话理解：

```text
plugins = 给框架或构建工具增加能力的小模块，例如让 Vite 支持 Vue、让项目增加调试或分析能力。
```

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

- Vite（`vue_hello`、`react_hello`、`typescript_hello`）：`http://localhost:5173`
- Next.js（`next_hello`）：`http://localhost:3000`
- Angular（`angular_hello`）：`http://localhost:4200`

说明与故障排查

- 推荐 Node.js 版本：Node 16 及以上。
- 若端口被占用，Vite/Next/Angular 会提示并可选择其它端口，或通过设置 `PORT` 环境变量固定端口。
- 若遇到依赖安装或构建错误，先删除 `node_modules` 并重新运行 `npm install`，必要时清空 npm 缓存。

如需更详细的步骤，请打开各示例目录下的 README 查看专属说明与示例代码。欢迎在仓库中贡献更多示例！
