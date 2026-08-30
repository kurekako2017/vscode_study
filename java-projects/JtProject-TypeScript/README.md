# JtProject-TypeScript：React + Express + NestJS 学习版

## 1. 当前项目技术结构

当前项目保留原有的 Express 方案，同时新增 NestJS 作为企业级框架对照学习入口：

- React + TypeScript + Vite
- Node.js + Express + TypeScript
- Node.js + NestJS + TypeScript
- 共享类型：packages/shared

## 2. 为什么保留 Express

Express 仍然保留，原因是它非常适合帮助理解 Node.js Web 基础：

- Router：路由注册和中间件是 Express 的核心概念
- Middleware：请求进入 Controller 前的统一处理
- Request / Response：HTTP 请求和响应对象的直接使用方式
- 与 NestJS 对照：最容易看出 Controller 和 Service 的职责分层

本次学习中，Express 继续作为原业务入口保留，方便做横向对照：

Express Router
↓
NestJS Controller
↓
Spring Boot Controller

## 3. 为什么新增 NestJS

NestJS 作为新增学习分支，重点放在企业项目结构与依赖注入：

- Controller
- Service
- Module
- Dependency Injection
- DTO
- Validation
- 统一异常处理
- 标准企业布局

它和 Spring Boot 更接近，适合把“手写 Express + 轻量业务逻辑”升级为“可维护的框架组织方式”。

## 4. Express 启动方法

```bash
cd java-projects/JtProject-TypeScript
npm install
npm run start:api
```

默认端口：

- Express: http://localhost:8090/api

## 5. NestJS 启动方法

```bash
cd java-projects/JtProject-TypeScript
npm install
npm --workspace apps/api-nestjs run start:dev
```

默认端口：

- NestJS: http://localhost:3002/api

## 6. React 启动方法

```bash
cd java-projects/JtProject-TypeScript
npm install
npm --workspace apps/web run dev -- --host 0.0.0.0
```

默认端口：

- React: http://localhost:5175

## 7. 各端口

| 角色 | 地址 | 说明 |
| --- | --- | --- |
| Express | http://localhost:8090/api | 原项目保留 |
| NestJS | http://localhost:3002/api | 新增学习框架 |
| React | http://localhost:5175 | 前端开发服务器 |

## 8. API 切换方式

前端默认还是指向原 Express：

```ts
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8090/api'
```

如果要切换到 NestJS，可以在启动前设置：

```bash
VITE_API_BASE_URL=http://localhost:3002/api npm --workspace apps/web run dev -- --host 0.0.0.0
```

也可以在本地 `.env` 中声明：

```env
VITE_API_BASE_URL=http://localhost:3002/api
```

这样 React 可以快速切换使用 Express 或 NestJS，便于对照学习。

## 9. 第二阶段迁移进度：Product 模板已复用到其余业务

在第一个 Product 模板验证完成后，本阶段按照同一套 NestJS 组织方式继续迁移现有 Express 中的剩余业务：

- User：认证 / 会话 / 管理员登录 / 注册 / 登出
- Cart：购物车列表 / 添加商品 / 删除商品
- Category：分类列表
- Product：已验证的标准模板

所有模块都保留当前内存数据方案，不额外设计数据库、ORM、Repository/BaseRepository 或微服务抽象。

```text
React + TypeScript + Vite
  │
  ├── Express (原项目保留)
  │     ├── /api/session
  │     ├── /api/auth/login
  │     ├── /api/auth/register
  │     ├── /api/auth/logout
  │     ├── /api/categories
  │     ├── /api/products
  │     ├── /api/cart
  │     ├── /api/cart/items/:productId
  │     └── /api/admin/*
  │
  └── NestJS (学习版第二阶段)
        ├── /api/session
        ├── /api/auth/*
        ├── /api/categories
        ├── /api/products
        ├── /api/cart
        └── /api/admin/*
```

### 9.1 真实业务发现

在原始 Express 中，实际存在的业务接口主要是：

