<script setup lang="ts">
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
