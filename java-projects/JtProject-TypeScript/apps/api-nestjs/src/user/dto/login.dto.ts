import { IsNotEmpty, IsString } from 'class-validator'

// LoginDto 和 Express 的 LoginBody 一一对应，保证 URL、JSON 字段名和前端一致。
export class LoginDto {
    @IsString()
    @IsNotEmpty()
    username!: string

    @IsString()
    @IsNotEmpty()
    password!: string
}
