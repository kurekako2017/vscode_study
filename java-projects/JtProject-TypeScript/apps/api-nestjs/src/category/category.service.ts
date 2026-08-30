import { Injectable } from '@nestjs/common'
import type { Category } from '../../../../packages/shared/src/index'
import { categories as seedCategories } from '../../../api/src/data/seed'

@Injectable()
export class CategoryService {
    private readonly categories: Category[] = structuredClone(seedCategories)

    findAll() {
        return this.categories
    }
}
