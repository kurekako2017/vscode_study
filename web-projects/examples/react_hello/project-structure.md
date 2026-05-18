# React 示例项目结构

- `index.html`：Vite 入口页面，挂载到 `#root`。
- `package.json`：脚本和依赖声明。
- `vite.config.js`：Vite 构建配置。
- `src/`：源代码目录。
  - `main.jsx`：React 入口，负责 `createRoot` 和渲染。
  - `App.jsx`：页面主体组件。
  - `style.css`：全局样式。

学习建议：

- 先理解 `main.jsx` 和 `App.jsx` 的职责分离。
- 逐步把页面拆成更小的组件，再练习 props 传参。
- 继续增加图片、按钮和交互，练习事件与状态管理。
