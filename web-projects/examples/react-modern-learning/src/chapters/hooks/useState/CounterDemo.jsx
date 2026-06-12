import { useMemo, useState } from 'react'

export default function CounterDemo() {
  // count 保存当前计数值，是最基础的组件状态示例。
  const [count, setCount] = useState(0)
  // step 保存每次点击按钮时增加多少，顺便演示表单控件和 state 的联动。
  const [step, setStep] = useState(1)

  // doubled 不是独立状态，而是由 count 推导出来的结果。
  // 这里用 useMemo 只是为了说明“派生值可以按依赖缓存”。
  // 初学者可以先把它理解成“计算结果缓存”，而不是新的数据源。
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
        {/* 函数式更新可以确保拿到最新的 count，初学者要重点记住这一点。 */}
        <button onClick={() => setCount((value) => value + step)}>+{step}</button>
        <button className="secondary" onClick={() => setCount(0)}>重置</button>
      </div>
      <label className="stack">
        步进
        {/* select 的 value 由 state 控制，onChange 再把新值写回 state。 */}
        <select value={step} onChange={(event) => setStep(Number(event.target.value))}>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="5">5</option>
        </select>
      </label>
    </article>
  )
}
