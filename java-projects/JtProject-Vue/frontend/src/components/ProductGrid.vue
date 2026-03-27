<script setup lang="ts">
import type { Product } from '../types'

defineProps<{
  products: Product[]
}>()

defineEmits<{
  addToCart: [productId: number]
}>()
</script>

<template>
  <div class="cards">
    <div v-for="product in products" :key="product.id" class="card">
      <img :src="product.image || 'https://placehold.co/320x160?text=Product'" :alt="product.name" />
      <strong>{{ product.name }}</strong>
      <span>{{ product.categoryName }}</span>
      <span>Price: {{ product.price }}</span>
      <span>Stock: {{ product.quantity }}</span>
      <p>{{ product.description }}</p>
      <button @click="$emit('addToCart', product.id)">Add To Cart</button>
    </div>
  </div>
</template>
