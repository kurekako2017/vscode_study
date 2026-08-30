import { BadRequestException, Body, ConflictException, Controller, Get, Post, Req, Res, UnauthorizedException } from '@nestjs/common'
import type { Request, Response } from 'express'
import type { AdminOverview, ApiResult, SessionInfo } from '../../../../packages/shared/src/index'
import { LoginDto } from './dto/login.dto'
import { RegisterDto } from './dto/register.dto'
import { UserService } from './user.service'

@Controller('session')
export class SessionController {
    constructor(private readonly userService: UserService) { }

    @Get()
    session(@Req() request: Request): ApiResult<SessionInfo> {
        return { success: true, message: 'Session loaded', data: this.userService.sessionData(request) }
    }
}

@Controller('auth')
export class UserController {
    constructor(private readonly userService: UserService) { }

    @Post('login')
    login(
        @Res({ passthrough: true }) response: Response,
        @Body() body: LoginDto
    ): ApiResult<SessionInfo> {
        const user = this.userService.checkLogin(body.username, body.password)
        if (!user || user.role !== 'ROLE_NORMAL') {
            throw new UnauthorizedException('Invalid user credentials')
        }

        response.cookie('jt_ts_session', user.username, this.userService.cookieOptions())
        return { success: true, message: 'User login successful', data: this.userService.sessionDataFor(user) }
    }

    @Post('register')
    register(
        @Res({ passthrough: true }) response: Response,
        @Body() body: RegisterDto
    ): ApiResult<SessionInfo> {
        const username = body.username.trim()
        const email = body.email.trim()
        const password = body.password.trim()
        const address = body.address.trim()

        if (!username || !email || !password) {
            throw new BadRequestException('Username, email and password are required')
        }
        if (this.userService.findUserByUsername(username)) {
            throw new ConflictException('Username already exists')
        }

        const user = this.userService.registerUser({ username, email, password, address })
        response.cookie('jt_ts_session', user.username, this.userService.cookieOptions())
        return { success: true, message: 'Registration successful', data: this.userService.sessionDataFor(user) }
    }

    @Post('logout')
    logout(@Res({ passthrough: true }) response: Response): ApiResult<SessionInfo> {
        response.clearCookie('jt_ts_session')
        return { success: true, message: 'User logout successful', data: this.userService.emptySession() }
    }
}

@Controller('admin')
export class AdminUserController {
    constructor(private readonly userService: UserService) { }

    @Post('login')
    login(
        @Res({ passthrough: true }) response: Response,
        @Body() body: LoginDto
    ): ApiResult<SessionInfo> {
        const user = this.userService.checkLogin(body.username, body.password)
        if (!user || user.role !== 'ROLE_ADMIN') {
            throw new UnauthorizedException('Invalid admin credentials')
        }

        response.cookie('jt_ts_admin', user.username, this.userService.cookieOptions())
        return {
            success: true,
            message: 'Admin login successful',
            data: this.userService.sessionDataFor(null, user.username)
        }
    }

    @Get('overview')
    overview(@Req() request: Request): ApiResult<AdminOverview> {
        const adminUsername = this.userService.requireAdmin(request)
        return {
            success: true,
            message: 'Admin overview loaded',
            data: {
                productCount: 0,
                categoryCount: 0,
                customerCount: 0,
                adminUsername
            }
        }
    }
}
