import './styles.css'
import {
  addToCartRequest,
  loadBootstrapData,
  loadCart,
  loginAdminRequest,
  loginUserRequest,
  logoutAdminRequest,
  logoutUserRequest,
  registerUserRequest,
  removeFromCartRequest
} from './services/appService'
import type { Category, Product, Session } from './types'
import { emptySession } from './types'

type View = 'products' | 'cart' | 'user' | 'admin'

type State = {
  view: View
  loading: boolean
  message: string
  error: string
  session: Session
  products: Product[]
  categories: Category[]
  cart: Product[]
}

const state: State = {
  view: 'products',
  loading: true,
  message: '',
  error: '',
  session: emptySession,
  products: [],
  categories: [],
  cart: []
}

const root = document.querySelector<HTMLDivElement>('#root')

if (!root) {
  throw new Error('Root element was not found.')
}

const appRoot = root

function money(value: number) {
  return `$${Number(value).toFixed(2)}`
}

function escapeHtml(value: unknown) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function categoryName(product: Product) {
  return product.categoryName || state.categories.find((category) => category.id === product.categoryId)?.name || '未分类'
}

function setMessage(message: string, error = '') {
  state.message = message
  state.error = error
}

async function run(action: () => Promise<void>) {
  state.loading = true
  render()
  try {
    await action()
  } catch (error) {
    setMessage('', error instanceof Error ? error.message : '操作失败')
  } finally {
    state.loading = false
    render()
  }
}

async function bootstrap() {
  await run(async () => {
    const data = await loadBootstrapData()
    state.session = data.session
    state.products = data.products
    state.categories = data.categories
    if (state.session.authenticated) {
      state.cart = await loadCart()
    }
    setMessage('数据已加载。')
  })
}

function renderTabs() {
  const tabs: Array<[View, string]> = [
    ['products', '商品'],
    ['cart', `购物车 ${state.cart.length}`],
    ['user', state.session.authenticated ? state.session.username : '用户登录'],
    ['admin', state.session.adminLoggedIn ? `管理 ${state.session.adminUsername}` : '管理员']
  ]
  return tabs
    .map(([view, label]) => `<button class="${state.view === view ? 'active' : ''}" data-view="${view}">${escapeHtml(label)}</button>`)
    .join('')
}

function renderProducts() {
  return `
    <section class="panel stack">
      <div class="toolbar">
        <div>
          <h2>商品列表</h2>
          <p class="muted">原生 TypeScript 直接调用 Spring Boot REST API，再用 DOM 渲染列表。</p>
        </div>
        <button class="secondary" data-action="reload">刷新</button>
      </div>
      <div class="grid">
        ${state.products
          .map(
            (product) => `
              <article class="product">
                <img src="${escapeHtml(product.image || 'https://placehold.co/640x480?text=Product')}" alt="${escapeHtml(product.name)}" />
                <div>
                  <h3>${escapeHtml(product.name)}</h3>
                  <p class="muted">${escapeHtml(categoryName(product))} · 库存 ${escapeHtml(product.quantity)}</p>
                  <p>${escapeHtml(product.description)}</p>
                  <p class="price">${money(product.price)}</p>
                </div>
                <button data-action="add-cart" data-id="${product.id}" ${state.session.authenticated ? '' : 'disabled'}>加入购物车</button>
              </article>
            `
          )
          .join('')}
      </div>
    </section>
  `
}

function renderCart() {
  if (!state.session.authenticated) {
    return `<section class="panel"><h2>购物车</h2><p class="muted">请先用普通用户登录。</p></section>`
  }
  return `
    <section class="panel stack">
      <div class="toolbar">
        <h2>购物车</h2>
        <button class="secondary" data-action="load-cart">刷新购物车</button>
      </div>
      ${
        state.cart.length
          ? state.cart
              .map(
                (product) => `
                  <div class="row">
                    <div>
                      <strong>${escapeHtml(product.name)}</strong>
                      <p class="muted">${money(product.price)} · ${escapeHtml(categoryName(product))}</p>
                    </div>
                    <button class="danger" data-action="remove-cart" data-id="${product.id}">移除</button>
                  </div>
                `
              )
              .join('')
          : '<p class="muted">购物车为空。</p>'
      }
    </section>
  `
}

function renderUser() {
  if (state.session.authenticated) {
    return `
      <section class="panel stack">
        <h2>普通用户</h2>
        <p>当前登录：<strong>${escapeHtml(state.session.username)}</strong></p>
        <button data-action="logout-user">退出普通用户</button>
      </section>
    `
  }
  return `
    <section class="hero">
      <form class="panel stack" data-form="user-login">
        <h2>普通用户登录</h2>
        <input name="username" value="lisa" placeholder="用户名" autocomplete="username" />
        <input name="password" value="765" type="password" placeholder="密码" autocomplete="current-password" />
        <button>登录</button>
      </form>
      <form class="panel stack" data-form="user-register">
        <h2>注册用户</h2>
        <div class="formGrid">
          <input name="username" placeholder="用户名" />
          <input name="email" placeholder="邮箱" />
          <input name="password" type="password" placeholder="密码" />
          <input name="address" placeholder="地址" />
        </div>
        <button>注册并登录</button>
      </form>
    </section>
  `
}

