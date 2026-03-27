import type { ApiResult } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8084/api'

export async function api<T>(path: string, init?: RequestInit) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  })
  const result = (await response.json()) as ApiResult<T>
  if (!response.ok || !result.success) {
    throw new Error(result.message || 'Request failed')
  }
  return result
}
