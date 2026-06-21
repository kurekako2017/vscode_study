import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // 只需 React 插件；端口等开发参数沿用 Vite 默认值。
  plugins: [react()],
})
