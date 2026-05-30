# Java 项目总启动导航

相关入口：

- 项目根入口：[README.md](./README.md)
- IDEA / 通用文档索引：[doc/README.md](./doc/README.md)

这个目录里现在主要有 6 个相关项目：

- `JtProject`：原始 Spring Boot + JSP 项目
- `JtProject-Thymeleaf`：独立复制版，页面模板改为 Thymeleaf
- `JtProject-React`：独立复制版，前端改为 React + TypeScript
- `JtProject-Vue`：独立复制版，前端改为 Vue 3 + TypeScript
- `JtProject-Next`：独立复制版，前端改为 Next.js + TypeScript
- `JtProject-TypeScript`：独立复制版，改为 Node.js + Express + React 的纯 TypeScript 全栈项目

---

## 我现在该启动哪个项目

如果你的目标是：

- 看原始电商项目最早的页面和 Controller 写法：启动 `JtProject`
- 学习 JSP 页面怎么迁移到模板引擎：启动 `JtProject-Thymeleaf`
- 学习 React 版前后端分离写法：启动 `JtProject-React`
- 学习 Vue 版前后端分离写法：启动 `JtProject-Vue`
- 学习 Next.js 版前后端分离写法：启动 `JtProject-Next`
- 学习纯 TypeScript 全栈写法：启动 `JtProject-TypeScript`

最常见的选择建议：

- 想看“最原始版本”时，先跑 `JtProject`
- 想做 JSP 和 Thymeleaf 对照时，同时看 `JtProject` 和 `JtProject-Thymeleaf`
- 想学现代前端页面组织方式时，跑 `JtProject-React` 或 `JtProject-Vue`

---

## 启动前准备

建议先确认本机环境：

- 已安装 Java 和 Maven Wrapper 可用
- 需要运行前端项目时，已安装 Node.js 和 npm
- PowerShell 当前工作区是 `d:\dev\source_code\vscode_study`

默认测试账号：

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

---

## 1. 原始项目：JtProject

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject
```

启动后端：

```powershell
.\mvnw.cmd spring-boot:run
```

访问地址：

```text
http://localhost:8082/
```

说明：

- 这是原始 JSP 版本
- 使用远程 MySQL：`192.168.10.2:3306/ecommjava`

学习入口：

- [JtProject/README.md](JtProject/README.md)

---

## 2. Thymeleaf 项目：JtProject-Thymeleaf

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Thymeleaf
```

启动后端：

```powershell
.\mvnw.cmd spring-boot:run
```

访问地址：

```text
http://localhost:8085/
```

H2 控制台：

```text
http://localhost:8085/h2-console
```

说明：

- 这是 Thymeleaf 学习版
- 默认使用 `templates/*.html`
- 数据库改为本地 H2 文件库
- 适合对照学习 JSP 页面如何迁移到 Thymeleaf

学习入口：

- [JtProject-Thymeleaf/README.md](JtProject-Thymeleaf/README.md)
- [JtProject-Thymeleaf/doc/reference/Thymeleaf学习指南.md](JtProject-Thymeleaf/doc/reference/Thymeleaf学习指南.md)
- [JtProject-Thymeleaf/doc/reference/JSP页面 vs Thymeleaf页面逐页对照.md](JtProject-Thymeleaf/doc/reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)

---

## 3. React 项目：JtProject-React

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React
```

启动后端：

```powershell
.\mvnw.cmd spring-boot:run
```

后端地址：

```text
http://localhost:8083/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React\frontend
npm install
npm run dev
```

前端地址：

```text
http://localhost:5173/
```

说明：

- 这是独立复制出来的 React 学习项目
- 后端仍然是 Spring Boot
- 数据库改为本地 H2 文件库

学习入口：

- [JtProject-React/README.md](JtProject-React/README.md)
- [JtProject-React/docs/README.md](JtProject-React/docs/README.md)

---

## 4. Vue 项目：JtProject-Vue

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue
```

启动后端：

```powershell
.\mvnw.cmd spring-boot:run
```

后端地址：

```text
http://localhost:8084/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue\frontend
npm install
npm run dev
```

前端地址：

```text
http://localhost:5174/
```

说明：

