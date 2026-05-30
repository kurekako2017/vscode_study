# 纯 TypeScript 全栈处理流程图

`JtProject-TypeScript` 的学习重点是：前端、后端、共享类型全部使用 TypeScript。和 Spring Boot 版本相比，这里没有 Java Controller / Service / DAO，而是用 Express 路由和 TypeScript Store 表达同一套业务。

如果你想先系统理解框架分层，先看：

- [TypeScript 全栈框架系统学习指南](./typescript-framework-guide.md)

## 关键文件

| 文件 | 作用 | 对应原始项目概念 |
| --- | --- | --- |
| `packages/shared/src/index.ts` | 前后端共享类型 | Java model / DTO |
| `apps/api/src/data/seed.ts` | 初始数据 | `data.sql` |
| `apps/api/src/data/store.ts` | 内存数据仓库 | DAO / Service 的一部分 |
| `apps/api/src/server.ts` | Express API | Controller |
| `apps/web/src/api.ts` | 前端请求封装 | API Service |
| `apps/web/src/App.tsx` | React 页面 | JSP / 前端页面 |

原始 SQL 已复制到：

- `docs/original-jtproject-data.sql`
- `docs/original-jtproject-basedata.sql`

## 整体流程

```mermaid
flowchart TD
    A[浏览器访问 http://localhost:5175] --> B[Vite 返回 React 应用]
    B --> C[apps/web/src/main.tsx 挂载 App]
    C --> D[App.tsx useEffect 加载初始数据]
    D --> E[api<T>() 调用 fetch]
    E --> F[Express: http://localhost:8090/api]
    F --> G[server.ts 路由函数]
    G --> H[Store 内存数据层]
    H --> I[(seed 数据 + carts Map)]
    I --> H --> G
    G --> J[ApiResult<T> JSON]
    J --> E
    E --> K[TypeScript 根据 T 推断 data 类型]
    K --> L[setProducts / setSession / setCart]
    L --> M[React 重新渲染 UI]
```

## 商品列表加载流程

```mermaid
sequenceDiagram
    participant Browser as Browser
    participant App as App.tsx
    participant Api as api<T>()
    participant Server as Express server.ts
    participant Store as Store

    Browser->>App: 打开页面
    App->>App: useEffect() 调用 loadInitialData()
    App->>Api: api<Product[]>('/products')
    Api->>Server: GET /api/products
    Server->>Store: store.getProducts()
    Store-->>Server: Product[]
    Server-->>Api: ApiResult<Product[]>
    Api-->>App: result.data 类型为 Product[]
    App->>App: setProducts(result.data)
    App-->>Browser: 渲染商品卡片
```

## 登录和购物车流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant App as App.tsx
    participant Api as api<T>()
    participant Server as Express API
    participant Cookie as Cookie
    participant Store as Store

    User->>App: 提交 lisa / 765
    App->>Api: api<SessionInfo>('/auth/login', POST)
    Api->>Server: JSON username/password
    Server->>Store: store.checkLogin()
    Store-->>Server: User
    Server->>Cookie: 写入 jt_ts_session
    Server-->>Api: ApiResult<SessionInfo>
    Api-->>App: session data
    App->>Api: api<Product[]>('/cart')
    Api->>Server: credentials include 携带 cookie
    Server->>Store: store.getCartProducts(user.id)
    Store-->>Server: Product[]
    Server-->>Api: ApiResult<Product[]>
    Api-->>App: 购物车商品
```

## 共享类型如何工作

前后端都从 `packages/shared/src/index.ts` 引入类型：

```ts
import type { Product, SessionInfo, ApiResult } from '../../../packages/shared/src/index'
```

这样带来三个好处：

- 后端返回 `Product[]` 时，前端 `setProducts` 能获得准确类型。
- `api<T>()` 可以复用同一个请求函数，同时保留不同接口的返回类型。
- 修改字段时，前后端会一起被 TypeScript 检查到。

## 接口速查

| 页面动作 | 前端函数 | 后端接口 | 返回类型 |
| --- | --- | --- | --- |
| 首页加载 | `loadInitialData()` | `GET /api/session` | `SessionInfo` |
| 首页加载 | `loadInitialData()` | `GET /api/products` | `Product[]` |
| 普通用户登录 | `submitUserLogin()` | `POST /api/auth/login` | `SessionInfo` |
| 管理员登录 | `submitAdminLogin()` | `POST /api/admin/login` | `SessionInfo` |
| 加入购物车 | `addToCart(productId)` | `POST /api/cart/items/{productId}` | `Product[]` |
| 删除购物车 | `removeFromCart(productId)` | `DELETE /api/cart/items/{productId}` | `Product[]` |
| 后台概览 | `loadOverview()` | `GET /api/admin/overview` | `AdminOverview` |
