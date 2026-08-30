# Java Projects 技术路线与 JtProject-TypeScript 升级方针

> 本文作为 `java-projects` 后续项目建设与学习路线的基准文档。以后涉及 `JtProject-TypeScript`、React、Next.js、Node.js、Express、NestJS、TypeScript 和 AWS 时，原则上按本文推进。

## 1. 先明确技术之间的关系

之前容易误解的一点是：**React 并不“属于 TypeScript”**。

正确理解是：

| 技术 | 定位 |
| --- | --- |
| JavaScript | 编程语言 |
| **TypeScript** | JavaScript 的类型化扩展/语言 |
| **React** | 前端 UI Library |
| **Next.js** | 基于 React 的应用框架 |
| **Node.js** | JavaScript / TypeScript 服务端运行环境 |
| **Express** | Node.js Web 框架 |
| **NestJS** | Node.js 企业级后端框架 |
| Vite | 前端构建工具 |
| AWS | 部署 / 云基础设施 |

React 可以使用 JavaScript，也可以使用 TypeScript。本项目采用的是 **React + TypeScript**。

Node.js 也不是另一种 JavaScript；它是 JavaScript/TypeScript 的服务端运行环境。Express 和 NestJS 则是 Node.js 后端框架。

因此，招聘中常见的：

`TypeScript + React/Next.js + Node/NestJS`

更准确地理解为：

```text
                    TypeScript
                        │
              前后端主要开发语言
                        │
          ┌─────────────┴─────────────┐
          │                           │
        前端                         后端
          │                           │
        React                       Node.js
          │                           │
       Next.js                     NestJS
   （React应用框架）          （企业级后端框架）
```

简单记忆：

> **TypeScript 写前后端代码；React / Next.js 负责前端；Node.js + NestJS 负责后端。**

---

## 2. 当前 java-projects 已经覆盖什么

| 项目 | 核心目的 |
| --- | --- |
| `JtProject` | Spring Boot + JSP |
| `JtProject-Thymeleaf` | Spring Boot + Thymeleaf |
| `JtProject-React` | Spring Boot + React + TypeScript |
| `JtProject-Vue` | Spring Boot + Vue + TypeScript |
| `JtProject-Next` | Spring Boot + Next.js + TypeScript |
| `JtProject-SpringBoot-TypeScript` | Spring Boot + 原生 TypeScript |
| `JtProject-TypeScript` | Node.js + Express + React + TypeScript |

因此目前已经有：

- React + TypeScript
- Next.js + TypeScript
- Node.js + Express + TypeScript
- Spring Boot 与多种前端组合

真正明显缺少的是：

> **Node.js + NestJS + TypeScript**

---

## 3. 最终选择方案

### 决定：升级 `JtProject-TypeScript` 补 NestJS

**不新增独立 `JtProject-NestJS`。**

**不新增 `JtProject-AWS`。**

采用：

> **Express + NestJS 并存对照学习，但 NestJS 是最终重点。**

原因：

1. 现有 `JtProject-TypeScript` 已经有 Node.js + Express，不浪费已有成果。
2. Express 适合理解 Node.js Web 后端基础。
3. NestJS 适合企业级项目，也是后续重点。
4. 同一业务横向比较 Express / NestJS / Spring Boot，更容易理解。
5. 避免为了每个框架不断新增完整业务项目。

---

## 4. JtProject-TypeScript 升级后的定位

升级后定义为：

> **TypeScript 全栈综合学习项目：React + TypeScript + Node.js + Express + NestJS + Shared Types**

建议结构：

```text
JtProject-TypeScript/
│
├── apps/
│   ├── web/
│   │   ├── React
│   │   ├── TypeScript
│   │   └── Vite
│   │
│   ├── api-express/
│   │   ├── Node.js
│   │   ├── Express
│   │   └── TypeScript
│   │
│   └── api-nestjs/
│       ├── Node.js
│       ├── NestJS
│       └── TypeScript
│
└── packages/
    └── shared/
        └── 前后端共享 TypeScript 类型
```

| 目录 | 技术 | 定位 |
| --- | --- | --- |
| `apps/web` | React + TypeScript + Vite | 前端 |
| `apps/api-express` | Node.js + Express + TypeScript | 基础 / 对照 |
| `apps/api-nestjs` | Node.js + NestJS + TypeScript | **重点 / 最终主后端** |
| `packages/shared` | TypeScript | DTO / interface / API 类型共享 |

技术关系应画成：

```text
                 JtProject-TypeScript
                        │
                 语言：TypeScript
                        │
          ┌─────────────┴─────────────┐
          │                           │
        前端                         后端
          │                           │
        React                       Node.js
          │                           │
        Vite                ┌─────────┴─────────┐
                            │                   │
                         Express             NestJS
                         基础对照             ★重点
```

这里不是“多个 JS”，主要开发语言仍然是 TypeScript。

---

## 5. Express + NestJS 为什么不会增加太大学习负担

关键是：**不要把两个后端都当成同等规模、长期同时维护的主项目。**

不采用：

```text
Express 完整功能 100%
+
NestJS 再完整重写 100%
```

而采用：

```text
现有 Express
    ↓
理解 Node.js / Router / Middleware / Request / Response
    ↓
作为基础参照保留
    ↓
选择代表性业务迁移到 NestJS
    ↓
重点学习 NestJS
    ↓
以后主要扩展 NestJS
```

Express 的定位：

- Router
- Middleware
- Request / Response
- Node.js Web API 基础
- Service 如何手工组织

NestJS 的重点：

- Controller
- Service
- Module
- Dependency Injection
- DTO
- Validation
- Guard
- Interceptor
- Exception Filter
- Repository / DB
- 企业级模块化结构

