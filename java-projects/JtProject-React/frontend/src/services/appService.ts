import { api } from '../api'
import type { Category, Overview, Product, Session, User } from '../types'

export type UserLoginForm = { username: string; password: string }
export type RegisterForm = { username: string; email: string; password: string; address: string }
export type AdminLoginForm = { username: string; password: string }
export type CategoryForm = { id: number; name: string }
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
export type ProfileForm = { username: string; email: string; password: string; address: string }

export async function loadBootstrapData() {
  const [sessionRes, productRes, categoryRes] = await Promise.all([
    api<Session>('/session'),
    api<Product[]>('/products'),
    api<Category[]>('/categories')
  ])
  return {
    session: sessionRes.data,
    products: productRes.data,
    categories: categoryRes.data
  }
}

export async function loadCart() {
  const result = await api<Product[]>('/cart')
  return result.data
}

export async function loadAdminData() {
  const [overviewRes, customersRes, profileRes, productRes, categoryRes] = await Promise.all([
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
    products: productRes.data,
    categories: categoryRes.data
  }
}

export async function loginUserRequest(form: UserLoginForm) {
  return (await api<Session>('/auth/login', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function registerUserRequest(form: RegisterForm) {
  return (await api<Session>('/auth/register', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function logoutUserRequest() {
  return (await api<Session>('/auth/logout', { method: 'POST', body: JSON.stringify({}) })).data
}

export async function addToCartRequest(productId: number) {
  return (await api<Product[]>(`/cart/items/${productId}`, { method: 'POST', body: JSON.stringify({}) })).data
}

export async function removeFromCartRequest(productId: number) {
  return (await api<Product[]>(`/cart/items/${productId}`, { method: 'DELETE' })).data
}

export async function loginAdminRequest(form: AdminLoginForm) {
  return (await api<Session>('/admin/login', { method: 'POST', body: JSON.stringify(form) })).data
}

export async function logoutAdminRequest() {
  return (await api<Session>('/admin/logout', { method: 'POST', body: JSON.stringify({}) })).data
}

export async function saveCategoryRequest(form: CategoryForm) {
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

export async function saveProfileRequest(form: ProfileForm) {
  return (await api<User>('/admin/profile', { method: 'PUT', body: JSON.stringify(form) })).data
}

export function emptyCategoryForm(): CategoryForm {
  return { id: 0, name: '' }
}

export function emptyProductForm(categories: Category[]): ProductForm {
  return {
    id: 0,
    name: '',
    categoryId: categories[0]?.id ?? 1,
    price: 1,
    weight: 1,
    quantity: 1,
    description: '',
    image: ''
  }
}
