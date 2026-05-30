import cookieParser from 'cookie-parser'
import cors from 'cors'
import express, { type Request, type Response } from 'express'
import type {
  AdminOverview,
  ApiResult,
  LoginBody,
  Product,
  ProductInput,
  RegisterBody,
  SessionInfo,
  User
} from '../../../packages/shared/src/index'
import { Store } from './data/store'

const app = express()
const store = new Store()
const port = Number(process.env.API_PORT ?? 8090)

// 这里用两个 cookie 模拟两类登录状态：
// - jt_ts_session：普通用户登录
// - jt_ts_admin：管理员登录
//
// 原始 Spring Boot 版使用 HttpSession；Express 版为了学习简单，用 cookie 保存用户名。
const sessionCookieName = 'jt_ts_session'
const adminCookieName = 'jt_ts_admin'

// Express 中间件相当于后端请求进入 Controller 前的统一处理。
// JSON parser 负责把 request body 转成对象，cors/cookieParser 负责跨端口 cookie 学习场景。
app.use(express.json())
app.use(cookieParser())
app.use(
  cors({
    origin: ['http://localhost:5175', 'http://127.0.0.1:5175'],
    credentials: true
  })
)

app.get('/api/health', (_request, response) => {
  // 健康检查接口用于确认后端服务已经启动。
  response.json(ok('JtProject TypeScript API is running', 'ok'))
})

app.get('/api/session', (request, response) => {
  // 前端刷新页面后会调用这个接口，从 cookie 恢复当前登录状态。
  response.json(ok('Session loaded', sessionData(request)))
})

app.post('/api/auth/login', (request: Request<Record<string, string>, unknown, LoginBody>, response) => {
  // Request<Params, ResBody, ReqBody> 的第三个泛型 LoginBody 表示 request.body 的类型。
  // 因此 request.body.username / password 会有类型提示。
  const user = store.checkLogin(clean(request.body.username), clean(request.body.password))
  if (!user || user.role !== 'ROLE_NORMAL') {
    return send(response, 401, fail('Invalid user credentials'))
  }

  // 登录成功后写 cookie。前端 fetch 使用 credentials: 'include' 后，后续请求会自动带上它。
  response.cookie(sessionCookieName, user.username, cookieOptions())
  return response.json(ok('User login successful', sessionDataFor(user, request)))
})

app.post('/api/auth/register', (request: Request<Record<string, string>, unknown, RegisterBody>, response) => {
  // 注册接口演示如何接收一个更复杂的 JSON body。
  // 当前前端没有注册页面，你可以后续照着登录表单扩展。
  const username = clean(request.body.username)
  const email = clean(request.body.email)
  const password = clean(request.body.password)
  const address = clean(request.body.address)
  if (!username || !email || !password) {
    return send(response, 400, fail('Username, email and password are required'))
  }
  if (store.findUserByUsername(username)) {
    return send(response, 409, fail('Username already exists'))
  }
  const user = store.registerUser({ username, email, password, address })
  response.cookie(sessionCookieName, user.username, cookieOptions())
  return send(response, 201, ok('Registration successful', sessionDataFor(user, request)))
})

app.post('/api/auth/logout', (_request, response) => {
  // 清除 cookie 后，浏览器后续请求就不会再被识别为普通用户。
  response.clearCookie(sessionCookieName)
  response.json(ok('User logout successful', emptySession()))
})

app.get('/api/categories', (_request, response) => {
  // 分类接口保留给后续扩展商品编辑页使用。
  response.json(ok('Categories loaded', store.getCategories()))
})

app.get('/api/products', (_request, response) => {
  // 商品列表是首页主要数据源。
  response.json(ok('Products loaded', store.getProducts()))
})

app.get('/api/cart', (request, response) => {
  // 购物车接口需要普通用户登录。
  // requireNormalUser 失败时已经写入 401 响应，所以这里直接 return。
  const user = requireNormalUser(request, response)
  if (!user) {
    return
  }
  response.json(ok('Cart loaded', store.getCartProducts(user.id)))
})

app.post('/api/cart/items/:productId', (request, response) => {
  // :productId 是 Express 路由参数。
  // request.params.productId 原本是 string，所以需要 Number(...) 转换。
  const user = requireNormalUser(request, response)
  if (!user) {
    return
  }
  const productId = Number(request.params.productId)
  response.json(ok('Product added to cart', store.addCartItem(user.id, productId)))
})

app.delete('/api/cart/items/:productId', (request, response) => {
  // DELETE 和 POST 使用同一路径，不同 HTTP method 表达不同动作。
  const user = requireNormalUser(request, response)
  if (!user) {
    return
  }
  const productId = Number(request.params.productId)
  response.json(ok('Product removed from cart', store.removeCartItem(user.id, productId)))
})

app.post('/api/admin/login', (request: Request<Record<string, string>, unknown, LoginBody>, response) => {
  // 管理员登录和普通登录共用 LoginBody，但角色必须是 ROLE_ADMIN。
  const user = store.checkLogin(clean(request.body.username), clean(request.body.password))
  if (!user || user.role !== 'ROLE_ADMIN') {
    return send(response, 401, fail('Invalid admin credentials'))
  }
  response.cookie(adminCookieName, user.username, cookieOptions())
  return response.json(ok('Admin login successful', sessionDataFor(null, request, user.username)))
})

