import { Navigate, NavLink, Route, Routes } from 'react-router-dom'
import { chapters } from './data/chapters'
import HomePage from './chapters/home/HomePage'
import HooksPage from './chapters/hooks/HooksPage'
import RouterPage from './chapters/router/RouterPage'
import { AboutPage, RouterHome, UserProfile } from './chapters/router/RouterPage'
import ContextPage from './chapters/context/ContextPage'
import ApiPage from './chapters/api/ApiPage'
import TestPage from './chapters/test/TestPage'

// AppShell 是整个学习站点的“公共外壳”。
// 所有章节都会共用这层结构，所以把标题、导航、内容容器统一放在这里最合适。
function AppShell({ children }) {
  return (
    <div className="app-shell">
      {/* 顶部区域负责展示项目标题和章节导航。 */}
      <header className="topbar">
        <div>
          <p className="eyebrow">React Modern Learning</p>
          <h1>现代 React 学习项目</h1>
        </div>
        {/* 导航栏直接根据 chapters 数据生成，避免手写重复链接。 */}
        <nav className="nav">
          {chapters.map((chapter) => (
            <NavLink
              key={chapter.path}
              to={chapter.path}
              // NavLink 会自动知道当前链接是否匹配路由；
              // isActive 为 true 时我们就额外加上 active 类名，方便高亮当前章节。
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
  // 你可以把它理解成“地址栏 = 当前该看哪一页”。
  return (
    <AppShell>
      {/* Routes 负责根据当前路径挑选要渲染的页面。 */}
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
          {/* 如果子路由没有匹配成功，就回到当前章节首页，避免页面空白。 */}
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
