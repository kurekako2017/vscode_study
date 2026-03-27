<script setup lang="ts">
const props = defineProps<{
  profileForm: { username: string; email: string; password: string; address: string }
}>()

defineEmits<{
  submit: []
}>()
</script>

<template>
  <article class="panel">
    <h2>Admin Profile</h2>
    <div class="stack">
      <input v-model="props.profileForm.username" placeholder="Username" />
      <input v-model="props.profileForm.email" placeholder="Email" />
      <input v-model="props.profileForm.password" placeholder="Password" />
      <input v-model="props.profileForm.address" placeholder="Address" />
      <button @click="$emit('submit')">Update Profile</button>
    </div>
  </article>
</template>
