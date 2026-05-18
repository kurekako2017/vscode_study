# Next.js 示例项目结构

- `pages/`：页面路由目录。
  - `index.js`：根路径 `/` 的页面。
  - `_app.js`：应用入口包装，可引入全局样式。
- `styles/`：全局样式目录，示例中使用 `globals.css`。
- `next.config.js`：Next.js 配置文件。
- `package.json`：依赖与脚本（`dev`、`build`、`start`）。

学习建议：

- 理解 `pages` 路由约定，再扩展到更多页面。
- 逐步添加 `components/` 和 `lib/` 目录来拆分逻辑。
- 若后面要接接口，可再加入 `api/` 或 `services/` 层。
