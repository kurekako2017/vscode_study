<script setup lang="ts">
import PageHeader from '../components/PageHeader.vue'
import CartList from '../components/CartList.vue'
import { useAppStore } from '../composables/useAppStore'

const { removeFromCart, store } = useAppStore()
</script>

<template>
  <section class="page-section">
    <article class="panel">
      <PageHeader
        eyebrow="Cart"
        title="购物车页"
        subtitle="对应原项目里的 `cart.jsp`。"
        :message="store.message"
        :meta="`User: ${store.session.authenticated ? store.session.username : 'guest'}`"
      />
      <p v-if="store.cart.length === 0" class="muted">购物车为空，先去商品页添加商品。</p>
      <CartList :cart="store.cart" @remove="removeFromCart" />
    </article>
  </section>
</template>
