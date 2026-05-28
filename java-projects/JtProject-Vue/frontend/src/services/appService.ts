import { api } from '../api'
import type { Category, Overview, Product, Session, User } from '../types'

// 这里统一放后端请求封装，页面和 composable 只关心“要做什么”，不关心 HTTP 细节。
export type ProductForm = {
  id: number
  name: string
  categoryId: number
  price: number
  weight: number
  quantity: number
  description: string
  image: string
}

// 启动时一次性加载会话、商品和分类，减少页面重复请求。
export async function loadBootstrapData() {
  const [sessionRes, productsRes, categoriesRes] = await Promise.all([
    api<Session>('/session'),
    api<Product[]>('/products'),
    api<Category[]>('/categories')
  ])
  return {
    session: sessionRes.data,
    products: productsRes.data,
    categories: categoriesRes.data
  }
}

// 购物车只在登录用户场景下才会用到，因此单独加载。
export async function loadCart() {
  return (await api<Product[]>('/cart')).data
}

// 管理后台需要的概览、客户、资料、商品和分类一次性并发拉取。
export async function loadAdminData() {
  const [overviewRes, customersRes, profileRes, productsRes, categoriesRes] = await Promise.all([
    api<Overview>('/admin/overview'),
    api<User[]>('/admin/customers'),
    api<User>('/admin/profile'),
    api<Product[]>('/admin/products'),
    api<Category[]>('/admin/categories')
  ])
  return {
    overview: overviewRes.data,
    customers: customersRes.data,
    profile: profileRes.data,
    products: productsRes.data,
    categories: categoriesRes.data
  }
}

// 登录、注册、登出和 CRUD 请求都保持轻量封装。
export async function loginUserRequest(form: { username: string; password: string }) {
  return (await api<Session>('/auth/login', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function registerUserRequest(form: { username: string; email: string; password: string; address: string }) {
  return (await api<Session>('/auth/register', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function logoutUserRequest() {
  return (await api<Session>('/auth/logout', { method: 'POST', body: '{}' })).data
}

export async function addToCartRequest(productId: number) {
  return (await api<Product[]>(`/cart/items/${productId}`, { method: 'POST', body: '{}' })).data
}

export async function removeFromCartRequest(productId: number) {
  return (await api<Product[]>(`/cart/items/${productId}`, { method: 'DELETE' })).data
}

export async function loginAdminRequest(form: { username: string; password: string }) {
  return (await api<Session>('/admin/login', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function logoutAdminRequest() {
  return (await api<Session>('/admin/logout', { method: 'POST', body: '{}' })).data
}

export async function saveCategoryRequest(form: { id: number; name: string }) {
  const path = form.id ? `/admin/categories/${form.id}` : '/admin/categories'
  const method = form.id ? 'PUT' : 'POST'
  return (await api<Category[]>(path, { method, body: JSON.stringify({ name: form.name }) })).data
}

export async function deleteCategoryRequest(id: number) {
  return (await api<Category[]>(`/admin/categories/${id}`, { method: 'DELETE' })).data
}

export async function saveProductRequest(form: ProductForm) {
  const path = form.id ? `/admin/products/${form.id}` : '/admin/products'
  const method = form.id ? 'PUT' : 'POST'
  return (await api<Product[]>(path, { method, body: JSON.stringify(form) })).data
}

export async function deleteProductRequest(id: number) {
  return (await api<Product[]>(`/admin/products/${id}`, { method: 'DELETE' })).data
}

export async function saveProfileRequest(form: { username: string; email: string; password: string; address: string }) {
  return (await api<User>('/admin/profile', { method: 'PUT', body: JSON.stringify(form) })).data
}

// 商品表单重置时根据当前分类选择默认分类，避免空值。
export function emptyProductForm(categoryId: number): ProductForm {
  return {
    id: 0,
    name: '',
    categoryId,
    price: 1,
    weight: 1,
    quantity: 1,
    description: '',
    image: ''
  }
}
