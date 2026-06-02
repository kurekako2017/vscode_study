# Spring Boot + 纯 TypeScript 数据流

这个版本的重点是把框架拿掉，只看前后端分离最基础的数据链路。

## 总体链路

```text
浏览器事件
  -> frontend/src/main.ts
  -> frontend/src/services/appService.ts
  -> frontend/src/api.ts
  -> Spring Boot /api/*
  -> ApiController.java
  -> Service
  -> DAO
  -> H2 数据库
```

## 商品列表

```text
frontend/src/main.ts
  -> loadBootstrapData()
  -> frontend/src/services/appService.ts
  -> api<Product[]>('/products')
  -> ApiController.products()
  -> ProductServiceImpl.java
  -> ProductDaoImpl.java
  -> renderProducts()
```

学习重点：

- `Product` 类型在 `frontend/src/types.ts`
- API 通用错误处理在 `frontend/src/api.ts`
- DOM 拼装和事件绑定在 `frontend/src/main.ts`

## 普通用户登录

```text
登录表单 submit
  -> loginUserRequest()
  -> api<Session>('/auth/login')
  -> ApiController.userLogin()
  -> UserServiceImpl.java
  -> UserDaoImpl.java
  -> Session 写入
  -> 前端更新 state.session
```

学习重点：

- 前端表单数据来自 `FormData`
- 后端登录状态通过 session / cookie 保持
- 前端请求使用 `credentials: 'include'`

## 购物车

```text
加入购物车按钮
  -> addToCartRequest(productId)
  -> api<Product[]>('/cart/items/{productId}')
  -> ApiController.addCartItem()
  -> CartServiceImpl.java
  -> CartProductDaoImpl.java
  -> 前端更新 state.cart
```

学习重点：

- 按钮事件通过 `data-action` 做事件委托
- 后端返回新的购物车商品列表
- 前端不直接修改 DOM 单点，而是更新状态后重新 `render()`

## 和 React / Vue 版的区别

- React / Vue 版：状态变化交给框架驱动组件更新
- 纯 TypeScript 版：自己维护 `state`，自己调用 `render()`
- React / Vue 版：组件拆分更适合大型应用
- 纯 TypeScript 版：更适合学习 API、状态、DOM 的底层关系
