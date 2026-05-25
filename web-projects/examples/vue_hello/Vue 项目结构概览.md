# Vue 项目结构概览

下面是一个典型的 Vue 3 + Vite 项目目录示例和简要说明，供学习与快速上手参考。

- `index.html`：应用入口页面，Vite 在此挂载应用。
- `src/`
  - `main.ts` 或 `main.js`：前端应用的启动文件，创建应用并挂载根组件。
  - `App.vue`：根组件，通常包含路由出口和全局布局。
  - `components/`：可复用组件目录（例如 `Header.vue`、`Footer.vue`、`UserCard.vue`）。
  - `views/` 或 `pages/`：页面级组件（路由对应的视图）。
  - `router/`：路由配置（通常 `index.ts` 导出路由实例）。
  - `store/` 或 `store/*`：状态管理（Pinia 或 Vuex 配置）。
  - `assets/`：静态资源（图片、字体等）。
  - `styles/`：全局样式或 CSS 变量文件。
  - `api/` 或 `services/`：封装的后端 API 调用逻辑。

- `public/`：无需打包的静态资源，直接拷贝到构建产物目录。
- `vite.config.ts`：Vite 配置文件（别名、代理、插件等）。
- `package.json`：项目元数据与 npm 脚本（`dev`、`build`、`preview` 等）。

开发常用命令示例：

```bash
npm install
npm run dev    # 本地开发，热重载
npm run build  # 生产构建
npm run preview # 本地预览构建产物
```

学习建议：
- 优先掌握 `Composition API`（`setup()`、`ref`、`reactive`）。
- 将页面拆分为小组件，练习组件通信（props、emits、provide/inject）。
- 使用 `Pinia` 或 `Vuex` 管理复杂状态。 
- 使用 `vite` 的代理功能在开发时连接后端 API（避免 CORS 问题）。

参考仓库中现有笔记：
- `java-projects/JtProject-Vue/docs/vue-framework-notes.md`
