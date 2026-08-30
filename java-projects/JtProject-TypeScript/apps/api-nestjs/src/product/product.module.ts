import { Module } from '@nestjs/common'
import { UserModule } from '../user/user.module'
import { AdminProductController, ProductController } from './product.controller'
import { ProductService } from './product.service'

// NestJS 里的 Module 是“业务模块入口”，负责装配 Controller 和 Service。
// 在 Spring Boot 中，最接近的是组件扫描 + 配置类组织业务边界。
@Module({
    imports: [UserModule],
    controllers: [ProductController, AdminProductController],
    providers: [ProductService]
})
export class ProductModule { }
