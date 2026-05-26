import type { FormEvent } from 'react'
// 文件说明：
// 管理员认证表单（AdminAuthForm），仅包含后台登录所需字段。
// 学习点：如何向父组件回传表单状态并触发提交回调。
// 对应 JSP 表单片段：adminlogin.jsp
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
            {/* 对应 adminlogin.jsp 中的表单片段（示例）：
                <form action="/admin/loginvalidate" method="post">
                  <input type="text" name="username" placeholder="Admin username" required>
                  <input type="password" name="password" placeholder="Admin Password" required>
                </form>
            */}
            <input value={adminLogin.username} onChange={(e) => setAdminLogin({ ...adminLogin, username: e.target.value })} placeholder="Admin username" />
            <input value={adminLogin.password} type="password" onChange={(e) => setAdminLogin({ ...adminLogin, password: e.target.value })} placeholder="Admin password" />
        <button type="submit">管理员登录</button>
      </form>
    </>
  )
}
