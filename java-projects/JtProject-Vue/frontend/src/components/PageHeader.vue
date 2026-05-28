<script setup lang="ts">
// 统一的页面标题区，复用在多个 view 中，减少重复模板。
defineProps<{
  eyebrow: string
  title: string
  subtitle: string
  message: string
  meta?: string
}>()
</script>

<template>
  <div class="page-header">
    <div>
      <p class="tag">{{ eyebrow }}</p>
      <h1>{{ title }}</h1>
      <p class="lead">{{ subtitle }}</p>
    </div>
    <div class="rail">
      <span>{{ message }}</span>
      <span v-if="meta">{{ meta }}</span>
    </div>
  </div>
</template>
