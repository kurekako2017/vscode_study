import ThemeContextDemo from './ThemeContextDemo'

export default function ContextPage() {
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
