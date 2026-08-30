import 'reflect-metadata'
import { ValidationPipe } from '@nestjs/common'
import { NestFactory } from '@nestjs/core'
import cookieParser from 'cookie-parser'
import { AppModule } from './app.module'
import { HttpExceptionFilter } from './common/filters/http-exception.filter'

async function bootstrap() {
    const app = await NestFactory.create(AppModule)

    app.use(cookieParser())
    app.setGlobalPrefix('api')

    // 统一异常处理：Express 里是手工 response.status()；
    // NestJS 通过全局 filter 把不同异常统一成 { success, message, data } 结构。
    app.useGlobalFilters(new HttpExceptionFilter())
    // 这里把 DTO 的校验规则应用到所有入参，统一处理 400 错误。
    app.useGlobalPipes(
        new ValidationPipe({
            whitelist: true,
            forbidNonWhitelisted: true,
            transform: true,
            transformOptions: { enableImplicitConversion: true }
        })
    )

    // 这里模拟与 Express 一样的跨域场景，方便 React 在本地切换后端地址。
    app.enableCors({
        origin: ['http://localhost:5175', 'http://127.0.0.1:5175'],
        credentials: true
    })

    const port = Number(process.env.NEST_PORT ?? 3002)
    await app.listen(port)
    console.log(`NestJS Product API: http://localhost:${port}/api`)
}

bootstrap()
