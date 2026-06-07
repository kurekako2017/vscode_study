import { useEffect, useState } from 'react'

const POSTS_URL = 'https://jsonplaceholder.typicode.com/posts?_limit=5'

export default function PostsDemo() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [posts, setPosts] = useState([])

  useEffect(() => {
    const controller = new AbortController()

    async function loadPosts() {
      try {
        setLoading(true)
        setError('')

        const response = await fetch(POSTS_URL, { signal: controller.signal })
        if (!response.ok) {
          throw new Error(`请求失败: ${response.status}`)
        }

        const data = await response.json()
        setPosts(data)
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }

    loadPosts()

    return () => controller.abort()
  }, [])

  return (
    <article className="card stack">
      <span className="pill">fetch</span>
      <h3>帖子列表</h3>
      {loading ? <p>Loading...</p> : null}
      {!loading && error ? <p>{error}</p> : null}
      {!loading && !error ? (
        <ol>
          {posts.map((post) => (
            <li key={post.id}>
              <strong>{post.title}</strong>
              <p className="muted">{post.body}</p>
            </li>
          ))}
        </ol>
      ) : null}
    </article>
  )
}
