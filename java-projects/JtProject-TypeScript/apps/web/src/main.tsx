import React from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'
import './styles.css'

// main.tsx 是浏览器端入口。
// Vite 从 index.html 读取这个文件，然后把 React 应用挂载到 #root。
//
// 对照传统后端页面：
// - JSP/Thymeleaf 是后端直接生成 HTML
// - 这里是浏览器先拿到 index.html，再由 React 接管页面渲染
const root = document.getElementById('root')

// TypeScript 无法保证 HTML 里一定存在 #root，所以这里做运行时检查。
// 检查通过后，root 的类型就从 HTMLElement | null 缩窄为 HTMLElement。
if (!root) {
  throw new Error('Root element was not found')
}

// React.StrictMode 只在开发环境帮助发现潜在问题。
// 它可能让某些生命周期逻辑执行两次，这是 React 故意用来提醒副作用问题的机制。
createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
