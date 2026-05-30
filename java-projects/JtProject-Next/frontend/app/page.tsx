'use client'

// 'use client' 表示这个页面是 Client Component。
// 本页面需要 useState、useEffect、表单事件和按钮点击，所以必须在浏览器端运行。

import { FormEvent, useEffect, useMemo, useState } from 'react'
import { api } from '@/lib/api'
import type { AdminOverview, Product, SessionInfo } from '@/lib/types'

// 空会话对象用于初始化 state。
// 明确标注 SessionInfo 可以让 TypeScript 检查字段是否完整。
const emptySession: SessionInfo = {
  authenticated: false,
  username: '',
  role: '',
  adminLoggedIn: false,
  adminUsername: ''
}

// app/page.tsx 会自动映射为首页路由 /。
// 这是 Next.js App Router 的约定式路由：文件路径就是 URL 结构。
export default function Home() {
  // 商品列表：来自后端 GET /api/products。
  const [products, setProducts] = useState<Product[]>([])

  // 购物车列表：登录普通用户后通过 /api/cart 或 /api/cart/items/{id} 更新。
  const [cart, setCart] = useState<Product[]>([])

  // session 保存当前普通用户和管理员登录状态。
  const [session, setSession] = useState<SessionInfo>(emptySession)

  // 后台概览允许为空，表示还没有加载或管理员未登录。
  const [overview, setOverview] = useState<AdminOverview | null>(null)

  // 表单 state 使用对象保存，输入框 onChange 时复制旧对象并替换单个字段。
  const [user, setUser] = useState({ username: 'lisa', password: '765' })
  const [admin, setAdmin] = useState({ username: 'admin', password: '123' })

  // message 和 loading 是页面级反馈状态，所有 API 动作共用。
  const [message, setMessage] = useState('Ready')
  const [loading, setLoading] = useState(false)

  // useMemo 用于从 cart 派生总价。
  // 只有 cart 变化时才重新计算，避免每次渲染都重复 reduce。
  const cartTotal = useMemo(() => cart.reduce((sum, item) => sum + Number(item.price || 0), 0), [cart])

  // 首页初始化数据加载：
  // Promise.all 并行请求 session 和 products，比串行等待更快。
  async function loadInitialData() {
    setLoading(true)
    try {
      const [sessionResult, productResult] = await Promise.all([
        api<SessionInfo>('/session'),
        api<Product[]>('/products')
      ])
      setSession(sessionResult.data)
      setProducts(productResult.data)
      setMessage(productResult.message)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  // useEffect 在 Client Component 首次挂载后执行。
  // void 表示我们有意不 await 这个 Promise，避免 React effect 返回 Promise。
  useEffect(() => {
    void loadInitialData()
  }, [])

  // React 表单提交事件类型写成 FormEvent<HTMLFormElement>。
  // event.preventDefault() 阻止浏览器刷新页面，改由 fetch 调后端 API。
  async function submitUserLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await runAction(async () => {
      const result = await api<SessionInfo>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(user)
      })
      setSession(result.data)
      setMessage(result.message)
      await loadCart()
    })
  }

  // 管理员登录和普通用户登录共享同一个 API 封装，但调用不同后端路径。
  async function submitAdminLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await runAction(async () => {
      const result = await api<SessionInfo>('/admin/login', {
        method: 'POST',
        body: JSON.stringify(admin)
      })
      setSession(result.data)
      setMessage(result.message)
      await loadOverview()
    })
  }

  // 添加购物车时只需要商品 id，登录用户由后端根据 cookie/session 判断。
  async function addToCart(productId: number) {
    await runAction(async () => {
      const result = await api<Product[]>(`/cart/items/${productId}`, { method: 'POST' })
      setCart(result.data)
      setMessage(result.message)
    })
  }

  // 删除购物车商品使用 DELETE 方法，和 REST 风格的后端接口保持一致。
  async function removeFromCart(productId: number) {
    await runAction(async () => {
      const result = await api<Product[]>(`/cart/items/${productId}`, { method: 'DELETE' })
      setCart(result.data)
      setMessage(result.message)
    })
  }

  // 单独封装 loadCart，方便登录成功后自动加载，也方便按钮手动刷新。
  async function loadCart() {
    const result = await api<Product[]>('/cart')
    setCart(result.data)
  }

  // 后台概览要求管理员登录，否则后端会返回未授权错误。
  async function loadOverview() {
    const result = await api<AdminOverview>('/admin/overview')
    setOverview(result.data)
  }

  // runAction 是页面内的小型通用流程：
  // 开始前进入 loading，成功时由具体 action 更新数据，失败时统一展示错误消息。
  async function runAction(action: () => Promise<void>) {
    setLoading(true)
    try {
      await action()
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Action failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    // JSX 是 TypeScript 中的 UI 描述语法。
    // className 对应 app/globals.css 中的样式类。
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Spring Boot + Next.js + TypeScript</p>
          <h1>JtProject Next</h1>
        </div>
        <div className="status" aria-live="polite">
          <span className={loading ? 'dot busy' : 'dot'} />
          {message}
        </div>
      </header>

      {/* dashboard 区域展示 session 与两个登录表单，是理解受控表单的主要位置。 */}
      <section className="dashboard">
        <div className="panel session-panel">
          <h2>Session</h2>
          <dl>
            <div>
              <dt>User</dt>
              <dd>{session.authenticated ? session.username : 'Guest'}</dd>
            </div>
            <div>
              <dt>Admin</dt>
              <dd>{session.adminLoggedIn ? session.adminUsername : 'Not signed in'}</dd>
            </div>
          </dl>
        </div>

        <form className="panel form-panel" onSubmit={submitUserLogin}>
          <h2>User Login</h2>
          <label>
            Username
            {/* value + onChange 组成受控组件：页面 state 是输入框的唯一数据来源。 */}
            <input value={user.username} onChange={(event) => setUser({ ...user, username: event.target.value })} />
          </label>
          <label>
            Password
            <input
              type="password"
              value={user.password}
              onChange={(event) => setUser({ ...user, password: event.target.value })}
            />
          </label>
          <button type="submit">Login User</button>
        </form>

        <form className="panel form-panel" onSubmit={submitAdminLogin}>
          <h2>Admin Login</h2>
          <label>
            Username
            {/* 展开运算符 ...admin 保留 password，只替换 username。 */}
            <input value={admin.username} onChange={(event) => setAdmin({ ...admin, username: event.target.value })} />
          </label>
          <label>
            Password
            <input
              type="password"
              value={admin.password}
              onChange={(event) => setAdmin({ ...admin, password: event.target.value })}
            />
          </label>
          <button type="submit">Login Admin</button>
        </form>
      </section>

      <section className="content-grid">
        <div className="product-area">
          <div className="section-title">
            <h2>Products</h2>
            <button type="button" className="secondary" onClick={() => void loadInitialData()}>
              Refresh
            </button>
          </div>
          <div className="product-grid">
            {/* products.map 把后端数组转换成一组商品卡片；key 帮助 React 识别列表项。 */}
            {products.map((product) => (
              <article className="product-card" key={product.id}>
                <div>
                  <p className="category">{product.categoryName || 'Uncategorized'}</p>
                  <h3>{product.name}</h3>
                  <p>{product.description || 'No description yet.'}</p>
                </div>
                <div className="product-meta">
                  <span>${Number(product.price || 0).toFixed(2)}</span>
                  <span>{product.quantity} in stock</span>
                </div>
                <button type="button" onClick={() => void addToCart(product.id)}>
                  Add to Cart
                </button>
              </article>
            ))}
          </div>
        </div>

        <aside className="side-panel">
          <section className="panel">
            <div className="section-title">
              <h2>Cart</h2>
              <button type="button" className="secondary" onClick={() => void runAction(loadCart)}>
                Load
              </button>
            </div>
            <ul className="cart-list">
              {/* 购物车为空时显示兜底状态；有数据时渲染每个商品和删除按钮。 */}
              {cart.map((item) => (
                <li key={`${item.id}-${item.name}`}>
                  <span>{item.name}</span>
                  <button type="button" className="link-button" onClick={() => void removeFromCart(item.id)}>
                    Remove
                  </button>
                </li>
              ))}
              {cart.length === 0 && <li className="muted">Cart is empty</li>}
            </ul>
            <strong>Total: ${cartTotal.toFixed(2)}</strong>
          </section>

          <section className="panel">
            <div className="section-title">
              <h2>Admin</h2>
              <button type="button" className="secondary" onClick={() => void runAction(loadOverview)}>
                Load
              </button>
            </div>
            {/* 可选链 ?. 避免 overview 还没加载时访问属性报错。 */}
            <dl className="stats">
              <div>
                <dt>Products</dt>
                <dd>{overview?.productCount ?? '-'}</dd>
              </div>
              <div>
                <dt>Categories</dt>
                <dd>{overview?.categoryCount ?? '-'}</dd>
              </div>
              <div>
                <dt>Customers</dt>
                <dd>{overview?.customerCount ?? '-'}</dd>
              </div>
            </dl>
          </section>
        </aside>
      </section>
    </main>
  )
}
