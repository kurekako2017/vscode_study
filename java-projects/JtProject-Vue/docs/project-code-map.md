# Vue 项目源码导读

## 整体结构

### 后端

- [ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
- [application.properties](../src/main/resources/application.properties)
- [WebMvcConfig.java](../src/main/java/com/jtspringproject/JtSpringProject/WebMvcConfig.java)

### 前端

- [main.ts](../frontend/src/main.ts)
- [App.vue](../frontend/src/App.vue)
- [style.css](../frontend/src/style.css)

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

## 建议你边看边改的地方

1. 先把 `App.vue` 中一块区域抽成子组件。
2. 再把请求逻辑抽到独立文件。
3. 再引入路由拆页面。
