// 文件说明：
// 管理员资料编辑器（ProfileEditor）是一个受控表单组件，接收 `profileForm` 和 `setProfileForm`。
// 学习点：受控输入、局部更新表单对象、表单提交处理由父组件传入 `onSubmit`。
// 对应 JSP：updateProfile.jsp
import type { FormEvent } from 'react'

type Props = {
  profileForm: { username: string; email: string; password: string; address: string }
  setProfileForm: (value: { username: string; email: string; password: string; address: string }) => void
  onSubmit: (event: FormEvent) => void
}

// 后台资料编辑器只处理管理员个人资料，不混入其他管理功能。
export function ProfileEditor({ profileForm, setProfileForm, onSubmit }: Props) {
  return (
    <article className="panel">
      <h2>Admin Profile</h2>
      <form onSubmit={onSubmit} className="form">
        {/* 受控输入：每次输入都把新的字段合并回 profileForm 对象 */}
        {/* 对应 updateProfile.jsp 中的表单片段（示例）：
            <form action="updateuser" method="post">
              <input type="hidden" name="userid" value="${userid}">
              <input type="text" name="username" value="${username}">
              <input type="email" name="email" value="${email}">
              <input type="password" name="password" value="${password}">
              <textarea name="address">${address}</textarea>
            </form>
        */}
        <input value={profileForm.username} onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })} placeholder="Username" />
        <input value={profileForm.email} onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })} placeholder="Email" />
        <input value={profileForm.password} onChange={(e) => setProfileForm({ ...profileForm, password: e.target.value })} placeholder="Password" />
        <input value={profileForm.address} onChange={(e) => setProfileForm({ ...profileForm, address: e.target.value })} placeholder="Address" />
        {/* 提交表单后父组件会调用 saveProfileRequest 并更新状态（对应后端 /admin/profile） */}
        <button type="submit">Update Profile</button>
      </form>
    </article>
  )
}
