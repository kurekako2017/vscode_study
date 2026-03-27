import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboardView from './views/AdminDashboardView.vue'
import AdminLoginView from './views/AdminLoginView.vue'
import CartView from './views/CartView.vue'
import ProductsView from './views/ProductsView.vue'
import UserLoginView from './views/UserLoginView.vue'
import { useAppStore } from './composables/useAppStore'

const { store } = useAppStore()

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: UserLoginView },
    { path: '/products', component: ProductsView },
    {
      path: '/cart',
      component: CartView,
      beforeEnter: () => (store.session.authenticated ? true : '/login')
    },
    { path: '/admin/login', component: AdminLoginView },
    {
      path: '/admin/dashboard',
      component: AdminDashboardView,
      beforeEnter: () => (store.session.adminLoggedIn ? true : '/admin/login')
    }
  ]
})

export default router
