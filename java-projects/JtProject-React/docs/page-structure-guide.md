# React 页面结构说明

## 当前目录分层

React 前端现在已经拆成这几层：

- `src/layouts/`
- `src/views/`
- `src/components/`
- `src/hooks/`
- `src/services/`

## 每一层是干什么的

### `layouts`

放页面骨架和通用导航。

当前文件：

- [AppLayout.tsx](../frontend/src/layouts/AppLayout.tsx)

你可以理解成：

- 页面外壳
- 顶部导航
- 跨页面共享的壳子

### `views`

放“路由级页面”。

当前文件：

- [UserLoginView.tsx](../frontend/src/views/UserLoginView.tsx)
- [ProductsView.tsx](../frontend/src/views/ProductsView.tsx)
- [CartView.tsx](../frontend/src/views/CartView.tsx)
- [AdminLoginView.tsx](../frontend/src/views/AdminLoginView.tsx)
- [AdminDashboardView.tsx](../frontend/src/views/AdminDashboardView.tsx)

这一层负责：

- 当前页面标题
- 页面级布局组合
- 把组件拼起来

### `components`

放可复用 UI 块。

例如：

- 表单
- 商品卡片区
- 购物车列表
- 分类管理块
- 商品管理块
- 用户列表
- 资料编辑块

这一层是“局部功能模块”。

### `hooks`

放 React 状态逻辑。

当前文件：

- [useAppState.ts](../frontend/src/hooks/useAppState.ts)

它负责：

- 初始化加载
- session 状态
- 商品、分类、购物车、后台数据状态
- 各种表单状态

### `services`

放请求和业务函数。

当前文件：

- [appService.ts](../frontend/src/services/appService.ts)

它负责：

- 请求后端 API
- 组装请求
- 返回业务数据

## 你应该怎么理解这套结构

一句话：

- `services` 管“怎么请求”
- `hooks` 管“怎么存状态”
- `components` 管“局部 UI”
- `views` 管“页面组合”
- `layouts` 管“全局外壳”

## 对应原 JSP 的关系

- `userLogin.jsp` -> `UserLoginView`
- `index.jsp` / `uproduct.jsp` -> `ProductsView`
- `cart.jsp` -> `CartView`
- `adminlogin.jsp` -> `AdminLoginView`
- `adminHome.jsp` / `categories.jsp` / `products.jsp` / `displayCustomers.jsp` / `updateProfile.jsp` -> `AdminDashboardView`

## 推荐你接下来练习的重构

1. 把 `ProductManager` 继续拆成“表单组件”和“列表组件”。
2. 把用户登录和注册拆成两个独立 view。
3. 把 `useAppState` 再拆成 `useUserState` 和 `useAdminState`。
