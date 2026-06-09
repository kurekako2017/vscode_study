import CounterDemo from './useState/CounterDemo'
import TimerDemo from './useEffect/TimerDemo'

export default function HooksPage() {
  // 这个页面本身不放复杂逻辑，只做章节封面和内容容器。
  // 真正的练习点放在下面两个 demo。
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Hooks</span>
        <h2>从 useState 和 useEffect 开始</h2>
        <p className="muted">先把局部状态和副作用搞清楚，再扩展到更复杂的逻辑。</p>
      </div>

      <div className="grid">
        <CounterDemo />
        <TimerDemo />
      </div>
    </section>
  )
}
