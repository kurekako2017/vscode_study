<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import AppLayout from './layouts/AppLayout.vue'
import { useAppStore } from './composables/useAppStore'

const router = useRouter()
const { bootstrap, logoutAdmin, logoutUser, store } = useAppStore()

// 启动时先加载会话、商品和分类，后续页面再基于 store 渲染。
async function init() {
  try {
    await bootstrap()
  } catch (error) {
    store.message = (error as Error).message
  }
}

// 用户退出后回到登录页。
async function handleUserLogout() {
  await logoutUser()
  router.push('/login')
}

// 管理员退出后回到管理员登录页。
async function handleAdminLogout() {
  await logoutAdmin()
  router.push('/admin/login')
}

onMounted(() => {
  void init()
})
</script>

<template>
  <AppLayout
    :authenticated="store.session.authenticated"
    :admin-logged-in="store.session.adminLoggedIn"
    @user-logout="handleUserLogout"
    @admin-logout="handleAdminLogout"
  >
    <RouterView />
  </AppLayout>
</template>