---

## 6. Express / NestJS / Spring Boot 对照

| 功能 | Express | NestJS | Spring Boot |
| --- | --- | --- | --- |
| HTTP入口 | Router | Controller | Controller |
| GET | `router.get()` | `@Get()` | `@GetMapping` |
| 业务层 | 自己组织 | Service | Service |
| DI | 自己处理 | 内置 DI | Spring DI |
| 模块 | 自己组织 | Module | Configuration / Component |
| DTO | TS interface/type | DTO class | Java DTO |
| Validation | 中间件等 | Pipe / class-validator | Bean Validation |
| 权限控制 | Middleware 等 | Guard | Spring Security |
| 异常处理 | Middleware | Exception Filter | ExceptionHandler |
| 企业项目结构 | 自己规定 | 框架规定 | 框架规定 |

同一业务：

```text
Express

GET /products
     ↓
Router
     ↓
Handler
     ↓
ProductService
     ↓
Store / DB
```

```text
NestJS

GET /products
     ↓
ProductController
     ↓
ProductService
     ↓
Repository / DB
```

```text
Spring Boot

GET /products
     ↓
ProductController
     ↓
ProductService
     ↓
ProductRepository
     ↓
DB
```

对已有 Spring Boot 经验的人，NestJS 的重点不是重新学习后端开发，而是把 Controller / Service / DI / DTO / 分层思想迁移到 TypeScript + Node.js。

---

## 7. Next.js 的处理方案

Next.js 已经由：

`JtProject-Next`

负责学习：

```text
Next.js
   ↓
React
   ↓
TypeScript
   ↓
Spring Boot API
```

所以暂时不需要为了 NestJS 再复制一套 Next.js 项目。

`JtProject-TypeScript` 重点负责：

```text
React + TypeScript
        ↓
Node.js
   ├── Express（基础对照）
   └── NestJS（★重点）
```

整个 `java-projects` 合起来已经可以覆盖：

```text
TypeScript
├── React
├── Next.js
├── Node.js
├── Express
└── NestJS
```

以后需要理解现代 TypeScript 全栈时，把两部分知识组合：

```text
JtProject-Next
Next.js + React + TypeScript
             ↓
          REST API
             ↓
JtProject-TypeScript
Node.js + NestJS + TypeScript
             ↓
             DB
```

---

## 8. AWS 不建立独立项目

AWS 属于部署 / 云基础设施层，不属于 React、Next.js、NestJS 这种业务开发框架。

因此不创建：

`JtProject-AWS`

而是以后作为现有项目的横向部署章节：

```text
                  AWS
                   │
      ┌────────────┼────────────┐
      │            │            │
Spring Boot     React/Next    Node/NestJS
      │            │            │
 EC2/ECS      S3/CloudFront   EC2/ECS
      │                         │
      └───────────┬─────────────┘
                  │
                 RDS
                  │
            CloudWatch
                  │
                 IAM
```

可逐步学习：

- EC2
- ECS / Docker
- RDS
- S3
- CloudFront
- IAM
- CloudWatch
- CI/CD
- GitHub Actions / CodePipeline

原则：

> **AWS 是所有项目都可以使用的部署能力，不单独复制一套业务项目。**

---

## 9. 后续学习与实施顺序

### 第一阶段：现有 Express

先理解：

```text
React + TypeScript
        ↓
HTTP / JSON
        ↓
Node.js + Express + TypeScript
```

重点：

- Node.js
- Router
- Request / Response
- Middleware
- Service
- API
- shared types

### 第二阶段：Express → NestJS 对照迁移

```text
Express Router
      ↓
NestJS Controller

Handler
      ↓
Controller Method

Service
      ↓
@Injectable Service

手工依赖
      ↓
Dependency Injection

手工目录组织
      ↓
Module
```

### 第三阶段：NestJS 作为重点

```text
Controller
↓
Service
↓
Module
↓
Dependency Injection
↓
DTO
↓
Validation
↓
Guard
↓
Interceptor
↓
Exception Filter
↓
Repository / DB
```

### 第四阶段：形成现代 TypeScript 全栈知识

```text
              TypeScript
                  │
       ┌──────────┴──────────┐
       │                     │
      前端                   后端
       │                     │
 React / Next.js           Node.js
       │                     │
       │                   NestJS
       │                     │
       └────── REST API ─────┘
                  │
                  DB
                  │
                 AWS
```

---

## 10. 后续统一实施基准

以后修改 `JtProject-TypeScript`、README、学习教程或让 Codex 实施代码时，默认遵循：

1. 保留现有七个项目。
2. **不新增独立 `JtProject-NestJS`。**
3. **升级 `JtProject-TypeScript` 增加 NestJS。**
4. Express 保留，但仅作为 Node.js 基础和 NestJS 对照。
5. NestJS 是 `JtProject-TypeScript` 后续主要后端学习方向。
6. `JtProject-Next` 继续负责 Next.js + React + TypeScript。
7. AWS 作为横向部署能力，不创建独立业务项目。
8. 不为了框架数量重复建设同一套完整业务。
9. 尽量使用同一业务做 Express / NestJS / Spring Boot 横向比较。
10. 最终重点覆盖 SES 现代 TypeScript 全栈路线：

```text
React / Next.js + TypeScript
             ↓
Node.js + NestJS + TypeScript
             ↓
             DB
             ↓
            AWS
```

### 一句话记忆

> **TypeScript 是语言；React 是前端 UI Library；Next.js 是 React 应用框架；Node.js 是后端运行环境；Express 是基础 Node Web 框架；NestJS 是重点企业级 Node 后端框架；AWS 是部署层。**
