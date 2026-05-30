import { LogIn, PackagePlus, RefreshCw, ShieldCheck, ShoppingCart, Trash2 } from 'lucide-react'
import { FormEvent, useEffect, useMemo, useState } from 'react'
import type { AdminOverview, Product, SessionInfo } from '../../../packages/shared/src/index'
import { api } from './api'

const emptySession: SessionInfo = {
  authenticated: false,
  username: '',
  role: '',
  adminLoggedIn: false,
  adminUsername: ''
}

// App 是这个纯 TypeScript 前端的主组件。
//
// 它承担三件事：
// 1. 保存页面状态：products/cart/session/overview/form/message/loading
// 2. 调用后端 API：登录、加载商品、购物车、后台概览
// 3. 根据 state 渲染界面：商品卡片、购物车、统计信息
export function App() {
  // 前端 state 都带有明确 TypeScript 类型。
  // 读代码时可以把这些 state 看作页面自己的小型数据模型。
  //
  // useState<Product[]>([]) 的意思是：
  // - 初始值是空数组
  // - 以后 setProducts 只能放 Product[]，不能误放字符串或别的对象
  const [products, setProducts] = useState<Product[]>([])
  const [cart, setCart] = useState<Product[]>([])

  // session 的初始值来自 emptySession。
  // 登录成功后，后端返回 SessionInfo，页面再用 setSession 更新。
  const [session, setSession] = useState<SessionInfo>(emptySession)

  // overview 是后台接口返回的数据。
  // null 表示“还没有加载”，所以渲染时要用 overview?.productCount 这类可选链。
  const [overview, setOverview] = useState<AdminOverview | null>(null)

  // user/admin 是登录表单的受控状态。
  // 输入框 value 来自这里，onChange 又把新值写回这里。
  const [user, setUser] = useState({ username: 'lisa', password: '765' })
  const [admin, setAdmin] = useState({ username: 'admin', password: '123' })

  // message 用于显示最近一次 API 动作的结果。
  // loading 用于提示当前是否有请求正在执行。
  const [message, setMessage] = useState('Ready')
  const [loading, setLoading] = useState(false)

  // cartTotal 是从购物车派生出来的数据，不需要单独保存到 state。
  // 如果把它也保存到 state，就要小心 cart 改了 total 忘记同步的问题。
  const cartTotal = useMemo(() => cart.reduce((sum, item) => sum + item.price, 0), [cart])

  // 加载首页初始数据。
  //
  // Promise.all 同时发两个请求：
  // - /session：看看浏览器 cookie 是否已经登录
  // - /products：取商品列表
  //
  // 这两个请求互不依赖，所以并行比串行更自然。
  async function loadInitialData() {
    await runAction(async () => {
      const [sessionResult, productResult] = await Promise.all([
        api<SessionInfo>('/session'),
        api<Product[]>('/products')
      ])
      setSession(sessionResult.data)
      setProducts(productResult.data)
      setMessage(productResult.message)
    })
  }

  // 首次进入页面时加载 session 和商品。
  // 空依赖数组表示这个 effect 只在组件挂载后运行一次。
  //
  // void loadInitialData() 的作用是告诉 TypeScript/ESLint：
  // 这里有意启动一个异步任务，但不把 Promise 返回给 useEffect。
  useEffect(() => {
    void loadInitialData()
  }, [])

  // 普通用户登录表单提交。
  //
  // FormEvent<HTMLFormElement> 给 event 一个准确类型，
  // 所以 TypeScript 知道 event.preventDefault() 是合法方法。
  async function submitUserLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await runAction(async () => {
      const result = await api<SessionInfo>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(user)
      })
      setSession(result.data)
      setMessage(result.message)

      // 登录成功后立刻加载购物车。
      // 这时浏览器已经收到后端 Set-Cookie，下一次请求会自动带上 cookie。
      await loadCart()
    })
  }

  // 管理员登录流程。
  // 它和普通用户登录的区别主要在接口路径和后端角色校验。
  async function submitAdminLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await runAction(async () => {
      const result = await api<SessionInfo>('/admin/login', {
        method: 'POST',
        body: JSON.stringify(admin)
      })
      setSession(result.data)
      setMessage(result.message)

      // 管理员登录成功后加载后台统计。
      await loadOverview()
    })
  }

  // 加载当前普通用户购物车。
  // 如果用户没登录，后端会返回 401，runAction 会把错误 message 显示到页面顶部。
  async function loadCart() {
    const result = await api<Product[]>('/cart')
    setCart(result.data)
  }

  // 加载管理员概览。
  // 返回值是 AdminOverview，前端可以直接安全访问 productCount/categoryCount 等字段。
  async function loadOverview() {
    const result = await api<AdminOverview>('/admin/overview')
    setOverview(result.data)
  }

  // 加入购物车。
  // productId 明确是 number，避免把商品名等其他值误传给接口。
  async function addToCart(productId: number) {
    await runAction(async () => {
      const result = await api<Product[]>(`/cart/items/${productId}`, { method: 'POST' })
      setCart(result.data)
      setMessage(result.message)
    })
  }

  // 从购物车移除商品。
  // 删除后后端直接返回最新购物车列表，前端用 setCart 覆盖旧 state。
  async function removeFromCart(productId: number) {
    await runAction(async () => {
      const result = await api<Product[]>(`/cart/items/${productId}`, { method: 'DELETE' })
      setCart(result.data)
      setMessage(result.message)
    })
  }

  // 页面动作都通过 runAction 包一层，统一处理 loading 和错误提示。
  //
  // action 的类型是 () => Promise<void>：
  // - 没有参数
  // - 返回 Promise
  // - 不关心返回值，真正的数据更新在 action 内部 setState
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
    // JSX 看起来像 HTML，但本质是 TypeScript/JavaScript 表达式。
    // 花括号 {} 内可以写变量、三元表达式、函数调用和数组 map。
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Pure TypeScript Full Stack</p>
          <h1>JtProject TypeScript</h1>
        </div>
        <div className="status" aria-live="polite">
          <span className={loading ? 'status-dot busy' : 'status-dot'} />
          {message}
        </div>
      </header>

      <section className="summary-grid">
        <div className="panel">
          <h2>Session</h2>
          <dl className="summary-list">
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
            {/* 受控输入框：value 由 state 决定，onChange 负责把用户输入同步回 state。 */}
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
          <button type="submit">
            <LogIn size={18} />
            Login User
          </button>
        </form>

        <form className="panel form-panel" onSubmit={submitAdminLogin}>
          <h2>Admin Login</h2>
          <label>
            Username
            {/* ...admin 会复制旧对象，避免更新 username 时把 password 丢掉。 */}
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
          <button type="submit">
            <ShieldCheck size={18} />
            Login Admin
          </button>
        </form>
      </section>

      <section className="workspace">
        <div>
          <div className="section-heading">
            <h2>Products</h2>
            <button type="button" className="secondary" onClick={() => void loadInitialData()}>
              <RefreshCw size={17} />
              Refresh
            </button>
          </div>
          <div className="product-grid">
            {/* 数组渲染：Product[] 通过 map 变成一组 article。key 用稳定 id 帮助 React 对比列表变化。 */}
            {products.map((product) => (
              <article className="product-card" key={product.id}>
                <img src={product.image} alt="" />
                <div>
                  <p className="category">{product.categoryName}</p>
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                </div>
                <div className="product-meta">
                  <strong>${product.price.toFixed(2)}</strong>
                  <span>{product.quantity} in stock</span>
                </div>
                <button type="button" onClick={() => void addToCart(product.id)}>
                  <PackagePlus size={18} />
                  Add
                </button>
              </article>
            ))}
          </div>
        </div>

        <aside className="side-stack">
          <section className="panel">
            <div className="section-heading compact">
              <h2>Cart</h2>
              <button type="button" className="secondary icon-only" aria-label="Load cart" onClick={() => void runAction(loadCart)}>
                <ShoppingCart size={18} />
              </button>
            </div>
            <ul className="cart-list">
              {/* 购物车列表同样来自 Product[]。如果没有商品，渲染一个空状态提示。 */}
              {cart.map((item) => (
                <li key={`${item.id}-${item.name}`}>
                  <span>{item.name}</span>
                  <button
                    type="button"
                    className="danger icon-only"
                    aria-label={`Remove ${item.name}`}
                    onClick={() => void removeFromCart(item.id)}
                  >
                    <Trash2 size={16} />
                  </button>
                </li>
              ))}
              {cart.length === 0 && <li className="muted">Cart is empty</li>}
            </ul>
            <strong>Total: ${cartTotal.toFixed(2)}</strong>
          </section>

          <section className="panel">
            <div className="section-heading compact">
              <h2>Admin</h2>
              <button type="button" className="secondary" onClick={() => void runAction(loadOverview)}>
                <RefreshCw size={17} />
                Load
              </button>
            </div>
            <dl className="stats">
              <div>
                <dt>Products</dt>
                {/* 可选链 ?. 处理 overview 仍为 null 的阶段；?? '-' 给出兜底显示。 */}
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
