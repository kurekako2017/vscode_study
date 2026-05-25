import type { Product } from '../types'

type Props = {
  products: Product[]
  onAddToCart?: (productId: number) => void
}

// 商品网格负责纯展示，也可以在需要时追加“加入购物车”按钮。
export function ProductGrid({ products, onAddToCart }: Props) {
  return (
    <div className="cards">
      {products.map((product) => (
        <div key={product.id} className="card">
          <img src={product.image || 'https://placehold.co/320x160?text=Product'} alt={product.name} />
          <strong>{product.name}</strong>
          <span>{product.categoryName}</span>
          <span>Price: {product.price}</span>
          <span>Stock: {product.quantity}</span>
          <p>{product.description}</p>
          {onAddToCart ? <button onClick={() => onAddToCart(product.id)}>Add To Cart</button> : null}
        </div>
      ))}
    </div>
  )
}
