import { Navigate, NavLink, Route, Routes } from 'react-router-dom'
import { chapters } from './data/chapters'
import HomePage from './chapters/home/HomePage'
import HooksPage from './chapters/hooks/HooksPage'
import RouterPage from './chapters/router/RouterPage'
import ContextPage from './chapters/context/ContextPage'
import ApiPage from './chapters/api/ApiPage'
import TestPage from './chapters/test/TestPage'

function AppShell({ children }) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">React Modern Learning</p>
          <h1>现代 React 学习项目</h1>
        </div>
        <nav className="nav">
          {chapters.map((chapter) => (
            <NavLink
              key={chapter.path}
              to={chapter.path}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              {chapter.title}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="content">{children}</main>
    </div>
  )
}

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/hooks" element={<HooksPage />} />
        <Route path="/router" element={<RouterPage />} />
        <Route path="/context" element={<ContextPage />} />
        <Route path="/api" element={<ApiPage />} />
        <Route path="/test" element={<TestPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  )
}
