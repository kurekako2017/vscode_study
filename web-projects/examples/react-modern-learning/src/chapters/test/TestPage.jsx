import Counter from './Counter'

export default function TestPage() {
  // 这个页面负责把“组件”和“测试文件”放在同一个章节里，方便对照学习。
  // 这样你既能看到组件如何工作，也能立刻知道它对应的测试怎么写。
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Test</span>
        <h2>组件和测试文件配对</h2>
        <p className="muted">这里的目标是让组件文件和测试文件并排放，便于学习和维护。</p>
      </div>

      {/* 左边是组件，右边是说明卡片；这种布局适合初学者同时看“结果”和“测试”。 */}
      <div className="grid">
        <Counter />
        <article className="card stack">
          <h3>测试文件</h3>
          <p className="muted">对应测试见 <code>src/chapters/test/Counter.test.jsx</code>。</p>
          <p className="muted">运行命令：<code>npm test</code></p>
        </article>
      </div>
    </section>
  )
}
