import { useEffect, useState } from 'react'

// 测试用公共接口，返回一小批帖子数据。
// 初学者可以把它理解成“后端返回列表”的模拟示例。
const POSTS_URL = 'https://jsonplaceholder.typicode.com/posts?_limit=5'

export default function PostsDemo() {
  // loading 表示“请求还在进行中”。
  const [loading, setLoading] = useState(true)
  // error 保存错误信息，方便把失败状态单独展示出来。
  const [error, setError] = useState('')
  // posts 保存成功拿到的数据。
  const [posts, setPosts] = useState([])

  // useEffect 在组件挂载后发起请求。
  // 这里还演示了：请求完成后，如果组件卸载，要取消请求。
  useEffect(() => {
    // AbortController 可以在请求未完成时主动取消 fetch。
    const controller = new AbortController()

    async function loadPosts() {
      try {
        setLoading(true)
        setError('')

        // fetch 返回 Response，需要手动判断是否成功。
        const response = await fetch(POSTS_URL, { signal: controller.signal })
        if (!response.ok) {
          throw new Error(`请求失败: ${response.status}`)
        }

        // 把 JSON 转成 JavaScript 对象数组。
        const data = await response.json()
        setPosts(data)
      } catch (err) {
        // AbortError 代表组件卸载导致的取消，不应该当成真正错误。
        if (err.name !== 'AbortError') {
          setError(err.message)
        }
      } finally {
        // 不管成功还是失败，请求结束后都关闭 loading。
        setLoading(false)
      }
    }

    // 组件一加载就开始请求。
    loadPosts()

    // 卸载时取消请求，避免组件不在了还继续更新状态。
    return () => controller.abort()
  }, [])

  return (
    <article className="card stack">
      <span className="pill">fetch</span>
      <h3>帖子列表</h3>
      {/* 三态展示：加载中、错误、成功。 */}
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
