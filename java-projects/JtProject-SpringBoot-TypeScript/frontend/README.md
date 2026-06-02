# JtProject-SpringBoot-TypeScript 前端入口

这个目录是 `JtProject-SpringBoot-TypeScript` 的独立前端工程，使用 Vite + 原生 TypeScript。

## 入口文件

- [index.html](./index.html)：浏览器加载入口，提供根挂载节点
- [src/main.ts](./src/main.ts)：页面状态、事件委托和 DOM 渲染入口
- [src/api.ts](./src/api.ts)：统一 `fetch` 封装
- [src/services/appService.ts](./src/services/appService.ts)：业务 API 调用封装
- [src/types.ts](./src/types.ts)：前端使用的数据类型
- [src/styles.css](./src/styles.css)：页面样式

## 配置文件

- [package.json](./package.json)：前端工程脚本和基础元信息
- [tsconfig.json](./tsconfig.json)：TypeScript 编译选项
- [vite.config.ts](./vite.config.ts)：Vite 开发服务器配置

## 运行方式

```bash
npm install
npm run dev
```

默认前端地址是 `http://localhost:5177/`。

## 学习建议

1. 先看 [src/main.ts](./src/main.ts)，理解没有框架时如何组织页面状态和事件
2. 再看 [src/services/appService.ts](./src/services/appService.ts)，理解业务请求如何统一封装
3. 然后看 [src/api.ts](./src/api.ts)，理解 `fetch`、cookie 和错误处理
4. 最后对照 Spring Boot 的 `ApiController.java` 看完整前后端链路
