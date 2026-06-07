import { useState } from 'react'

export default function Counter() {
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
