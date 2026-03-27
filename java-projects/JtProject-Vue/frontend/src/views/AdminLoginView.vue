<script setup lang="ts">
import { useRouter } from 'vue-router'
import AdminAuthForm from '../components/AdminAuthForm.vue'
import { useAppStore } from '../composables/useAppStore'

const router = useRouter()
const { loginAdmin, store } = useAppStore()

async function submitAdminLogin() {
  await loginAdmin()
  router.push('/admin/dashboard')
}
</script>

<template>
  <section class="page-section">
    <article class="panel auth-panel narrow">
      <p class="tag">Admin Login</p>
      <h1>管理员登录页</h1>
      <p class="lead">对应原项目里的 `adminlogin.jsp`。</p>
      <AdminAuthForm :message="store.message" :admin-login="store.adminLogin" @login="submitAdminLogin" />
    </article>
  </section>
</template>
