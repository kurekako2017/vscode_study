import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // Vite 插件负责处理 JSX、Fast Refresh 等 React 开发体验。
  plugins: [react()],
  // 测试环境用 jsdom，这样组件测试可以像在浏览器里一样访问 DOM。
  test: {
    environment: 'jsdom',
    // 这里会先执行测试初始化文件，补齐 jest-dom 断言。
    setupFiles: './src/test/setup.js',
  },
})
