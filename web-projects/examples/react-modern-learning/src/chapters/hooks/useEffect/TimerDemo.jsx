import { useEffect, useState } from 'react'

export default function TimerDemo() {
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    const id = window.setInterval(() => {
      setSeconds((value) => value + 1)
    }, 1000)

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
