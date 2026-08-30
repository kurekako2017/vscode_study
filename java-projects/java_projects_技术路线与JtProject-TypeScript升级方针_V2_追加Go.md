# Java Projects 技术路线与 JtProject-TypeScript 升级方针

> 本文作为 `java-projects` 后续项目建设与学习路线的基准文档。以后涉及 `JtProject-TypeScript`、React、Next.js、Node.js、Express、NestJS、TypeScript 和 AWS 时，原则上按本文推进。

## 1. 先明确技术之间的关系

之前容易误解的一点是：**React 并不“属于 TypeScript”**。

正确理解是：

| 技术                 | 定位                                   |
| -------------------- | -------------------------------------- |
| JavaScript           | 编程语言                               |
| **TypeScript** | JavaScript 的类型化扩展/语言           |
| **React**      | 前端 UI Library                        |
| **Next.js**    | 基于 React 的应用框架                  |
| **Node.js**    | JavaScript / TypeScript 服务端运行环境 |
| **Express**    | Node.js Web 框架                       |
| **NestJS**     | Node.js 企业级后端框架                 |
| Vite                 | 前端构建工具                           |
| AWS                  | 部署 / 云基础设施                      |

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

| 项目                                | 核心目的                               |
| ----------------------------------- | -------------------------------------- |
| `JtProject`                       | Spring Boot + JSP                      |
| `JtProject-Thymeleaf`             | Spring Boot + Thymeleaf                |
| `JtProject-React`                 | Spring Boot + React + TypeScript       |
| `JtProject-Vue`                   | Spring Boot + Vue + TypeScript         |
| `JtProject-Next`                  | Spring Boot + Next.js + TypeScript     |
| `JtProject-SpringBoot-TypeScript` | Spring Boot + 原生 TypeScript          |
| `JtProject-TypeScript`            | Node.js + Express + React + TypeScript |

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

| 目录                 | 技术                           | 定位                           |
| -------------------- | ------------------------------ | ------------------------------ |
| `apps/web`         | React + TypeScript + Vite      | 前端                           |
| `apps/api-express` | Node.js + Express + TypeScript | 基础 / 对照                    |
| `apps/api-nestjs`  | Node.js + NestJS + TypeScript  | **重点 / 最终主后端**    |
| `packages/shared`  | TypeScript                     | DTO / interface / API 类型共享 |

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

| 功能         | Express           | NestJS                 | Spring Boot               |
| ------------ | ----------------- | ---------------------- | ------------------------- |
| HTTP入口     | Router            | Controller             | Controller                |
| GET          | `router.get()`  | `@Get()`             | `@GetMapping`           |
| 业务层       | 自己组织          | Service                | Service                   |
| DI           | 自己处理          | 内置 DI                | Spring DI                 |
| 模块         | 自己组织          | Module                 | Configuration / Component |
| DTO          | TS interface/type | DTO class              | Java DTO                  |
| Validation   | 中间件等          | Pipe / class-validator | Bean Validation           |
| 权限控制     | Middleware 等     | Guard                  | Spring Security           |
| 异常处理     | Middleware        | Exception Filter       | ExceptionHandler          |
| 企业项目结构 | 自己规定          | 框架规定               | 框架规定                  |

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

---

# 11. Go 语言版本追加方案（SES 案件导向）

## 11.1 为什么追加 Go

后续 `java-projects` 再追加一个 Go 版本是有价值的，但定位应和前面的 TypeScript 学习路线不同。

Go 更适合补强以下 SES / フリーランス案件方向：

- 高并发 Web API
- 微服务
- 云原生后端
- AWS / GCP 上的后端服务
- Docker / Kubernetes
- API Gateway 后端
- 大规模业务系统的后端服务拆分
- 金融、支付、EC、SaaS 等高并发服务

因此 Go 版本不应该只是：

```text
把 Java Spring Boot 代码机械改写成 Go
```

而应该作为：

