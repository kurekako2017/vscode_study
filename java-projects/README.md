# Java 项目根入口

这个目录是 `vscode_study` 里的 Java 项目总入口。

建议先看：

- [Java项目总启动导航.md](./Java项目总启动导航.md)
- [doc/README.md](./doc/README.md)
- [前端项目现状总览.md](./前端项目现状总览.md)

主要项目：

- `JtProject`：原始 Spring Boot + JSP 版本
- `JtProject-Thymeleaf`：Thymeleaf 学习版
- `JtProject-React`：React + TypeScript 学习版
- `JtProject-Vue`：Vue 3 + TypeScript 学习版
- `JtProject-Next`：Next.js + TypeScript 学习版
- `JtProject-SpringBoot-TypeScript`：Spring Boot + 纯 TypeScript 学习版
- `JtProject-TypeScript`：纯 TypeScript 全栈学习版

目录说明：

- `JtProject/`：原始项目源码与项目内文档
- `JtProject-Thymeleaf/`：Thymeleaf 改写版源码与学习文档
- `JtProject-React/`：React 前后端分离版源码与文档
- `JtProject-Vue/`：Vue 前后端分离版源码与文档
- `JtProject-Next/`：Next.js 前后端分离版源码与文档
- `JtProject-SpringBoot-TypeScript/`：Spring Boot + 原生 TypeScript 前后端分离版源码与文档
- `JtProject-TypeScript/`：Node.js + Express + React + TypeScript 全栈版源码与文档
- `doc/`：`java-projects` 级别的 IDEA 和通用辅助文档
- `data/`：部分项目运行后生成的本地数据目录
- `Java项目总启动导航.md`：总启动入口
- `README.md`：当前这个目录级导航页

如果你只是想尽快跑起来，直接打开上面的总启动导航即可。

如果你想先弄清楚 `Next / Vue / TypeScript` 这几条现代前端路线的当前状态，先看 [前端项目现状总览.md](./前端项目现状总览.md)。

## 七个版本对比

这七个项目不是“完全不同的业务”，而是围绕同一套电商业务做的不同技术栈练习。它们最适合拿来对比“同一业务在不同前端/视图技术下，知识点到底差在哪里”。

| 版本 | 主要学习内容 | 核心知识点 | 和其他版本的区别 |
| --- | --- | --- | --- |
| `JtProject` | 原始 Spring Boot + JSP 版本 | Controller 跳转、JSP 标签、Servlet / 请求响应链路、Service / DAO 分层、远程 MySQL 配置 | 最贴近传统 Java Web，前后端耦合最紧，适合先理解“后端如何直接驱动页面” |
| `JtProject-Thymeleaf` | JSP 到 Thymeleaf 的视图层迁移 | `th:text`、`th:if`、`th:each`、`th:href`、模板片段复用、模型数据绑定 | 业务链路基本不变，重点是“视图层替换”；比 JSP 更现代，但仍是服务端渲染 |
| `JtProject-React` | React + TypeScript + Vite 前后端分离 | 组件拆分、Hooks、状态提升、路由、表单控制、API 封装、前后端分离、TypeScript 类型设计 | 前端从“页面模板”变成“组件树 + 状态驱动 UI”，页面交互和数据请求都在前端控制 |
| `JtProject-Vue` | Vue 3 + TypeScript + Vite 前后端分离 | 组合式 API、响应式状态、组件通信、路由、表单控制、API 调用、TypeScript 类型设计 | 和 React 一样是前后端分离，但写法更偏“响应式数据 + 组合函数”，适合对比两种现代前端思路 |
| `JtProject-Next` | Next.js + TypeScript 前后端分离 | App Router、客户端组件、API 封装、环境变量、TypeScript 类型设计 | 用 Next.js 组织页面和前端入口，适合继续学习 React 生态里的应用框架写法 |
| `JtProject-SpringBoot-TypeScript` | Spring Boot + 纯 TypeScript 前后端分离 | 原生 DOM、事件委托、Fetch API、状态对象、Vite、TypeScript 类型设计 | 不使用 React / Vue / Next，适合先理解现代前端框架封装之前的底层数据流 |
| `JtProject-TypeScript` | 纯 TypeScript 全栈 | Express API、React 前端、共享类型、泛型 API、前后端类型一致性 | 不再使用 Java 后端，前后端都用 TypeScript，适合学习全栈 TS 的数据流和类型复用 |

### 一眼看懂的差异

