import { Body, Controller, Delete, Get, Param, ParseIntPipe, Post, Put, Req, Res, UnauthorizedException } from '@nestjs/common'
import type { Request, Response } from 'express'
import type { ApiResult, Product, ProductInput } from '../../../../packages/shared/src/index'
import { UserService } from '../user/user.service'
import { CreateProductDto } from './dto/create-product.dto'
import { UpdateProductDto } from './dto/update-product.dto'
import { ProductService } from './product.service'

// @Controller('products') 这种写法表示路由前缀是 /products。
// Express 里是 app.get('/api/products')，NestJS 里典型写法会是 @Controller('products') + app.setGlobalPrefix('api')。
// 所以最终 URL 会是 /api/products。
@Controller('products')
export class ProductController {
    constructor(private readonly productService: ProductService) { }

    @Get()
    getAll(): ApiResult<Product[]> {
        return { success: true, message: 'Products loaded', data: this.productService.findAll() }
    }

    @Get(':id')
    getOne(@Param('id', ParseIntPipe) id: number): ApiResult<Product> {
        return { success: true, message: 'Product loaded', data: this.productService.findOne(id) }
    }
}

@Controller('admin/products')
export class AdminProductController {
    constructor(
        private readonly productService: ProductService,
        private readonly userService: UserService
    ) { }

    @Get()
    getAll(@Req() request: Request): ApiResult<Product[]> {
        this.userService.requireAdmin(request)
        return { success: true, message: 'Products loaded', data: this.productService.findAll() }
    }

    @Post()
    create(
        @Req() request: Request,
        @Body() body: CreateProductDto
    ): ApiResult<Product> {
        this.userService.requireAdmin(request)

        const input: ProductInput = {
            name: body.name,
            image: body.image,
            price: body.price,
            weight: body.weight,
            quantity: body.quantity,
            description: body.description,
            categoryId: body.categoryId
        }

        return { success: true, message: 'Product created', data: this.productService.create(input) }
    }

    @Put(':id')
    update(
        @Req() request: Request,
        @Param('id', ParseIntPipe) id: number,
        @Body() body: UpdateProductDto
    ): ApiResult<Product> {
        this.userService.requireAdmin(request)

        const current = this.productService.findOne(id)
        const input: ProductInput = {
            name: body.name ?? current.name,
            image: body.image ?? current.image,
            price: body.price ?? current.price,
            weight: body.weight ?? current.weight,
            quantity: body.quantity ?? current.quantity,
            description: body.description ?? current.description,
            categoryId: body.categoryId ?? current.categoryId
        }

        return { success: true, message: 'Product updated', data: this.productService.update(id, input) }
    }

    @Delete(':id')
    delete(@Req() request: Request, @Param('id', ParseIntPipe) id: number): ApiResult<Product> {
        this.userService.requireAdmin(request)
        return { success: true, message: 'Product deleted', data: this.productService.remove(id) }
    }
}
