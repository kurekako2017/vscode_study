import { NavLink, Outlet, useParams } from 'react-router-dom'

export function RouterHome() {
  // 默认子路由页面，用户进入 /router 时会先看到它。
  return <p>这里是站内路由示例首页。可以切到 About 或用户详情页。</p>
}

export function AboutPage() {
  // 普通静态子页面，用来演示切换路由后内容会改变。
  return <p>About 页面演示了简单的页面切换。</p>
}

export function UserProfile() {
  // useParams 可以读取 URL 里的动态参数，比如 users/42 的 42。
  const { id } = useParams()
  return (
    <p>
      当前用户 ID: <strong>{id}</strong>
    </p>
  )
}

export default function RouterPage() {
  // 这个父页面负责：
  // 1. 展示路由章节说明
  // 2. 提供子路由切换按钮
  // 3. 用 Outlet 渲染当前子页面
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
          {/* to="." 代表当前章节首页，也就是 /router */}
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="." end>
            Home
          </NavLink>
          {/* to="about" 会跳到 /router/about */}
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="about">
            About
          </NavLink>
          {/* 动态参数示例：/router/users/42 */}
          <NavLink className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} to="users/42">
            User 42
          </NavLink>
        </nav>

        {/* Outlet 是子路由的“插槽”，当前匹配到哪一页，就把哪一页放进来。 */}
        <div className="card" style={{ boxShadow: 'none', background: '#f8fafc' }}>
          <Outlet />
        </div>
      </article>
    </section>
  )
}
