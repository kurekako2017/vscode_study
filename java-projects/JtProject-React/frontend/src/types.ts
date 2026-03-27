export type Session = {
  authenticated: boolean
  username: string
  role: string
  adminLoggedIn: boolean
  adminUsername: string
}

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

export const emptySession: Session = {
  authenticated: false,
  username: '',
  role: '',
  adminLoggedIn: false,
  adminUsername: ''
}
