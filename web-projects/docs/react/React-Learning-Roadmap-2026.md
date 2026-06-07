# React 学习路线与 GitHub 项目推荐（2026）

> 面向：
>
> - React 初学者
> - 想学习前端开发
> - 想进入 React + TypeScript 全栈路线
> - 使用 VSCode / Cursor / Codex 开发的人

---

# 一、React 到底是什么？

React 是：

```text
用于构建 Web UI 的 JavaScript 库
```

核心：

- 组件化
- 状态管理
- 响应式 UI
- 前后端分离

现在绝大多数：

- AI Web
- SaaS
- 后台系统
- 管理系统
- AI Agent UI

都大量使用 React。

---

# 二、React 正确学习路线（非常重要）

很多人：

- 一上来学 Redux
- 一上来学 Next.js
- 一上来学全家桶

结果：

> 连组件和状态都没真正理解。

正确路线：

```text
HTML/CSS/JS
↓
React 基础
↓
Hooks
↓
组件设计
↓
React Router
↓
API 调用
↓
TypeScript
↓
状态管理
↓
Next.js
↓
全栈开发
```

---

# 三、最推荐的 GitHub React 学习项目

---

## 1. react-beginner（中文 React 入门）

GitHub：

https://github.com/ruanyf/react-demos

特点：

- 阮一峰 React Demo
- 中文
- 简单直接
- 非常适合第一次学习 React

推荐指数：

⭐⭐⭐⭐⭐

适合：

- 完全初学者
- 想快速理解 React

---

## 2. react-docs（React 官方文档）

官网：

https://react.dev/

中文：

https://zh-hans.react.dev/

特点：

- 官方最新文档
- Hooks 讲得非常好
- 示例丰富
- React 18+

推荐指数：

⭐⭐⭐⭐⭐

非常重要。

很多老教程已经过时。

---

## 3. react-typescript-cheatsheet（TS 最佳教程）

GitHub：

https://github.com/typescript-cheatsheets/react

特点：

- React + TypeScript 最经典资料
- 企业开发必备
- Hooks + TS

推荐指数：

⭐⭐⭐⭐⭐

---

## 4. bulletproof-react（企业级 React）

GitHub：

https://github.com/alan2207/bulletproof-react

特点：

- 企业级项目结构
- 最佳实践
- TypeScript
- Zustand
- React Query
- Feature 架构

推荐指数：

⭐⭐⭐⭐⭐

适合：

- 进阶学习
- 真正项目开发

---

## 5. react-admin（后台管理系统）

GitHub：

https://github.com/marmelab/react-admin

特点：

- 后台系统学习
- CRUD
- 数据管理

推荐指数：

⭐⭐⭐⭐

---

## 6. awesome-react（React 资源大全）

GitHub：

https://github.com/enaqx/awesome-react

特点：

- React 全资源导航
- 长期更新

推荐指数：

⭐⭐⭐⭐

---

# 四、最推荐学习的视频教程（中文）

---

## 1. 尚硅谷 React

B站搜索：

```text
尚硅谷 React
```

特点：

- 中文
- 最适合零基础
- 非常详细

---

## 2. 黑马 React

特点：

- 简洁
- 项目化
- 适合快速入门

---

## 3. React 官方 Tutorial

推荐：

官方 Tutorial 必做。

---

# 五、现在真正主流 React 技术栈

现在企业基本：

```text
React
+
TypeScript
+
Vite
+
TailwindCSS
+
React Query
+
Zustand
+
Next.js
```

---

# 六、React 最重要的核心概念

---

## 1. Component（组件）

React 一切都是组件。

例如：

```jsx
function Button() {
  return <button>Click</button>
}
```

---

## 2. Props（参数）

组件之间传值。

---

## 3. State（状态）

动态数据。

例如：

```jsx
const [count, setCount] = useState(0)
```

---

## 4. Hooks（最重要）

包括：

| Hook | 用途 |
|---|---|
| useState | 状态 |
| useEffect | 生命周期 |
| useRef | DOM |
| useMemo | 性能优化 |
| useCallback | 函数缓存 |

---

## 5. Router（路由）

页面切换。

推荐：

```text
React Router
```

---

# 七、推荐学习顺序（非常重要）

---

## 第一阶段

学习：

- JSX
- Component
- Props
- State

项目：

- TodoList
- 计数器

---

## 第二阶段

学习：

- Hooks
- useEffect
- API 调用

项目：

- 天气 App
- GitHub 用户搜索

---

## 第三阶段

学习：

- React Router
- 状态管理

项目：

- 后台系统

---

## 第四阶段

学习：

- TypeScript
- React Query
- Zustand

项目：

- 企业项目结构

---

## 第五阶段

学习：

- Next.js
- SSR
- 全栈

项目：

- AI Web
- SaaS

---

# 八、最适合练习的 React 项目

---

## 1. Todo App

学习：

- State
- Component

---

## 2. 天气 App

学习：

- API
- useEffect

---

## 3. GitHub Search

学习：

- 搜索
- Loading
- Error Handling

---

## 4. AI Chat UI

学习：

- Chat UI
- Streaming

非常推荐。

---

## 5. 后台管理系统

学习：

- Router
- 状态管理
- CRUD

---

# 九、现在最推荐的 React 开发环境

推荐：

```text
VSCode
+
Vite
+
TypeScript
+
ESLint
+
Prettier
```

---

# 十、推荐 VSCode 插件

| 插件 | 用途 |
|---|---|
| ES7 React Snippets | React 快捷代码 |
| Tailwind CSS IntelliSense | Tailwind |
| Error Lens | 错误高亮 |
| Prettier | 格式化 |
| ESLint | 代码规范 |
| GitLens | Git |

---

# 十一、React 项目创建方式（最新）

推荐：

```bash
npm create vite@latest
```

选择：

```text
React
TypeScript
```

然后：

```bash
npm install
npm run dev
```

---

# 十二、现在不推荐的东西

不要：

- CRA（Create React App）
- class component
- Redux 老写法

现在主流：

```text
Function Component
+
Hooks
+
TypeScript
```

---

# 十三、推荐技术路线（最适合现在）

推荐：

```text
React
↓
TypeScript
↓
Vite
↓
TailwindCSS
↓
React Query
↓
Zustand
↓
Next.js
```

---

# 十四、如果以后想做 AI Web

React 非常重要。

因为：

- ChatGPT UI
- Cursor
- Codex Web
- AI SaaS
- Agent Dashboard

基本都：

```text
React + TypeScript
```

---

# 十五、最终推荐路线（非常重要）

如果你现在开始：

推荐：

```text
React 基础
↓
Hooks
↓
TypeScript
↓
Vite
↓
组件设计
↓
API 调用
↓
React Query
↓
Next.js
↓
AI Web
```

这是目前最主流、最适合就业与 AI 开发的路线。

