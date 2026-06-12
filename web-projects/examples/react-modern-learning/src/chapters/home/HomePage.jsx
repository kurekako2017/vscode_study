import { Link } from 'react-router-dom'
import { chapters } from '../../data/chapters'

export default function HomePage() {
  // 首页负责做“章节总入口”。
  // 每个章节都被做成卡片，点击后跳转到对应路由。
  // 这里尽量不写复杂逻辑，只负责把章节目录展示给用户。
  return (
    <section className="page">
      <div className="card">
        <span className="pill">章节入口</span>
        <h2>按主题拆开的现代 React 学习页</h2>
        <p className="muted">
          这个项目故意不把所有内容塞进一个页面，而是把每个主题拆成单独章节，方便你逐项学习和改造。
        </p>
      </div>

      {/* 用 grid 把每个章节卡片排成网格，页面更像一个学习目录。 */}
      <div className="grid">
        {chapters.map((chapter) => (
          // Link 负责跳转到章节对应的路由。
          // 这里的 chapter 来自统一的数据源，所以新增章节时只要改一处。
          <Link key={chapter.path} className="card" to={chapter.path}>
            <h3>{chapter.title}</h3>
            <p className="muted">{chapter.summary}</p>
          </Link>
        ))}
      </div>
    </section>
  )
}
