// client/src/main.jsx
// 入口 JS：负责将 React 应用挂载到 `div#root`。
// 说明：
// - Vite 会按 ESM 模块加载本文件（开发环境无需打包）。
// - `React.StrictMode` 用于开发模式下的额外检查（不会影响生产渲染，但会触发双重渲染以检测副作用）。
// - 如需初始化全局状态、样式或提供 Context，可在这里进行扩展。
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
