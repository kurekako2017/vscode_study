<script setup lang="ts">
// 商品页负责把页面头部和商品网格组合起来，逻辑交给 store 和 service 层。
import PageHeader from '../components/PageHeader.vue'
import ProductGrid from '../components/ProductGrid.vue'
import { useAppStore } from '../composables/useAppStore'

const { addToCart, store } = useAppStore()
</script>

<template>
  <section class="page-section">
    <article class="panel">
      <PageHeader
        eyebrow="Products"
        title="商品页"
        subtitle="对应原项目里的 `index.jsp` 和 `uproduct.jsp`。"
        :message="store.message"
        :meta="`User: ${store.session.authenticated ? store.session.username : 'guest'}`"
      />
      <ProductGrid :products="store.products" @add-to-cart="addToCart" />
    </article>
  </section>
</template>
