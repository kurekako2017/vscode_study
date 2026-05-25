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
            <strong>{product.name}</strong>
            <p>{product.categoryName}</p>
          </div>
          <button className="ghost" onClick={() => onRemove(product.id)}>Remove</button>
        </div>
      ))}
    </div>
  )
}