- 如果你想学“传统 Java Web 怎么把请求直接渲染成页面”，先看 `JtProject`
- 如果你想学“服务端模板如何比 JSP 更清晰”，看 `JtProject-Thymeleaf`
- 如果你想学“现代前端如何用组件和状态组织页面”，看 `JtProject-React`
- 如果你想学“Vue 3 的响应式思路和组件组织方式”，看 `JtProject-Vue`
- 如果你想学“Next.js 如何在 React 基础上组织应用”，看 `JtProject-Next`
- 如果你想学“不用框架时 TypeScript 如何直接调 API 和操作 DOM”，看 `JtProject-SpringBoot-TypeScript`
- 如果你想学“前后端都用 TypeScript 如何共享类型”，看 `JtProject-TypeScript`

### 按知识点拆开看

| 知识点 | `JtProject` | `JtProject-Thymeleaf` | `JtProject-React` | `JtProject-Vue` | `JtProject-Next` | `JtProject-SpringBoot-TypeScript` | `JtProject-TypeScript` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 页面渲染方式 | JSP 服务端渲染 | Thymeleaf 服务端渲染 | 前端组件渲染 | 前端组件渲染 | Next.js 页面 + 客户端组件 | 原生 DOM 渲染 | React + Vite 前端组件 |
| 数据流向 | 后端 Controller -> JSP | 后端 Controller -> 模板 | 后端 API -> 前端状态 -> 组件 | 后端 API -> 响应式状态 -> 组件 | 后端 API -> Next 页面状态 -> 组件 | 后端 API -> Fetch -> TypeScript 状态 -> DOM | Express API -> 共享类型 -> React 状态 -> 组件 |
| 状态管理 | 主要在后端和会话里 | 主要在后端和模型里 | 前端 state / hooks 管理 | 前端响应式数据 / composables 管理 | React state / hooks 管理 | 手写 state 对象 + render 函数 | React state + TypeScript Store |
| 表单处理 | JSP 表单 + Controller | 模板表单 + Controller | 受控表单 + 事件回调 | 双向绑定 / 响应式表单 | 受控表单 + Next 页面事件 | FormData + 事件委托 | 受控表单 + Express JSON API |
| 路由方式 | 后端跳转为主 | 后端跳转为主 | 前端路由切换 | 前端路由切换 | App Router | 手写视图切换 | Express API 路由 + 单页前端 |
| 类型体系 | Java 后端类型 | Java 后端类型 | TypeScript 前端类型 | TypeScript 前端类型 | TypeScript 前端类型 | Java 后端类型 + TypeScript 前端类型 | 前后端共享 TypeScript 类型 |

### 学习顺序建议

1. 先看 `JtProject`，理解原始业务和页面流转
2. 再看 `JtProject-Thymeleaf`，理解服务端模板替换
3. 然后看 `JtProject-React`，理解前后端分离和组件化状态管理
4. 再看 `JtProject-Vue`，对比 Vue 3 的响应式写法和 React 的区别
5. 再看 `JtProject-Next`，理解 React 生态里的应用框架组织方式
6. 再看 `JtProject-SpringBoot-TypeScript`，理解不借助框架时 TypeScript 如何直接组织状态、事件和 DOM
7. 最后看 `JtProject-TypeScript`，理解前后端共享 TypeScript 类型的全栈写法

如果你的目标是“把同一套业务完整学一遍”，最好的方式不是只看单个项目，而是把这七个版本按上面的顺序串起来看。

### 七个版本的技术知识点目录对比

这里的“目录”指学习目录，不是项目文件夹目录。可以把每一行当成一个章节，用同一业务在七个版本里的不同实现方式做横向对比。

