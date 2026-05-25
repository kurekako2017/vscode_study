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
          <NavLink to="/login">用户登录</NavLink>
          <NavLink to="/products">商品页</NavLink>
          <NavLink to="/cart">购物车</NavLink>
          <NavLink to="/admin/login">管理登录</NavLink>
          <NavLink to="/admin/dashboard">管理后台</NavLink>
          {authenticated ? <button onClick={onUserLogout}>退出用户</button> : null}
          {adminLoggedIn ? <button onClick={onAdminLogout}>退出管理</button> : null}
        </nav>
      </header>
      {children}
    </main>
  )
}
