// 前端请求地址配置。
// 默认情况下，开发环境直接访问本机 8000 端口的 FastAPI。
const DEFAULT_API_BASE_URL = "http://localhost:8000";

function stripTrailingSlash(value: string): string {
  // 统一去掉末尾斜杠，避免后面拼接路径时出现 //api/task 这种问题。
  return value.replace(/\/+$/, "");
}

function deriveWsBaseUrl(apiBaseUrl: string): string {
  // WebSocket 地址通常和 HTTP API 地址同源，只是协议从 http/https 变成 ws/wss。
  if (import.meta.env.VITE_WS_BASE_URL) {
    return stripTrailingSlash(import.meta.env.VITE_WS_BASE_URL);
  }

  if (apiBaseUrl.startsWith("https://")) {
    return apiBaseUrl.replace(/^https:\/\//, "wss://");
  }

  if (apiBaseUrl.startsWith("http://")) {
    return apiBaseUrl.replace(/^http:\/\//, "ws://");
  }

  return `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}`;
}

export const API_BASE_URL = stripTrailingSlash(
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
);

// 这个值会被 useDeepAgentSession 用来建立 /ws/{thread_id} 连接。
export const WS_BASE_URL = deriveWsBaseUrl(API_BASE_URL);
