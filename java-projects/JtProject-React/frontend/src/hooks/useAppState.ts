import { useEffect, useState } from 'react'
import type { Category, Overview, Product, Session, User } from '../types'
import { emptySession } from '../types'
import {
  emptyCategoryForm,
  emptyProductForm,
  loadAdminData,
  loadBootstrapData,
  loadCart,
  type AdminLoginForm,
  type CategoryForm,
  type ProductForm,
  type ProfileForm,
  type RegisterForm,
  type UserLoginForm
} from '../services/appService'

export function useAppState() {
  // 这里集中管理跨页面共享状态，避免每个页面重复拉取和拼装数据。
  // 全局提示信息（用户操作后的短提示），初始为 Loading...；由各操作通过 setMessage 更新
  const [message, setMessage] = useState('Loading...')

  // 会话信息（来自后端 /api/session），结构见 types.ts 的 Session 定义
  // 初始为 emptySession（未认证状态）；会在 bootstrap 中由后端数据覆盖
  // 何时更新：登录/登出/注册后由 AppShell 调用 setSession 更新
  const [session, setSession] = useState<Session>(emptySession)

  // 商品列表（产品数组），用于商品页与后台管理的渲染
  // 初始为空数组，bootstrap 会从 /api/products 加载并 setProducts 覆盖
  const [products, setProducts] = useState<Product[]>([])

  // 分类列表（Category[]），用于下拉选择与展示
  // 初始为空数组，bootstrap 会从 /api/categories 加载
  const [categories, setCategories] = useState<Category[]>([])

  // 当前登录用户的购物车（以 Product[] 表示购物车内的商品条目）
  // 初始为空：仅在用户 authenticated 时通过 loadCart 填充
  // 何时更新：加入/移除商品时由 addToCart/removeFromCart 的返回值更新
  const [cart, setCart] = useState<Product[]>([])

  // 后台客户列表，仅在 adminLoggedIn 为 true 时才会加载（refreshAdmin）
  const [customers, setCustomers] = useState<User[]>([])

  // 管理后台概览（counts、adminUsername 等），null 表示未加载
  const [overview, setOverview] = useState<Overview | null>(null)

  // 登录/表单相关的受控状态：下面各项用于表单绑定与提交
  // userLogin: 登录表单的当前值（预填示例用于调试），通过 setUserLogin 更新
  const [userLogin, setUserLogin] = useState<UserLoginForm>({ username: 'lisa', password: '765' })
  // registerForm: 注册表单的当前值，提交后由 registerUserRequest 使用并清空
  const [registerForm, setRegisterForm] = useState<RegisterForm>({ username: '', email: '', password: '', address: '' })
  // adminLogin: 管理员登录表单的当前值
  const [adminLogin, setAdminLogin] = useState<AdminLoginForm>({ username: 'admin', password: '123' })

  // 后台编辑表单状态（分类、商品、管理员资料）——用于在管理视图里做受控编辑
  const [categoryForm, setCategoryForm] = useState<CategoryForm>(emptyCategoryForm())
  const [productForm, setProductForm] = useState<ProductForm>(emptyProductForm([]))
  const [profileForm, setProfileForm] = useState<ProfileForm>({ username: '', email: '', password: '', address: '' })

  useEffect(() => {
    // 首次进入应用时先拉取会话、商品和分类，再决定是否补充购物车或后台数据。
    // 详细流程：
    // 1. loadBootstrapData() 同时请求 /api/session, /api/products, /api/categories
    // 2. 把返回的 session/products/categories 写入对应状态
    // 3. 根据 session.authenticated 决定是否调用 loadCart()
    // 4. 根据 session.adminLoggedIn 决定是否调用 refreshAdmin()（加载后台数据）
    // bootstrap 是应用启动时的单次初始化逻辑，不会重复触发
    void bootstrap()
  }, [])

  async function bootstrap() {
    const data = await loadBootstrapData()
    setSession(data.session)
    setProducts(data.products)
    setCategories(data.categories)
    setProductForm(emptyProductForm(data.categories))
    if (data.session.authenticated) {
      setCart(await loadCart())
    }
    if (data.session.adminLoggedIn) {
      await refreshAdmin()
    }
    setMessage('Ready')
  }

  // 用户态刷新只需要重新拉购物车。
  async function refreshCart() {
    // 从后端重新加载当前用户的购物车并写入状态
    // 用处：登录后、加入/移除购物车后、或你想手动刷新购物车时调用
    setCart(await loadCart())
  }

  // 管理员态刷新会同步更新概览、客户、商品、分类和个人资料。
  async function refreshAdmin() {
    const data = await loadAdminData()
    setOverview(data.overview)
    setCustomers(data.customers)
    setProducts(data.products)
    setCategories(data.categories)
    setProfileForm({
      username: data.profile.username,
      email: data.profile.email,
      password: data.profile.password,
      address: data.profile.address ?? ''
    })
  }

  // 返回 Hook 暴露的状态和方法：
  // - 状态值（message, session, products, ...）
  // - set 函数（setMessage, setSession, setProducts, ...）用于在组件中更新状态
  // - refreshCart / refreshAdmin 为方便的异步刷新函数（会调用后端并更新相关状态）
  return {
    message,
    setMessage,
    session,
    setSession,
    products,
    setProducts,
    categories,
    setCategories,
    cart,
    setCart,
    customers,
    setCustomers,
    overview,
    setOverview,
    userLogin,
    setUserLogin,
    registerForm,
    setRegisterForm,
    adminLogin,
    setAdminLogin,
    categoryForm,
    setCategoryForm,
    productForm,
    setProductForm,
    profileForm,
    setProfileForm,
    refreshCart,
    refreshAdmin
  }
}
