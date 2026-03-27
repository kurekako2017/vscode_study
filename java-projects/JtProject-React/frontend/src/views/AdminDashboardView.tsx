import type { FormEvent } from 'react'
import { CategoryManager } from '../components/CategoryManager'
import { CustomerList } from '../components/CustomerList'
import { PageHeader } from '../components/PageHeader'
import { ProductManager } from '../components/ProductManager'
import { ProfileEditor } from '../components/ProfileEditor'
import type { Category, Overview, Product, User } from '../types'

type ProductForm = {
  id: number
  name: string
  categoryId: number
  price: number
  weight: number
  quantity: number
  description: string
  image: string
}

type Props = {
  message: string
  overview: Overview | null
  categories: Category[]
  products: Product[]
  customers: User[]
  profileForm: { username: string; email: string; password: string; address: string }
  categoryForm: { id: number; name: string }
  productForm: ProductForm
  setCategoryForm: (value: { id: number; name: string }) => void
  setProductForm: (value: ProductForm) => void
  setProfileForm: (value: { username: string; email: string; password: string; address: string }) => void
  onSubmitCategory: (event: FormEvent) => void
  onDeleteCategory: (id: number) => void
  onSubmitProduct: (event: FormEvent) => void
  onDeleteProduct: (id: number) => void
  onSubmitProfile: (event: FormEvent) => void
}

export function AdminDashboardView(props: Props) {
  const { message, overview } = props

  return (
    <section className="pageSection">
      <article className="panel">
        <PageHeader
          eyebrow="Admin Dashboard"
          title="管理后台页"
          subtitle="对应原项目里的 `adminHome.jsp`、`categories.jsp`、`products.jsp`、`displayCustomers.jsp`、`updateProfile.jsp`。"
          message={message}
          meta={overview?.adminUsername}
        />
        {overview ? (
          <div className="chips">
            <span>{overview.categoryCount} categories</span>
            <span>{overview.productCount} products</span>
            <span>{overview.customerCount} customers</span>
          </div>
        ) : null}
      </article>

      <section className="grid wide">
        <CategoryManager
          categories={props.categories}
          categoryForm={props.categoryForm}
          setCategoryForm={props.setCategoryForm}
          onSubmit={props.onSubmitCategory}
          onDelete={props.onDeleteCategory}
        />
        <ProductManager
          categories={props.categories}
          products={props.products}
          productForm={props.productForm}
          setProductForm={props.setProductForm}
          onSubmit={props.onSubmitProduct}
          onDelete={props.onDeleteProduct}
        />
      </section>

      <section className="grid wide">
        <CustomerList customers={props.customers} />
        <ProfileEditor profileForm={props.profileForm} setProfileForm={props.setProfileForm} onSubmit={props.onSubmitProfile} />
      </section>
    </section>
  )
}
