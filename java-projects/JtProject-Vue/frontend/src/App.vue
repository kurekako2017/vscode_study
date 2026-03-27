<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import AppLayout from './layouts/AppLayout.vue'
import { useAppStore } from './composables/useAppStore'

const router = useRouter()
const { bootstrap, logoutAdmin, logoutUser, store } = useAppStore()

async function init() {
  try {
    await bootstrap()
  } catch (error) {
    store.message = (error as Error).message
  }
}

async function handleUserLogout() {
  await logoutUser()
  router.push('/login')
}

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
