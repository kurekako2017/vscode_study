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
  const [message, setMessage] = useState('Loading...')
  const [session, setSession] = useState<Session>(emptySession)
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [cart, setCart] = useState<Product[]>([])
  const [customers, setCustomers] = useState<User[]>([])
  const [overview, setOverview] = useState<Overview | null>(null)
  const [userLogin, setUserLogin] = useState<UserLoginForm>({ username: 'lisa', password: '765' })
  const [registerForm, setRegisterForm] = useState<RegisterForm>({ username: '', email: '', password: '', address: '' })
  const [adminLogin, setAdminLogin] = useState<AdminLoginForm>({ username: 'admin', password: '123' })
  const [categoryForm, setCategoryForm] = useState<CategoryForm>(emptyCategoryForm())
  const [productForm, setProductForm] = useState<ProductForm>(emptyProductForm([]))
  const [profileForm, setProfileForm] = useState<ProfileForm>({ username: '', email: '', password: '', address: '' })

  useEffect(() => {
    // 首次进入应用时先拉取会话、商品和分类，再决定是否补充购物车或后台数据。
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
