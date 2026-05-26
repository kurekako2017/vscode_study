import type { FormEvent } from 'react'
import type { Category, Product } from '../types'

// 文件说明：
// 后台商品管理表单，包含新增/编辑商品的输入项和提交逻辑（由父组件处理）。
// 学习点：如何用 `productForm` 与 `setProductForm` 构建受控表单并回传给父组件。
// 对应 JSP：products.jsp（列表）、productsAdd.jsp（添加表单）、productsUpdate.jsp（更新表单）
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
            {/* 分类选择：受控 select，值为 categoryId（number）
                对应 productsAdd.jsp / productsUpdate.jsp 中的 <select name="categoryid">，示例：
                <select name="categoryid">
                  <c:forEach var="category" items="${categories}">
                    <option value="${category.id}">${category.name}</option>
                  </c:forEach>
                </select>
            */}
            <select value={productForm.categoryId} onChange={(e) => setProductForm({ ...productForm, categoryId: Number(e.target.value) })}>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
            {/* 价格、数量、重量采用 number 输入，需注意转换为 Number 类型 */}
            {/* 对应 JSP 表单字段 name="price"（示例： <input type="number" name="price">） */}
            <input value={productForm.price} type="number" onChange={(e) => setProductForm({ ...productForm, price: Number(e.target.value) })} placeholder="Price" />
            {/* 对应 JSP 表单字段 name="quantity"（示例： <input type="number" name="quantity">） */}
            <input value={productForm.quantity} type="number" onChange={(e) => setProductForm({ ...productForm, quantity: Number(e.target.value) })} placeholder="Quantity" />
            {/* 对应 JSP 表单字段 name="weight"（示例： <input type="number" name="weight">） */}
            <input value={productForm.weight} type="number" onChange={(e) => setProductForm({ ...productForm, weight: Number(e.target.value) })} placeholder="Weight" />
            {/* 图片 URL 与描述字段 */}
            {/* 对应 JSP name="productImage"（示例： <input name="productImage">） */}
            <input value={productForm.image} onChange={(e) => setProductForm({ ...productForm, image: e.target.value })} placeholder="Image URL" />
            {/* 对应 JSP name="description"（textarea，示例： <textarea name="description">） */}
            <textarea value={productForm.description} onChange={(e) => setProductForm({ ...productForm, description: e.target.value })} placeholder="Description" />
            {/* 提交按钮文本根据是否为编辑模式改变 */}
            <button type="submit">{productForm.id ? 'Update Product' : 'Create Product'}</button>
      </form>
      <div className="stack">
        {products.map((product) => (
          <div key={product.id} className="listRow">
            {/* 列表中展示商品名称，编辑/删除操作由按钮触发 */}
            <span>{product.name}</span>
            <div className="inlineActions">
              {/* Edit：把选中商品的属性填充到编辑表单中 */}
              <button className="ghost" onClick={() => setProductForm(productFormFromProduct(product))}>Edit</button>
              {/* Delete：调用父组件传入的删除回调 */}
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
