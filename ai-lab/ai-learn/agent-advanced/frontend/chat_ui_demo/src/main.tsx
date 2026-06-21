import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// StrictMode 会在开发环境帮助发现不安全的副作用和旧 API。
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
