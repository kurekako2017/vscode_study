// 这个文件只放 TypeScript 类型定义。
// 好处是：页面组件、API 封装、业务函数都可以复用同一套数据形状，避免到处写 any。

// ApiResult<T> 使用泛型 T 表示 data 的真实类型。
// 例如 api<Product[]>('/products') 返回的 data 就会被 TypeScript 识别为 Product[]。
export type ApiResult<T> = {
  success: boolean
  message: string
  data: T
}

// SessionInfo 对应 Spring Boot /api/session 返回的登录状态。
// 前端页面通过这个类型知道哪些字段一定存在。
export type SessionInfo = {
  authenticated: boolean
  username: string
  role: string
  adminLoggedIn: boolean
  adminUsername: string
}

// Product 对应后端 ApiController.productMaps() 组装出来的商品 JSON。
// 字段命名保持和后端返回一致，这样前端不需要再做二次转换。
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

// Category 保留给分类页面或后台维护页面继续扩展。
export type Category = {
  id: number
  name: string
}

// AdminOverview 对应 /api/admin/overview，用于后台统计卡片。
export type AdminOverview = {
  categoryCount: number
  productCount: number
  customerCount: number
  adminUsername: string
}