function renderAdmin() {
  if (!state.session.adminLoggedIn) {
    return `
      <form class="panel stack" data-form="admin-login">
        <h2>管理员登录</h2>
        <input name="username" value="admin" placeholder="管理员用户名" autocomplete="username" />
        <input name="password" value="123" type="password" placeholder="密码" autocomplete="current-password" />
        <button>登录管理员</button>
      </form>
    `
  }
  return `
    <section class="panel stack">
      <div class="toolbar">
        <div>
          <h2>管理入口</h2>
          <p class="muted">这个版本只保留轻量管理入口，重点观察 API 调用、状态更新和 DOM 重绘。</p>
        </div>
        <button data-action="logout-admin">退出管理员</button>
      </div>
      <div class="summary">
        <span class="notice">管理员：${escapeHtml(state.session.adminUsername)}</span>
        <span class="notice">商品：${state.products.length}</span>
        <span class="notice">分类：${state.categories.length}</span>
      </div>
    </section>
  `
}

function renderCurrentView() {
  if (state.view === 'cart') return renderCart()
  if (state.view === 'user') return renderUser()
  if (state.view === 'admin') return renderAdmin()
  return renderProducts()
}

function render() {
  appRoot.innerHTML = `
    <main class="page">
      <header class="hero">
        <section class="panel">
          <h1>Spring Boot + 纯 TypeScript</h1>
          <p class="muted">后端继续使用 Spring Boot REST API，前端只使用 Vite、TypeScript、Fetch 和 DOM API。</p>
        </section>
        <section class="panel stack">
          <strong>数据流定位</strong>
          <span class="muted">ApiController.java -> api.ts -> appService.ts -> main.ts -> DOM</span>
        </section>
      </header>
      <nav class="tabs">${renderTabs()}</nav>
      ${state.loading ? '<p class="notice">加载中...</p>' : ''}
      ${state.message ? `<p class="notice">${escapeHtml(state.message)}</p>` : ''}
      ${state.error ? `<p class="notice error">${escapeHtml(state.error)}</p>` : ''}
      ${renderCurrentView()}
    </main>
  `
}

function formData(form: HTMLFormElement) {
  return Object.fromEntries(new FormData(form).entries()) as Record<string, string>
}

root.addEventListener('click', (event) => {
  const target = event.target as HTMLElement
  const viewButton = target.closest<HTMLButtonElement>('[data-view]')
  const actionButton = target.closest<HTMLButtonElement>('[data-action]')

  if (viewButton) {
    state.view = viewButton.dataset.view as View
    setMessage('')
    render()
    return
  }

  if (!actionButton) return
  const id = Number(actionButton.dataset.id)
  const action = actionButton.dataset.action

  if (action === 'reload') void bootstrap()
  if (action === 'load-cart') void run(async () => { state.cart = await loadCart(); setMessage('购物车已刷新。') })
  if (action === 'add-cart') void run(async () => { state.cart = await addToCartRequest(id); setMessage('已加入购物车。') })
  if (action === 'remove-cart') void run(async () => { state.cart = await removeFromCartRequest(id); setMessage('已从购物车移除。') })
  if (action === 'logout-user') void run(async () => { state.session = await logoutUserRequest(); state.cart = []; setMessage('普通用户已退出。') })
  if (action === 'logout-admin') void run(async () => { state.session = await logoutAdminRequest(); setMessage('管理员已退出。') })
})

root.addEventListener('submit', (event) => {
  event.preventDefault()
  const form = event.target as HTMLFormElement
  const data = formData(form)

  if (form.dataset.form === 'user-login') {
    void run(async () => {
      state.session = await loginUserRequest({ username: data.username, password: data.password })
      state.cart = await loadCart()
      state.view = 'products'
      setMessage('普通用户登录成功。')
    })
  }

  if (form.dataset.form === 'user-register') {
    void run(async () => {
      state.session = await registerUserRequest({
        username: data.username,
        email: data.email,
        password: data.password,
        address: data.address
      })
      state.cart = []
      state.view = 'products'
      setMessage('注册成功。')
    })
  }

  if (form.dataset.form === 'admin-login') {
    void run(async () => {
      state.session = await loginAdminRequest({ username: data.username, password: data.password })
      setMessage('管理员登录成功。')
    })
  }
})

render()
void bootstrap()
