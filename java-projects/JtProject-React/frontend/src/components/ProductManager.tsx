import type { FormEvent } from 'react'
import type { Category, Product } from '../types'

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
  categories: Category[]
  products: Product[]
  productForm: ProductForm
  setProductForm: (value: ProductForm) => void
  onSubmit: (event: FormEvent) => void
  onDelete: (id: number) => void
}

// 商品管理器把编辑表单和现有商品列表放在一起，方便后台直接维护库存数据。
export function ProductManager({ categories, products, productForm, setProductForm, onSubmit, onDelete }: Props) {
  return (
    <article className="panel">
      <h2>Product Editor</h2>
      <form onSubmit={onSubmit} className="form">
        <input value={productForm.name} onChange={(e) => setProductForm({ ...productForm, name: e.target.value })} placeholder="Product name" />
        <select value={productForm.categoryId} onChange={(e) => setProductForm({ ...productForm, categoryId: Number(e.target.value) })}>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>{category.name}</option>
          ))}
        </select>
        <input value={productForm.price} type="number" onChange={(e) => setProductForm({ ...productForm, price: Number(e.target.value) })} placeholder="Price" />
        <input value={productForm.quantity} type="number" onChange={(e) => setProductForm({ ...productForm, quantity: Number(e.target.value) })} placeholder="Quantity" />
        <input value={productForm.weight} type="number" onChange={(e) => setProductForm({ ...productForm, weight: Number(e.target.value) })} placeholder="Weight" />
        <input value={productForm.image} onChange={(e) => setProductForm({ ...productForm, image: e.target.value })} placeholder="Image URL" />
        <textarea value={productForm.description} onChange={(e) => setProductForm({ ...productForm, description: e.target.value })} placeholder="Description" />
        <button type="submit">{productForm.id ? 'Update Product' : 'Create Product'}</button>
      </form>
      <div className="stack">
        {products.map((product) => (
          <div key={product.id} className="listRow">
            <span>{product.name}</span>
            <div className="inlineActions">
              <button className="ghost" onClick={() => setProductForm(productFormFromProduct(product))}>Edit</button>
              <button className="ghost" onClick={() => onDelete(product.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}

function productFormFromProduct(product: Product): ProductForm {
  return {
    id: product.id,
    name: product.name,
    categoryId: product.categoryId,
    price: product.price,
    weight: product.weight,
    quantity: product.quantity,
    description: product.description,
    image: product.image
  }
}
