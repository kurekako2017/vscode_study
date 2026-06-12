import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './style.css'

// 入口文件的职责很单纯：
// 1. 把 React 应用挂到页面上的 #root
// 2. 用 BrowserRouter 包住整个应用，后续页面才能使用路由
// 3. 加载全局样式，让整个项目的视觉统一
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
