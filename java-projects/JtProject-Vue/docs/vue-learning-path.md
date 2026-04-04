# Vue 学习路线

## 1. 你在这个项目里要学什么

这个项目适合学习这几件事：

- Vue 组件是什么
- `ref` 和 `reactive` 有什么区别
- `onMounted` 怎么在页面加载后请求数据
- `v-model` 怎么做表单绑定
- `v-for` 怎么渲染列表
- `@click` 怎么处理事件
- 如何通过 `fetch` 调用后端 API

## 2. 建议顺序

### 第一步：看入口

先看：
[main.ts](../frontend/src/main.ts)

你要理解：

- `createApp(App).mount('#app')` 是 Vue 应用入口

### 第二步：看主组件

再看：
[App.vue](../frontend/src/App.vue)

重点按顺序看：

1. 类型定义
2. `ref(...)`
3. `reactive(...)`
4. `api(...)`
5. `submitUserLogin / submitCategory / submitProduct`
6. `<template>` 模板部分

### 第三步：理解 Vue 的核心思想

Vue 的思路也可以记成一句话：

`响应式数据变化 -> 模板自动更新`

比如：

- `session.value = ...`
- `products.value = ...`
- `Object.assign(productForm, product)`

这些数据一变，模板会自动刷新。

## 3. 这个项目里的 Vue 语法对应关系

### `ref`

适合基本值或者整体替换的数据。

项目里的例子：

- `const message = ref('Loading...')`
- `const products = ref<Product[]>([])`

### `reactive`

适合表单对象这类结构化数据。

项目里的例子：

- `const userLogin = reactive(...)`
- `const productForm = reactive(...)`

### `onMounted`

相当于组件挂载完成后执行逻辑。

项目里是：

- 页面初始化时加载 session、商品、分类

### 模板语法

当前项目里你会看到：

- `v-model`
- `v-for`
- `v-if`
- `@click`

这些是 Vue 最常用的模板语法。

## 4. 你可以自己做的练习

### 初级练习

1. 把商品卡片拆成 `ProductCard.vue`
2. 把购物车区域拆成 `CartPanel.vue`
3. 把管理员资料区域拆成 `ProfilePanel.vue`

### 中级练习

1. 引入 `vue-router`
2. 把用户页和管理页拆开
3. 提取 `src/api.ts`

### 进阶练习

1. 使用 `computed`
2. 使用 `watch`
3. 引入 Pinia 做状态管理

## 5. 学 Vue 时最容易卡住的点

### `ref` 需要 `.value`

在 `script` 里你经常要写：

```ts
products.value = result.data
```

### `reactive` 一般不整体替换

所以项目里用：

```ts
Object.assign(productForm, product)
```

而不是直接重新赋值。

### 模板和脚本要分开理解

`<template>` 负责显示，
`<script setup>` 负责数据和逻辑。
