import ThemeContextDemo from './ThemeContextDemo'

export default function ContextPage() {
  // 这里是 Context 章节的外层容器，实际的 Provider/Consumer 示例放在 ThemeContextDemo。
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Context</span>
        <h2>跨层传值</h2>
        <p className="muted">这个章节展示 Provider、useContext 和主题切换。</p>
      </div>

      <ThemeContextDemo />
    </section>
  )
}
