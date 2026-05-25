# Angular 示例项目结构

- `angular.json`：Angular CLI 配置入口。
- `package.json`：依赖与脚本（`dev`、`build`、`start`）。
- `tsconfig.json` / `tsconfig.app.json`：TypeScript 编译配置。
- `src/`：源码目录。
  - `index.html`：应用挂载页，包含根组件选择器 `<app-root>`。
  - `main.ts`：应用启动入口，负责 `bootstrapApplication`。
  - `styles.css`：全局样式。
  - `app/`：组件目录。
    - `app.component.ts`：根组件定义。
    - `app.component.html`：根组件模板。
    - `app.component.css`：根组件样式。

学习建议：

- 先理解 `bootstrapApplication` 的启动方式，再看组件模板和样式如何拆分。
- 后续可以继续补 `routes.ts`、`services/`、`shared/` 等目录。
