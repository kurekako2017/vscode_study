# Vue 页面结构说明

## 当前目录分层

Vue 前端现在已经拆成这几层：

- `src/layouts/`
- `src/views/`
- `src/components/`
- `src/composables/`
- `src/services/`

## 每一层是干什么的

### `layouts`

放页面骨架和全局导航。

当前文件：

- [AppLayout.vue](../frontend/src/layouts/AppLayout.vue)

### `views`

放路由级页面。

当前文件：

- [UserLoginView.vue](../frontend/src/views/UserLoginView.vue)
- [ProductsView.vue](../frontend/src/views/ProductsView.vue)
- [CartView.vue](../frontend/src/views/CartView.vue)
- [AdminLoginView.vue](../frontend/src/views/AdminLoginView.vue)
- [AdminDashboardView.vue](../frontend/src/views/AdminDashboardView.vue)

这一层负责：

- 页面级结构
- 页面标题
- 将组件组合成完整页面

### `components`

放可复用功能块。

例如：

- 登录表单
- 商品网格
- 购物车列表
- 分类管理块
- 商品管理块
- 用户列表
- 资料编辑块

### `composables`

放 Vue 的组合式逻辑。

当前文件：

- [useAppStore.ts](../frontend/src/composables/useAppStore.ts)

它负责：

- 页面共享状态
- 初始化加载
- 登录、购物车、后台管理等操作逻辑

### `services`

放请求和业务服务函数。

当前文件：

- [appService.ts](../frontend/src/services/appService.ts)

它负责：

- 调用后端 API
- 封装请求函数
- 返回给 composable 使用

## 你应该怎么理解这套结构

一句话：

- `services` 管“怎么请求”
- `composables` 管“怎么组织响应式逻辑”
- `components` 管“局部块”
- `views` 管“页面”
- `layouts` 管“全局壳”

## 对应原 JSP 的关系

- `userLogin.jsp` -> `UserLoginView`
- `index.jsp` / `uproduct.jsp` -> `ProductsView`
- `cart.jsp` -> `CartView`
- `adminlogin.jsp` -> `AdminLoginView`
- `adminHome.jsp` / `categories.jsp` / `products.jsp` / `displayCustomers.jsp` / `updateProfile.jsp` -> `AdminDashboardView`

## 推荐你接下来练习的重构

1. 把 `useAppStore` 继续拆成 `useUserApp` 和 `useAdminApp`。
2. 给每个 view 再补一个专属 composable。
3. 把商品页和购物车页加上独立的搜索、筛选、分页练习。
