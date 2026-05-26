import type { FormEvent } from 'react'
// 文件说明：
// 分类管理组件：用于在管理后台创建/删除分类并展示分类列表。
// 学习点：受控表单、回调与列表渲染的结合使用。
// 对应 JSP：categories.jsp
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
           {/* 对应 categories.jsp 中 modal 的输入片段（示例）：
               <form action="categories" method="post">
                 <input type="text" name="categoryname">
               </form>
           */}
           <input value={categoryForm.name} onChange={(e) => setCategoryForm({ ...categoryForm, name: e.target.value })} placeholder="Category name" />
        <button type="submit">{categoryForm.id ? 'Update Category' : 'Create Category'}</button>
      </form>
      <div className="stack">
        {categories.map((category) => (
          <div key={category.id} className="listRow">
            <span>{category.name}</span>
            <div className="inlineActions">
                 {/* 对应 categories.jsp 表格中的删除表单（示例）：
                     <form action="categories/delete" method="get">
                       <input type="hidden" name="id" value="${category.id}">
                       <input type="submit" value="Delete">
                     </form>
                     React 这里用 onDelete 回调触发后端删除接口 */}
                 <button className="ghost" onClick={() => onDelete(category.id)}>Delete</button>
                 {/* 对应 categories.jsp 中 update 模态框的填充（categoryid / categoryname）示例 */}
                 <button className="ghost" onClick={() => setCategoryForm({ id: category.id, name: category.name })}>Edit</button>
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}