> **“现代云原生后端 + React/Next.js 前端”学习版本**

来建设。

---

## 11.2 从 SES 案件需求看 Go 的定位

2026 年日本 SES / フリーランス市场中，Go 的案件总量通常少于 Java，但单价和稀缺性表现较好。

因此学习策略不是用 Go 替代 Java，而是形成：

```text
Java / Spring Boot
    ↓
传统企业系统、金融、公共、大型业务系统

TypeScript / NestJS
    ↓
现代 Web / SaaS / 前后端 TypeScript

Go
    ↓
高并发 API / 微服务 / 云原生 / AWS
```

三条路线互补。

### 建议定位

Go 版本重点不是前端框架本身，而是：

```text
前端：
React / Next.js + TypeScript

后端：
Go

后端框架：
Gin 为主

数据访问：
GORM 或 sqlc

数据库：
PostgreSQL

基础设施：
Docker
AWS（后续部署）
```

---

# 12. 新增项目建议：`JtProject-Go`

与 NestJS 不同，Go 建议新增一个独立项目：

```text
JtProject-Go
```

原因是：

- Go 是新的编程语言，不只是 Node.js 下换一个框架。
- 代码结构、错误处理、并发模型、依赖管理、编译方式都与 Java/TypeScript 不同。
- 如果直接塞进 `JtProject-TypeScript`，反而会破坏项目边界。
- 独立版本更方便和 Spring Boot、NestJS 做横向比较。

因此后续项目体系可以变为：

```text
JtProject
JtProject-Thymeleaf
JtProject-React
JtProject-Vue
JtProject-Next
JtProject-SpringBoot-TypeScript
JtProject-TypeScript
JtProject-Go
```

---

# 13. `JtProject-Go` 推荐技术栈

## 13.1 最推荐方案

```text
Frontend
Next.js
React
TypeScript
    ↓
REST API
    ↓
Backend
Go
Gin
    ↓
Service
Repository
    ↓
PostgreSQL
```

建议技术栈：

| 层           | 技术                        |
| ------------ | --------------------------- |
| 前端语言     | TypeScript                  |
| 前端 UI      | React                       |
| 前端框架     | Next.js                     |
| 后端语言     | Go                          |
| Web 框架     | Gin                         |
| ORM / DB访问 | GORM（入门）→ sqlc（后续） |
| DB           | PostgreSQL                  |
| API          | REST API                    |
| API 文档     | OpenAPI / Swagger           |
| 配置         | env                         |
| 日志         | slog / zap                  |
| 测试         | Go testing                  |
| 容器         | Docker / Docker Compose     |
| 云部署       | AWS（后续横向部署）         |

---

# 14. 为什么 Go 后端建议首先用 Gin

Go 本身的标准库已经可以开发 HTTP 服务。

但为了学习效率和日本实际项目可读性，第一版建议：

```text
Go + Gin
```

原因：

- API 路由简单
- Middleware 清晰
- 学习成本低
- 容易理解 Go Web 开发
- 适合从 Spring Boot / NestJS 横向比较

不要一开始堆太多框架。

第一阶段不建议同时学习：

```text
Gin
Echo
Fiber
Chi
```

而应该：

```text
Gin = 主学习框架
```

其他框架以后只做概念比较。

---

# 15. Go 前后台整体框架

建议最终形成：

```text
                    JtProject-Go
                         │
          ┌──────────────┴──────────────┐
          │                             │
        Frontend                      Backend
          │                             │
      TypeScript                        Go
          │                             │
        React                          Gin
          │                             │
       Next.js                     Controller
                                        │
                                     Service
                                        │
                                   Repository
                                        │
                                  PostgreSQL
```

实际请求链路：

