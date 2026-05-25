import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite 配置保持尽量精简，只保留 React 插件和开发端口设置。
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  }
})
