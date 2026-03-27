import type { Product } from '../types'

type Props = {
  cart: Product[]
  onRemove: (productId: number) => void
}

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
