import { reactive } from 'vue'
import type { Category, Overview, Product, Session, User } from '../types'
import {
  addToCartRequest,
  deleteCategoryRequest,
  deleteProductRequest,
  emptyProductForm,
  loadAdminData,
  loadBootstrapData,
  loadCart,
  loginAdminRequest,
  loginUserRequest,
  logoutAdminRequest,
  logoutUserRequest,
  registerUserRequest,
  removeFromCartRequest,
  saveCategoryRequest,
  saveProductRequest,
  saveProfileRequest,
  type ProductForm
} from '../services/appService'

// 这里用一个响应式对象集中保存页面共享状态，方便 views 和 components 直接读取。
export const store = reactive({
  message: 'Loading...',
  session: {
    authenticated: false,
    username: '',
    role: '',
    adminLoggedIn: false,
    adminUsername: ''
  } as Session,
  products: [] as Product[],
  categories: [] as Category[],
  cart: [] as Product[],
  customers: [] as User[],
  overview: null as Overview | null,
  userLogin: { username: 'lisa', password: '765' },
  registerForm: { username: '', email: '', password: '', address: '' },
  adminLogin: { username: 'admin', password: '123' },
  categoryForm: { id: 0, name: '' },
  productForm: emptyProductForm(1) as ProductForm,
  profileForm: { username: '', email: '', password: '', address: '' }
})

export function useAppStore() {
  // 启动阶段统一拉取基础数据，避免每个页面重复请求。
  async function bootstrap() {
    const data = await loadBootstrapData()
    store.session = data.session
    store.products = data.products
    store.categories = data.categories
    store.productForm = emptyProductForm(data.categories[0]?.id ?? 1)
    if (store.session.authenticated) await refreshCart()
    if (store.session.adminLoggedIn) await refreshAdmin()
    store.message = 'Ready'
  }

  // 用户购物车和后台数据按需加载，减少无关页面的请求量。
  async function refreshCart() {
    store.cart = await loadCart()
  }

  async function refreshAdmin() {
    const data = await loadAdminData()
    store.overview = data.overview
    store.customers = data.customers
    store.products = data.products
    store.categories = data.categories
    store.profileForm = {
      username: data.profile.username,
      email: data.profile.email,
      password: data.profile.password,
      address: data.profile.address ?? ''
    }
  }

  // 用户登录与注册成功后都要同步购物车和会话状态。
  async function loginUser() {
    store.session = await loginUserRequest(store.userLogin)
    await refreshCart()
    store.message = 'User login successful.'
  }

  async function registerUser() {
    store.session = await registerUserRequest(store.registerForm)
    await refreshCart()
    store.registerForm = { username: '', email: '', password: '', address: '' }
    store.message = 'Registration successful.'
  }

  // 用户退出时只清理与普通用户相关的状态。
  async function logoutUser() {
    store.session = { ...store.session, ...(await logoutUserRequest()) }
    store.cart = []
    store.message = 'User logout successful.'
  }

  // 购物车操作直接复用后端返回的最新列表。
  async function addToCart(productId: number) {
    store.cart = await addToCartRequest(productId)
    store.message = 'Product added to cart.'
  }

  async function removeFromCart(productId: number) {
    store.cart = await removeFromCartRequest(productId)
    store.message = 'Product removed from cart.'
  }

  // 管理员登录后刷新后台概览、商品、分类和客户列表。
  async function loginAdmin() {
    store.session = { ...store.session, ...(await loginAdminRequest(store.adminLogin)) }
    await refreshAdmin()
    store.message = 'Admin login successful.'
  }

  // 管理员退出时清空后台态，避免误以为仍在登录中。
  async function logoutAdmin() {
    store.session = { ...store.session, ...(await logoutAdminRequest()) }
    store.overview = null
    store.customers = []
    store.message = 'Admin logout successful.'
  }

  // 分类、商品和资料编辑都走同一套“提交 -> 保存 -> 刷新后台数据”的套路。
  async function saveCategory() {
    store.categories = await saveCategoryRequest(store.categoryForm)
    store.categoryForm = { id: 0, name: '' }
    await refreshAdmin()
    store.message = 'Category saved.'
  }

  async function deleteCategory(id: number) {
    store.categories = await deleteCategoryRequest(id)
    await refreshAdmin()
    store.message = 'Category deleted.'
  }

  async function saveProduct() {
    store.products = await saveProductRequest(store.productForm)
    store.productForm = emptyProductForm(store.categories[0]?.id ?? 1)
    await refreshAdmin()
    store.message = 'Product saved.'
  }

  async function deleteProduct(id: number) {
    store.products = await deleteProductRequest(id)
    await refreshAdmin()
    store.message = 'Product deleted.'
  }

  async function saveProfile() {
    const profile = await saveProfileRequest(store.profileForm)
    store.profileForm = {
      username: profile.username,
      email: profile.email,
      password: profile.password,
      address: profile.address ?? ''
    }
    await refreshAdmin()
    store.message = 'Profile updated.'
  }

  // 点击列表中的编辑按钮时，把实体数据回填到表单里。
  function fillCategoryForm(category: Category) {
    store.categoryForm = { ...category }
  }

  function fillProductForm(product: Product) {
    store.productForm = {
      id: product.id,
      name: product.name,
      categoryId: product.categoryId,
      price: product.price,
      weight: product.weight,
      quantity: product.quantity,
      description: product.description,
      image: product.image
    }
  }

  return {
    store,
    bootstrap,
    refreshCart,
    refreshAdmin,
    loginUser,
    registerUser,
    logoutUser,
    addToCart,
    removeFromCart,
    loginAdmin,
    logoutAdmin,
    saveCategory,
    deleteCategory,
    saveProduct,
    deleteProduct,
    saveProfile,
    fillCategoryForm,
    fillProductForm
  }
}
