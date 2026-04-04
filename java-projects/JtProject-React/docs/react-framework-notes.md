# React 框架速查

## React 是什么

React 是一个组件驱动的前端库。

你可以把页面拆成很多小块：

- 页面根组件
- 商品列表组件
- 登录表单组件
- 购物车组件

每个组件负责一小块 UI 和逻辑。

## React 核心概念

### 1. Component

React 的页面由组件组成。

当前项目暂时把逻辑都放在：
[App.tsx](../frontend/src/App.tsx)

后面你可以继续拆分。

### 2. Props

组件之间传值用 `props`。

现在项目还没有大规模拆组件，所以你后面正好可以练这个。

### 3. State

组件内部数据一般用 `useState`。

### 4. Effect

和后端交互、初始化加载，一般用 `useEffect`。

### 5. JSX

JSX 是“在 JavaScript 里写 UI”。

例如：

```tsx
<button onClick={handleUserLogout}>User Logout</button>
```

## React 和 JSP 的差别

### JSP

- 后端渲染页面
- 控制器直接返回视图
- 页面里能写 EL、JSTL

### React

- 前端单独运行
- 后端只提供数据接口
- 前端自己决定怎么显示数据

所以在这个 React 项目里：

- Java 负责 `/api/...`
- React 负责页面显示

## 这个项目里的学习重点文件

- React 入口：[main.tsx](../frontend/src/main.tsx)
- 页面逻辑：[App.tsx](../frontend/src/App.tsx)
- 样式文件：[styles.css](../frontend/src/styles.css)
- API 控制器：[ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)

## 下一步推荐重构

你学习 React 时，可以把当前大组件继续拆成：

- `src/components/UserAuthPanel.tsx`
- `src/components/AdminAuthPanel.tsx`
- `src/components/ProductGrid.tsx`
- `src/components/CartPanel.tsx`
- `src/components/CategoryPanel.tsx`
- `src/components/ProfilePanel.tsx`

这样最能练到 React 的组件化思维。
