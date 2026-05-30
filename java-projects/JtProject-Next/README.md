# JtProject-Next：Next.js + TypeScript 学习入口

这个目录是从原始 `JtProject` 复制出来的独立项目。当前版本的主要学习目标是：

- 用 `Next.js App Router` 组织前端页面
- 用 `TypeScript` 描述接口返回、页面状态和函数参数
- 用 `fetch` 调用 Spring Boot JSON API
- 理解“浏览器页面 -> Next.js 组件 -> Spring Boot Controller -> Service/DAO -> H2 数据库”的完整处理流程

- 后端：Spring Boot
- 前端：Next.js + TypeScript
- 后端端口：`8086`
- 前端端口：`3000`
- 数据库：本地 H2 文件库，路径在项目 `data/` 目录下

## 学习路线

建议按这个顺序看：

1. [doc/reference/nextjs-framework-guide.md](./doc/reference/nextjs-framework-guide.md)：系统理解 Next.js 框架分层
2. [frontend/app/layout.tsx](./frontend/app/layout.tsx)：理解 Next.js 根布局和 `metadata`
3. [frontend/app/page.tsx](./frontend/app/page.tsx)：理解首页路由、Client Component、React state、表单和事件
4. [frontend/lib/types.ts](./frontend/lib/types.ts)：理解 TypeScript 类型和泛型数据模型
5. [frontend/lib/api.ts](./frontend/lib/api.ts)：理解统一 API 请求封装、cookie session 和错误处理
6. [doc/reference/nextjs-typescript-flow.md](./doc/reference/nextjs-typescript-flow.md)：对照流程图理解前后端处理链路

## 快速启动

启动后端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next
.\mvnw.cmd spring-boot:run
```

后端接口基地址：

```text
http://localhost:8086/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next\frontend
npm install
npm run dev
```

前端页面地址：

```text
http://localhost:3000
```

## 默认账号

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

## 项目结构

- `src/main/java`：Spring Boot 后端源码
- `src/main/resources`：后端配置、初始化数据、静态资源
- `src/main/webapp/views`：原始 JSP 页面副本，保留作对照
- `frontend/app`：Next.js App Router 页面，重点看 `layout.tsx` 和 `page.tsx`
- `frontend/lib`：TypeScript 类型和 API 封装
- `doc/reference/nextjs-typescript-flow.md`：Next.js + TypeScript 前后端流程图

## 学习重点

- `app/page.tsx` 为什么要写 `'use client'`
- `useState<Product[]>` 这类写法如何让页面状态具备类型
- `api<T>()` 泛型函数如何让不同接口复用同一个请求封装
- `credentials: 'include'` 如何让浏览器携带 Spring Session cookie
- `Promise.all`、`try/catch/finally` 如何组织页面加载流程
- 后端 Controller 如何把 Service/DAO 数据转换成前端 JSON

## 前后端处理流程图

完整说明见：[Next.js + TypeScript 前后端处理流程图](./doc/reference/nextjs-typescript-flow.md)

框架系统学习见：[Next.js 框架系统学习指南](./doc/reference/nextjs-framework-guide.md)

```mermaid
flowchart TD
    Browser[Browser: http://localhost:3000] --> NextPage[Next.js app/page.tsx Client Component]
    NextPage --> ApiHelper[frontend/lib/api.ts api<T>()]
    ApiHelper --> SpringApi[Spring Boot /api Controller]
    SpringApi --> Service[Service Layer]
    Service --> Dao[DAO / Hibernate SessionFactory]
    Dao --> H2[(H2 file database)]
    H2 --> Dao
    Dao --> Service
    Service --> SpringApi
    SpringApi --> Json[ApiResult<T> JSON]
    Json --> ApiHelper
    ApiHelper --> State[React state: products/cart/session]
    State --> Ui[Rendered UI]
```
