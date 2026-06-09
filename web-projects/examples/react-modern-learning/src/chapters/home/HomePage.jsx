import { Link } from 'react-router-dom'
import { chapters } from '../../data/chapters'

export default function HomePage() {
  // 首页负责做“章节总入口”。
  // 每个章节都被做成卡片，点击后跳转到对应路由。
  return (
    <section className="page">
      <div className="card">
        <span className="pill">章节入口</span>
        <h2>按主题拆开的现代 React 学习页</h2>
        <p className="muted">
          这个项目故意不把所有内容塞进一个页面，而是把每个主题拆成单独章节，方便你逐项学习和改造。
        </p>
      </div>

      <div className="grid">
        {chapters.map((chapter) => (
          <Link key={chapter.path} className="card" to={chapter.path}>
            <h3>{chapter.title}</h3>
            <p className="muted">{chapter.summary}</p>
          </Link>
        ))}
      </div>
    </section>
  )
}
