export type Session = {
  authenticated: boolean
  username: string
  role: string
  adminLoggedIn: boolean
  adminUsername: string
}

// 这里集中放置前端和后端共享的数据结构，避免各个组件重复定义同一套字段。
export type Product = {
  id: number
  name: string
  image: string
  categoryId: number
  categoryName: string
  quantity: number
  price: number
  weight: number
  description: string
}

export type Category = {
  id: number
  name: string
}

export type User = {
  id: number
  username: string
  email: string
  role: string
  address: string
  password: string
}

export type Overview = {
  categoryCount: number
  productCount: number
  customerCount: number
  adminUsername: string
}

export type ApiResult<T> = {
  success: boolean
  message: string
  data: T
}

// 空会话对象用于初始化页面状态，避免组件里到处写空值判断。
export const emptySession: Session = {
  authenticated: false,
  username: '',
  role: '',
  adminLoggedIn: false,
  adminUsername: ''
}
