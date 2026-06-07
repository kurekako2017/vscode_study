import { useMemo, useState } from 'react'

export default function CounterDemo() {
  const [count, setCount] = useState(0)
  const [step, setStep] = useState(1)

  const doubled = useMemo(() => count * 2, [count])

  return (
    <article className="card stack">
      <span className="pill">useState</span>
      <h3>计数器</h3>
      <p className="muted">这个例子练的是状态更新、事件处理和派生值。</p>
      <p>
        当前值：<strong>{count}</strong>
      </p>
      <p>
        派生值：<strong>{doubled}</strong>
      </p>
      <div className="button-row">
        <button onClick={() => setCount((value) => value + step)}>+{step}</button>
        <button className="secondary" onClick={() => setCount(0)}>重置</button>
      </div>
      <label className="stack">
        步进
        <select value={step} onChange={(event) => setStep(Number(event.target.value))}>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="5">5</option>
        </select>
      </label>
    </article>
  )
}
