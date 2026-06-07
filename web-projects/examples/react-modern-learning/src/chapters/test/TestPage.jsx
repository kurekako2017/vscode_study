import Counter from './Counter'

export default function TestPage() {
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Test</span>
        <h2>组件和测试文件配对</h2>
        <p className="muted">这里的目标是让组件文件和测试文件并排放，便于学习和维护。</p>
      </div>

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