- User / Auth / Session
- Product
- Category
- Cart
- Admin Overview / Admin Product Management

实际没有发现独立的完整 `Order` 模块。也就是说，项目里当前没有可迁移的现成 `Order` 业务表和 `Order` API。后续如果要新增 Order，应该遵循同样 Product 模板的方式，并且必须先明确原 Express 中是否真的存在这部分逻辑。

## 10. Express / NestJS / Spring Boot 对照表

| 概念 | Express | NestJS | Spring Boot |
| --- | --- | --- | --- |
| 路由入口 | app.get()/post() | @Controller + @Get() | @RestController + @GetMapping() |
| 请求处理 | handler function | Controller method | Controller method |
| 业务逻辑 | function / service-like | @Injectable() Service | @Service |
| 依赖注入 | 手工传参/模块化 | constructor 注入 | 构造器注入 |
| 请求体校验 | 手工 if + 校验 | DTO + ValidationPipe | DTO + @Valid |
| 统一异常 | 手工 response.status() | Global Filter | @ControllerAdvice |
| 模块组织 | 单文件 app.js | Module | @Configuration + ComponentScan |

## 11. Express API ↔ NestJS API 对照

本项目中的主要接口保持了尽量一致的 URL 与 JSON 契约：

| 业务 | Express | NestJS | 说明 |
| --- | --- | --- | --- |
| 会话 | `GET /api/session` | `GET /api/session` | 返回 `SessionInfo` |
| 用户登录 | `POST /api/auth/login` | `POST /api/auth/login` | 统一 `ApiResult<SessionInfo>` |
| 用户注册 | `POST /api/auth/register` | `POST /api/auth/register` | 统一 `201` / `409` |
| 用户登出 | `POST /api/auth/logout` | `POST /api/auth/logout` | 清除 cookie |
| 分类 | `GET /api/categories` | `GET /api/categories` | 统一返回分类数组 |
| 商品列表 | `GET /api/products` | `GET /api/products` | 统一返回商品数组 |
| 购物车 | `GET /api/cart` | `GET /api/cart` | 需要登录 cookie |
| 加入购物车 | `POST /api/cart/items/:productId` | `POST /api/cart/items/:productId` | 统一返回购物车列表 |
| 删除购物车 | `DELETE /api/cart/items/:productId` | `DELETE /api/cart/items/:productId` | 统一返回购物车列表 |
| 管理员登录 | `POST /api/admin/login` | `POST /api/admin/login` | 统一 cookie + 权限校验 |
| 管理概览 | `GET /api/admin/overview` | `GET /api/admin/overview` | 显示 product/category/customer 统计 |
| 后台商品列表 | `GET /api/admin/products` | `GET /api/admin/products` | 管理员权限保护 |
| 创建商品 | `POST /api/admin/products` | `POST /api/admin/products` | DTO 校验 |
| 更新商品 | `PUT /api/admin/products/:id` | `PUT /api/admin/products/:id` | DTO 校验 |
| 删除商品 | `DELETE /api/admin/products/:id` | `DELETE /api/admin/products/:id` | 统一删除返回 |

所有后端返回统一遵守：

```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```

## 12. 运行说明

建议的学习顺序：

1. 启动 Express：体验 Node.js / Express / Middleware / Router
2. 启动 NestJS：观察 Controller / Module / Service / DTO / DI
3. 切换前端 API Base：对比同一 Product 数据在两个后端上的行为
4. 在 Product 完成后，再按同样套路扩展 User、Cart、Order

## 13. 默认账号

- 普通用户：lisa / 765
- 管理员：admin / 123

## 14. 目录结构

```text
JtProject-TypeScript/
├── apps/
│   ├── api/                 # 现有 Express 入口
│   ├── api-nestjs/          # 新增 NestJS 学习应用
│   └── web/                 # React + Vite 前端
├── packages/
│   └── shared/              # 共享类型
├── package.json
├── tsconfig.base.json
├── README.md
└── docs/
```
