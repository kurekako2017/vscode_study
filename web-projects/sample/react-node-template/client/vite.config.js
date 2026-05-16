// client/vite.config.js
// Vite 开发服务器配置（教学注释）
// 说明：
// - `server.port` 指定前端开发服务器端口（默认 3000）。
// - `proxy['/api']` 用于将前端对 `/api` 的请求代理到后端（避免 CORS），
//   开发时前端请求 `http://localhost:3000/api/hello` 将被转发到 `http://localhost:4000/api/hello`。
// - 如果后端运行在不同主机或端口，请修改 `target`。
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
