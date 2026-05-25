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
        <input value={profileForm.username} onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })} placeholder="Username" />
        <input value={profileForm.email} onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })} placeholder="Email" />
        <input value={profileForm.password} onChange={(e) => setProfileForm({ ...profileForm, password: e.target.value })} placeholder="Password" />
        <input value={profileForm.address} onChange={(e) => setProfileForm({ ...profileForm, address: e.target.value })} placeholder="Address" />
        <button type="submit">Update Profile</button>
      </form>
    </article>
  )
}
