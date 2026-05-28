import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

// 应用入口只负责创建 Vue 应用、挂载路由和引入全局样式，具体页面逻辑都下放到 App 与子页面。
createApp(App).use(router).mount('#app')
