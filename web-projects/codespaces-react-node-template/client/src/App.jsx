import React, { useEffect, useState } from 'react'

export default function App() {
  const [msg, setMsg] = useState('loading...')

  useEffect(() => {
    fetch('/api/hello')
      .then((r) => r.json())
      .then((d) => setMsg(d.message))
      .catch(() => setMsg('无法连接到后端'))
  }, [])

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>React + Node 模板</h1>
      <p>后端消息：{msg}</p>
      <p>在 Codespaces 中运行：前端端口 3000，后端端口 4000。</p>
    </div>
  )
}
