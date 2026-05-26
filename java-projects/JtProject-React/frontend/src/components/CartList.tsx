// 文件说明：
// 购物车项列表组件，展示商品及移除按钮，动作通过 `onRemove` 回调上抛。
// 学习点：演示如何把事件回调传入子组件并携带参数（如 productId）。
// 对应 JSP：cartproduct.jsp（购物车项局部模板）
import type { Product } from '../types'

type Props = {
  cart: Product[]
  onRemove: (productId: number) => void
}

// 购物车列表只展示当前条目和删除入口，业务操作由上层回调处理。
export function CartList({ cart, onRemove }: Props) {
  return (
    <div className="stack">
      {cart.map((product, index) => (
        <div key={`${product.id}-${index}`} className="listRow">
          <div>
            {/* 对应 cart.jsp 中表格行的示例片段：
                <c:forEach var="product" items="${products}">
                  <tr>
                    <td>${product.name}</td>
                    <td>${product.category.name}</td>
                    <td>${product.price}</td>
                    <td>${product.description}</td>
                    <td>
                      <form action="/user/cart/delete" method="get">
                        <input type="hidden" name="id" value="${product.id}">
                        <button type="submit">Delete</button>
                      </form>
                    </td>
                  </tr>
                </c:forEach>
            */}
            <strong>{product.name}</strong>
            <p>{product.categoryName}</p>
          </div>
          {/* 移除按钮：对应 cart.jsp 中的删除表单（hidden id + submit）
              React 这里简化为按钮回调，父组件会调用 /api/cart/items/{id} 的删除接口 */}
          <button className="ghost" onClick={() => onRemove(product.id)}>Remove</button>
        </div>
      ))}
    </div>
  )
}
