import { PageHeader } from '../components/PageHeader'
import { CartList } from '../components/CartList'
import type { Product, Session } from '../types'

type Props = {
  session: Session
  cart: Product[]
  message: string
  onRemoveFromCart: (productId: number) => void
}

// 购物车页面只负责展示当前会话的商品列表和移除操作。
export function CartView({ session, cart, message, onRemoveFromCart }: Props) {
  return (
    <section className="pageSection">
      <article className="panel">
        <PageHeader
          eyebrow="Cart"
          title="购物车页"
          subtitle="对应原项目里的 `cart.jsp`。"
          message={message}
          meta={`User: ${session.authenticated ? session.username : 'guest'}`}
        />
        {cart.length === 0 ? <p className="muted">购物车为空，先去商品页添加商品。</p> : null}
        <CartList cart={cart} onRemove={onRemoveFromCart} />
      </article>
    </section>
  )
}
