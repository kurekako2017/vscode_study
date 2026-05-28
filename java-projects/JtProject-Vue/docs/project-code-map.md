# Vue 项目源码导读

## 这套分层该怎么读

这个项目的 Vue 前端已经按“路由页面 -> 组件 -> composable -> service”拆开，阅读顺序建议是：

1. 先看 [main.ts](../frontend/src/main.ts) 和 [App.vue](../frontend/src/App.vue) 理解入口。
2. 再看 [router.ts](../frontend/src/router.ts) 理解页面如何切换。
3. 然后看 [useAppStore.ts](../frontend/src/composables/useAppStore.ts) 理解页面状态与业务操作如何组织。
4. 最后看 [appService.ts](../frontend/src/services/appService.ts) 和各个 view/component。

## 整体结构

### 后端

- [ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
- [application.properties](../src/main/resources/application.properties)
- [WebMvcConfig.java](../src/main/java/com/jtspringproject/JtSpringProject/WebMvcConfig.java)

### 前端

- [main.ts](../frontend/src/main.ts)
- [App.vue](../frontend/src/App.vue)
- [router.ts](../frontend/src/router.ts)
- [layouts/AppLayout.vue](../frontend/src/layouts/AppLayout.vue)
- [style.css](../frontend/src/style.css)
- [composables/useAppStore.ts](../frontend/src/composables/useAppStore.ts)
- [services/appService.ts](../frontend/src/services/appService.ts)

### 页面和组件

#### views

- [UserLoginView.vue](../frontend/src/views/UserLoginView.vue)
- [ProductsView.vue](../frontend/src/views/ProductsView.vue)
- [CartView.vue](../frontend/src/views/CartView.vue)
- [AdminLoginView.vue](../frontend/src/views/AdminLoginView.vue)
- [AdminDashboardView.vue](../frontend/src/views/AdminDashboardView.vue)

#### components

- [PageHeader.vue](../frontend/src/components/PageHeader.vue)
- [UserAuthForms.vue](../frontend/src/components/UserAuthForms.vue)
- [AdminAuthForm.vue](../frontend/src/components/AdminAuthForm.vue)
- [ProductGrid.vue](../frontend/src/components/ProductGrid.vue)
- [CartList.vue](../frontend/src/components/CartList.vue)
- [CategoryManager.vue](../frontend/src/components/CategoryManager.vue)
- [ProductManager.vue](../frontend/src/components/ProductManager.vue)
- [CustomerList.vue](../frontend/src/components/CustomerList.vue)
- [ProfileEditor.vue](../frontend/src/components/ProfileEditor.vue)

### 你可以怎么理解它们

- `views` 管页面拼装。
- `components` 管局部复用。
- `composables` 管响应式业务逻辑。
- `services` 管请求封装。
- `layouts` 管全局壳和导航。

## 你可以怎么对照学习

### 登录

Vue 前端：

- `submitUserLogin`
- `submitAdminLogin`

后端接口：

- `/api/auth/login`
- `/api/admin/login`

### 商品列表

Vue 前端：

- `v-for="product in products"`

后端接口：

- `/api/products`
- `/api/admin/products`

### 购物车

Vue 前端：

- `addToCart`
- `removeFromCart`

后端接口：

- `POST /api/cart/items/{productId}`
- `DELETE /api/cart/items/{productId}`

### 分类与商品管理

Vue 前端：

- `submitCategory`
- `submitProduct`

后端接口：

- `/api/admin/categories`
- `/api/admin/products`

## 建议补充的学习图

如果你想继续往深里理解，推荐把这几个图和代码一起看：

- 路由图：`router.ts` 如何把 view 串起来。
- 状态图：`useAppStore.ts` 如何集中管理 session、商品、购物车、后台数据。
- 请求图：`appService.ts` 如何把 `api()` 包装成具体业务函数。
- 页面图：`AdminDashboardView.vue` 如何把多个组件组合成一个页面。

## 建议你边看边改的地方

1. 先把 `App.vue` 中一块区域抽成子组件。
2. 再把请求逻辑抽到独立文件。
3. 再引入路由拆页面。
