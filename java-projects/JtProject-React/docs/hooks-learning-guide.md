# React Hooks 学习文档

## 这份文档学什么

结合当前 React 项目，重点学习：

- `useState`
- `useEffect`
- 自定义 Hook

推荐对照文件：

- [App.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/App.tsx)
- [useAppState.ts](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/hooks/useAppState.ts)
- [appService.ts](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/services/appService.ts)

## 1. `useState`

`useState` 用来保存组件状态。

在这个项目里你会看到：

```ts
const [message, setMessage] = useState('Loading...')
```

含义是：

- `message` 是当前值
- `setMessage` 是更新值的方法

在我们的项目里，`useState` 主要保存：

- 登录状态
- 商品列表
- 分类列表
- 购物车
- 管理页表单

## 2. `useEffect`

`useEffect` 用于处理副作用，例如：

- 页面首次加载时请求数据
- 依赖变化后做额外处理

在当前项目里：
[useAppState.ts](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/hooks/useAppState.ts)

里面最关键的是初始化：

```ts
useEffect(() => {
  void bootstrap()
}, [])
```

这表示：

- 组件首次挂载时执行 `bootstrap`
- 用来加载 session、商品、分类

## 3. 自定义 Hook

### 什么是自定义 Hook

自定义 Hook 本质上就是：

- 把一组 React 状态逻辑抽成函数
- 让多个页面或组件可以复用

当前项目里我们做的就是：

- [useAppState.ts](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/hooks/useAppState.ts)

### 它解决了什么问题

如果不抽 Hook，`App.tsx` 会越来越大。

抽出来后：

- `App.tsx` 更像页面路由总控
- `useAppState.ts` 更像状态中心
- `appService.ts` 更像请求层

这就是更真实的 React 项目结构。

## 4. 当前项目里的分层关系

- `services/appService.ts`
  负责请求后端
- `hooks/useAppState.ts`
  负责状态管理
- `views/*.tsx`
  负责页面
- `components/*.tsx`
  负责可复用 UI

## 5. 你现在最适合做的练习

1. 从 `useAppState` 中再抽一个 `useAdminState`
2. 再抽一个 `useUserState`
3. 给商品页单独做一个 `useProductsPage`

## 6. 这次“拆页面再拆组件”的实战练习

这次我额外做了一次组件拆分：

- 新增了 [PageHeader.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/components/PageHeader.tsx)

它把多个页面里重复的页面头部抽成了公共组件。

你可以看到它已经被这些页面复用：

- [ProductsView.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/views/ProductsView.tsx)
- [CartView.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/views/CartView.tsx)
- [AdminDashboardView.tsx](/d:/dev/source_code/vscode_study/java-projects/JtProject-React/frontend/src/views/AdminDashboardView.tsx)

这就是很典型的 React 学习路径：

1. 先写在页面里
2. 发现重复
3. 抽成组件
4. 如果状态逻辑也重复，再抽 Hook
