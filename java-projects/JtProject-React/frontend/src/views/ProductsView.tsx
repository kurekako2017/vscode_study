import { PageHeader } from '../components/PageHeader'
import { ProductGrid } from '../components/ProductGrid'
import type { Product, Session } from '../types'

type Props = {
  session: Session
  products: Product[]
  message: string
  onAddToCart: (productId: number) => void
}

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
