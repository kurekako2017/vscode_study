export default function AdminPage() {
  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-4xl font-bold mb-6">管理后台（演示）</h1>
      <p className="text-gray-700 mb-4">此页面为演示用的管理后台占位。生产中请替换为真正的认证与管理界面。</p>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h3 className="font-semibold mb-2">站点统计</h3>
          <ul className="text-sm text-gray-600">
            <li>页面访问: 1234</li>
            <li>联系人表单: 12</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <h3 className="font-semibold mb-2">内容管理</h3>
          <p className="text-gray-600 text-sm">示例：管理新闻、页面与服务条目。</p>
        </div>
      </div>
    </div>
  )
}
