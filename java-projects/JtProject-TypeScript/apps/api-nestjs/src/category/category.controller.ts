import { Controller, Get } from '@nestjs/common'
import type { ApiResult, Category } from '../../../../packages/shared/src/index'
import { CategoryService } from './category.service'

@Controller('categories')
export class CategoryController {
    constructor(private readonly categoryService: CategoryService) { }

    @Get()
    getAll(): ApiResult<Category[]> {
        return { success: true, message: 'Categories loaded', data: this.categoryService.findAll() }
    }
}
