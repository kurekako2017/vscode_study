import { MemoryRouter, NavLink, Navigate, Route, Routes, useParams } from 'react-router-dom'

function UserProfile() {
  const { id } = useParams()
  return <p>当前用户 ID: <strong>{id}</strong></p>
}

function RouterHome() {
  return <p>这里是站内路由示例首页。可以切到 About 或用户详情页。</p>
}

function AboutPage() {
  return <p>About 页面演示了简单的页面切换。</p>
}

export default function RouterDemo() {
  return (
    <article className="card stack">
      <span className="pill">MemoryRouter</span>
      <MemoryRouter initialEntries={['/']}>
        <nav className="button-row">
          <NavLink
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            to="/"
          >
            Home
          </NavLink>
          <NavLink
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            to="/about"
          >
            About
          </NavLink>
          <NavLink
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            to="/users/42"
          >
            User 42
          </NavLink>
        </nav>

        <div className="card" style={{ boxShadow: 'none', background: '#f8fafc' }}>
          <Routes>
            <Route path="/" element={<RouterHome />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/users/:id" element={<UserProfile />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </MemoryRouter>
    </article>
  )
}
