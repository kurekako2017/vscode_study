<script setup lang="ts">
const props = defineProps<{
  message: string
  userLogin: { username: string; password: string }
  registerForm: { username: string; email: string; password: string; address: string }
}>()

defineEmits<{
  login: []
  register: []
}>()
</script>

<template>
  <p class="banner">{{ props.message }}</p>
  <div class="split">
    <div class="stack">
      <h2>Login</h2>
      <input v-model="props.userLogin.username" placeholder="Username" />
      <input v-model="props.userLogin.password" type="password" placeholder="Password" />
      <button @click="$emit('login')">登录</button>
    </div>
    <div class="stack">
      <h2>Register</h2>
      <input v-model="props.registerForm.username" placeholder="New username" />
      <input v-model="props.registerForm.email" placeholder="Email" />
      <input v-model="props.registerForm.password" type="password" placeholder="Password" />
      <input v-model="props.registerForm.address" placeholder="Address" />
      <button @click="$emit('register')">注册并登录</button>
    </div>
  </div>
</template>
