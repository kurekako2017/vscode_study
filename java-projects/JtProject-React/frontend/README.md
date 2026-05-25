# JtProject-React 前端入口

这个目录是 `JtProject-React` 的独立前端工程，使用 React + TypeScript + Vite。

## 入口文件

- [index.html](./index.html)：浏览器加载入口，提供根挂载节点
- [src/main.tsx](./src/main.tsx)：React 应用入口，负责挂载根组件
- [src/App.tsx](./src/App.tsx)：页面路由和业务壳层

## 配置文件

- [package.json](./package.json)：前端工程依赖、脚本和基础元信息
- [tsconfig.json](./tsconfig.json)：TypeScript 编译选项
- [vite.config.ts](./vite.config.ts)：Vite 开发服务器与插件配置

## 运行方式

```bash
npm install
npm run dev
```

默认前端地址是 `http://localhost:5173/`。

## 学习建议

1. 先看 [src/main.tsx](./src/main.tsx)，理解入口如何挂载
2. 再看 [src/App.tsx](./src/App.tsx)，理解页面路由和状态分发
3. 然后看 [src/types.ts](./src/types.ts) 和 [src/services/appService.ts](./src/services/appService.ts)，理解类型和 API 封装
4. 最后对照 [src/views/](./src/views/) 和 [src/components/](./src/components/) 看组件拆分方式