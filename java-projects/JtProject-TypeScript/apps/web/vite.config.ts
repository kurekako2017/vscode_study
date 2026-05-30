import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Vite 是前端开发服务器和构建工具。
// 这里把端口固定为 5175，避免和 React/Vue/Next 学习项目冲突。
export default defineConfig({
  // root 指向当前 apps/web 目录。
  // 因为 npm run build 是从项目根目录执行的，如果不设置 root，Vite 会去根目录找 index.html。
  root: new URL('.', import.meta.url).pathname,

  // React 插件负责处理 TSX、Fast Refresh 等 React 开发体验。
  plugins: [react()],
  server: {
    port: 5175
  },
  preview: {
    port: 4175
  }
})
