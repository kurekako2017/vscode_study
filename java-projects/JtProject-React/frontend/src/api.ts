import type { ApiResult } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8083/api'

// 统一的 API 请求封装，负责补齐 JSON 头、携带 cookie 并处理后端错误返回。
export async function api<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  })
  const data = (await response.json()) as ApiResult<T>
  if (!response.ok || !data.success) {
    throw new Error(data.message || 'Request failed')
  }
  return data
}
