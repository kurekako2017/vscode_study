import Link from 'next/link'

export default function AboutPage() {
  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-4xl font-bold mb-6">关于我们</h1>
      <p className="text-lg text-gray-700 mb-6">
        我们是专注于企业数字化转型的服务团队，拥有多年行业经验，提供从咨询、设计到实施的全流程服务。
      </p>

      <section className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-semibold mb-4">我们的使命</h2>
        <p className="text-gray-600 mb-4">帮助企业在快速变化的商业环境中稳健成长，提升业务效率与用户体验。</p>

        <h3 className="text-xl font-semibold mt-4">团队</h3>
        <ul className="list-disc list-inside text-gray-600">
          <li>产品与业务咨询</li>
          <li>技术架构与实现</li>
          <li>运维与持续交付</li>
        </ul>
      </section>

      <div className="mt-8">
        <Link href="/contact" className="btn-primary">联系我们</Link>
      </div>
    </div>
  )
}
