// 文件说明：
// 展示商品卡片网格的纯展示组件（无副作用），用于商品列表页和后台管理的预览。
// 学习点：组件应尽量纯粹，动作（如加入购物车）通过回调由父组件提供。
// 对应 JSP：uproduct.jsp（用户商品视图）、products.jsp（后台商品列表）
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
        // 对应 JSP 列表中 <c:forEach var="product"> 的每一行 <tr>
        // JSP 示例行：
        // <c:forEach var="product" items="${products}">
        //   <tr>
        //     <td>${product.name}</td>
        //     <td>${product.category.name}</td>
        //     <td>${product.price}</td>
        //     <td>${product.quantity}</td>
        //     <td>${product.description}</td>
        //   </tr>
        // </c:forEach>
        <div key={product.id} className="card">
          {/* 商品图片，若无图片使用占位图；JSP 中通常通过 ${product.image} 显示 */}
          <img src={product.image || 'https://placehold.co/320x160?text=Product'} alt={product.name} />
          {/* 商品名称与分类信息 */}
          <strong>{product.name}</strong>
          <span>{product.categoryName}</span>
          {/* 价格与库存信息，简单展示 */}
          <span>Price: {product.price}</span>
          <span>Stock: {product.quantity}</span>
          {/* 简短描述文本 */}
          <p>{product.description}</p>
          {/* 如果父组件提供了 onAddToCart 回调，则渲染加入购物车按钮 */}
          {onAddToCart ? <button onClick={() => onAddToCart(product.id)}>Add To Cart</button> : null}
        </div>
      ))}
    </div>
  )
}
