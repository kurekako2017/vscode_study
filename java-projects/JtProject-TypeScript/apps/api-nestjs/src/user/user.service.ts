import { Injectable, UnauthorizedException } from '@nestjs/common'
import type { Request } from 'express'
import type { ApiResult, LoginBody, RegisterBody, SessionInfo, User } from '../../../../packages/shared/src/index'
import { users as seedUsers } from '../../../api/src/data/seed'

const sessionCookieName = 'jt_ts_session'
const adminCookieName = 'jt_ts_admin'

@Injectable()
export class UserService {
    private readonly users: User[] = structuredClone(seedUsers)

    findUserByUsername(username: string) {
        return this.users.find((user) => user.username === username)
    }

    checkLogin(username: string, password: string) {
        return this.users.find((user) => user.username === username && user.password === password)
    }

    getUsers() {
        return this.users
    }

    registerUser(input: Omit<User, 'id' | 'role'>) {
        const user: User = {
            ...input,
            id: this.nextId(this.users),
            role: 'ROLE_NORMAL'
        }
        this.users.push(user)
        return user
    }

    requireNormalUser(request: Request) {
        const user = this.currentUser(request)
        if (!user || user.role !== 'ROLE_NORMAL') {
            throw new UnauthorizedException('Please login as a normal user first')
        }
        return user
    }

    requireAdmin(request: Request) {
        const username = this.currentAdminUsername(request)
        const user = username ? this.findUserByUsername(username) : undefined
        if (!user || user.role !== 'ROLE_ADMIN') {
            throw new UnauthorizedException('Please login as admin first')
        }
        return username
    }

    currentUser(request: Request) {
        const username = this.clean(request.cookies[sessionCookieName])
        return username ? this.findUserByUsername(username) : undefined
    }

    currentAdminUsername(request: Request) {
        return this.clean(request.cookies[adminCookieName])
    }

    sessionData(request: Request): SessionInfo {
        const user = this.currentUser(request)
        const adminUsername = this.currentAdminUsername(request)
        return {
            authenticated: Boolean(user),
            username: user?.username ?? '',
            role: user?.role ?? '',
            adminLoggedIn: Boolean(adminUsername),
            adminUsername
        }
    }

    sessionDataFor(user: User | null, adminUsername = ''): SessionInfo {
        return {
            authenticated: Boolean(user),
            username: user?.username ?? '',
            role: user?.role ?? '',
            adminLoggedIn: Boolean(adminUsername),
            adminUsername
        }
    }

    ok<T>(message: string, data: T): ApiResult<T> {
        return { success: true, message, data }
    }

    fail<T>(message: string): ApiResult<T | null> {
        return { success: false, message, data: null }
    }

    emptySession(): SessionInfo {
        return {
            authenticated: false,
            username: '',
            role: '',
            adminLoggedIn: false,
            adminUsername: ''
        }
    }

    cookieOptions() {
        return {
            httpOnly: true,
            sameSite: 'lax' as const,
            maxAge: 7 * 24 * 60 * 60 * 1000
        }
    }

    private clean(value: unknown) {
        return typeof value === 'string' ? value.trim() : ''
    }

    private nextId(items: Array<{ id: number }>) {
        return Math.max(0, ...items.map((item) => item.id)) + 1
    }
}
