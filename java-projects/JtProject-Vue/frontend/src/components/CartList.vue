<script setup lang="ts">
import type { Product } from '../types'

defineProps<{
  cart: Product[]
}>()

defineEmits<{
  remove: [productId: number]
}>()
</script>

<template>
  <div class="stack">
    <div v-for="(product, index) in cart" :key="`${product.id}-${index}`" class="list-row">
      <div>
        <strong>{{ product.name }}</strong>
        <p>{{ product.categoryName }}</p>
      </div>
      <button class="ghost" @click="$emit('remove', product.id)">Remove</button>
    </div>
  </div>
</template>
