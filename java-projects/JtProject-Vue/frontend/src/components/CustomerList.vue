<script setup lang="ts">
import type { User } from '../types'

defineProps<{
  customers: User[]
}>()
</script>

<template>
  <article class="panel">
    <h2>Customers</h2>
    <div class="stack">
      <div v-for="customer in customers" :key="customer.id" class="list-row">
        <div>
          <strong>{{ customer.username }}</strong>
          <p>{{ customer.email }} / {{ customer.role }}</p>
        </div>
        <span>{{ customer.address }}</span>
      </div>
    </div>
  </article>
</template>
