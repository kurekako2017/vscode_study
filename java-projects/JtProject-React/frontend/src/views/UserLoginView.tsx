import type { FormEvent } from 'react'
// 文件说明：
// 普通用户登录/注册视图，封装了登录与注册两个表单区域。
// 学习点：如何把表单状态与回调从父组件传入到子组件并处理提交事件。
// 对应 JSP：userLogin.jsp（登录）、register.jsp（注册）
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

// 用户登录与注册页面共用一组表单状态，避免在路由层重复拆分逻辑。
export function UserLoginView(props: Props) {
  return (
    <section className="pageSection">
      <article className="panel authPanel">
        <div>
          <p className="eyebrow">User Login</p>
          <h1>用户登录页</h1>
          <p className="subtitle">对应原来的 `userLogin.jsp` 和 `register.jsp`，现在拆成了独立路由页面。</p>
        </div>
        {/* 把 message、表单状态和回调全部传给组合表单组件，由该组件负责渲染两个表单 */}
        <UserAuthForms {...props} />
      </article>
    </section>
  )
}
