import { useEffect, useState } from 'react'

export default function TimerDemo() {
  // seconds 记录这个组件已经“运行了多久”。
  const [seconds, setSeconds] = useState(0)

  // useEffect 用来演示副作用：
  // 组件挂载后启动定时器，卸载时清理定时器。
  // 这类“开始一个外部动作 + 结束时收尾”的逻辑，很适合放进 useEffect。
  useEffect(() => {
    // setInterval 每 1 秒执行一次回调。
    const id = window.setInterval(() => {
      // 同样使用函数式更新，避免拿到旧状态。
      setSeconds((value) => value + 1)
    }, 1000)

    // 清理函数：组件卸载时停止定时器，防止内存泄漏。
    return () => window.clearInterval(id)
  }, [])

  return (
    <article className="card stack">
      <span className="pill">useEffect</span>
      <h3>定时器</h3>
      <p className="muted">这个例子练的是副作用执行和清理。</p>
      <p>
        已运行：<strong>{seconds}</strong> 秒
      </p>
      <div className="button-row">
        <button onClick={() => setSeconds(0)}>归零</button>
      </div>
    </article>
  )
}
