import { NavLink, Outlet, useParams } from 'react-router-dom'

export function RouterHome() {
  return <p>这里是站内路由示例首页。可以切到 About 或用户详情页。</p>
}

export function AboutPage() {
  return <p>About 页面演示了简单的页面切换。</p>
}

export function UserProfile() {
  const { id } = useParams()
  return (
    <p>
      当前用户 ID: <strong>{id}</strong>
    </p>
  )
}

export default function RouterPage() {
  return (
    <section className="page">
      <div className="card">
        <span className="pill">Router</span>
        <h2>路由与页面组织</h2>
        <p className="muted">这个章节直接挂在外层 BrowserRouter 上，用嵌套路由演示页面切换。</p>
      </div>

      <article className="card stack">
        <span className="pill">Nested Routes</span>
        <nav className="button-row">
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="." end>
            Home
          </NavLink>
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="about">
            About
          </NavLink>
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="users/42">
            User 42
          </NavLink>
        </nav>

        <div className="card" style={{ boxShadow: 'none', background: '#f8fafc' }}>
          <Outlet />
        </div>
      </article>
    </section>
  )
}
