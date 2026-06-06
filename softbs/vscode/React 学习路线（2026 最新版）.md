# React 学习路线（2026 最新版）

适合对象：

- React 初学者
- 有 Vue / Java / C# 背景转前端
- 想做全栈
- 想做日本现场 React 项目
- 想进入 AI + Web 开发

---

# 一、2026 React 技术栈现状

现在 React 主流已经变成：

```txt
React + TypeScript + Vite
```

而不是以前：

```txt
React + CRA + class component
```

现在企业主流：

| 技术 | 是否推荐 |
|---|---|
| React Hooks | ✅ 必学 |
| TypeScript | ✅ 必学 |
| Vite | ✅ 主流 |
| Zustand | ✅ 推荐 |
| TanStack Query | ✅ 推荐 |
| Next.js | ✅ 企业级 |
| TailwindCSS | ✅ 主流 |
| Redux 老写法 | ❌ 不推荐优先 |
| class component | ❌ 基本淘汰 |
| CRA(create-react-app) | ❌ 已过时 |

---

# 二、React 学习顺序（非常重要）

不要乱学，推荐按照下面顺序：

```txt
JavaScript
↓
React 基础
↓
Hooks
↓
小项目
↓
TypeScript
↓
状态管理
↓
API 请求
↓
企业级项目
↓
Next.js
↓
全栈
```

---

# 三、第一阶段：JavaScript 基础（必须）

React 学不会，90% 是 JS 不扎实。

## 必学内容

```js
let / const
箭头函数
解构赋值
展开运算符
map/filter/reduce
Promise
async/await
模块化 import/export
```

## 推荐教程

### JavaScript 现代教程（中文）

https://zh.javascript.info/

推荐原因：

- 中文
- 系统
- 现代 JavaScript
- 适合长期查阅

---

# 四、第二阶段：React 基础

## 官方文档（必须）

React 中文：

https://zh-hans.react.dev/

重点学习：

- 组件
- props
- state
- useState
- useEffect
- 条件渲染
- 列表渲染
- 表单

---

## React 必学 Hooks

| Hook | 重要度 |
|---|---|
| useState | ⭐⭐⭐⭐⭐ |
| useEffect | ⭐⭐⭐⭐⭐ |
| useRef | ⭐⭐⭐⭐ |
| useMemo | ⭐⭐⭐ |
| useCallback | ⭐⭐⭐ |
| useContext | ⭐⭐⭐⭐ |

### Hooks 学习顺序

建议先学：

```txt
useState
↓
useEffect
↓
useRef
↓
useContext
↓
useMemo / useCallback
```

不要一开始就纠结性能优化，先把状态、事件、组件通信、数据请求搞清楚。

---

# 五、第三阶段：开始做项目（关键）

不要只看视频。

一定要：

```txt
自己重新敲代码
```

推荐练习：

- TodoList
- 天气 App
- 记账 App
- 简单博客
- 登录注册页面
- 商品列表页面

---

# 六、最推荐 React 初级 GitHub 项目

## 1. TodoList Clone

GitHub：

https://github.com/karlhadwen/todoist-clone

适合：

- React 初学者
- Hooks 入门
- 状态管理入门

学习点：

```txt
useState
组件拆分
列表操作
表单
Context
```

推荐练习改造：

- 添加搜索
- 添加分类
- 添加暗色模式
- 添加本地存储
- 添加拖拽排序

---

## 2. RealWorld（神级项目）

GitHub：

https://github.com/gothinkster/realworld

React 版本：

https://github.com/gothinkster/react-redux-realworld-example-app

这是 React 圈非常经典的实战项目。

你会学到：

- 登录注册
- JWT
- API 请求
- CRUD
- 路由
- 状态管理
- 项目结构

适合：

```txt
真正进入企业开发
```

---

## 3. Jira Clone

GitHub：

https://github.com/oldboyxx/jira_clone

学习点：

```txt
复杂状态
拖拽
项目结构
React Router
组件设计
```

适合：

```txt
中级提升
```

建议学完 Todo 和 RealWorld 之后再看。

---

## 4. React Tetris

GitHub：

https://github.com/chvin/react-tetris

适合：

```txt
理解 React 状态流
```

学习：

```txt
useEffect
键盘事件
动画
状态管理
```

---

# 七、TypeScript（必须学）

现在 React 企业开发：

```txt
几乎默认 TypeScript
```

## TypeScript 必学

```ts
interface
type
泛型
函数类型
联合类型
类型推导
```

学习方式：

```txt
不要单独死磕 TS，边做 React 项目边学 TS。
```

---

# 八、状态管理（现在推荐）

以前很多项目使用：

```txt
Redux
```

现在新项目可以优先学习：

```txt
Zustand
```

GitHub：