- 这是独立复制出来的 Vue 学习项目
- 后端仍然是 Spring Boot
- 数据库改为本地 H2 文件库

学习入口：

- [JtProject-Vue/README.md](JtProject-Vue/README.md)
- [JtProject-Vue/docs/README.md](JtProject-Vue/docs/README.md)

---

## 5. Next.js 项目：JtProject-Next

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next
```

启动后端：

```powershell
.\mvnw.cmd spring-boot:run
```

后端地址：

```text
http://localhost:8086/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next\frontend
npm install
npm run dev
```

前端地址：

```text
http://localhost:3000/
```

说明：

- 这是独立复制出来的 Next.js 学习项目
- 后端仍然是 Spring Boot
- 数据库改为本地 H2 文件库

学习入口：

- [JtProject-Next/README.md](JtProject-Next/README.md)

---

## 6. 纯 TypeScript 全栈项目：JtProject-TypeScript

项目目录：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-TypeScript
```

安装依赖：

```powershell
npm install
```

同时启动前后端：

```powershell
npm run dev
```

后端地址：

```text
http://localhost:8090/api
```

前端地址：

```text
http://localhost:5175/
```

说明：

- 这是独立复制出来的纯 TypeScript 全栈学习项目
- 后端使用 Node.js + Express + TypeScript
- 前端使用 React + Vite + TypeScript
- `packages/shared` 保存前后端共享类型
- 初始业务数据来自原始 `JtProject` 的 `data.sql`

学习入口：

- [JtProject-TypeScript/README.md](JtProject-TypeScript/README.md)
- [JtProject-TypeScript/docs/fullstack-typescript-flow.md](JtProject-TypeScript/docs/fullstack-typescript-flow.md)

---

## 端口速查

| 项目 | 后端/页面地址 | 前端地址 |
| --- | --- | --- |
| `JtProject` | `http://localhost:8082/` | 无 |
| `JtProject-Thymeleaf` | `http://localhost:8085/` | 无 |
| `JtProject-React` | `http://localhost:8083/api` | `http://localhost:5173/` |
| `JtProject-Vue` | `http://localhost:8084/api` | `http://localhost:5174/` |
| `JtProject-Next` | `http://localhost:8086/api` | `http://localhost:3000/` |
| `JtProject-TypeScript` | `http://localhost:8090/api` | `http://localhost:5175/` |

---

## 最快启动命令速查

### 1. 只启动原始 JSP 项目

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject
.\mvnw.cmd spring-boot:run
```

打开：

```text
http://localhost:8082/
```

### 2. 只启动 Thymeleaf 项目

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Thymeleaf
.\mvnw.cmd spring-boot:run
```

打开：

```text
http://localhost:8085/
```

### 3. 启动 React 项目

后端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React
.\mvnw.cmd spring-boot:run
```

前端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React\frontend
npm install
npm run dev
```

打开：

```text
http://localhost:5173/
```

### 4. 启动 Vue 项目

后端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue
.\mvnw.cmd spring-boot:run
```

前端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue\frontend
npm install
npm run dev
```

打开：

```text
http://localhost:5174/
```

### 5. 启动 Next.js 项目

后端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next
.\mvnw.cmd spring-boot:run
```

前端窗口：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Next\frontend
npm install
npm run dev
```

打开：

```text
http://localhost:3000/
```

