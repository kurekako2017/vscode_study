import type { ApiResult } from './types'

// NEXT_PUBLIC_ 前缀表示这个环境变量可以暴露给浏览器端代码。
// 如果没有配置 .env.local，就默认调用本项目 Spring Boot 后端的 8086 端口。
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8086/api'

// 统一 API 请求函数。
// T 是调用方传入的返回数据类型，例如 api<Product[]>('/products')。
// 这样 response.data 在页面里会自动拥有 Product[] 的类型提示。
export async function api<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  // credentials: 'include' 会让浏览器带上 JSESSIONID 等 cookie。
  // 本项目的登录状态存在 Spring Session 中，所以登录、购物车、后台接口都需要它。
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  })

  // 后端统一返回 { success, message, data }，这里先按 ApiResult<T> 解析。
  const data = (await response.json()) as ApiResult<T>

  // 统一在 API 层把错误转成异常，页面只需要在 try/catch 里显示 message。
  if (!response.ok || !data.success) {
    throw new Error(data.message || 'Request failed')
  }
  return data
}
