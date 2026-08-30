import { Module } from '@nestjs/common'
import { AdminUserController, SessionController, UserController } from './user.controller'
import { UserService } from './user.service'

// UserModule 负责认证、会话恢复和管理员权限。
// Express 里这些逻辑都在 server.ts 里手写；NestJS 则按模块拆分。
@Module({
    controllers: [SessionController, UserController, AdminUserController],
    providers: [UserService],
    exports: [UserService]
})
export class UserModule { }
