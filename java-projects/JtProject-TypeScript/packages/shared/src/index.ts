// shared 包只保存“前后端共同认可”的数据结构。
//
// 为什么要单独放一个 shared 包？
// 1. 后端返回什么字段，前端就按同一份类型接收，避免两边各写一套后慢慢不一致。
// 2. 修改字段时，TypeScript 会同时检查 API 和页面代码，错误更早暴露。
// 3. 这里不写业务逻辑，只写 type，让它成为干净的“接口契约层”。

// 角色使用联合类型，而不是普通 string。
// 这样 role 只能是这两个值之一，写成 ROLE_USER 之类会被 TypeScript 报错。
export type Role = 'ROLE_ADMIN' | 'ROLE_NORMAL'

// 后端所有接口都统一返回 ApiResult<T>。
//
// T 是泛型参数，表示 data 里的真实数据类型：
// - ApiResult<Product[]> 表示商品数组
// - ApiResult<SessionInfo> 表示登录状态
// - ApiResult<AdminOverview> 表示后台统计
export type ApiResult<T> = {
  success: boolean
  message: string
  data: T
}

// Category 对应原始 JtProject 的 CATEGORY 表。
// 在纯 TypeScript 版中，它既是后端内存数据结构，也是前端可直接使用的类型。
export type Category = {
  id: number
  name: string
}

// User 对应原始 JtProject 的 CUSTOMER 表。
// 注意：这里为了学习和对齐原始项目，password 仍是明文字段；真实项目应由后端加密保存。
export type User = {
  id: number
  username: string
  email: string
  password: string
  role: Role
  address: string
}

// Product 是前端真正渲染商品卡片时用到的形状。
// 它不是完全照搬数据库字段，而是把 categoryName 也带上，前端就不用再查分类表。
export type Product = {
  id: number
  name: string
  image: string
  price: number
  weight: number
  quantity: number
  description: string
  categoryId: number
  categoryName: string
}

// SessionInfo 描述“当前浏览器会话”的状态。
// 普通用户登录和管理员登录在本学习项目里分开保存，所以这里同时有两组状态。
export type SessionInfo = {
  authenticated: boolean
  username: string
  role: Role | ''
  adminLoggedIn: boolean
  adminUsername: string
}

// 后台首页统计卡片的数据结构。
// 它对应 GET /api/admin/overview 的返回 data。
export type AdminOverview = {
  productCount: number
  categoryCount: number
  customerCount: number
  adminUsername: string
}

// 登录接口请求体。
// 前端 submitUserLogin / submitAdminLogin 会把表单 state JSON.stringify 成这个形状。
export type LoginBody = {
  username: string
  password: string
}

// 注册接口请求体。
// 当前页面还没有注册表单，但后端接口保留，方便你后续练习扩展页面。
export type RegisterBody = {
  username: string
  email: string
  password: string
  address: string
}

// 管理员创建/更新商品时提交的数据。
// id 和 categoryName 不由前端提交：id 由后端生成，categoryName 由 categoryId 查出来。
export type ProductInput = {
  name: string
  image: string
  price: number
  weight: number
  quantity: number
  description: string
  categoryId: number
}
