import { Navigate, NavLink, Route, Routes } from 'react-router-dom'
import { chapters } from './data/chapters'
import HomePage from './chapters/home/HomePage'
import HooksPage from './chapters/hooks/HooksPage'
import RouterPage from './chapters/router/RouterPage'
import { AboutPage, RouterHome, UserProfile } from './chapters/router/RouterPage'
import ContextPage from './chapters/context/ContextPage'
import ApiPage from './chapters/api/ApiPage'
import TestPage from './chapters/test/TestPage'

// AppShell 是“公共外壳”。
// 顶部导航、标题、页面容器都统一放在这里，方便各章节共享布局。
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
  // Routes 根据地址栏中的路径决定显示哪个章节。
  // 这样每个学习主题都能单独访问、单独分享、单独练习。
  return (
    <AppShell>
      <Routes>
        {/* 首页：展示所有章节卡片 */}
        <Route path="/" element={<HomePage />} />
        {/* Hooks：演示组件状态和副作用 */}
        <Route path="/hooks" element={<HooksPage />} />
        {/* Router：演示嵌套路由和动态参数 */}
        <Route path="/router/*" element={<RouterPage />}>
          <Route index element={<RouterHome />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="users/:id" element={<UserProfile />} />
          {/* 未匹配到子路由时回到当前章节首页 */}
          <Route path="*" element={<Navigate to="." replace />} />
        </Route>
        {/* Context：演示跨层传值 */}
        <Route path="/context" element={<ContextPage />} />
        {/* API：演示请求数据和 loading / error / success 状态 */}
        <Route path="/api" element={<ApiPage />} />
        {/* Test：演示组件和测试文件如何配对 */}
        <Route path="/test" element={<TestPage />} />
        {/* 所有未匹配路由都回到首页，避免白屏 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  )
}
