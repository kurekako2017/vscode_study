import type { FormEvent } from 'react'
import type { AdminLoginForm } from '../services/appService'

type Props = {
  message: string
  adminLogin: AdminLoginForm
  setAdminLogin: (value: AdminLoginForm) => void
  onLogin: (event: FormEvent) => void
}

// 管理员认证表单统一承载提示信息和输入控件，供登录页复用。
export function AdminAuthForm({ message, adminLogin, setAdminLogin, onLogin }: Props) {
  return (
    <>
      <p className="banner">{message}</p>
      <form onSubmit={onLogin} className="form">
        <input value={adminLogin.username} onChange={(e) => setAdminLogin({ ...adminLogin, username: e.target.value })} placeholder="Admin username" />
        <input value={adminLogin.password} type="password" onChange={(e) => setAdminLogin({ ...adminLogin, password: e.target.value })} placeholder="Admin password" />
        <button type="submit">管理员登录</button>
      </form>
    </>
  )
}