### 6. 启动纯 TypeScript 全栈项目

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-TypeScript
npm install
npm run dev
```

打开：

```text
http://localhost:5175/
```

### 7. 想同时对照学习两套页面

推荐组合：

- `JtProject` + `JtProject-Thymeleaf`
- `JtProject` + `JtProject-React`
- `JtProject` + `JtProject-Vue`
- `JtProject` + `JtProject-Next`
- `JtProject` + `JtProject-TypeScript`

这样最容易对照同一套业务在不同视图技术里的写法差异。

---

## 推荐学习顺序

1. 先运行 `JtProject`，理解 JSP 版本原始页面结构
2. 再运行 `JtProject-Thymeleaf`，对照学习 JSP 页面如何改写成 Thymeleaf
3. 再运行 `JtProject-React`，对照学习 React 的组件、路由、hooks
4. 再运行 `JtProject-Vue`，对照学习 Vue 的组件、路由、composables
5. 再运行 `JtProject-Next`，对照学习 Next.js 的 App Router 和 React 应用框架写法
6. 最后运行 `JtProject-TypeScript`，对照学习纯 TypeScript 全栈写法

---

## 常见问题排查

### 1. 端口被占用

如果启动时提示 `Port already in use`，说明对应端口已经被别的进程占用了。

本目录常用端口：

- `8082`：`JtProject`
- `8083`：`JtProject-React` 后端
- `8084`：`JtProject-Vue` 后端
- `8085`：`JtProject-Thymeleaf`
- `8086`：`JtProject-Next` 后端
- `8090`：`JtProject-TypeScript` 后端
- `3000`：`JtProject-Next` 前端
- `5173`：`JtProject-React` 前端
- `5174`：`JtProject-Vue` 前端
- `5175`：`JtProject-TypeScript` 前端

可以先在 PowerShell 里查看端口占用：

```powershell
netstat -ano | findstr :8085
netstat -ano | findstr :5173
```

如果确认是旧进程占用，再去任务管理器或用 `taskkill` 停掉对应 PID。

### 2. 第一次启动比较慢

第一次运行 `.\mvnw.cmd spring-boot:run` 或 `npm install` 时，通常会下载依赖，所以慢一些是正常的。

常见现象：

- Maven 首次下载依赖
- Node.js 首次下载前端依赖
- H2 数据文件首次创建

如果控制台还在持续输出日志，通常说明不是卡死，而是在准备依赖。

### 3. `mvnw.cmd` 无法运行

如果 PowerShell 提示找不到 `.\mvnw.cmd`，一般有两种原因：

- 当前目录不对
- 项目文件没有完整打开

先确认你已经切到对应项目目录，例如：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Thymeleaf
Get-ChildItem mvnw.cmd
```

如果能看到 `mvnw.cmd`，再执行启动命令。

### 4. 前端项目启动失败

`JtProject-React` 和 `JtProject-Vue` 需要分别启动前端。

标准顺序：

```powershell
cd 对应项目\frontend
npm install
npm run dev
```

如果 `npm run dev` 失败，优先检查：

- 是否已经先执行过 `npm install`
- Node.js 版本是否可用
- `frontend` 目录是否切对了

### 5. 页面能打开但接口报错

这类问题通常是后端没启动，或者前端和后端没有同时运行。

例如：

- React 页面能打开，但商品列表加载失败
- Vue 页面能打开，但登录请求报错

这时通常要确认两件事：

1. Spring Boot 后端是否还在运行
2. 前端开发服务器是否也在运行

对于 React 和 Vue 项目，前后端缺一不可。

### 6. 数据库连接失败

不同项目的数据库来源不同：

- `JtProject`：偏向原始项目配置，可能使用远程 MySQL
- `JtProject-Thymeleaf`：本地 H2 文件库
- `JtProject-React`：本地 H2 文件库
- `JtProject-Vue`：本地 H2 文件库
- `JtProject-Next`：本地 H2 文件库
- `JtProject-TypeScript`：内存数据仓库，重启后恢复初始数据

如果是 `JtProject` 启动时报数据库连接错误，要优先检查：

- 远程数据库地址是否可达
- 用户名密码是否正确
- 当前使用的 profile 是否正确

如果是另外三个学习版项目，一般先看本地 H2 文件是否能正常创建，以及配置文件是否被误改。

### 7. 该先看哪个 README

如果你只是想快速跑起来，优先看各项目根目录下的 `README.md`：

- [JtProject/README.md](JtProject/README.md)
- [JtProject-Thymeleaf/README.md](JtProject-Thymeleaf/README.md)
- [JtProject-React/README.md](JtProject-React/README.md)
- [JtProject-Vue/README.md](JtProject-Vue/README.md)
- [JtProject-Next/README.md](JtProject-Next/README.md)
- [JtProject-TypeScript/README.md](JtProject-TypeScript/README.md)

总原则是：

- 先看本总览文档，知道每个项目做什么
- 再进具体项目看对应 `README.md`
- 启动异常时再看该项目下更详细的说明文档
