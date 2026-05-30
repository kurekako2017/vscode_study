import type { ApiResult } from '../../../packages/shared/src/index'

// 纯 TypeScript 版 API 地址。
// VITE_ 前缀的变量可以在浏览器端通过 import.meta.env 读取。
//
// 如果你以后把后端端口改成 9000，可以在 .env.local 中写：
// VITE_API_BASE_URL=http://localhost:9000/api
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8090/api'

// 前端统一请求函数。
// T 由调用方指定，例如 api<Product[]>('/products')，返回值会自动拥有 Product[] 类型。
export async function api<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  // fetch 的第一个参数是完整 URL，第二个参数是请求配置。
  // init 允许调用方传 method/body 等配置，例如 POST 登录或 DELETE 删除购物车。
  const response = await fetch(`${API_BASE}${path}`, {
    // credentials: 'include' 是登录能工作的关键：
    // 后端通过 cookie 识别用户，如果不带 cookie，购物车和后台接口都会认为未登录。
    credentials: 'include',

    // 默认按 JSON 发送；调用方也可以通过 init.headers 覆盖或追加 header。
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  })

  // 这里把 JSON 断言成 ApiResult<T>。
  // TypeScript 只能在编译期检查类型，运行时仍然要相信后端返回符合约定。
  const data = (await response.json()) as ApiResult<T>

  // 后端错误和业务失败统一转成 Error。
  // 页面组件只需要 catch Error 并显示 message。
  if (!response.ok || !data.success) {
    throw new Error(data.message || 'Request failed')
  }

  return data
}
