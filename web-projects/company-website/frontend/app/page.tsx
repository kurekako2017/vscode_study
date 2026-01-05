import Link from 'next/link'
import { ArrowRight, CheckCircle, Mail, Phone } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* 导航栏 */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container py-4">
          <div className="flex justify-between items-center">
            <div className="text-2xl font-bold text-primary-600">公司 LOGO</div>
            <div className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-primary-600">首页</Link>
              <Link href="/about" className="text-gray-700 hover:text-primary-600">关于我们</Link>
              <Link href="/services" className="text-gray-700 hover:text-primary-600">服务</Link>
              <Link href="/news" className="text-gray-700 hover:text-primary-600">新闻动态</Link>
              <Link href="/contact" className="text-gray-700 hover:text-primary-600">联系我们</Link>
            </div>
            <Link href="/admin" className="btn-primary">
              管理后台
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero 区域 */}
      <section className="bg-gradient-to-br from-primary-50 to-blue-100 py-20">
        <div className="container">
          <div className="max-w-3xl">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              专业的企业服务<br />助力您的业务增长
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              我们提供一站式企业解决方案，帮助您的企业在数字化时代保持竞争力
            </p>
            <div className="flex gap-4">
              <Link href="/contact" className="btn-primary inline-flex items-center gap-2">
                立即咨询 <ArrowRight size={20} />
              </Link>
              <Link href="/services" className="btn-secondary">
                了解更多
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 服务特点 */}
      <section className="py-20">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">为什么选择我们</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: '专业团队', desc: '10年以上行业经验，为您提供专业服务' },
              { title: '快速响应', desc: '24小时内响应，高效解决您的问题' },
              { title: '性价比高', desc: '合理的价格，超值的服务体验' },
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                <CheckCircle className="text-primary-600 mb-4" size={40} />
                <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 最新动态 */}
      <section className="py-20 bg-gray-50">
        <div className="container">
          <div className="flex justify-between items-center mb-12">
            <h2 className="text-3xl font-bold">最新动态</h2>
            <Link href="/news" className="text-primary-600 hover:text-primary-700 flex items-center gap-2">
              查看全部 <ArrowRight size={20} />
            </Link>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[1, 2, 3].map((item) => (
              <article key={item} className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
                <div className="h-48 bg-gray-200"></div>
                <div className="p-6">
                  <div className="text-sm text-gray-500 mb-2">2026年1月{item}日</div>
                  <h3 className="text-xl font-bold mb-2">新闻标题示例 {item}</h3>
                  <p className="text-gray-600 mb-4">这里是新闻的摘要内容，简要介绍新闻的主要内容...</p>
                  <Link href={`/news/${item}`} className="text-primary-600 hover:text-primary-700 inline-flex items-center gap-2">
                    阅读更多 <ArrowRight size={16} />
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* CTA 区域 */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">准备好开始了吗？</h2>
          <p className="text-xl mb-8 opacity-90">联系我们，获取免费咨询服务</p>
          <div className="flex justify-center gap-6">
            <a href="tel:400-123-4567" className="flex items-center gap-2 text-lg hover:opacity-80">
              <Phone size={24} /> 400-123-4567
            </a>
            <a href="mailto:info@company.com" className="flex items-center gap-2 text-lg hover:opacity-80">
              <Mail size={24} /> info@company.com
            </a>
          </div>
        </div>
      </section>

      {/* 页脚 */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-white font-bold mb-4">公司名称</h3>
              <p className="text-sm">专业的企业服务提供商</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">快速链接</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/about" className="hover:text-white">关于我们</Link></li>
                <li><Link href="/services" className="hover:text-white">服务</Link></li>
                <li><Link href="/news" className="hover:text-white">新闻</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">联系方式</h4>
              <ul className="space-y-2 text-sm">
                <li>电话: 400-123-4567</li>
                <li>邮箱: info@company.com</li>
                <li>地址: 北京市朝阳区</li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">关注我们</h4>
              <div className="flex gap-4">
                <a href="#" className="hover:text-white">微信</a>
                <a href="#" className="hover:text-white">微博</a>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
            © 2026 公司名称. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