```text
Browser
   ↓
Next.js / React
   ↓
fetch / REST API
   ↓
Go Gin Router
   ↓
Handler / Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

---

# 16. 推荐目录结构

```text
JtProject-Go/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   ├── cmd/
│   │   └── api/
│   │       └── main.go
│   │
│   ├── internal/
│   │   ├── handler/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── model/
│   │   ├── middleware/
│   │   └── config/
│   │
│   ├── pkg/
│   ├── go.mod
│   └── go.sum
│
├── docker/
│
├── docker-compose.yml
│
└── README.md
```

其中：

```text
handler
   ≈ Spring Boot Controller
   ≈ NestJS Controller

service
   ≈ Spring Boot Service
   ≈ NestJS Service

repository
   ≈ Spring Data Repository
   ≈ NestJS Repository

model
   ≈ Java Entity / DTO
```

---

# 17. Spring Boot / NestJS / Go Gin 横向比较

| 功能     | Spring Boot       | NestJS            | Go + Gin                |
| -------- | ----------------- | ----------------- | ----------------------- |
| 语言     | Java              | TypeScript        | Go                      |
| HTTP入口 | Controller        | Controller        | Handler                 |
| 路由     | `@GetMapping`   | `@Get()`        | `router.GET()`        |
| Service  | `@Service`      | `@Injectable()` | struct + method         |
| DI       | Spring DI         | Nest DI           | 手工注入 / Wire 等      |
| DTO      | Java class        | TS class          | Go struct               |
| JSON     | Jackson           | 内置序列化        | `encoding/json` / Gin |
| ORM      | JPA               | TypeORM/Prisma    | GORM                    |
| DB       | PostgreSQL/MySQL  | PostgreSQL/MySQL  | PostgreSQL/MySQL        |
| 并发     | Thread / Executor | Event Loop        | Goroutine               |
| 构建     | Maven/Gradle      | npm/pnpm          | `go build`            |
| 部署     | JVM               | Node.js           | 单一二进制              |
| 典型方向 | 企业系统          | Web/SaaS          | 微服务/高并发/云原生    |

---

# 18. Go 学习重点

Go 版本不能只学习 API CRUD。

必须重点掌握：

## 18.1 Go 语言基础

```text
package
变量
struct
interface
pointer
slice
map
method
error
defer
context
```

## 18.2 Go 特有重点

```text
goroutine
channel
context.Context
并发控制
错误处理
interface
组合优于继承
```

这些才是 Go 和 Java / TypeScript 真正拉开差异的地方。

## 18.3 Web API

```text
Gin Router
Handler
Middleware
Request
Response
JSON
Validation
Error handling
```

## 18.4 DB

第一阶段：

```text
PostgreSQL
+
GORM
```

后续可以追加：

```text
database/sql
sqlc
transaction
connection pool
```

## 18.5 工程化

```text
go mod
go test
Docker
config
logging
OpenAPI
health check
graceful shutdown
```

---

# 19. Go 版本业务修改范围

Go 版本继续使用 `JtProject` 的同一套电商业务，不重新设计新业务。

但实现方式应更偏 API / 微服务风格。

建议优先迁移：

```text
用户
├── 登录
├── 用户信息
└── 权限

商品
├── 商品列表
├── 商品详情
└── 商品检索

购物车
├── 加入购物车
├── 修改数量
└── 删除

订单
├── 创建订单
├── 查询订单
└── 订单状态
```

第一阶段仍然可以保持：

```text
一个 Go API 服务
```

不要一开始真的拆成多个微服务。

---

# 20. Go 微服务学习阶段

当单体 Go API 学完后，再追加微服务章节：

```text
                API Gateway
                     │
        ┌────────────┼────────────┐
        │            │            │
     User API     Product API   Order API
        │            │            │
       Go           Go           Go
        │            │            │
     PostgreSQL   PostgreSQL   PostgreSQL
```

学习重点：

- REST API
- 服务拆分
- API Gateway
- Context
- Timeout
- Retry
- Circuit Breaker 概念
- gRPC
- Docker
- Kubernetes 概念
- AWS ECS / EKS 概念

但：

> **微服务属于 Go 第二阶段，不作为最开始学习的前提。**

---

# 21. Go 与 AWS 的关系

仍然遵守前面的原则：

> **AWS 不建立独立 `JtProject-AWS`。**

Go 后端后续可部署为：

```text
Next.js / React
      │
 CloudFront / S3
      │
      ↓
