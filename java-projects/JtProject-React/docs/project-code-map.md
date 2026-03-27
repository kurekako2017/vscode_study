# React 项目源码导读

## 整体结构

### 后端

- [ApiController.java](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
- [application.properties](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/src/main/resources/application.properties)
- [WebMvcConfig.java](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/src/main/java/com/jtspringproject/JtSpringProject/WebMvcConfig.java)

### 前端

- [main.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/main.tsx)
- [App.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/App.tsx)
- [styles.css](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/styles.css)

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
