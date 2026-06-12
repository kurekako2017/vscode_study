# React Modern Learning 说明

这份文档专门讲“怎么学这套页面”，重点是按顺序看、按页面练、按组件理解。

## 学习顺序

### 1. 首页 `/`

- 页面：`HomePage.jsx`
- 看点：项目有哪些章节，入口长什么样
- 练习建议：先点击几个章节卡片，理解路由跳转

### 2. Hooks `/hooks`

- 页面：`HooksPage.jsx`
- 示例：`CounterDemo.jsx`、`TimerDemo.jsx`
- 看点：`useState`、`useEffect`、状态更新、事件处理、清理函数
- 练习建议：先改按钮文案，再改状态值，观察页面如何变化

### 3. Router `/router`

- 页面：`RouterPage.jsx`
- 子页：`RouterHome`、`AboutPage`、`UserProfile`
- 看点：`NavLink`、`Outlet`、嵌套路由、动态参数
- 练习建议：切换不同子页面，观察地址栏和内容区的联动

### 4. Context `/context`

- 页面：`ContextPage.jsx`
- 示例：`ThemeContextDemo.jsx`
- 看点：`createContext`、`Provider`、`useContext`
- 练习建议：先看主题状态怎么切换，再看子组件怎么拿到主题值

### 5. API `/api`

- 页面：`ApiPage.jsx`
- 示例：`PostsDemo.jsx`
- 看点：`fetch`、`loading`、`error`、`success`、请求取消
- 练习建议：先看三态分支，再看请求成功后如何渲染列表

### 6. Test `/test`

- 页面：`TestPage.jsx`
- 组件：`Counter.jsx`
- 测试：`Counter.test.jsx`
- 看点：组件如何和测试文件配对，如何从用户行为写断言
- 练习建议：先看组件，再看测试，最后尝试自己改一个断言

## 每页怎么读

1. 先看页面标题和说明文字，知道这一页在讲什么
2. 再看页面里的 demo 组件，找状态、事件和条件渲染
3. 最后看对应测试或子页面，理解它们是怎么配合的

## 你可以怎么改

- 先改文字，再改状态值
- 先改一个按钮，再改一个输入框
- 先看效果，再回到代码对照理解

## 结构提示

- 首页只做导航，不放复杂逻辑
- 每个章节一个目录
- 每个章节尽量有一个主示例
- `Router` 章节最适合用来理解子页面组织方式

如果你想看完整文件树和页面名称，可以打开 [project-structure.md](./project-structure.md)。
