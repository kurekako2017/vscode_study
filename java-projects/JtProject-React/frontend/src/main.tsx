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
