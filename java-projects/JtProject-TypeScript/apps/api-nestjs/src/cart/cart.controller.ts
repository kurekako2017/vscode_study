import { Controller, Delete, Get, Param, ParseIntPipe, Post, Req } from '@nestjs/common'
import type { Request } from 'express'
import type { ApiResult, Product } from '../../../../packages/shared/src/index'
import { UserService } from '../user/user.service'
import { CartService } from './cart.service'

@Controller('cart')
export class CartController {
    constructor(
        private readonly cartService: CartService,
        private readonly userService: UserService
    ) { }

    @Get()
    getCart(@Req() request: Request): ApiResult<Product[]> {
        const user = this.userService.requireNormalUser(request)
        return { success: true, message: 'Cart loaded', data: this.cartService.getCartProducts(user.id) }
    }

    @Post('items/:productId')
    addCartItem(@Req() request: Request, @Param('productId', ParseIntPipe) productId: number): ApiResult<Product[]> {
        const user = this.userService.requireNormalUser(request)
        return { success: true, message: 'Product added to cart', data: this.cartService.addCartItem(user.id, productId) }
    }

    @Delete('items/:productId')
    removeCartItem(@Req() request: Request, @Param('productId', ParseIntPipe) productId: number): ApiResult<Product[]> {
        const user = this.userService.requireNormalUser(request)
        return { success: true, message: 'Product removed from cart', data: this.cartService.removeCartItem(user.id, productId) }
    }
}
