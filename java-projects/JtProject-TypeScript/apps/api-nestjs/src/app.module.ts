import { Module } from '@nestjs/common'
import { CartModule } from './cart/cart.module'
import { CategoryModule } from './category/category.module'
import { ProductModule } from './product/product.module'
import { UserModule } from './user/user.module'

// NestJS Module 相当于把多个组件汇总起来的“容器/配置单元”。
// Spring Boot 里对应 @Configuration + @ComponentScan 的组合思路，
// 只是 Nest 用 Module 显式声明依赖关系。
@Module({
    imports: [ProductModule, UserModule, CartModule, CategoryModule]
})
export class AppModule { }