app.get('/api/admin/overview', (request, response) => {
  // 管理员概览是一个典型的聚合接口：它不是直接返回一张表，而是汇总多个数组长度。
  const adminUsername = requireAdmin(request, response)
  if (!adminUsername) {
    return
  }
  const data: AdminOverview = {
    productCount: store.getProducts().length,
    categoryCount: store.getCategories().length,
    customerCount: store.getUsers().length,
    adminUsername
  }
  response.json(ok('Admin overview loaded', data))
})

app.get('/api/admin/products', (request, response) => {
  // 后台商品列表和前台商品列表可以复用同一份 Store 数据。
  if (!requireAdmin(request, response)) {
    return
  }
  response.json(ok('Products loaded', store.getProducts()))
})

app.post('/api/admin/products', (request: Request<Record<string, string>, unknown, ProductInput>, response) => {
  // ProductInput 是前后端共享类型，确保前端提交和后端接收的字段一致。
  if (!requireAdmin(request, response)) {
    return
  }
  response.status(201).json(ok('Product created', store.createProduct(request.body)))
})

app.put('/api/admin/products/:id', (request: Request<{ id: string }, unknown, ProductInput>, response) => {
  // PUT 用于更新指定 id 的商品。
  // Request<{ id: string }, unknown, ProductInput> 同时标注了 params.id 和 body 类型。
  if (!requireAdmin(request, response)) {
    return
  }
  const product = store.updateProduct(Number(request.params.id), request.body)
  if (!product) {
    return send(response, 404, fail('Product not found'))
  }
  return response.json(ok('Product updated', product))
})

app.delete('/api/admin/products/:id', (request, response) => {
  // 删除商品后返回最新商品列表，前端可以直接刷新 state。
  if (!requireAdmin(request, response)) {
    return
  }
  response.json(ok('Product deleted', store.deleteProduct(Number(request.params.id))))
})

app.listen(port, () => {
  // app.listen 是 Express 后端真正开始监听端口的地方。
  console.log(`JtProject TypeScript API: http://localhost:${port}/api`)
})

// ok/fail/send 这三个小函数统一 API 返回格式。
// 好处是所有接口都能返回 { success, message, data }，前端 api<T>() 就可以统一处理。
function ok<T>(message: string, data: T): ApiResult<T> {
  return { success: true, message, data }
}

function fail(message: string): ApiResult<null> {
  return { success: false, message, data: null }
}

function send<T>(response: Response, status: number, body: ApiResult<T>) {
  return response.status(status).json(body)
}

// clean 把未知输入安全地转成 trim 后的字符串。
// 因为 HTTP 请求来自外部，不能假设 body/cookie 一定是字符串。
function clean(value: unknown) {
  return typeof value === 'string' ? value.trim() : ''
}

// 从普通用户 cookie 中恢复 User。
// 注意这里没有访问数据库，而是查 Store 的内存 users 数组。
function currentUser(request: Request) {
  const username = clean(request.cookies[sessionCookieName])
  return username ? store.findUserByUsername(username) : undefined
}

// 从管理员 cookie 中读取管理员用户名。
function currentAdminUsername(request: Request) {
  return clean(request.cookies[adminCookieName])
}

// 权限守卫：要求普通用户登录。
// 返回 User 表示通过；返回 null 表示已经给客户端写了 401 响应。
function requireNormalUser(request: Request, response: Response) {
  const user = currentUser(request)
  if (!user || user.role !== 'ROLE_NORMAL') {
    send(response, 401, fail('Please login as a normal user first'))
    return null
  }
  return user
}

// 权限守卫：要求管理员登录。
// 这里返回 username 而不是 User，是因为当前后台概览只需要显示管理员名。
function requireAdmin(request: Request, response: Response) {
  const username = currentAdminUsername(request)
  const user = username ? store.findUserByUsername(username) : undefined
  if (!user || user.role !== 'ROLE_ADMIN') {
    send(response, 401, fail('Please login as admin first'))
    return null
  }
  return username
}

// 根据当前 request 里的 cookie 组装 SessionInfo。
function sessionData(request: Request): SessionInfo {
  return sessionDataFor(currentUser(request) ?? null, request)
}

// sessionDataFor 是更底层的组装函数。
// 登录成功时已经拿到了 user，可以直接传进来，避免再从 cookie 查一遍。
function sessionDataFor(user: User | null, request: Request, adminUsername = currentAdminUsername(request)): SessionInfo {
  return {
    authenticated: Boolean(user),
    username: user?.username ?? '',
    role: user?.role ?? '',
    adminLoggedIn: Boolean(adminUsername),
    adminUsername
  }
}

// 空会话对象用于登出和初始化兜底。
function emptySession(): SessionInfo {
  return {
    authenticated: false,
    username: '',
    role: '',
    adminLoggedIn: false,
    adminUsername: ''
  }
}

// cookieOptions 统一 cookie 策略。
// httpOnly 表示前端 JS 不能直接读取 cookie，减少 XSS 风险。
// sameSite: 'lax' 适合本地学习环境里的普通导航和同站请求。
function cookieOptions() {
  return {
    httpOnly: true,
    sameSite: 'lax' as const,
    maxAge: 7 * 24 * 60 * 60 * 1000
  }
}
