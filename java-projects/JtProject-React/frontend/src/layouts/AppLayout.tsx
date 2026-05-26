// 文件说明：
// 应用布局组件，包含全局导航（顶部）与内容容器。几乎所有页面都嵌入在该布局中。
// 学习点：
// - 使用 `PropsWithChildren` 接收 `children`，这是构建布局组件的常见做法
// 对应 JSP 参考：index.jsp、adminHome.jsp 中的顶部/导航布局，可用作对照
import type { PropsWithChildren } from 'react'
import { NavLink } from 'react-router-dom'

type Props = PropsWithChildren<{
  authenticated: boolean
  adminLoggedIn: boolean
  onUserLogout: () => void
  onAdminLogout: () => void
}>

// 页面统一外壳：顶部导航、退出按钮和内容容器都放在这一层。
export function AppLayout({ authenticated, adminLoggedIn, onUserLogout, onAdminLogout, children }: Props) {
  return (
    <main className="page">
      <header className="hero compact">
        <div>
          <p className="eyebrow">JtProject React Edition</p>
          <h1>Spring Boot + React 多页面结构</h1>
        </div>
        <nav className="topnav">
          {/* 导航链接：使用路由的 NavLink，可根据路径激活样式 */}
          <NavLink to="/login">用户登录</NavLink>
          <NavLink to="/products">商品页</NavLink>
          <NavLink to="/cart">购物车</NavLink>
          <NavLink to="/admin/login">管理登录</NavLink>
          <NavLink to="/admin/dashboard">管理后台</NavLink>
          {/* 根据鉴权状态显示退出按钮（点击调用父组件回调完成登出） */}
          {authenticated ? <button onClick={onUserLogout}>退出用户</button> : null}
          {adminLoggedIn ? <button onClick={onAdminLogout}>退出管理</button> : null}
        </nav>
      </header>
      {children}
    </main>
  )
}
