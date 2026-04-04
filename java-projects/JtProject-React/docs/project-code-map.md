# React 项目源码导读

## 整体结构

### 后端

- [ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
- [application.properties](../src/main/resources/application.properties)
- [WebMvcConfig.java](../src/main/java/com/jtspringproject/JtSpringProject/WebMvcConfig.java)

### 前端

- [main.tsx](../frontend/src/main.tsx)
- [App.tsx](../frontend/src/App.tsx)
- [styles.css](../frontend/src/styles.css)

## 你可以怎么对照学习

### 登录

React 前端：

- `handleUserLogin`
- `handleAdminLogin`

后端接口：

- `/api/auth/login`
- `/api/admin/login`

### 商品列表

React 前端：

- `products.map(...)`

后端接口：

- `/api/products`
- `/api/admin/products`

### 购物车

React 前端：

- `addToCart`
- `removeFromCart`

后端接口：

- `POST /api/cart/items/{productId}`
- `DELETE /api/cart/items/{productId}`

### 分类与商品管理

React 前端：

- `submitCategory`
- `submitProduct`

后端接口：

- `/api/admin/categories`
- `/api/admin/products`

## 建议你边看边改的地方

1. 先把 `App.tsx` 中某一块单独抽成组件。
2. 再把 `api(...)` 抽到独立文件。
3. 再加上路由，把页面拆分。
