import { useState } from 'react'

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false)

  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-4xl font-bold mb-6">联系我们</h1>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <p className="text-gray-700 mb-4">电话: 400-123-4567</p>
          <p className="text-gray-700 mb-4">邮箱: info@company.com</p>
          <p className="text-gray-700">地址: 北京市朝阳区</p>
        </div>

        <div>
          {!submitted ? (
            <form
              onSubmit={(e) => {
                e.preventDefault()
                setSubmitted(true)
              }}
              className="bg-white p-6 rounded-xl shadow-md"
            >
              <div className="mb-4">
                <label className="block text-sm mb-1">姓名</label>
                <input name="name" className="w-full border px-3 py-2 rounded" required />
              </div>
              <div className="mb-4">
                <label className="block text-sm mb-1">邮箱</label>
                <input name="email" type="email" className="w-full border px-3 py-2 rounded" required />
              </div>
              <div className="mb-4">
                <label className="block text-sm mb-1">消息</label>
                <textarea name="message" className="w-full border px-3 py-2 rounded" rows={5} required />
              </div>
              <button className="btn-primary">发送</button>
            </form>
          ) : (
            <div className="bg-white p-6 rounded-xl shadow-md">
              <h3 className="text-xl font-semibold mb-2">感谢您的联系</h3>
              <p className="text-gray-600">我们已收到您的信息，稍后会有工作人员与您联系。</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
