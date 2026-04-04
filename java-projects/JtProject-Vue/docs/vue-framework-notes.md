# Vue 框架速查

## Vue 是什么

Vue 是一个渐进式前端框架。

它的特点是：

- 模板语法直观
- 响应式机制清晰
- 组件拆分自然

对初学者来说，Vue 往往比 React 更容易先上手模板部分。

## Vue 核心概念

### 1. Component

Vue 页面也是由组件组成的。

当前项目暂时把主要逻辑集中在：
[App.vue](../frontend/src/App.vue)

### 2. Reactive Data

Vue 的核心是响应式数据。

常用的是：

- `ref`
- `reactive`

### 3. Template

Vue 使用模板描述页面：

- `v-if`
- `v-for`
- `v-model`
- `@click`

### 4. Lifecycle

在 Vue 3 Composition API 中，常用：

- `onMounted`

## Vue 和 JSP 的差别

### JSP

- 后端直接渲染页面
- 服务器返回 HTML

### Vue

- 前端独立运行
- 页面在浏览器端渲染
- 后端只返回 JSON 数据

所以这个 Vue 项目里：

- Java 负责 `/api/...`
- Vue 负责模板和交互

## 这个项目里的学习重点文件

- Vue 入口：[main.ts](../frontend/src/main.ts)
- 主组件：[App.vue](../frontend/src/App.vue)
- 样式文件：[style.css](../frontend/src/style.css)
- API 控制器：[ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)

## 下一步推荐重构

你学习 Vue 时，可以把当前页面继续拆成：

- `src/components/UserAuthPanel.vue`
- `src/components/AdminAuthPanel.vue`
- `src/components/ProductGrid.vue`
- `src/components/CartPanel.vue`
- `src/components/CategoryPanel.vue`
- `src/components/ProfilePanel.vue`

这样最能练到 Vue 的组件化和模板拆分能力。
