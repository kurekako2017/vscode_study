import { Injectable, NotFoundException } from '@nestjs/common'
import type { Product, ProductInput } from '../../../../packages/shared/src/index'
import { categories as seedCategories, products as seedProducts } from '../../../api/src/data/seed'

// @Injectable() 表示这是一个可被 Nest 注入的服务。
// Express 里直接在 server.ts 调用 Store；NestJS 则把数据访问逻辑封装进 Service。
// Spring Boot 对应的概念是 @Service。
@Injectable()
export class ProductService {
    private readonly categories = structuredClone(seedCategories)
    private products: Product[] = structuredClone(seedProducts)

    findAll() {
        return this.products
    }

    findOne(id: number) {
        const product = this.products.find((item) => item.id === id)
        if (!product) {
            throw new NotFoundException(`Product with id ${id} not found`)
        }
        return product
    }

    create(input: ProductInput) {
        const product = this.toProduct(input, this.nextId(this.products))
        this.products.push(product)
        return product
    }

    update(id: number, input: ProductInput) {
        const index = this.products.findIndex((item) => item.id === id)
        if (index < 0) {
            throw new NotFoundException(`Product with id ${id} not found`)
        }

        const product = this.toProduct(input, id)
        this.products[index] = product
        return product
    }

    remove(id: number) {
        const index = this.products.findIndex((item) => item.id === id)
        if (index < 0) {
            throw new NotFoundException(`Product with id ${id} not found`)
        }

        const [deleted] = this.products.splice(index, 1)
        return deleted
    }

    private toProduct(input: ProductInput, id: number): Product {
        const category = this.categories.find((item) => item.id === input.categoryId)
        return {
            id,
            ...input,
            categoryName: category?.name ?? 'Uncategorized'
        }
    }

    private nextId(items: Array<{ id: number }>) {
        return Math.max(0, ...items.map((item) => item.id)) + 1
    }
}
