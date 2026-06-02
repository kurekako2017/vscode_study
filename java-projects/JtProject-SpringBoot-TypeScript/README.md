# JtProject-SpringBoot-TypeScript 学习与启动入口

相关入口：

- 项目总导航：[Java项目总启动导航.md](../Java项目总启动导航.md)
- Java 项目根入口：[README.md](../README.md)
- 项目文档总入口：[docs/README.md](./docs/README.md)

## 项目说明

这个目录是从 `JtProject-React` 的 Spring Boot API 版本复制出来的独立项目，前端改造成了不使用 React、Vue、Next 的纯 TypeScript 版本。

- 后端：Spring Boot REST API
- 前端：Vite + TypeScript + 原生 DOM / Fetch API
- 后端端口：`8087`
- 前端端口：`5177`
- 数据库：本地 H2 文件库，路径在项目 `data/` 目录下
- 适合重点：理解“前后端分离 + TypeScript”在没有框架时的底层数据流

## 快速启动（Windows / PowerShell）

启动后端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-SpringBoot-TypeScript
.\mvnw.cmd spring-boot:run
```

后端接口基地址：

```text
http://localhost:8087/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-SpringBoot-TypeScript\frontend
npm install
npm run dev
```

前端页面地址：

```text
http://localhost:5177/
```

## 账号与验证

默认账号：

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

验证建议：

1. 先启动 Spring Boot 后端
2. 再启动 `frontend` 前端开发服务器
3. 打开首页后测试商品列表、普通用户登录、购物车、管理员登录

## 学习重点

- 不借助框架时如何组织 TypeScript 前端
- `fetch` 如何调用 Spring Boot REST API
- 前端状态对象如何驱动 DOM 重新渲染
- 表单提交、按钮事件和事件委托
- Java 后端分层与 TypeScript 前端服务层的连接方式

## 核心数据流

```text
ApiController.java
  -> UserServiceImpl.java / ProductServiceImpl.java
  -> UserDaoImpl.java / ProductDaoImpl.java
  -> frontend/src/api.ts
  -> frontend/src/services/appService.ts
  -> frontend/src/main.ts
  -> 浏览器 DOM
```

## 学习文档

- 学习入口：[docs/README.md](./docs/README.md)
- 数据流说明：[docs/springboot-typescript-flow.md](./docs/springboot-typescript-flow.md)
- 项目源码导读：[docs/project-code-map.md](./docs/project-code-map.md)

## 使用建议

1. 先跑通后端和前端
2. 看 `frontend/src/main.ts`，理解状态、事件和渲染函数
3. 看 `frontend/src/services/appService.ts`，理解业务请求如何封装
4. 看 `frontend/src/api.ts`，理解通用 API 调用
5. 对照后端 `ApiController.java` 和 Service / DAO，串起完整链路
