import { useState } from 'react'

export default function Counter() {
  // 这是一个最小测试组件：
  // 只保留一个按钮和一个状态，方便测试文件专注验证“点击后值会不会变化”。
  const [count, setCount] = useState(0)

  return (
    <article className="card stack">
      <span className="pill">测试组件</span>
      <h3>Counter</h3>
      <p>
        当前值：<strong>{count}</strong>
      </p>
      <div className="button-row">
        <button onClick={() => setCount((value) => value + 1)}>+1</button>
      </div>
    </article>
  )
}
