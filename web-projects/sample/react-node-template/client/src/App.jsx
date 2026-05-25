import React, { useEffect, useState } from 'react'

// client/src/App.jsx
// 教学注释：演示如何在 React 中向后端发起请求并显示结果。
export default function App() {
  // 使用 useState 保存从后端获取到的消息（初始为 loading...）
  const [msg, setMsg] = useState('loading...')

  // useEffect 在组件首次挂载时运行一次（空依赖数组）
  useEffect(() => {
    // fetch 调用到 /api/hello，由 Vite 的代理或实际后端处理
    fetch('/api/hello')
      // 解析 JSON 响应
      .then((r) => r.json())
      // 把后端返回的 message 字段放入 state，触发重渲染
      .then((d) => setMsg(d.message))
      // 如果网络错误或后端不可达，设置错误提示（中文）
      .catch(() => setMsg('无法连接到后端'))
  }, [])

  // 简单的 UI：标题 + 后端返回的消息
  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>React + Node 模板</h1>
      <p>后端消息：{msg}</p>
      <p>在本地开发时：前端通常在端口 3000，后端在 4000，Vite 代理会把 `/api` 转发给后端。</p>
    </div>
  )
}