https://github.com/pmndrs/zustand

优点：

- 简单
- 学习成本低
- 现代
- 适合个人项目和中小项目

---

# 九、API 请求（企业必须）

现在推荐：

```txt
TanStack Query
```

GitHub：

https://github.com/TanStack/query

学习重点：

```txt
loading
error
缓存
自动刷新
分页
接口状态管理
```

---

# 十、CSS 推荐路线

推荐：

```txt
TailwindCSS
```

GitHub：

https://github.com/tailwindlabs/tailwindcss

原因：

- 企业主流
- 开发快
- AI 生成代码友好
- 适合个人项目快速出效果

---

# 十一、Next.js（后期重点）

React 只是 UI 层，企业项目经常会用：

```txt
Next.js
```

官网：

https://nextjs.org/

## Next.js 学什么

```txt
SSR
App Router
Server Component
SEO
API Route
FullStack
```

---

# 十二、React 项目结构（企业级）

推荐结构：

```txt
src/
 ├── api/
 ├── components/
 ├── hooks/
 ├── pages/
 ├── store/
 ├── types/
 ├── utils/
 └── app/
```

说明：

- api：接口请求
- components：通用组件
- hooks：自定义 Hooks
- pages：页面
- store：状态管理
- types：TypeScript 类型
- utils：工具函数
- app：应用入口或 Next.js App Router

---

# 十三、2026 推荐开发工具

## 编辑器

推荐 VSCode。

插件：

```txt
ESLint
Prettier
Error Lens
Tailwind CSS IntelliSense
GitLens
```

## AI 编程工具

| 工具 | 推荐度 |
|---|---|
| ChatGPT Codex CLI | ⭐⭐⭐⭐⭐ |
| Continue.dev | ⭐⭐⭐⭐ |
| Cursor | ⭐⭐⭐⭐ |
| GitHub Copilot | ⭐⭐⭐ |

---

# 十四、最推荐学习方式

错误方式：

```txt
一直看视频
```

正确方式：

```txt
自己模仿写
自己改功能
自己报错
自己调试
```

真正进步来自：

- 自己搭项目
- 自己看报错
- 自己查文档
- 自己改需求
- 自己重构代码

---

# 十五、React 面试重点

## 初级

```txt
props / state
useEffect
生命周期
组件通信
条件渲染
列表渲染
```

## 中级

```txt
性能优化
React.memo
useMemo
useCallback
状态管理
接口请求
```

## 高级

```txt
React Fiber
Concurrent Rendering
SSR
Hydration
Next.js
```

---

# 十六、日本现场常见 React 技术栈

日本现场常见：

```txt
React + TypeScript
Next.js
Material UI
TailwindCSS
AWS
```

也经常有：

```txt
React + Spring Boot
```

以及：

```txt
React + .NET
```

如果你是做业务系统开发，重点应该放在：

- React
- TypeScript
- API 对接
- 表单
- 表格
- 权限
- 登录认证
- 画面设计书理解
- Git 协作

---

# 十七、React 学习误区

## 1. 一直看视频

不推荐。必须自己写。

## 2. 一开始学 Redux

不推荐。先掌握：

```txt
useState + useContext + Zustand
```

## 3. 一开始看源码

容易放弃。先做项目。

## 4. 项目太大

不要一开始做：

```txt
电商后台
ERP
复杂管理系统
```

先从 Todo、博客、RealWorld 开始。

---

# 十八、最佳学习路线

## 第 1 个月

学习：

```txt
JavaScript
React 基础
Hooks 基础
```

项目：

```txt
Todo
天气 App
记账 App
```

## 第 2 个月

学习：

```txt
TypeScript
API 请求
Zustand
React Router
```

项目：

```txt
博客系统
登录注册系统
商品列表系统
```

## 第 3 个月

学习：

```txt
RealWorld
企业级项目结构
权限
CRUD
```

目标：

```txt
真正接近公司开发
```

## 第 4 个月

学习：

```txt
Next.js
全栈开发
部署
```

目标：

```txt
能做一个完整可上线项目
```

---

# 十九、推荐中文视频资源

## 技术胖

适合：

```txt
入门
```

## CodeWhy

适合：

```txt
系统学习
```

## 尚硅谷 React

适合：

```txt
基础扎实
```

---

# 二十、最终建议

真正能学会 React 的人，不是看得最多的人，而是自己做得最多的人。

建议：

```txt
每天至少写代码 2 小时
```

比看 10 个小时视频更有效。

---

# 二十一、推荐最终技术路线（2026）

最推荐：

```txt
React
+ TypeScript
+ Vite
+ TailwindCSS
+ Zustand
+ TanStack Query
+ Next.js
```

这是目前：

```txt
个人开发 + 企业开发 + AI 开发
综合最强路线
```
