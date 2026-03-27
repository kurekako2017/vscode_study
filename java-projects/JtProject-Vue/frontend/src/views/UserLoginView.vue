<script setup lang="ts">
import { useRouter } from 'vue-router'
import UserAuthForms from '../components/UserAuthForms.vue'
import { useAppStore } from '../composables/useAppStore'

const router = useRouter()
const { loginUser, registerUser, store } = useAppStore()

async function submitUserLogin() {
  await loginUser()
  router.push('/products')
}

async function submitRegister() {
  await registerUser()
  router.push('/products')
}
</script>

<template>
  <section class="page-section">
    <article class="panel auth-panel">
      <div>
        <p class="tag">User Login</p>
        <h1>用户登录页</h1>
        <p class="lead">对应原项目里的 `userLogin.jsp` 和 `register.jsp`。</p>
      </div>
      <UserAuthForms
        :message="store.message"
        :user-login="store.userLogin"
        :register-form="store.registerForm"
        @login="submitUserLogin"
        @register="submitRegister"
      />
    </article>
  </section>
</template>
