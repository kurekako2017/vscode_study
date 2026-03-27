import type { FormEvent } from 'react'
import { AdminAuthForm } from '../components/AdminAuthForm'
import type { AdminLoginForm } from '../services/appService'

type Props = {
  message: string
  adminLogin: AdminLoginForm
  setAdminLogin: (value: AdminLoginForm) => void
  onLogin: (event: FormEvent) => void
}

export function AdminLoginView(props: Props) {
  return (
    <section className="pageSection">
      <article className="panel authPanel narrow">
        <p className="eyebrow">Admin Login</p>
        <h1>管理员登录页</h1>
        <p className="subtitle">对应原项目里的 `adminlogin.jsp`。</p>
        <AdminAuthForm {...props} />
      </article>
    </section>
  )
}
