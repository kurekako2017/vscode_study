# Vue Composables 学习文档

## 这份文档学什么

结合当前 Vue 项目，重点学习：

- `ref`
- `reactive`
- composable

推荐对照文件：

- [App.vue](../frontend/src/App.vue)
- [useAppStore.ts](../frontend/src/composables/useAppStore.ts)
- [appService.ts](../frontend/src/services/appService.ts)

## 1. `ref`

`ref` 适合保存单个值或者整体替换的数据。

如果你后面继续拆 composable，经常会看到：

```ts
const message = ref('Loading...')
```

在脚本里访问时一般要用 `.value`。

## 2. `reactive`

`reactive` 适合对象状态。

当前项目为了更像一个页面级 store，把多个状态统一组织到了：

- [useAppStore.ts](../frontend/src/composables/useAppStore.ts)

这里的 `store` 就是一个响应式对象。

## 3. 什么是 composable

composable 本质上就是：

- 把一组 Vue 组合式逻辑抽成函数
- 供页面和组件复用

当前项目里我们做的是：

- `useAppStore()`

它集中管理：

- 登录状态
- 商品状态
- 管理页状态
- 表单状态
- 后端请求后的结果更新

## 4. 当前项目里的分层关系

- `services/appService.ts`
  负责请求后端
- `composables/useAppStore.ts`
  负责响应式业务逻辑
- `views/*.vue`
  负责页面
- `components/*.vue`
  负责可复用块

## 5. 当前项目里最该观察的点

### 请求层

看：
[appService.ts](../frontend/src/services/appService.ts)

这里负责：

- 登录请求
- 商品请求
- 分类请求
- 购物车请求

### 组合逻辑层

看：
[useAppStore.ts](../frontend/src/composables/useAppStore.ts)

这里负责：

- `bootstrap`
- `refreshCart`
- `refreshAdmin`
- `loginUser`
- `saveProduct`

### 页面层

看：

- [ProductsView.vue](../frontend/src/views/ProductsView.vue)
- [CartView.vue](../frontend/src/views/CartView.vue)

页面会更干净，因为逻辑已经抽到 composable。

## 6. 这次“拆页面再拆组件”的实战练习

这次我额外做了一次组件拆分：

- 新增了 [PageHeader.vue](../frontend/src/components/PageHeader.vue)

它被这些页面复用：

- [ProductsView.vue](../frontend/src/views/ProductsView.vue)
- [CartView.vue](../frontend/src/views/CartView.vue)
- [AdminDashboardView.vue](../frontend/src/views/AdminDashboardView.vue)

这就是 Vue 学习里非常重要的一步：

1. 页面先能跑
2. 模板里发现重复
3. 抽成组件
4. 逻辑再抽成 composable

## 7. 你现在最适合做的练习

1. 从 `useAppStore` 中再抽 `useUserApp`
2. 再抽 `useAdminApp`
3. 给商品页单独做一个 `useProductsPage`
