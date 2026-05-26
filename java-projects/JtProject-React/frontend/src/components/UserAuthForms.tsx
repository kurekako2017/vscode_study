// 文件说明：
// 用户登录与注册表单组合组件，会把表单状态提升到父组件（AppShell）。
// 学习点：演示受控组件与父组件回调的标准模式。
// 对应 JSP：userLogin.jsp（登录表单）、register.jsp（注册表单）
import type { FormEvent } from 'react'
import type { RegisterForm, UserLoginForm } from '../services/appService'

type Props = {
  message: string
  userLogin: UserLoginForm
  registerForm: RegisterForm
  setUserLogin: (value: UserLoginForm) => void
  setRegisterForm: (value: RegisterForm) => void
  onLogin: (event: FormEvent) => void
  onRegister: (event: FormEvent) => void
}

export function UserAuthForms(props: Props) {
  const { message, userLogin, registerForm, setUserLogin, setRegisterForm, onLogin, onRegister } = props

  return (
    <>
      {/* 页面顶端横幅，用于显示来自父组件的提示消息 */}
      <p className="banner">{message}</p>
      <div className="split">
        <form onSubmit={onLogin} className="form">
          <h2>Login</h2>
          {/* 登录表单：受控输入，onSubmit 由父组件传入以便统一处理 */}
          {/* 对应 userLogin.jsp 中的表单片段（示例）：
              <form action="/userloginvalidate" method="post">
                <input type="text" name="username" id="username" placeholder="Username*" required>
                <input type="password" name="password" id="password" placeholder="Password*" required>
              </form>
          */}
          <input value={userLogin.username} onChange={(e) => setUserLogin({ ...userLogin, username: e.target.value })} placeholder="Username" />
          <input value={userLogin.password} type="password" onChange={(e) => setUserLogin({ ...userLogin, password: e.target.value })} placeholder="Password" />
          <button type="submit">登录</button>
        </form>
        <form onSubmit={onRegister} className="form">
          <h2>Register</h2>
          {/* 注册表单：输入会合并回 registerForm，提交后父组件会调用注册 API */}
          {/* 对应 register.jsp 中的表单片段（示例）：
              <form action="newuserregister" method="post">
                <input type="text" name="username">
                <input type="email" name="email">
                <input type="password" name="password">
                <textarea name="address"></textarea>
              </form>
          */}
          <input value={registerForm.username} onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })} placeholder="New username" />
          <input value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} placeholder="Email" />
          <input value={registerForm.password} type="password" onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} placeholder="Password" />
          <input value={registerForm.address} onChange={(e) => setRegisterForm({ ...registerForm, address: e.target.value })} placeholder="Address" />
          <button type="submit">注册并登录</button>
        </form>
      </div>
    </>
  )
}
