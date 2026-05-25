import type { FormEvent } from 'react'
import type { Category } from '../types'

type Props = {
  categories: Category[]
  categoryForm: { id: number; name: string }
  setCategoryForm: (value: { id: number; name: string }) => void
  onSubmit: (event: FormEvent) => void
  onDelete: (id: number) => void
}

// 分类管理器负责创建、编辑和删除分类，表单与列表放在同一个面板里。
export function CategoryManager({ categories, categoryForm, setCategoryForm, onSubmit, onDelete }: Props) {
  return (
    <article className="panel">
      <h2>Categories</h2>
      <form onSubmit={onSubmit} className="form">
        <input value={categoryForm.name} onChange={(e) => setCategoryForm({ ...categoryForm, name: e.target.value })} placeholder="Category name" />
        <button type="submit">{categoryForm.id ? 'Update Category' : 'Create Category'}</button>
      </form>
      <div className="stack">
        {categories.map((category) => (
          <div key={category.id} className="listRow">
            <span>{category.name}</span>
            <div className="inlineActions">
              <button className="ghost" onClick={() => setCategoryForm(category)}>Edit</button>
              <button className="ghost" onClick={() => onDelete(category.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}
