# React Modern Learning

这是一个面向现代 React 的学习项目骨架。它把 `Hooks`、`Router`、`Context`、`API`、`Test` 拆成独立章节，适合按主题逐个练习。

## 目录设计

- `src/chapters/hooks/`：`useState`、`useEffect` 等 Hook 示例
- `src/chapters/router/`：`react-router-dom` 示例
- `src/chapters/context/`：Context 与 Provider / Consumer 示例
- `src/chapters/api/`：`fetch`、加载中、错误态、数据态示例
- `src/chapters/test/`：组件与测试文件配对示例
- 结构树见 [project-structure.md](./project-structure.md)

## 运行方式

```bash
npm install
npm run dev
```

## 学习顺序

1. 先看首页，理解章节入口。
2. 再从 `Hooks` 开始练状态和副作用。
3. 接着看 `Router`，理解页面切换和嵌套路由。
4. 然后看 `Context`，理解跨层传值。
5. 再看 `API`，练请求、加载态和错误态。
6. 最后看 `Test`，把组件和测试文件配成一组。
