import { useState } from 'react'

export default function Counter() {
  // 这是一个最小测试组件：
  // 只保留一个按钮和一个状态，方便测试文件专注验证“点击后值会不会变化”。
  // 组件越小，测试目标就越明确，也越适合初学者理解。
  const [count, setCount] = useState(0)

  return (
    <article className="card stack">
      <span className="pill">测试组件</span>
      <h3>Counter</h3>
      <p>
        当前值：<strong>{count}</strong>
      </p>
      <div className="button-row">
        {/* 按钮点击后只做一件事：让数字加 1。测试也只需要验证这一件事。 */}
        <button onClick={() => setCount((value) => value + 1)}>+1</button>
      </div>
    </article>
  )
}
