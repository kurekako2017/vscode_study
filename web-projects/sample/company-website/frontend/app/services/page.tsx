import Link from 'next/link'

export default function ServicesPage() {
  const services = [
    { title: '咨询与策略', desc: '行业调研、数字化转型路线规划' },
    { title: '系统开发', desc: '定制化 Web / 后端系统开发与集成' },
    { title: '运维与支持', desc: 'SLA 支持、监控与持续交付' },
  ]

  return (
    <div className="min-h-screen container py-12">
      <h1 className="text-4xl font-bold mb-6">我们的服务</h1>

      <div className="grid md:grid-cols-3 gap-6">
        {services.map((s, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-xl font-semibold mb-2">{s.title}</h3>
            <p className="text-gray-600">{s.desc}</p>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <Link href="/contact" className="btn-primary">获取服务报价</Link>
      </div>
    </div>
  )
}