API Gateway / ALB
      │
      ↓
Go API
EC2 / ECS
      │
      ↓
RDS PostgreSQL
      │
      ↓
CloudWatch
```

Go 特别适合作为：

```text
Docker
+
ECS
+
RDS
```

的实战对象。

后续再进阶：

```text
EKS / Kubernetes
```

---

# 22. Go 版本学习顺序

推荐：

```text
01 Go 基础
↓
02 struct / interface / error
↓
03 goroutine / channel / context
↓
04 Gin REST API
↓
05 Controller/Handler → Service → Repository
↓
06 PostgreSQL + GORM
↓
07 React/Next.js 调 Go API
↓
08 Validation / Middleware / Error
↓
09 Testing
↓
10 Docker
↓
11 AWS ECS / RDS
↓
12 Microservices / gRPC
```

不要一开始同时学习 Kubernetes、gRPC、微服务。

---

# 23. 最终 java-projects 技术地图

后续整体学习路线形成：

```text
                         java-projects
                              │
        ┌─────────────────────┼──────────────────────┐
        │                     │                      │
   Java / Spring        TypeScript 全栈          Go 全栈
        │                     │                      │
  Spring Boot             React                  React
        │                   │                      │
 JSP/Thymeleaf           Next.js                Next.js
 React/Vue/Next            │                      │
                            │                      │
                         Node.js                   Go
                            │                      │
                    Express → NestJS              Gin
                    基础       ★重点               │
                                                   │
                                             PostgreSQL
        │                     │                      │
        └─────────────────────┴──────────────────────┘
                              │
                             AWS
                       （横向部署能力）
```

---

# 24. SES 导向下的三条主线

今后不要把所有技术混成一条路线。

应分成三条：

### A. Java 企业系统路线

```text
Java
+
Spring Boot
+
SQL
+
AWS
```

适合：

- 银行
- 金融
- 公共
- 大型企业系统
- 长期维护和迁移案件

### B. TypeScript 现代 Web 全栈路线

```text
TypeScript
+
React / Next.js
+
Node.js / NestJS
+
AWS
```

适合：

- SaaS
- Web 服务
- 新规开发
- Startup / Web 系统
- 前后端全栈

### C. Go 云原生后端路线

```text
Go
+
Gin
+
PostgreSQL
+
Docker
+
AWS
```

前端配：

```text
React / Next.js + TypeScript
```

适合：

- 高并发 API
- 微服务
- 云原生
- 支付
- EC
- SaaS 后端
- 大规模 Web 服务

---

# 25. Go 版本最终实施基准

后续如果开始建设 `JtProject-Go`，默认遵循：

1. 新增独立 `JtProject-Go`，因为 Go 是新语言，不塞入 `JtProject-TypeScript`。
2. 继续复用现有电商业务。
3. 前端采用 **React / Next.js + TypeScript**。
4. 后端采用 **Go + Gin**。
5. DB 优先 PostgreSQL。
6. 第一阶段 ORM 使用 GORM，后续再学习 `database/sql` / sqlc。
7. 第一阶段做模块化单体，不一开始拆微服务。
8. 第二阶段再学习微服务 / gRPC / Kubernetes。
9. Docker 和 AWS 作为部署实战加入。
10. AWS 仍然不是独立业务项目。
11. Go 学习重点必须包含 goroutine / channel / context，而不是只做 CRUD。
12. 通过 Spring Boot / NestJS / Go Gin 横向比较学习。

最终目标：

```text
React / Next.js + TypeScript
             ↓
          REST API
             ↓
          Go + Gin
             ↓
        PostgreSQL
             ↓
      Docker + AWS
```

这将作为 Go 语言版本未来建设和学习的基准方案。
