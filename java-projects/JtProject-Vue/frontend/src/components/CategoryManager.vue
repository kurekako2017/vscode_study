<script setup lang="ts">
import type { Category } from '../types'

const props = defineProps<{
  categories: Category[]
  categoryForm: { id: number; name: string }
}>()

defineEmits<{
  submit: []
  edit: [category: Category]
  delete: [id: number]
}>()
</script>

<template>
  <article class="panel">
    <h2>Category Studio</h2>
    <div class="stack">
      <input v-model="props.categoryForm.name" placeholder="Category name" />
      <button @click="$emit('submit')">{{ props.categoryForm.id ? 'Update Category' : 'Create Category' }}</button>
    </div>
    <div class="stack">
      <div v-for="category in props.categories" :key="category.id" class="list-row">
        <span>{{ category.name }}</span>
        <div class="actions">
          <button class="ghost" @click="$emit('edit', category)">Edit</button>
          <button class="ghost" @click="$emit('delete', category.id)">Delete</button>
        </div>
      </div>
    </div>
  </article>
</template>
