import RouterDemo from './RouterDemo'

export default function RouterPage() {
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Router</span>
        <h2>路由与页面组织</h2>
        <p className="muted">这个章节用 MemoryRouter 做一个小型站内导航，不干扰外层应用路由。</p>
      </div>

      <RouterDemo />
    </section>
  )
}
