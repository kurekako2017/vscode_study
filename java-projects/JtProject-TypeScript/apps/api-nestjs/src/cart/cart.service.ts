import { Injectable, NotFoundException } from '@nestjs/common'
import type { Product } from '../../../../packages/shared/src/index'
import { products as seedProducts } from '../../../api/src/data/seed'

@Injectable()
export class CartService {
    private readonly products: Product[] = structuredClone(seedProducts)
    private readonly carts = new Map<number, number[]>()

    getCartProducts(userId: number) {
        const productIds = this.carts.get(userId) ?? []
        return productIds.flatMap((id) => this.products.find((product) => product.id === id) ?? [])
    }

    addCartItem(userId: number, productId: number) {
        const current = this.carts.get(userId) ?? []
        this.carts.set(userId, [...current, productId])
        return this.getCartProducts(userId)
    }

    removeCartItem(userId: number, productId: number) {
        const current = this.carts.get(userId) ?? []
        const index = current.indexOf(productId)
        if (index >= 0) {
            current.splice(index, 1)
        }
        this.carts.set(userId, current)
        return this.getCartProducts(userId)
    }
}
