import type { FormEvent } from 'react'
import { AdminAuthForm } from '../components/AdminAuthForm'
// 文件说明：
// 管理员登录视图，包含管理员登录表单，供后台访问使用。
// 学习点：表单受控组件与提交处理的常见模式。
// 对应 JSP：adminlogin.jsp
import type { AdminLoginForm } from '../services/appService'

type Props = {
  message: string
  adminLogin: AdminLoginForm
  setAdminLogin: (value: AdminLoginForm) => void
  onLogin: (event: FormEvent) => void
}

// 管理员登录页只负责收集凭据并调用统一的登录回调。
export function AdminLoginView(props: Props) {
  return (
    <section className="pageSection">
      <article className="panel authPanel narrow">
        <p className="eyebrow">Admin Login</p>
        <h1>管理员登录页</h1>
        <p className="subtitle">对应原项目里的 `adminlogin.jsp`。</p>
        {/* 直接把 props 展开传给 AdminAuthForm，让表单与父组件共享同一套状态与回调 */}
        <AdminAuthForm {...props} />
      </article>
    </section>
  )
}
