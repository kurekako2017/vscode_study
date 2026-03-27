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
      <p className="banner">{message}</p>
      <div className="split">
        <form onSubmit={onLogin} className="form">
          <h2>Login</h2>
          <input value={userLogin.username} onChange={(e) => setUserLogin({ ...userLogin, username: e.target.value })} placeholder="Username" />
          <input value={userLogin.password} type="password" onChange={(e) => setUserLogin({ ...userLogin, password: e.target.value })} placeholder="Password" />
          <button type="submit">登录</button>
        </form>
        <form onSubmit={onRegister} className="form">
          <h2>Register</h2>
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
