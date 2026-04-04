# React 学习路线

## 1. 你在这个项目里要学什么

这个项目适合学习这几件事：

- React 组件是什么
- `useState` 怎么管理页面状态
- `useEffect` 怎么在页面加载时请求后端
- 事件处理怎么写
- 表单输入怎么双向绑定到状态
- 列表渲染怎么写
- 如何通过 `fetch` 调后端 API

## 2. 建议顺序

### 第一步：先看入口

看这个文件：
[main.tsx](../frontend/src/main.tsx)

你要理解的是：

- `ReactDOM.createRoot(...)` 是 React 应用挂载入口
- `<App />` 是整个页面的根组件

### 第二步：看主组件

看这个文件：
[App.tsx](../frontend/src/App.tsx)

重点按顺序看：

1. 类型定义 `type Session / Product / Category`
2. `useState(...)`
3. `useEffect(...)`
4. `api(...)` 这个通用请求函数
5. `handleUserLogin / submitProduct / submitProfile` 这些事件函数
6. 最后再看 `return (...)` 里的 JSX

### 第三步：理解 React 的核心思想

React 的思路可以记成一句话：

`状态变化 -> 组件重新渲染 -> 页面自动更新`

比如：

- 登录成功后，`setSession(...)`
- 购物车更新后，`setCart(...)`
- 商品列表更新后，`setProducts(...)`

你不需要自己去手动操作 DOM，React 会根据状态自动刷新页面。

## 3. 这个项目里的 React 语法对应关系

### 组件

在 React 里，页面本质上是函数组件。

例如：

- [App.tsx](../frontend/src/App.tsx)

它本质是：

```tsx
export default function App() {
  return (...)
}
```

### 状态

React 用 `useState` 管数据。

项目里的例子：

- `const [products, setProducts] = useState<Product[]>([])`
- `const [session, setSession] = useState<Session>(...)`

含义：

- `products` 是当前数据
- `setProducts` 是更新它的方法

### 副作用

React 用 `useEffect` 处理“页面加载后做点事”。

项目里的例子是启动时加载：

- session
- 商品列表
- 分类列表

### 事件

React 里按钮点击、表单提交，本质上就是传函数。

例如：

- `onClick={handleUserLogout}`
- `onSubmit={handleUserLogin}`

### 列表渲染

React 用 `array.map(...)` 渲染列表。

项目里商品区和购物车区都是这样做的。

## 4. 你可以自己做的练习

### 初级练习

1. 把商品卡片单独拆成 `ProductCard.tsx`
2. 把购物车列表拆成 `CartPanel.tsx`
3. 把管理员分类表单拆成 `CategoryEditor.tsx`

### 中级练习

1. 给 React 项目加一个简单路由
2. 把用户页和管理页分开
3. 提取公共 API 文件，比如 `src/api.ts`

### 进阶练习

1. 引入 `react-router-dom`
2. 引入状态管理方案，比如 Context
3. 增加加载中、错误提示、空数据状态

## 5. 学 React 时最容易卡住的点

### JSX 不是字符串模板

React 的 JSX 本质是 JavaScript 里的 UI 描述，不是 JSP。

JSP 是服务端拼 HTML。
React 是浏览器里根据状态渲染组件。

### 不要直接改状态对象

应该用：

```tsx
setUserLogin({ ...userLogin, username: e.target.value })
```

不要直接：

```tsx
userLogin.username = 'xxx'
```

### `useEffect` 不是“任何逻辑都往里塞”

它主要放：

- 初始化请求
- 依赖变化后的副作用

普通点击逻辑仍然应该放在事件函数里。
