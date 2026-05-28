<script setup lang="ts">
// 全局布局只负责页面外壳、导航和退出按钮，不关心具体页面内容。
defineProps<{
  authenticated: boolean
  adminLoggedIn: boolean
}>()

defineEmits<{
  userLogout: []
  adminLogout: []
}>()
</script>

<template>
  <main class="page">
    <section class="masthead compact">
      <div>
        <p class="tag">JtProject Vue Edition</p>
        <h1>Spring Boot + Vue 多页面结构</h1>
      </div>
      <nav class="topnav">
        <RouterLink to="/login">用户登录</RouterLink>
        <RouterLink to="/products">商品页</RouterLink>
        <RouterLink to="/cart">购物车</RouterLink>
        <RouterLink to="/admin/login">管理登录</RouterLink>
        <RouterLink to="/admin/dashboard">管理后台</RouterLink>
        <button v-if="authenticated" @click="$emit('userLogout')">退出用户</button>
        <button v-if="adminLoggedIn" @click="$emit('adminLogout')">退出管理</button>
      </nav>
    </section>
    <slot />
  </main>
</template>
