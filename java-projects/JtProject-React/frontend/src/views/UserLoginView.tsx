import type { FormEvent } from 'react'
import { UserAuthForms } from '../components/UserAuthForms'
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

export function UserLoginView(props: Props) {
  return (
    <section className="pageSection">
      <article className="panel authPanel">
        <div>
          <p className="eyebrow">User Login</p>
          <h1>用户登录页</h1>
          <p className="subtitle">对应原来的 `userLogin.jsp` 和 `register.jsp`，现在拆成了独立路由页面。</p>
        </div>
        <UserAuthForms {...props} />
      </article>
    </section>
  )
}
