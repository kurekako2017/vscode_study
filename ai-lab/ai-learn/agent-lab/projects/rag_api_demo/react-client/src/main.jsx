import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// 把 React 应用挂载到 index.html 中 id="root" 的 DOM 节点。
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