| 学习章节 | `JtProject` | `JtProject-Thymeleaf` | `JtProject-React` | `JtProject-Vue` | `JtProject-Next` | `JtProject-SpringBoot-TypeScript` | `JtProject-TypeScript` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01. 项目定位 | 传统 Java Web 原始版 | JSP 替换为 Thymeleaf 的服务端模板版 | Spring Boot API + React 前端分离版 | Spring Boot API + Vue 3 前端分离版 | Spring Boot API + Next.js 前端版 | Spring Boot API + 原生 TS 前端版 | Node.js + Express + React 全栈 TS 版 |
| 02. 页面渲染 | JSP 服务端渲染 | Thymeleaf 服务端渲染 | React 组件渲染 | Vue 组件渲染 | Next.js App Router + 客户端组件 | DOM API 手动渲染 | React + Vite 组件渲染 |
| 03. 路由设计 | 后端 Controller 页面跳转 | 后端 Controller 模板跳转 | React Router 前端路由 | Vue Router 前端路由 | Next.js 文件约定路由 | 手写 tab / view 状态切换 | Express API 路由 + 前端路由 |
| 04. 数据流 | `UserController.java` / `AdminController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `UserDaoImpl.java` / `ProductDaoImpl.java` -> `userLogin.jsp` / `products.jsp` | `UserController.java` / `AdminController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `UserDaoImpl.java` / `ProductDaoImpl.java` -> `userLogin.html` / `products.html` | `ApiController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `frontend/src/api.ts` -> `frontend/src/hooks/useAppState.ts` -> `ProductsView.tsx` / `CartView.tsx` | `ApiController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `frontend/src/api.ts` -> `frontend/src/composables/useAppStore.ts` -> `ProductsView.vue` / `CartView.vue` | `ApiController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `frontend/lib/api.ts` -> `frontend/app/page.tsx` | `ApiController.java` -> `UserServiceImpl.java` / `ProductServiceImpl.java` -> `frontend/src/api.ts` -> `frontend/src/services/appService.ts` -> `frontend/src/main.ts` | `apps/api/src/server.ts` -> `apps/api/src/data/store.ts` -> `packages/shared/src/index.ts` -> `apps/web/src/api.ts` -> `apps/web/src/App.tsx` |
| 05. 表单处理 | JSP form 提交到 Controller | Thymeleaf form 绑定和提交 | React 受控表单 | Vue 响应式表单 / 双向绑定 | React 受控表单 + Next 页面交互 | `FormData` + submit 事件 | React 表单 + Express JSON API |
| 06. 状态管理 | Session、Model、后端对象为主 | Model、模板上下文为主 | `useState` / `useEffect` / 自定义 hooks | `ref` / `reactive` / `computed` / composables | React hooks + 页面级状态 | `State` 对象 + `render()` | 前端状态 + 共享 TypeScript 类型 |
| 07. API 通信 | 页面请求和后端渲染耦合 | 页面请求和模板渲染耦合 | 前端通过 HTTP 调 Spring Boot API | 前端通过 HTTP 调 Spring Boot API | Next 前端通过封装 API 调后端 | `fetch` 调 Spring Boot API | React 前端调 Express API |
| 08. 类型体系 | Java 类型为核心 | Java 类型为核心 | Java 后端类型 + TypeScript 前端类型 | Java 后端类型 + TypeScript 前端类型 | Java 后端类型 + TypeScript 前端类型 | Java 后端类型 + TypeScript 前端类型 | 前后端共享 TypeScript 类型 |
| 09. 组件化 | JSP 片段 / include 思路 | Thymeleaf fragment 思路 | React components / hooks | Vue components / composables | Next 页面组件 / 客户端组件 | 函数拆分渲染片段 | React components + shared package |
| 10. 工程化 | Maven + Spring Boot | Maven + Spring Boot + Thymeleaf | Maven 后端 + Vite React 前端 | Maven 后端 + Vite Vue 前端 | Maven 后端 + Next.js 前端 | Maven 后端 + Vite TS 前端 | TypeScript monorepo / workspaces |
| 11. 适合重点 | 理解原始业务、MVC、请求响应 | 理解服务端模板现代化 | 理解 React 前后端分离 | 理解 Vue 3 响应式模型 | 理解 React 应用框架组织 | 理解框架之前的 TS 数据流 | 理解全栈 TypeScript 和类型共享 |

#### 技术目录差异速记

- `JtProject` 和 `JtProject-Thymeleaf` 的学习主线是“后端直接渲染页面”，重点看 Controller、Model、模板语法和页面跳转。
- `JtProject-React`、`JtProject-Vue`、`JtProject-Next` 的学习主线是“后端提供 API，前端负责页面和状态”，重点看组件、路由、表单、API 封装和类型定义。
- `JtProject-React` 和 `JtProject-Vue` 最适合横向比较：一个用 hooks 组织逻辑，一个用 composables 和响应式 API 组织逻辑。
- `JtProject-Next` 适合放在 React 之后看，重点从“组件库写法”升级到“应用框架写法”。
- `JtProject-SpringBoot-TypeScript` 适合补在现代前端框架之前或之后看，重点理解框架帮你封装了哪些 DOM、事件和状态更新细节。
- `JtProject-TypeScript` 适合最后看，重点从“Java 后端 + TS 前端”转到“前后端统一 TypeScript 类型体系”。

相关入口：

- 项目启动总览：[Java项目总启动导航.md](./Java项目总启动导航.md)
- IDEA / 通用文档索引：[doc/README.md](./doc/README.md)
