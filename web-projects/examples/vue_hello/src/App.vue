<template>
  <main class="page-shell">
    <section class="hero-card">
      <p class="eyebrow">Vue 3</p>
      <h1>Hello Vue!</h1>
      <p>这是一个 Vue 3 + Vite 最小示例，展示入口文件、单文件组件和样式分层。</p>
      <p class="lesson">{{ lesson }}</p>
    </section>
  </main>
</template>

<script setup>
const lesson = 'template + script setup + style'
</script>

<style scoped>
.lesson {
  display: inline-block;
  margin-top: 18px;
  color: #047857;
  font-size: 14px;
  font-weight: 700;
}
</style>
