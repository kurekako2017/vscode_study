import { defineConfig } from 'vite'

// 纯 TypeScript 版本不使用 React/Vue/Next 插件，只保留 Vite 开发服务器。
export default defineConfig({
  server: {
    port: 5177
  }
})
