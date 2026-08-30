import {
    ArgumentsHost,
    Catch,
    ExceptionFilter,
    HttpException,
    HttpStatus,
    InternalServerErrorException
} from '@nestjs/common'
import type { Response } from 'express'

// 统一异常处理相当于 Spring Boot 的 @ControllerAdvice + @ExceptionHandler。
// 它让所有接口返回的结构更统一，方便前端统一解析。
@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
    catch(exception: unknown, host: ArgumentsHost) {
        const context = host.switchToHttp()
        const response = context.getResponse<Response>()

        const status =
            exception instanceof HttpException ? exception.getStatus() : HttpStatus.INTERNAL_SERVER_ERROR

        const message =
            exception instanceof HttpException ? this.extractMessage(exception) : 'Internal server error'

        response.status(status).json({
            success: false,
            message,
            data: null
        })
    }

    private extractMessage(exception: HttpException) {
        const response = exception.getResponse()
        if (typeof response === 'string') {
            return response
        }
        if (response && typeof response === 'object' && 'message' in response) {
            const message = response.message
            if (Array.isArray(message)) {
                return message.join('; ')
            }
            if (typeof message === 'string') {
                return message
            }
        }
        return exception.message
    }
}
