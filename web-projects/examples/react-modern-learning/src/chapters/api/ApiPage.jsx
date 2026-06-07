import PostsDemo from './PostsDemo'

export default function ApiPage() {
  return (
    <section className="page">
      <div className="card">
        <span className="pill">API</span>
        <h2>请求数据与状态分支</h2>
        <p className="muted">这个章节练的是 loading、error、success 三种常见状态。</p>
      </div>

      <PostsDemo />
    </section>
  )
}
