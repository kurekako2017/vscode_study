# Java 项目根入口

这个目录是 `vscode_study` 里的 Java 项目总入口。

建议先看：

- [Java项目总启动导航.md](./Java项目总启动导航.md)
- [doc/README.md](./doc/README.md)

主要项目：

- `JtProject`：原始 Spring Boot + JSP 版本
- `JtProject-Thymeleaf`：Thymeleaf 学习版
- `JtProject-React`：React + TypeScript 学习版
- `JtProject-Vue`：Vue 3 + TypeScript 学习版

目录说明：

- `JtProject/`：原始项目源码与项目内文档
- `JtProject-Thymeleaf/`：Thymeleaf 改写版源码与学习文档
- `JtProject-React/`：React 前后端分离版源码与文档
- `JtProject-Vue/`：Vue 前后端分离版源码与文档
- `doc/`：`java-projects` 级别的 IDEA 和通用辅助文档
- `data/`：部分项目运行后生成的本地数据目录
- `Java项目总启动导航.md`：总启动入口
- `README.md`：当前这个目录级导航页

如果你只是想尽快跑起来，直接打开上面的总启动导航即可。

## 四个版本对比

这四个项目不是“完全不同的业务”，而是围绕同一套电商业务做的不同技术栈练习。它们最适合拿来对比“同一业务在不同前端/视图技术下，知识点到底差在哪里”。

| 版本 | 主要学习内容 | 核心知识点 | 和其他版本的区别 |
| --- | --- | --- | --- |
| `JtProject` | 原始 Spring Boot + JSP 版本 | Controller 跳转、JSP 标签、Servlet / 请求响应链路、Service / DAO 分层、远程 MySQL 配置 | 最贴近传统 Java Web，前后端耦合最紧，适合先理解“后端如何直接驱动页面” |
| `JtProject-Thymeleaf` | JSP 到 Thymeleaf 的视图层迁移 | `th:text`、`th:if`、`th:each`、`th:href`、模板片段复用、模型数据绑定 | 业务链路基本不变，重点是“视图层替换”；比 JSP 更现代，但仍是服务端渲染 |
| `JtProject-React` | React + TypeScript + Vite 前后端分离 | 组件拆分、Hooks、状态提升、路由、表单控制、API 封装、前后端分离、TypeScript 类型设计 | 前端从“页面模板”变成“组件树 + 状态驱动 UI”，页面交互和数据请求都在前端控制 |
| `JtProject-Vue` | Vue 3 + TypeScript + Vite 前后端分离 | 组合式 API、响应式状态、组件通信、路由、表单控制、API 调用、TypeScript 类型设计 | 和 React 一样是前后端分离，但写法更偏“响应式数据 + 组合函数”，适合对比两种现代前端思路 |

### 一眼看懂的差异

- 如果你想学“传统 Java Web 怎么把请求直接渲染成页面”，先看 `JtProject`
- 如果你想学“服务端模板如何比 JSP 更清晰”，看 `JtProject-Thymeleaf`
- 如果你想学“现代前端如何用组件和状态组织页面”，看 `JtProject-React`
- 如果你想学“Vue 3 的响应式思路和组件组织方式”，看 `JtProject-Vue`

### 按知识点拆开看

| 知识点 | `JtProject` | `JtProject-Thymeleaf` | `JtProject-React` | `JtProject-Vue` |
| --- | --- | --- | --- | --- |
| 页面渲染方式 | JSP 服务端渲染 | Thymeleaf 服务端渲染 | 前端组件渲染 | 前端组件渲染 |
| 数据流向 | 后端 Controller -> JSP | 后端 Controller -> 模板 | 后端 API -> 前端状态 -> 组件 | 后端 API -> 响应式状态 -> 组件 |
| 状态管理 | 主要在后端和会话里 | 主要在后端和模型里 | 前端 state / hooks 管理 | 前端响应式数据 / composables 管理 |
| 表单处理 | JSP 表单 + Controller | 模板表单 + Controller | 受控表单 + 事件回调 | 双向绑定 / 响应式表单 |
| 路由方式 | 后端跳转为主 | 后端跳转为主 | 前端路由切换 | 前端路由切换 |
| 类型体系 | Java 后端类型 | Java 后端类型 | TypeScript 前端类型 | TypeScript 前端类型 |

### 学习顺序建议

1. 先看 `JtProject`，理解原始业务和页面流转
2. 再看 `JtProject-Thymeleaf`，理解服务端模板替换
3. 然后看 `JtProject-React`，理解前后端分离和组件化状态管理
4. 最后看 `JtProject-Vue`，对比 Vue 3 的响应式写法和 React 的区别

如果你的目标是“把同一套业务完整学一遍”，最好的方式不是只看单个项目，而是把这四个版本按上面的顺序串起来看。

相关入口：

- 项目启动总览：[Java项目总启动导航.md](./Java项目总启动导航.md)
- IDEA / 通用文档索引：[doc/README.md](./doc/README.md)
