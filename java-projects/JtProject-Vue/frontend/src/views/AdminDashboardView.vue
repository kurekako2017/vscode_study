<script setup lang="ts">
import CategoryManager from '../components/CategoryManager.vue'
import CustomerList from '../components/CustomerList.vue'
import PageHeader from '../components/PageHeader.vue'
import ProductManager from '../components/ProductManager.vue'
import ProfileEditor from '../components/ProfileEditor.vue'
import { useAppStore } from '../composables/useAppStore'

const { deleteCategory, deleteProduct, fillCategoryForm, fillProductForm, saveCategory, saveProduct, saveProfile, store } = useAppStore()
</script>

<template>
  <section class="page-section">
    <article class="panel">
      <PageHeader
        eyebrow="Admin Dashboard"
        title="管理后台页"
        subtitle="对应原项目里的 `adminHome.jsp`、`categories.jsp`、`products.jsp`、`displayCustomers.jsp`、`updateProfile.jsp`。"
        :message="store.message"
        :meta="store.overview?.adminUsername"
      />
      <div v-if="store.overview" class="stats">
        <span>{{ store.overview.categoryCount }} categories</span>
        <span>{{ store.overview.productCount }} products</span>
        <span>{{ store.overview.customerCount }} customers</span>
      </div>
    </article>

    <section class="board wide">
      <CategoryManager
        :categories="store.categories"
        :category-form="store.categoryForm"
        @submit="saveCategory"
        @edit="fillCategoryForm"
        @delete="deleteCategory"
      />
      <ProductManager
        :categories="store.categories"
        :products="store.products"
        :product-form="store.productForm"
        @submit="saveProduct"
        @edit="fillProductForm"
        @delete="deleteProduct"
      />
    </section>

    <section class="board wide">
      <CustomerList :customers="store.customers" />
      <ProfileEditor :profile-form="store.profileForm" @submit="saveProfile" />
    </section>
  </section>
</template>
