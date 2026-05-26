// 文件说明：
// 应用入口（entrypoint），负责把 React 根组件挂载到 HTML 中。
// 学习点：
// - 使用 `ReactDOM.createRoot` 初始化应用
// - 把全局样式（styles.css）在入口处引入
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// 应用入口只负责挂载根组件和全局样式，页面逻辑都下放到 App 里处理。
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
