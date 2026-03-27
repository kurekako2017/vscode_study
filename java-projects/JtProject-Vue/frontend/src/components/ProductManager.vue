<script setup lang="ts">
import type { Category, Product } from '../types'

const props = defineProps<{
  categories: Category[]
  products: Product[]
  productForm: {
    id: number
    name: string
    categoryId: number
    price: number
    weight: number
    quantity: number
    description: string
    image: string
  }
}>()

defineEmits<{
  submit: []
  edit: [product: Product]
  delete: [id: number]
}>()
</script>

<template>
  <article class="panel">
    <h2>Product Studio</h2>
    <div class="stack">
      <input v-model="props.productForm.name" placeholder="Product name" />
      <select v-model.number="props.productForm.categoryId">
        <option v-for="category in props.categories" :key="category.id" :value="category.id">{{ category.name }}</option>
      </select>
      <input v-model.number="props.productForm.price" type="number" placeholder="Price" />
      <input v-model.number="props.productForm.quantity" type="number" placeholder="Quantity" />
      <input v-model.number="props.productForm.weight" type="number" placeholder="Weight" />
      <input v-model="props.productForm.image" placeholder="Image URL" />
      <textarea v-model="props.productForm.description" placeholder="Description" />
      <button @click="$emit('submit')">{{ props.productForm.id ? 'Update Product' : 'Create Product' }}</button>
    </div>
    <div class="stack">
      <div v-for="product in props.products" :key="product.id" class="list-row">
        <span>{{ product.name }}</span>
        <div class="actions">
          <button class="ghost" @click="$emit('edit', product)">Edit</button>
          <button class="ghost" @click="$emit('delete', product.id)">Delete</button>
        </div>
      </div>
    </div>
  </article>
</template>
