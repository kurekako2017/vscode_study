import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // React 插件负责 JSX 转换和开发时热更新。
  plugins: [react()],
  server: {
    // 监听所有网卡，方便容器或局域网访问这个教学客户端。
    host: '0.0.0.0',
    port: 5173,
  },
})
