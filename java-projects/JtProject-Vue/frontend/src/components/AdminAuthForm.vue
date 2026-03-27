<script setup lang="ts">
const props = defineProps<{
  message: string
  adminLogin: { username: string; password: string }
}>()

defineEmits<{
  login: []
}>()
</script>

<template>
  <p class="banner">{{ props.message }}</p>
  <div class="stack">
    <input v-model="props.adminLogin.username" placeholder="Admin username" />
    <input v-model="props.adminLogin.password" type="password" placeholder="Admin password" />
    <button @click="$emit('login')">管理员登录</button>
  </div>
</template>
