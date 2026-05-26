// 文件说明：
// 商品列表页：展示商品并提供“加入购物车”的入口。
// 学习点：
// - 视图组件保持纯展示职责，把逻辑（如添加到购物车）委托给父组件
// 对应 JSP：products.jsp（服务端渲染的商品列表页）、uproduct.jsp（用户商品视图）
import { PageHeader } from '../components/PageHeader'
import { ProductGrid } from '../components/ProductGrid'
import type { Product, Session } from '../types'

type Props = {
  session: Session
  products: Product[]
  message: string
  onAddToCart: (productId: number) => void
}

// 商品页承载浏览与加入购物车的主流程，保持视图尽量薄。
export function ProductsView({ session, products, message, onAddToCart }: Props) {
  return (
    <section className="pageSection">
      <article className="panel">
        <PageHeader
          eyebrow="Products"
          title="商品页"
          subtitle="对应原项目里的 `index.jsp` 和 `uproduct.jsp`。"
          message={message}
          meta={`User: ${session.authenticated ? session.username : 'guest'}`}
        />
        <ProductGrid products={products} onAddToCart={onAddToCart} />
      </article>
    </section>
  )
}
